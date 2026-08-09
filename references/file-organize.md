# 相册整理

```bash
node scripts/quark-drive.cjs organize --query <QUERY>
node scripts/quark-drive.cjs organize-copy --task-id <TASK_ID>
node scripts/quark-drive.cjs organize-move --task-id <TASK_ID>
```

`organize` 可能调用夸克侧的图像/视频理解与搜索能力。用户明确要求相册智能整理时可以使用，并如实说明这是服务端能力。

如果结果需要用户在“复制”与“移动”之间选择，必须等待选择后再执行对应确认命令。移动会改变原文件位置，比复制风险更高。

不要把该能力扩展到用户没有要求的文档、资料或其他文件类型。
