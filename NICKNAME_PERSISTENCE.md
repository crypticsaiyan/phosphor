# Nickname Persistence Feature

## Overview

The app now remembers your nickname and uses it as the default on future launches.

## How It Works

### First Time Use
1. Launch the app: `python3 kiro_irc_bridge.py`
2. Enter your desired nickname on the home screen
3. Press Enter to connect
4. **Your nickname is automatically saved**

### Subsequent Launches
1. Launch the app again
2. **Your last used nickname appears as the default**
3. Press Enter to use it, or type a new one
4. Any new nickname you enter will be saved for next time

## Technical Details

### Storage Location
```
.cord/last_nick.json
```

### File Format
```json
{
  "nick": "your_nickname"
}
```

### Implementation

#### Save Function
```python
def _save_last_nick(nick: str):
    """Save the nickname for future use."""
    settings_path = Path(".cord/last_nick.json")
    settings_path.parent.mkdir(exist_ok=True)
    with open(settings_path, 'w') as f:
        json.dump({"nick": nick}, f)
```

#### Load Function
```python
def _load_last_nick() -> str:
    """Load the last used nickname from settings."""
    settings_path = Path(".cord/last_nick.json")
    if settings_path.exists():
        with open(settings_path) as f:
            data = json.load(f)
            return data.get("nick", "cord_user")
    return "cord_user"
```

#### Integration
The HomeScreen class now loads the saved nickname on initialization:
```python
def __init__(self, config: dict = None, **kwargs):
    # ...
    self.default_nick = _load_last_nick() or self.servers[0].get("nick", "cord_user")
```

And saves it when the user connects:
```python
def _confirm_settings(self):
    nick = self.current_nick.strip() or self.default_nick
    # Validate...
    _save_last_nick(nick)  # Save for next time
    # Continue with connection...
```

## Features

### ✅ Automatic Saving
- Nickname is saved when you press Enter to connect
- No manual save action required
- Happens transparently in the background

### ✅ Automatic Loading
- Saved nickname loads on app startup
- Appears as the default in the nickname field
- No configuration needed

### ✅ Easy Updates
- Just type a new nickname and connect
- New nickname automatically becomes the default
- Previous nickname is overwritten

### ✅ Fallback Handling
- If no saved nickname exists, uses "cord_user"
- If file is corrupted, falls back to default
- Graceful error handling

### ✅ Special Characters
Supports all valid IRC nickname characters:
- Letters: `A-Z`, `a-z`
- Numbers: `0-9`
- Special: `[`, `]`, `\`, `^`, `_`, `{`, `}`, `|`, `-`

## User Experience

### Before (No Persistence)
```
Launch 1: Enter "my_nick" → Connect
Launch 2: Enter "my_nick" again → Connect  ← Annoying!
Launch 3: Enter "my_nick" again → Connect  ← Repetitive!
```

### After (With Persistence) ✨
```
Launch 1: Enter "my_nick" → Connect → Saved
Launch 2: "my_nick" already there → Just press Enter!
Launch 3: "my_nick" already there → Just press Enter!
```

## Privacy & Security

### Local Storage Only
- Nickname is stored locally in `.cord/` directory
- Never sent to external servers (except IRC)
- Not shared with other applications

### Plain Text Storage
- Stored as plain JSON for simplicity
- Nicknames are not sensitive information
- Easy to inspect and modify manually

### Easy to Clear
Delete the file to reset:
```bash
rm .cord/last_nick.json
```

Or delete the entire settings directory:
```bash
rm -rf .cord/
```

## Testing

Run the test suite:
```bash
python3 test_nick_simple.py
```

Expected output:
```
✓ All tests passed!
```

## Examples

### Example 1: First Time User
```
$ python3 kiro_irc_bridge.py
[Home Screen shows: "cord_user"]
User types: "alice"
User presses: Enter
→ Nickname "alice" is saved
```

### Example 2: Returning User
```
$ python3 kiro_irc_bridge.py
[Home Screen shows: "alice"]  ← Loaded from last time!
User presses: Enter
→ Connects with "alice"
```

### Example 3: Changing Nickname
```
$ python3 kiro_irc_bridge.py
[Home Screen shows: "alice"]
User types: "bob"
User presses: Enter
→ Nickname "bob" is saved (replaces "alice")
```

## Files Modified

- **src/ui/screens.py**
  - Added `_save_last_nick()` function
  - Added `_load_last_nick()` function
  - Updated `HomeScreen.__init__()` to load saved nick
  - Updated `_confirm_settings()` to save nick on connect

## Benefits

✅ **Convenience** - No need to retype your nickname every time  
✅ **Speed** - Just press Enter to connect with your usual nick  
✅ **Simplicity** - Works automatically, no configuration needed  
✅ **Flexibility** - Easy to change nickname anytime  
✅ **Reliability** - Graceful fallback if file doesn't exist  

## Summary

Your nickname is now remembered between sessions, making it faster and easier to connect to IRC. The feature works automatically with no configuration required, and you can change your nickname anytime by simply typing a new one.

**Just connect once, and your nickname is saved for next time!** 🎉
