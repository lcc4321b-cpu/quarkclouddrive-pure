#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
STATE_DIR="$HOME/.quarkclouddrive-pure"

if [ "${1:-}" != "--yes" ]; then
  printf '%s\n' "此操作会尝试撤销当前授权，并删除 $STATE_DIR。"
  printf '%s\n' "请在用户已明确确认后重新执行: bash scripts/uninstall.sh --yes"
  exit 2
fi

if [ -f "$SKILL_DIR/scripts/quark-drive.cjs" ]; then
  node "$SKILL_DIR/scripts/quark-drive.cjs" logout >/dev/null 2>&1 || \
    printf '%s\n' "[warn] 服务端授权撤销未成功或当前未登录；继续清理本地状态。" >&2
fi

if [ -d "$STATE_DIR" ]; then
  rm -rf -- "$STATE_DIR"
fi

printf '%s\n' "[ok] 已清理 quarkclouddrive-pure 本地状态。Skill 源码目录未删除。"
