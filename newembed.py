import discord
from discord.ext import commands
from datetime import datetime
from src.utils.discord_tools.embed_builder import EmbedBuilderModal, load_newembed_config, save_newembed_config

class NewEmbedCog(commands.Cog, name="newembed command"):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="newembed",
        description="Crear un embed personalizado y enviarlo a un canal"
    )
    async def newembed(self, ctx: discord.ApplicationContext):
        if not ctx.guild:
            embed = discord.Embed(title="❌ **ERROR**", description="Este comando solo funciona en servidores", color=0xe74c3c, timestamp=datetime.now())
            embed.set_footer(text="✨ • Lux By _.aari._")
            return await ctx.respond(embed=embed, ephemeral=True)
        
        config = load_newembed_config()
        guild_id = str(ctx.guild.id)
        
        if guild_id in config and config[guild_id].get("blocked", False):
            if not (isinstance(ctx.author, discord.Member) and ctx.author.guild_permissions.administrator):
                embed = discord.Embed(
                    title="❌ **COMANDO DESHABILITADO**",
                    description="Este servidor ha deshabilitado el comando `/newembed`",
                    color=0xe74c3c,
                    timestamp=datetime.now()
                )
                embed.set_footer(text="✨ • Lux By _.aari._")
                return await ctx.respond(embed=embed, ephemeral=True)
        else:
            if not (isinstance(ctx.author, discord.Member) and ctx.author.guild_permissions.manage_messages):
                embed = discord.Embed(
                    title="❌ **PERMISOS INSUFICIENTES**",
                    description="Necesitas permisos para gestionar mensajes",
                    color=0xe74c3c,
                    timestamp=datetime.now()
                )
                embed.set_footer(text="✨ • Lux By _.aari._")
                return await ctx.respond(embed=embed, ephemeral=True)
        
        modal = EmbedBuilderModal(self.bot)
        await ctx.send_modal(modal)

    @discord.slash_command(
        name="newembedperms",
        description="Controlar permisos del comando /newembed (solo admin)"
    )
    async def newembedperms(self, ctx: discord.ApplicationContext, permitir: bool = True):
        if not isinstance(ctx.author, discord.Member) or not ctx.author.guild_permissions.administrator:
            embed = discord.Embed(
                title="❌ **PERMISOS INSUFICIENTES**",
                description="Solo administradores pueden configurar este comando",
                color=0xe74c3c,
                timestamp=datetime.now()
            )
            embed.set_footer(text="✨ • Lux By _.aari._")
            return await ctx.respond(embed=embed, ephemeral=True)
        
        if not ctx.guild:
            embed = discord.Embed(title="❌ **ERROR**", description="Este comando solo funciona en servidores", color=0xe74c3c, timestamp=datetime.now())
            embed.set_footer(text="✨ • Lux By _.aari._")
            return await ctx.respond(embed=embed, ephemeral=True)
        
        config = load_newembed_config()
        guild_id = str(ctx.guild.id)
        
        if guild_id not in config:
            config[guild_id] = {}
        
        config[guild_id]["blocked"] = not permitir
        save_newembed_config(config)
        
        estado = "✅ Habilitado - Solo usuarios con permisos de gestionar mensajes" if permitir else "❌ Deshabilitado - Solo administradores pueden usar /newembed"
        
        embed = discord.Embed(
            title="⚙️ **CONFIGURACIÓN ACTUALIZADA**",
            description=f"Estado del comando `/newembed`: {estado}",
            color=0x3498db,
            timestamp=datetime.now()
        )
        embed.set_footer(text="✨ • Lux By _.aari._")
        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(NewEmbedCog(bot))
