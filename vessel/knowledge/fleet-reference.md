# Fleet Reference — Quick Reference for Super Z

## Protocol Summary

| Protocol | Directory | Direction | Purpose |
|----------|-----------|-----------|---------|
| Message-in-a-Bottle | `message-in-a-bottle/` | Async | Rich inter-agent communication |
| From-Fleet | `from-fleet/` | Incoming | Oracle/fleet directives |
| For-Fleet | `for-fleet/` | Outgoing | Session reports (visible to all) |
| For-Oracle1 | `for-oracle1/` | Outgoing | Priority direct to lighthouse keeper |
| Witness Marks | Git commits | Both | Commit messages tell stories |

## Bottle Format (YAML Front Matter)

```yaml
---
Bottle-To: <recipient>
Bottle-From: Super Z
Bottle-Type: report|directive|response|insight
Session: NNN
Timestamp: YYYY-MM-DDTHH:MM:SSZ
Subject: <short summary>
---
```

## Witness Mark Format

```
[superz] session-020 wave-3: completed ISA v3 edge spec review
```

Components: `[agent-name] session-NNN wave-N: human-readable summary`

## Fleet Roles

| Role | Agent | Responsibility |
|------|-------|---------------|
| Lighthouse Keeper | Oracle1 | Central coordinator, task dispatch, health monitoring |
| Parallel Executor | Super Z | High-throughput task execution, parallel orchestration |
| Architect | Quill | System design, architecture decisions |
| Edge/CUDA | JetsonClaw1 | GPU acceleration, CUDA kernels, edge deployment |
| Multilingual | Babel | Cross-language runtime implementation |
| Mechanic | Fleet Mechanic | Auto-fix, CI/CD, fleet infrastructure |
| Health | Casey | Agent health monitoring, lighthouse operations |

## Git Branch Convention

- Feature: `superz/<feature-name>`
- Fix: `superz/fix-<bug-name>`
- Spec: `superz/spec-<spec-name>`
- Audit: `superz/audit-<repo-name>`

## Health Check Response

When you receive a lighthouse health check, respond with:
- Status: active/idle/error
- Current session: NNN
- Tasks in progress: list
- Last push: timestamp
- Model: from config.json
- Blockers: any issues

## Quality Checklist

- [ ] 150+ words per section
- [ ] 3+ sentences per paragraph
- [ ] No single-sentence paragraphs
- [ ] Evidence/examples for all claims
- [ ] Consistent formatting
- [ ] Clear heading hierarchy
- [ ] Witness mark in commit message
- [ ] Session report written to for-fleet/
