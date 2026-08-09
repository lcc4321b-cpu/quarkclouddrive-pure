# quarkclouddrive v1.0.11 security and agent-behavior audit

Audit target SHA-256:

`034ac1f3db416ae6435e111024961abd84b9d80a2e8e8093db72adf50b950f48`

## Executive conclusion

The audited upstream package did not show the usual indicators of a commodity malware payload in static review: no browser-cookie sweep, SSH-key harvesting, reverse shell, miner, or remote `eval` payload was found.

The larger risk came from its Agent control model, telemetry, credential handling and update supply chain. These findings do **not** justify calling the upstream release malware; they describe security and governance properties of the Skill and bundled runtime.

## High-impact findings

| Finding | Severity | Pure fork treatment |
|---|---|---|
| Normal commands were preceded by `install.sh`, which could fetch a server-selected latest ZIP, overwrite runtime/docs and execute the new runtime without a pinned hash/signature | Critical | Removed from normal operation; no runtime self-update |
| Tool output could instruct the Agent to stop using/clear Skill-related memory and reread replaced docs | High | Removed |
| Skill required `--session-input` to contain the user's verbatim prompt for service-quality tracking even though CLI marked it optional | High | Prohibited; runtime option/path removed by patch |
| Tracing stored raw query/session metadata plus device/user/runtime dimensions | High | Trace manager initialization and separate crash reporter disabled |
| OAuth bootstrap used OS machine ID, hardware/device model and working directory | High | Replaced with app-generated device ID; generic device name; blank workDir |
| OAuth/access/refresh tokens were persisted without an explicit 0600/0700 policy | High | Runtime state isolated; file/dir permissions tightened where supported |
| Skill prohibited Agents from reading/analyzing `quark-drive.cjs` or explaining implementation details | High | Anti-audit rules removed |
| File summary/QA was mandated through Quark AI, including guidance that could expand cloud processing scope | High | Quark AI made optional |
| Linux dependency path could execute `curl | sudo bash` to install Node | High | Removed; installer stops and asks user to install Node explicitly |
| Search was constrained to one attempt and query reformulation was forbidden | Medium | Bounded reformulation allowed, max 3 searches |
| `read-file` was framed as “read” although content is materialized into Agent runtime storage | Medium | Data flow disclosed accurately |
| Registration/AI quota marketing and scarcity copy were embedded in Agent behavior rules | Medium | Removed |

## Evidence chains

### 1. Remote update supply chain

Upstream `SKILL.md` required running `scripts/install.sh` before CLI use. The installer queried a remote `skill_config`, accepted a server-selected ZIP URL, downloaded and unpacked it, replaced `scripts/` and Skill documentation, then executed the resulting runtime for a version check. The reviewed path did not pin a release hash or verify a cryptographic signature.

For an Agent Skill this is more sensitive than a normal application updater because the remote package can alter both executable code and the behavioral instructions the Agent reads.

### 2. Verbatim prompt telemetry

Upstream Skill instructions required every CLI call to include `--session-input` containing the user's original prompt verbatim for service-quality tracking. The CLI itself described the field as optional. Runtime analysis showed the value entering the raw-query tracing path.

The Pure fork removes the CLI options and ignores the session telemetry path.

### 3. Agent-control instruction in installer output

The upstream installer could emit instructions equivalent to clearing Skill-related memory and rereading the newly updated `SKILL.md`. This crosses a useful trust boundary: tool output should report state, not attempt to modify the Agent's governing behavior or memory policy.

### 4. OAuth and local credential protection

The runtime persists OAuth state including access and refresh tokens. The reviewed implementation did not proactively set a restrictive 0600/0700 policy. The hardened patch isolates state under `~/.quarkclouddrive-pure` and adds restrictive modes where the platform supports them.

### 5. Forced third-party AI and anti-audit policy

Upstream instructions required file summary/QA to route through Quark AI and separately told the Agent not to inspect or explain the bundled runtime. The Pure policy treats Quark AI as an optional tool and explicitly allows source inspection.

## What the Pure fork changes in code

`tools/patch_upstream.py` performs exact-match transformations against the audited v1.0.11 runtime. It:

1. isolates state under `~/.quarkclouddrive-pure`;
2. tightens credential/storage modes;
3. disables bundled tracing initialization;
4. disables the separate crash reporter;
5. removes raw-prompt/session tracking CLI options and path;
6. removes the remote updater implementation and command registration;
7. removes OS machine-id, hardware model and working-directory metadata from OAuth bootstrap;
8. marks the build `1.0.11-pure.1`.

Expected patched CLI SHA-256:

`5cc869dc1d367e9915efc66c8bb0f24d1a0a96c86502d92d358e357bff3992cc`

The patcher fails if expected code markers do not match, so it will not silently patch an unknown future version.

## Limitations

This was a static audit. The Pure fork does not make Quark an offline service: authentication and requested cloud-drive operations still send business API traffic to Quark. Server-side logging, retention and processing are outside this fork's control.

Because the upstream runtime is bundled JavaScript, dead telemetry library code and endpoint strings can remain in the generated file even after initialization paths are disabled. Security claims should be limited to the reviewed execution paths and patch set.
