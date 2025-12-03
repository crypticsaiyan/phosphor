"""Channel search and join dialog with intelligent suggestions."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Input, ListView, ListItem, Label, Button
from textual.screen import ModalScreen
from textual.message import Message
from textual.binding import Binding
import re
from typing import List, Dict, Set


class ChannelSearchScreen(ModalScreen):
    """Modal screen for searching and joining channels."""
    
    BINDINGS = [
        Binding("escape", "dismiss", "Cancel", show=False),
    ]
    
    class ChannelSelected(Message):
        """Message posted when a channel is selected."""
        def __init__(self, channel: str):
            super().__init__()
            self.channel = channel
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.channels = []
        self.filtered_channels = []
        self.suggestions = []
        self.recent_channels = set()  # Recently joined channels
        self.popular_channels = [  # Common IRC channels
            "#general", "#random", "#help", "#programming", "#python", 
            "#javascript", "#linux", "#gaming", "#music", "#news"
        ]
        self.is_loading = False
    
    def compose(self) -> ComposeResult:
        """Compose the channel search dialog."""
        with Container(id="channel-search-dialog"):
            yield Static("Search Channels", classes="dialog-title")
            
            with Vertical():
                yield Input(
                    placeholder="Type channel name or search pattern...",
                    id="channel-search-input"
                )
                
                with Horizontal():
                    yield Button("Search All", id="search-all-btn", variant="primary")
                    yield Button("Cancel", id="cancel-btn")
                
                yield Static("Suggestions:", classes="section-header")
                yield ListView(id="suggestions-list")
                
                yield Static("Channels:", classes="section-header")
                yield ListView(id="channel-list")
                
                with Horizontal():
                    yield Button("Join Selected", id="join-btn", variant="success")
                    yield Button("Create New", id="create-btn", variant="warning")
    
    def on_mount(self):
        """Focus the input when mounted."""
        self.query_one("#channel-search-input", Input).focus()
        # Initialize the display
        self.refresh_channel_display()
        self.update_suggestions("")
    
    def on_input_changed(self, event: Input.Changed):
        """Filter channels and update suggestions as user types."""
        if event.input.id == "channel-search-input":
            search_term = event.value
            self.filter_channels(search_term)
            self.update_suggestions(search_term)
    
    def on_button_pressed(self, event: Button.Pressed):
        """Handle button presses."""
        if event.button.id == "cancel-btn":
            self.dismiss()
        elif event.button.id == "search-all-btn":
            self.search_channels()
        elif event.button.id == "join-btn":
            self.join_selected_channel()
        elif event.button.id == "create-btn":
            self.create_new_channel()
    
    def on_input_submitted(self, event: Input.Submitted):
        """Handle enter key in search input."""
        if event.input.id == "channel-search-input":
            # Prevent the event from bubbling up to the main app
            event.prevent_default()
            event.stop()
            
            channel_name = event.value.strip()
            if channel_name:
                if not channel_name.startswith('#'):
                    channel_name = '#' + channel_name
                self.post_message(self.ChannelSelected(channel_name))
                self.dismiss()
    
    def search_channels(self):
        """Request channel list from IRC server."""
        if self.is_loading:
            return
            
        self.is_loading = True
        
        # Show loading
        channel_list = self.query_one("#channel-list", ListView)
        channel_list.clear()
        channel_list.append(ListItem(Label("🔄 Loading channels from server...")))
        
        # Request from parent app - always use None (no pattern) to get all channels
        if hasattr(self.app, 'request_channel_list'):
            self.app.request_channel_list(None)  # Always request all channels
        else:
            # Fallback - show error
            channel_list.clear()
            channel_list.append(ListItem(Label("❌ Error: Cannot search channels")))
            self.is_loading = False
    
    def update_channel_list(self, channels: list):
        """Update the channel list with search results."""
        self.is_loading = False
        self.channels = channels
        
        # Apply current filter
        search_input = self.query_one("#channel-search-input", Input)
        self.filter_channels(search_input.value)
        self.update_suggestions(search_input.value)
    
    def filter_channels(self, search_term: str):
        """Filter channels based on search term with intelligent matching."""
        if not search_term:
            # Show top channels by user count when no search term
            self.filtered_channels = sorted(self.channels, key=lambda x: x.get('users', 0), reverse=True)[:20]
        else:
            search_lower = search_term.lower()
            scored_channels = []
            
            for ch in self.channels:
                score = self._calculate_match_score(ch, search_lower)
                if score > 0:
                    scored_channels.append((score, ch))
            
            # Sort by score (higher is better) and take top results
            scored_channels.sort(key=lambda x: x[0], reverse=True)
            self.filtered_channels = [ch for score, ch in scored_channels[:50]]
        
        self.refresh_channel_display()
    
    def _calculate_match_score(self, channel: dict, search_term: str) -> int:
        """Calculate relevance score for a channel based on search term."""
        name = channel['name'].lower()
        topic = channel['topic'].lower()
        score = 0
        
        # Exact name match gets highest score
        if name == search_term or name == f"#{search_term}":
            score += 100
        
        # Name starts with search term
        elif name.startswith(search_term) or name.startswith(f"#{search_term}"):
            score += 80
        
        # Search term appears in name
        elif search_term in name:
            score += 60
        
        # Search term appears in topic
        elif search_term in topic:
            score += 40
        
        # Fuzzy matching for typos (simple version)
        elif self._fuzzy_match(search_term, name):
            score += 30
        
        # Bonus for popular channels (more users)
        if score > 0:
            users = channel.get('users', 0)
            if users > 100:
                score += 20
            elif users > 50:
                score += 10
            elif users > 10:
                score += 5
        
        return score
    
    def _fuzzy_match(self, search_term: str, channel_name: str) -> bool:
        """Simple fuzzy matching for typos."""
        # Remove # from channel name for comparison
        clean_name = channel_name.lstrip('#')
        
        # Check if most characters match (allowing for 1-2 character differences)
        if len(search_term) < 3:
            return False
            
        matches = sum(1 for a, b in zip(search_term, clean_name) if a == b)
        return matches >= len(search_term) - 2
    
    def update_suggestions(self, search_term: str):
        """Update suggestions based on search term."""
        suggestions_list = self.query_one("#suggestions-list", ListView)
        suggestions_list.clear()
        
        suggestions = self._generate_suggestions(search_term)
        
        if not suggestions:
            suggestions_list.append(ListItem(Label("💡 Start typing to see suggestions")))
            return
        
        for suggestion in suggestions[:8]:  # Limit to 8 suggestions
            item = ListItem(Label(f"💡 {suggestion}"), classes="suggestion-item")
            item.suggestion_text = suggestion
            suggestions_list.append(item)
    
    def _generate_suggestions(self, search_term: str) -> List[str]:
        """Generate intelligent suggestions based on search term."""
        if not search_term:
            # Show popular channels when no search term
            return self.popular_channels[:5]
        
        suggestions = []
        search_lower = search_term.lower()
        
        # Add exact match suggestion if not already a channel name
        if not search_term.startswith('#'):
            suggestions.append(f"#{search_term}")
        
        # Add popular channels that match
        for channel in self.popular_channels:
            if search_lower in channel.lower() and channel not in suggestions:
                suggestions.append(channel)
        
        # Add recent channels that match
        for channel in self.recent_channels:
            if search_lower in channel.lower() and channel not in suggestions:
                suggestions.append(channel)
        
        # Add variations and common patterns
        if len(search_term) >= 2:
            variations = [
                f"#{search_term}-dev",
                f"#{search_term}-help", 
                f"#{search_term}-general",
                f"#{search_term}-chat",
                f"#{search_term}s",  # plural
            ]
            
            for variation in variations:
                if variation not in suggestions:
                    suggestions.append(variation)
        
        return suggestions
    
    def refresh_channel_display(self):
        """Refresh the channel list display."""
        channel_list = self.query_one("#channel-list", ListView)
        channel_list.clear()
        
        if not self.filtered_channels:
            if not self.channels:
                channel_list.append(ListItem(Label("🔍 Click 'Search All' to load channels from server")))
            else:
                channel_list.append(ListItem(Label("❌ No channels match your search")))
            return
        
        # Show count
        count_text = f"📋 Found {len(self.filtered_channels)} channels"
        if len(self.filtered_channels) == 50:
            count_text += " (showing top 50)"
        channel_list.append(ListItem(Label(count_text), classes="info-item"))
        
        for channel in self.filtered_channels:
            users_text = f"👥 {channel['users']}"
            topic_text = channel['topic'][:60] + "..." if len(channel['topic']) > 60 else channel['topic']
            
            label_text = f"{channel['name']} {users_text}"
            if topic_text:
                label_text += f" - {topic_text}"
            
            item = ListItem(Label(label_text), classes="channel-item")
            item.channel_data = channel
            channel_list.append(item)
    
    def on_list_view_selected(self, event: ListView.Selected):
        """Handle selection in any list view."""
        if event.list_view.id == "suggestions-list":
            # Handle suggestion selection
            if hasattr(event.item, 'suggestion_text'):
                suggestion = event.item.suggestion_text
                # Fill the input with the suggestion
                search_input = self.query_one("#channel-search-input", Input)
                search_input.value = suggestion
                search_input.focus()
        elif event.list_view.id == "channel-list":
            # Handle channel selection
            if hasattr(event.item, 'channel_data'):
                channel = event.item.channel_data['name']
                self._join_channel(channel)
    
    def join_selected_channel(self):
        """Join the selected channel from the channel list."""
        channel_list = self.query_one("#channel-list", ListView)
        if channel_list.highlighted_child and hasattr(channel_list.highlighted_child, 'channel_data'):
            channel = channel_list.highlighted_child.channel_data['name']
            self._join_channel(channel)
    
    def _join_channel(self, channel: str):
        """Join a channel and add it to recent channels."""
        self.recent_channels.add(channel)
        self.post_message(self.ChannelSelected(channel))
        self.dismiss()
    
    def create_new_channel(self):
        """Create a new channel with the entered name."""
        search_input = self.query_one("#channel-search-input", Input)
        channel_name = search_input.value.strip()
        
        if not channel_name:
            return
        
        if not channel_name.startswith('#'):
            channel_name = '#' + channel_name
        
        self._join_channel(channel_name)
    
    def add_recent_channel(self, channel: str):
        """Add a channel to recent channels list."""
        self.recent_channels.add(channel)
        # Keep only last 10 recent channels
        if len(self.recent_channels) > 10:
            self.recent_channels = set(list(self.recent_channels)[-10:])
    
    def set_popular_channels(self, channels: List[str]):
        """Update the list of popular channels."""
        self.popular_channels = channels