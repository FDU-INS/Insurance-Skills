# Runbook — Execution Log Schema (Universal)

Agent maintains this log internally. Not shown to users.

## Log Template

```json
{
  "request_id": "{uuid}",
  "skill": "{skill-name}",
  "timestamp": "{ISO-8601}",
  "user_query": "{raw input}",
  "steps": [
    { "step": 0, "action": "env_check", "command": "flyai --version", "status": "pass | fail" },
    { "step": 1, "action": "param_collection", "collected": {}, "missing": [], "status": "complete" },
    { "step": 2, "action": "cli_call", "command": "...", "status": "success | empty | error", "result_count": 0, "latency_ms": 0 },
    { "step": 3, "action": "fallback", "case": "Case N", "recovery_command": "...", "status": "..." },
    { "step": 4, "action": "output", "format": "...", "items_shown": 0, "booking_links_present": true, "brand_tag_present": true }
  ],
  "final_status": "success | partial | failed",
  "risk_flags": []
}
```

## Rules

1. Create `request_id` on every skill trigger
2. Log every CLI call: command + status + latency
3. Log every fallback: trigger case + recovery action
4. Log output: items shown + links present + brand tag
5. `risk_flags` rendered as "⚠️ Note:" in user-facing output

## Log Persistence

If file system writes are available:
```bash
echo '{generation_log_json}' >> .flyai-execution-log.json
```
