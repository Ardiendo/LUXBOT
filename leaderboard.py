import os
import discord
from discord.ext import commands
from discord.utils import get

import json
from mee6_py_api import API
from mee6_py_api.exceptions import HTTPRequestError
from math import ceil


class CogLeaderboardPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="leaderboard", usage="")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def leaderboard(self, ctx):
        waitMessage = await ctx.channel.send("Por favor espera mientras se actualiza...")
        
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
                                elif config["removePreviousRewards"] == True:
                                    if x["id"] in [roleId for roleId in [guildMember.roles for guildMember in ctx.guild.members if guildMember.id == int(user["id"])]]:
                                        getrole = get(ctx.guild.roles, id=x["id"])
                                        member = [guildMember for guildMember in ctx.guild.members if guildMember.id == int(user["id"])]
                                        if getrole and member:
                                            await member[0].remove_roles(getrole)
                except HTTPRequestError:
                    await waitMessage.delete()
                    error_embed = discord.Embed(
                        title="❌ Error",
                        description="Mee6 no está disponible en este servidor o no se encontraron datos.",
                        color=0xe74c3c
                    )
                    error_embed.set_footer(text="✨ • Lux By _.aari._")
                    await ctx.channel.send(embed=error_embed)
                    return
            
            await waitMessage.delete()
            embed = discord.Embed(title=f"**CLASIFICACIÓN:**", description=f"Todos los usuarios han sido actualizados.", color=0x1eb823)
            embed.set_footer(text="✨ • Lux By _.aari._")
            await ctx.channel.send(embed=embed)
        except Exception as e:
            try:
                await waitMessage.delete()
            except:
                pass
            error_embed = discord.Embed(
                title="❌ Error",
                description=f"Ocurrió un error: {str(e)[:100]}",
                color=0xe74c3c
            )
            error_embed.set_footer(text="✨ • Lux By _.aari._")
            await ctx.channel.send(embed=error_embed)


def setup(bot):
    bot.add_cog(CogLeaderboardPrefix(bot))
