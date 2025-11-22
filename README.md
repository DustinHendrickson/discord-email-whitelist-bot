# WhitelistBot

A Discord bot for verifying users via email and giving them a Verified role.  

---

## What This Bot Does

- Lets users verify themselves with an email.
- Assigns the Verified role if their email is on the whitelist.
- Dynamic whitelist: updates immediately without restarting the bot.
- Imports mailchip email lists into the whitelist.json

---

## Requirements

- Windows, macOS, or Linux
- Python 3.10 or newer (https://www.python.org/downloads/)
- A Discord server where you can manage roles and add bots.

---

## Step 0: Prepare Your Folder

Create a folder anywhere you want and place these files inside:

- bot.py (the bot code)
- import_mailchimp.py (importer code)
- config.json (bot configuration)
- whitelist.json (emails for verification)
- /imports/ (folder for imported csv files)
- README.md (this file)

---

## Step 1: Download the Bot

Option 1: Using Git

1. Install Git: https://git-scm.com/downloads
2. Open Command Prompt (Windows) or Terminal (macOS/Linux)
3. Navigate to the folder where you want the bot using `cd`
4. Run `git clone https://github.com/DustinHendrickson/WhitelistBot.git`
5. Navigate into the folder using `cd WhitelistBot`

Option 2: Download ZIP

1. Click Code → Download ZIP in the GitHub repository.
2. Extract the ZIP to a folder, e.g., C:\Users\YourName\Documents\WhitelistBot

---

## Step 2: Install Python

1. Download Python 3.10+ from https://www.python.org/downloads/
2. During installation, check “Add Python to PATH” (Windows only)
3. Open Command Prompt or Terminal and run `python --version` to verify installation.

---

## Step 3: Install Discord.py

Open Command Prompt or Terminal in the bot folder and run:

```python -m pip install discord.py```

---

## Step 4: Create Your Discord Bot

1. Go to https://discord.com/developers/applications
2. Click New Application, name it, and create it
3. On the left, select Bot → Click Add Bot
4. Copy the Bot Token and save it for config.json

---

## Step 5: Enable Required Bot Intents

1. On the Bot page, enable:
   - Server Members Intent
   - Message Content Intent
   - Presence Intent
2. Click Save Changes

---

## Step 6: Invite the Bot to Your Server

1. In Developer Portal → OAuth2 → URL Generator
2. Scopes: bot
3. Bot Permissions: Manage Roles, Read Message History, Send Messages
4. Copy the generated URL, open in browser, and authorize the bot

---

## Step 7: Create the Verified Role

1. Server Settings → Roles → Create a role named Verified
2. Drag it below the bot’s role in the hierarchy
3. Grant Verified role access to channels you want unlocked

---

## Step 8: Copy Your Server ID

1. Right-click your server name in Discord → Copy Server ID
2. Use this number in config.json as guild_id

---

## Step 9: Create JSON Configuration Files

config.json
```
{
  "token": "YOUR_BOT_TOKEN",
  "guild_id": 123456789012345678,
  "role_name": "Verified"
}
```
whitelist.json
```
[
  "allowed1@example.com",
  "allowed2@example.com"
]
```
---

## Step 10: Bulk Update Whitelist from Mailchimp CSVs

1. Place exported Mailchimp CSV files into the `/imports/` folder.
2. Each CSV should contain a column with emails, default header: `Email Address`. (Can be changed in the python file but this is the default from Mailchimp)
3. Run the script `update_whitelist.py`:
4. The script will merge all emails from CSVs into `whitelist.json` automatically.
5. After updating, users in the CSV can verify using the bot immediately.

---

## Step 11: Launch the Bot

1. Open Command Prompt or Terminal in the bot folder
2. Run:

```python bot.py```

3. If successful, terminal prints: Logged in as BotName
4. The bot is now online

---

## Commands

```!help - Explains how to use the !verify command.```

```!verify - Users type this in the server to start verification. Bot DMs them for email.```

---

## User Verification Flow

1. User joins the server
2. User DM's the bot !verify their_email@gmail.com
3. Bot checks email against whitelist.json
4. If allowed, Verified role is applied
5. Verified role unlocks configured channels

---

## Notes

- Whitelist updates are instant; edit whitelist.json to add/remove emails
- Bot must be above Verified role in hierarchy to assign it
- Users must be server members to be verified
