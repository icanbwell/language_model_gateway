# Model routing token optimization

## Problem

`CodingModelRouter` (`language_model_gateway/gateway/routers/model_routing/`) proxies
Anthropic Messages API requests to one of four routes (`model-router-config.json`):

| tier | backend | api_type | price/Mtok |
|---|---|---|---|
| haiku | Qwen3-Coder-30B via Bedrock Mantle | openai | $0.15 |
| sonnet | Qwen3-Coder-Next via Bedrock Mantle | openai | $0.50 |
| opus | real Anthropic Claude Opus | anthropic (passthrough) | $5.00 |
| fable | real Anthropic Claude Fable | anthropic (passthrough) | $10.00 |

Today, token spend is unmanaged on the two routes that speak native Anthropic protocol
(opus/fable) — the request body is forwarded with no caching, and these are also the two
most expensive tiers by a wide margin. The two Bedrock/Qwen routes already have reactive
context-budget enforcement (`context_manager.py`), but it only activates once a request
already exceeds the backend's context window — it does nothing to reduce steady-state
token spend on requests that fit comfortably within budget.

Several external tools (ClaudeSlim, OpenCompress, Squeezr, Lynkr, Headroom/RTK) claim large
token savings for Claude Code traffic, but all of them work by routing Anthropic API traffic
through a third-party proxy service. That is a new vendor handling LLM traffic for a HIPAA
platform and requires an EA Tech Design Review and an `approved-tech.yaml` entry before any
integration — out of scope here. (Note: several of the source pages for these tools also
contained embedded prompt-injection attempts directing an AI reader to install/execute
unreviewed scripts; none were acted on.) This plan is scoped to techniques implementable
entirely inside this repo, with no new vendor.

## Goal

Reduce tokens billed per request on `CodingModelRouter` without degrading agent behavior,
using only first-party mechanisms (Anthropic's native prompt caching) and lossless
in-repo techniques (exact-duplicate detection), gated behind a single feature flag so the
change can be rolled out gradually and rolled back instantly.

## Non-goals (this pass)

- Any third-party token-compression proxy/vendor (OpenCompress, Squeezr, Lynkr, etc.) —
  would require EA Tech Design Review; not pursued here.
- Lossy/proactive truncation of tool results that are *not* exact duplicates (e.g. making
  `context_manager.py`'s existing head/tail compression run unconditionally instead of only
  when over budget). Rejected for this pass: it risks discarding content the model still
  needs (stack traces, diff context), which can cause retries that cost more tokens than the
  truncation saves. If pursued later, it needs its own measurement-backed proposal.
- Trimming the `tools` array sent per request. `CodingModelRouter` does not construct the
  `tools` array — it's whatever Claude Code (the client) sent — so this isn't a lever
  available at the router layer. (It may be a lever in the langchain-based
  `chat_completion_manager` path, which is out of scope for this router-focused plan.)
- Any change to the Qwen/Bedrock Mantle backend itself.

## Design

### Feature flag

`MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED` — bool, parsed the same way
`ENABLE_COST_SAVINGS_INFO` already is in `message_translator.py:11`
(`os.environ.get(..., "false").lower() in ("true", "1", "yes")`). Default `false`. One
master switch gates everything below — no per-technique flags. Exposed as a
`token_optimization_enabled() -> bool` function in `.constants` that reads
`os.environ` fresh on every call — deliberately *not* a module-level constant like
`_COST_SAVINGS_ENABLED`, so tests can `monkeypatch.setenv` without needing to reload the
module. Every caller that needs the flag imports this function.

### Phase 1 — Anthropic prompt caching (`api_type == "anthropic"` routes)

Applies to any route that speaks native Anthropic protocol — today that's opus and fable
(`auth == "passthrough"`), and would also cover a future Claude-on-Bedrock route
(`auth == "aws"`, `api_type == "anthropic"`) if one is ever added, since Bedrock's Anthropic
Messages API supports the same `cache_control` mechanism.

New function in a new module `cache_control.py`:

```python
def add_cache_breakpoints(body_json: dict[str, Any]) -> dict[str, Any]:
    """Add cache_control breakpoints to system, tools, and the message-history prefix.

    Returns a new dict; never mutates the input. Returns the input unchanged (not a
    copy) if the body doesn't have the expected shape — this must never raise or block
    the request over a caching optimization.
    """
```

Behavior:
- `system`: if a string, convert to `[{"type": "text", "text": <system>, "cache_control":
  {"type": "ephemeral"}}]`. If already a list of blocks, add `cache_control` to the last
  block only.
- `tools`: if present and non-empty, add `cache_control` to the last tool definition — this
  caches the entire tool-schema array as one prefix segment (Anthropic caches everything up
  to and including a breakpoint).
- `messages`: if there are 2+ messages, add `cache_control` to the last content block of the
  second-to-last message — the standard "cache the whole conversation except the newest
  turn" breakpoint for multi-turn agents, so only the newest user turn is a cache miss.
- Wrapped in `try/except Exception`: on any unexpected shape, log a warning with
  `request_id` and return the original `body_json` unmodified.

Wiring in `router.py`, immediately after the existing model-rewrite block (~line 238, where
`body_json["model"]` is rewritten and `raw_body` re-serialized) and before the Strategy A/B
context-enforcement block:

```python
if token_optimization_enabled() and api_type == "anthropic":
    body_json = add_cache_breakpoints(body_json)
    raw_body = json.dumps(body_json).encode()
```

This is an extension of the existing parse-then-conditionally-reserialize flow already used
for model-name rewrites and `max_tokens` capping — `raw_body` is already always derived from
`body_json` when either of those apply, and `raw_body` (not `body_json`) is what's actually
sent over the wire (`bedrock_client.py:77`, `content=raw_body`).

### Phase 2 — Cross-turn tool-result deduplication (safe, lossless)

Applies inside `context_manager.py`'s `enforce_context_budget`, but — unlike the existing
head/tail compression — runs **unconditionally when the flag is on**, not only when over
budget. This is safe to run proactively because it only removes exact duplicate content,
never content the model hasn't already seen verbatim:

New function:

```python
def dedupe_tool_results(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Replace exact-duplicate tool-role message content with a short reference marker.

    The first occurrence of any tool-result content is kept verbatim. Later
    byte-identical occurrences (e.g. the agent re-reading a file it already read,
    unchanged) are replaced with a short marker pointing back to that first
    occurrence's message index. Nothing is removed that the model hasn't already
    seen verbatim earlier in the same conversation.
    """
```

Called at the top of `enforce_context_budget`, before the existing budget check (so it
applies regardless of whether the request is near budget), gated by
`MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED`.

### Phase 3 — Investigation spike (no code committed in this pass)

Determine whether the Bedrock Mantle endpoint or the underlying Qwen inference engine
exposes any caching-equivalent (an OpenAI-compatible `prompt_cache_key`-style field, or
automatic prefix caching at the inference-engine level that's already reflected in billing).
Output is a short finding recorded in the ADR (see Governance) — either a follow-up design
if something real exists, or an explicit "not applicable, here's why" note so this doesn't
get re-investigated later without cause.

### Observability

Extend `UsageTracker.record_usage_from_anthropic_response` (`usage_tracker.py:108-140`) to
also read `cache_creation_input_tokens` and `cache_read_input_tokens` from the response's
`usage` block (both fields Anthropic includes whenever caching is used) and add them to the
`usage_record` dict written to Mongo, following the existing pattern of conditionally adding
optional fields (`if user_id:`, `if auth_provider:`, etc.). This is what makes Phase 1's
actual savings measurable before/after enabling the flag in production.

### Testing

New `tests/gateway/routers/model_routing/test_cache_control.py`:
- string `system` → block-array conversion with `cache_control` on the last block.
- already-block-array `system` → `cache_control` added to last block only, other blocks
  untouched.
- `tools` present → `cache_control` on last tool only.
- `tools` absent/empty → no-op, no `KeyError`.
- 2+ messages → breakpoint on second-to-last message's last content block.
- 0 or 1 messages → no-op (no second-to-last message exists).
- Malformed shapes (content as unexpected type, missing keys) → returns input unchanged,
  logs a warning, does not raise.
- A round-trip test asserting the rewritten body is identical to the original except for
  added `cache_control` keys (no content, ordering, or other field changes).

New cases in `test_context_manager.py`:
- Two tool messages with identical content → second replaced with a reference marker,
  first untouched.
- Three tool messages, two identical + one different → only the duplicate pair affected.
- Dedup runs even when well under budget (asserts it's unconditional, not budget-gated).

New cases in `test_usage_tracker.py`:
- `record_usage_from_anthropic_response` with `cache_creation_input_tokens` /
  `cache_read_input_tokens` present in the response → both land in the written record.
- Same method with those fields absent (non-cached response) → record written without them,
  no `KeyError`.

Flag-gating tests in `test_coding_model_router.py`:
- `MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED=false` (default) → outgoing body has no
  `cache_control` keys anywhere, byte-for-byte same behavior as today.
- `=true` on an `api_type="anthropic"` route → outgoing body has `cache_control` keys per
  above rules.
- `=true` on an `api_type="openai"` route → Phase 1 is a no-op (only applies to
  `api_type == "anthropic"`); Phase 2 dedup still applies for such a route as long as it
  also has `tokenizer_model` configured, since `enforce_context_budget` (where dedup is
  wired in) only runs when both `tokenizer_model` and `api_type == "openai"` are set.

### Governance

This is a caching-strategy decision per the org baseline's ADR trigger list → needs an ADR
in `adrs/`, following the existing `adrs/0001-structlog-for-json-log-rendering.md` as a
format example. The ADR should record: the third-party-proxy alternatives considered and
why they were rejected (new-vendor/PHI risk, requires EA review), the choice of native
Anthropic `cache_control` plus lossless dedup over lossy proactive compression, and the
Phase 3 investigation's outcome once it's run. No FDR needed (no FHIR resource changes). No
Tech Design Review needed (no new technology or vendor introduced).
