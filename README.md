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
| `--session-input` 原始问题追踪 | Agent 强制 | **移除** |
| session ID 服务质量追踪 | Agent 强制 | **移除** |
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

要求：Python 3、Node.js >= 16。

本仓库**不直接提交 478 KB 的生成后 bundled runtime**。原因是希望让安全修改可复现、可审查，而不是再发布一个新的大黑盒 bundle。

先从官方 `quarkclouddrive v1.0.11` 包中取得：

```text
scripts/quark-drive.cjs
```

然后生成 Pure runtime：

```bash
python tools/patch_upstream.py \
  /path/to/upstream/scripts/quark-drive.cjs \
  scripts/quark-drive.cjs
```

成功时输出文件 SHA-256 必须为：

```text
5cc869dc1d367e9915efc66c8bb0f24d1a0a96c86502d92d358e357bff3992cc
```

再执行一次本地准备检查：

```bash
bash scripts/install.sh
```

`install.sh` 不会联网下载代码、不使用 `sudo`、不修改系统 Node.js，也不会自动更新 Skill。

之后由 Agent / Skill 直接调用：

```bash
node scripts/quark-drive.cjs <command> [options]
```

## 为什么采用 patch-first 发布？

它提供三件事：

1. **固定输入**：只针对已审计的 v1.0.11；
2. **显式 diff**：所有安全修改集中在 `tools/patch_upstream.py`；
3. **确定输出**：Pure runtime 有固定 SHA-256，任何人都能独立复现。

如果未来上游 bundle 的关键结构变化，补丁器会直接失败，而不是把旧补丁静默套到未知版本。

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

完整审计：[`docs/SECURITY_AUDIT.md`](docs/SECURITY_AUDIT.md)。

## 上游固定版本

```text
quarkclouddrive v1.0.11
Audited ZIP SHA-256:
034ac1f3db416ae6435e111024961abd84b9d80a2e8e8093db72adf50b950f48

Pure runtime SHA-256:
5cc869dc1d367e9915efc66c8bb0f24d1a0a96c86502d92d358e357bff3992cc
```

更多 provenance 信息见 [`UPSTREAM.md`](UPSTREAM.md) 和 [`NOTICE.md`](NOTICE.md)。

## 验证

生成 `scripts/quark-drive.cjs` 后：

```bash
bash -n scripts/install.sh
bash -n scripts/uninstall.sh
node --check scripts/quark-drive.cjs
node --check scripts/hash-worker.cjs
python tests/static_checks.py
```

## 小红书发布材料

对应的技术内容发布稿保存在：[`docs/xiaohongshu-post.md`](docs/xiaohongshu-post.md)。

## License / provenance

上游 ClawHub 页面将 `quarkdrive/quarkclouddrive` v1.0.11 标注为 **MIT-0**。本仓库保留 [`NOTICE.md`](NOTICE.md) 说明来源，并采用 MIT-0。

本项目是社区 fork，与夸克官方无隶属或背书关系。
