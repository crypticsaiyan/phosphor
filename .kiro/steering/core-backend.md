---
inclusion: fileMatch
fileMatchPattern: "src/core/**/*.py"
---

# Core Backend Guidelines

## IRC Client
- Use async/await for all IRC operations
- Implement callback pattern for message handling
- Handle reconnection gracefully
- Reference: #[[file:src/core/irc_client.py]]

## MCP Integration
- Tools registered in `mcp_client.py`
- Return structured JSON responses
- Add new tools to the tools registry dict
- Reference: #[[file:src/core/mcp_client.py]]

## Wormhole File Transfer
- Use magic-wormhole for P2P transfers
- Generate human-readable codes
- Provide status callbacks for UI updates
- Reference: #[[file:src/core/wormhole.py]]

## Audio Sonification
- Map log levels to audio frequencies
- Thread-safe playback
- Escalating sounds for error rates
- Reference: #[[file:src/core/audio.py]]

## Azure Integration
- Use azure-identity for authentication
- Container management via azure-mgmt-containerinstance
- Reference: #[[file:src/core/azure_bot_client.py]]
