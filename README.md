# hongyukeji/tap

[![Tests](https://github.com/hongyukeji/homebrew-tap/actions/workflows/tests.yml/badge.svg)](https://github.com/hongyukeji/homebrew-tap/actions/workflows/tests.yml)
[![Sync releases](https://github.com/hongyukeji/homebrew-tap/actions/workflows/sync.yml/badge.svg)](https://github.com/hongyukeji/homebrew-tap/actions/workflows/sync.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

中文 | [English](README.en.md)

[@hongyukeji](https://github.com/hongyukeji) 的 Homebrew tap，所有工具共用这一个。每个工具在自己的仓库开发和发布，这里只放安装配方，新版本发布后自动更新。

[安装](#安装) · [可用工具](#可用工具) · [更新](#更新) · [卸载](#卸载) · [常见问题](#常见问题) · [工作原理](#工作原理) · [添加工具](#添加工具)

## 安装

前提：已安装 [Homebrew](https://brew.sh/zh-cn/)。不需要 Xcode。

```bash
brew tap hongyukeji/tap
brew trust hongyukeji/tap
brew install <工具名>
```

Homebrew 7 起默认不加载第三方 tap 的配方，需要先用 `brew trust` 信任本 tap。前两条命令只需执行一次，之后安装其他工具只要 `brew install <工具名>`。

## 可用工具

| 工具 | 说明 | 安装 |
| --- | --- | --- |
| [PolySub](https://github.com/hongyukeji/polysub) | 把视频变成任意语言的字幕，支持本机或云端模型（Apple Silicon、macOS 13+） | `brew install polysub`，再运行 `polysub install` 把应用复制到「应用程序」 |

每个工具的用法、更新和卸载细节以它自己仓库的 README 为准。

## 更新

```bash
brew update
brew upgrade <工具名>
```

带图形界面的工具在升级后还需要把新版本复制到「应用程序」，例如 PolySub 要再运行一次 `polysub install`。

## 卸载

```bash
brew uninstall <工具名>
brew untap hongyukeji/tap    # 不再使用本 tap 中的任何工具时
```

`brew uninstall` 只删除 Homebrew 里的文件。复制到「应用程序」的应用和工具自己的数据，请按各工具 README 的「卸载」一节处理。

## 常见问题

### 提示 untrusted tap

执行一次 `brew trust hongyukeji/tap`，再重新安装或升级。

### 打开应用时弹出安全提示

通过本 tap 安装不应出现这个提示：配方由 Homebrew 用 curl 下载，文件不带隔离标记，macOS 不会拦截。如果仍然出现，请在 [Issues](https://github.com/hongyukeji/homebrew-tap/issues) 反馈机型、macOS 版本、工具版本和提示截图。

### 新版本已经发布，`brew upgrade` 还是旧版

本 tap 每 30 分钟检查一次各工具的最新 Release。先执行 `brew update` 刷新配方；刚发布的版本可能要等到下一次检查。

### 提示工具名已被 homebrew-core 占用

添加工具时已核对过 homebrew-core 没有同名配方。如果以后出现重名，用完整名称安装：`brew install hongyukeji/tap/<工具名>`。

## 工作原理

- **配方而非 Cask**：应用以 Formula 形式安装。Homebrew 用 curl 下载，文件不带隔离标记，打开时不弹 Gatekeeper 提示。各工具的发布流程会对应用做 ad-hoc 签名。
- **保持签名**：Homebrew 安装时会改写二进制里的库路径，这会破坏签名。所以配方把应用原样打包成 zip 放进 `libexec`，安装后再用 `ditto` 解压（`post_install_steps`）。
- **自动同步**：[Sync releases](.github/workflows/sync.yml) 每 30 分钟（也可手动运行）读取 [`tools.json`](tools.json) 中每个工具的最新已公开 Release，从 `SHA256SUMS` 取校验和，更新配方的 `url`、`version`、`sha256`，在 macOS 上 `brew style`、安装、测试通过后提交。全程不需要任何 token。
- **配方测试**：配方有改动时，[Tests](.github/workflows/tests.yml) 对每个配方做同样的检查。

## 添加工具

1. **工具仓库**：用 `packaging/macos/build.sh` 构建 macOS 应用，复制 [PolySub 的 release.yml](https://github.com/hongyukeji/polysub/blob/main/.github/workflows/release.yml)（改 `APP_NAME`），并按 [发布说明规范](https://github.com/hongyukeji/polysub/blob/main/docs/releases/README.md) 维护 `docs/releases/`。推送 `vX.Y.Z` 标签会创建草稿 Release，附带 `<App>-<version>-macos-arm64.zip` 和 `SHA256SUMS`；验证后公开发布，本 tap 随后自动更新。
2. **本仓库**：在 `tools.json` 加一项，复制 `Formula/polysub.rb` 为 `Formula/<工具名>.rb` 并修改。
3. **检查重名**：`curl -sI https://formulae.brew.sh/api/formula/<工具名>.json` 应返回 404，否则 `brew install <工具名>` 会装到 homebrew-core 里的同名工具。
4. 在上方[可用工具](#可用工具)表格中加一行。

### 目录

| 路径 | 内容 |
| --- | --- |
| [`Formula/`](Formula/) | 各工具的配方 |
| [`tools.json`](tools.json) | 需要自动同步的工具：配方名、仓库、发行包文件名 |
| [`scripts/sync_formulae.py`](scripts/sync_formulae.py) | 读取最新 Release 并更新配方 |
| [`.github/workflows/`](.github/workflows/) | 同步与测试 |

GitHub 会暂停 60 天没有活动的仓库里的定时任务。如果发生，在 Actions 页重新启用 **Sync releases**，或在发布后手动运行一次。

## 许可

本仓库遵循 [MIT License](LICENSE)。各工具的许可见各自仓库。
