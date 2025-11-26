import discord
from discord.ext import commands
from src.utils.discord_tools.error_logger import log_error_to_channel
from src.utils.lux_quotes import get_error_quote

class ErrorHandlerCog(commands.Cog, name="error handler"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CommandNotFound):
            return
        
        cmd_name = ctx.command.name if ctx.command else 'Unknown'
        await log_error_to_channel(
            self.bot,
            error,
            context=f"Prefix Command: {cmd_name}",
            user=ctx.author if isinstance(ctx.author, discord.User) else None,
            guild=ctx.guild if isinstance(ctx.guild, discord.Guild) else None
        )

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: Exception):
        cmd_name = ctx.command.qualified_name if ctx.command else 'Unknown'
        await log_error_to_channel(
            self.bot,
            error,
            context=f"Slash Command: {cmd_name}",
            user=ctx.author if isinstance(ctx.author, discord.User) else None,
            guild=ctx.guild if isinstance(ctx.guild, discord.Guild) else None
        )

def setup(bot):
    bot.add_cog(ErrorHandlerCog(bot))
