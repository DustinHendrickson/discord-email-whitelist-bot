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

bot = commands.Bot(command_prefix="!", intents=intents)

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

# Optional: show whitelist (for admins)
@bot.command()
@commands.has_permissions(administrator=True)
async def show_whitelist(ctx):
    whitelist = load_whitelist()
    await ctx.send("Whitelist:\n" + "\n".join(whitelist))

bot.run(TOKEN)
