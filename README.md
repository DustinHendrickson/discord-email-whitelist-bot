# WhitelistBot

A Discord bot for verifying users via email and granting them a role in your server.  
The bot uses JSON files for configuration and dynamically loads the whitelist each time a user verifies.

---

## 1. Create the bot in Discord Developer Portal

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)  
2. Click **New Application**  
3. Name it and create it  
4. On the left, select **Bot**  
5. Click **Add Bot**  
6. Copy the **Bot Token** — you will put it in `config.json`.

---

## 2. Enable required bot intents

On the Bot page, enable:  
- **Server Members Intent**  
- **Message Content Intent**  
- **Presence Intent**  

Click **Save Changes**.

---

## 3. Invite the bot to your server

1. In the Developer Portal, select **OAuth2 → URL Generator**  
2. Under **Scopes**, select: `bot`  
3. Under **Bot Permissions**, select:  
   - Manage Roles  
   - Read Message History  
   - Send Messages  
4. Copy the generated URL, open it in a browser, and authorize the bot into your server.

---

## 4. Create the Verified role in Discord

1. Open **Server Settings → Roles**  
2. Create a role named `Verified`  
3. Drag it **below the bot’s role** in the role order (bot cannot assign roles above it)  
4. Grant the `Verified` role access to all channels you want unlocked after verification.

---

## 5. Copy your server ID

1. Right-click your server name in Discord  
2. Click **Copy Server ID**  
3. Use this number in `config.json` as `guild_id`.

---

## 6. Install discord.py

```bash
python -m pip install discord.py
