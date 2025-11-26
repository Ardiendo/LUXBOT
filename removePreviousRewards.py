import os
import discord
import json

from discord.ext import commands
from discord.ext.commands import has_permissions

class RemovePreviousRewardsCog(commands.Cog, name="removePreviousRewards command"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='removepreviousrewards', aliases=["rpr", "settings"])
    @has_permissions(administrator=True)
    async def removepreviousrewards(self, ctx, trueOrFalse):
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "configuration.json")
        with open(config_path, "r") as configFile:
            data = json.load(configFile)
        
        trueOrFalse = trueOrFalse.lower()
        if trueOrFalse in ["false", "falso", "no"]:
            data["removePreviousRewards"] = False
        elif trueOrFalse in ["true", "verdadero", "si"]:
            data["removePreviousRewards"] = True   
        else:
            embed = discord.Embed(title=f"**ERROR**", description=f"El valor debe ser verdadero o falso\nSigue el ejemplo: ``{self.bot.command_prefix}removepreviousrewards <verdadero/falso>``", color=0xe00000)
            embed.set_footer(text="✨ • Lux By _.aari._")
            return await ctx.channel.send(embed=embed)

        newdata = json.dumps(data, indent=4, ensure_ascii=False)
        with open(config_path, "w") as configFile:
            configFile.write(newdata)

        embed = discord.Embed(title=f"**CONFIGURACIÓN:**", description=f"La configuración de eliminar recompensas anteriores ha sido modificada.", color=0x1eb823)
        embed.set_footer(text="✨ • Lux By _.aari._")
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(RemovePreviousRewardsCog(bot))
