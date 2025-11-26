import discord
from datetime import datetime
import traceback
from src.utils.lux_quotes import get_error_quote

ERROR_CHANNEL_ID = 1443091711038587051
DEVELOPER_ID = 819080793447333918

async def log_error_to_channel(bot, error: Exception, context: str = "Unknown", user: discord.User | None = None, guild: discord.Guild | None = None):
    try:
        channel = bot.get_channel(ERROR_CHANNEL_ID)
        if not channel:
            print(f"❌ Error logging channel not found: {ERROR_CHANNEL_ID}")
            return
        
        tb_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        tb_lines = tb_str.split('\n')
        tb_short = '\n'.join(tb_lines[-10:])
        
        lux_quote = get_error_quote()
        
        embed = discord.Embed(
            title="🚨 **¡OH NO! MI MAGIA FALLÓ**",
            description=lux_quote,
            color=0xe74c3c,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="📌 Contexto",
            value=f"`{context}`",
            inline=False
        )
        
        embed.add_field(
            name="⚠️ Error",
            value=f"```python\n{str(error)[:500]}```",
            inline=False
        )
        
        embed.add_field(
            name="📋 Traceback",
            value=f"```python\n{tb_short[:1000]}```",
            inline=False
        )
        
        if user:
            embed.add_field(
                name="👤 Usuario",
                value=f"{user.mention} ({user.id})",
                inline=True
            )
        
        if guild:
            embed.add_field(
                name="🏢 Servidor",
                value=f"{guild.name} ({guild.id})",
                inline=True
            )
        
        embed.add_field(
            name="🔧 Tipo de Error",
            value=f"`{type(error).__name__}`",
            inline=True
        )
        
        embed.set_footer(text="✨ • Lux By _.aari._ | Tú eres el buscador de la verdad")
        
        await channel.send(embed=embed)
    except Exception as log_error:
        print(f"❌ Failed to log error: {log_error}")
