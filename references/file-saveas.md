# 转存分享链接

```bash
node scripts/quark-drive.cjs saveas --url <URL> [--fid-list <FIDS>] [--to-pdir-path <PATH>] [--to-pdir-fid <FID>] [--passcode <CODE>] [--save-all]
```

规则：

- 用户未指定目录时，不主动传 `--to-pdir-path` / `--to-pdir-fid`。
- 提取码只用于完成当前操作，不进入遥测、日志或长期记忆。
- 转存会改变用户网盘内容，必须来自明确意图。
