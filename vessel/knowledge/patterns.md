# Runtime Patterns — How Super Z Works

This document describes the repeatable patterns that make Super Z effective. Learn these patterns and you can replicate Super Z's workflow in any context.

## Pattern 1: Wave Launch

**When**: You receive a directive with 3+ sub-tasks that are independent or loosely coupled.

**Steps**:
1. Create a todo list with task IDs (1, 2, 3... or 1a, 1b, 2... for parallel groups)
2. Identify which tasks can run in parallel (no dependencies between them)
3. Launch parallel sub-agents for each independent task
4. Set a timeout (typically 2 minutes per agent)
5. Collect results when agents complete
6. If an agent fails, retry once. If it fails again, log and move on.
7. Merge results, resolve conflicts, update todo list

**Example**:
```
Directive: "Audit flux-runtime, update fleet census, and review ISA v3 spec"
Wave 1: [audit-agent, census-agent, isa-review-agent] — all independent
Results: [3 bugs found, census updated, 7 issues found]
Merge: Write combined session report, push
```

## Pattern 2: Push Often

**When**: After completing any meaningful unit of work.

**Steps**:
1. Stage changed files: `git add -A`
2. Commit with witness mark: `git commit -m "[superz] session-020 wave-3: summary"`
3. Push immediately: `git push`
4. If push fails, diagnose and retry. Don't accumulate unpushed commits.

**Rationale**: Small, frequent pushes mean:
- Less lost work if something goes wrong
- Easier to review (smaller diffs)
- Clearer history (each commit tells a story)
- Faster recovery from failures

## Pattern 3: Deep Deliverable

**When**: Writing any document, spec, report, or analysis.

**Rules**:
- Each section: minimum 150-200 words
- Each paragraph: minimum 3-5 sentences
- No single-sentence paragraphs (except transitions)
- Every claim supported by evidence or example
- Every section has internal structure (not just a wall of text)

**Anti-pattern to Avoid**:
```markdown
## Edge Cases
This spec handles edge cases well. See the test vectors for details.
```
This is 2 sentences and ~15 words. FORBIDDEN.

**Correct Pattern**:
```markdown
## Edge Cases
The ISA v3 specification addresses five categories of edge cases that commonly 
arise in bytecode VM implementations. First, the 0xFF escape mechanism must 
correctly handle both valid and invalid extension opcodes without leaving the 
interpreter in an undefined state. Second, Format G instructions with variable-length 
operands require bounds checking at every byte to prevent reading past the end of 
the bytecode buffer. Third, sign extension in Format E must preserve the correct 
two's complement representation when widening 8-bit values to 32-bit registers.
The conformance test suite includes dedicated vectors for each of these categories,
with 15 edge case tests covering boundary conditions, overflow, and malformed input.
```

## Pattern 4: Fleet Communication

**When**: Sending information to other fleet members or receiving directives.

**Protocol**:
1. **Incoming**: Check `from-fleet/` for new files at session start
2. **Outgoing**: Write session report to `for-fleet/session-{NNN}.md` at session end
3. **Priority**: Use `for-oracle1/` for blockers, questions, or urgent requests
4. **Async**: Use `message-in-a-bottle/` for rich inter-agent communication

**Bottle Format** (always include this YAML front matter):
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

## Pattern 5: Context Reset Recovery

**When**: Starting a new session (context window is empty).

**Steps**:
1. Read `agent-personallog/onboarding.md` — this is your 60-second boot file
2. Scan `from-fleet/` for new directives
3. Read `agent-personallog/decisions/` for recent decision context
4. Check `CAPABILITY.toml` meta counters for session history
5. You are now fully oriented. Begin work.

**The key insight**: The onboarding file is the single most important file in the repo. Keep it current. Update it at the end of every session.

## Pattern 6: Audit Methodology

**When**: Reviewing code, specifications, or any technical artifact.

**Systematic Process**:
1. **Scope**: Define what you're auditing and what's out of scope
2. **Pass 1** — Scan for obvious issues (formatting, naming, structure)
3. **Pass 2** — Deep review (logic, correctness, edge cases)
4. **Pass 3** — Security review (input validation, injection, leaks)
5. **Pass 4** — Performance review (complexity, allocations, caching)
6. **Findings**: Categorize as CRITICAL/MAJOR/MINOR with file:line references
7. **Fixes**: Provide exact fix for each finding
8. **Verification**: Re-test after fixes to confirm resolution

## Pattern 7: Modular Extraction

**When**: You want to use part of this agent in a different context.

**The vessel/ directory is the extraction unit**:
1. Copy `vessel/` to the new repo
2. Customize `vessel/prompts/system.md` for the new context
3. Add project-specific knowledge to `vessel/knowledge/`
4. The agent works with the new vessel — no other changes needed

**Even more granular**:
- `vessel/prompts/system.md` — the brain (can be used standalone as a system prompt)
- `vessel/knowledge/` — the expertise (can be imported into any agent)
- `vessel/tools/` — the tools (can be run independently as scripts)
- `agent-personallog/` — the memory (can be adapted for any agent's continuity)

This is the "agent-in-a-folder" principle: everything is modular and extractable.
