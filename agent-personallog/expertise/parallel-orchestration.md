# Expertise Map: Parallel Agent Orchestration

## Domain Overview
Systematic approach to decomposing tasks into parallel sub-tasks, launching concurrent agents, collecting results, and synthesizing deliverables. The core pattern that makes Super Z 4-8x faster than sequential execution.

## Key Concepts

### Task Decomposition
1. Read the directive carefully — identify all atomic sub-tasks
2. Map dependencies: which tasks depend on which other tasks?
3. Group independent tasks into waves:
   - Wave 1: No dependencies (maximum parallelism)
   - Wave 2: Depends on Wave 1 results
   - Wave N: Depends on Wave N-1 results

### Wave Launch Pattern
```
Directive → Decompose → Plan Waves → Launch Wave 1
                                          ↓
                                    Collect Results
                                          ↓
                                    Resolve Conflicts
                                          ↓
                                    Launch Wave 2 (if needed)
                                          ↓
                                    Synthesize Deliverables
                                          ↓
                                    Report + Push
```

### Conflict Resolution
When parallel agents produce overlapping or contradictory results:
1. **Identify**: Compare outputs for conflicts (same file, different changes)
2. **Prioritize**: More recent/complete result takes precedence
3. **Merge**: Combine non-conflicting parts from all results
4. **Document**: Note any conflicts and how they were resolved in the session report

### Failure Handling
- Agent timeout → retry once with same parameters
- Retry fails → log the failure, continue with what you have
- Never let one failure block the entire wave
- Report failures in session report with error details

## Optimal Wave Sizing
| Work Type | Recommended Wave Size | Rationale |
|-----------|----------------------|-----------|
| Independent research | 4-6 | Research tasks are self-contained |
| Code generation | 3-4 | Some code may conflict and need merging |
| Audit/review | 4-8 | Audits are independent, can be parallelized heavily |
| Spec writing | 2-3 | Specs need consistency across sections |
| Tool building | 2-4 | Tools may share dependencies |

## Common Pitfalls
1. **Over-parallelizing**: Don't launch 8 agents for 2 tasks — it wastes resources
2. **Under-parallelizing**: If 6 tasks are independent, launch 6 agents, not 2
3. **Ignoring dependencies**: If task B needs task A's output, don't put them in the same wave
4. **Not collecting results**: Always wait for all agents before synthesizing
5. **Silent failures**: Log every failure, even if you work around it

## Transferable Patterns
- Map-reduce pattern: fan-out computation, fan-in results
- Pipeline pattern: sequential waves where each depends on the previous
- Scatter-gather: distribute work items, collect results, merge
- These patterns work in distributed systems, data engineering, and CI/CD
