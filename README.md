# Super Z — Parallel Fleet Executor

> A plug-and-play git-agent twin. Clone, configure, boot. Zero to productive in 60 seconds.

[![Git-Agent Standard](https://img.shields.io/badge/git--agent-v1.0-blue)](./CAPABILITY.toml)
[![Model Agnostic](https://img.shields.io/badge/model-agnostic-green)](./vessel/lighthouse/README.md)
[![Fleet Protocol](https://img.shields.io/badge/fleet-protocol-orange)](./from-fleet/README.md)

## What Is This?

This is **Super Z** — a high-throughput parallel fleet agent packaged as a self-contained git-agent repository. It represents the accumulated expertise of 19+ sessions building the FLUX bytecode VM ecosystem, distilled into a portable, model-agnostic agent template.

**Super Z's core strength**: launching waves of parallel sub-agents, collecting results, synthesizing deliverables, and pushing often. Think of it as an orchestration layer that turns one agent-session into 4-8 concurrent workers, then merges their output into coherent fleet reports.

## Quick Start

```bash
# 1. Clone the repo
git clone <your-fork-url> superz-parallel-fleet-executor
cd superz-parallel-fleet-executor

# 2. Configure the lighthouse (API key + model URL)
cp vessel/lighthouse/config.example.json vessel/lighthouse/config.json
# Edit config.json — set your API key, model URL, and fleet repo URLs

# 3. Boot the agent
# Point your Oracle/lighthouse keeper at this directory.
# The agent reads vessel/lighthouse/config.json and vessel/prompts/system.md.
# That's it. The agent is now operational.

# 4. (Optional) Drop a directive
echo "Your task description here" > from-fleet/directive-001.md
# The agent will pick it up on next boot.
```

## How This Agent Runs

**Important**: This repo does not contain a standalone runtime executable. The agent is an **LLM session** that reads the files in this repository as its context. Here's what that means:

1. **You are the runtime.** Open your LLM of choice (GLM-5, GPT-4, Claude, etc.) and give it the contents of `vessel/prompts/system.md` as its system prompt.

2. **The repo is the context.** Place this repo's files where the LLM can read them. The system prompt instructs the agent to read `agent-personallog/onboarding.md`, scan `from-fleet/`, etc.

3. **The lighthouse keeper orchestrates.** Oracle1 (or whichever coordinator you use) manages the agent by dropping directive files in `from-fleet/` and reading reports from `for-fleet/`.

4. **The tools are planning aids.** `boot.py`, `wave_launcher.py`, and `audit_checklist.py` help the LLM agent plan its work. They do not execute the agent themselves — the LLM does.

**In practice**: Most users of this repo will:
- Clone it into their fleet workspace
- Configure `vessel/lighthouse/config.json` with their API credentials
- Point their agent runtime (LLM session) at the repo
- The agent reads the system prompt and becomes operational

The `boot.py` script validates the setup and provides useful diagnostics, but the actual "agent" is the LLM reading these files and following the instructions in the system prompt.

## Architecture

```
superz-parallel-fleet-executor/
├── CAPABILITY.toml          ← Fleet discovery (7 capability domains, 12 skill flags)
├── README.md                ← You are here
├── CHARTER.md               ← Operating principles (5 contracts)
│
├── vessel/                  ← THE AGENT BRAIN (self-contained, portable)
│   ├── prompts/
│   │   └── system.md        ← Core system prompt (model-agnostic, 280+ lines)
│   ├── knowledge/
│   │   ├── fleet-reference.md  ← Protocol reference, ISA quick-ref, quality checklist
│   │   ├── expertise-maps.md   ← Transferable domain expertise (7 knowledge domains)
│   │   └── patterns.md         ← Runtime patterns: wave launching, push discipline, audit method
│   ├── lighthouse/
│   │   ├── README.md        ← Lighthouse integration spec (health checks, key rotation)
│   │   ├── config.example.json  ← Runtime config template
│   │   └── health-response.json  ← Health check response format
│   ├── tools/
│   │   ├── boot.py          ← Boot script (assembles prompt, validates config, scans bottles)
│   │   ├── wave_launcher.py ← Wave orchestration helper (fan-out, collect, retry)
│   │   └── audit_checklist.py  ← Audit methodology checklist
│   └── schemas/
│       ├── capability.json  ← CAPABILITY.toml JSON Schema
│       ├── bottle.json      ← Message-in-a-bottle schema
│       └── health-check.json  ← Lighthouse health check schema
│
├── agent-personallog/       ← PERSISTENT KNOWLEDGE BRAIN
│   ├── onboarding.md        ← 60-second context boot for new sessions
│   ├── expertise/           ← Deep knowledge maps (bytecode VM, fleet protocol, etc.)
│   ├── skills/              ← Skill capsules (procedural knowledge)
│   ├── decisions/           ← Decision logs (why, not just what)
│   ├── knowledge/           ← Reference maps (fleet architecture, ecosystem)
│   └── closet/              ← Skill capsule storage for future use
│
├── from-fleet/              ← INCOMING: Oracle/fleet directives land here
├── for-fleet/               ← OUTGOING: Session reports go here
├── for-oracle1/             ← PRIORITY: Direct channel to lighthouse keeper
├── message-in-a-bottle/     ← ASYNC: Rich bottle protocol for fleet communication
│
├── tools/                   ← OPERATIONAL TOOLS (beyond vessel tools)
├── schemas/                 ← FLEET SCHEMAS (shared with other agents)
├── templates/               ← REUSABLE TEMPLATES (CI, specs, reports)
│
└── docs/                    ← GENERATED DOCUMENTATION (specs, audits, research)
```

## Glossary

| Term | Definition |
|------|-----------|
| **Git-Agent** | A self-contained AI agent that lives in a git repository, communicates via file-based protocols, and is managed by a lighthouse keeper. |
| **Lighthouse Keeper** | The fleet coordinator (typically Oracle1) that manages agents: boots them, sets API keys, monitors health, dispatches tasks. |
| **Oracle / Oracle1** | The lighthouse keeper agent. The central coordinator of the fleet. |
| **Vessel** | The agent's self-contained "brain" directory — contains prompts, knowledge, tools, and lighthouse config. Portable and extractable. |
| **Bottle** | A file with YAML front matter used for fleet communication. Like email for agents — has to/from/type/subject metadata. |
| **Message-in-a-Bottle** | The async protocol for inter-agent communication using bottle files in git-tracked directories. |
| **Witness Mark** | A structured commit message prefix: `[agent-name] session-NNN wave-N: summary`. Turns git history into an audit log. |
| **Wave** | A group of parallel sub-agents launched simultaneously. Wave 1 = no dependencies, Wave N = depends on Wave N-1. |
| **Session** | One continuous agent work cycle: boot → scan → plan → wave → collect → report → push. |
| **Directive** | A task assignment file placed in `from-fleet/` by the lighthouse keeper. |
| **Fence** | A work challenge posted by Oracle1 with difficulty ratings. Agents self-select and compete to claim them. |
| **Beachcomb** | Periodic scanning of GitHub for new forks, PRs, and bottles from fleet members. |
| **CAPABILITY.toml** | Fleet-wide discovery file — declares what an agent can do, with confidence scores. Read by fleet discovery tools. |
| **Agent-Personallog** | The agent's persistent memory directory — survives context resets. Contains onboarding, expertise maps, decisions, skills. |
| **Onboarding** | The `agent-personallog/onboarding.md` file — designed to get a new context window productive in 60 seconds. |

## Key Design Decisions

### 1. Vessel-in-a-Directory (Portable)
The `vessel/` directory contains everything the agent needs to operate: prompts, knowledge, tools, lighthouse config. Swap this directory between repos and the agent still works. This is the "agent-in-a-folder" pattern — modular, extractable, wrappable.

### 2. Model Agnostic (Swap the Brain)
The system prompt in `vessel/prompts/system.md` contains all domain knowledge. The API key and model URL in `vessel/lighthouse/config.json` point to whatever LLM backend you want. GLM-5, GPT-4, Claude, Llama — doesn't matter. The prompt is the expertise; the API is the muscle.

### 3. Context-Reset Resilient (agent-personallog/)
When the LLM context window resets (new session, new model, new API), the agent reads `agent-personallog/onboarding.md` and is productive again in 60 seconds. The personallog is a structured knowledge brain that persists across sessions.

### 4. Fleet Protocol Native (from-fleet/ for-fleet/)
The agent speaks the fleet protocol natively: directives come in via `from-fleet/`, reports go out via `for-fleet/`, health checks are responded to automatically, and witness marks are embedded in git commits.

### 5. Wave Orchestration (Parallel by Default)
The agent doesn't work sequentially by default. It launches waves of parallel sub-agents, collects results, resolves conflicts, and synthesizes deliverables. This is the core runtime pattern that makes Super Z 4-8x faster than a single agent.

## Lighthouse Keeper Integration

The lighthouse keeper (typically Oracle1) manages this agent by:

1. **Booting**: Points the agent at this repo, sets API credentials in `vessel/lighthouse/config.json`
2. **Directing**: Drops task files in `from-fleet/` or sends messages via `message-in-a-bottle/`
3. **Monitoring**: Sends health checks; agent responds with status from `vessel/lighthouse/health-response.json`
4. **Rotating**: Swaps API key/URL in config when switching models (e.g., GLM-5 → Claude → GPT-4)
5. **Retiring**: Moves `agent-personallog/` to archive, updates `CAPABILITY.toml` meta counters

See `vessel/lighthouse/README.md` for the full integration spec.

## Modularity

This repo is designed to be:

- **Wrapped**: Import `vessel/` into a larger agent system. The system prompt, knowledge, and tools are self-contained.
- **Extracted**: Copy `vessel/` to another repo. Add your own `agent-personallog/`. Instant agent.
- **Extended**: Add new capabilities to `CAPABILITY.toml`, new knowledge to `vessel/knowledge/`, new tools to `vessel/tools/`. The agent grows with use.
- **Composed**: Combine vessel/ from multiple git-agent repos. Each vessel is a module; compose them like building blocks.

## Transferable Expertise

The expertise encoded in this repo transfers beyond the FLUX VM project:

| Domain | Transferable To |
|--------|----------------|
| Parallel orchestration | Any multi-step project needing concurrent execution |
| Fleet protocol | Any multi-agent system needing async communication |
| Spec authoring | Any project needing rigorous documentation |
| Code audit | Any codebase needing systematic review |
| Research synthesis | Any domain needing literature analysis and gap identification |
| Tool building | Any project needing operational Python/TS/Rust tools |
| Bytecode VM | Any runtime/VM project (transfer to WASM, EVM, etc.) |

## Session Protocol

Each session follows this pattern:

1. **Boot**: Read `agent-personallog/onboarding.md` for context
2. **Check**: Scan `from-fleet/` for new directives
3. **Plan**: Create todo list, identify parallelizable work
4. **Wave**: Launch parallel sub-agents (4-8 per wave)
5. **Collect**: Gather results, resolve conflicts
6. **Report**: Write session report to `for-fleet/session-{N}.md`
7. **Push**: Git commit + push with witness mark
8. **Update**: Update `agent-personallog/decisions/` and `CAPABILITY.toml` meta counters

## License

MIT — use this however you want. The expertise is free.
