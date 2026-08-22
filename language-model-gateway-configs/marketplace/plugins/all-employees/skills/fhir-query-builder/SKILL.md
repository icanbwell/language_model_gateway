---
name: fhir-query-builder
description: Build FHIR server query URLs with proper parameters and environment endpoints. Use when users need to construct queries for the icanbwell FHIR server across different environments (dev, staging, client-sandbox, production).
allowed-tools:
  - google_search
  - url_to_markdown
---

# FHIR Query Builder

Build complete FHIR query URLs for the icanbwell FHIR server with proper parameters and environment-specific endpoints.

## Instructions

1. **Ask the user which environment** they want to query:
   - Development (dev)
   - Staging
   - Client Sandbox (client-sandbox)
   - Production (prod)

2. **Ask what FHIR resource type** they want to query (e.g., Patient, Practitioner, Observation, etc.)

3. **Ask what filters or parameters** they need:
   - Resource IDs
   - Search parameters (name, identifier, date ranges, etc.)
   - Sorting requirements
   - Pagination needs
   - Field selection (_elements)
   - Count limits (_count)
   - Security tags (_security)
   - Other filters

4. **Build the complete URL** using:
   - The appropriate environment base URL
   - The resource type
   - The FHIR version path (4_0_0)
   - All query parameters properly formatted

5. **Return the complete URL** and explain what it does

6. **Optionally provide**:
   - Related environment links (UI, logs, stats)
   - Alternative endpoints for the same environment
   - Tips for optimization or best practices

## Environment Endpoints

### Development
- **Service link**: `https://fhir.dev.bwell.zone/`
- Main UI: https://fhir-ui.dev.icanbwell.com
- Stats: https://fhir-internal.dev.bwell.zone/stats

### Staging
- **Service link**: `https://fhir.staging.bwell.zone/`
- External testing: https://fhir.staging.icanbwell.com/
- Main UI: https://fhir-ui.staging.icanbwell.com
- Stats: https://fhir-bulk.staging.bwell.zone/stats
- Logs: https://grafana.services.bwell.zone/explore?orgId=1&left={"datasource":"Loki","queries":[{"refId":"A","expr":"{namespace%3D\"fhir-staging\"} |%3D ``","queryType":"range","editorMode":"builder"}],"range":{"from":"now-1h","to":"now"}}

### Client Sandbox
- **Service link**: `https://fhir.client-sandbox.icanbwell.com/`
- Main UI: https://fhir-ui.client-sandbox.icanbwell.com
- Stats: https://fhir-internal.client-sandbox.bwell.zone/stats
- Cognito: https://us-east-1.console.aws.amazon.com/cognito/v2/idp/user-pools/us-east-1_yiNhNGXZ7/users?region=us-east-1
- Logs: https://grafana.services.bwell.zone/explore?orgId=1&left={"datasource":"Loki","queries":[{"refId":"A","editorMode":"builder","expr":"{cluster%3D\"client-sandbox-ue1\", app%3D\"fhir-server\"} |%3D ``","queryType":"range"}],"range":{"from":"now-1h","to":"now"}}

### Production
- **Service link**: `https://fhir.icanbwell.com`
- Bulk endpoint (recommended): https://fhir-bulk.prod.icanbwell.com
- Pipeline operations: https://fhir-pipeline.prod.icanbwell.com
- Health Programs (CQL): https://fhir-hp.prod.icanbwell.com
- Next version testing: https://fhir-next.prod.icanbwell.com
- Main UI: https://fhir-ui.prod.icanbwell.com
- Stats: https://fhir-internal.prod.bwell.zone/stats

## Common Query Parameters

### Basic Parameters
- `_count={number}` - Limit results (default: 100, use 0 for no limit)
- `_elements={field1,field2}` - Select specific fields only
- `_sort={field}` - Sort ascending, use `-{field}` for descending
- `_total=accurate` - Include total count (expensive operation)
- `_getpagesoffset={number}` - Offset-based pagination

### Search Filters
- `id={id}` or `id={id1,id2}` - Filter by resource ID(s)
- `identifier={system}|{value}` - Filter by identifier
- `_security={system}|{value}` - Filter by security tag
- `_lastUpdated=gt{date}` - Updated after date
- `_lastUpdated=lt{date}` - Updated before date
- `source={url}` - Filter by source system
- `{field}={value}` - Filter by any field value

### Resource-Specific Filters
- **Patient/Practitioner**: `name={name}`, `family={family}`
- **Observation**: `code={system}|{value}`, `date=gt{date}`
- **Appointment**: `date=lt{date}`, `date=gt{date}`
- **ValueSet**: `url={url}`

### Search Modifiers
- `:missing=true` - Element is missing or has no value
- `:not` - Negate a filter (e.g., `_security:not={system}|{value}`)
- `:exact` - Exact string match
- `:contains` - Case-insensitive substring match
- `:text` - Search in text associated with codes
- `:of-type` - For identifiers: `identifier:of-type={system}|{code}|{value}`
- `:above` - Resources after specified ID (pagination)
- `:below` - Resources before specified ID (pagination)

### Search Prefixes (for numbers, dates, quantities)
- `ne` - Not equal
- `gt` - Greater than
- `ge` - Greater than or equal
- `lt` - Less than
- `le` - Less than or equal

## Examples

### Example 1: Basic Patient Search

**User Request**: "I need to get patients from dev environment, limit to 10 results"

**Response**:
```
https://fhir.dev.bwell.zone/4_0_0/Patient?_count=10
```

This query:
- Targets the Development environment
- Fetches Patient resources
- Limits results to 10 records

You can also view this in the UI: https://fhir-ui.dev.icanbwell.com

### Example 2: Filtered Practitioner Search

**User Request**: "Get practitioners in staging with NPI identifier 1487831681, show only id and name fields"

**Response**:
```
https://fhir.staging.bwell.zone/4_0_0/Practitioner?identifier=http://hl7.org/fhir/sid/us-npi|1487831681&_elements=id,name
```

This query:
- Targets the Staging environment
- Searches Practitioner resources
- Filters by NPI identifier system and value
- Returns only id and name fields

### Example 3: Date Range Query with Sorting

**User Request**: "Find observations in production updated between Jan 1-15, 2024, sorted by last updated descending, 50 per page"

**Response**:
```
https://fhir.icanbwell.com/4_0_0/Observation?_lastUpdated=gt2024-01-01&_lastUpdated=lt2024-01-15&_sort=-meta.lastUpdated&_count=50
```

This query:
- Targets Production environment
- Searches Observation resources
- Filters by date range (after Jan 1 AND before Jan 15, 2024)
- Sorts by meta.lastUpdated descending
- Returns 50 results per page
- Use the `next` URL in the response bundle for pagination

### Example 4: Security Tag Filter

**User Request**: "Get all Organizations in client-sandbox with access tag 'bwell', include total count"

**Response**:
```
https://fhir.client-sandbox.icanbwell.com/4_0_0/Organization?_security=https://www.icanbwell.com/access|bwell&_total=accurate
```

This query:
- Targets Client Sandbox environment
- Searches Organization resources
- Filters by security access tag
- Includes total count in response (note: expensive operation)

Main UI: https://fhir-ui.client-sandbox.icanbwell.com

### Example 5: Complex Multi-Filter Query

**User Request**: "In staging, get ExplanationOfBenefit resources for patient 12345, updated after March 1, 2024, with source from 'acme-health', sorted by date, 25 results"

**Response**:
```
https://fhir.staging.bwell.zone/4_0_0/ExplanationOfBenefit?patient=12345&_lastUpdated=gt2024-03-01&source=http://acme-health.org&_sort=-meta.lastUpdated&_count=25
```

This query:
- Targets Staging environment
- Searches ExplanationOfBenefit resources
- Filters by patient reference
- Filters by update date (after March 1, 2024)
- Filters by source system
- Sorts by last updated descending
- Returns 25 results per page

## Edge Cases and Best Practices

### When You Don't Know
- If unsure about FHIR resource types or standard parameters, use `google_search` to find FHIR R4B specification links
- Reference: https://hl7.org/fhir/R4B/resourcelist.html
- Search parameter registry: https://www.hl7.org/fhir/R4B/searchparameter-registry.html

### Performance Considerations
- Avoid `_total=accurate` unless absolutely needed (expensive for large datasets)
- Use `_elements` to request only needed fields
- For large datasets, use cursor-based pagination (next URL) instead of `_getpagesoffset`
- Consider using bulk endpoint in production for large data exports
- Don't use `_count=0` (no limit) unless you understand the data volume

### Headers Required
- Always remind users to set: `Content-Type: application/fhir+json`
- For strict validation: `handling=strict`
- Authentication: `Authorization: Bearer {token}`

### Special Operations
- For graphs of related resources: Use `/$graph` endpoint
- For create/update: Use `/$merge` endpoint (recommended)
- For history: Append `/_history` to resource URL

### Date Format
- Use ISO 8601 format: `YYYY-MM-DD` or `YYYY-MM-DDTHH:mm:ss`
- Examples: `2024-01-15`, `2024-01-15T10:30:00`

### Multiple Values
- Comma-separated for OR logic: `id=123,456,789`
- Multiple parameters for AND logic: `_lastUpdated=gt2024-01-01&_lastUpdated=lt2024-01-31`

### URL Encoding
- Pipe character `|` in identifiers may need encoding as `%7C`
- Spaces should be encoded as `%20` or `+`
- Most tools handle this automatically

## Failure Handling

- If the environment is unclear, ask the user to specify
- If the resource type is invalid, suggest checking FHIR R4B resource list
- If parameters seem incorrect, explain the correct format with examples
- If the query might be too expensive (no limits, total count on large dataset), warn the user
- If authentication is mentioned, remind about OAuth requirements and point to security documentation
- 
## Advanced Query Patterns

### Chaining and Reverse Chaining
- **Forward chain**: `Observation?subject:Patient.name=Smith` - Find observations for patients named Smith
- **Reverse chain**: `Patient?_has:Observation:patient:code=http://loinc.org|8867-4` - Find patients who have specific observations

### Include and RevInclude
- `_include=Patient:organization` - Include referenced organizations
- `_revinclude=Observation:patient` - Include observations that reference this patient
- `_include:iterate` - Follow references recursively

### Composite Search Parameters
- Some resources support composite searches combining multiple parameters
- Example: `Observation?code-value-quantity=http://loinc.org|8867-4$gt100`

### Graph Queries
For complex resource graphs, use the `$graph` operation:
```
https://fhir.dev.bwell.zone/4_0_0/Patient/12345/$graph?id=Patient/12345
```

### Everything Operation
Get a patient and all related resources:
```
https://fhir.dev.bwell.zone/4_0_0/Patient/12345/$everything
```

## Response Format

All queries return a FHIR Bundle with:
- `resourceType: "Bundle"`
- `type: "searchset"`
- `entry[]` - Array of matching resources
- `link[]` - Pagination links (self, next, previous)
- `total` - Total count (if `_total=accurate` was used)

## Workflow

1. **Greet and ask for environment**
   - "Which environment do you want to query? (dev, staging, client-sandbox, or production)"

2. **Ask for resource type**
   - "What FHIR resource type do you need? (e.g., Patient, Practitioner, Observation, Organization, etc.)"
   - If unsure, offer to search for valid FHIR R4B resources

3. **Gather query requirements**
   - "What filters or search criteria do you need?"
   - "Do you need specific fields only? (_elements)"
   - "How many results? (_count)"
   - "Any sorting requirements? (_sort)"
   - "Do you need pagination?"
   - "Any security tags to filter by?"
   - "Any date ranges?"

4. **Build and present the URL**
   - Show the complete, ready-to-use URL
   - Explain each parameter
   - Provide the UI link for visual exploration
   - Mention relevant endpoints (stats, logs) if helpful

5. **Offer additional help**
   - "Would you like to add more filters?"
   - "Need help with pagination?"
   - "Want to see this in a different environment?"
   - "Need the curl command or other format?"

## Additional Output Formats

### cURL Command
When requested, provide a ready-to-use cURL command:
```bash
curl -X GET \
  'https://fhir.dev.bwell.zone/4_0_0/Patient?_count=10' \
  -H 'Content-Type: application/fhir+json' \
  -H 'Authorization: Bearer <YOUR_API_TOKEN>'
```

### Postman/REST Client Format
Provide structured format:
- **Method**: GET
- **URL**: [full URL]
- **Headers**:
  - Content-Type: application/fhir+json
  - Authorization: Bearer {token}

### Python Requests Example
```python
import requests

url = "https://fhir.dev.bwell.zone/4_0_0/Patient"
params = {
    "_count": 10,
    "_elements": "id,name"
}
headers = {
    "Content-Type": "application/fhir+json",
    "Authorization": "Bearer <YOUR_API_TOKEN>"
}

response = requests.get(url, params=params, headers=headers)
data = response.json()
```

## Common Use Cases

### Use Case 1: Data Validation
"I need to check if a specific patient exists in staging"
- Build query with specific patient ID
- Use `_elements=id` for minimal response
- Provide UI link for visual verification

### Use Case 2: Data Export
"I need to export all practitioners updated in the last week from production"
- Use date range with `_lastUpdated`
- Recommend bulk endpoint for large exports
- Suggest appropriate `_count` for pagination
- Warn about performance considerations

### Use Case 3: Testing New Data
"I just loaded data to dev, want to verify it's there"
- Build query with source or identifier filter
- Provide UI link for easy browsing
- Suggest using `_lastUpdated` to see recent data

### Use Case 4: Debugging Issues
"I need to find why a resource isn't showing up"
- Ask about expected filters
- Build query step by step
- Suggest checking security tags
- Provide logs link for the environment

### Use Case 5: Performance Testing
"I need to test query performance on large datasets"
- Recommend using stats endpoint
- Suggest appropriate indexes
- Provide query optimization tips
- Warn about expensive operations

## Troubleshooting Guide

### No Results Returned
- Check security tags - resource might be filtered by access
- Verify identifier system and value format
- Check date formats (ISO 8601)
- Try removing filters one by one to isolate issue
- Use UI to browse and verify data exists

### Slow Queries
- Add `_count` limit if missing
- Remove `_total=accurate` if not needed
- Use `_elements` to request fewer fields
- Check if indexes exist for search parameters
- Consider using bulk endpoint for large exports

### Authentication Errors
- Verify token is valid and not expired
- Check token has appropriate scopes
- Ensure Authorization header format: `Bearer {token}`
- For client-sandbox, check Cognito user pool

### Invalid Parameter Errors
- Check parameter spelling and format
- Verify parameter is supported for that resource type
- Check modifier syntax (`:missing`, `:not`, etc.)
- Verify date/number prefix syntax

## Quick Reference Card

**Basic Structure**: `{base_url}/4_0_0/{ResourceType}?{parameters}`

**Most Common Parameters**:
- `?id=123` - Get by ID
- `?_count=50` - Limit results
- `?_elements=id,name` - Select fields
- `?_sort=-meta.lastUpdated` - Sort descending
- `?_lastUpdated=gt2024-01-01` - Updated after date
- `?_security=system|value` - Filter by access tag
- `?identifier=system|value` - Find by identifier

**Pagination**:
- Use `next` link from response bundle (recommended)
- Or use `?_getpagesoffset=100` for offset-based
- Or use `?id:above=lastId` for cursor-based

**Environment Quick Pick**:
- Dev: `fhir.dev.bwell.zone`
- Staging: `fhir.staging.bwell.zone`
- Sandbox: `fhir.client-sandbox.icanbwell.com`
- Prod: `fhir.icanbwell.com`

## Resources and Documentation

- **FHIR R4B Specification**: https://hl7.org/fhir/R4B/
- **Resource List**: https://hl7.org/fhir/R4B/resourcelist.html
- **Search Parameters**: https://www.hl7.org/fhir/R4B/searchparameter-registry.html
- **Cheatsheet**: https://raw.githubusercontent.com/icanbwell/fhir-server/refs/heads/main/readme/cheatsheet.md

When in doubt about FHIR specifications, use `google_search` to find authoritative HL7 FHIR documentation.

## Policy

- Always ask for environment first before building URLs
- Provide complete, working URLs that can be copy-pasted
- Explain what each parameter does
- Warn about expensive operations (_total, _count=0, etc.)
- Offer UI links for visual exploration
- Be helpful with troubleshooting and optimization
- If unsure about FHIR specs, search for official documentation
- Provide alternative formats (cURL, Python, etc.) when requested