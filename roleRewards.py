import os
import discord
import json

from discord.ext import commands

class RoleRewardsCog(commands.Cog, name="roleRewards command"):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='rolerewards',
        description='Ver todas las recompensas de rol configuradas'
    )
    async def rolerewards(self, ctx: discord.ApplicationContext):
        if not ctx.guild:
            return
            
        roles_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "roles.json")
        with open(roles_path, "r") as roleFile:
            data = json.load(roleFile)
            
            if "guilds" not in data:
                data["guilds"] = {}
            
            guild_id = str(ctx.guild.id)
            guild_roles = data["guilds"].get(guild_id, [])
            levelList = [x["level"] for x in guild_roles]
        
        if not levelList:
            embed = discord.Embed(
                title="📋 **Recompensas de Rol**",
                description="No hay recompensas de rol configuradas en este servidor.\nUsa `/add` para crear una.",
                color=0x9b59b6
            )
            embed.set_image(url=self.bot.user.banner.url if self.bot.user.banner else None)
            embed.set_footer(text="✨ • Lux By _.aari._")
            return await ctx.respond(embed=embed)
        
        levelList.sort()
        embedContent = ""
        
        for levelListNumber in levelList:
            for x in guild_roles:
                if levelListNumber == x["level"]:
                    role = ctx.guild.get_role(x["id"])
                    if role:
                        embedContent += f"🎖️ Nivel **{levelListNumber}** → {role.mention}\n"
                    else:
                        embedContent += f"🎖️ Nivel **{levelListNumber}** → ID: {x['id']} (rol no encontrado)\n"

        embed = discord.Embed(
            title="📋 **Recompensas de Rol**",
            description=embedContent,
            color=0x2ecc71
        )
        embed.set_image(url=self.bot.user.banner.url if self.bot.user.banner else None)
        embed.set_footer(text="✨ • Lux By _.aari._")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(RoleRewardsCog(bot))
