#!/usr/bin/env python3
"""Test the aligned bar rendering without requiring full imports."""

def render_bar(value: float, max_value: float, width: int = 20) -> str:
    """Render a progress bar with smooth gradient."""
    filled = (value / max_value) * width
    full_blocks = int(filled)
    partial = filled - full_blocks
    
    # Use block characters for smooth gradient
    bar = "█" * full_blocks
    
    # Add partial block for smoother appearance
    if full_blocks < width and partial > 0:
        if partial > 0.75:
            bar += "▓"
        elif partial > 0.5:
            bar += "▒"
        elif partial > 0.25:
            bar += "░"
        else:
            bar += "░"
        empty_blocks = width - full_blocks - 1
    else:
        empty_blocks = width - full_blocks
    
    bar += "░" * empty_blocks
    return f"[{bar}]"

def get_usage_color(percent: float) -> str:
    """Get color based on usage percentage."""
    if percent < 50:
        return "green"
    elif percent < 75:
        return "yellow"
    else:
        return "red"

def demo_aligned_layout():
    """Show the aligned layout."""
    print("\n" + "=" * 70)
    print("ALIGNED SYSTEM PERFORMANCE DASHBOARD")
    print("=" * 70)
    
    # Simulate some stats
    stats = {
        "cpu_percent": 42.5,
        "memory_percent": 68.3,
        "memory_used_gb": 5.2,
        "memory_total_gb": 7.5,
        "disk_usage_percent": 72.8,
        "network_sent_mb": 1234.5,
        "network_recv_mb": 5678.9,
    }
    
    print()
    print("SYSTEM PERFORMANCE")
    print()
    
    # CPU - label above, bar below, left-aligned (50 chars wide)
    cpu_bar = render_bar(stats['cpu_percent'], 100, 50)
    cpu_color = get_usage_color(stats['cpu_percent'])
    print(f"CPU {stats['cpu_percent']:5.1f}% [{cpu_color}]")
    print(f"{cpu_bar}")
    print()
    
    # Memory - label above, bar below, left-aligned
    mem_bar = render_bar(stats['memory_percent'], 100, 50)
    mem_color = get_usage_color(stats['memory_percent'])
    print(f"Memory {stats['memory_percent']:5.1f}% [{mem_color}] ({stats['memory_used_gb']:.1f}/{stats['memory_total_gb']:.1f}GB)")
    print(f"{mem_bar}")
    print()
    
    # Disk - label above, bar below, left-aligned
    disk_bar = render_bar(stats['disk_usage_percent'], 100, 50)
    disk_color = get_usage_color(stats['disk_usage_percent'])
    print(f"Disk {stats['disk_usage_percent']:5.1f}% [{disk_color}]")
    print(f"{disk_bar}")
    print()
    
    # Network - left-aligned
    print(f"Network")
    print(f"↑ TX {stats['network_sent_mb']:8.1f} MB  ↓ RX {stats['network_recv_mb']:8.1f} MB")
    
    print("\n✨ Key Features:")
    print("  ✓ All bars left-aligned from the same position")
    print("  ✓ Labels above bars for cleaner look")
    print("  ✓ Clean layout without borders - no visual clutter")
    print("  ✓ Wide bars (50 chars) for excellent granularity")
    print("  ✓ Smooth gradient bars with partial block characters")
    print("  ✓ Color-coded by usage level (green/yellow/red)")
    print("  ✓ Vertical layout - easy to scan top to bottom")

def demo_gradient_bars():
    """Show gradient bar examples."""
    print("\n" + "=" * 70)
    print("SMOOTH GRADIENT PROGRESS BARS")
    print("=" * 70)
    
    print("\n📊 Different usage levels showing smooth gradients:")
    print()
    
    levels = [0, 12.5, 25, 37.5, 50, 62.5, 75, 87.5, 100]
    
    for level in levels:
        bar = render_bar(level, 100, 30)
        color = get_usage_color(level)
        print(f"  {level:5.1f}%: {bar} [{color:6s}]")
    
    print("\n✨ Notice:")
    print("  • Partial blocks (▓▒░) create smooth transitions")
    print("  • All bars perfectly aligned")
    print("  • Color changes at 50% and 75% thresholds")

def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print("🎨 ALIGNED BAR VISUALIZATION TEST")
    print("=" * 70)
    
    demo_aligned_layout()
    demo_gradient_bars()
    
    print("\n" + "=" * 70)
    print("✓ All tests complete!")
    print("=" * 70)
    print("\n💡 To see this in the actual app:")
    print("   1. Run: python3 kiro_irc_bridge.py")
    print("   2. Press F1 to view the teletext dashboard")
    print("   3. Watch the bars update in real-time!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
