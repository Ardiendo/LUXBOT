import os
import discord
from discord.ext import commands
from datetime import datetime
from src.utils.discord_tools.views import HelpView
from src.utils.discord_tools.embeds import set_footer_with_author


class HelpCog(commands.Cog, name="help command"):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="help",
        description="Ver la página de ayuda del bot con menú desplegable"
    )
    async def slash_help(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="📖 **Página de Ayuda - Lux✨**",
            description="Selecciona una categoría en el menú desplegable para obtener más información",
            color=0xdeaa0c,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="🏠 Principal",
            value="Información general sobre el bot",
            inline=True
        )
        embed.add_field(
            name="🏆 Recompensas",
            value="Comandos de recompensas de nivel",
            inline=True
        )
        embed.add_field(
            name="🛠️ Utilidades",
            value="Herramientas disponibles",
            inline=True
        )
        embed.add_field(
            name="⚙️ Administración",
            value="Comandos solo para admins",
            inline=True
        )
        embed.add_field(
            name="📊 Sistema",
            value="Logs y notificaciones",
            inline=True
        )
        embed.add_field(
            name="✨ Novedades",
            value="Últimas funcionalidades",
            inline=True
        )
        
        if self.bot.user and self.bot.user.banner:
            embed.set_image(url=self.bot.user.banner.url)
        if self.bot.user and self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
        
        embed = set_footer_with_author(embed)
        view = HelpView(self.bot)
        await ctx.respond(embed=embed, view=view)


def setup(bot):
    bot.remove_command("help")
    bot.add_cog(HelpCog(bot))
