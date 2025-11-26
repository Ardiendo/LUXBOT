import os
import discord
from discord.ext import commands
from discord import Option
from datetime import datetime
from src.utils.discord_tools.embeds import create_banner_embed, create_success_embed, set_footer_with_author


class NotificationsCog(commands.Cog, name="notifications command"):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command(
        name="setnotifications",
        description="Configura el canal para notificaciones de subida de nivel"
    )
    @discord.default_permissions(administrator=True)
    async def slash_setnotifications(
        self,
        ctx: discord.ApplicationContext,
        canal: discord.TextChannel = Option(
            description="Canal donde se enviarán las notificaciones",
            required=True
        )
    ):
        embed = create_banner_embed(
            self.bot,
            "🔔 **Notificaciones Activadas**",
            f"Las notificaciones de nivel se enviarán a {canal.mention}",
            0x2ecc71
        )
        embed.add_field(
            name="📝 Información",
            value="Se notificará cuando un usuario:\n• Suba de nivel\n• Obtenga un nuevo rol de recompensa",
            inline=False
        )
        embed = set_footer_with_author(embed)
        await ctx.respond(embed=embed)
    
    @discord.slash_command(
        name="disablenotifications",
        description="Desactiva las notificaciones de nivel"
    )
    @discord.default_permissions(administrator=True)
    async def slash_disablenotifications(self, ctx: discord.ApplicationContext):
        embed = create_banner_embed(
            self.bot,
            "🔕 **Notificaciones Desactivadas**",
            "Ya no se enviarán notificaciones de nivel.",
            0xe74c3c
        )
        embed = set_footer_with_author(embed)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(NotificationsCog(bot))
