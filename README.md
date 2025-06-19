# 🎁 Donarius

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Last Commit](https://img.shields.io/github/last-commit/TheeMrK/Donarius)
![Stars](https://img.shields.io/github/stars/TheeMrK/Donarius?style=social)

> A role-restricted Discord giveaway bot with logging, scheduling, and winner automation.


---

## 📦 Features

- 🎉 Customizable giveaway embeds
- 🕒 Schedule start and end times
- 🛡️ Restrict entry based on roles
- 🔐 Admin/Owner-only command access
- 🔔 Winner is DM'd and publicly announced
- 📜 Actions logged to a server log channel
- 📁 Configurable with `.env` and `config.py`

---

## 🚀 Setup Instructions

### 1. Clone the Bot Repository

```bash
git clone https://github.com/yourusername/giveaway-bot.git
cd giveaway-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> Requires Python 3.8 or newer.

### 3. Create a `.env` File

```env
DISCORD_TOKEN=your_discord_bot_token_here
```

### 4. Configure `config.py`

```python
PREFIX = "!"
DEFAULT_EMOJI = "🎉"

EVENTS_CHANNEL_ID = 1379237723185086544      # #events-giveaways
LOGS_CHANNEL_ID = 1379243941953540176        # #server-logs

ALLOWED_ROLE_IDS = [
    1379230385917005915,  # Admin role
    1379221955776872538   # Owner role
]
```

### 5. Run the Bot

```bash
python bot.py
```

---

## 🛠 Permissions Checklist

When setting up the bot invite in the Discord Developer Portal:

### ✅ Scopes
- `bot`
- `applications.commands` *(optional for future slash commands)*

### ✅ Bot Permissions
- `Send Messages`
- `Embed Links`
- `Add Reactions`
- `Read Message History`
- `View Channels`
- *(Optional)* `Manage Messages`, `Use External Emojis`, `Mention Everyone`

---

## 📜 Bot Commands

Only users with roles in `ALLOWED_ROLE_IDS` can use commands. Bot replies are only visible to the command issuer.

| Command                            | Description                                             |
|------------------------------------|---------------------------------------------------------|
| `!set_title <text>`                | Set the giveaway title                                  |
| `!set_description <text>`          | Set the giveaway description                            |
| `!set_emoji <emoji>`               | Set the emoji used for entry                            |
| `!add_role <role name>`            | Add a role to the eligible entry list                   |
| `!remove_role <role name>`         | Remove a role from eligibility                          |
| `!preview_embed`                   | Preview the current giveaway setup                      |
| `!set_start YYYY-MM-DD HH:MM`      | Set the giveaway start time (UTC)                       |
| `!set_end YYYY-MM-DD HH:MM`        | Set the giveaway end time (UTC)                         |
| `!start_giveaway`                  | Post the giveaway embed in the events channel           |
| `!draw_winner`                     | Pick a random winner and announce it                    |
| `!cancel_giveaway`                 | Cancel the giveaway and reset the configuration         |

---

## 📊 Example Usage

```text
!set_title Nitro Giveaway
!set_description React to enter free Nitro!
!set_emoji 🎉
!add_role Server Booster
!set_start 2025-06-20 18:00
!set_end 2025-06-21 18:00
!start_giveaway
```

---

## 🏆 Winner Selection

- Winner is randomly selected from users who react with the correct emoji.
- Only users with required roles are eligible (if set).
- The winner is announced in the giveaway channel and DM’d.
- A log embed is posted in the logs channel.

---

## 🔒 Security Best Practices

- Do **not** commit your `.env` file.
- Use `.gitignore` to keep secrets out of version control.
- Use Discord channel permissions to protect command access.

---

## 🧪 Ideas for Future Features

- Slash command support
- Persistent storage for entries
- Web dashboard for managing events
- Role assignment on win

---

## 📄 License

MIT License – free to use and modify.
