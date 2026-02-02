import discord
from discord.ext import commands
import json
import os
import random
import string
from datetime import datetime, timedelta
import requests

# Load config from JSON
with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["token"]
GUILD_ID = config["guild_id"]
ROLE_NAME = config["role_name"]
SMTP2GO_API_KEY = config["smtp2go_api_key"]
FROM_EMAIL = config["from_email"]

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

# Disable default help so custom !help works
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

def load_whitelist():
    """Load the latest whitelist from JSON"""
    with open("whitelist.json", "r") as f:
        return [email.lower().strip() for email in json.load(f)]

def generate_verification_code():
    """Generate a random 6-character verification code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def load_pending_verifications():
    """Load pending verifications from JSON"""
    if os.path.exists("pending.json"):
        with open("pending.json", "r") as f:
            data = json.load(f)
            # Convert timestamp strings back to datetime
            for email, info in data.items():
                info['timestamp'] = datetime.fromisoformat(info['timestamp'])
            # Clean expired
            now = datetime.now()
            data = {email: info for email, info in data.items() if now - info['timestamp'] <= timedelta(minutes=30)}
            # Save cleaned data
            save_pending_verifications(data)
            return data
    return {}

def save_pending_verifications(pending):
    """Save pending verifications to JSON"""
    data = {}
    for email, info in pending.items():
        data[email] = {
            'code': info['code'],
            'timestamp': info['timestamp'].isoformat(),
            'user_id': info['user_id']
        }
    with open("pending.json", "w") as f:
        json.dump(data, f)

def send_verification_email(email, code):
    """Send verification email using SMTP2GO API"""
    try:
        # SMTP2GO API endpoint
        url = "https://api.smtp2go.com/v3/email/send"
        
        # Prepare email data
        payload = {
            "api_key": SMTP2GO_API_KEY,
            "to": [email],
            "sender": FROM_EMAIL,
            "subject": "Your Verification Code",
            "html_body": f"<p>Your verification code is: <strong>{code}</strong></p><p>This code expires in 30 minutes.</p>"
        }
        
        # Send request
        response = requests.post(url, json=payload)
        
        # Check response
        if response.status_code == 200:
            result = response.json()
            return result.get('data', {}).get('succeeded', 0) > 0
        else:
            print(f"SMTP2GO API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Verify command
@bot.command()
async def verify(ctx, email: str, code: str = None):
    email = email.strip().lower()
    whitelist = load_whitelist()

    if email not in whitelist:
        await ctx.send("Email not on whitelist. Access denied.")
        return

    if code is None:
        # Generate and send code
        pending = load_pending_verifications()
        verification_code = generate_verification_code()
        pending[email] = {
            'code': verification_code,
            'timestamp': datetime.now(),
            'user_id': ctx.author.id
        }
        save_pending_verifications(pending)

        if send_verification_email(email, verification_code):
            await ctx.send("Verification code sent to your email. Please check your inbox and reply with `!verify your_email@example.com CODE` within 30 minutes.")
        else:
            await ctx.send("Failed to send verification email. Please try again later.")
    else:
        # Verify code
        pending = load_pending_verifications()
        if email not in pending:
            await ctx.send("No pending verification for this email.")
            return

        info = pending[email]
        if info['user_id'] != ctx.author.id:
            await ctx.send("This verification code is not for you.")
            return

        if info['code'] != code.upper():
            await ctx.send("Invalid verification code.")
            return

        if datetime.now() - info['timestamp'] > timedelta(minutes=30):
            await ctx.send("Verification code has expired. Please request a new one.")
            del pending[email]
            save_pending_verifications(pending)
            return

        # Code is valid, assign role
        guild = bot.get_guild(GUILD_ID)
        if guild is None:
            await ctx.send("Bot is not in the server.")
            return

        member = guild.get_member(ctx.author.id)
        if member is None:
            try:
                member = await guild.fetch_member(ctx.author.id)
            except:
                await ctx.send("Could not find you in the server.")
                return

        role = discord.utils.get(guild.roles, name=ROLE_NAME)
        if role is None:
            await ctx.send(f"Role '{ROLE_NAME}' does not exist in this server.")
            return

        if role not in member.roles:
            await member.add_roles(role)
        await ctx.send(f"Access granted. Role '{ROLE_NAME}' applied.")

        # Clean up
        del pending[email]
        save_pending_verifications(pending)

# Custom help command
@bot.command()
async def help(ctx):
    help_text = (
        "📌 **Verify Command Help** 📌\n\n"
        "Use the following commands to verify your email and gain access to the server:\n"
        "1. Request verification: `!verify your_email@example.com`\n"
        "2. Enter code: `!verify your_email@example.com CODE`\n\n"
        "- Replace `your_email@example.com` with the email you registered.\n"
        "- You will receive a 6-character code via email.\n"
        "- Enter the code within 30 minutes to get the access role.\n"
        "- If your email is not on the whitelist, access will be denied.\n"
    )
    await ctx.send(help_text)

bot.run(TOKEN)
