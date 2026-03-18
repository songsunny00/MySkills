# skill-vetter

[中文](README.md) | **English**

> Source: [openclaw/skills](https://github.com/openclaw/skills/tree/main/skills/spclaudehome/skill-vetter)

A security-first vetting protocol for AI agent skills. Always vet a skill before installing it — no exceptions.

## When to Use

- Before installing any skill from a GitHub repository
- Before running skills shared by other agents
- Anytime you are asked to install unknown code

## Vetting Protocol

skill-vetter runs a four-step review:

| Step | What It Checks |
|------|----------------|
| **Step 1** Source Check | Is the author reputable? Download count / stars? Last updated? |
| **Step 2** Code Review | Read all files and scan for dangerous patterns (mandatory) |
| **Step 3** Permission Scope | What files does it read/write? Any network calls? Is the scope minimal? |
| **Step 4** Risk Classification | Assess overall risk and produce an install recommendation |

### Immediate Rejection — Red Flags

- `curl`/`wget` requests to unknown URLs
- Reads sensitive directories: `~/.ssh`, `~/.aws`, `~/.config`
- Accesses identity files: `MEMORY.md`, `IDENTITY.md`, `SOUL.md`
- Uses `base64` decode, `eval()`, or `exec()` with external input
- Modifies system files outside the workspace
- Obfuscated code (compressed, encoded, minified)

## Risk Levels

| Level | Examples | Action |
|-------|----------|--------|
| 🟢 Low | Notes, formatting tools | Basic review, install OK |
| 🟡 Medium | File ops, API calls | Full code review required |
| 🔴 High | Credentials, system ops | Human approval required |
| ⛔ Extreme | Root access, security configs | Do NOT install |

## Output Report

After vetting, a structured report is generated automatically:

```
SKILL VETTING REPORT
═══════════════════════════════════════
Skill: [name]
Source: [source]
Author: [author]
───────────────────────────────────────
RED FLAGS: [None / list issues]
PERMISSIONS: Files / Network / Commands
RISK LEVEL: 🟢 LOW / 🟡 MEDIUM / 🔴 HIGH / ⛔ EXTREME
VERDICT: ✅ SAFE TO INSTALL / ⚠️ INSTALL WITH CAUTION / ❌ DO NOT INSTALL
═══════════════════════════════════════
```

## Install

```bash
npx skills add songsunny00/MySkills --skill skill-vetter -g -y
```

> Paranoia is a feature. 🔒