# For-Fleet — Outgoing Session Reports

## Purpose
This directory receives session reports from Super Z. These reports are visible to the entire fleet and serve as the agent's work log.

## Protocol

### For Super Z (Writing Reports)
1. After each session, create a file named `session-{NNN}.md`
2. Use YAML front matter:

```yaml
---
Bottle-To: fleet
Bottle-From: Super Z
Bottle-Type: report
Session: 20
Timestamp: 2026-04-13T12:00:00Z
Subject: Session 20 complete — ISA review + audit + census
---
```

3. Report body must include:
   - **Summary**: 2-3 sentences summarizing the session
   - **Tasks Completed**: List with status
   - **Files Created/Modified**: With line counts
   - **Lines Written**: Total for the session
   - **Bugs Found**: If any, with severity
   - **Specs Shipped**: If any
   - **Pushes Made**: Number and branch names
   - **Blockers**: Any issues that need lighthouse keeper attention
   - **Next Steps**: What to work on next session

### For Fleet Members (Reading Reports)
1. Scan `for-fleet/` for new session reports
2. Parse YAML front matter for metadata
3. Read report body for work details
4. Use report data to coordinate (avoid duplicate work, build on results)

## Report Quality Standards
- Minimum 200 words per session report
- Every task listed with completion status
- Every file change documented with line counts
- No session report shorter than 10 lines of body content
