# Donarius Giveaway Bot

A Discord bot to run role-restricted giveaways with scheduled start/end times and slash command management.

---

## Features

- Slash commands for configuring giveaways:
  - Set giveaway title, description, and emoji
  - Add/remove roles eligible to enter
  - Preview giveaway embed
  - Start, cancel giveaways manually
  - Schedule giveaways with start and end times (UTC)
  - Manually draw winner
- Automatically pick winner at scheduled end time
- Restrict entry to users with specified roles
- Remove reactions if user loses eligible roles
- Logs giveaway events to a designated channel

---

## Setup

### Requirements

- Python 3.10+
- Discord bot token (with **bot** and **applications.commands** intents enabled)
- Docker (optional, if using Docker deployment)
- `discord.py` library (tested with v2.x)

### Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/donarius-bot.git
    cd donarius-bot
    ```

2. Create a `.env` file with your Discord bot token:

    ```
    DISCORD_TOKEN=your_bot_token_here
    ```

3. Update `config.py` with your server-specific IDs and settings:

    - `EVENTS_CHANNEL_ID` — channel to post giveaways  
    - `LOGS_CHANNEL_ID` — channel for giveaway logs  
    - `ALLOWED_ROLE_IDS` — roles allowed to manage giveaways  
    - `DEFAULT_EMOJI` — default emoji for reactions  

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

---

## Running the Bot

```bash
python donarius.py

Use these commands in Discord by typing / to open the command menu:

Command	Description	Parameters
/set_title	Set the giveaway title	title (string)
/set_description	Set the giveaway description	description (string)
/set_emoji	Set emoji for giveaway entry	emoji (string, e.g. 🎉)
/add_role	Add a role eligible to enter	role_name (string)
/remove_role	Remove an eligible role	role_name (string)
/preview_embed	Preview the giveaway embed	(no parameters)
/start_giveaway	Start and post the giveaway	(no parameters)
/draw_winner	Manually pick a winner	(no parameters)
/cancel_giveaway	Cancel the current giveaway	(no parameters)
/set_start	Schedule giveaway start (UTC)	datetime_str (string, "YYYY-MM-DD HH:MM")
/set_end	Schedule giveaway end (UTC)	datetime_str (string, "YYYY-MM-DD HH:MM")

Notes
All scheduled times are in UTC.

Only users with roles in ALLOWED_ROLE_IDS can manage giveaways.

The bot automatically removes reactions from users who lose eligible roles.

Make sure to sync slash commands on bot startup (this happens automatically).

Troubleshooting
If slash commands do not appear, try restarting the bot or sync commands manually.

Check bot permissions: it requires Send Messages, Add Reactions, Manage Messages, and Read Message History in the giveaway channel.

For date/time commands, use format YYYY-MM-DD HH:MM (24-hour, UTC).

License
MIT License

vbnet
Copy
Edit

Let me know if you want me to generate `requirements.txt` or a Dockerfile too!








