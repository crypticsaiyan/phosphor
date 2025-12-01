# Cord-TUI Testing Checklist

## Pre-Demo Setup

### Environment
- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] No syntax errors (`python -m py_compile src/**/*.py`)

### Optional Dependencies
- [ ] simpleaudio working (test with `python -c "import simpleaudio"`)
- [ ] magic-wormhole installed (test with `wormhole --version`)
- [ ] Docker running (test with `docker ps`)

### Configuration
- [ ] `.cord/config.json` exists and is valid JSON
- [ ] IRC server details are correct
- [ ] Audio settings configured

## Feature Testing

### 1. Basic UI
- [ ] App launches without errors
- [ ] 3-pane layout renders correctly
- [ ] Sidebar shows channels
- [ ] Member list shows users
- [ ] Input bar is visible and focused
- [ ] Colors match Discord theme

### 2. Chat Functionality
- [ ] Can type in input bar
- [ ] Messages appear in chat pane
- [ ] Markdown renders correctly (bold, code blocks)
- [ ] System messages are styled differently
- [ ] Chat scrolls automatically

### 3. IRC Connection
- [ ] Connects to IRC server
- [ ] Joins configured channels
- [ ] Receives messages from others
- [ ] Can send messages to channel
- [ ] Handles disconnections gracefully

### 4. Teletext Dashboard (F1)
- [ ] F1 toggles to Teletext screen
- [ ] Retro colors render correctly (cyan, yellow, magenta)
- [ ] ASCII charts display
- [ ] System stats are shown
- [ ] F1 returns to chat screen
- [ ] Transition is smooth

### 5. Wormhole File Transfer
- [ ] `/send <file>` generates a code
- [ ] Code is displayed in chat
- [ ] Code is human-readable (e.g., "7-guitar-ocean")
- [ ] `/grab <code>` initiates receive
- [ ] File transfers successfully
- [ ] Status messages appear in chat
- [ ] Handles missing files gracefully
- [ ] Handles invalid codes gracefully

### 6. MCP Commands
- [ ] `/ai docker-stats` returns data
- [ ] `/ai system-info` returns data
- [ ] `/ai analyze-db` returns data
- [ ] Results are formatted as embeds
- [ ] Embeds have colored borders
- [ ] JSON is syntax-highlighted
- [ ] Unknown commands show error

### 7. Audio Feedback
- [ ] INFO messages play quiet tick
- [ ] ERROR messages play loud thud
- [ ] CRITICAL messages play crackle
- [ ] Sounds don't block UI
- [ ] Volume is appropriate
- [ ] Can be disabled in config

### 8. Edge Cases
- [ ] Handles empty messages
- [ ] Handles very long messages
- [ ] Handles rapid message spam
- [ ] Handles network disconnection
- [ ] Handles invalid commands
- [ ] Handles missing files
- [ ] Handles terminal resize

## Demo Simulation

### Setup
- [ ] `demo.py` runs without errors
- [ ] Simulates normal operations
- [ ] Simulates warnings
- [ ] Simulates errors
- [ ] Simulates critical failures
- [ ] Audio escalates appropriately

### Timing
- [ ] Demo completes in ~60 seconds
- [ ] Pacing is appropriate
- [ ] Audio is audible but not overwhelming

## Performance Testing

### Memory
- [ ] Initial memory < 50MB
- [ ] Memory stable over time
- [ ] No memory leaks after 1000 messages

### CPU
- [ ] Idle CPU < 5%
- [ ] Active CPU < 20%
- [ ] No CPU spikes

### Responsiveness
- [ ] UI responds instantly to input
- [ ] No lag when typing
- [ ] Smooth scrolling
- [ ] Fast screen transitions

## Presentation Checklist

### Before Demo
- [ ] Terminal font size is large (18pt+)
- [ ] Terminal colors are vibrant
- [ ] Screen recording software ready
- [ ] Backup video prepared
- [ ] Demo script memorized
- [ ] Sample files prepared

### During Demo
- [ ] Speak clearly and confidently
- [ ] Show logo first (`cat assets/logo.txt`)
- [ ] Explain the pitch (30s)
- [ ] Demo each feature (2m)
- [ ] Handle questions gracefully
- [ ] End with the closer (15s)

### Backup Plans
- [ ] If IRC fails: Use mock data
- [ ] If audio fails: Show visual indicators
- [ ] If wormhole fails: Explain concept
- [ ] If Docker fails: Use mock stats

## Documentation Review

- [ ] README.md is clear and concise
- [ ] QUICKSTART.md has correct commands
- [ ] ARCHITECTURE.md is accurate
- [ ] DEMO_SCRIPT.md is rehearsed
- [ ] PROJECT_SUMMARY.md is compelling

## Code Quality

- [ ] No syntax errors
- [ ] No import errors
- [ ] Consistent style (PEP 8)
- [ ] Meaningful variable names
- [ ] Comments where needed
- [ ] No debug print statements
- [ ] No TODO comments

## Git & Deployment

- [ ] All files committed
- [ ] .gitignore is correct
- [ ] README has installation instructions
- [ ] Requirements.txt is complete
- [ ] License file added (if needed)
- [ ] GitHub repo is public
- [ ] Repo has good description

## Final Checks

- [ ] Run full demo end-to-end
- [ ] Time the demo (should be ~3 minutes)
- [ ] Test on fresh machine
- [ ] Test with fresh Python environment
- [ ] Get feedback from teammate
- [ ] Practice presentation 3+ times

## Emergency Contacts

- Textual Discord: [Link]
- Python IRC: #python on Libera.Chat
- magic-wormhole issues: [GitHub]

## Notes

Use this space for any issues encountered during testing:

---

**Last tested**: [Date]  
**Tested by**: [Name]  
**Environment**: [OS, Python version]  
**Status**: [ ] Pass [ ] Fail [ ] Needs work
