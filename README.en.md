# hongyukeji/tap

[![Tests](https://github.com/hongyukeji/homebrew-tap/actions/workflows/tests.yml/badge.svg)](https://github.com/hongyukeji/homebrew-tap/actions/workflows/tests.yml)
[![Sync releases](https://github.com/hongyukeji/homebrew-tap/actions/workflows/sync.yml/badge.svg)](https://github.com/hongyukeji/homebrew-tap/actions/workflows/sync.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

[中文](README.md) | English

The Homebrew tap shared by all tools from [@hongyukeji](https://github.com/hongyukeji). Each tool is developed and released in its own repository; this tap only holds the formulae, which update automatically when a new version is released.

[Install](#install) · [Tools](#tools) · [Update](#update) · [Uninstall](#uninstall) · [FAQ](#faq) · [How it works](#how-it-works) · [Adding a tool](#adding-a-tool)

## Install

Requires [Homebrew](https://brew.sh/). Xcode is not needed.

```bash
brew tap hongyukeji/tap
brew trust hongyukeji/tap
brew install <tool>
```

Since Homebrew 7, formulae from third-party taps load only after you trust the tap with `brew trust`. The first two commands are needed once; after that, installing another tool is just `brew install <tool>`.

## Tools

| Tool | Description | Install |
| --- | --- | --- |
| [PolySub](https://github.com/hongyukeji/polysub) | Turn any video into subtitles in any language with local or cloud models (Apple silicon, macOS 13+) | `brew install polysub`, then `polysub install` to copy the app to /Applications |

Each tool's README is the reference for its usage, updates and removal.

## Update

```bash
brew update
brew upgrade <tool>
```

Tools with an app need the new version copied to /Applications after upgrading; for PolySub, run `polysub install` again.

## Uninstall

```bash
brew uninstall <tool>
brew untap hongyukeji/tap    # when you no longer use any tool from this tap
```

`brew uninstall` removes only the files inside Homebrew. For the copy in /Applications and the tool's own data, see the **Uninstall** section of that tool's README.

## FAQ

### Homebrew reports an untrusted tap

Run `brew trust hongyukeji/tap` once, then install or upgrade again.

### macOS shows a security prompt when opening the app

It should not when installed from this tap: Homebrew downloads formulae with curl, so the files carry no quarantine flag and macOS does not block them. If you do see one, please open an [issue](https://github.com/hongyukeji/homebrew-tap/issues) with your Mac model, macOS version, tool version and a screenshot.

### A new version is out but `brew upgrade` installs the old one

This tap checks each tool's latest release every 30 minutes. Run `brew update` to refresh the formulae; a release published moments ago may need to wait for the next check.

### The tool name is taken by homebrew-core

Tool names here are checked against homebrew-core when added. If a clash appears later, install with the full name: `brew install hongyukeji/tap/<tool>`.

## How it works

- **Formulae, not casks**: apps are installed as formulae. Homebrew downloads them with curl, so they carry no quarantine flag and open without a Gatekeeper prompt. Each tool's release workflow ad-hoc signs its app.
- **Keeping the signature**: Homebrew rewrites library paths in binaries during installation, which breaks signatures. The formula therefore keeps the app zipped in `libexec` and unzips it with `ditto` after installation (`post_install_steps`).
- **Automatic sync**: [Sync releases](.github/workflows/sync.yml) runs every 30 minutes (or by hand). For each tool in [`tools.json`](tools.json) it reads the latest published release, takes the checksum from `SHA256SUMS`, updates the formula's `url`, `version` and `sha256`, and commits after `brew style`, install and test pass on macOS. No tokens are needed.
- **Formula tests**: when a formula changes, [Tests](.github/workflows/tests.yml) runs the same checks on every formula.

## Adding a tool

1. **Tool repository**: build a macOS app with `packaging/macos/build.sh`, copy [PolySub's release.yml](https://github.com/hongyukeji/polysub/blob/main/.github/workflows/release.yml) (change `APP_NAME`), and keep `docs/releases/` as described in the [release-notes guide](https://github.com/hongyukeji/polysub/blob/main/docs/releases/README.md). Pushing a `vX.Y.Z` tag creates a draft release with `<App>-<version>-macos-arm64.zip` and `SHA256SUMS`; publish it after checking, and this tap follows automatically.
2. **This repository**: add an entry to `tools.json`, and copy `Formula/polysub.rb` to `Formula/<tool>.rb` and adapt it.
3. **Check the name**: `curl -sI https://formulae.brew.sh/api/formula/<tool>.json` must return 404; otherwise `brew install <tool>` installs the homebrew-core formula instead.
4. Add a row to the [Tools](#tools) table above.

### Layout

| Path | Contents |
| --- | --- |
| [`Formula/`](Formula/) | One formula per tool |
| [`tools.json`](tools.json) | Tools to sync: formula name, repository, release asset name |
| [`scripts/sync_formulae.py`](scripts/sync_formulae.py) | Reads the latest releases and updates the formulae |
| [`.github/workflows/`](.github/workflows/) | Sync and tests |

GitHub pauses scheduled workflows in repositories without activity for 60 days. If that happens, re-enable **Sync releases** in the Actions tab, or run it by hand after a release.

## License

This repository is under the [MIT License](LICENSE). Each tool's license is in its own repository.
