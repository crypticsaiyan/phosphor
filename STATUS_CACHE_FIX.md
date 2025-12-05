# Container Status Cache Fix

## Problem
When running `/ai show status`, containers were always shown as "running" even after they were stopped in Azure. This was due to cached data being used instead of fetching real-time status.

## Root Cause
The `AzureContainerManager.get_all_containers()` method uses a 30-second cache to avoid excessive API calls. When the `answer_question()` method handled status queries, it used the cached data without forcing a refresh.

**Before:**
```python
def answer_question(self, question: str) -> str:
    containers = self.get_all_containers()  # Uses cache
    
    if 'status' in question_lower:
        running = [c for c in containers if c['status'] in ['Running', 'Succeeded']]
        # ... shows cached status
```

## Solution
Force a cache refresh when querying real-time status information.

**After:**
```python
def answer_question(self, question: str) -> str:
    containers = self.get_all_containers()  # Initial fetch (may use cache)
    
    if 'status' in question_lower:
        containers = self.get_all_containers(force_refresh=True)  # Force refresh
        running = [c for c in containers if c['status'] in ['Running', 'Succeeded']]
        # ... shows real-time status
```

## Changes Made

### File: `src/azure_container_manager.py`

1. **Status Query (line ~233)**: Added `force_refresh=True` when handling status queries
2. **Health Check (line ~280)**: Added `force_refresh=True` when checking container health

Both of these operations require real-time data to be accurate.

## Testing

Run the test script to verify the fix:

```bash
python test_status_fix.py
```

### Manual Test Steps:
1. Run `/ai show status` - note all containers shown as running
2. Stop a container in Azure Portal
3. Wait a few seconds
4. Run `/ai show status` again
5. **Expected**: Stopped container should now show as stopped
6. **Before fix**: Would still show as running (cached)

## Impact

- Status queries now always show real-time data
- Health checks use fresh container information
- Other queries (IPs, ports, resources) can still use cache for performance
- Cache still helps reduce API calls for non-critical queries

## Cache Behavior

The cache is still useful for:
- Listing containers (general overview)
- Getting IPs and ports (rarely change)
- Resource information (static)
- Location data (never changes)

The cache is bypassed for:
- Status checks (need real-time state)
- Health checks (need current status)

## Performance Note

Status queries now make an API call to Azure every time, which adds ~1-2 seconds latency. This is acceptable because:
1. Status accuracy is critical
2. Users expect real-time information when checking status
3. The cache still helps for other query types
