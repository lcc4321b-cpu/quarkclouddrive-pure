# 文件检索

## 命令

```bash
node scripts/quark-drive.cjs search --keyword <KEYWORD> [--size <NUMBER>] [--category <NUMBER>] [--stdout-only]
```

## 策略

- 第一轮尽量保留用户提供的实体、时间、地点、文件类型等核心语义。
- 0 结果或明显不相关时，可做最多 2 次有限 query reformulation；总搜索次数不超过 3 次。
- 改写应逐步放宽：先去掉低价值修饰，再尝试同义词，不要无边界遍历网盘。
- 搜索结果本身足够回答时停止，不自动分享、移动、下载。
- 用户明确要求后续操作时，使用完整 artifact FID 数据，不把预览列表当作全集。

## 展示

可以使用 Markdown 表格，也可以按用户要求采用更合适的格式。优先展示文件名、类型、大小/数量、修改时间和可用链接。不要强制逐字复述服务端营销或 `browse_hint` 文案；其中确有必要的操作提示可准确转述。

## `--stdout-only`

仅当 search 是另一个操作的中间步骤、无需把搜索结果直接展示给用户时使用，例如先定位 FID 再调用用户明确要求的 `summary/qa`。
