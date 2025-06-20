import os
from dotenv import load_dotenv
import discord
from discord.ext import tasks
import random
from datetime import datetime, timezone
from config import DEFAULT_EMOJI, EVENTS_CHANNEL_ID, LOGS_CHANNEL_ID, ALLOWED_ROLE_IDS

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

# Giveaway config and state (in-memory)
giveaway_config = {
    "title": "Giveaway!",
    "description": "React to enter!",
    "emoji": DEFAULT_EMOJI,
    "eligible_roles": []
}
current_message_id = None
giveaway_schedule = {"start": None, "end": None}


# Helper to check user roles
def is_authorized(member: discord.Member) -> bool:
    return any(role.id in ALLOWED_ROLE_IDS for role in member.roles)


# Logging helper
async def log_action(guild: discord.Guild, title: str, description: str):
    log_channel = guild.get_channel(LOGS_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(title=title, description=description, color=discord.Color.orange())
        await log_channel.send(embed=embed)


async def pick_winner_and_announce():
    global giveaway_config, current_message_id, giveaway_schedule
    channel = bot.get_channel(EVENTS_CHANNEL_ID)
    if not current_message_id or not giveaway_config:
        return

    try:
        message = await channel.fetch_message(current_message_id)
    except Exception:
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
            eligible.append(user)
        else:
            member_roles = [role.name for role in member.roles]
            if any(role in member_roles for role in giveaway_config["eligible_roles"]):
                eligible.append(user)

    if not eligible:
        await channel.send("❌ No eligible users.", delete_after=5)
        return

    winner = random.choice(eligible)
    await channel.send(f"🎉 Congratulations {winner.mention}! You won the giveaway! 🎉")

    try:
        await winner.send(f"🎉 Congratulations! You won the giveaway in **{guild.name}**! 🎉")
    except discord.Forbidden:
        await channel.send(f"⚠️ Could not DM {winner.mention}, but they won the giveaway!", delete_after=15)

    await log_action(guild, "Giveaway Winner Drawn", f"Winner: {winner.mention} (Scheduled or manual)")

    # Reset giveaway
    giveaway_config.update({
        "title": "Giveaway!",
        "description": "React to enter!",
        "emoji": DEFAULT_EMOJI,
        "eligible_roles": []
    })
    current_message_id = None
    giveaway_schedule["start"] = None
    giveaway_schedule["end"] = None


# Slash commands:

@tree.command(name="set_title", description="Set the giveaway title")
async def set_title(interaction: discord.Interaction, title: str):
    if not is_authorized(interaction.user):
        await interaction.response.send_message("❌ You are not authorized.", ephemeral=True)
        return
    giveaway_config["title"] = title
    await interaction.response.send_message("✅ Giveaway title updated.", ephemeral=True)


@tree.command(name="set_description", description="Set the giveaway description")
async def set_description(interaction: discord.Interaction, description: str):
    if not is_authorized(interaction.user):
        await interaction.response.send_message("❌ You are not authorized.", ephemeral=True)
        return
    giveaway_config["description"] = description
    await interaction.response.send_message("✅ Giveaway description updated.", ephemeral=True)


@tree.command(name="set_emoji", description="Set the emoji used for giveaway reactions")
async def set_emoji(interaction: discord.Interaction, emoji: str):
    if not is_authorized(interaction.user):
        await interaction.response.send_message("❌ You are not authorized.", ephemeral=True)
        return
    giveaway_config["emoji"] = emoji
    await interaction.response.send_message("✅ Giveaway emoji updated.", ephemeral=True)


@tree.command(name="add_role", description="Add a role eligible to enter the giveaway")
async def add_role(interaction: discord.Interaction, role_name: str):
    if not is_authorized(interaction.user):
        await interaction.response.send_message("❌ You are not authorized.", ephemeral=True)
        return
    if role_name not in giveaway_config["eligible_roles"]:
        giveaway_config["eligible_roles"].append(role_name)
    await interaction.response.send_message(f"✅ Role '{role_name}' added to eligible roles.", ephemeral=True)


@tree.command(name="remove_role", description="Remove a role from eligible roles")
async def remove_role(interaction: discord.Interaction, role_name: str):
    if not is_authorized(interaction.user):
        await interaction.response.send_message("❌ You are not authorized.", ephemeral=True)
        return
    if role_name in giveaway_config["eligible_roles"]:
        giveaway_config["eligible_roles"].remove(role_name)
        await interaction.response.send_message(f"✅ Role '{role_name}' removed from eligible roles.", ephemeral=True)
    else:
        await interaction.response.send_message(f"⚠️ Role '{role_name}' not found in eligible roles.", ephemeral=True)


@tree.command(name="preview_embed", description="Preview the giveaway embed")
async def preview_embed(interaction: discord.Interaction):
    if not is_authorized(interaction.user):
        await interaction.response.send_message("❌ You are not authorized.", ephemeral=True)
        return
    roles = ", ".join(giveaway_config["eligible_roles"]) or "No role restrictions (everyone eligible)"
    embed = discord.Embed(
        title=giveaway_config["title"],
        description=f"{giveaway_config['description']}\n\n**Eligible Roles:** {roles}",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@tree.command(name="start_giveaway", description="Post the giveaway and open entry")
async def start_giveaway(interaction: discord.Interaction):
    if not is_authorized(interaction.user):
        await interaction.response.send_message("❌ You are not authorized.", ephemeral=True)
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
    await interaction.response.send_message("✅ Giveaway started.", ephemeral=True)
    await log_action(interaction.guild, "Giveaway Posted", f"Posted in {channel.mention} by {interaction.user.mention}")


@tree.command(name="draw_winner", description="Pick a winner and announce")
async def draw_winner(interaction: discord.Interaction):
    if not is_authorized(interaction.user):
        await interaction.response.send_message("❌ You are not authorized.", ephemeral=True)
        return
    await pick_winner_and_announce()
    await interaction.response.send_message("✅ Winner drawn.", ephemeral=True)


@tree.command(name="cancel_giveaway", description="Cancel the current giveaway")
async def cancel_giveaway(interaction: discord.Interaction):
    if not is_authorized(interaction.user):
        await interaction.response.send_message("❌ You are not authorized.", ephemeral=True)
        return
    global giveaway_config, current_message_id, giveaway_schedule
    giveaway_config.update({
        "title": "Giveaway!",
        "description": "React to enter!",
        "emoji": DEFAULT_EMOJI,
        "eligible_roles": []
    })
    current_message_id = None
    giveaway_schedule["start"] = None
    giveaway_schedule["end"] = None
    await interaction.response.send_message("✅ Giveaway cancelled.", ephemeral=True)
    await log_action(interaction.guild, "Giveaway Cancelled", f"Cancelled by {interaction.user.mention}")


@tree.command(name="set_start", description="Set giveaway start datetime (UTC, YYYY-MM-DD HH:MM)")
async def set_start(interaction: discord.Interaction, datetime_str: str):
    if not is_authorized(interaction.user):
        await interaction.response.send_message("❌ You are not authorized.", ephemeral=True)
        return
    try:
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        giveaway_schedule["start"] = dt
        await interaction.response.send_message(f"✅ Start time set to {dt.isoformat()} UTC", ephemeral=True)
        await log_action(interaction.guild, "Giveaway Start Set", f"Start time set to {dt.isoformat()} UTC")
    except Exception:
        await interaction.response.send_message("❌ Invalid date/time format. Use YYYY-MM-DD HH:MM", ephemeral=True)


@tree.command(name="set_end", description="Set giveaway end datetime (UTC, YYYY-MM-DD HH:MM)")
async def set_end(interaction: discord.Interaction, datetime_str: str):
    if not is_authorized(interaction.user):
        await interaction.response.send_message("❌ You are not authorized.", ephemeral=True)
        return
    try:
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        giveaway_schedule["end"] = dt
        await interaction.response.send_message(f"✅ End time set to {dt.isoformat()} UTC", ephemeral=True)
        await log_action(interaction.guild, "Giveaway End Set", f"End time set to {dt.isoformat()} UTC")
    except Exception:
        await interaction.response.send_message("❌ Invalid date/time format. Use YYYY-MM-DD HH:MM", ephemeral=True)


# Background task remains largely the same:
@tasks.loop(seconds=30)
async def giveaway_scheduler():
    now = datetime.now(timezone.utc)
    global current_message_id

    if giveaway_schedule["start"] and giveaway_schedule["end"]:
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

        if current_message_id and now >= giveaway_schedule["end"]:
            await pick_winner_and_announce()


@giveaway_scheduler.before_loop
async def before_scheduler():
    await bot.wait_until_ready()


giveaway_scheduler.start()


@bot.event
async def on_member_update(before, after):
    global current_message_id, giveaway_config

    if not current_message_id or not giveaway_config["eligible_roles"]:
        return

    lost_roles = set(role.name for role in before.roles) - set(role.name for role in after.roles)
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

    for reaction in message.reactions:
        if str(reaction.emoji) == emoji:
            users = await reaction.users().flatten()
            if after in users:
                try:
                    await reaction.remove(after)
                    try:
                        await after.send("Your reaction was removed because you no longer have the required role(s) for the giveaway.")
                    except discord.Forbidden:
                        pass
                except discord.Forbidden:
                    pass
            break


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    # Sync slash commands globally or to guild for faster update
    try:
        # For development, sync to guild for immediate effect:
        # guild = discord.Object(id=YOUR_GUILD_ID)
        # await tree.sync(guild=guild)
        await tree.sync()  # global sync
        print("Slash commands synced.")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")


bot.run(TOKEN)
