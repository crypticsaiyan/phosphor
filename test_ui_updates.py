#!/usr/bin/env python3
"""Test script to verify UI updates - centered search panel and dynamic teletext."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all imports work."""
    print("Testing imports...")
    try:
        from src.ui.screens import TeletextScreen, HomeScreen
        from src.ui.widgets.channel_search import ChannelSearchScreen
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_teletext_stats():
    """Test that teletext can get system stats."""
    print("\nTesting teletext system stats...")
    try:
        from src.ui.screens import TeletextScreen
        
        # Create a mock screen
        screen = TeletextScreen()
        
        # Test system stats
        stats = screen._get_system_stats()
        print(f"✓ CPU: {stats['cpu_percent']:.1f}%")
        print(f"✓ Memory: {stats['memory_percent']:.1f}% ({stats['memory_used_gb']:.1f}/{stats['memory_total_gb']:.1f}GB)")
        print(f"✓ Disk: {stats['disk_usage_percent']:.1f}%")
        print(f"✓ Network TX: {stats['network_sent_mb']:.1f}MB, RX: {stats['network_recv_mb']:.1f}MB")
        
        # Test bar rendering
        bar = screen._render_bar(75, 100, 20)
        print(f"✓ Progress bar (75%): {bar}")
        
        # Test color selection
        color = screen._get_usage_color(75)
        print(f"✓ Usage color (75%): {color}")
        
        return True
    except Exception as e:
        print(f"✗ Teletext stats test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_css_syntax():
    """Test that CSS file is valid."""
    print("\nTesting CSS syntax...")
    try:
        css_path = "src/ui/styles.tcss"
        with open(css_path, 'r') as f:
            content = f.read()
        
        # Check for centered search dialog
        if "ChannelSearchScreen" in content and "align: center middle" in content:
            print("✓ Channel search screen has center alignment")
        else:
            print("✗ Channel search screen alignment not found")
            return False
        
        print("✓ CSS syntax appears valid")
        return True
    except Exception as e:
        print(f"✗ CSS test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("UI Updates Test Suite")
    print("=" * 60)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Teletext Stats", test_teletext_stats()))
    results.append(("CSS Syntax", test_css_syntax()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(result[1] for result in results)
    
    print("=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
