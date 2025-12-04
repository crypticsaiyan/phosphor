# IRC Visibility Protocol - Public vs Private Responses

## Overview

The DevOps Channel Assistant supports two visibility modes for responses:
- **PUBLIC** - Response goes to the entire IRC channel
- **PRIVATE** - Response goes only to the requesting user

This allows sensitive information, detailed explanations, or verbose output to be kept private while keeping team-wide updates public.

## User Commands

### Public Mode (Default)

```
/ai <message>
```

**Examples:**
```
/ai check docker health
/ai what's the status of prod-web?
/ai why is the API slow?
```

**Behavior:**
- Response is sent to the channel (e.g., #ops)
- Everyone in the channel sees the response
- Best for: incident updates, health checks, team-wide info

### Private Mode

```
/ai private <message>
```

**Examples:**
```
/ai private explain what a slow query is
/ai private show me detailed logs for prod-db
/ai private draft a message for the CTO about downtime
```

**Behavior:**
- Response is sent only to the requesting user (DM)
- Other channel members don't see the response
- Best for: learning, sensitive data, verbose output

## Protocol Specification

### For AI Responses

Every AI response MUST start with a visibility directive:

```
VISIBILITY: public

<response content here>
```

or

```
VISIBILITY: private

<response content here>
```

### Rules

1. **First Line**: Must be exactly `VISIBILITY: public` or `VISIBILITY: private`
2. **Blank Line**: Add a blank line after the visibility directive
3. **Content**: Then provide the actual response

### Example Responses

**Public Response:**
```
VISIBILITY: public

🏥 Docker Health Check
========================================
🟢 Summary: 3 healthy, 0 warning, 0 critical

Details:
✅ prod-web-1: RUNNING, healthy, up 2h
✅ prod-api-1: RUNNING, healthy, up 2h
✅ prod-db-1: RUNNING, healthy, up 5d
```

**Private Response:**
```
VISIBILITY: private

Here's a detailed explanation of Docker health checks:

1. Health Check Basics
   - Docker can run periodic health checks on containers
   - Defined in Dockerfile with HEALTHCHECK instruction
   - Returns: healthy, unhealthy, or starting

2. How It Works
   - Docker runs a command inside the container
   - If exit code is 0: healthy
   - If exit code is 1: unhealthy
   - If still checking: starting

3. Example Configuration
   ```dockerfile
   HEALTHCHECK --interval=30s --timeout=3s \
     CMD curl -f http://localhost/ || exit 1
   ```

Would you like me to explain any specific aspect in more detail?
```

## Bridge Implementation

### Parsing Commands

The IRC bridge parses incoming commands:

```python
# Public command
"/ai check docker health"
→ is_private = False

# Private command
"/ai private explain health checks"
→ is_private = True
→ prompt = "explain health checks"
```

### Parsing Responses

The bridge parses AI responses:

```python
response = """VISIBILITY: public

Summary: All systems healthy"""

visibility, content = parse_visibility(response)
# visibility = "public"
# content = "Summary: All systems healthy"
```

### Routing Responses

Based on visibility:

```python
if visibility == "private":
    send_to_user(nick, content)
else:
    send_to_channel(channel, content)
```

## Use Cases

### Public Mode Use Cases

1. **Health Checks**
   ```
   /ai check docker health
   ```
   → Everyone sees container status

2. **Incident Updates**
   ```
   /ai what's wrong with prod-api?
   ```
   → Team sees the diagnosis

3. **Quick Status**
   ```
   /ai is the database up?
   ```
   → Quick yes/no for the team

4. **Action Items**
   ```
   /ai what should we do about high CPU?
   ```
   → Team sees recommendations

### Private Mode Use Cases

1. **Learning/Explanations**
   ```
   /ai private explain what a circuit breaker is
   ```
   → Detailed explanation just for you

2. **Sensitive Information**
   ```
   /ai private show me the error logs with stack traces
   ```
   → Logs might contain sensitive data

3. **Drafting Messages**
   ```
   /ai private draft an incident report for the outage
   ```
   → Work on the draft privately first

4. **Verbose Output**
   ```
   /ai private explain all docker health check options
   ```
   → Long explanation doesn't spam the channel

5. **Personal Queries**
   ```
   /ai private how do I configure my local docker?
   ```
   → Personal help without bothering the team

## Security Considerations

### Public Mode

**DO:**
- ✅ Share health summaries
- ✅ Share high-level status
- ✅ Share action items
- ✅ Share incident summaries

**DON'T:**
- ❌ Share secrets, tokens, passwords
- ❌ Share full environment variables
- ❌ Share personal data
- ❌ Share sensitive stack traces

### Private Mode

**DO:**
- ✅ Provide detailed explanations
- ✅ Show more verbose output
- ✅ Include teaching/mentoring content
- ✅ Draft messages or reports

**DON'T:**
- ❌ Share real secrets/credentials (even in private)
- ❌ Assume private = completely secure

### AI Behavior

The AI should:
1. Detect sensitive information in responses
2. Suggest using private mode if needed:
   ```
   VISIBILITY: public
   
   This looks sensitive. Use `/ai private <query>` for details.
   ```

## Examples

### Example 1: Public Health Check

**User in #ops:**
```
alice: /ai check prod
```

**AI Response:**
```
VISIBILITY: public

🏥 Docker Health Check - Production
========================================
🟢 Summary: 5 healthy, 0 warning, 0 critical

Details:
✅ prod-web-1: RUNNING, healthy, up 2d
✅ prod-web-2: RUNNING, healthy, up 2d
✅ prod-api-1: RUNNING, healthy, up 2d
✅ prod-db-1: RUNNING, healthy, up 10d
✅ prod-redis-1: RUNNING, healthy, up 10d
```

**Result:** Everyone in #ops sees the health status

### Example 2: Private Explanation

**User in #ops:**
```
bob: /ai private explain what "healthy" means
```

**AI Response:**
```
VISIBILITY: private

Docker Health Status Explained:

**Healthy** means:
1. The container is running
2. The health check command succeeds (exit code 0)
3. The health check has passed consistently

For example, if your health check is:
```
HEALTHCHECK CMD curl -f http://localhost/ || exit 1
```

Then "healthy" means:
- The curl command succeeds
- The HTTP endpoint responds
- This has been true for multiple checks

Other statuses:
- **Starting**: Health check hasn't completed yet
- **Unhealthy**: Health check is failing
- **No health check**: Container has no HEALTHCHECK defined

Does this help clarify?
```

**Result:** Only bob sees this detailed explanation (DM)

### Example 3: Sensitive Data Detection

**User in #ops:**
```
charlie: /ai show me the environment variables for prod-api
```

**AI Response:**
```
VISIBILITY: public

⚠️  Environment variables may contain sensitive information.

Use `/ai private show me the environment variables for prod-api` for details.

Or run manually:
```
docker inspect prod-api-1 | grep -A 20 Env
```
```

**Result:** Everyone sees the warning, not the actual env vars

### Example 4: Private Detailed Query

**User in #ops:**
```
charlie: /ai private show me the environment variables for prod-api
```

**AI Response:**
```
VISIBILITY: private

Environment Variables for prod-api-1:

Note: Some values redacted for security

- NODE_ENV=production
- PORT=3000
- DATABASE_URL=postgres://[REDACTED]
- REDIS_URL=redis://[REDACTED]
- API_KEY=[REDACTED]
- LOG_LEVEL=info
- MAX_CONNECTIONS=100

⚠️  Keep these values secure. Don't share in public channels.
```

**Result:** Only charlie sees this (DM)

## Testing

### Test Public Mode

```bash
# In IRC:
/ai check docker health

# Expected:
# - Response appears in channel
# - Starts with "VISIBILITY: public" (hidden by bridge)
# - Everyone sees the health summary
```

### Test Private Mode

```bash
# In IRC:
/ai private explain docker health checks

# Expected:
# - Response appears as DM to you
# - Starts with "VISIBILITY: private" (hidden by bridge)
# - Only you see the detailed explanation
```

### Test Programmatically

```python
from kiro_irc_bridge import KiroIRCBridge

bridge = KiroIRCBridge(config)

# Test visibility parsing
response = """VISIBILITY: public

Test message"""

visibility, content = bridge._parse_visibility(response)
assert visibility == "public"
assert content == "Test message"
```

## Configuration

No special configuration needed. The visibility protocol is built into the bridge.

### Config File (kiro_bridge_config.json)

```json
{
  "irc": {
    "host": "irc.libera.chat",
    "port": 6697,
    "ssl": true,
    "nick": "devops-ai",
    "channels": ["#ops"],
    "debug": false
  },
  "command_prefix": "/ai ",
  "kiro": {
    "agent": "ops-ai"
  }
}
```

## Troubleshooting

### Response Goes to Wrong Place

**Problem:** Private response appears in channel

**Solution:** Check that the AI response starts with `VISIBILITY: private`

### No Visibility Directive

**Problem:** AI response doesn't include visibility directive

**Solution:** The bridge defaults to public. Update AI prompt to include protocol instructions.

### Visibility Line Visible in IRC

**Problem:** Users see "VISIBILITY: public" in messages

**Solution:** Bridge should strip this line. Check `_parse_visibility()` method.

## Best Practices

### For Users

1. **Default to public** for team-relevant information
2. **Use private** for:
   - Learning/explanations
   - Sensitive data
   - Verbose output
   - Personal queries
3. **Don't abuse private mode** - share knowledge with the team when appropriate

### For AI Responses

1. **Always include visibility directive** as first line
2. **Be concise in public mode** - IRC has line limits
3. **Detect sensitive data** and suggest private mode
4. **Provide value in both modes**:
   - Public: actionable summaries
   - Private: detailed explanations

### For Bridge Operators

1. **Log visibility decisions** for debugging
2. **Monitor for abuse** of private mode
3. **Test both modes** regularly
4. **Document the protocol** for your team

## Summary

The visibility protocol enables:
- ✅ Team-wide incident response (public)
- ✅ Private learning and exploration (private)
- ✅ Sensitive data protection (private)
- ✅ Concise channel updates (public)
- ✅ Detailed explanations when needed (private)

Use `/ai` for public, `/ai private` for private. Simple!
