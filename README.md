# ✨ Lux - Discord Bot

**Lux** is a free, open-source Discord bot that replicates Mee6's premium level-based role rewards functionality. Designed for Discord server administrators who want automatic role assignments based on user levels without paying for premium subscriptions.

Created by **_.aari._** (Discord ID: 819080793447333918)

## 📋 Features

### 🏆 Level-Based Role Rewards
- Automatically assign Discord roles based on user levels from Mee6
- Configurable level thresholds for role rewards
- Optional automatic removal of lower-tier roles when users level up
- Real-time updates on message events
- Scheduled bulk updates every 5 minutes

### 🎮 Economy System
- **39 items** across 5 rarity tiers:
  - ⭐ **Común** - Basic badges and stars
  - 🔮 **Raro** - Crowns, crystals, and trophies
  - 💫 **Épico** - Gems, celestial items, and enchantments
  - ✨ **Legendario** - Divine artifacts and exclusive items
  - 🔱 **Exclusiva** - Developer-only items
- User economy with balance tracking
- Daily bonus rewards
- Interactive shop interface

### 🎫 Ticket System
- Create and manage support tickets
- Claim tickets for assignment
- Auto-delete ticket channels after closing
- Ticket statistics and analytics

### ⚙️ Modern Discord Interactions
- Slash commands with full autocomplete
- Interactive dropdown menus
- Modal forms for user input
- Button-based interactions
- Modern Views and Select menus

### 📖 Customizable Server Rules
- Three pre-built rule templates:
  - 📋 **Formal** - Structured, professional rules
  - 😊 **Permissive** - Relaxed, friendly rules
  - 🛡️ **Strict** - Zero-tolerance rules
- Bilingual support (Spanish/English)
- Custom title personalization via modal
- Color-coded embeds by rule type

### 🌍 Bilingual Support
- Complete Spanish and English interface
- Slash commands in both languages
- Customizable server rules with language selection

### 📊 Administration Tools
- Role reward configuration and management
- Log channel setup for tracking events
- Level-up notifications
- Global announcement system
- Maintenance mode with user notifications
- Server backup and restore functionality

### 🛡️ Security & Error Handling
- Comprehensive error logging with Discord channel integration
- Graceful error handling for all operations
- Role permission validation
- Database fallback to JSON-only mode

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Discord Bot Token
- Mee6 API access (public, no token required)
- PostgreSQL database (optional, JSON fallback available)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AriDev/lux-discord-bot.git
   cd lux-discord-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create a .env file or set these in your environment
   DISCORD_BOT_TOKEN=your_bot_token_here
   DATABASE_URL=postgresql://user:password@localhost/lux  # Optional
   DEVELOPER_ID=your_discord_id  # For developer commands
   ```

4. **Run the bot**
   ```bash
   python src/bot/main.py
   ```

## 📁 Project Structure

```
lux-discord-bot/
├── src/
│   ├── bot/
│   │   └── main.py                 # Bot entry point
│   ├── cogs/                       # Command modules
│   │   ├── add.py                  # Role reward configuration
│   │   ├── economy/                # Economy system cogs
│   │   ├── tickets/                # Ticket system cogs
│   │   ├── rules.py                # Server rules command
│   │   └── ...                     # Other feature cogs
│   └── utils/
│       └── discord_tools/
│           ├── error_logger.py     # Error handling
│           ├── embeds.py           # Embed utilities
│           └── views.py            # UI components
├── config/
│   ├── roles.json                  # Role reward mappings
│   ├── configuration.json          # Bot settings
│   ├── economy.json                # Economy data
│   ├── shop.json                   # Shop items
│   └── ...                         # Other config files
├── requirements.txt                # Python dependencies
└── replit.md                       # Project documentation
```

## 🔧 Configuration

### Role Rewards (`config/roles.json`)
```json
{
  "guild_id": {
    "roles": {
      "level": "role_id",
      "5": "1234567890",
      "10": "1234567891"
    },
    "updateEachMessage": true,
    "updateEachTime": true,
    "removePreviousRewards": true
  }
}
```

### Economy Setup
Use `/economysetup` command to configure:
- Starting balance
- Daily bonus amount
- Currency name
- Shop items

### Ticket System
Use `/ticketsetup` command to configure:
- Ticket category
- Support role
- Ticket prefix
- Log channel

## 📚 Commands

### Administration
- `/add <level> <role>` - Add role reward
- `/remove <level>` - Remove role reward
- `/setlogchannel` - Configure logging channel
- `/setnotifications` - Configure notifications
- `/backup` - Export guild configuration
- `/removepreviousrewards <true/false>` - Toggle role removal

### Utility
- `/help` - Interactive help system
- `/rolerewards` - List all role rewards
- `/stats` - Server statistics
- `/invite` - Bot information and invite link
- `/rules` - Display customizable server rules

### Economy
- `/economysetup` - Configure economy system
- `/admin` - Economy admin management
- `/itemlist` - Browse shop items
- `/shop` - Purchase items
- `/balance` - Check user balance
- `/dailybonus` - Claim daily rewards

### Tickets
- `/ticketsetup` - Configure ticket system
- `/ticketstats` - View ticket statistics
- Interactive buttons for ticket management

### Moderation
- `/mod <user>` - Moderation menu (kick, ban, warn, mute)
- `/purge <amount>` - Delete messages

### Developer
- `/maintenance <activate> [message]` - Toggle maintenance mode
- `/restart` - Restart bot
- `/announce` - Send global announcement
- `/updateannounce` - Update and resend announcement

## 🔌 External Dependencies

### Discord API
- **py-cord 2.6.1** - Modern Discord API wrapper with slash command support
- **discord-py 2.6.4** - Legacy compatibility layer

### Data Sources
- **Mee6 Public API** - User levels and leaderboard data
  - No authentication required
  - Endpoints: User level lookup, paginated leaderboard

### Database (Optional)
- **PostgreSQL** - Optional for scaling and performance
  - asyncpg 0.31.0 - Async PostgreSQL driver
  - psycopg2-binary 2.9.11 - PostgreSQL adapter

### HTTP & Utilities
- **aiohttp 3.13.2** - Asynchronous HTTP requests
- **Pillow 12.0.0** - Image processing (future features)

## 🔒 Security & Privacy

- Bot requires `members`, `message_content`, and `default` intents
- No personal user data is stored permanently
- Supports optional PostgreSQL with connection string from environment
- Comprehensive error logging with traceback information
- Mentions developer for critical errors
- See [Privacy & Policy.md](./Privacy%20&%20Policy.md) and [Terms & Conditions.md](./Terms%20&%20Conditions.md)

## 🛠️ Development

### Adding New Commands
1. Create a new Cog file in `src/cogs/`
2. Extend `commands.Cog` class
3. Define slash commands with `@discord.slash_command`
4. Add setup function: `def setup(bot): bot.add_cog(YourCog(bot))`

### Error Handling
All errors are automatically logged to the designated error channel with:
- Error traceback
- User information
- Guild information
- Command context
- Developer mentions for critical errors

### Testing
The bot includes a testing cog (`src/cogs/Ari/testing.py`) for development and debugging.

## 📊 Current Status

**Version:** V1.5.1  
**Status:** Production Ready ✅

- ✓ 31 cogs loaded successfully
- ✓ Zero runtime errors
- ✓ Full feature parity with V1.5.0+
- ✓ Stable Mee6 API integration
- ✓ Comprehensive error handling

## 📝 License

This project is open-source. See LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Report bugs via GitHub Issues
- Suggest features and improvements
- Submit pull requests with enhancements

## 💬 Support

For issues, questions, or feature requests:
1. Check existing GitHub Issues
2. Create a new Issue with detailed information
3. Include bot version, error logs, and reproduction steps

## 👤 Author

**_.aari._**
- Discord: _.aari._ (ID: 819080793447333918)
- GitHub: [AriDev](https://github.com/AriDev)

## 🎉 Acknowledgments

- Inspired by Mee6's level-based role reward system
- Built with [py-cord](https://github.com/Pycord-Development/py-cord)
- API data from Mee6's public API

---

**Lux ✨** - Making premium features accessible to all Discord communities.
