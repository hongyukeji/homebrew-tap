"""Update each formula listed in tools.json to its tool's latest GitHub release.

Reads the release's SHA256SUMS (or checksums.txt) for the SHA256 and rewrites the formula's
url/version/sha256 lines. Prints the names of the formulae it changed (one per line).
Uses GITHUB_TOKEN when present (higher API rate limit); needs no other secrets.
"""
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get(url, accept="application/vnd.github+json"):
    req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": "hongyukeji-tap-sync"})
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def sync(tool):
    rel = json.loads(get(f"https://api.github.com/repos/{tool['repo']}/releases/latest"))
    version = rel["tag_name"].lstrip("v")
    asset = tool["asset"].format(version=version)
    assets = {a["name"]: a["browser_download_url"] for a in rel["assets"]}
    sums_name = next((n for n in ("SHA256SUMS", "checksums.txt") if n in assets), None)
    if asset not in assets or not sums_name:
        print(f"{tool['formula']}: release {rel['tag_name']} lacks {asset} or SHA256SUMS", file=sys.stderr)
        return False
    sums = dict(reversed(line.split()) for line in get(assets[sums_name], "*/*").decode().splitlines() if line.strip())
    sha = sums.get(asset)
    if not sha or not re.fullmatch(r"[0-9a-f]{64}", sha):
        print(f"{tool['formula']}: no valid SHA256 for {asset}", file=sys.stderr)
        return False
    path = os.path.join(ROOT, "Formula", f"{tool['formula']}.rb")
    old = open(path, encoding="utf-8").read()
    new = re.sub(r'^(\s*url ")[^"]+(")', rf'\g<1>{assets[asset]}\g<2>', old, count=1, flags=re.M)
    new = re.sub(r'^(\s*version ")[^"]+(")', rf'\g<1>{version}\g<2>', new, count=1, flags=re.M)
    new = re.sub(r'^(\s*sha256 ")[0-9a-f]{64}(")', rf'\g<1>{sha}\g<2>', new, count=1, flags=re.M)
    if new == old:
        return False
    open(path, "w", encoding="utf-8").write(new)
    return True


def main():
    tools = json.load(open(os.path.join(ROOT, "tools.json"), encoding="utf-8"))
    only = set(sys.argv[1:])
    for tool in tools:
        if only and tool["formula"] not in only:
            continue
        try:
            if sync(tool):
                print(tool["formula"])
        except Exception as e:  # keep going with the other tools
            print(f"{tool['formula']}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
