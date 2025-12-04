# IRC Commands Reference

Quick reference for using the DevOps Channel Assistant in IRC.

## Basic Commands

### Check Docker Health (Public)

```
/ai
/ai check docker health
/ai status
```

**Response:** Goes to the channel (everyone sees it)

**Example:**
```
alice: /ai

devops-ai: 🏥 Docker Health Check
devops-ai: ========================================
devops-ai: 🟢 Summary: 5 healthy, 0 warning, 0 critical
devops-ai: 
devops-ai: Details:
devops-ai: ✅ prod-web-1: RUNNING, healthy, up 2d
devops-ai: ✅ prod-api-1: RUNNING, healthy, up 2d
```

### Filter by Environment (Public)

```
/ai prod
/ai staging
/ai dev
```

**Example:**
```
bob: /ai prod

devops-ai: 🏥 Docker Health Check - Production
devops-ai: ========================================
devops-ai: 🟢 Summary: 3 healthy, 0 warning, 0 critical
```

### Filter by Service (Public)

```
/ai web
/ai api
/ai db
/ai worker
```

**Example:**
```
charlie: /ai web

devops-ai: 🏥 Docker Health Check - Web Services
devops-ai: ========================================
devops-ai: 🟢 Summary: 2 healthy, 0 warning, 0 critical
```

### Combined Filters (Public)

```
/ai prod web
/ai staging api
/ai prod db
```

**Example:**
```
diana: /ai prod api

devops-ai: 🏥 Docker Health Check - Production API
devops-ai: ========================================
devops-ai: 🟢 Summary: 1 healthy, 0 warning, 0 critical
devops-ai: 
devops-ai: Details:
devops-ai: ✅ prod-api-1: RUNNING, healthy, up 2d
```

## Private Commands

### Get Private Explanation

```
/ai private <question>
```

**Response:** Goes only to you (DM)

**Example:**
```
eve: /ai private explain what "healthy" means

[DM from devops-ai to eve]:
Docker Health Status Explained:

**Healthy** means:
1. The container is running
2. The health check command succeeds (exit code 0)
3. The health check has passed consistently
...
```

### Private Detailed Query

```
/ai private show me detailed logs
/ai private explain docker health checks
/ai private how do I configure health checks?
```

**Example:**
```
frank: /ai private explain restart counts

[DM from devops-ai to frank]:
Restart Count Explained:

The restart count shows how many times Docker has
automatically restarted a container. This happens when:

1. Container crashes (exit code != 0)
2. Health check fails repeatedly
3. OOM (out of memory) kill
...
```

## Help Commands

### Show Available Commands

```
/ai help
```

**Example:**
```
grace: /ai help

devops-ai: 🤖 DevOps Health Bot - Available Commands:
devops-ai: 
devops-ai: **Docker Health (Default):**
devops-ai: • /ai - Check all Docker containers
devops-ai: • /ai prod - Check production containers
devops-ai: • /ai staging web - Check staging web containers
...
```

## Advanced Usage

### Check Specific Container

```
/ai <container-name>
```

**Example:**
```
henry: /ai goofy_keldysh

devops-ai: 🏥 Docker Health Check
devops-ai: ========================================
devops-ai: 🟢 Summary: 1 healthy, 0 warning, 0 critical
devops-ai: 
devops-ai: Details:
devops-ai: ✅ goofy_keldysh: RUNNING, up 10m
```

### Ask Questions (Public)

```
/ai why is <service> slow?
/ai what's wrong with <container>?
/ai is <service> up?
```

**Example:**
```
iris: /ai why is prod-api slow?

devops-ai: Checking prod-api health...
devops-ai: 
devops-ai: ⚠️  prod-api-1: High CPU usage (85%)
devops-ai: 
devops-ai: Possible causes:
devops-ai: • High request volume
devops-ai: • Slow database queries
devops-ai: • Memory leak causing GC pressure
devops-ai: 
devops-ai: Recommended actions:
devops-ai: • Check logs: docker logs prod-api-1
devops-ai: • Monitor metrics: docker stats prod-api-1
```

### Ask Questions (Private)

```
/ai private how do I debug <issue>?
/ai private explain <concept>
/ai private draft a message about <topic>
```

**Example:**
```
jack: /ai private how do I debug high CPU?

[DM from devops-ai to jack]:
Debugging High CPU Usage:

1. Check current stats:
   docker stats <container>

2. Identify the process:
   docker exec <container> top

3. Check for CPU-intensive operations:
   - Infinite loops
   - Heavy computation
   - Inefficient algorithms
...
```

## Quick Reference Table

| Command | Visibility | Description |
|---------|-----------|-------------|
| `/ai` | Public | Check all containers |
| `/ai prod` | Public | Check production |
| `/ai staging` | Public | Check staging |
| `/ai web` | Public | Check web services |
| `/ai prod web` | Public | Check prod web |
| `/ai help` | Public | Show help |
| `/ai private <query>` | Private | Private explanation |
| `/ai private explain <topic>` | Private | Detailed explanation |
| `/ai private show <data>` | Private | Sensitive data |

## Tips

### When to Use Public

✅ Health checks
✅ Status updates
✅ Incident summaries
✅ Team-wide information
✅ Action items

### When to Use Private

✅ Learning/explanations
✅ Sensitive data
✅ Verbose output
✅ Personal queries
✅ Drafting messages

### Best Practices

1. **Default to public** for team-relevant info
2. **Use private** for learning or sensitive data
3. **Be specific** in your queries
4. **Use filters** to narrow results (prod, staging, web, api)
5. **Share knowledge** - don't overuse private mode

## Examples by Scenario

### Scenario 1: Morning Health Check

```
alice: /ai

devops-ai: 🟢 All systems healthy
```

### Scenario 2: Incident Response

```
bob: /ai prod api

devops-ai: ❌ prod-api-1: EXITED, restarts=5
devops-ai: 
devops-ai: Recommended actions:
devops-ai: • Check logs: docker logs prod-api-1
devops-ai: • Investigate recent deployments
```

### Scenario 3: Learning

```
charlie: /ai private explain what "restarts=5" means

[DM]: Restart count of 5 means the container has crashed
and been automatically restarted 5 times...
```

### Scenario 4: Debugging

```
diana: /ai private show me environment variables for prod-api

[DM]: ⚠️  Environment variables may contain sensitive info:
- NODE_ENV=production
- DATABASE_URL=postgres://[REDACTED]
...
```

### Scenario 5: Team Update

```
eve: /ai staging

devops-ai: 🟡 staging-web-1: High CPU (80%)
devops-ai: 
devops-ai: Monitoring recommended

frank: Thanks! I'll check it out
```

## Troubleshooting

### Command Not Working

**Problem:** Bot doesn't respond

**Solutions:**
- Check bot is online: Look for "devops-ai" in user list
- Check command prefix: Should be `/ai` (with space)
- Try in DM: `/msg devops-ai help`

### Response Goes to Wrong Place

**Problem:** Expected private response in channel

**Solution:** Use `/ai private <query>` for private responses

### No Containers Found

**Problem:** "No Docker containers found"

**Solution:** Check Docker permissions (see FIX_DOCKER_PERMISSIONS.md)

### Container Names Show as "unknown"

**Problem:** Container names not displaying

**Solution:** This is fixed in the latest version. Update your bot.

## Configuration

The bot uses these defaults:

- **Command prefix:** `/ai `
- **Public by default:** Yes
- **Private keyword:** `private`
- **Channels:** Configured in `kiro_bridge_config.json`

## Summary

- **Public:** `/ai <query>` → Everyone sees response
- **Private:** `/ai private <query>` → Only you see response
- **Default:** Docker health checks
- **Filters:** prod, staging, dev, web, api, db, worker
- **Help:** `/ai help`

Simple and powerful! 🚀
