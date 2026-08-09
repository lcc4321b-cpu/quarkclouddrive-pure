# 文件操作

## 创建文件夹

```bash
node scripts/quark-drive.cjs create-folder --dir-path <DIR_PATH> [--parent-fid <PDIR_FID>]
```

## 移动

```bash
node scripts/quark-drive.cjs move <FID1> [FID2...] --target-fid <TARGET_FID>
```

移动会改变网盘结构，只在用户明确要求时执行。

## 下载 / 读取

```bash
node scripts/quark-drive.cjs read-file --fid <FID> [--overwrite]
node scripts/quark-drive.cjs read-file <FID1> <FID2> [--overwrite]
node scripts/quark-drive.cjs read-file list [--state <state>]
node scripts/quark-drive.cjs read-file resume --record-id <id>
node scripts/quark-drive.cjs read-file delete --record-id <id>
```

`read-file` 的实现会把网盘内容下载到 Agent 的运行时文件系统后再供 Agent 读取。涉及隐私或数据流说明时必须使用这一准确表述。
