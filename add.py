import os
import discord
import json

from discord.ext import commands
from discord import Option

class AddCog(commands.Cog, name="add command"):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='add',
        description='Añadir una recompensa de rol por nivel'
    )
    @discord.default_permissions(administrator=True)
    async def add(
        self, 
        ctx: discord.ApplicationContext,
        nivel: int = discord.Option(description="Número de nivel", required=True),
        rol: discord.Role = discord.Option(description="Rol a recompensar", required=True)
    ):
        try:
            if not ctx.guild:
                return
                
            roles_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "roles.json")
            
            with open(roles_path, "r") as roleFile:
                data = json.load(roleFile)
            
            if "guilds" not in data:
                data["guilds"] = {}
            
            guild_id = str(ctx.guild.id)
            if guild_id not in data["guilds"]:
                data["guilds"][guild_id] = []
            
            for x in data["guilds"][guild_id]:
                if x["level"] == nivel:
                    embed = discord.Embed(
                        title="❌ **ERROR**", 
                        description=f"El nivel **{nivel}** ya está configurado.",
                        color=0xe74c3c
                    )
                    if self.bot.user and self.bot.user.banner:
                        embed.set_image(url=self.bot.user.banner.url)
                    embed.set_footer(text="✨ • Lux By _.aari._")
                    return await ctx.respond(embed=embed, ephemeral=True)
            
            data["guilds"][guild_id].append({"level": nivel, "id": rol.id})
            
            with open(roles_path, "w") as roleFile:
                json.dump(data, roleFile, indent=4, ensure_ascii=False)
            
            embed = discord.Embed(
                title="✅ **ÉXITO**", 
                description=f"Se agregó **{rol.mention}** como recompensa del nivel **{nivel}**.",
                color=0x2ecc71
            )
            if self.bot.user and self.bot.user.banner:
                embed.set_image(url=self.bot.user.banner.url)
            embed.set_footer(text="✨ • Lux By _.aari._")
            await ctx.respond(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="⚠️ **ERROR**",
                description=f"Ocurrió un error: {str(e)[:100]}",
                color=0xe74c3c
            )
            if self.bot.user and self.bot.user.banner:
                embed.set_image(url=self.bot.user.banner.url)
            embed.set_footer(text="✨ • Lux By _.aari._")
            await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(AddCog(bot))
