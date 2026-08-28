# Model Routing Token Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce billed tokens on `CodingModelRouter`'s two Anthropic-protocol routes (opus/fable — the two most expensive tiers) via native Anthropic prompt caching, plus a lossless cross-turn tool-result dedup on the Bedrock/Qwen routes — all gated behind one feature flag with zero behavior change when off.

**Architecture:** Two new small modules (`cache_control.py`, an addition to `context_manager.py`) wired into the existing `proxy_messages` request path in `router.py`, gated by a single env-var-driven flag read fresh on each check (not frozen at import) so it's trivially testable with `monkeypatch.setenv`. `usage_tracker.py` gains two optional fields to make savings measurable.

**Tech Stack:** Python 3.12, FastAPI/Starlette, httpx, pytest + pytest-asyncio + pytest-httpx (existing stack — no new dependencies).

## Global Constraints

- No new dependencies, no new vendor/service — everything is either a native Anthropic Messages API field (`cache_control`) or in-repo logic. (Per the approved spec: third-party token-compression proxies are explicitly out of scope — they'd require an EA Tech Design Review.)
- Feature flag `MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED` defaults to `"false"` — every new behavior in this plan must be a no-op until the flag is explicitly set to a truthy value (`"true"`, `"1"`, or `"yes"`, matching the existing `ENABLE_COST_SAVINGS_INFO` parsing convention in `message_translator.py:11`).
- Nothing in this plan may raise out of the request path or change response status codes — caching/dedup are optimizations; a bug in them must degrade to today's behavior (fail open), never fail a request.
- Every behavioral change ships with tests in the same task (per repo convention — every existing module here has a matching `test_*.py`).
- Commit messages in this repo must start with a JIRA issue key (see `CLAUDE.md`) — if none exists yet for this work, that must be created before the first commit in Task 1. This plan writes the commit steps as illustrative `git commit -m "<JIRA-KEY> ..."` — substitute the real key when executing.

---

## Task 1: Feature-flag helper

**Files:**
- Modify: `language_model_gateway/gateway/routers/model_routing/constants.py`
- Test: `tests/gateway/routers/model_routing/test_constants.py` (new file)

**Interfaces:**
- Produces: `token_optimization_enabled() -> bool` — reads `MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED` from `os.environ` fresh on every call (deliberately *not* a module-level constant like `_COST_SAVINGS_ENABLED`, so tests can `monkeypatch.setenv` without needing to reload the module). Every later task that needs the flag imports this function from `.constants`.

- [ ] **Step 1: Write the failing test**

Create `tests/gateway/routers/model_routing/test_constants.py`:

```python
from __future__ import annotations

from language_model_gateway.gateway.routers.model_routing.constants import (
    token_optimization_enabled,
)


def test_token_optimization_disabled_by_default(monkeypatch) -> None:
    monkeypatch.delenv("MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED", raising=False)
    assert token_optimization_enabled() is False


def test_token_optimization_enabled_true(monkeypatch) -> None:
    monkeypatch.setenv("MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED", "true")
    assert token_optimization_enabled() is True


def test_token_optimization_enabled_1(monkeypatch) -> None:
    monkeypatch.setenv("MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED", "1")
    assert token_optimization_enabled() is True


def test_token_optimization_enabled_yes(monkeypatch) -> None:
    monkeypatch.setenv("MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED", "yes")
    assert token_optimization_enabled() is True


def test_token_optimization_disabled_false(monkeypatch) -> None:
    monkeypatch.setenv("MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED", "false")
    assert token_optimization_enabled() is False


def test_token_optimization_disabled_garbage(monkeypatch) -> None:
    monkeypatch.setenv("MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED", "banana")
    assert token_optimization_enabled() is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/gateway/routers/model_routing/test_constants.py -v`
Expected: FAIL with `ImportError: cannot import name 'token_optimization_enabled'`

- [ ] **Step 3: Write minimal implementation**

In `language_model_gateway/gateway/routers/model_routing/constants.py`, add `import os` to the existing imports and append at the end of the file:

```python
def token_optimization_enabled() -> bool:
    """Master switch for all token-optimization behavior in model_routing.

    Read fresh on every call (not cached at import time) so tests can flip it
    with `monkeypatch.setenv` without reloading this module. Defaults to
    disabled — every optimization gated on this must be a no-op until an
    operator explicitly opts in.
    """
    return os.environ.get(
        "MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED", "false"
    ).lower() in ("true", "1", "yes")
```

The top of `constants.py` becomes:

```python
from __future__ import annotations

import os
import re
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/gateway/routers/model_routing/test_constants.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
git add language_model_gateway/gateway/routers/model_routing/constants.py tests/gateway/routers/model_routing/test_constants.py
git commit -m "<JIRA-KEY> Add MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED feature flag"
```

---

## Task 2: `cache_control.py` — Anthropic prompt-caching breakpoint injection

**Files:**
- Create: `language_model_gateway/gateway/routers/model_routing/cache_control.py`
- Test: `tests/gateway/routers/model_routing/test_cache_control.py` (new file)

**Interfaces:**
- Consumes: nothing from other tasks (pure function over a plain dict).
- Produces: `add_cache_breakpoints(body_json: dict[str, Any], request_id: str = "") -> dict[str, Any]` — used by Task 3.

- [ ] **Step 1: Write the failing tests**

Create `tests/gateway/routers/model_routing/test_cache_control.py`:

```python
from __future__ import annotations

import copy
from typing import Any

from language_model_gateway.gateway.routers.model_routing.cache_control import (
    add_cache_breakpoints,
)

_CACHE_CONTROL = {"type": "ephemeral"}


def test_string_system_converted_to_cached_block() -> None:
    body = {"model": "claude-opus-4-8", "system": "You are helpful.", "messages": []}

    result = add_cache_breakpoints(body)

    assert result["system"] == [
        {"type": "text", "text": "You are helpful.", "cache_control": _CACHE_CONTROL}
    ]


def test_block_array_system_gets_cache_control_on_last_block_only() -> None:
    body = {
        "model": "claude-opus-4-8",
        "system": [{"type": "text", "text": "part 1"}, {"type": "text", "text": "part 2"}],
        "messages": [],
    }

    result = add_cache_breakpoints(body)

    assert result["system"][0] == {"type": "text", "text": "part 1"}
    assert result["system"][1] == {
        "type": "text",
        "text": "part 2",
        "cache_control": _CACHE_CONTROL,
    }


def test_no_system_is_a_noop_for_system() -> None:
    body = {"model": "claude-opus-4-8", "messages": []}

    result = add_cache_breakpoints(body)

    assert "system" not in result


def test_tools_get_cache_control_on_last_tool_only() -> None:
    body = {
        "model": "claude-opus-4-8",
        "tools": [{"name": "read_file"}, {"name": "write_file"}],
        "messages": [],
    }

    result = add_cache_breakpoints(body)

    assert result["tools"][0] == {"name": "read_file"}
    assert result["tools"][1] == {"name": "write_file", "cache_control": _CACHE_CONTROL}


def test_empty_tools_is_a_noop() -> None:
    body = {"model": "claude-opus-4-8", "tools": [], "messages": []}

    result = add_cache_breakpoints(body)

    assert result["tools"] == []


def test_missing_tools_is_a_noop() -> None:
    body = {"model": "claude-opus-4-8", "messages": [{"role": "user", "content": "hi"}]}

    result = add_cache_breakpoints(body)

    assert "tools" not in result


def test_two_plus_messages_gets_breakpoint_on_second_to_last_string_content() -> None:
    body = {
        "model": "claude-opus-4-8",
        "messages": [
            {"role": "user", "content": "turn 1"},
            {"role": "assistant", "content": "turn 1 reply"},
            {"role": "user", "content": "turn 2 (newest)"},
        ],
    }

    result = add_cache_breakpoints(body)

    # second-to-last message (index -2) is the assistant reply; it becomes a
    # cached block, the newest user turn (index -1) is untouched.
    assert result["messages"][1]["content"] == [
        {"type": "text", "text": "turn 1 reply", "cache_control": _CACHE_CONTROL}
    ]
    assert result["messages"][2] == {"role": "user", "content": "turn 2 (newest)"}
    assert result["messages"][0] == {"role": "user", "content": "turn 1"}


def test_two_plus_messages_block_array_content_gets_breakpoint_on_last_block() -> None:
    body = {
        "model": "claude-opus-4-8",
        "messages": [
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "a"},
                    {"type": "tool_use", "id": "t1", "name": "read_file", "input": {}},
                ],
            },
            {"role": "user", "content": "newest"},
        ],
    }

    result = add_cache_breakpoints(body)

    second_to_last_content = result["messages"][0]["content"]
    assert second_to_last_content[0] == {"type": "text", "text": "a"}
    assert second_to_last_content[1] == {
        "type": "tool_use",
        "id": "t1",
        "name": "read_file",
        "input": {},
        "cache_control": _CACHE_CONTROL,
    }


def test_zero_or_one_messages_is_a_noop_for_messages() -> None:
    body = {"model": "claude-opus-4-8", "messages": [{"role": "user", "content": "only one"}]}

    result = add_cache_breakpoints(body)

    assert result["messages"] == [{"role": "user", "content": "only one"}]


def test_empty_messages_is_a_noop() -> None:
    body = {"model": "claude-opus-4-8", "messages": []}

    result = add_cache_breakpoints(body)

    assert result["messages"] == []


def test_second_to_last_message_with_unexpected_content_shape_is_skipped_safely() -> None:
    body = {
        "model": "claude-opus-4-8",
        "system": "cache me",
        "messages": [
            {"role": "user", "content": None},
            {"role": "user", "content": "newest"},
        ],
    }

    result = add_cache_breakpoints(body)

    # system still got its breakpoint; messages left untouched since content
    # shape (None) isn't str or a non-empty list.
    assert result["system"][0]["cache_control"] == _CACHE_CONTROL
    assert result["messages"][0] == {"role": "user", "content": None}


def test_does_not_mutate_input() -> None:
    body: dict[str, Any] = {
        "model": "claude-opus-4-8",
        "system": "sys",
        "tools": [{"name": "t"}],
        "messages": [{"role": "user", "content": "a"}, {"role": "user", "content": "b"}],
    }
    original = copy.deepcopy(body)

    add_cache_breakpoints(body)

    assert body == original


def test_malformed_body_fails_open() -> None:
    # `tools` is not a list of dicts here — indexing/`.get` on a string would
    # raise; add_cache_breakpoints must catch that and return the input as-is.
    body = {"model": "claude-opus-4-8", "tools": "not-a-list", "messages": []}

    result = add_cache_breakpoints(body)

    assert result == body
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/gateway/routers/model_routing/test_cache_control.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named '...cache_control'`

- [ ] **Step 3: Write minimal implementation**

Create `language_model_gateway/gateway/routers/model_routing/cache_control.py`:

```python
"""
Anthropic prompt-caching breakpoint injection for api_type=="anthropic" routes.

Adds cache_control: {"type": "ephemeral"} to the last block of `system`, the
last entry of `tools`, and the last content block of the second-to-last
message — the standard "cache everything except the newest turn" pattern for
multi-turn agents. Anthropic allows up to 4 cache_control breakpoints per
request; this uses at most 3.

Gated by MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED at the call site (router.py),
not in this module — this module is a pure transform with no env-var reads.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

_CACHE_CONTROL: dict[str, str] = {"type": "ephemeral"}


def add_cache_breakpoints(
    body_json: dict[str, Any], request_id: str = ""
) -> dict[str, Any]:
    """
    Add cache_control breakpoints to system, tools, and the message-history
    prefix of an Anthropic Messages API request body.

    Returns a new dict; never mutates body_json. On any unexpected shape (a
    field that isn't the type the Anthropic API contract promises), logs a
    warning and returns body_json unchanged — a caching optimization must
    never raise or block a request.
    """
    try:
        result: dict[str, Any] = dict(body_json)

        if system := result.get("system"):
            if isinstance(system, str):
                result["system"] = [
                    {
                        "type": "text",
                        "text": system,
                        "cache_control": dict(_CACHE_CONTROL),
                    }
                ]
            elif isinstance(system, list):
                new_system = [dict(block) for block in system]
                new_system[-1]["cache_control"] = dict(_CACHE_CONTROL)
                result["system"] = new_system

        if tools := result.get("tools"):
            new_tools = [dict(tool) for tool in tools]
            new_tools[-1]["cache_control"] = dict(_CACHE_CONTROL)
            result["tools"] = new_tools

        messages = result.get("messages")
        if isinstance(messages, list) and len(messages) >= 2:
            breakpoint_msg = dict(messages[-2])
            content = breakpoint_msg.get("content")
            new_content: list[Any] | None = None
            if isinstance(content, str):
                new_content = [
                    {
                        "type": "text",
                        "text": content,
                        "cache_control": dict(_CACHE_CONTROL),
                    }
                ]
            elif isinstance(content, list) and content:
                new_content = [dict(block) for block in content]
                new_content[-1]["cache_control"] = dict(_CACHE_CONTROL)

            if new_content is not None:
                breakpoint_msg["content"] = new_content
                new_messages = list(messages)
                new_messages[-2] = breakpoint_msg
                result["messages"] = new_messages

        return result
    except Exception:
        logger.warning(
            "[cache_control] failed to add cache breakpoints; forwarding "
            "request unmodified. request_id=%s",
            request_id,
            exc_info=True,
        )
        return body_json
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/gateway/routers/model_routing/test_cache_control.py -v`
Expected: 13 passed

- [ ] **Step 5: Commit**

```bash
git add language_model_gateway/gateway/routers/model_routing/cache_control.py tests/gateway/routers/model_routing/test_cache_control.py
git commit -m "<JIRA-KEY> Add Anthropic prompt-caching breakpoint injection"
```

---

## Task 3: Wire prompt caching into `CodingModelRouter.proxy_messages`

**Files:**
- Modify: `language_model_gateway/gateway/routers/model_routing/router.py`
- Test: `tests/gateway/routers/test_coding_model_router.py`

**Interfaces:**
- Consumes: `token_optimization_enabled()` from Task 1 (`.constants`), `add_cache_breakpoints()` from Task 2 (`.cache_control`).
- Produces: no new public interface — this task only changes `proxy_messages`'s outgoing request body under the flag.

- [ ] **Step 1: Write the failing tests**

Add to `tests/gateway/routers/test_coding_model_router.py` (append near the other passthrough tests, e.g. after `test_passthrough_route_forwards_auth_header`):

```python
async def test_cache_control_not_added_when_flag_disabled(
    router_client: httpx.AsyncClient,
    httpx_mock: HTTPXMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED", raising=False)
    fake_route = {
        "claude_model": "claude-cache-test",
        "url": "https://api.anthropic.com/v1/messages",
        "model": "claude-cache-test",
        "auth": "passthrough",
    }
    upstream_body = json.dumps(
        {
            "id": "msg_1",
            "type": "message",
            "role": "assistant",
            "content": [{"type": "text", "text": "ok"}],
            "model": "claude-cache-test",
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 1},
        }
    ).encode()
    httpx_mock.add_response(
        url="https://api.anthropic.com/v1/messages",
        method="POST",
        status_code=200,
        content=upstream_body,
        headers={"content-type": "application/json"},
    )

    with patch.dict(_ROUTES, {"claude-cache-test": fake_route}):
        body = {
            "model": "claude-cache-test",
            "system": "You are helpful.",
            "messages": [
                {"role": "user", "content": "turn 1"},
                {"role": "assistant", "content": "reply 1"},
                {"role": "user", "content": "turn 2"},
            ],
            "stream": False,
        }
        response = await router_client.post(
            "/v1/messages",
            json=body,
            headers={"content-type": "application/json", "authorization": "Bearer k"},
        )

    assert response.status_code == 200
    sent_body = json.loads(httpx_mock.get_requests()[0].content)
    assert sent_body["system"] == "You are helpful."
    assert "cache_control" not in json.dumps(sent_body)


async def test_cache_control_added_when_flag_enabled_on_anthropic_route(
    router_client: httpx.AsyncClient,
    httpx_mock: HTTPXMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED", "true")
    fake_route = {
        "claude_model": "claude-cache-test-2",
        "url": "https://api.anthropic.com/v1/messages",
        "model": "claude-cache-test-2",
        "auth": "passthrough",
    }
    upstream_body = json.dumps(
        {
            "id": "msg_1",
            "type": "message",
            "role": "assistant",
            "content": [{"type": "text", "text": "ok"}],
            "model": "claude-cache-test-2",
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 1},
        }
    ).encode()
    httpx_mock.add_response(
        url="https://api.anthropic.com/v1/messages",
        method="POST",
        status_code=200,
        content=upstream_body,
        headers={"content-type": "application/json"},
    )

    with patch.dict(_ROUTES, {"claude-cache-test-2": fake_route}):
        body = {
            "model": "claude-cache-test-2",
            "system": "You are helpful.",
            "tools": [{"name": "read_file", "input_schema": {}}],
            "messages": [
                {"role": "user", "content": "turn 1"},
                {"role": "assistant", "content": "reply 1"},
                {"role": "user", "content": "turn 2"},
            ],
            "stream": False,
        }
        response = await router_client.post(
            "/v1/messages",
            json=body,
            headers={"content-type": "application/json", "authorization": "Bearer k"},
        )

    assert response.status_code == 200
    sent_body = json.loads(httpx_mock.get_requests()[0].content)
    assert sent_body["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert sent_body["tools"][0]["cache_control"] == {"type": "ephemeral"}
    assert sent_body["messages"][1]["content"][0]["cache_control"] == {
        "type": "ephemeral"
    }
    # newest turn is untouched
    assert sent_body["messages"][2] == {"role": "user", "content": "turn 2"}


async def test_cache_control_not_added_on_openai_route_even_when_flag_enabled(
    router_client: httpx.AsyncClient,
    httpx_mock: HTTPXMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """cache_control is an Anthropic-protocol field; it must never be sent to
    the OpenAI-compatible Bedrock Mantle endpoint even when the flag is on."""
    monkeypatch.setenv("MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED", "true")
    fake_route = {
        "claude_model": "claude-oai-cache-test",
        "url": "https://bedrock-mantle.us-east-1.api.aws/v1/chat/completions",
        "model": "qwen.qwen3-coder-30b-a3b-v1:0",
        "auth": "aws",
        "aws_region": "us-east-1",
        "api_type": "openai",
        "context_window": 262144,
        "max_tokens": 1024,
    }
    with patch.dict(_ROUTES, {"claude-oai-cache-test": fake_route}):
        with patch(
            "language_model_gateway.gateway.routers.model_routing.router.add_cache_breakpoints"
        ) as mock_add_cache:
            httpx_mock.add_exception(httpx.ConnectError("no real network in test"))
            body = {
                "model": "claude-oai-cache-test",
                "system": "sys",
                "messages": [{"role": "user", "content": "hi"}],
                "stream": False,
            }
            await router_client.post(
                "/v1/messages",
                json=body,
                headers={"content-type": "application/json"},
            )
            mock_add_cache.assert_not_called()
```

Note on the third test: this repo has no existing test exercising the full
`api_type: openai` dispatch path end-to-end (only its translation *functions*
are unit-tested directly), so `test_cache_control_not_added_on_openai_route_even_when_flag_enabled`
is exploring new territory — the injected `httpx.ConnectError` propagates
through the `openai` SDK client and is expected to surface as a 500 from
FastAPI's default `ServerErrorMiddleware` rather than raising out of the
test. If this doesn't hold when actually run, replace the network-level
mock with a direct assertion instead: call `proxy_messages` isn't private-testable
that granularly, so fall back to patching `oai_client.chat.completions.create`
(via `unittest.mock.patch("openai.resources.chat.completions.AsyncCompletions.create")`)
to return a minimal fake response object instead of hitting the network at
all — the goal of this test (`add_cache_breakpoints` not called for
`api_type=="openai"`) is unaffected by which mocking approach reaches it.

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/gateway/routers/test_coding_model_router.py -k cache_control -v`
Expected: FAIL — `test_cache_control_added_when_flag_enabled_on_anthropic_route` and the noop test both fail because no `cache_control` handling exists yet in `router.py` (the "flag enabled" test fails its assertions; the "flag disabled" test currently passes coincidentally, but the third test fails on `mock_add_cache` — patch target doesn't exist yet, `AttributeError`).

- [ ] **Step 3: Write minimal implementation**

In `language_model_gateway/gateway/routers/model_routing/router.py`:

Add to the import block (near the other `.constants` and local imports, after the existing `from .constants import (...)` block, ~line 55-61):

```python
from .cache_control import add_cache_breakpoints
from .constants import (
    _ANTHROPIC_ONLY_HEADERS,
    _HOP_BY_HOP_HEADERS,
    _MAX_THROTTLE_RETRIES,
    _SKIP_HEADERS,
    _TOKEN_ESTIMATE_SAFETY_BUFFER,
    token_optimization_enabled,
)
```

Then insert this block right after the existing model-rewrite block and before the `# ── Context enforcement` comment (~line 239-241 in the current file):

```python
        # Rewrite model name if upstream differs
        if upstream_model != model:
            body_json["model"] = upstream_model
            raw_body = json.dumps(body_json).encode()

        # ── Token optimization: Anthropic prompt caching ──────────────────────
        # cache_control is an Anthropic-protocol field; only api_type=="anthropic"
        # routes (opus/fable passthrough today, and any future Claude-on-Bedrock
        # route) accept it. Bedrock Mantle/Qwen routes speak OpenAI's wire format
        # and would reject an unrecognized field.
        if token_optimization_enabled() and api_type == "anthropic":
            body_json = add_cache_breakpoints(body_json, request_id=request_id)
            raw_body = json.dumps(body_json).encode()

        # ── Context enforcement ───────────────────────────────────────────────
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/gateway/routers/test_coding_model_router.py -v`
Expected: all pass, including the 3 new cache_control tests and every pre-existing test in the file (no regressions)

- [ ] **Step 5: Commit**

```bash
git add language_model_gateway/gateway/routers/model_routing/router.py tests/gateway/routers/test_coding_model_router.py
git commit -m "<JIRA-KEY> Wire Anthropic prompt caching into CodingModelRouter passthrough"
```

---

## Task 4: Cross-turn tool-result deduplication in `context_manager.py`

**Files:**
- Modify: `language_model_gateway/gateway/routers/model_routing/context_manager.py`
- Test: `tests/gateway/routers/model_routing/test_context_manager.py`

**Interfaces:**
- Consumes: `token_optimization_enabled()` from Task 1 (`.constants`).
- Produces: `dedupe_tool_results(messages: list[dict[str, Any]]) -> list[dict[str, Any]]`, called unconditionally (when the flag is on) at the top of `enforce_context_budget`, before the existing budget check.

- [ ] **Step 1: Write the failing tests**

Add to `tests/gateway/routers/model_routing/test_context_manager.py` (append near the other compression tests; the file already defines `_msg` and `_tool_call_group` helpers — reuse them):

```python
from language_model_gateway.gateway.routers.model_routing.context_manager import (
    dedupe_tool_results,
)


def test_dedupe_keeps_first_occurrence_and_marks_later_duplicate() -> None:
    messages = [
        _msg("tool", "file contents: abc", tool_call_id="1"),
        _msg("user", "do something else"),
        _msg("tool", "file contents: abc", tool_call_id="2"),
    ]

    result = dedupe_tool_results(messages)

    assert result[0]["content"] == "file contents: abc"
    assert result[1] == messages[1]
    assert "duplicate of tool result at message index 0" in result[2]["content"]
    assert "file contents: abc" not in result[2]["content"]


def test_dedupe_leaves_distinct_tool_results_untouched() -> None:
    messages = [
        _msg("tool", "content A", tool_call_id="1"),
        _msg("tool", "content B", tool_call_id="2"),
    ]

    result = dedupe_tool_results(messages)

    assert result == messages


def test_dedupe_ignores_non_tool_messages() -> None:
    messages = [
        _msg("user", "same text"),
        _msg("assistant", "same text"),
    ]

    result = dedupe_tool_results(messages)

    assert result == messages


def test_dedupe_handles_three_occurrences() -> None:
    messages = [
        _msg("tool", "dup", tool_call_id="1"),
        _msg("tool", "dup", tool_call_id="2"),
        _msg("tool", "dup", tool_call_id="3"),
    ]

    result = dedupe_tool_results(messages)

    assert result[0]["content"] == "dup"
    assert "duplicate of tool result at message index 0" in result[1]["content"]
    assert "duplicate of tool result at message index 0" in result[2]["content"]


def test_dedupe_skips_non_string_or_empty_content() -> None:
    messages = [
        _msg("tool", "", tool_call_id="1"),
        {"role": "tool", "content": None, "tool_call_id": "2"},
    ]

    result = dedupe_tool_results(messages)

    assert result == messages


def test_dedupe_runs_unconditionally_even_when_well_under_budget(
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    monkeypatch.setenv("MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED", "true")
    route = {"tokenizer_model": None}
    oai_body = {
        "messages": [
            _msg("tool", "same content", tool_call_id="1"),
            _msg("user", "tiny request, nowhere near budget"),
            _msg("tool", "same content", tool_call_id="2"),
        ]
    }

    result = enforce_context_budget(oai_body, route, tokenizer_model="unused")

    tool_messages = [m for m in result["messages"] if m.get("role") == "tool"]
    assert tool_messages[0]["content"] == "same content"
    assert "duplicate of tool result" in tool_messages[1]["content"]


def test_dedupe_does_not_run_when_flag_disabled(
    monkeypatch: "pytest.MonkeyPatch",
) -> None:
    monkeypatch.delenv("MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED", raising=False)
    route = {"tokenizer_model": None}
    oai_body = {
        "messages": [
            _msg("tool", "same content", tool_call_id="1"),
            _msg("user", "tiny request"),
            _msg("tool", "same content", tool_call_id="2"),
        ]
    }

    result = enforce_context_budget(oai_body, route, tokenizer_model="unused")

    tool_messages = [m for m in result["messages"] if m.get("role") == "tool"]
    assert tool_messages[0]["content"] == "same content"
    assert tool_messages[1]["content"] == "same content"
```

Note: `test_dedupe_runs_unconditionally_even_when_well_under_budget` and
`test_dedupe_does_not_run_when_flag_disabled` call the real
`enforce_context_budget`, which calls `count_oai_request_tokens` — check the
existing tests in this file (they already exercise `enforce_context_budget`
without mocking the tokenizer, per the file's own docstring: "the tokenizer is
mocked so these tests run without downloading any HuggingFace model" — follow
whatever mocking pattern the existing tests in this file already use for
`tokenizer_model` so this doesn't attempt a real HuggingFace download).

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/gateway/routers/model_routing/test_context_manager.py -k dedupe -v`
Expected: FAIL with `ImportError: cannot import name 'dedupe_tool_results'`

- [ ] **Step 3: Write minimal implementation**

In `language_model_gateway/gateway/routers/model_routing/context_manager.py`:

Add to imports (after the existing `from .tokenizer import count_oai_request_tokens`):

```python
from .constants import token_optimization_enabled
```

Add the new function, placed after `_compress_tool_messages` (in the "Tool result compression" section) since it's conceptually adjacent:

```python
def dedupe_tool_results(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Replace exact-duplicate tool-role message content with a short reference marker.

    The first occurrence of any tool-result content is kept verbatim. Later
    byte-identical occurrences (e.g. the agent re-reading a file it already
    read, unchanged) are replaced with a short marker pointing back to that
    first occurrence's message index. Nothing is removed that the model
    hasn't already seen verbatim earlier in the same conversation, so this is
    safe to run unconditionally rather than only when over budget.
    """
    first_index: dict[str, int] = {}
    result: list[dict[str, Any]] = []
    for i, msg in enumerate(messages):
        content = msg.get("content")
        if msg.get("role") != "tool" or not isinstance(content, str) or not content:
            result.append(msg)
            continue
        if content not in first_index:
            first_index[content] = i
            result.append(msg)
        else:
            marker = (
                f"[duplicate of tool result at message index {first_index[content]}; "
                f"{len(content):,} chars omitted — content unchanged since then]"
            )
            result.append({**msg, "content": marker})
    return result
```

Modify `enforce_context_budget` to call it first, before `budget = build_budget(route)`:

```python
def enforce_context_budget(
    oai_body: dict[str, Any],
    route: dict[str, Any],
    tokenizer_model: str,
) -> dict[str, Any]:
    """
    ... (existing docstring unchanged) ...
    """
    if token_optimization_enabled():
        oai_body = {
            **oai_body,
            "messages": dedupe_tool_results(oai_body.get("messages", [])),
        }

    budget = build_budget(route)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/gateway/routers/model_routing/test_context_manager.py -v`
Expected: all pass, including every pre-existing test in the file (no regressions)

- [ ] **Step 5: Commit**

```bash
git add language_model_gateway/gateway/routers/model_routing/context_manager.py tests/gateway/routers/model_routing/test_context_manager.py
git commit -m "<JIRA-KEY> Add lossless cross-turn tool-result deduplication"
```

---

## Task 5: Capture cache token counts in `usage_tracker.py`

**Files:**
- Modify: `language_model_gateway/gateway/routers/model_routing/usage_tracker.py`
- Test: `tests/gateway/routers/model_routing/test_usage_tracker.py`

**Interfaces:**
- Consumes: nothing new from other tasks — this only reads two additional optional keys off the Anthropic response's existing `usage` dict.
- Produces: `record_usage` gains two new optional keyword parameters (`cache_creation_input_tokens`, `cache_read_input_tokens`); `record_usage_from_anthropic_response`'s behavior extends to pass them through when present.

- [ ] **Step 1: Write the failing tests**

Check `tests/gateway/routers/model_routing/test_usage_tracker.py` first for the existing test pattern for `record_usage_from_anthropic_response` (it should already construct a `UsageTracker` with a fake/mocked `_collection` and assert on the inserted document — follow that exact pattern). Add:

```python
async def test_record_usage_from_anthropic_response_captures_cache_tokens() -> None:
    tracker = UsageTracker(mongo_uri="mongodb://fake")
    tracker._collection = AsyncMock()  # bypass real Mongo connection

    response_body = {
        "usage": {
            "input_tokens": 100,
            "output_tokens": 50,
            "cache_creation_input_tokens": 20,
            "cache_read_input_tokens": 80,
        }
    }

    await tracker.record_usage_from_anthropic_response(
        request_id="req-1",
        auth_info={"user_id": "u1"},
        model="claude-opus-4-8",
        response_body=response_body,
    )

    inserted = tracker._collection.insert_one.call_args[0][0]
    assert inserted["cache_creation_input_tokens"] == 20
    assert inserted["cache_read_input_tokens"] == 80


async def test_record_usage_from_anthropic_response_without_cache_fields() -> None:
    tracker = UsageTracker(mongo_uri="mongodb://fake")
    tracker._collection = AsyncMock()

    response_body = {"usage": {"input_tokens": 100, "output_tokens": 50}}

    await tracker.record_usage_from_anthropic_response(
        request_id="req-2",
        auth_info={"user_id": "u1"},
        model="claude-opus-4-8",
        response_body=response_body,
    )

    inserted = tracker._collection.insert_one.call_args[0][0]
    assert "cache_creation_input_tokens" not in inserted
    assert "cache_read_input_tokens" not in inserted
```

(Match whichever async-mocking imports — e.g. `from unittest.mock import AsyncMock` — the rest of the file already uses; if the file already has a fixture/helper for a `UsageTracker` with a stubbed collection, use that helper instead of constructing `_collection` inline.)

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/gateway/routers/model_routing/test_usage_tracker.py -k cache_tokens -v`
Expected: FAIL — assertion errors (`KeyError`/`AssertionError`) since the fields aren't captured yet.

- [ ] **Step 3: Write minimal implementation**

In `language_model_gateway/gateway/routers/model_routing/usage_tracker.py`, modify `record_usage`'s signature and body:

```python
    async def record_usage(
        self,
        request_id: str,
        user_id: str | None,
        model: str,
        input_tokens: int,
        output_tokens: int,
        auth_provider: str | None = None,
        email: str | None = None,
        user_name: str | None = None,
        cache_creation_input_tokens: int | None = None,
        cache_read_input_tokens: int | None = None,
    ) -> None:
        """Record token usage to MongoDB."""
        if input_tokens == 0 and output_tokens == 0:
            return

        await self._ensure_connected()

        if self._collection is None:
            return

        usage_record: dict[str, Any] = {
            "request_id": request_id,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
        }

        if user_id:
            usage_record["user_id"] = user_id
        if auth_provider:
            usage_record["auth_provider"] = auth_provider
        if email:
            usage_record["email"] = email
        if user_name:
            usage_record["user_name"] = user_name
        if cache_creation_input_tokens is not None:
            usage_record["cache_creation_input_tokens"] = cache_creation_input_tokens
        if cache_read_input_tokens is not None:
            usage_record["cache_read_input_tokens"] = cache_read_input_tokens
```

(the rest of `record_usage`'s body — the try/except insert — is unchanged)

And modify `record_usage_from_anthropic_response`:

```python
    async def record_usage_from_anthropic_response(
        self,
        request_id: str,
        auth_info: dict[str, Any],
        model: str,
        response_body: dict[str, Any],
    ) -> None:
        """Extract usage from Anthropic response and record it."""
        usage = response_body.get("usage", {})
        input_tokens = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)

        # auth_info's identity fields are only populated when the caller's
        # Authorization header verified as a genuine OIDC token (see
        # CodingModelRouter._get_auth_info) — never re-derive identity from
        # raw, caller-controlled headers here.
        user_id = auth_info.get("user_id") if isinstance(auth_info, dict) else None
        email = auth_info.get("email") if isinstance(auth_info, dict) else None
        user_name = auth_info.get("user_name") if isinstance(auth_info, dict) else None
        auth_provider = (
            auth_info.get("auth_provider") if isinstance(auth_info, dict) else None
        )

        await self.record_usage(
            request_id=request_id,
            user_id=user_id,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            auth_provider=auth_provider,
            email=email,
            user_name=user_name,
            cache_creation_input_tokens=usage.get("cache_creation_input_tokens"),
            cache_read_input_tokens=usage.get("cache_read_input_tokens"),
        )
```

(`record_usage_from_openai_response` is unchanged — OpenAI's Chat Completions
`usage` block has no equivalent cache-token fields for this backend.)

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/gateway/routers/model_routing/test_usage_tracker.py -v`
Expected: all pass, including every pre-existing test in the file (no regressions)

- [ ] **Step 5: Commit**

```bash
git add language_model_gateway/gateway/routers/model_routing/usage_tracker.py tests/gateway/routers/model_routing/test_usage_tracker.py
git commit -m "<JIRA-KEY> Capture Anthropic cache token counts in usage tracking"
```

---

## Task 6: Documentation — env var + docker-compose

**Files:**
- Modify: `docs/coding_model_router.md`
- Modify: `docker-compose.yml`

**Interfaces:** none (docs-only task).

- [ ] **Step 1: Add the env var row**

In `docs/coding_model_router.md`, in the "## Environment variables" table (~line 63-75), add a new row directly after the `MODEL_ROUTING_ACCOUNT_DIRECTORY_COLLECTION_NAME` row:

```markdown
| `MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED` | `false` | Master switch for token-optimization behavior: Anthropic prompt caching (`cache_control` breakpoints on system/tools/message-history prefix) on `api_type: anthropic` routes, and lossless cross-turn tool-result deduplication on `api_type: openai` (Bedrock/Qwen) routes. Off by default; see `docs/superpowers/specs/2026-07-12-model-routing-token-optimization-design.md` for the design rationale. |
```

- [ ] **Step 2: Add the docker-compose entry**

In `docker-compose.yml`, near the existing `ENABLE_COST_SAVINGS_INFO: "false"` line (~line 55), add:

```yaml
      # Master switch for model-routing token optimization (prompt caching + dedup)
      MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED: "false"
```

- [ ] **Step 3: Commit**

```bash
git add docs/coding_model_router.md docker-compose.yml
git commit -m "<JIRA-KEY> Document MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED"
```

---

## Task 7: ADR + Phase 3 investigation finding

**Files:**
- Create: `adrs/0002-model-routing-token-optimization.md`

**Interfaces:** none (governance artifact, no code).

- [ ] **Step 1: Read the existing ADR for format**

Read `adrs/0001-structlog-for-json-log-rendering.md` to match its exact MADR section headers and tone.

- [ ] **Step 2: Investigate Phase 3 (Bedrock Mantle / Qwen caching)**

Check whether the Bedrock Mantle endpoint (`https://bedrock-mantle.us-east-1.api.aws/v1/chat/completions`) or its underlying serving stack documents any prompt-caching-equivalent field (e.g. an OpenAI-compatible `prompt_cache_key`, or documentation confirming the inference engine does automatic prefix-KV-caching that's reflected in the `price_per_mtok` billing for the haiku/sonnet routes). Record whichever of the two outcomes is true directly in the ADR's "Consequences" section:
- If something real exists: note it as a follow-up (do not implement it in this plan — it needs its own design pass).
- If nothing applies or billing doesn't reflect a discount: state that explicitly, so this doesn't get silently re-investigated without new information later.

- [ ] **Step 3: Write the ADR**

Create `adrs/0002-model-routing-token-optimization.md` with MADR sections: Context, Decision Drivers, Considered Options (native Anthropic caching + lossless dedup vs. third-party compression proxy vs. status quo), Decision Outcome (native caching + dedup, gated by feature flag), Pros/Cons of each option, and Consequences (including the Phase 3 finding from Step 2).

- [ ] **Step 4: Commit**

```bash
git add adrs/0002-model-routing-token-optimization.md
git commit -m "<JIRA-KEY> Add ADR for model routing token optimization"
```

---

## Task 8: Full regression pass

- [ ] **Step 1: Run the full model_routing test suite**

Run: `python -m pytest tests/gateway/routers/model_routing/ tests/gateway/routers/test_coding_model_router.py -v`
Expected: all pass, zero regressions.

- [ ] **Step 2: Run the full repo test suite**

Check the repo's canonical test command (e.g. `Makefile`, `pyproject.toml`/`Pipfile` scripts) rather than guessing, and run it in full to confirm nothing outside `model_routing` broke (e.g. an import cycle from the new `.constants` import in `cache_control.py`/`context_manager.py`).

- [ ] **Step 3: Confirm default-off behavior manually**

With `MODEL_ROUTING_TOKEN_OPTIMIZATION_ENABLED` unset, confirm via the Task 3/4 "disabled" tests (already covered) that request bodies are byte-identical to pre-change behavior — this is the rollback guarantee: unsetting the env var in production reverts to today's exact behavior with no code rollback needed.
