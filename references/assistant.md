# 文件分析与夸克 AI 助手

夸克侧提供 `summary` 与 `qa`，但在本 fork 中它们是**可选能力**，不是强制路径。

## 文件总结

```bash
node scripts/quark-drive.cjs summary --query <QUERY> [--fid-list <FID1,FID2,...>]
```

## 文件问答

```bash
node scripts/quark-drive.cjs qa --query <QUERY> --fid-list <FID1,FID2,...>
```

## 选择原则

优先直接读取文件并由当前 Agent 完成分析；以下情况可以使用夸克 AI：

- 用户明确说“用夸克 AI/知识库”；
- 文件数量或体量使直接读取明显不经济；
- 当前运行环境无法读取目标格式，而夸克侧能力可处理。

如果调用第三方 AI 会扩大数据处理范围，应提前说明这一点。不要为调用该功能而擅自上传原本不在夸克的本地文件。

返回结果可以被当前 Agent 复核、压缩、解释或与其他证据交叉验证；不要求原样转发。
