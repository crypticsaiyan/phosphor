#!/usr/bin/env python3
"""Simple test for nickname persistence without requiring textual."""

import json
from pathlib import Path

def save_last_nick(nick: str):
    """Save the nickname for future use."""
    settings_path = Path(".cord/last_nick.json")
    settings_path.parent.mkdir(exist_ok=True)
    try:
        with open(settings_path, 'w') as f:
            json.dump({"nick": nick}, f)
        return True
    except Exception as e:
        print(f"Error saving: {e}")
        return False

def load_last_nick() -> str:
    """Load the last used nickname from settings."""
    settings_path = Path(".cord/last_nick.json")
    if settings_path.exists():
        try:
            with open(settings_path) as f:
                data = json.load(f)
                return data.get("nick", "cord_user")
        except Exception as e:
            print(f"Error loading: {e}")
    return "cord_user"

def main():
    print("=" * 60)
    print("🧪 NICKNAME PERSISTENCE TEST")
    print("=" * 60)
    
    # Test 1: Save and load
    print("\n1. Testing save and load...")
    test_nick = "my_awesome_nick"
    if save_last_nick(test_nick):
        print(f"   ✓ Saved: '{test_nick}'")
    else:
        print("   ✗ Failed to save")
        return 1
    
    loaded = load_last_nick()
    if loaded == test_nick:
        print(f"   ✓ Loaded: '{loaded}'")
    else:
        print(f"   ✗ Expected '{test_nick}', got '{loaded}'")
        return 1
    
    # Test 2: Update nickname
    print("\n2. Testing update...")
    new_nick = "updated_nick"
    save_last_nick(new_nick)
    loaded = load_last_nick()
    if loaded == new_nick:
        print(f"   ✓ Updated to: '{loaded}'")
    else:
        print(f"   ✗ Expected '{new_nick}', got '{loaded}'")
        return 1
    
    # Test 3: Special characters
    print("\n3. Testing special characters...")
    special_nicks = ["user_123", "test-user", "User[IRC]", "test^user"]
    for nick in special_nicks:
        save_last_nick(nick)
        loaded = load_last_nick()
        if loaded == nick:
            print(f"   ✓ '{nick}'")
        else:
            print(f"   ✗ '{nick}' failed")
            return 1
    
    # Test 4: File location
    print("\n4. Checking file location...")
    settings_path = Path(".cord/last_nick.json")
    if settings_path.exists():
        print(f"   ✓ File exists at: {settings_path.absolute()}")
        with open(settings_path) as f:
            data = json.load(f)
            print(f"   ✓ Contents: {data}")
    else:
        print("   ✗ File not found")
        return 1
    
    # Test 5: Default fallback
    print("\n5. Testing default fallback...")
    settings_path.unlink()
    loaded = load_last_nick()
    if loaded == "cord_user":
        print(f"   ✓ Default fallback: '{loaded}'")
    else:
        print(f"   ✗ Expected 'cord_user', got '{loaded}'")
        return 1
    
    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)
    
    print("\n💡 How it works:")
    print("   1. User enters nickname on home screen")
    print("   2. When user presses Enter to connect:")
    print("      → Nickname is saved to .cord/last_nick.json")
    print("   3. Next time app starts:")
    print("      → Saved nickname is loaded automatically")
    print("      → User sees their last used nickname as default")
    print("\n📁 Storage location: .cord/last_nick.json")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
