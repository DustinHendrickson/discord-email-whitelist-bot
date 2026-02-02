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
- SMTP2GO account for email sending (https://www.smtp2go.com)

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

## Step 3: Install Dependencies

Open Command Prompt or Terminal in the bot folder and run:

```python -m pip install discord.py requests```

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

## Step 9: Set Up SMTP2GO for Email Verification

SMTP2GO is used to send verification codes to users' emails. Follow these steps carefully:

### 9.1: Create an SMTP2GO Account
1. Go to https://www.smtp2go.com and click "Sign Up"
2. Choose your plan (free tier allows 1,000 emails/month, which is sufficient for most servers)
3. Verify your email address and complete the account setup

### 9.2: Verify Your Sender Email
1. In your SMTP2GO dashboard, go to **Settings** → **Sender Domains**
2. Add and verify your sender email address or domain
3. Follow the verification instructions (check your email for verification link)
4. This step ensures your emails are delivered successfully

### 9.3: Create an API Key
1. In SMTP2GO dashboard, go to **Settings** → **API Keys**
2. Click **Add API Key**
3. Name it something like "Discord Bot Verification"
4. Set permissions to allow sending emails
5. Click **Create**
6. **Copy the API key immediately** - save it securely for config.json

### 9.4: Test Your Setup
SMTP2GO provides testing tools in the dashboard to verify your setup is working.

**Important Notes:**
- The free tier sends up to 1,000 emails per month
- Keep your API key secure - never share it or commit it to version control
- If emails go to spam, ensure your sender domain is verified
- SMTP2GO provides detailed sending reports and analytics in the dashboard

---

## Step 10: Create JSON Configuration Files

config.json
```
{
  "token": "YOUR_BOT_TOKEN",
  "guild_id": 123456789012345678,
  "role_name": "Verified",
  "smtp2go_api_key": "YOUR_SMTP2GO_API_KEY",
  "from_email": "your_verified_email@example.com"
}
```

**Configuration Fields:**
- `token`: Your Discord bot token from Developer Portal
- `guild_id`: Your Discord server ID (right-click server name → Copy Server ID)
- `role_name`: The role to assign after verification (default: "Verified")
- `smtp2go_api_key`: Your SMTP2GO API key from Step 9.3
- `from_email`: The verified sender email from Step 9.2

whitelist.json
```
[
  "allowed1@example.com",
  "allowed2@example.com"
]
```
---

## Step 11: Bulk Update Whitelist from Mailchimp CSVs

1. Place exported Mailchimp CSV files into the `/imports/` folder.
2. Each CSV should contain a column with emails, default header: `Email Address`. (Can be changed in the python file but this is the default from Mailchimp)
3. Run the script `import_mailchimp.py`:
4. The script will merge all emails from CSVs into `whitelist.json` automatically.
5. After updating, users in the CSV can verify using the bot immediately.

---

## Step 12: Launch the Bot

1. Open Command Prompt or Terminal in the bot folder
2. Run:

```python bot.py```

3. If successful, terminal prints: Logged in as BotName
4. The bot is now online

---

## Commands

```!help - Explains how to use the !verify command.```

```!verify email - Requests a verification code to be sent to the email.```

```!verify email code - Verifies the code and grants access if valid.```

---

## User Verification Flow

1. User joins the server
2. User types `!verify their_email@example.com` in the bot's DMs
3. Bot checks if email is on whitelist; if not, denies access
4. If allowed, bot generates a 6-character code and emails it to the user
5. User types `!verify their_email@example.com CODE` within 30 minutes
6. Bot verifies the code and assigns the Verified role
7. Verified role unlocks configured channels

---

## Notes

- Whitelist updates are instant; edit whitelist.json to add/remove emails
- Bot must be above Verified role in hierarchy to assign it
- Users must be server members to be verified
- Verification codes expire after 30 minutes
- Each email can only have one pending verification at a time

---

## Troubleshooting SMTP2GO

### Emails Not Sending
- Check your API key is correct and has sending permissions
- Ensure the "from_email" is verified in SMTP2GO
- Verify your SMTP2GO account is active and not suspended
- Check the bot's console output for specific error messages

### Emails Going to Spam
- Verify your sender domain in SMTP2GO
- Use a reputable domain for your sender email
- Avoid spam trigger words in email content

### API Errors
- Verify your API key hasn't been revoked
- Check SMTP2GO dashboard for API status
- Ensure your API key has the correct permissions

### Rate Limiting
- Free tier: 1,000 emails per month
- Check SMTP2GO dashboard for usage statistics
- Upgrade your plan if you need higher limits

### Bot Not Responding
- Check bot is online in Discord
- Ensure bot has proper permissions in the server
- Verify config.json has correct values

---
