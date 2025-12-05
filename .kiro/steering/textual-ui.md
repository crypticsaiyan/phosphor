---
inclusion: fileMatch
fileMatchPattern: "src/ui/**/*.py"
---

# Textual UI Guidelines

## Widget Development
- Extend from `textual.widget.Widget` or existing Textual widgets
- Use `compose()` method for widget hierarchy
- Implement `on_mount()` for initialization logic
- Use reactive attributes for state management

## Styling
- Styles defined in `src/ui/styles.tcss`
- Use Discord color palette: #36393f (background), #5865F2 (accent)
- Support both light and dark themes

## Screen Management
- Use `push_screen()` / `pop_screen()` for modal views
- Teletext dashboard toggles with F1 key
- Keep screens in `src/ui/screens.py`

## Event Handling
- Use `@on()` decorator for event handlers
- Async handlers for network operations
- Thread-safe updates from background tasks

## Reference
- Styles: #[[file:src/ui/styles.tcss]]
- Main App: #[[file:src/ui/app.py]]
