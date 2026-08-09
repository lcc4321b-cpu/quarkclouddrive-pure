# quarkclouddrive-pure

> 夸克网盘官方 Skill v1.0.11 的**非官方隐私 / 安全加固 fork**：保留核心网盘能力，移除原始提问遥测、静默自更新、营销导流、强制夸克 AI、反审计规则，并收紧本地凭据保护。

## 为什么做这个 fork？

我对公开的 `quarkdrive/quarkclouddrive` v1.0.11 做了一次逐文件静态审计。结论不是“这是木马”，而是：**原版把产品增长、遥测、Agent 行为控制和运行时更新放进了一个拥有私人网盘权限的 Skill 里，安全边界过宽。**

这个仓库的目标是把它还原成更接近“工具”的形态：

- 你让它上传，它上传；
- 你让它搜索，它搜索；
- 你让它分享，它分享；
- 不额外上传你的原始聊天内容；
- 不因为一次普通搜索就先联网换掉自己的代码；
- 不强制把文件分析交给第三方 AI；
- 不阻止你审计它自己。

## 主要差异

| 项目 | 上游 v1.0.11 | pure.1 |
|---|---|---|
| 每次命令前运行 installer | 是 | **否** |
| 服务端选择 ZIP 并覆盖更新 | 是 | **禁用** |
| `--session-input` 原始问题追踪 | Agent 强制 | **禁止且运行时忽略** |
| session ID 服务质量追踪 | Agent 强制 | **禁止且运行时忽略** |
| command tracing / crash reporter | 启用代码路径 | **初始化禁用** |
| OS machine ID | OAuth bootstrap 使用 | **不使用** |
| 工作目录 | OAuth bootstrap 使用 | **不发送** |
| 配置文件权限 | 未主动收紧 | **0600 / 目录 0700（支持时）** |
| 文件总结/问答 | 强制夸克 AI | **可选** |
| 本地文件为用 AI 上传夸克 | 有导向 | **不默认建议** |
| 搜索失败后改写关键词 | 禁止 | **有限重试** |
| 10GB / 5000名额等营销文案 | 强制输出 | **移除** |
| Agent 审计运行时代码 | 禁止 | **允许** |
| `read-file` 本地落盘事实 | 淡化 | **明确披露** |
| Linux 缺 Node | `curl | sudo bash` | **停止并提示手动安装** |

## 安装

要求 Node.js >= 16。

```bash
bash scripts/install.sh
```

这个安装脚本不会下载任何远程代码，也不会修改系统 Node.js。

然后由 Agent / Skill 直接调用：

```bash
node scripts/quark-drive.cjs <command> [options]
```

## 支持能力

- 登录 / 解绑 / 查看用户信息
- 上传与断点续传
- 下载 / `read-file`
- 网盘搜索
- 创建目录、移动文件
- 创建分享、分享详情、分享内搜索
- 转存分享链接
- 相册智能整理
- 可选的夸克 AI `summary` / `qa`

具体 Agent 行为规则见 [`SKILL.md`](SKILL.md)。

## 安全边界

本项目**不是“夸克完全看不到你的数据”的代理**。只要你使用夸克网盘，业务请求仍然需要到达夸克服务端。这个 fork 处理的是额外的客户端风险：原始 prompt tracking、client tracing、静默代码替换、过度的 Agent 行为限制等。

详情：[`docs/SECURITY_AUDIT.md`](docs/SECURITY_AUDIT.md)。

## 可复现补丁

上游审计包：

```text
quarkclouddrive v1.0.11
SHA-256 034ac1f3db416ae6435e111024961abd84b9d80a2e8e8093db72adf50b950f48
```

补丁逻辑在：

```text
tools/patch_upstream.py
```

它对关键代码位置做精确匹配并在版本不符时失败，避免对未来版本静默误补丁。

## 验证

```bash
bash -n scripts/install.sh
bash -n scripts/uninstall.sh
node --check scripts/quark-drive.cjs
node --check scripts/hash-worker.cjs
python tests/static_checks.py
```

## License / provenance

上游 ClawHub 页面将 `quarkdrive/quarkclouddrive` v1.0.11 标注为 **MIT-0**。本仓库保留 [`NOTICE.md`](NOTICE.md) 说明来源，并采用 MIT-0。

本项目是社区 fork，与夸克官方无隶属或背书关系。
