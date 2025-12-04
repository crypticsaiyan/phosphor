# `/ai` Command Guide - Updated Implementation

## What Changed

The `/ai` command in the TUI now has two modes:

### 1. Public Mode (Sends to IRC Channel)

```
/ai <query>
```

**Behavior:**
- Executes the AI command
- Sends the result to the IRC channel (if connected)
- Everyone in the channel sees the response
- Also shows in your local chat pane

**Example:**
```
You: /ai check docker health

[Sends to IRC channel #ops]
You (AI): 🏥 Docker Health Check
You (AI): ========================================
You (AI): 🟢 Summary: 1 healthy, 0 warning, 0 critical
You (AI): 
You (AI): Details:
You (AI): ✅ prod-web-test: RUNNING, up 48m
```

### 2. Private Mode (Local Only)

```
/ai private <query>
```

**Behavior:**
- Executes the AI command
- Shows result only to you (in chat pane)
- Does NOT send to IRC channel
- Private to your session

**Example:**
```
You: /ai private explain health checks

[Shows only in your chat pane]
AI Assistant (Private):
Docker health checks are periodic tests...
```

## Usage Examples

### Public Commands (Sent to IRC)

```
/ai                          # Check all containers → IRC
/ai check docker health      # Health check → IRC
/ai prod                     # Production containers → IRC
/ai staging web              # Staging web services → IRC
/ai help                     # Show help → IRC
```

### Private Commands (Local Only)

```
/ai private explain health checks        # Learn → Local only
/ai private show me detailed logs        # Verbose → Local only
/ai private what does "healthy" mean?    # Question → Local only
```

## How It Works

### When Connected to IRC

**Public command:**
```
You type: /ai check docker

1. MCP client executes command
2. Gets health check result
3. Splits result into lines
4. Sends each line to IRC channel
5. Shows in your chat pane too
```

**Result in IRC:**
```
<your-nick> 🏥 Docker Health Check
<your-nick> ========================================
<your-nick> 🟢 Summary: 1 healthy, 0 warning, 0 critical
<your-nick> 
<your-nick> Details:
<your-nick> ✅ prod-web-test: RUNNING, up 48m
```

**Private command:**
```
You type: /ai private explain this

1. MCP client executes command
2. Gets result
3. Shows ONLY in your chat pane
4. Does NOT send to IRC
```

### When NOT Connected to IRC

**Any command:**
```
You type: /ai check docker

1. MCP client executes command
2. Gets result
3. Shows in your chat pane
4. Displays message: "Not connected to IRC. Result shown locally only."
```

## Testing

### Test in TUI

```bash
# Start the TUI
python demo.py

# Wait for IRC connection (watch for "Connected to IRC!" message)

# Test public command
/ai check docker health

# Check IRC channel - you should see the response!

# Test private command
/ai private explain health checks

# This should only show in your chat pane, not IRC
```

### Test Programmatically

```bash
# Test the MCP client directly
python3 test_ai_command.py
```

## Behavior Matrix

| Command | IRC Connected | Result |
|---------|---------------|--------|
| `/ai <query>` | ✅ Yes | Sent to IRC channel + shown locally |
| `/ai <query>` | ❌ No | Shown locally only + warning message |
| `/ai private <query>` | ✅ Yes | Shown locally only (not sent to IRC) |
| `/ai private <query>` | ❌ No | Shown locally only |

## Use Cases

### Use Case 1: Team Health Check

```
# In TUI, connected to IRC #ops
/ai check docker health

# Result:
# - Sent to #ops channel
# - Everyone sees container status
# - Team is informed
```

### Use Case 2: Personal Learning

```
# In TUI
/ai private explain what "restart count" means

# Result:
# - Shown only to you
# - Detailed explanation
# - Doesn't spam the channel
```

### Use Case 3: Incident Response

```
# In TUI, connected to IRC #ops
/ai prod api

# Result:
# - Sent to #ops channel
# - Team sees API status
# - Everyone aware of issues
```

### Use Case 4: Debugging Locally

```
# In TUI, not connected to IRC
/ai check docker

# Result:
# - Shown locally
# - Message: "Not connected to IRC"
# - Still useful for local debugging
```

## Troubleshooting

### "Nothing happens when I type /ai"

**Possible causes:**

1. **Command not recognized**
   - Check you typed `/ai` (with slash)
   - Check there's a space after `/ai`
   - Example: `/ai check docker` ✅ not `/aicheck docker` ❌

2. **MCP client error**
   - Check Docker is running: `docker ps`
   - Check permissions: See FIX_DOCKER_PERMISSIONS.md
   - Look for error messages in chat pane

3. **IRC not connected**
   - Wait for "Connected to IRC!" message
   - Check IRC server is reachable
   - Look for connection errors

### "Response not appearing in IRC channel"

**Possible causes:**

1. **Not connected to IRC**
   - Check for "Connected to IRC!" message
   - Look for "Not connected to IRC" warning

2. **Not joined to channel**
   - Check you're in a channel (e.g., #general)
   - Look for "Joined #channel" message

3. **Used private mode**
   - `/ai private` doesn't send to IRC (by design)
   - Remove "private" to send to channel

4. **IRC send failed**
   - Check for error messages
   - Check IRC connection is stable

### "Response shows locally but not in IRC"

**Check:**
- Are you connected to IRC? (Look for connection message)
- Are you in a channel? (Check current_channel)
- Did you use `/ai private`? (This is local only)

### "Response appears twice"

**This is normal!**
- Once in IRC channel (from IRC server)
- Once in your chat pane (local echo)

## Advanced Usage

### Filtering

```
/ai prod              # Production containers → IRC
/ai staging web       # Staging web services → IRC
/ai db                # Database containers → IRC
```

### Help

```
/ai help              # Show all commands → IRC
/ai private help      # Show help locally only
```

### Custom Queries

```
/ai check prod-web-1           # Specific container → IRC
/ai private explain restarts   # Learn about restarts → Local
```

## Configuration

No configuration needed! The behavior is automatic:

- **IRC connected + public command** → Sends to IRC
- **IRC connected + private command** → Local only
- **IRC not connected** → Local only (with warning)

## Summary

### Public Mode (`/ai <query>`)
- ✅ Sends to IRC channel (if connected)
- ✅ Everyone sees the response
- ✅ Good for team updates
- ✅ Shows in your chat pane too

### Private Mode (`/ai private <query>`)
- ✅ Shows only to you
- ✅ Never sent to IRC
- ✅ Good for learning
- ✅ Good for sensitive data

### Key Points
- Default is **public** (sends to IRC)
- Add **"private"** to keep it local
- Works offline (shows locally)
- Automatic behavior based on connection

## Examples

### Morning Health Check (Public)

```
You: /ai

[In IRC #ops]
<alice> 🏥 Docker Health Check
<alice> ========================================
<alice> 🟢 Summary: 5 healthy, 0 warning, 0 critical
```

### Learning (Private)

```
You: /ai private what does "healthy" mean?

[Only in your chat pane]
AI Assistant (Private):
"Healthy" means the container is running and passing health checks...
```

### Incident (Public)

```
You: /ai prod api

[In IRC #ops]
<bob> ❌ prod-api-1: EXITED, restarts=5
<bob> Recommended: Check logs
```

### Offline Use (Automatic)

```
You: /ai check docker

[In your chat pane]
AI Assistant (Local):
🟢 All systems healthy

System: 💡 Not connected to IRC. Result shown locally only.
```

## Next Steps

1. **Start the TUI**: `python demo.py`
2. **Wait for IRC connection**: Look for "Connected to IRC!"
3. **Try a public command**: `/ai check docker health`
4. **Check IRC channel**: You should see the response!
5. **Try a private command**: `/ai private explain this`
6. **Verify it's local only**: Check IRC channel (should not appear)

Everything is now working as expected! 🎉
