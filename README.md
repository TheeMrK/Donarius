<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Donarius - Giveaway Bot</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
        Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
      max-width: 800px;
      margin: 2rem auto;
      padding: 0 1rem;
      background: #f9f9f9;
      color: #24292e;
    }
    h1 {
      color: #0366d6;
      border-bottom: 2px solid #e1e4e8;
      padding-bottom: 0.3rem;
    }
    h2 {
      border-bottom: 1px solid #e1e4e8;
      padding-bottom: 0.2rem;
      margin-top: 2rem;
      color: #24292e;
    }
    pre {
      background: #f6f8fa;
      padding: 1rem;
      overflow-x: auto;
      border-radius: 6px;
      border: 1px solid #d1d5da;
    }
    code {
      font-family: "SFMono-Regular", Consolas, "Liberation Mono",
        Menlo, Courier, monospace;
      background: #f6f8fa;
      padding: 0.2em 0.4em;
      border-radius: 3px;
    }
    blockquote {
      border-left: 4px solid #dfe2e5;
      padding-left: 1rem;
      color: #6a737d;
      margin: 1rem 0;
      font-style: italic;
    }
    table {
      border-collapse: collapse;
      width: 100%;
      margin-top: 1rem;
    }
    th,
    td {
      border: 1px solid #d1d5da;
      padding: 0.6rem;
      text-align: left;
    }
    th {
      background-color: #f6f8fa;
    }
    a {
      color: #0366d6;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <h1>🎁 Donarius - Giveaway Bot</h1>
  <p>
    A Discord bot for running server-based giveaways with
    role-based eligibility, scheduled start/end times, and automated
    logging.
  </p>

  <h2>📦 Features</h2>
  <ul>
    <li>🎉 Customizable giveaway embeds</li>
    <li>🕒 Schedule start and end times</li>
    <li>🛡️ Restrict entry based on roles</li>
    <li>🔐 Admin/Owner-only command access</li>
    <li>🔔 Winner is DM'd and publicly announced</li>
    <li>📜 Actions logged to a server log channel</li>
    <li>📁 Configurable with <code>.env</code> and <code>config.py</code></li>
  </ul>

  <h2>🚀 Setup Instructions</h2>
  <h3>1. Clone the Bot Repository</h3>
  <pre><code>git clone https://github.com/TheeMrK/Donarius.git
cd Donarius
</code></pre>

  <h3>2. Install Dependencies</h3>
  <pre><code>pip install -r requirements.txt
</code></pre>
  <p><em>Requires Python 3.8 or newer.</em></p>

  <h3>3. Create a <code>.env</code> File</h3>
  <pre><code>DISCORD_TOKEN=your_discord_bot_token_here
</code></pre>

  <h3>4. Configure <code>config.py</code></h3>
  <pre><code>PREFIX = "!"
DEFAULT_EMOJI = "🎉"

EVENTS_CHANNEL_ID = 1379237723185086544      # #events-giveaways
LOGS_CHANNEL_ID = 1379243941953540176        # #server-logs

ALLOWED_ROLE_IDS = [
    1379230385917005915,  # Admin role
    1379221955776872538   # Owner role
]
</code></pre>

  <h3>5. Run the Bot</h3>
  <pre><code>python Donarius.py
</code></pre>

  <h2>🛠 Permissions Checklist</h2>
  <p>When setting up the bot invite in the Discord Developer Portal:</p>
  <ul>
    <li><strong>Scopes:</strong> <code>bot</code>, <code>applications.commands</code> (optional)</li>
    <li><strong>Bot Permissions:</strong></li>
    <ul>
      <li>Send Messages</li>
      <li>Embed Links</li>
      <li>Add Reactions</li>
      <li>Read Message History</li>
      <li>View Channels</li>
      <li>(Optional) Manage Messages, Use External Emojis, Mention Everyone</li>
    </ul>
  </ul>

  <h2>📜 Bot Commands</h2>
  <p>Only users with roles in <code>ALLOWED_ROLE_IDS</code> can use commands. Bot replies are only visible to the command issuer.</p>
  <table>
    <thead>
      <tr>
        <th>Command</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><code>!set_title &lt;text&gt;</code></td><td>Set the giveaway title</td></tr>
      <tr><td><code>!set_description &lt;text&gt;</code></td><td>Set the giveaway description</td></tr>
      <tr><td><code>!set_emoji &lt;emoji&gt;</code></td><td>Set the emoji used for entry</td></tr>
      <tr><td><code>!add_role &lt;role name&gt;</code></td><td>Add a role to the eligible entry list</td></tr>
      <tr><td><code>!remove_role &lt;role name&gt;</code></td><td>Remove a role from eligibility</td></tr>
      <tr><td><code>!preview_embed</code></td><td>Preview the current giveaway setup</td></tr>
      <tr><td><code>!set_start YYYY-MM-DD HH:MM</code></td><td>Set the giveaway start time (UTC)</td></tr>
      <tr><td><code>!set_end YYYY-MM-DD HH:MM</code></td><td>Set the giveaway end time (UTC)</td></tr>
      <tr><td><code>!start_giveaway</code></td><td>Post the giveaway embed in the events channel</td></tr>
      <tr><td><code>!draw_winner</code></td><td>Pick a random winner and announce it</td></tr>
      <tr><td><code>!cancel_giveaway</code></td><td>Cancel the giveaway and reset the configuration</td></tr>
    </tbody>
  </table>

  <h2>📊 Example Usage</h2>
  <pre><code>!set_title Nitro Giveaway
!set_description React to enter free Nitro!
!set_emoji 🎉
!add_role Server Booster
!set_start 2025-06-20 18:00
!set_end 2025-06-21 18:00
!start_giveaway
</code></pre>

  <h2>🏆 Winner Selection</h2>
  <ul>
    <li>Winner is randomly selected from users who react with the correct emoji.</li>
    <li>Only users with required roles are eligible (if set).</li>
    <li>The winner is announced in the giveaway channel and DM’d.</li>
    <li>A log embed is posted in the logs channel.</li>
  </ul>

  <h2>🔒 Security Best Practices</h2>
  <ul>
    <li>Do <strong>not</strong> commit your <code>.env</code> file.</li>
    <li>Use <code>.gitignore</code> to keep secrets out of version control.</li>
    <li>Use Discord channel permissions to protect command access.</li>
  </ul>

  <h2>🧪 Ideas for Future Features</h2>
  <ul>
    <li>Slash command support</li>
    <li>Persistent storage for entries</li>
    <li>Web dashboard for managing events</li>
    <li>Role assignment on win</li>
  </ul>

  <h2>📄 License</h2>
  <p>MIT License – free to use and modify.</p>
</body>
</html>
