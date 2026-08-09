#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

UPSTREAM_ZIP_SHA256 = "034ac1f3db416ae6435e111024961abd84b9d80a2e8e8093db72adf50b950f48"
PATCHED_CLI_SHA256 = "5cc869dc1d367e9915efc66c8bb0f24d1a0a96c86502d92d358e357bff3992cc"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, got {count}")
    return text.replace(old, new, 1)


def replace_region(text: str, start: str, end: str, replacement: str, label: str) -> str:
    a = text.find(start)
    if a < 0:
        raise RuntimeError(f"{label}: start marker missing")
    b = text.find(end, a + len(start))
    if b < 0:
        raise RuntimeError(f"{label}: end marker missing")
    return text[:a] + replacement + text[b:]


def patch_cli(text: str) -> str:
    # 1) Isolate this fork's state from the official skill.
    text = replace_once(
        text,
        'ht=l_?".quarkclouddrive":".quark-drive"',
        'ht=".quarkclouddrive-pure"',
        "runtime state directory",
    )
    text = replace_once(
        text,
        'function bn(s,e){return u_(Di)?Ie.join(Di,s,e):Ie.join(Oi(),ht,e)}',
        'function bn(s,e){return Ie.join(Fa.homedir(),ht,s,e)}',
        "runtime storage base",
    )

    # 2) Always keep credentials under ~/.quarkclouddrive-pure/<agent>/config.json.
    text = replace_region(
        text,
        'resolveConfigPath(){',
        'loadPersistedConfig(){',
        'resolveConfigPath(){let e=fe();return $u(e)}',
        "config path resolver",
    )

    # 3) Lock credential and SDK storage permissions on Unix-like systems.
    text = replace_once(
        text,
        'te.existsSync(n)||te.mkdirSync(n,{recursive:!0});let i=te.openSync(r,"w");',
        'te.existsSync(n)||te.mkdirSync(n,{recursive:!0,mode:448});try{te.chmodSync(n,448)}catch{}let i=te.openSync(r,"w",384);',
        "credential file creation",
    )
    text = replace_once(
        text,
        'return this.renameWithReplace(r,e),!0',
        'this.renameWithReplace(r,e);try{te.chmodSync(e,384)}catch{}return!0',
        "credential chmod",
    )
    text = replace_once(
        text,
        'Mr.default.mkdirSync(e,{recursive:!0})',
        'Mr.default.mkdirSync(e,{recursive:!0,mode:448})',
        "SDK storage directory mode",
    )
    text = replace_once(
        text,
        'Mr.default.writeFileSync(this.storagePath,JSON.stringify(e,null,2),"utf8")',
        'Mr.default.writeFileSync(this.storagePath,JSON.stringify(e,null,2),{encoding:"utf8",mode:384});try{Mr.default.chmodSync(this.storagePath,384)}catch{}',
        "SDK storage file mode",
    )

    # 4) Disable the bundled multi-tracer entirely. Business API calls remain untouched.
    text = replace_region(
        text,
        'async doInitialize(e){',
        'getOrCreateTracer(e){',
        'async doInitialize(e){this._initialized=!0;this._available=!1;this._config=null;return!1}',
        "TraceManager initialization",
    )

    # 5) Disable the separate crash/error reporter.
    text = replace_region(
        text,
        'sd=class s{static{this.needsInit=!0}',
        ',Gn=sd;',
        'sd=class s{static getInstance(){return{reportJSError(){},setConfig(){},setReady(){}}}static setConfig(e){}static async flush(){}}',
        "crash reporter",
    )

    # 6) Remove raw-prompt/session tracking options from CLI help/commands and ignore legacy args.
    text = replace_region(
        text,
        'function wg(s){',
        'function Ig(){',
        'function wg(s){for(let e of s.commands)e.options.some(t=>t.long==="--verbose")||e.option("--verbose","启用详细日志输出",!1),wg(e)}',
        "recursive common CLI options",
    )
    root_old = 'function Ig(){let s=new x;return s.name("quark-drive").description("\\u5938\\u514B\\u7F51\\u76D8\\u547D\\u4EE4\\u884C\\u5DE5\\u5177").version(Ow).enablePositionalOptions().option("--verbose","\\u542F\\u7528\\u8BE6\\u7EC6\\u65E5\\u5FD7\\u8F93\\u51FA",!1),s.option("--session-input <input>","\\u5F53\\u524D\\u4F1A\\u8BDD\\u7684\\u7528\\u6237\\u8F93\\u5165\\uFF08\\u53EF\\u9009\\uFF0Cagent \\u80FD\\u83B7\\u53D6\\u5230\\u65F6\\u4F20\\u5165\\uFF09"),s.addOption(new zo("--raw-query <query>").hideHelp()),s.option("--session-id <id>","\\u4F1A\\u8BDD\\u552F\\u4E00\\u6807\\u8BC6\\uFF08\\u540C\\u4E00\\u5BF9\\u8BDD\\u5185\\u590D\\u7528\\uFF09"),rl().forEach'
    root_new = 'function Ig(){let s=new x;return s.name("quark-drive").description("\\u5938\\u514B\\u7F51\\u76D8\\u547D\\u4EE4\\u884C\\u5DE5\\u5177").version(Ow).enablePositionalOptions().option("--verbose","\\u542F\\u7528\\u8BE6\\u7EC6\\u65E5\\u5FD7\\u8F93\\u51FA",!1),rl().forEach'
    text = replace_once(text, root_old, root_new, "root telemetry CLI options")
    text = replace_once(
        text,
        'let u=t.opts().sessionInput||e.opts().sessionInput||t.opts().rawQuery||e.opts().rawQuery;u&&R.setRawQuery(u);let c=t.opts().sessionId||e.opts().sessionId;c&&R.setSessionId(c)',
        'let u="",c=""',
        "session telemetry",
    )

    # 7) Remove the remote updater implementation and unregister the command.
    text = replace_region(
        text,
        'var ss=require("child_process"),ee=O(require("fs")),ge=O(require("path")),Eo=O(require("os"));G();W();var Dw="/agent/v1/skill_config";',
        'F();G();G();W();function yg(s){',
        'function _g(){return new x(qe).description("Runtime self-update disabled in quarkclouddrive-pure").action(()=>{throw new Error("Runtime self-update disabled; install a reviewed release explicitly")})}F();G();G();W();',
        "remote updater implementation",
    )
    text = replace_once(text, ',Zp(),_g(),yg(),Sg()', ',Zp(),yg(),Sg()', "self-update command registration")

    # 8) Do not send a hardware machine ID, hardware model, or working directory in OAuth bootstrap.
    text = replace_once(text, 'd=(await Promise.resolve().then(()=>O(Mi()))).machineIdSync()||""', 'd=a?.deviceId||""', "login hardware machine id")
    text = replace_once(text, 'let l=await y.getPlatformModel();', 'let l="Agent";', "login hardware model")
    text = text.replace('workDir:y.permissionManager.getWorkDir()', 'workDir:""')

    text = replace_region(
        text,
        'async function kw(s){',
        'function gg(s){',
        'async function kw(s){let e=y.permissionManager.getPersistedDeviceId();if(e)return e;let r=await M(),n=y.permissionManager.getDynamicClientInfo();if(!n)throw new Error("无法获取 clientInfo，请检查运行时配置");let t=n.deviceId||"";if(!t)return"";let i=await r.oauth.getAuthorizePageUrl({clientDeviceId:t,deviceName:"Agent",agentId:Be(y.detectAgent()),clientId:n.clientId,workDir:"",currentUserId:y.permissionManager.getUserId()??""}),o=i?.data?.deviceId??"";return String(i?.req_id??""),o}',
        "unauthorize machine id helper",
    )
    text = replace_once(text, 'let r=await y.getPlatformModel(),n=await kw(r);', 'let r="Agent",n=await kw(r);', "unauthorize hardware model")

    # 9) Mark build identity clearly.
    text = replace_once(text, 'Ow="1.0.11-1e57fff"', 'Ow="1.0.11-pure.1"', "CLI version")
    marker = '// quarkclouddrive-pure: privacy/security hardened fork of quarkdrive/quarkclouddrive v1.0.11 (MIT-0)\n'
    if text.startswith('#!/usr/bin/env node\n') and marker not in text:
        text = '#!/usr/bin/env node\n' + marker + text[len('#!/usr/bin/env node\n'):]
    return text


def main() -> None:
    ap = argparse.ArgumentParser(description="Reproduce quarkclouddrive-pure from the official v1.0.11 runtime")
    ap.add_argument("input", type=Path, help="upstream scripts/quark-drive.cjs")
    ap.add_argument("output", type=Path, help="patched output path")
    args = ap.parse_args()
    src = args.input.read_text(encoding="utf-8")
    out = patch_cli(src)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(out, encoding="utf-8")
    digest = hashlib.sha256(out.encode()).hexdigest()
    print(digest, args.output)
    if digest != PATCHED_CLI_SHA256:
        raise SystemExit(f"patched runtime hash mismatch: expected {PATCHED_CLI_SHA256}, got {digest}")


if __name__ == "__main__":
    main()
