# Cord-TUI Quick Start

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or use uv (recommended)
uv pip install -r requirements.txt
```

## Running the App

```bash
python -m src.main
```

## Key Features to Demo

### 1. Discord-Like Interface
- 3-pane layout: Channels | Chat | Members
- Markdown support in messages
- Rich embeds for AI responses

### 2. Teletext Dashboard (F1)
- Press F1 to toggle
- Retro 1980s Ceefax-style interface
- Live system metrics with ASCII charts
- Press F1 again to return to chat

### 3. Wormhole File Transfer
```
/send <filepath>     # Send a file, get a code
/grab <code>         # Receive a file with the code
```

Example:
```
/send config.json
# Returns: Code: 7-guitar-ocean
# Teammate runs: /grab 7-guitar-ocean
```

### 4. AI Commands (MCP)
```
/ai docker-stats     # Get Docker container stats
/ai system-info      # Get system information
/ai analyze-db       # Analyze database (demo)
```

### 5. Geiger Counter Audio
- Automatic audio feedback for log events
- INFO: Quiet tick
- ERROR: Loud thud
- CRITICAL: Geiger counter crackle

## Configuration

Edit `.cord/config.json` to customize:
- IRC servers and channels
- Theme colors
- Audio settings

## Demo Script

Run the demo simulation:
```bash
python demo.py
```

This simulates a server dying with increasing error rates, perfect for showcasing the Geiger counter feature.

## Troubleshooting

### No audio?
Install simpleaudio dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev libasound2-dev

# macOS
brew install portaudio
```

### Wormhole not working?
Install magic-wormhole:
```bash
pip install magic-wormhole
```

### IRC connection fails?
Check your network and firewall settings. The default config connects to irc.libera.chat:6667.

## Architecture

```
src/
├── core/           # Backend logic
│   ├── irc_client.py    # IRC connection
│   ├── mcp_client.py    # AI/MCP integration
│   ├── wormhole.py      # P2P file transfer
│   └── audio.py         # Geiger counter
└── ui/             # Frontend (Textual)
    ├── app.py           # Main app
    ├── screens.py       # Teletext screen
    └── widgets/         # Custom components
```

## Next Steps

1. Customize the theme in `src/ui/styles.tcss`
2. Add more MCP tools in `src/core/mcp_client.py`
3. Connect to your own IRC server
4. Add custom audio samples in `.cord/sounds/`
