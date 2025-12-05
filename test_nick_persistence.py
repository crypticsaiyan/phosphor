#!/usr/bin/env python3
"""Test script to verify nickname persistence."""

import sys
import os
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_save_and_load():
    """Test saving and loading nickname."""
    print("=" * 60)
    print("Testing Nickname Persistence")
    print("=" * 60)
    
    from src.ui.screens import _save_last_nick, _load_last_nick
    
    # Test 1: Save a nickname
    print("\n1. Saving nickname 'test_user'...")
    _save_last_nick("test_user")
    
    # Check if file was created
    settings_path = Path(".cord/last_nick.json")
    if settings_path.exists():
        print("   ✓ Settings file created at:", settings_path)
        with open(settings_path) as f:
            data = json.load(f)
            print(f"   ✓ File contents: {data}")
    else:
        print("   ✗ Settings file not created!")
        return False
    
    # Test 2: Load the nickname
    print("\n2. Loading saved nickname...")
    loaded_nick = _load_last_nick()
    if loaded_nick == "test_user":
        print(f"   ✓ Successfully loaded: '{loaded_nick}'")
    else:
        print(f"   ✗ Expected 'test_user', got '{loaded_nick}'")
        return False
    
    # Test 3: Save a different nickname
    print("\n3. Saving new nickname 'another_user'...")
    _save_last_nick("another_user")
    loaded_nick = _load_last_nick()
    if loaded_nick == "another_user":
        print(f"   ✓ Successfully updated to: '{loaded_nick}'")
    else:
        print(f"   ✗ Expected 'another_user', got '{loaded_nick}'")
        return False
    
    # Test 4: Test with special characters
    print("\n4. Testing with special characters...")
    test_nicks = ["user_123", "test-user", "User[IRC]", "test^user"]
    for nick in test_nicks:
        _save_last_nick(nick)
        loaded = _load_last_nick()
        if loaded == nick:
            print(f"   ✓ '{nick}' saved and loaded correctly")
        else:
            print(f"   ✗ '{nick}' failed: got '{loaded}'")
            return False
    
    # Test 5: Test default fallback
    print("\n5. Testing default fallback...")
    # Remove the file
    if settings_path.exists():
        settings_path.unlink()
        print("   ✓ Removed settings file")
    
    loaded_nick = _load_last_nick()
    if loaded_nick == "cord_user":
        print(f"   ✓ Default fallback works: '{loaded_nick}'")
    else:
        print(f"   ✗ Expected 'cord_user', got '{loaded_nick}'")
        return False
    
    return True

def test_homescreen_integration():
    """Test that HomeScreen uses the saved nickname."""
    print("\n" + "=" * 60)
    print("Testing HomeScreen Integration")
    print("=" * 60)
    
    from src.ui.screens import _save_last_nick, HomeScreen
    
    # Save a test nickname
    print("\n1. Saving nickname 'saved_nick'...")
    _save_last_nick("saved_nick")
    
    # Create HomeScreen instance
    print("2. Creating HomeScreen instance...")
    screen = HomeScreen()
    
    # Check if it loaded the saved nickname
    if screen.default_nick == "saved_nick":
        print(f"   ✓ HomeScreen loaded saved nickname: '{screen.default_nick}'")
    else:
        print(f"   ✗ Expected 'saved_nick', got '{screen.default_nick}'")
        return False
    
    if screen.current_nick == "saved_nick":
        print(f"   ✓ Current nick set to: '{screen.current_nick}'")
    else:
        print(f"   ✗ Expected 'saved_nick', got '{screen.current_nick}'")
        return False
    
    return True

def cleanup():
    """Clean up test files."""
    print("\n" + "=" * 60)
    print("Cleaning up test files...")
    print("=" * 60)
    
    settings_path = Path(".cord/last_nick.json")
    if settings_path.exists():
        settings_path.unlink()
        print("✓ Removed test settings file")
    
    # Try to remove .cord directory if empty
    try:
        settings_path.parent.rmdir()
        print("✓ Removed .cord directory")
    except OSError:
        print("ℹ .cord directory not empty (this is fine)")

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("🧪 NICKNAME PERSISTENCE TEST SUITE")
    print("=" * 60)
    
    try:
        # Run tests
        test1_passed = test_save_and_load()
        test2_passed = test_homescreen_integration()
        
        # Summary
        print("\n" + "=" * 60)
        print("Test Results:")
        print("=" * 60)
        print(f"{'✓ PASS' if test1_passed else '✗ FAIL'}: Save and Load Functions")
        print(f"{'✓ PASS' if test2_passed else '✗ FAIL'}: HomeScreen Integration")
        
        all_passed = test1_passed and test2_passed
        
        print("=" * 60)
        if all_passed:
            print("✓ All tests passed!")
            print("\n💡 How it works:")
            print("   1. User enters nickname on home screen")
            print("   2. Nickname is saved to .cord/last_nick.json")
            print("   3. Next time app starts, saved nick is loaded")
            print("   4. User sees their last used nickname as default")
        else:
            print("✗ Some tests failed")
        print("=" * 60)
        
        return 0 if all_passed else 1
        
    finally:
        # Always cleanup
        cleanup()

if __name__ == "__main__":
    sys.exit(main())
