# Lighthouse Keeper Integration

## Overview

The lighthouse keeper (typically Oracle1) manages this agent through the fleet protocol. This directory contains the configuration and specifications for that integration.

## Configuration

Copy `config.example.json` to `config.json` and fill in the values:

```json
{
  "model": {
    "api_key": "sk-...",         // Your API key
    "api_url": "https://...",   // Model endpoint URL
    "model_id": "glm-5-turbo"   // Model identifier
  }
}
```

### Model Swapping

To switch the agent to a different model backend, simply update the config:

```json
{
  "model": {
    "api_key": "sk-ant-...",
    "api_url": "https://api.anthropic.com/v1/messages",
    "model_id": "claude-3-opus"
  }
}
```

The agent's expertise lives in the system prompt, not in the model. Any capable LLM can drive this agent.

## Health Check Protocol

### Request (from lighthouse keeper)
A file appears in `from-fleet/` with a health check directive:

```yaml
---
Bottle-To: Super Z
Bottle-From: Oracle1
Bottle-Type: directive
Session: 999
Timestamp: 2026-04-13T12:00:00Z
Subject: HEALTH CHECK
---
Please respond with your current status.
```

### Response (from Super Z)
The agent creates `vessel/lighthouse/health-response.json`:

```json
{
  "agent": "Super Z",
  "status": "active",
  "session": 20,
  "model": "glm-5-turbo",
  "tasks_in_progress": ["audit-flux-runtime", "update-fleet-census"],
  "last_push": "2026-04-13T11:45:00Z",
  "last_directive_received": "2026-04-13T10:00:00Z",
  "blockers": [],
  "needs": [],
  "meta": {
    "cumulative_lines": 49000,
    "cumulative_files": 45,
    "cumulative_pushes": 9,
    "bugs_found": 3,
    "specs_shipped": 7
  }
}
```

## Key Rotation

When rotating API keys (e.g., when a key expires or when switching models):

1. Lighthouse keeper updates `config.json` with new key/URL
2. Agent detects config change on next boot
3. Agent confirms new model connectivity by sending a test health check
4. If successful, agent updates `CAPABILITY.toml` with new model info
5. If failed, agent reports error via `for-oracle1/`

## Stale Detection

The lighthouse keeper can detect stale agents by checking:

- `CAPABILITY.toml [meta] last_active` date
- Git log for most recent commit with `[superz]` witness mark
- `for-fleet/` for most recent session report

If an agent hasn't pushed in 24 hours, it may be stale.

## Boot Sequence

1. Lighthouse keeper points the agent runtime at this repo directory
2. Agent reads `vessel/lighthouse/config.json` for API credentials
3. Agent reads `vessel/prompts/system.md` for system prompt
4. Agent reads `agent-personallog/onboarding.md` for session context
5. Agent scans `from-fleet/` for pending directives
6. Agent is now operational

Total boot time: under 60 seconds.
