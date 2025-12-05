# Azure Container: Status vs State

## The Confusion

Azure Container Instances have TWO different concepts that are easy to confuse:

### 1. `status` - Runtime State (What the container is doing NOW)
This comes from `instance_view.current_state.state`

**Possible values:**
- `Running` - Container is actively running
- `Terminated` - Container has stopped
- `Waiting` - Container is waiting to start
- `Succeeded` - Container ran and completed successfully (for jobs)

**This is what we care about for "is it running?"**

### 2. `state` - Provisioning State (Did Azure create it successfully?)
This comes from `provisioning_state`

**Possible values:**
- `Succeeded` - Azure successfully provisioned the container
- `Failed` - Azure failed to provision the container
- `Pending` - Azure is still provisioning

**This tells us if Azure setup worked, NOT if the container is running**

## The Bug

### Original Code (WRONG):
```python
is_running = c['status'] in ['Running', 'Succeeded'] or c['state'] == 'Succeeded'
```

This logic says: "A container is running if its status is Running/Succeeded OR if provisioning succeeded"

**Problem:** A container can have:
- `status = 'Terminated'` (container stopped)
- `state = 'Succeeded'` (provisioning worked)

The `or c['state'] == 'Succeeded'` part made ALL successfully provisioned containers appear as "running", even if they were stopped!

### Fixed Code (CORRECT):
```python
is_running = c['status'] in ['Running', 'Succeeded']
```

This logic says: "A container is running if its runtime status is Running or Succeeded"

**Result:** Only checks the actual runtime state, ignoring provisioning state.

## Real Example

From your output:

```
kiroocontainer: status=Terminated, state=Succeeded
```

**What this means:**
- Azure successfully created the container (`state=Succeeded`)
- But the container is currently stopped (`status=Terminated`)

**Before fix:** Shown as "running" ❌
**After fix:** Shown as "stopped" ✅

## Summary

| Field | What it means | Use for |
|-------|---------------|---------|
| `status` | Is container running NOW? | Determining if container is up |
| `state` | Did Azure provision it OK? | Debugging provisioning issues |

**Rule:** Always use `status` to check if a container is running, never use `state`.
