import os
import discord
import json

from discord.ext import commands
from discord.utils import get

from datetime import datetime
from mee6_py_api import API


class OnMessageCog(commands.Cog, name="on message"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Agregar XP a usuario
        try:
            from src.cogs.economy.storage import can_gain_xp, add_xp
            if can_gain_xp(message.author.id):
                xp_result = add_xp(message.author.id, 10)
                if xp_result.get("level_up"):
                    try:
                        level_up_embed = discord.Embed(
                            title=f"🎉 **LEVEL UP!**",
                            description=f"¡{message.author.mention} ha subido a nivel {xp_result['level']}!",
                            color=0xf1c40f
                        )
                        level_up_embed.add_field(name="⭐ Nivel", value=str(xp_result["level"]), inline=True)
                        level_up_embed.add_field(name="💫 XP Total", value=str(xp_result["total_xp"]), inline=True)
                        level_up_embed.set_footer(text="✨ • Lux By _.aari._")
                        await message.channel.send(embed=level_up_embed, delete_after=10)
                    except:
                        pass
        except:
            pass

        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "configuration.json")
        with open(config_path, "r") as configFile:
            config = json.load(configFile)

        if config["updateEachMessage"]:
            guild_id = message.guild.id
            mee6API = API(guild_id)
            
            user_id = message.author.id
            try:
                userLevel = await mee6API.levels.get_user_level(user_id)
            except Exception:
                return

            if userLevel is None:
                date = datetime.now().strftime("%x %X")
                return print(f"{date} La búsqueda del nivel del jugador ha fallado.")

            old_level = None
            if hasattr(self.bot, 'db') and self.bot.db.pool:
                cached = await self.bot.db.get_cached_level(guild_id, user_id)
                if cached:
                    old_level = cached.get('level')
                await self.bot.db.update_cached_level(guild_id, user_id, userLevel)

            roles_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "roles.json")
            with open(roles_path, "r") as roleFile:
                data = json.load(roleFile)
            
            if "guilds" not in data:
                data["guilds"] = {}
            
            guild_id_str = str(guild_id)
            guild_roles = data["guilds"].get(guild_id_str, [])
            
            level_up_role = None
            for x in guild_roles:
                if x["level"] <= userLevel:
                    if x["id"] not in [y.id for y in message.author.roles]:
                        getrole = get(message.guild.roles, id=x["id"])
                        if getrole:
                            await message.author.add_roles(getrole)
                            level_up_role = getrole
                            
                            if hasattr(self.bot, 'db') and self.bot.db.pool:
                                await self.bot.db.log_role_action(
                                    guild_id, user_id, x["id"], "add", x["level"]
                                )
                            
                            try:
                                log_embed = discord.Embed(
                                    title="✅ **Rol Asignado**",
                                    description=f"{message.author.mention} obtuvo {getrole.mention}",
                                    color=0x2ecc71,
                                    timestamp=datetime.now()
                                )
                                log_embed.add_field(name="Nivel", value=str(x["level"]), inline=True)
                                log_embed.set_footer(text="✨ • Lux By _.aari._")
                            except:
                                pass

                        if config["removePreviousRewards"]:
                            for userRole in message.author.roles:
                                if (userRole.id in [roleReward["id"] for roleReward in guild_roles]) and userRole.id != x["id"]:
                                    await message.author.remove_roles(userRole)
                                    
                                    if hasattr(self.bot, 'db') and self.bot.db.pool:
                                        await self.bot.db.log_role_action(
                                            guild_id, user_id, userRole.id, "remove"
                                        )

            # Notificación de subida de nivel (función simplificada)
            if old_level and old_level < userLevel and level_up_role:
                try:
                    notif_embed = discord.Embed(
                        title="🎉 **¡LEVEL UP!**",
                        description=f"{message.author.mention} ha subido de nivel",
                        color=0xf1c40f,
                        timestamp=datetime.now()
                    )
                    notif_embed.add_field(name="📊 Nivel Anterior", value=str(old_level), inline=True)
                    notif_embed.add_field(name="⭐ Nivel Nuevo", value=str(userLevel), inline=True)
                    notif_embed.add_field(name="🎖️ Rol", value=level_up_role.mention, inline=True)
                    notif_embed.set_footer(text="✨ • Lux By _.aari._")
                except:
                    pass

def setup(bot):
    bot.add_cog(OnMessageCog(bot))
