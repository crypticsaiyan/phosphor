---
inclusion: fileMatch
fileMatchPattern: "**/*.py"
---

# Python Development Guidelines

## Version
- Python 3.11+ required

## Dependencies
- Install via: `pip install -r requirements.txt`
- Key packages: textual, miniirc, magic-wormhole, psutil, azure-*

## Async Patterns
- Use `asyncio` for concurrent operations
- Prefer `async def` over threading where possible
- Use `asyncio.create_task()` for background operations

## Error Handling
- Use specific exception types
- Log errors appropriately
- Graceful degradation for optional features (audio, Azure)

## Type Hints
- Use type hints for function signatures
- Import from `typing` module as needed

## Imports
- Standard library first
- Third-party packages second
- Local imports last
- Use absolute imports from `src`
