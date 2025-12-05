"""Sidebar widget - channels and servers."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Static, Tree
from textual.message import Message

from src.ui.widgets.user_colors import format_username_colored


class Sidebar(Container):
    """Left sidebar with channel list."""
    
    class ChannelSelected(Message):
        """Message posted when a channel is selected."""
        
        def __init__(self, channel: str):
            super().__init__()
            self.channel = channel
    
    def __init__(self, channels: list[str], bookmarked_channels: list[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.channels = channels
        self.bookmarked_channels = bookmarked_channels or []
        self.active_channel = None
    
    def compose(self) -> ComposeResult:
        """Compose the sidebar."""
        with Vertical():
            yield Static("CORD-TUI", classes="server-name")
            tree = Tree("Channels")
            tree.root.expand()
            
            # Add bookmarked channels first with a star
            if self.bookmarked_channels:
                for channel in self.bookmarked_channels:
                    tree.root.add_leaf(f"⭐ {channel}", data=channel)
            
            # Add regular channels
            for channel in self.channels:
                if channel not in self.bookmarked_channels:
                    tree.root.add_leaf(channel, data=channel)
            
            yield tree
    
    def on_tree_node_selected(self, event: Tree.NodeSelected):
        """Handle channel selection."""
        if event.node.data:
            self.active_channel = event.node.data
            self.post_message(self.ChannelSelected(event.node.data))
    
    def update_channels(self, channels: list[str]):
        """Update the channel list with new channels."""
        self.channels = channels
        self._refresh_tree()
    
    def add_bookmark(self, channel: str):
        """Add a channel to bookmarks."""
        if channel not in self.bookmarked_channels:
            self.bookmarked_channels.append(channel)
            self._refresh_tree()
    
    def remove_bookmark(self, channel: str):
        """Remove a channel from bookmarks."""
        if channel in self.bookmarked_channels:
            self.bookmarked_channels.remove(channel)
            self._refresh_tree()
    
    def _refresh_tree(self, select_channel: str = None):
        """Refresh the channel tree display."""
        tree = self.query_one(Tree)
        tree.root.remove_children()
        
        # Add bookmarked channels first with a star
        if self.bookmarked_channels:
            for channel in self.bookmarked_channels:
                tree.root.add_leaf(f"⭐ {channel}", data=channel)
        
        # Add regular channels
        for channel in self.channels:
            if channel not in self.bookmarked_channels:
                tree.root.add_leaf(channel, data=channel)
        
        # Select the specified channel or active channel after refresh
        channel_to_select = select_channel or self.active_channel
        if channel_to_select:
            self._select_node_by_channel(tree, channel_to_select)
    
    def _select_node_by_channel(self, tree: Tree, channel: str):
        """Find and select a channel node in the tree."""
        for idx, node in enumerate(tree.root.children):
            if node.data == channel:
                # Line 0 is root "Channels", children start at line 1
                tree.cursor_line = idx + 1
                break
    
    def select_channel(self, channel: str):
        """Select and focus a channel in the tree."""
        self.active_channel = channel
        tree = self.query_one(Tree)
        self._select_node_by_channel(tree, channel)


class MemberList(Container):
    """Right sidebar with member list."""
    
    can_focus = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.members = []
        self.current_nick = None  # The current user's IRC nick
    
    def compose(self) -> ComposeResult:
        """Compose the member list."""
        with Vertical():
            yield Static("Members (0)", id="member-count")
            yield Static("", id="member-names")
    
    def set_current_nick(self, nick: str):
        """Set the current user's nick for highlighting."""
        self.current_nick = nick
    
    def update_members(self, members: list[str]):
        """Update the member list with current channel members."""
        self.members = sorted(members)
        
        # Update count header
        self.query_one("#member-count", Static).update(f"Members ({len(self.members)})")
        
        # Update names list with colored usernames
        lines = []
        for m in self.members:
            # Strip IRC prefixes for comparison
            clean_name = m.lstrip("@+%~&")
            if self.current_nick and clean_name == self.current_nick:
                lines.append(f"• {format_username_colored(m)} (you)")
            else:
                lines.append(f"• {format_username_colored(m)}")
        names_text = "\n".join(lines)
        self.query_one("#member-names", Static).update(names_text)
    
    def show_loading(self, channel: str):
        """Show loading state for member list."""
        self.query_one("#member-count", Static).update(f"Loading {channel}...")
        self.query_one("#member-names", Static).update("Loading...")
