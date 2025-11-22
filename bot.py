import discord
from discord.ext import commands
import json
import os

# Load config from JSON
with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["token"]
GUILD_ID = config["guild_id"]
ROLE_NAME = config["role_name"]

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

# Verify command
@bot.command()
async def verify(ctx, *, email: str = None):
    if email is None:
        await ctx.send("Usage: !verify your_email@example.com")
        return

    email = email.strip().lower()
    whitelist = load_whitelist()  # Load fresh every time

    if email in whitelist:
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
    else:
        await ctx.send("Email not on whitelist. Access denied.")

# Custom help command
@bot.command()
async def help(ctx):
    help_text = (
        "📌 **Verify Command Help** 📌\n\n"
        "Use the following command to verify your email and gain access to the server:\n"
        "`!verify your_email@example.com`\n\n"
        "- Replace `your_email@example.com` with the email you registered.\n"
        "- If your email is in the whitelist, the bot will assign you the access role.\n"
        "- If your email is not on the whitelist, access will be denied.\n"
    )
    await ctx.send(help_text)

bot.run(TOKEN)
