# 上传

```bash
node scripts/quark-drive.cjs upload <PATH1> [PATH2...] [--parent-fid <PDIR_FID>]
node scripts/quark-drive.cjs upload --file-path <LOCAL_PATH> [--parent-fid <PDIR_FID>]
```

用户未指定目标目录时省略 `--parent-fid`，不要擅自填 `0`。

上传属于把本地数据发送到夸克网盘的操作。必须来自用户明确意图；敏感文件如果意图不清晰，应先确认目标文件和目的地。

断点续传：

```bash
node scripts/quark-drive.cjs upload list [--state <STATE>]
node scripts/quark-drive.cjs upload resume --record-id <ID>
node scripts/quark-drive.cjs upload delete --record-id <ID>
```
