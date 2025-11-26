import os
import discord
from discord.ext import commands
from discord.utils import get
from math import ceil
import json
from mee6_py_api import API
from mee6_py_api.exceptions import HTTPRequestError


class CogRankSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="leaderboard",
        description="Actualizar roles de todos los usuarios del servidor"
    )
    @discord.default_permissions(administrator=True)
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def leaderboard(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        
        if not ctx.guild:
            return
        
        try:
            roles_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "roles.json")
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "configuration.json")
            
            with open(roles_path, "r") as roleFile:
                data = json.load(roleFile)
            
            with open(config_path, "r") as configFile:
                config = json.load(configFile)

            if "guilds" not in data:
                data["guilds"] = {}
            
            guild_id_str = str(ctx.guild.id)
            guild_roles = data["guilds"].get(guild_id_str, [])

            mee6API = API(ctx.guild.id)
            pageNumber = ceil(len(ctx.guild.members)/100)
            updated = 0
            
            for i in range(pageNumber):
                try:
                    leaderboard_page = await mee6API.levels.get_leaderboard_page(i)
                    for user in leaderboard_page["players"]:
                        if int(user["id"]) in [guildMember.id for guildMember in ctx.guild.members]:
                            for x in guild_roles:
                                if x["level"] <= user["level"]:
                                    if x["id"] not in [roleId for roleId in [guildMember.roles for guildMember in ctx.guild.members if guildMember.id == int(user["id"])]]:
                                        getrole = get(ctx.guild.roles, id=x["id"])
                                        member = [guildMember for guildMember in ctx.guild.members if guildMember.id == int(user["id"])]
                                        if getrole and member:
                                            await member[0].add_roles(getrole)
                                            updated += 1
                                elif config["removePreviousRewards"] == True:
                                    if x["id"] in [roleId for roleId in [guildMember.roles for guildMember in ctx.guild.members if guildMember.id == int(user["id"])]]:
                                        getrole = get(ctx.guild.roles, id=x["id"])
                                        member = [guildMember for guildMember in ctx.guild.members if guildMember.id == int(user["id"])]
                                        if getrole and member:
                                            await member[0].remove_roles(getrole)
                except HTTPRequestError:
                    error_embed = discord.Embed(
                        title="❌ Error",
                        description="Mee6 no está disponible en este servidor. Asegúrate de que Mee6 esté instalado.",
                        color=0xe74c3c
                    )
                    error_embed.set_footer(text="✨ • Lux By _.aari._")
                    await ctx.respond(embed=error_embed)
                    return

            embed = discord.Embed(
                title="📊 **Clasificación Actualizada**",
                description=f"Se han actualizado los roles de **{updated}** usuarios.",
                color=0x2ecc71
            )
            embed.set_image(url=self.bot.user.banner.url if self.bot.user.banner else None)
            embed.set_footer(text="✨ • Lux By _.aari._")
            await ctx.respond(embed=embed)
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Error",
                description=f"Ocurrió un error: {str(e)[:100]}",
                color=0xe74c3c
            )
            error_embed.set_footer(text="✨ • Lux By _.aari._")
            await ctx.respond(embed=error_embed)


def setup(bot):
    bot.add_cog(CogRankSlash(bot))
