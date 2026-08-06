# b.well App Login → mcp-fhir-agent (dev) — Call Sequence

Repos involved: `language-model-gateway`, `language-model-common`, `oidc-auth-lib`, `mcp-fhir-agent`.

## 1. Chat request with no cached FHIR token yet → gateway returns login links

```bash
curl -X POST http://localhost:5050/api/v1/chat/completions \
  -H "Authorization: Bearer <your gateway SSO JWT>" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "ai_sdk_local_dev",
        "messages": [{"role": "user", "content": "what are my vitals?"}]
      }'
```
Gateway verifies the bearer JWT, looks up a cached FHIR token keyed by `(sub, "oktafhirdev")`, finds none, and instead of calling the tool returns a message containing a `Login to b.well App` link to `/app/login?state=<signed>`.
*(`pass_through_token_manager.py:264-444`, `chat_completion_router.py:352-414`)*

## 2. You open the login form

```bash
curl "http://localhost:5050/app/login?state=<signed_state_from_step_1>"
```
Renders a username/password form; `state` decodes to `auth_provider=oktafhirdev`, `referring_subject=<your sub>`.
*(`app_login_router.py:69-112`)*

## 3. You submit b.well credentials to the gateway

```bash
curl -X POST "http://localhost:5050/app/login?state=<same_state>" \
  -d "username=<b.well_username>" \
  -d "password=<b.well_password>" \
  -d "client_key=Dev"
```
*(`app_login_router.py:115-185`)*

## 4. Gateway → b.well identity service (server-to-server, triggered by step 3)

Dev client key (from `language-model-gateway-configs/marketplace/plugins/all-employees/.mcp.json:58`, `fhir-server-dev.oauth.appLogin.clientKeys.Dev`):
```
eyJyIjoiY2Zoa2h3ODZvNHdoNWFiOW9kaHgiLCJlbnYiOiJkZXYiLCJraWQiOiJid2VsbF9kZW1vLWRldiJ9
```

```bash
curl -X POST https://api.dev.icanbwell.com/identity/account/login \
  -H "clientkey: eyJyIjoiY2Zoa2h3ODZvNHdoNWFiOW9kaHgiLCJlbnYiOiJkZXYiLCJraWQiOiJid2VsbF9kZW1vLWRldiJ9" \
  -H "Content-Type: application/json" \
  -d '{"username": "<b.well_username>", "password": "<b.well_password>"}'
```
Response:
```json
{
  "accessToken":  {"jwtToken": "<FHIR-scoped JWT — carries clientFhirPersonId, scope>"},
  "idToken":      {"jwtToken": "..."},
  "refreshToken": {"token": "..."}
}
```
Gateway caches `accessToken.jwtToken` in Mongo keyed by `(referring_subject, "oktafhirdev")`.
*(`app_login_manager.py:73-191`)*

## 5. You retry the same chat request

```bash
curl -X POST http://localhost:5050/api/v1/chat/completions \
  -H "Authorization: Bearer <your gateway SSO JWT>" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "ai_sdk_local_dev",
        "messages": [{"role": "user", "content": "what are my vitals?"}]
      }'
```
This time the cache lookup for `(sub, "oktafhirdev")` hits. The interceptor overwrites the outbound `Authorization` header with the cached token before calling the tool.
*(`auth.py:129-183, 248-282`)*

## 6. Gateway → mcp-fhir-agent (server-to-server, triggered by step 5)

```bash
curl -X POST http://mcp-fhir-agent-dev:5000/ \
  -H "Authorization: Bearer <accessToken.jwtToken from step 4>" \
  -H "X-Client-Id: Aiden" \
  -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": "get_vitals", "arguments": {}}
      }'
```
*(`mcp_tool_provider.py:233-259` builds this call; tool name/args from `fhir_observations/register.py:58-174`)*

mcp-fhir-agent validates the JWT (`TokenReaderVerifier`, decode + verify against its own `AUTH_PROVIDERS` list), pulls `clientFhirPersonId` off the claims, resolves the `get_vitals` tool.
*(`token_reader_verifier.py:27-143`, `person_id_extractor.py:60`)*

## 7. mcp-fhir-agent → FHIR server (server-to-server, triggered by step 6)

```bash
curl -X GET "http://fhir-server-internal.fhir-server-internal-dev.svc.cluster.local:3000/4_0_0/Observation?patient=person.<clientFhirPersonId>&category=vital-signs&_sort=-date" \
  -H "Authorization: Bearer <same JWT forwarded unchanged>" \
  -H "Prefer: global_id=true"
```
*(`fhir_data_loader.py:266-371`, `fhir_vitals_retriever.py:135-155`)*

The same JWT that mcp-fhir-agent validated in step 6 is forwarded as-is to the FHIR server — mcp-fhir-agent does not mint a separate FHIR credential for this path. The `patient=person.<id>` param is what actually scopes the query to that one user; person-level scoping and a token-scope check (`FhirScopesManager.is_user_allowed_to_access_fhir_cache_async`, `fhir_scopes_manager.py:43-114`) happen before the request is even sent.

---

## Optional/conditional branch not in the path above

mcp-fhir-agent also supports a **`ClientKey`-header token exchange**, independent of the gateway's own AppLoginManager exchange in step 4:

```bash
curl -X POST http://mcp-fhir-agent-dev:5000/ \
  -H "Authorization: Bearer <raw b.well session token>" \
  -H "ClientKey: <client key>" \
  -H "Content-Type: application/json" \
  -d '{ "jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {} }'
```
If a `ClientKey` header is present, `ClientKeyAuthorizationMiddleware` (`client_key_authorization_middleware.py:17-53`) intercepts *before* MCP auth and does its own exchange:
```bash
curl -X POST https://api.dev.icanbwell.com/v1/graphql \
  -H "authorization: <raw jwt, no 'Bearer ' prefix>" \
  -H "clientkey: <client key>" \
  -H "content-type: application/json" \
  -d '{"query": "query authenticate { getToken { accessToken { jwtToken } idToken { jwtToken } refreshToken { token } } } "}'
```
and swaps the resulting `accessToken.jwtToken` in as the request's `Authorization` header before it reaches step 6/7's logic.

**Flag for porting to another project:** the `ai-sdk-local-dev.json` config sends `X-Client-Id: Aiden`, not `ClientKey` — that middleware doesn't fire on this path. It exists for a different caller pattern (something posting a raw session token straight to mcp-fhir-agent instead of going through the gateway's own AppLoginManager exchange). Don't assume the two exchange steps compose in series unless you confirm which header your other project's client actually sends.
