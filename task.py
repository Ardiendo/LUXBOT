import os
import discord
from discord.ext import commands, tasks
from discord.utils import get

import json
from mee6_py_api import API
from mee6_py_api.exceptions import HTTPRequestError
from math import ceil


class CogTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.updateRoles.start()

    def cog_unload(self):
        self.updateRoles.cancel()

    @tasks.loop(minutes=5)
    async def updateRoles(self):
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "configuration.json")
        with open(config_path, "r") as configFile:
            config = json.load(configFile)

        for guildId in config["updateEachTime"]:
            guild = self.bot.get_guild(guildId)
            if guild:
                try:
                    roles_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "roles.json")
                    with open(roles_path, "r") as roleFile:
                        data = json.load(roleFile)

                    if "guilds" not in data:
                        data["guilds"] = {}
                    
                    guild_id_str = str(guild.id)
                    guild_roles = data["guilds"].get(guild_id_str, [])

                    mee6API = API(guild.id)
                    pageNumber = ceil(len(guild.members)/100)
                    for i in range(pageNumber):
                        try:
                            leaderboard_page = await mee6API.levels.get_leaderboard_page(i)
                            for user in leaderboard_page["players"]:
                                if int(user["id"]) in [guildMember.id for guildMember in guild.members]:
                                    for x in guild_roles:
                                        if x["level"] <= user["level"]:
                                            if x["id"] not in [roleId for roleId in [guildMember.roles for guildMember in guild.members if guildMember.id == int(user["id"])]]:
                                                getrole = get(guild.roles, id=x["id"])
                                                member = [guildMember for guildMember in guild.members if guildMember.id == int(user["id"])]
                                                if getrole and member:
                                                    await member[0].add_roles(getrole)
                                        elif config["removePreviousRewards"] == True:
                                            if x["id"] in [roleId for roleId in [guildMember.roles for guildMember in guild.members if guildMember.id == int(user["id"])]]:
                                                getrole = get(guild.roles, id=x["id"])
                                                member = [guildMember for guildMember in guild.members if guildMember.id == int(user["id"])]
                                                if getrole and member:
                                                    await member[0].remove_roles(getrole)
                        except HTTPRequestError:
                            print(f"❌ Error al actualizar roles para {guild.name} (Guild {guildId}): Mee6 no está disponible en este servidor")
                            break
                except Exception as e:
                    print(f"❌ Error inesperado en actualización de roles para {guild.name}: {str(e)}")

    @updateRoles.before_loop
    async def before_updateRoles(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(CogTask(bot))
