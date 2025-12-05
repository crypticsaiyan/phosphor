# Quick UI Enhancement Guide

## What Changed?

### 1. ✨ Centered Search/Join Dialog
The channel search panel now appears perfectly centered on your screen.

**How to use:**
- Press `Ctrl+J` or type `/join`
- Dialog appears in the center of the screen
- Type channel name and press Enter

### 2. 📊 Dynamic Teletext Dashboard
The teletext screen (F1) now shows real-time system performance.

**How to use:**
- Press `F1` to open dashboard
- View live metrics that update every second:
  - CPU usage with color-coded bar
  - Memory usage (percentage and GB)
  - Disk usage
  - Network traffic (sent/received)
- Press `F1` again to return to chat

## Visual Examples

### Teletext Dashboard Display
```
System Performance
──────────────────
CPU:    ████████░░░░░░░░░░░░  40.0%
Memory: ██████████░░░░░░░░░░  50.0% (3.7/7.5GB)
Disk:   ██████████████░░░░░░  72.3%
Net TX:    272.7 MB  RX:    600.7 MB

IRC Connection
──────────────
CONNECTED TO SERVER ●
Server: irc.libera.chat:6667
Nick:   cord_user
Uptime: 0d 00:15:32
```

### Color Coding
- 🟢 Green (< 50%): Healthy
- 🟡 Yellow (50-75%): Moderate
- 🔴 Red (> 75%): High usage

## Testing

Run demos to see the changes:
```bash
# Test functionality
python3 test_ui_updates.py

# See visual demo
python3 demo_ui_enhancements.py

# Run the app
python3 kiro_irc_bridge.py
```

## Files Modified
- `src/ui/styles.tcss` - Centered dialog
- `src/ui/screens.py` - Dynamic metrics

No breaking changes - everything is backward compatible!
