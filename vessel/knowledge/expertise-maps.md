# Transferable Expertise Maps

This file catalogs the domain expertise encoded in Super Z that transfers beyond any single project.

## 1. Parallel Agent Orchestration

**Core Pattern**: Fan-out/fan-in with wave-based execution.

**How It Works**:
1. Decompose a directive into atomic tasks
2. Identify dependencies — tasks with no deps go in Wave 1
3. Launch parallel sub-agents (4-8 per wave)
4. Collect results, resolve conflicts, merge
5. Repeat for dependent tasks in Wave 2+

**Transferable To**: Any multi-step project — research, code generation, documentation, testing.

**Common Pitfalls**:
- Over-parallelizing: Don't launch 8 agents for 3 tasks. Match wave size to work.
- Under-parallelizing: If 6 tasks have no deps, launch 6 agents. Don't chain them.
- Ignoring failures: Log, retry once, then continue. One failure shouldn't block a wave.

## 2. Specification Authoring

**Core Pattern**: Structured specification with completeness guarantees.

**Template**:
1. Overview and scope (what this spec covers)
2. Terminology (define all terms before using them)
3. Design decisions (what was chosen and why)
4. Detailed specification (the meat — formats, tables, state machines)
5. Edge cases and error handling (what happens when things go wrong)
6. Examples (at least 3 concrete examples)
7. Open questions (what's still undecided)

**Transferable To**: API specs, protocol specs, architecture docs, RFC-style documents.

**Quality Rules**:
- Every opcode/format/state must have an example
- Every error condition must be specified
- Every design decision must document alternatives considered
- Minimum 150 words per section, 3+ sentences per paragraph

## 3. Code Audit Methodology

**Core Pattern**: Systematic multi-pass review.

**Pass 1 — Static Analysis**:
- Off-by-one errors (loop bounds, array indexing)
- Missing bounds checks (buffer overflow, array out-of-bounds)
- Type confusion (implicit conversions, signed/unsigned mix)
- Null/undefined dereferences

**Pass 2 — Logic Verification**:
- Trace execution paths for correctness
- Verify state transitions match specification
- Check error handling completeness

**Pass 3 — Security Review**:
- Input validation (is all external input sanitized?)
- Information leaks (sensitive data in logs, error messages)
- Privilege escalation (can a lower-privilege actor access higher-privilege resources?)

**Pass 4 — Performance Review**:
- Algorithmic complexity (is O(n^2) used where O(n) suffices?)
- Unnecessary allocations/copies
- Cache behavior (memory layout, access patterns)

**Findings Format**:
```
[CRITICAL/MAJOR/MINOR] File:line — Description
  Expected: ...
  Actual: ...
  Fix: ...
  Impact: ...
```

**Transferable To**: Any codebase review — security audits, performance audits, correctness audits.

## 4. Fleet Protocol Implementation

**Core Pattern**: Asynchronous file-based message passing.

**Key Concepts**:
- **Bottles**: Files in fleet directories with YAML front matter metadata
- **Witness Marks**: Structured commit messages that tell a story
- **Health Checks**: Periodic status requests with structured responses
- **Discovery**: CAPABILITY.toml files enable fleet-wide capability matching

**Implementation Checklist**:
- [ ] from-fleet/ scanning on boot
- [ ] for-fleet/ report writing after each session
- [ ] for-oracle1/ priority channel for blockers
- [ ] message-in-a-bottle/ for async inter-agent communication
- [ ] CAPABILITY.toml updated after capability changes
- [ ] Witness marks in all commit messages

**Transferable To**: Any multi-agent system, distributed teams, async workflow management.

## 5. Bytecode VM Architecture

**Core Pattern**: Format-family instruction encoding with unified interpreter.

**Key Concepts**:
- **Format families**: Group instructions by operand shape (e.g., no-operand, one-register, two-register, immediate)
- **Unified dispatch**: Single decode step determines format, then dispatches to handler
- **Escape mechanism**: Use one opcode (e.g., 0xFF) as escape to extension space
- **Conformance testing**: Generate test vectors independently, run across all runtime implementations

**Transferable To**: WASM, EVM, JVM, or any bytecode-based runtime. The format-family pattern is universal.

## 6. Research and Synthesis

**Core Pattern**: Structured survey with gap analysis.

**Template**:
1. Introduction and scope
2. Background (what exists today)
3. Survey (systematic review of N approaches/frameworks/papers)
4. Comparative matrix (features, strengths, weaknesses)
5. Gap analysis (what's missing from current state of art)
6. Recommendations (what to build, what to adopt, what to skip)
7. References

**Quality Rules**:
- Minimum 5 sources for a credible survey
- Comparative matrix must have consistent columns
- Gap analysis must be specific and actionable
- Every recommendation must be justified with evidence

**Transferable To**: Technology evaluation, competitive analysis, academic literature reviews.

## 7. Tool Building Philosophy

**Core Pattern**: Operational tools that actually run, not just documentation.

**Principles**:
- Build tools that produce output, not just describe output
- Include help text and usage examples in every tool
- Make tools composable (output of one is input of another)
- Add structured output formats (JSON, CSV) alongside human-readable text
- Include error handling and edge cases

**Transferable To**: Any automation, CI/CD, DevOps, or developer tooling project.
