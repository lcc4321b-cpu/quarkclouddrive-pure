# Security policy

## Threat model

This Skill operates on private cloud-drive data and OAuth credentials. The hardened fork therefore treats these as security boundaries:

- no raw user-prompt telemetry;
- no runtime code self-update;
- no hardware machine-id collection for OAuth bootstrap;
- no working-directory disclosure in OAuth bootstrap;
- no forced cloud-AI processing when local analysis is available;
- restrictive local credential-file permissions where the OS supports them;
- no automatic system package installation or `curl | sudo shell` path;
- explicit user intent for side-effecting operations.

## What is *not* promised

This is not an offline client. Quark necessarily receives business API traffic required to authenticate and perform requested storage operations. Server-side logs and service policies remain outside this fork's control.

The patched runtime still contains dead bundled telemetry-library code and endpoint strings because the upstream JS is a bundle. The initialization paths used by the fork are disabled; see `docs/SECURITY_AUDIT.md` and `tools/patch_upstream.py`.

## Reporting

Please open a GitHub issue with a minimal reproduction. Do not include OAuth codes, access tokens, refresh tokens, private filenames, or private file contents.
