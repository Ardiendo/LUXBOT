import os
import discord
import random 
import asyncio
import time
import os
import datetime

from datetime import datetime
from discord.ext import commands
from discord.ext.commands import MissingPermissions

class EventsCog(commands.Cog, name="EventsCog"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            jour = round(error.retry_after/86400)
            heure = round(error.retry_after/3600)
            minute = round(error.retry_after/60)
            if jour > 0:
                await ctx.send('Este comando tiene un tiempo de espera, debes esperar '+str(jour)+ " día(s)")
            elif heure > 0:
                await ctx.send('Este comando tiene un tiempo de espera, debes esperar '+str(heure)+ " hora(s)")
            elif minute > 0:
                await ctx.send('Este comando tiene un tiempo de espera, debes esperar '+ str(minute)+" minuto(s)")
            else:
                await ctx.send(f'Este comando tiene un tiempo de espera, debes esperar {error.retry_after:.2f} segundo(s)')
        if isinstance(error, MissingPermissions):
            await ctx.send("No tienes permisos para usar este comando.")
        else:
            print(error)

def setup(bot):
    bot.add_cog(EventsCog(bot))
