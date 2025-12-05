#!/usr/bin/env python3
"""Demo script to showcase the UI enhancements."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_teletext_rendering():
    """Demonstrate the teletext dashboard rendering."""
    print("\n" + "=" * 70)
    print("TELETEXT DASHBOARD - DYNAMIC SYSTEM METRICS")
    print("=" * 70)
    
    from src.ui.screens import TeletextScreen
    
    # Create screen instance
    screen = TeletextScreen()
    
    # Get current stats
    stats = screen._get_system_stats()
    
    print("\n📊 Real-Time System Performance (Aligned & Boxed):")
    print()
    print("╔═══════════════════════════════════════════════════════╗")
    print("║  SYSTEM PERFORMANCE                                   ║")
    print("╠═══════════════════════════════════════════════════════╣")
    
    # CPU
    cpu_bar = screen._render_bar(stats['cpu_percent'], 100, 25)
    cpu_color = screen._get_usage_color(stats['cpu_percent'])
    print(f"║  CPU    : {cpu_bar} {stats['cpu_percent']:5.1f}% [{cpu_color}]  ║")
    
    # Memory
    mem_bar = screen._render_bar(stats['memory_percent'], 100, 25)
    mem_color = screen._get_usage_color(stats['memory_percent'])
    print(f"║  Memory : {mem_bar} {stats['memory_percent']:5.1f}% [{mem_color}]  ║")
    print(f"║           {stats['memory_used_gb']:5.2f}GB / {stats['memory_total_gb']:5.2f}GB used              ║")
    
    # Disk
    disk_bar = screen._render_bar(stats['disk_usage_percent'], 100, 25)
    disk_color = screen._get_usage_color(stats['disk_usage_percent'])
    print(f"║  Disk   : {disk_bar} {stats['disk_usage_percent']:5.1f}% [{disk_color}]  ║")
    
    # Network
    print("╠═══════════════════════════════════════════════════════╣")
    print(f"║  Network: ↑ TX {stats['network_sent_mb']:8.1f} MB              ║")
    print(f"║           ↓ RX {stats['network_recv_mb']:8.1f} MB              ║")
    print("╚═══════════════════════════════════════════════════════╝")
    
    # Show color legend
    print("\n🎨 Color Coding:")
    print("  Green  (< 50%)  : Healthy")
    print("  Yellow (50-75%) : Moderate")
    print("  Red    (> 75%)  : High")
    
    print("\n✨ Features:")
    print("  • All bars aligned at same X coordinate")
    print("  • Fixed-width labels for perfect alignment")
    print("  • Boxed layout with Unicode borders")
    print("  • Smooth gradient bars with partial blocks")

def demo_bar_examples():
    """Show examples of progress bars at different levels."""
    print("\n" + "=" * 70)
    print("PROGRESS BAR EXAMPLES - SMOOTH GRADIENT")
    print("=" * 70)
    
    from src.ui.screens import TeletextScreen
    screen = TeletextScreen()
    
    levels = [10, 25, 33.3, 50, 66.7, 75, 90, 100]
    
    print("\n📊 Usage Levels with Smooth Gradients:")
    for level in levels:
        bar = screen._render_bar(level, 100, 30)
        color = screen._get_usage_color(level)
        print(f"{level:5.1f}%: {bar} [{color}]")
    
    print("\n✨ Notice the smooth gradient effect with partial blocks!")

def demo_css_changes():
    """Show the CSS changes for centered dialog."""
    print("\n" + "=" * 70)
    print("CSS CHANGES - CENTERED SEARCH DIALOG")
    print("=" * 70)
    
    print("\n📝 Before:")
    print("""
#channel-search-dialog {
    width: 70;
    height: 35;
    background: #36393f;
    border: solid #5865F2;
    padding: 2;
    margin: 2;  ← Dialog offset from edges
}
    """)
    
    print("📝 After:")
    print("""
ChannelSearchScreen {
    align: center middle;  ← Screen-level centering
}

#channel-search-dialog {
    width: 70;
    height: 35;
    background: #36393f;
    border: solid #5865F2;
    padding: 2;  ← No margin, perfect center
}
    """)
    
    print("✨ Result: Dialog is now perfectly centered on screen!")

def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print("🎨 phosphor UI ENHANCEMENTS DEMO")
    print("=" * 70)
    
    try:
        demo_teletext_rendering()
        demo_bar_examples()
        demo_css_changes()
        
        print("\n" + "=" * 70)
        print("✓ Demo Complete!")
        print("=" * 70)
        print("\n💡 To see these changes in action:")
        print("   1. Run: python3 kiro_irc_bridge.py")
        print("   2. Press F1 to view dynamic teletext dashboard")
        print("   3. Press Ctrl+J to see centered search dialog")
        print("=" * 70 + "\n")
        
        return 0
    except Exception as e:
        print(f"\n✗ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
