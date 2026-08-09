# 授权与账号管理

## 登录

优先：

```bash
node scripts/quark-drive.cjs login
```

若浏览器 OAuth 超时且用户已经取得一次性授权码：

```bash
node scripts/quark-drive.cjs login --token <agent_auth_code>
```

安全要求：

- 授权码、access token、refresh token 都视为凭据。
- 不在回复中复述，不加入 `--session-input` / `--raw-query`，不保存到日志或笔记。
- 本 fork 将运行时状态隔离到 `~/.quarkclouddrive-pure/`，并对配置文件使用尽可能严格的本地权限。

## 未授权

业务命令返回未授权时，不要无限重试。提示用户需要登录；用户同意继续后执行 `login`，成功后再重试原任务一次。

## 取消授权

用户明确要求解绑当前设备时：

```bash
node scripts/quark-drive.cjs unauthorize
```

该命令可能生成需要在夸克 App 中确认的解除授权链接。

## 用户信息

```bash
node scripts/quark-drive.cjs get-user-info
```

仅在用户需要查看绑定状态或账号信息时调用。

## 卸载

卸载属于不可逆操作。先获得明确确认，然后：

```bash
bash scripts/uninstall.sh --yes
```

该脚本尝试调用 `logout` 撤销授权，再删除 `~/.quarkclouddrive-pure/`。它不会删除 Skill 源码目录，也不会删除 `/usr/local/bin` 中任何同名第三方文件。

## 更新

运行时自动更新已禁用。不要调用 `update`，也不要从 `skill_config` 下载远程 ZIP 覆盖当前代码。
