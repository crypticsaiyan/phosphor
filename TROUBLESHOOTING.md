# Cord-TUI Troubleshooting Guide

## Installation Issues

### Problem: `pip install` fails
**Symptoms**: Error messages during dependency installation

**Solutions**:
1. Upgrade pip: `pip install --upgrade pip`
2. Use Python 3.11+: `python3 --version`
3. Install system dependencies first (see below)
4. Try with `--no-cache-dir`: `pip install --no-cache-dir -r requirements.txt`

### Problem: `simpleaudio` won't install
**Symptoms**: Compilation errors, missing headers

**Solutions**:

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install python3-dev libasound2-dev
pip install simpleaudio
```

**macOS**:
```bash
brew install portaudio
pip install simpleaudio
```

**Windows**:
```bash
# Usually works out of the box
pip install simpleaudio
```

**Workaround**: Disable audio in `.cord/config.json`:
```json
"audio": {
  "enabled": false
}
```

### Problem: `magic-wormhole` not found
**Symptoms**: `/send` and `/grab` commands fail

**Solutions**:
1. Install: `pip install magic-wormhole`
2. Verify: `wormhole --version`
3. Add to PATH if needed

**Workaround**: Demo the concept without actual transfers

## Runtime Issues

### Problem: App won't start
**Symptoms**: Import errors, crashes on launch

**Solutions**:
1. Check Python version: `python3 --version` (need 3.11+)
2. Verify all imports: `python -c "import textual, bottom"`
3. Check for syntax errors: `python -m py_compile src/main.py`
4. Run with verbose errors: `python -m src.main --verbose`

### Problem: IRC connection fails
**Symptoms**: "Connection failed" message, no messages

**Solutions**:
1. Check network: `ping irc.libera.chat`
2. Check firewall: Allow port 6667
3. Try different server in `.cord/config.json`
4. Check server status: https://libera.chat/

**Workaround**: Use mock data for demo:
```python
# In src/ui/app.py, add dummy messages
self.chat_pane.add_message("Alice", "Hello from IRC!")
```

### Problem: Teletext (F1) shows errors
**Symptoms**: Blank screen, Python errors

**Solutions**:
1. Check plotext: `python -c "import plotext"`
2. Verify terminal supports colors: `echo $TERM`
3. Try different terminal emulator
4. Check Docker: `docker ps` (for live stats)

**Workaround**: Use static data instead of live stats

### Problem: No audio feedback
**Symptoms**: Silent operation, no sounds

**Solutions**:
1. Check audio enabled: `.cord/config.json` → `"enabled": true`
2. Test simpleaudio: `python -c "import simpleaudio"`
3. Check system volume
4. Verify audio device: `aplay -l` (Linux) or `system_profiler SPAudioDataType` (macOS)

**Workaround**: Visual indicators instead:
```python
# Add to chat_pane.py
if "error" in message.lower():
    self.add_message("System", "🔴 ERROR DETECTED", is_system=True)
```

### Problem: Wormhole transfers fail
**Symptoms**: Timeout, connection refused

**Solutions**:
1. Check wormhole installed: `wormhole --version`
2. Test manually: `wormhole send test.txt`
3. Check network/firewall
4. Try with `--relay-url` option

**Workaround**: Show code generation, explain concept

## UI Issues

### Problem: Colors look wrong
**Symptoms**: Washed out, incorrect theme

**Solutions**:
1. Check terminal supports 256 colors: `echo $TERM`
2. Try different terminal: iTerm2, Alacritty, Windows Terminal
3. Force color mode: `export TERM=xterm-256color`
4. Adjust `styles.tcss` colors

### Problem: Layout is broken
**Symptoms**: Overlapping widgets, wrong sizes

**Solutions**:
1. Resize terminal: Minimum 80x24
2. Check Textual version: `pip show textual`
3. Clear terminal: `clear` or `reset`
4. Restart app

### Problem: Input lag
**Symptoms**: Slow typing, delayed responses

**Solutions**:
1. Check CPU usage: `top` or `htop`
2. Reduce message history (limit chat_pane messages)
3. Disable audio if enabled
4. Check for infinite loops in code

## Demo Issues

### Problem: Demo script fails
**Symptoms**: `demo.py` crashes or hangs

**Solutions**:
1. Run directly: `python demo.py`
2. Check asyncio: `python -c "import asyncio"`
3. Simplify script (remove async if needed)

### Problem: Presentation lag
**Symptoms**: Slow screen transitions, stuttering

**Solutions**:
1. Close other apps
2. Increase terminal font size (18pt+)
3. Use hardware-accelerated terminal
4. Pre-load screens before demo

### Problem: Audio too loud/quiet
**Symptoms**: Can't hear or too overwhelming

**Solutions**:
1. Adjust volume in `.cord/config.json`: `"volume": 0.3`
2. Adjust system volume
3. Modify frequencies in `audio.py`
4. Test before demo: `python demo.py`

## Development Issues

### Problem: Changes not reflected
**Symptoms**: Code edits don't appear

**Solutions**:
1. Restart app (Ctrl+C, then rerun)
2. Check file saved
3. Clear Python cache: `find . -type d -name __pycache__ -exec rm -rf {} +`
4. Verify correct file being edited

### Problem: Import errors
**Symptoms**: `ModuleNotFoundError`

**Solutions**:
1. Check virtual environment activated: `which python`
2. Install in correct env: `pip install -r requirements.txt`
3. Check PYTHONPATH: `echo $PYTHONPATH`
4. Use absolute imports: `from src.core import ...`

### Problem: Textual CSS not loading
**Symptoms**: No styling, default appearance

**Solutions**:
1. Check `CSS_PATH` in `app.py`: `CSS_PATH = "styles.tcss"`
2. Verify file exists: `ls src/ui/styles.tcss`
3. Check for CSS syntax errors
4. Use inline styles as fallback

## Platform-Specific Issues

### Linux
**Problem**: Permission denied for audio
**Solution**: Add user to audio group: `sudo usermod -a -G audio $USER`

**Problem**: Terminal doesn't support Unicode
**Solution**: Install fonts: `sudo apt-get install fonts-noto`

### macOS
**Problem**: `bottom` SSL errors
**Solution**: Update certificates: `pip install --upgrade certifi`

**Problem**: Terminal colors wrong
**Solution**: Use iTerm2 or Alacritty instead of Terminal.app

### Windows
**Problem**: ANSI colors not working
**Solution**: Use Windows Terminal (not CMD or PowerShell ISE)

**Problem**: Path issues
**Solution**: Use forward slashes or raw strings: `r"C:\path\to\file"`

## Performance Issues

### Problem: High memory usage
**Symptoms**: >100MB RAM

**Solutions**:
1. Limit message history (clear old messages)
2. Disable audio if not needed
3. Check for memory leaks (use `tracemalloc`)
4. Restart app periodically

### Problem: High CPU usage
**Symptoms**: >10% CPU when idle

**Solutions**:
1. Check for infinite loops
2. Reduce update frequency
3. Profile code: `python -m cProfile src/main.py`
4. Optimize hot paths

## Emergency Fallbacks

### If everything fails:
1. **Show the code**: Walk through architecture
2. **Show screenshots**: Pre-recorded demo
3. **Explain the concept**: Focus on innovation
4. **Show mock data**: Fake the features

### Backup demo plan:
1. Show logo: `cat assets/logo.txt`
2. Show file structure: `tree src/`
3. Explain architecture: Use ARCHITECTURE.md
4. Show code highlights: Key files in editor
5. Show comparison: COMPARISON.md

## Getting Help

### Resources
- Textual Discord: https://discord.gg/Enf6Z3qhVr
- Python IRC: #python on irc.libera.chat
- Stack Overflow: Tag with `textual`, `python-asyncio`

### Debug Mode
Add to `src/main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Verbose Output
Run with:
```bash
python -m src.main 2>&1 | tee debug.log
```

## Prevention

### Before Demo
- [ ] Test on fresh machine
- [ ] Test with fresh Python env
- [ ] Record backup video
- [ ] Prepare screenshots
- [ ] Have fallback plan
- [ ] Test audio levels
- [ ] Check network connection
- [ ] Verify all dependencies

### During Demo
- [ ] Have backup terminal ready
- [ ] Keep demo.py running
- [ ] Monitor system resources
- [ ] Have code editor open
- [ ] Keep documentation handy

## Common Error Messages

### `ModuleNotFoundError: No module named 'textual'`
**Fix**: `pip install textual`

### `ImportError: cannot import name 'bottom'`
**Fix**: `pip install bottom`

### `FileNotFoundError: [Errno 2] No such file or directory: '.cord/config.json'`
**Fix**: Create config file or run from project root

### `ConnectionRefusedError: [Errno 111] Connection refused`
**Fix**: Check IRC server, network, firewall

### `OSError: [Errno -9996] Invalid output device`
**Fix**: Check audio device, disable audio, or install audio drivers

## Still Stuck?

1. Check the logs: Look for error messages
2. Simplify: Remove features until it works
3. Ask for help: Use resources above
4. Document: Note the error for future reference
5. Move on: Focus on what works for the demo

Remember: A partial demo is better than no demo. Focus on your strongest features!
