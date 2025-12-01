#!/bin/bash
# Cord-TUI Setup Script

echo "🚀 Setting up Cord-TUI..."
echo "================================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check for optional dependencies
echo ""
echo "🔍 Checking optional dependencies..."

# Check for audio support
if ! python3 -c "import simpleaudio" 2>/dev/null; then
    echo "⚠️  Audio support not available. Install system dependencies:"
    echo "   Ubuntu/Debian: sudo apt-get install python3-dev libasound2-dev"
    echo "   macOS: brew install portaudio"
fi

# Check for wormhole
if ! command -v wormhole &> /dev/null; then
    echo "⚠️  magic-wormhole not found in PATH. File transfers may not work."
    echo "   Install with: pip install magic-wormhole"
fi

# Check for Docker (for MCP demo)
if ! command -v docker &> /dev/null; then
    echo "ℹ️  Docker not found. MCP docker-stats command will not work."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run Cord-TUI:"
echo "  source venv/bin/activate"
echo "  python -m src.main"
echo ""
echo "To run the demo:"
echo "  python demo.py"
echo ""
echo "Press F1 in the app to toggle Teletext dashboard"
echo "================================"
