# 📋 Complete Setup Guide

## Before You Start

- ✅ You need a Discord server you own/manage
- ✅ You need to create a Discord bot application
- ✅ Python 3.8+ must be installed

---

## Step 1: Create Discord Bot

### 1.1 Go to Developer Portal
- Visit: https://discord.com/developers/applications
- Click "New Application"
- Give it a name (e.g., "Voting Bot")
- Click "Create"

### 1.2 Create the Bot
- Click "Bot" in left sidebar
- Click "Add Bot"
- Under "TOKEN", click "Copy" to copy your bot token
- **⚠️ KEEP THIS SECRET! Don't share it!**

### 1.3 Enable Intents
- Scroll down to "GATEWAY INTENTS"
- Enable these:
  - ✅ Server Members Intent
  - ✅ Message Content Intent

---

## Step 2: Invite Bot to Server

### 2.1 Generate Invite Link
- Click "OAuth2" in left sidebar
- Click "URL Generator"
- Select "bot" under Scopes
- Select these Permissions:
  - ✅ Send Messages
  - ✅ Embed Links
  - ✅ Read Messages/View Channels

### 2.2 Copy & Use Link
- Copy the generated URL
- Open it in your browser
- Select your server
- Click "Authorize"

---

## Step 3: Install Bot Files

### 3.1 Download Files
- Download the `voting_bot` folder
- Extract it somewhere on your computer
- You should have: