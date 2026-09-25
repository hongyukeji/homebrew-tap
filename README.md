# hongyukeji/tap

Homebrew tap for tools by [@hongyukeji](https://github.com/hongyukeji).

```bash
brew tap hongyukeji/tap
brew trust hongyukeji/tap   # once (Homebrew 7+ requires trusting third-party taps)
brew install polysub
```

| Formula | Description |
| --- | --- |
| [polysub](https://github.com/hongyukeji/polysub) | Turn any video into subtitles in any language with local or cloud models (macOS, Apple silicon) |

Upgrade with `brew upgrade <formula>`.

## How releases reach this tap

Each tool lives in its own repository and publishes GitHub Releases. Every 30 minutes
(`.github/workflows/sync.yml`, or run it by hand) this tap checks the latest release of
every tool in `tools.json`, takes the SHA256 from the release's `SHA256SUMS`, updates the
formula, installs and tests it on macOS, and commits. No tokens are needed anywhere.

Apps are installed as **formulae, not casks**: Homebrew downloads them with curl, so they do
not get the quarantine flag and open without a Gatekeeper prompt. Each app is ad-hoc signed
by its release workflow.

## Adding a tool

1. In the tool's repository: build a macOS app with `packaging/macos/build.sh`, and copy
   `.github/workflows/release.yml` from [polysub](https://github.com/hongyukeji/polysub)
   (change `APP_NAME`). Pushing a `vX.Y.Z` tag creates a draft release with
   `<App>-<version>-macos-arm64.zip` and `SHA256SUMS`; the tap picks it up once it is published.
2. Here: add an entry to `tools.json` and a `Formula/<name>.rb` (copy `polysub.rb`).
3. Check the name is not already taken by homebrew-core
   (`curl -sI https://formulae.brew.sh/api/formula/<name>.json` must return 404),
   otherwise `brew install <name>` installs the other one.

Note: GitHub pauses scheduled workflows in repositories without activity for 60 days;
if that happens, re-enable **Sync releases** in the Actions tab (or run it by hand after a release).
