import discord
from datetime import datetime


def create_banner_embed(bot, title: str, description: str = "", color: int = 0x9b59b6) -> discord.Embed:
    """Crea un embed con el banner del bot"""
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.now()
    )
    if bot.user and bot.user.banner:
        embed.set_image(url=bot.user.banner.url)
    return embed


def create_success_embed(bot, title: str, description: str = "") -> discord.Embed:
    """Crea un embed de éxito con banner"""
    embed = create_banner_embed(bot, title, description, 0x2ecc71)
    return embed


def create_error_embed(bot, title: str, description: str = "") -> discord.Embed:
    """Crea un embed de error con banner"""
    embed = create_banner_embed(bot, title, description, 0xe74c3c)
    return embed


def create_info_embed(bot, title: str, description: str = "") -> discord.Embed:
    """Crea un embed informativo con banner"""
    embed = create_banner_embed(bot, title, description, 0x3498db)
    return embed


def set_footer_with_author(embed: discord.Embed, text: str = "✨ • Lux By _.aari._"):
    """Añade pie de página a un embed"""
    embed.set_footer(text=text)
    return embed
