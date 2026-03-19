# 🎯 Discord Voting Bot

A fully autonomous Discord voting bot with **real-time vote tracking and live-updating leaderboards**!

## 📁 Folder Structure

```
voting_bot/
├── voting_bot.py          # Main bot file
├── requirements.txt       # Dependencies
├── .env                   # Bot token (create this)
├── README.md             # This file
├── SETUP_GUIDE.md        # Detailed setup instructions
└── bot_config.json       # Auto-generated (server settings)
└── voting_data.json      # Auto-generated (vote records)
└── leaderboard_messages.json # Auto-generated (leaderboard tracking)
```

## 🚀 Quick Start (3 Steps)

### Step 1️⃣: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2️⃣: Add Your Bot Token
1. Open `.env` file
2. Replace `your_bot_token_here` with your actual Discord bot token
3. Save the file

### Step 3️⃣: Run the Bot
```bash
python voting_bot.py
```

You should see:
```
✅ [YourBotName] has connected to Discord!
✅ Synced X command(s)
```

---

## 🎮 Commands

### 👨‍💼 Admin Commands
| Command | Purpose |
|---------|---------|
| `/setup` | **FIRST**: Configure bot (channel, difficulty, cooldown) |
| `/leaderboard` | Post live-updating leaderboard |
| `/vote_stats` | View voting statistics |
| `/view_settings` | See current configuration |
| `/reset_guild_data` | Clear all voting data |

### 👥 User Commands
| Command | Purpose |
|---------|---------|
| `/vote` | Vote by answering a math question |
| `/recent_votes` | View recent voters with timestamps |

---

## ⚙️ Initial Setup (For Server Admins)

### First Time Setup:
1. **Invite bot to your server** (if not done already)
2. **Run `/setup`** in your Discord server
3. **Follow the wizard**:
   - Select voting channel
   - Choose difficulty (Easy/Medium/Hard)
   - Set cooldown (6h/12h/24h/48h)
4. **Done!** Members can now use `/vote`

### Post Leaderboard:
1. Run `/leaderboard` in desired channel
2. Leaderboard auto-updates every 30 seconds
3. Shows top 15 recent voters

---

## 🎓 Difficulty Levels

| Level | Numbers | Operations | Best For |
|-------|---------|------------|----------|
| **Easy** | 1-20 | +, -, * | Most servers |
| **Medium** | 10-50 | +, -, * | Moderate challenge |
| **Hard** | 50-100 | +, -, * | Advanced servers |

---

## 📊 Real-Time Updates

### How Timestamps Work:
- **30 seconds ago** → Shows as "30s ago"
- **5 minutes ago** → Shows as "5m ago"  
- **2 hours ago** → Shows as "2h ago"
- **3 days ago** → Shows as "3d ago"

### Live Leaderboard Updates:
✅ Updates every 30 seconds automatically
✅ Shows newest voters at top
✅ Displays "voted X time ago" for each voter

---

## 💾 Data Files (Auto-Generated)

| File | Purpose |
|------|---------|
| `bot_config.json` | Server settings (per-guild) |
| `voting_data.json` | Vote records with timestamps |
| `leaderboard_messages.json` | Leaderboard message IDs |

**Each server has completely separate data!**

---

## ❓ FAQ

**Q: Where do I get a bot token?**
A: [Discord Developer Portal](https://discord.com/developers/applications)

**Q: Can I use this on multiple servers?**
A: YES! Each server gets its own independent configuration.

**Q: How often does the leaderboard update?**
A: Every 30 seconds automatically.

**Q: Do timestamps update live?**
A: YES! "30s ago" becomes "1m ago" automatically.

**Q: What if leaderboard message gets deleted?**
A: Just run `/leaderboard` again to create a new one.

**Q: How do I change settings after setup?**
A: Run `/setup` again to reconfigure.

**Q: Can I have multiple leaderboards?**
A: YES! Run `/leaderboard` in different channels.

---

## 🐛 Troubleshooting

### Bot doesn't respond to commands
- ✅ Check bot is online (check console for "connected to Discord")
- ✅ Make sure you waited 5 seconds after starting bot
- ✅ Bot must have "Send Messages" permission

### Can't run /setup
- ✅ You must be a server **Administrator**
- ✅ Wait for bot to sync commands (check console)

### Leaderboard not updating
- ✅ Check bot can edit messages
- ✅ Make sure bot is in the channel
- ✅ Restart bot if it's been running for hours

### Bot keeps crashing
- ✅ Check `.env` file has correct token
- ✅ Make sure token doesn't have extra spaces
- ✅ Check console for error messages

---

## 🔧 Customization (Optional)

### Change Leaderboard Update Speed
Edit `voting_bot.py`, find:
```python
@tasks.loop(seconds=30)  # Change 30 to 15 for faster updates
async def update_leaderboards(self):
```

### Change Leaderboard Size
Find in `voting_bot.py`:
```python
)[:15]  # Shows top 15 voters, change to 20, 10, etc
```

### Add More Math Operations
In `voting_bot.py`, find where it defines operations and add:
```python
"operations": ["+", "-", "*", "//"]  # Add division
```

---

## 📞 Support

Check the console output for error messages if something doesn't work.

Common errors:
- `Token is invalid` → Fix bot token in `.env`
- `Command sync failed` → Restart the bot
- `Channel not found` → Make sure voting channel exists

---

## ✨ Features Summary

✅ **Self-Setup Wizard** - No coding needed
✅ **Per-Server Configuration** - Each server independent
✅ **Real-Time Timestamps** - "2h ago" updates automatically
✅ **Live Leaderboards** - Updates every 30 seconds
✅ **Easy/Medium/Hard** - Adjustable difficulty
✅ **Flexible Cooldowns** - 6h to 48h options
✅ **Vote Tracking** - Complete voting history
✅ **Beautiful Embeds** - Professional Discord UI

---

**Made with ❤️ for Discord servers**