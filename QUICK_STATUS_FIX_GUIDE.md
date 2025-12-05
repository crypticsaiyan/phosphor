# Quick Fix Guide: Container Status Always Shows Running

## The Problem
`/ai show status` was showing all containers as "running" even when some were stopped.

**Two issues found:**
1. Using cached data (30-second TTL) instead of real-time status
2. Wrong logic: checking `state` (provisioning) instead of just `status` (runtime)

## The Fix
Updated `src/azure_container_manager.py` to:
1. Force refresh the cache when checking status
2. Only check `status` field (runtime state), not `state` field (provisioning state)

## What Changed

**Three changes made:**

1. Line ~217: Fixed container summary logic
```python
# Before
is_running = c['status'] in ['Running', 'Succeeded'] or c['state'] == 'Succeeded'

# After  
is_running = c['status'] in ['Running', 'Succeeded']
```

2. Line ~273: Force refresh + fixed logic for status queries
```python
# Before
containers = self.get_all_containers()  # Uses cache
running = [c for c in containers if c['status'] in ['Running', 'Succeeded'] or c['state'] == 'Succeeded']

# After  
containers = self.get_all_containers(force_refresh=True)  # Always fresh
running = [c for c in containers if c['status'] in ['Running', 'Succeeded']]
```

3. Line ~373: Force refresh for health checks
```python
# Before
containers = self.get_all_containers()  # Uses cache

# After  
containers = self.get_all_containers(force_refresh=True)  # Always fresh
```

## Test It

```bash
# Run the test script
python test_status_fix.py

# Or test manually in your IRC client
/ai show status
```

## How to Verify

1. Check status: `/ai show status` (all running)
2. Stop a container in Azure Portal
3. Wait 5 seconds
4. Check status again: `/ai show status` (should show stopped)

**Before fix:** Would still show as running (cached + wrong logic)  
**After fix:** Shows actual state (refreshed + correct logic)

Example: Container with `status=Terminated, state=Succeeded`
- Before: Shown as "running" (because state=Succeeded)
- After: Shown as "stopped" (because status=Terminated)

## Why This Works

- Status queries need real-time accuracy
- Cache is bypassed for status/health checks
- Other queries (IPs, ports) still use cache for speed
- No performance impact on non-critical queries

## Files Modified

- `src/azure_container_manager.py` (3 changes)
- `test_status_fix.py` (new test script)
- `STATUS_CACHE_FIX.md` (detailed documentation)
- `STATUS_VS_STATE_EXPLAINED.md` (explains status vs state)
