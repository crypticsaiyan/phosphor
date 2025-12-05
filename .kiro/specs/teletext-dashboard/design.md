# Teletext Dashboard Design

## Architecture

### Screen Component
Location: `src/ui/screens.py` - `TeletextScreen` class

### Data Flow
```
F1 Press → app.py → push_screen(TeletextScreen)
         → psutil (CPU/Memory)
         → Docker API (containers)
         → Git subprocess (commits)
         → plotext (ASCII charts)
         → Render to terminal
```

## Correctness Properties

### CP1: Toggle Behavior
- F1 pushes TeletextScreen onto screen stack
- Second F1 pops screen, returning to chat
- No state loss in underlying chat view

### CP2: Color Compliance
- Only 8 teletext colors used
- No gradients or extended palette
- High contrast for readability

### CP3: Data Freshness
- Metrics refresh every 1 second
- No stale data displayed
- Graceful handling if data source unavailable

### CP4: Performance
- Dashboard render < 100ms
- No blocking of main event loop
- Async data fetching

## Dependencies
- psutil for system metrics
- plotext for ASCII charts
- Docker SDK (optional) for container status

## References
- #[[file:src/ui/screens.py]]
- #[[file:src/core/mcp_client.py]]
