# Nickname Persistence - Quick Guide

## What's New? 🎉

**Your nickname is now remembered!** No need to type it every time you launch the app.

---

## How to Use

### First Time
```
1. Launch app
   ┌─────────────────────────────────────┐
   │ NICKNAME: cord_user_                │  ← Default
   └─────────────────────────────────────┘

2. Type your nickname
   ┌─────────────────────────────────────┐
   │ NICKNAME: alice_                    │  ← Your choice
   └─────────────────────────────────────┘

3. Press Enter
   → Nickname "alice" is saved ✓
   → You connect to IRC
```

### Next Time
```
1. Launch app
   ┌─────────────────────────────────────┐
   │ NICKNAME: alice_                    │  ← Remembered!
   └─────────────────────────────────────┘

2. Just press Enter
   → Connects with "alice" immediately
```

---

## Visual Flow

```
┌──────────────┐
│ Launch App   │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────┐
│ Check for saved nickname     │
└──────┬───────────────────────┘
       │
       ├─── Found? ──────────┐
       │                     │
       ▼                     ▼
   Use saved            Use default
   nickname            "cord_user"
       │                     │
       └──────┬──────────────┘
              │
              ▼
       ┌──────────────┐
       │ Show on      │
       │ Home Screen  │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │ User presses │
       │ Enter        │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │ Save nickname│
       │ to file      │
       └──────┬───────┘
              │
              ▼
       ┌──────────────┐
       │ Connect to   │
       │ IRC          │
       └──────────────┘
```

---

## Examples

### Scenario 1: Regular User
```
Day 1:
  Launch → Type "bob" → Connect
  [Saved: bob]

Day 2:
  Launch → See "bob" → Press Enter
  [Quick connect!]

Day 3:
  Launch → See "bob" → Press Enter
  [Quick connect!]
```

### Scenario 2: Changing Nickname
```
Launch → See "bob" → Type "alice" → Connect
[Saved: alice]

Next launch → See "alice"
[New default!]
```

### Scenario 3: Multiple Users
```
User A:
  Launch → Type "alice" → Connect
  [Saved: alice]

User B (same computer):
  Launch → See "alice" → Type "bob" → Connect
  [Saved: bob, replaces alice]
```

---

## Where Is It Saved?

```
your-project/
└── .cord/
    └── last_nick.json  ← Your nickname here
```

File contents:
```json
{
  "nick": "your_nickname"
}
```

---

## FAQ

### Q: Do I need to do anything special?
**A:** No! It works automatically.

### Q: Can I change my nickname?
**A:** Yes! Just type a new one and press Enter.

### Q: What if I want to reset?
**A:** Delete `.cord/last_nick.json` or just type a new nickname.

### Q: Is my nickname shared online?
**A:** No, it's only stored locally on your computer.

### Q: What if the file gets deleted?
**A:** The app will use "cord_user" as default.

### Q: Can I manually edit the file?
**A:** Yes! It's just a JSON file.

---

## Benefits

| Before | After |
|--------|-------|
| Type nickname every time | Type once, remembered forever |
| Slow to connect | Quick connect with Enter |
| Easy to mistype | Consistent nickname |
| Annoying repetition | Smooth experience |

---

## Technical Info

**Storage:** `.cord/last_nick.json`  
**Format:** JSON  
**Size:** ~30 bytes  
**Privacy:** Local only  
**Backup:** Not needed (just a nickname)  

---

## Summary

✅ **Automatic** - Saves when you connect  
✅ **Persistent** - Remembers between sessions  
✅ **Simple** - No configuration needed  
✅ **Fast** - Quick connect with saved nick  
✅ **Flexible** - Change anytime  

**Your nickname, remembered. Just the way it should be.** 🎉
