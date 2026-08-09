#!/usr/bin/env python3
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
cli_path = ROOT / "scripts/quark-drive.cjs"
skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
install = (ROOT / "scripts/install.sh").read_text(encoding="utf-8")
uninstall = (ROOT / "scripts/uninstall.sh").read_text(encoding="utf-8")

if not cli_path.exists():
    raise SystemExit("scripts/quark-drive.cjs is not generated yet; run tools/patch_upstream.py first")

cli = cli_path.read_text(encoding="utf-8")
checks = {
    "pure build marker": "quarkclouddrive-pure: privacy/security hardened fork" in cli,
    "pure version": 'Ow="1.0.11-pure.1"' in cli,
    "isolated runtime dir": 'ht=".quarkclouddrive-pure"' in cli,
    "trace provider disabled": "async doInitialize(e){this._initialized=!0;this._available=!1;this._config=null;return!1}" in cli,
    "crash reporter disabled": "reportJSError(){},setConfig(){},setReady(){}" in cli,
    "raw prompt ignored": 'let u="",c=""' in cli,
    "telemetry CLI options removed": "--session-input <input>" not in cli and "--raw-query <query>" not in cli and "--session-id <id>" not in cli,
    "self updater unregistered": ",Zp(),_g(),yg(),Sg()" not in cli,
    "remote updater implementation removed": "skill_config" not in cli and "curl -fsSL" not in cli,
    "machine id removed": "machineIdSync()" not in cli,
    "cwd metadata removed": "workDir:y.permissionManager.getWorkDir()" not in cli,
    "config dir chmod": "chmodSync(n,448)" in cli,
    "config file chmod": "chmodSync(e,384)" in cli,
    "skill forbids session telemetry args": "禁止传入 `--session-input`" in skill,
    "local installer has no curl command": "\ncurl " not in install and "$(curl " not in install,
    "local installer has no sudo command": "\nsudo " not in install and "$(sudo " not in install,
    "local installer has no remote updater": "skill_config" not in install,
    "uninstall requires explicit yes": '${1:-}' in uninstall and '--yes' in uninstall,
    "uninstall avoids usr-local deletion": "/usr/local/bin" not in uninstall,
}

bad = [name for name, ok in checks.items() if not ok]
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL"), name)

print("CLI_SHA256", hashlib.sha256(cli.encode()).hexdigest())
if bad:
    raise SystemExit("failed: " + ", ".join(bad))
