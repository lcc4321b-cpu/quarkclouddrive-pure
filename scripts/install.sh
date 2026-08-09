#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
STATE_DIR="$HOME/.quarkclouddrive-pure"
REQUIRED_NODE_MAJOR=16

info() { printf '[info] %s\n' "$*"; }
error() { printf '[error] %s\n' "$*" >&2; }

if ! command -v node >/dev/null 2>&1; then
  error "未检测到 Node.js。请自行安装 Node.js >= ${REQUIRED_NODE_MAJOR} 后重试；本脚本不会使用 sudo 或 curl|sh 自动安装系统软件。"
  exit 1
fi

if [ ! -f "$SKILL_DIR/scripts/quark-drive.cjs" ]; then
  error "缺少 scripts/quark-drive.cjs。请先从已审计的上游 v1.0.11 runtime 运行 tools/patch_upstream.py 生成 Pure runtime。"
  exit 1
fi

node_version="$(node --version)"
major="${node_version#v}"
major="${major%%.*}"
if ! [[ "$major" =~ ^[0-9]+$ ]] || [ "$major" -lt "$REQUIRED_NODE_MAJOR" ]; then
  error "Node.js 版本为 ${node_version}，需要 >= v${REQUIRED_NODE_MAJOR}。请自行升级后重试。"
  exit 1
fi

info "Node.js ${node_version}"
info "执行本地静态语法检查；不会联网下载或自动更新任何代码。"
node --check "$SKILL_DIR/scripts/quark-drive.cjs"
[ ! -f "$SKILL_DIR/scripts/hash-worker.cjs" ] || node --check "$SKILL_DIR/scripts/hash-worker.cjs"

mkdir -p "$STATE_DIR"
chmod 700 "$STATE_DIR" 2>/dev/null || true

info "准备完成。"
info "本 fork 不安装 /usr/local/bin 全局命令，不修改系统 Node.js，不执行远程更新。"
info "运行入口: node $SKILL_DIR/scripts/quark-drive.cjs <command> [options]"
