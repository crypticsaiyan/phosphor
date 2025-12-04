# `/ai` Command - Quick Reference

## TL;DR

**Send to IRC channel:**
```
/ai check docker health
```

**Keep it private (local only):**
```
/ai private explain this
```

That's it! 🎉

## Commands

| Command | Where It Goes | Use For |
|---------|--------------|---------|
| `/ai` | IRC channel | Team updates |
| `/ai <query>` | IRC channel | Health checks |
| `/ai prod` | IRC channel | Production status |
| `/ai private <query>` | Local only | Learning |
| `/ai private explain X` | Local only | Questions |

## Examples

### Public (Everyone Sees)

```
/ai                          → IRC channel
/ai check docker health      → IRC channel
/ai prod                     → IRC channel
/ai staging web              → IRC channel
```

### Private (Only You See)

```
/ai private explain health checks     → Local only
/ai private what does "healthy" mean? → Local only
/ai private show me logs              → Local only
```

## Behavior

### When Connected to IRC

**Public:**
```
You: /ai check docker

[Sent to IRC #ops]
<you> 🟢 All systems healthy
```

**Private:**
```
You: /ai private explain this

[Only in your chat pane]
AI Assistant (Private):
Explanation here...
```

### When NOT Connected to IRC

**Any command:**
```
You: /ai check docker

[In your chat pane]
AI Assistant (Local):
🟢 All systems healthy

System: 💡 Not connected to IRC. Result shown locally only.
```

## Quick Test

```bash
# 1. Start TUI
python demo.py

# 2. Wait for "Connected to IRC!"

# 3. Try public command
/ai check docker health

# 4. Check IRC channel - you should see it!

# 5. Try private command
/ai private explain health checks

# 6. Check IRC channel - should NOT see it (local only)
```

## Troubleshooting

### Nothing happens?

- Check: `/ai` with slash and space ✅
- Check: Docker running? `docker ps`
- Check: Permissions? `./fix_docker_permissions.sh`

### Not in IRC channel?

- Check: "Connected to IRC!" message?
- Check: Joined a channel?
- Check: Used `/ai private`? (local only by design)

## Summary

- **Default = Public** (sends to IRC)
- **Add "private" = Local** (only you see)
- **Works offline** (shows locally with warning)

Simple! 🚀

---

**Full guide:** [AI_COMMAND_GUIDE.md](AI_COMMAND_GUIDE.md)
