# Changelog

## 1.0.11-pure.1

Initial hardened fork of upstream v1.0.11.

- removed runtime self-update registration;
- replaced remote/self-updating installer with local validation only;
- disabled bundled command tracing initialization and crash reporter;
- ignored raw prompt/session telemetry parameters;
- removed OS machine-id, hardware model and working-directory metadata from OAuth bootstrap;
- isolated runtime state under `~/.quarkclouddrive-pure`;
- hardened credential/storage file permissions on supporting OSes;
- removed marketing/FOMO instructions;
- removed anti-audit instructions;
- made Quark AI optional;
- allowed bounded search reformulation;
- documented actual local download behavior;
- made uninstall explicit with `--yes` and stopped touching unrelated global files.
