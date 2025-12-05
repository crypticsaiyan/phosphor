"""Chat pane widget - the center message stream."""

from textual.containers import VerticalScroll
from textual.widgets import Static, Markdown

from src.ui.widgets.user_colors import format_username_colored


class ChatPane(VerticalScroll):
    """The main chat message stream."""
    
    can_focus = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Store messages per channel: {channel: [(author, content, is_system), ...]}
        self.channel_messages = {}
        self.current_channel = None
        self.current_nick = None  # The current user's IRC nick
    
    def add_message(self, author: str, content: str, is_system: bool = False, channel: str = None):
        """Add a message to the chat."""
        # Strip leading colon from content if present (IRC protocol artifact)
        content = content.lstrip(": ")
        
        # Store message in history
        if channel:
            if channel not in self.channel_messages:
                self.channel_messages[channel] = []
            self.channel_messages[channel].append((author, content, is_system))
        
        # Only display if it's for the current channel or no channel specified (system messages)
        if channel is None or channel == self.current_channel:
            if is_system:
                msg_widget = Static(f"[italic yellow]⚙ {content}[/]", classes="system-message")
            else:
                # Use colored username with Rich markup
                colored_author = format_username_colored(author)
                # Add (you) indicator if this is the current user
                if self.current_nick and author == self.current_nick:
                    msg_widget = Static(f"{colored_author} (you): {content}", classes="message")
                else:
                    msg_widget = Static(f"{colored_author}: {content}", classes="message")
            
            self.mount(msg_widget)
            self.scroll_end(animate=False)
    
    def switch_channel(self, channel: str):
        """Switch to a different channel and restore its message history."""
        self.current_channel = channel
        
        # Clear current display
        self.remove_children()
        
        # Restore messages for this channel
        if channel in self.channel_messages:
            for author, content, is_system in self.channel_messages[channel]:
                if is_system:
                    msg_widget = Static(f"[italic yellow]⚙ {content}[/]", classes="system-message")
                else:
                    # Use colored username with Rich markup
                    colored_author = format_username_colored(author)
                    # Add (you) indicator if this is the current user
                    if self.current_nick and author == self.current_nick:
                        msg_widget = Static(f"{colored_author} (you): {content}", classes="message")
                    else:
                        msg_widget = Static(f"{colored_author}: {content}", classes="message")
                self.mount(msg_widget)
        
        self.scroll_end(animate=False)
    
    def add_embed(self, title: str, content: str, embed_type: str = "info"):
        """Add a Discord-style embed card."""
        embed_content = f"**{title}**\n\n{content}"
        embed_widget = Markdown(embed_content)
        embed_widget.add_class("embed")
        
        if embed_type == "success":
            embed_widget.add_class("embed-success")
        elif embed_type == "error":
            embed_widget.add_class("embed-error")
        
        self.mount(embed_widget)
        self.scroll_end(animate=False)
