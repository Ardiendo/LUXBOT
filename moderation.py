import discord
from discord.ext import commands
from datetime import datetime
from src.utils.discord_tools.mod_view import ModView

class ModerationCog(commands.Cog, name="moderation commands"):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="mod",
        description="Herramientas de moderación con menú interactivo"
    )
    async def mod(self, ctx: discord.ApplicationContext, usuario: discord.Member, razon: str = "Sin razón especificada"):
        if not isinstance(ctx.author, discord.Member) or not ctx.author.guild_permissions.moderate_members:
            embed = discord.Embed(
                title="❌ **PERMISOS INSUFICIENTES**",
                description="No tienes permisos para usar comandos de moderación",
                color=0xe74c3c,
                timestamp=datetime.now()
            )
            embed.set_footer(text="✨ • Lux By _.aari._")
            return await ctx.respond(embed=embed, ephemeral=True)
        
        if usuario == ctx.author:
            embed = discord.Embed(
                title="❌ **ERROR**",
                description="No puedes moderar tu propio usuario",
                color=0xe74c3c,
                timestamp=datetime.now()
            )
            embed.set_footer(text="✨ • Lux By _.aari._")
            return await ctx.respond(embed=embed, ephemeral=True)
        
        embed = discord.Embed(
            title="⚙️ **HERRAMIENTAS DE MODERACIÓN**",
            description=f"Selecciona una acción para {usuario.mention}",
            color=0x9b59b6,
            timestamp=datetime.now()
        )
        embed.add_field(
            name="👤 Usuario objetivo",
            value=f"{usuario.mention} ({usuario.id if usuario.id else 'N/A'})",
            inline=False
        )
        embed.add_field(
            name="👮 Moderador",
            value=f"{ctx.author.mention}",
            inline=True
        )
        embed.add_field(
            name="🏢 Servidor",
            value=f"{ctx.guild.name if ctx.guild else 'N/A'}",
            inline=True
        )
        embed.add_field(
            name="📋 Razón",
            value=razon,
            inline=False
        )
        
        if usuario.avatar:
            embed.set_thumbnail(url=usuario.avatar.url)
        
        embed.set_footer(text="✨ • Lux By _.aari._")
        
        view = ModView(usuario, ctx.author, razon)
        await ctx.respond(embed=embed, view=view)


def setup(bot):
    bot.add_cog(ModerationCog(bot))
