import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import random
from datetime import datetime, timezone
from config import PREFIX, DEFAULT_EMOJI, EVENTS_CHANNEL_ID, LOGS_CHANNEL_ID, ALLOWED_ROLE_IDS

# Load the Discord bot token from the .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Enable all intents including members and reactions (required for role updates and reaction tracking)
intents = discord.Intents.all()

# Create bot instance with the specified prefix and intents
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Giveaway configuration stored in memory
giveaway_config = {
    "title": "Giveaway!",
    "description": "React to enter!",
    "emoji": DEFAULT_EMOJI,
    "eligible_roles": []  # List of role names eligible to enter
}

# ID of the giveaway message to track reactions
current_message_id = None

# Scheduled giveaway start and end times (datetime objects in UTC)
giveaway_schedule = {
    "start": None,
    "end": None
}

# === HELPER FUNCTIONS ===

def is_authorized(ctx):
    """Check if the command author has a role in ALLOWED_ROLE_IDS"""
    return any(role.id in ALLOWED_ROLE_IDS for role in ctx.author.roles)

async def ephemeral(ctx, message="✅ Done."):
    """Send a temporary ephemeral confirmation message (auto-deletes after 5 sec)"""
    await ctx.send(message, delete_after=5)

async def log_action(guild, title, description):
    """Send a log embed to the configured logs channel"""
    log_channel = guild.get_channel(LOGS_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(title=title, description=description, color=discord.Color.orange())
        await log_channel.send(embed=embed)

async def pick_winner_and_announce():
    """Pick a random eligible winner from reactions, announce publicly and via DM, and reset giveaway"""
    global giveaway_config, current_message_id, giveaway_schedule
    channel = bot.get_channel(EVENTS_CHANNEL_ID)
    if not current_message_id or not giveaway_config:
        return

    try:
        message = await channel.fetch_message(current_message_id)
    except Exception:
        # Could not fetch the giveaway message; maybe deleted
        return

    emoji = giveaway_config.get("emoji", DEFAULT_EMOJI)
    reaction = discord.utils.get(message.reactions, emoji=emoji)
    if not reaction:
        await channel.send("❌ No reactions found.", delete_after=5)
        return

    users = await reaction.users().flatten()
    eligible = []
    guild = channel.guild
    for user in users:
        if user.bot:
            continue
        member = guild.get_member(user.id)
        if not giveaway_config["eligible_roles"]:
            # If no role restrictions, all users who reacted are eligible
            eligible.append(user)
        else:
            member_roles = [role.name for role in member.roles]
            # Only users with at least one eligible role qualify
            if any(role in member_roles for role in giveaway_config["eligible_roles"]):
                eligible.append(user)

    if not eligible:
        await channel.send("❌ No eligible users.", delete_after=5)
        return

    winner = random.choice(eligible)
    # Announce winner publicly in giveaway channel
    await channel.send(f"🎉 Congratulations {winner.mention}! You won the giveaway! 🎉")

    # Try to DM the winner; ignore if DMs are closed
    try:
        await winner.send(f"🎉 Congratulations! You won the giveaway in **{guild.name}**! 🎉")
    except discord.Forbidden:
        await channel.send(f"⚠️ Could not DM {winner.mention}, but they won the giveaway!", delete_after=15)

    # Log the winner announcement
    await log_action(guild, "Giveaway Winner Drawn", f"Winner: {winner.mention} (Scheduled or manual)")

    # Reset giveaway state for next giveaway
    giveaway_config = {
        "title": "Giveaway!",
        "description": "React to enter!",
        "emoji": DEFAULT_EMOJI,
        "eligible_roles": []
    }
    current_message_id = None
    giveaway_schedule["start"] = None
    giveaway_schedule["end"] = None

# === COMMANDS ===

@bot.command()
async def set_title(ctx, *, title):
    """Set the giveaway title."""
    if not is_authorized(ctx):
        return
    giveaway_config["title"] = title
    await ephemeral(ctx)

@bot.command()
async def set_description(ctx, *, description):
    """Set the giveaway description."""
    if not is_authorized(ctx):
        return
    giveaway_config["description"] = description
    await ephemeral(ctx)

@bot.command()
async def set_emoji(ctx, emoji):
    """Set the emoji used for giveaway entry reactions."""
    if not is_authorized(ctx):
        return
    giveaway_config["emoji"] = emoji
    await ephemeral(ctx)

@bot.command()
async def add_role(ctx, *, role_name):
    """Add a role name to the list of eligible roles for giveaway entry."""
    if not is_authorized(ctx):
        return
    if role_name not in giveaway_config["eligible_roles"]:
        giveaway_config["eligible_roles"].append(role_name)
    await ephemeral(ctx)

@bot.command()
async def remove_role(ctx, *, role_name):
    """Remove a role name from the eligible roles list."""
    if not is_authorized(ctx):
        return
    if role_name in giveaway_config["eligible_roles"]:
        giveaway_config["eligible_roles"].remove(role_name)
    await ephemeral(ctx)

@bot.command()
async def preview_embed(ctx):
    """Preview the giveaway embed with current settings."""
    if not is_authorized(ctx):
        return
    roles = ", ".join(giveaway_config["eligible_roles"]) or "No role restrictions (everyone eligible)"
    embed = discord.Embed(
        title=giveaway_config["title"],
        description=f"{giveaway_config['description']}\n\n**Eligible Roles:** {roles}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed, delete_after=20)

@bot.command()
async def start_giveaway(ctx):
    """Post the giveaway embed and add reaction for entry."""
    if not is_authorized(ctx):
        return
    channel = bot.get_channel(EVENTS_CHANNEL_ID)
    embed = discord.Embed(
        title=giveaway_config["title"],
        description=giveaway_config["description"],
        color=discord.Color.blue()
    )
    message = await channel.send(embed=embed)
    await message.add_reaction(giveaway_config["emoji"])
    global current_message_id
    current_message_id = message.id
    await ephemeral(ctx)
    await log_action(ctx.guild, "Giveaway Posted", f"Posted in {channel.mention} by {ctx.author.mention}")

@bot.command()
async def draw_winner(ctx):
    """Manually pick a winner and announce."""
    if not is_authorized(ctx):
        return
    await pick_winner_and_announce()

@bot.command()
async def cancel_giveaway(ctx):
    """Cancel the current giveaway and reset all config."""
    if not is_authorized(ctx):
        return
    global giveaway_config, current_message_id, giveaway_schedule
    giveaway_config = {
        "title": "Giveaway!",
        "description": "React to enter!",
        "emoji": DEFAULT_EMOJI,
        "eligible_roles": []
    }
    current_message_id = None
    giveaway_schedule["start"] = None
    giveaway_schedule["end"] = None
    await ephemeral(ctx)
    await log_action(ctx.guild, "Giveaway Cancelled", f"Cancelled by {ctx.author.mention}")

@bot.command()
async def set_start(ctx, date: str, time: str):
    """Set scheduled giveaway start datetime (UTC). Format: YYYY-MM-DD HH:MM"""
    if not is_authorized(ctx):
        return
    try:
        dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        giveaway_schedule["start"] = dt
        await ephemeral(ctx, f"✅ Start time set to {dt.isoformat()} UTC")
        await log_action(ctx.guild, "Giveaway Start Set", f"Start time set to {dt.isoformat()} UTC")
    except Exception:
        await ctx.send("❌ Invalid date/time format. Use YYYY-MM-DD HH:MM", delete_after=10)

@bot.command()
async def set_end(ctx, date: str, time: str):
    """Set scheduled giveaway end datetime (UTC). Format: YYYY-MM-DD HH:MM"""
    if not is_authorized(ctx):
        return
    try:
        dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        giveaway_schedule["end"] = dt
        await ephemeral(ctx, f"✅ End time set to {dt.isoformat()} UTC")
        await log_action(ctx.guild, "Giveaway End Set", f"End time set to {dt.isoformat()} UTC")
    except Exception:
        await ctx.send("❌ Invalid date/time format. Use YYYY-MM-DD HH:MM", delete_after=10)

# === BACKGROUND TASK ===
@tasks.loop(seconds=30)
async def giveaway_scheduler():
    """Checks giveaway schedule every 30 seconds and auto-starts or auto-ends giveaways"""
    now = datetime.now(timezone.utc)
    global current_message_id

    if giveaway_schedule["start"] and giveaway_schedule["end"]:
        # Auto-start giveaway if scheduled time has passed and giveaway not active
        if giveaway_config and not current_message_id:
            if now >= giveaway_schedule["start"]:
                channel = bot.get_channel(EVENTS_CHANNEL_ID)
                embed = discord.Embed(
                    title=giveaway_config["title"],
                    description=giveaway_config["description"],
                    color=discord.Color.blue()
                )
                message = await channel.send(embed=embed)
                await message.add_reaction(giveaway_config["emoji"])
                current_message_id = message.id
                await log_action(channel.guild, "Giveaway Started Automatically", f"Giveaway started at scheduled time {now.isoformat()}")

        # Auto-end giveaway if scheduled end time reached
        if current_message_id and now >= giveaway_schedule["end"]:
            await pick_winner_and_announce()

giveaway_scheduler.before_loop(lambda: bot.wait_until_ready())
giveaway_scheduler.start()

# === EVENT: REMOVE REACTIONS IF USER LOSES REQUIRED ROLE ===
@bot.event
async def on_member_update(before, after):
    """
    When a member's roles update, remove their giveaway reaction if they lost an eligible role.
    """
    global current_message_id, giveaway_config

    # If no giveaway running or no role restrictions, no action needed
    if not current_message_id or not giveaway_config["eligible_roles"]:
        return

    # Determine which roles the member lost (by name)
    lost_roles = set(role.name for role in before.roles) - set(role.name for role in after.roles)
    # Check if any lost role is in eligible roles
    if not lost_roles.intersection(set(giveaway_config["eligible_roles"])):
        return

    channel = bot.get_channel(EVENTS_CHANNEL_ID)
    if not channel:
        return

    try:
        message = await channel.fetch_message(current_message_id)
    except Exception:
        return

    emoji = giveaway_config.get("emoji", DEFAULT_EMOJI)

    # Find the reaction matching the giveaway emoji
    for reaction in message.reactions:
        if str(reaction.emoji) == emoji:
            users = await reaction.users().flatten()
            # If the member has reacted, remove their reaction
            if after in users:
                try:
                    await reaction.remove(after)
                    # Notify user via DM about reaction removal
                    try:
                        await after.send("Your reaction was removed because you no longer have the required role(s) for the giveaway.")
                    except discord.Forbidden:
                        # User has DMs closed or blocked the bot
                        pass
                except discord.Forbidden:
                    # Bot lacks Manage Messages permission or cannot remove reaction
                    pass
            break

# Run the bot
bot.run(TOKEN)
