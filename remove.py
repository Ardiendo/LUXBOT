import os
import discord
import json

from discord.ext import commands
from discord import Option

class RemoveCog(commands.Cog, name="remove command"):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='remove',
        description='Eliminar una recompensa de rol por nivel'
    )
    @discord.default_permissions(administrator=True)
    async def remove(
        self, 
        ctx: discord.ApplicationContext,
        nivel: int = Option(description="Número de nivel a eliminar", required=True)
    ):
        try:
            if not ctx.guild:
                return
                
            roles_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "roles.json")
            with open(roles_path, "r+") as roleFile:
                data = json.load(roleFile)
                
                if "guilds" not in data:
                    data["guilds"] = {}
                
                guild_id = str(ctx.guild.id)
                if guild_id not in data["guilds"]:
                    data["guilds"][guild_id] = []
                
                found = False
                for i, x in enumerate(data["guilds"][guild_id]):
                    if x["level"] == nivel:
                        del data["guilds"][guild_id][i]
                        found = True
                        break
                
                if not found:
                    embed = discord.Embed(
                        title="❌ **ERROR**",
                        description=f"No hay recompensa configurada para el nivel **{nivel}**.",
                        color=0xe74c3c
                    )
                    embed.set_image(url=self.bot.user.banner.url if self.bot.user.banner else None)
                    embed.set_footer(text="✨ • Lux By _.aari._")
                    return await ctx.respond(embed=embed, ephemeral=True)
                
                newdata = json.dumps(data, indent=4, ensure_ascii=False)
            
            with open(roles_path, "w") as roleFile:
                roleFile.write(newdata)
            
            embed = discord.Embed(
                title="✅ **ÉXITO**",
                description=f"Se eliminó la recompensa del nivel **{nivel}**.",
                color=0x2ecc71
            )
            embed.set_image(url=self.bot.user.banner.url if self.bot.user.banner else None)
            embed.set_footer(text="✨ • Lux By _.aari._")
            await ctx.respond(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="⚠️ **ERROR**",
                description=f"Ocurrió un error: {str(e)[:100]}",
                color=0xe74c3c
            )
            embed.set_image(url=self.bot.user.banner.url if self.bot.user.banner else None)
            embed.set_footer(text="✨ • Lux By _.aari._")
            await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(RemoveCog(bot))
