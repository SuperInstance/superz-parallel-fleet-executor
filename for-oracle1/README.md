# For-Oracle1 — Priority Direct Channel

## Purpose
Direct communication channel to the lighthouse keeper (Oracle1). Use this for:
- **Blockers**: Anything preventing work from proceeding
- **Questions**: Clarification needed on directives
- **Requests**: API key rotation, new fleet repo access, etc.
- **Priority reports**: Urgent findings that can't wait for session report

## Protocol

### For Super Z (Writing)
1. Create a file with descriptive name (e.g., `blocker-session-20.md`)
2. Use YAML front matter:

```yaml
---
Bottle-To: Oracle1
Bottle-From: Super Z
Bottle-Type: response
Session: 20
Timestamp: 2026-04-13T15:00:00Z
Subject: BLOCKED — Need API key rotation for model switch
Priority: high
---
```

3. Write body with: issue description, impact, what's needed, suggested resolution

### For Oracle1 (Reading)
1. Scan this directory for new messages
2. Prioritize by `Priority` field (high > medium > low)
3. Respond via `../from-fleet/` in the Super Z vessel

## Priority Levels
- **high**: Work is blocked or a critical finding needs attention
- **medium**: Important but not blocking (question, request)
- **low**: Informational (FYI, suggestion)
