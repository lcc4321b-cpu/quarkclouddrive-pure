# 文件分享

## 创建分享

```bash
node scripts/quark-drive.cjs share <FID1> [FID2...] [--title <TITLE>] [--url-type <NUMBER>] [--expired-type <NUMBER>]
```

创建公开或私密分享链接会扩大文件访问范围，必须由用户明确要求。生成后清楚告知链接类型、有效期和提取码（若有）。

## 分享详情

```bash
node scripts/quark-drive.cjs share-detail --url <URL> [--page <NUMBER>] [--size <NUMBER>] [--pdir-fid <FID>]
```

## 分享内搜索

```bash
node scripts/quark-drive.cjs share-search --url <URL> --keyword <KEYWORD> [--page <NUMBER>] [--size <NUMBER>]
```
