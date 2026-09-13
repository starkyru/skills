---
name: agent-signals
description: >-
  Sends a push signal to the user's devices (macOS menu-bar app, phone) through
  their agent-signals broker, via the `notify` MCP tool or plain HTTP. Use when
  the user says "notify me", "ping me", "alert me", "signal me", "send it to my
  mac/phone", asks to be told when a long task finishes, or when an agent
  finishes a long unattended task, becomes blocked on user input, or finds
  something the user asked to watch for.
---

# Agent Signals

Send a short signal to the user's devices through their personal agent-signals
broker. A signal is one JSON object; the broker fans it out to every connected
client (macOS menu-bar app notification banner, future iOS push).

## When to use

- A long or unattended task just finished — send `kind: "done"`.
- Blocked and need the user's reply/approval to continue — send `kind: "waiting"`.
- Found something the user asked to watch for (email, log line, price, PR review) — send `kind: "found"`.
- Hit a failure the user must know about — send `kind: "error"`.
- Do NOT signal routine progress. One signal per event the user cares about;
  never spam. Reserve `priority: "high"` for genuinely urgent items.

## Instructions

### Preferred path: MCP tool

If an MCP tool named `notify` is available (connector "agent-signals"), call it
directly:

```json
{
  "source": "<who is sending, e.g. claude-code, cowork, inbox-watcher>",
  "kind": "done",
  "title": "Deploy finished",
  "body": "All 3 services green. Health check 202.",
  "url": "https://github.com/OWNER/REPO/actions/runs/123"
}
```

Expected result text: `Signal delivered (id=…, kind=…).`

**Reaching Telegram vs the app.** A plain signal goes to the macOS app / SSE
only. To ALSO relay it to the user's Telegram, add `"relay": true` to the
payload (it's opt-in; absent/false = app only). Relay still requires the user to
have configured a bot + subscription in the dashboard.

### Get a reply back: the `ask` tool

When you need the user's decision/approval/input to continue and they may be away
from the machine, call the `ask` MCP tool instead of just printing a question. It
delivers the question to their Telegram and BLOCKS until they reply, returning
their answer as the tool result:

```json
{ "question": "Deploy to prod now, or wait for review?", "timeout_seconds": 180 }
```

Returns `User replied: <their text>`, or a no-reply notice on timeout. Keep the
question short and specific; use it only when an answer is actually required.

### Fallback path: HTTP POST

When the MCP tool is not connected, use curl. Credentials live in
`$HOME/.config/agent-signals/env` (written by the macOS app; defines
`AGENT_SIGNALS_URL` and `AGENT_SIGNALS_TOKEN`), or in the environment already.

```bash
. "$HOME/.config/agent-signals/env" 2>/dev/null || true
curl -sS -m 5 -X POST "${AGENT_SIGNALS_URL:-https://signals.ilia.to}/api/notify" \
  -H "authorization: Bearer ${AGENT_SIGNALS_TOKEN}" \
  -H "content-type: application/json" \
  -d '{"source":"claude-code","kind":"done","title":"Task finished"}'
```

Expected: HTTP 202 with `{"ok":true,"id":"…","ts":…}`.

Never echo, log, or commit `AGENT_SIGNALS_TOKEN`. Only source it into the
command's environment.

## Signal fields

| Field | Required | Constraints |
|-------|----------|-------------|
| `source` | yes | who sent it; ≤64 chars, stable per producer |
| `kind` | yes | `waiting` \| `done` \| `found` \| `info` \| `error` |
| `title` | yes | ≤200 chars — this is the notification headline, keep it short |
| `body` | no | ≤4000 chars — detail goes here, not in title |
| `session` | no | ≤200 chars — set to group related signals (notifications stack by it) |
| `url` | no | ≤2048 chars — include when there is one obvious link to open |
| `priority` | no | `low` \| `normal` (default) \| `high` |

## Edge cases

- `401 unauthorized` → token missing/wrong. Do not retry; tell the user to
  re-check the token (macOS app Settings, or the env file).
- `422 invalid signal` → payload violates a constraint above; the response
  lists the exact issues. Fix and resend once.
- Env file absent and no MCP tool → don't guess a token; report that signals
  are not configured on this machine and how to set them up (macOS app
  Settings → Save, or add the MCP connector).
- Broker unreachable → mention it and move on; a missed notification must
  never fail the surrounding task (note the `-m 5` timeout).
