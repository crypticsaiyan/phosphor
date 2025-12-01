# Cord-TUI Demo Script

## Setup (Before Demo)
1. Have the app running: `python -m src.main`
2. Have a terminal ready for the death simulation: `python demo.py`
3. Prepare a sample file for wormhole demo

## The Pitch (30 seconds)
"This is Cord-TUI. It looks like Discord, right? But it's actually IRC running in your terminal. It uses 20MB of RAM instead of 2GB. And it has three killer features that resurrect dead tech."

## Feature 1: The Interface (15 seconds)
- Point out the 3-pane layout
- "Left: servers and channels. Center: chat with markdown. Right: member list."
- "It's Discord, but it's text-mode and blazing fast."

## Feature 2: Teletext Dashboard (30 seconds)
- Press F1
- "This is Page 100. Remember Ceefax? Teletext from the 80s?"
- "It's a retro dashboard showing live Docker stats."
- "Zero latency. No browser. Just pure terminal graphics."
- Press F1 again to return

## Feature 3: Wormhole Transfer (45 seconds)
- Type: `/send demo.txt`
- "This resurrects IRC's DCC file transfer, but better."
- "It generates a code: 7-guitar-ocean"
- "My teammate types /grab 7-guitar-ocean"
- "The file tunnels peer-to-peer. No cloud. No traces. Pure magic."

## Feature 4: The Geiger Counter (60 seconds)
- "Now for the coolest part. Listen."
- Switch to demo terminal, run: `python demo.py`
- "This simulates a server dying."
- "Hear that? The Geiger counter."
- "Normal requests: quiet ticks."
- "Errors: louder thuds."
- "Critical failures: crackling chaos."
- "I can HEAR the server dying before I even look at logs."

## The Closer (15 seconds)
"Cord-TUI proves modern collaboration doesn't need 2GB of RAM. It just needs better design. IRC isn't dead. It's been waiting for a resurrection."

## Total Time: ~3 minutes

## Backup Demos
If something breaks:
- Show the CSS file (styles.tcss) - "This is how we made it look like Discord"
- Show the wormhole code - "One library, 50 lines, peer-to-peer magic"
- Show the audio engine - "Map log levels to frequencies"
