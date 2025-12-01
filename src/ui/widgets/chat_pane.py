"""Chat pane widget - the center message stream."""

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Static, Markdown
from textual.reactive import reactive


class ChatPane(VerticalScroll):
    """The main chat message stream."""
    
    messages = reactive([])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messages = []
    
    def add_message(self, author: str, content: str, is_system: bool = False):
        """Add a message to the chat."""
        if is_system:
            msg_widget = Static(f"[italic yellow]⚙ {content}[/]", classes="system-message")
        else:
            msg_widget = Markdown(f"**{author}**: {content}")
            msg_widget.add_class("message")
        
        self.mount(msg_widget)
        self.scroll_end(animate=False)
    
    def add_embed(self, title: str, content: str, embed_type: str = "info"):
        """Add a Discord-style embed card."""
        embed_class = "embed"
        if embed_type == "success":
            embed_class = "embed embed-success"
        elif embed_type == "error":
            embed_class = "embed embed-error"
        
        embed_content = f"**{title}**\n\n{content}"
        embed_widget = Markdown(embed_content)
        embed_widget.add_class(embed_class)
        
        self.mount(embed_widget)
        self.scroll_end(animate=False)
