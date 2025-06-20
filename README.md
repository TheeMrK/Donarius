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
