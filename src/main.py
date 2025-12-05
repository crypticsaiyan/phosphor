"""Application entry point."""

import asyncio
from src.ui.app import Phosphor


def main():
    """Launch the phosphor application."""
    app = Phosphor()
    app.run()


if __name__ == "__main__":
    main()
