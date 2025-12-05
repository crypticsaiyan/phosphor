# Phosphor Project Guidelines

## Project Overview
Phosphor is a terminal-based IRC client combining IRC protocol with Discord-like UX. Built with Python 3.11+ using Textual for the TUI framework.

## Architecture
- **Core Layer** (`src/core/`): Backend logic - IRC client, MCP integration, wormhole file transfer, audio sonification
- **UI Layer** (`src/ui/`): Textual-based frontend - app, screens, widgets, styles
- **Config** (`.phosphor/`): User configuration and settings

## Key Technologies
- Textual for TUI
- miniirc for IRC protocol
- magic-wormhole for P2P file transfers
- psutil for system metrics
- Azure SDK for container management

## Code Style
- Use async/await for all network operations
- Keep UI and backend decoupled via callbacks
- Thread-safe UI updates using `call_from_thread`
- Follow PEP 8 conventions

## Testing
- Run tests with: `pytest tests/`
- Demo scripts available: `demo.py`, `demo_teletext.sh`

## Key Commands
- `python -m src.main` - Run the application
- `./setup.sh` - Initial setup
- `F1` - Toggle Teletext dashboard
- `/ai` - DevOps health bot commands
