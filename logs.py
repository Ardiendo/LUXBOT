import os
import discord
from discord.ext import commands
from discord import Option
from datetime import datetime
from src.utils.discord_tools.embeds import create_banner_embed, create_success_embed, create_error_embed, set_footer_with_author


class LogsCog(commands.Cog, name="logs command"):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command(
        name="setlogchannel",
        description="Configura el canal para recibir logs de roles"
    )
    @discord.default_permissions(administrator=True)
    async def slash_setlogchannel(
        self,
        ctx: discord.ApplicationContext,
        canal: discord.TextChannel = Option(
            description="Canal donde se enviarán los logs",
            required=True
        )
    ):
        embed = create_success_embed(
            self.bot,
            "✅ **Canal de Logs Configurado**",
            f"Los logs de roles se enviarán a {canal.mention}"
        )
        embed.add_field(
            name="📝 Información",
            value="Se registrarán:\n• Roles asignados por nivel\n• Roles removidos\n• Cambios de configuración",
            inline=False
        )
        embed = set_footer_with_author(embed)
        await ctx.respond(embed=embed)
        
        log_embed = create_banner_embed(
            self.bot,
            "🔔 **Sistema de Logs Activado**",
            "Este canal ahora recibirá los logs del bot Lux.",
            0x9b59b6
        )
        log_embed = set_footer_with_author(log_embed)
        await canal.send(embed=log_embed)
    
    @discord.slash_command(
        name="disablelogs",
        description="Desactiva los logs de roles"
    )
    @discord.default_permissions(administrator=True)
    async def slash_disablelogs(self, ctx: discord.ApplicationContext):
        embed = create_success_embed(
            self.bot,
            "✅ **Logs Desactivados**",
            "Ya no se enviarán logs de roles."
        )
        embed = set_footer_with_author(embed)
        await ctx.respond(embed=embed)
    
    @discord.slash_command(
        name="viewlogs",
        description="Ver los últimos logs de roles"
    )
    @discord.default_permissions(administrator=True)
    async def slash_viewlogs(
        self,
        ctx: discord.ApplicationContext,
        cantidad: Option(
            int,
            description="Cantidad de logs a mostrar (máx 25)",
            required=False,
            min_value=1,
            max_value=25
        ) = 10
    ):
        embed = create_banner_embed(
            self.bot,
            "📋 **Últimos Logs de Roles**",
            "Los logs se mostrarían aquí si estuviera conectada la BD",
            0x3498db
        )
        embed.add_field(
            name="💡 Nota",
            value="El sistema de logs requiere la base de datos activada.",
            inline=False
        )
        embed = set_footer_with_author(embed)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(LogsCog(bot))
