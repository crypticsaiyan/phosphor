"""Application entry point."""

import asyncio
from src.ui.app import CordTUI


def main():
    """Launch the Cord-TUI application."""
    app = CordTUI()
    app.run()


if __name__ == "__main__":
    main()
