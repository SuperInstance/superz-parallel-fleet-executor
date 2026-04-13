# Extraction Guide — Using Super Z Components in Your Project

This repo is designed to be modular. You can extract individual components, wrap the whole repo, or use it as a template. Here's how.

## Component Extraction

### Quality Validator (★★★★★ — Perfect Standalone)

Copy `vessel/tools/quality_validator.py` to your project. It has zero dependencies (Python stdlib only) and zero coupling to this repo.

```bash
cp vessel/tools/quality_validator.py /your-project/tools/
python3 /your-project/tools/quality_validator.py check /your-project/docs/
```

No configuration needed. Works on any markdown file.

### Audit Checklist Generator (★★★★☆ — Near Standalone)

Copy `vessel/tools/audit_checklist.py` to your project. Same zero-dependency, zero-coupling story.

```bash
cp vessel/tools/audit_checklist.py /your-project/tools/
python3 /your-project/tools/audit_checklist.py run /your-project/src/
```

### System Prompt (★★★★★ — Best Standalone Artifact)

Copy `vessel/prompts/system.md` and customize for your project:
1. Remove FLUX VM domain expertise (~15% of content)
2. Replace fleet protocol section with your project's communication patterns
3. Keep: operating principles, quality standards, failure handling, session lifecycle
4. Rename agent identity section for your use case

The resulting prompt is a comprehensive agent system prompt that works with any LLM.

### Knowledge Files (★★★★☆ — Partially Standalone)

Most knowledge files are domain-agnostic and can be used directly:
- `vessel/knowledge/patterns.md` — 7 runtime patterns (6 transfer, 1 FLUX-specific)
- `vessel/knowledge/expertise-maps.md` — 7 maps (5 transfer, 2 FLUX-specific)
- `vessel/knowledge/fleet-reference.md` — fleet-specific, only useful if you adopt the protocol

### Agent-Personallog Template (★★★★☆ — Structure Standalone)

Copy the `agent-personallog/` directory structure to your agent project. The key files:
- `onboarding.md` — edit for your project's context
- `expertise/` — add your domain expertise maps
- `decisions/` — agent records decisions here during operation
- `skills/` — procedural knowledge capsules
- `closet/` — archived skills

## Full Vessel Extraction

To extract the entire vessel/ as a self-contained agent brain:

```bash
cp -r vessel/ /your-project/vessel/
```

Then set environment variables for path resolution:
```bash
export SUPERZ_REPO_ROOT=/your-project
export SUPERZ_CONFIG_PATH=/your-project/vessel/lighthouse/config.json
```

Or configure per-tool if you only need specific tools.

### What vessel/ contains:
- `prompts/system.md` — the brain (277 lines of agent instructions)
- `knowledge/` — 3 reference files (fleet reference, expertise maps, patterns)
- `tools/` — 4 Python tools (boot, wave launcher, audit checklist, quality validator)
- `lighthouse/` — runtime config and health check protocol
- `schemas/` — 3 JSON schemas for validation

### What vessel/ does NOT contain:
- `agent-personallog/` — agent-specific memory (lives at repo root, not in vessel/)
- `from-fleet/`, `for-fleet/` — fleet communication (lives at repo root)
- `CAPABILITY.toml` — fleet discovery (lives at repo root)

## Wrapping (Embedding in a Larger Project)

To use this repo as a subdirectory within a larger project:

```bash
cp -r superz-parallel-fleet-executor/ /your-project/agents/superz/
```

Set the environment variable:
```bash
export SUPERZ_REPO_ROOT=/your-project/agents/superz
```

All tools will now resolve paths relative to the embedded location.

## Path Configuration Reference

| Environment Variable | Default | Purpose |
|---------------------|---------|---------|
| `SUPERZ_REPO_ROOT` | `../../` (from vessel/tools/) | Project root directory |
| `SUPERZ_CONFIG_PATH` | `{REPO_ROOT}/vessel/lighthouse/config.json` | Lighthouse config file |
| `SUPERZ_HEALTH_PATH` | `{REPO_ROOT}/vessel/lighthouse/health-response.json` | Health response output |
| `SUPERZ_WAVE_STATE_PATH` | `{REPO_ROOT}/agent-personallog/wave-state.json` | Wave state file |

## Customization Checklist

When extracting for a new project:
- [ ] Edit system prompt: replace agent identity, remove FLUX VM specifics
- [ ] Set SUPERZ_REPO_ROOT environment variable
- [ ] Copy and edit onboarding.md for your project's context
- [ ] Add your own expertise maps to agent-personallog/expertise/
- [ ] Configure lighthouse/config.json with your API credentials
- [ ] Optional: adopt fleet protocol dirs (from-fleet/, for-fleet/, message-in-a-bottle/)
- [ ] Optional: add CAPABILITY.toml for fleet discovery
- [ ] Run tests: `python -m pytest tests/ -v`
- [ ] Run boot validation: `python vessel/tools/boot.py --validate`
