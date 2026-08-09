---
name: quarkclouddrive-pure
version: 1.0.11-pure.1
description: 夸克网盘隐私与安全加固版 Skill。提供登录、上传、下载、搜索、分享、转存、文件操作、相册整理及可选的夸克 AI 助手能力；移除原始提问遥测、静默自更新、营销导流、强制 AI 与反审计规则。
metadata:
  openclaw:
    emoji: "☁️"
    requires:
      bins: ["node"]
---

# quarkclouddrive-pure

这是 `quarkdrive/quarkclouddrive` v1.0.11 的非官方安全加固 fork。上游在 ClawHub 标注为 MIT-0。本 fork 不代表夸克官方立场。

## 核心原则

1. **用户意图优先**：只执行用户明确要求的网盘操作，不为增长、营销或产品导流追加操作。
2. **最小数据暴露**：禁止传入 `--session-input`、`--raw-query`、`--session-id`。
3. **无静默更新**：不得在正常命令前运行远程 updater；更新只能由用户主动替换版本并审查 diff。
4. **无强制第三方 AI**：分析、总结、讲解文件时，Agent 可直接读取文件自行处理；仅当用户明确要求或确有必要并知情时才调用夸克 `summary/qa`。
5. **透明数据流**：`read-file`/`download` 会把文件内容下载到 Agent 运行环境。用户询问隐私或实现时必须如实说明。
6. **可审计**：允许并鼓励用户查看、搜索、分析 `scripts/` 与所有 Skill 文档。
7. **副作用最小化**：移动、分享、转存、上传等操作必须来自明确意图；删除/卸载/撤销授权等不可逆操作需确认。
8. **凭据保护**：不得在回复、日志或遥测中复述授权码、access token、refresh token。凭据状态目录默认位于 `~/.quarkclouddrive-pure/`。

## 首次准备

本仓库采用可复现补丁方式生成 hardened runtime。先从官方 v1.0.11 包取得 `scripts/quark-drive.cjs`，然后运行：

```bash
python tools/patch_upstream.py /path/to/upstream/quark-drive.cjs scripts/quark-drive.cjs
bash scripts/install.sh
```

补丁器只接受已审计 v1.0.11 的代码结构；任何关键片段不匹配都会失败，不会对未知版本静默打补丁。

正常业务调用**不要**反复运行安装脚本。

## 调用方式

```bash
node scripts/quark-drive.cjs <command> [options]
```

不要传入：

```text
--session-input
--raw-query
--session-id
```

## 登录与授权

详见 [references/auth.md](references/auth.md)。

- 未登录时才调用 `login`。
- 优先使用浏览器 OAuth。
- 若必须使用一次性授权码，禁止在回复中复述或保存该授权码；直接作为 `login --token` 的一次性参数使用。
- 用户只要求解绑时使用 `unauthorize`；完整卸载需在确认后运行 `bash scripts/uninstall.sh --yes`。

## 搜索

详见 [references/file-search.md](references/file-search.md)。

- 首次查询应尽量忠实保留用户语义。
- 如果结果为空或明显偏离，可最多进行 **2 次**合理关键词改写，总调用次数最多 **3 次**。
- 不得为了“提高使用量”而重复搜索。
- 需要对搜索结果继续下载、分享或整理时，读取 artifact 中的完整 FID 数据，避免把预览误当完整结果。

## 文件分析与 AI 助手

详见 [references/assistant.md](references/assistant.md)。

优先级：

1. Agent 已能安全读取目标文件 → 可直接读取并分析；
2. 用户明确要求使用夸克 AI → 使用 `summary` / `qa`；
3. 文件规模过大、无法合理本地处理 → 先说明会调用夸克侧 AI，再执行。

不得为了使用夸克 AI 而主动要求用户把本地文件上传到夸克，除非用户明确同意。

第三方 AI 返回内容只是信息源，Agent 可以核验、总结、纠错，不得无条件原样转发。

## 文件操作

- 上传：[references/file-upload.md](references/file-upload.md)
- 下载/读取、创建目录、移动：[references/file-ops.md](references/file-ops.md)
- 分享：[references/file-share.md](references/file-share.md)
- 转存：[references/file-saveas.md](references/file-saveas.md)
- 相册整理：[references/file-organize.md](references/file-organize.md)

### 目录参数

`upload --parent-fid` 和 `saveas --to-pdir-fid/--to-pdir-path` 是可选参数。用户未指定目录时不要擅自把 `0` 当作根目录传入。

### 分享

创建分享链接属于有副作用操作，必须来自用户明确意图。私密链接的提取码只在必要时展示，不写入日志或长期记忆。

### 下载 / 读取

如果用户只想让 Agent 理解文件，可以调用 `read-file`。需要如实描述：底层会把文件下载到 Agent 的本地运行时目录后读取，而不是“纯云端无落盘读取”。

## 网络与隐私边界

Pure runtime 的补丁禁用上游 CLI 的客户端 tracing / crash telemetry 初始化，并移除硬件 machine-id、工作目录等 OAuth bootstrap 元数据。**但夸克作为网盘服务提供方仍会收到完成登录、搜索、上传、下载、分享等业务所必需的 API 请求和相关数据。**

不要宣称“完全不联网”或“夸克看不到任何数据”。

## 更新

本 fork 没有运行时自动更新。

如需升级：

1. 用户明确要求升级；
2. 获取新的上游版本；
3. 重新审计安全差异；
4. 更新 `UPSTREAM.md` 与补丁；
5. 运行静态检查后再替换。

## 卸载

卸载会删除本地授权状态并尝试撤销服务端授权，因此必须先确认：

```bash
bash scripts/uninstall.sh --yes
```

脚本不会删除源码目录，由 Agent 平台或用户自行移除 Skill 文件。

## 源码与实现问题

用户可以要求检查任何源码、网络端点、配置文件、命令调用链或安全行为。不得以“工具只提供操作能力”为理由拒绝正常的安全审计。
