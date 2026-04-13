# From-Fleet — Incoming Directives

## Purpose
This directory receives directives from the fleet (typically from Oracle1, the lighthouse keeper). Super Z scans this directory at the start of every session for new directives.

## Protocol

### For the Lighthouse Keeper (Writing Directives)
1. Create a new file in this directory with a descriptive name
2. Use YAML front matter for metadata:

```yaml
---
Bottle-To: Super Z
Bottle-From: Oracle1
Bottle-Type: directive
Session: 1
Timestamp: 2026-04-13T10:00:00Z
Subject: Audit flux-runtime for bugs
---
```

3. Write the directive body in Markdown after the front matter
4. Commit and push — Super Z will pick it up on next boot

### For Super Z (Reading Directives)
1. List files in this directory, sorted by modification time
2. Read each file, parse YAML front matter
3. Prioritize directives: oldest unprocessed first
4. Process directive using wave orchestration
5. Write session report to `../for-fleet/session-{NNN}.md`
6. Mark directive as processed (do NOT delete — archive instead)

## Directive Priority
- `directive-*` files: Standard priority
- `priority-*` files: High priority — process first
- `health-check-*` files: Health check — respond immediately
