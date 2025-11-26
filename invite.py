import discord
from discord.ext import commands
from datetime import datetime
from src.utils.discord_tools.invite_view import InviteView

INVITE_URL = "https://discord.com/oauth2/authorize?client_id=1410066380593692702"


class InviteCog(commands.Cog, name="invite command"):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="invite",
        description="Invitar a Lux✨ a tu servidor"
    )
    async def invite(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        
        embed = discord.Embed(
            title="🎉 **INVITAR A LUX✨**",
            description="Selecciona una opción para obtener más información",
            color=0x5865f2,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="📖 ¿Qué es Lux?",
            value="Un bot que replica las recompensas premium de Mee6",
            inline=False
        )
        
        if self.bot.user:
            embed.add_field(
                name="👤 Bot",
                value=f"{self.bot.user.mention}",
                inline=True
            )
            embed.add_field(
                name="🆔 ID",
                value=f"`{self.bot.user.id}`",
                inline=True
            )
        
        if self.bot.user and self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
        
        if self.bot.user and self.bot.user.banner:
            embed.set_image(url=self.bot.user.banner.url)
        
        embed.set_footer(text="✨ • Lux By _.aari._")
        
        view = InviteView(self.bot)
        await ctx.respond(embed=embed, view=view)


def setup(bot):
    bot.add_cog(InviteCog(bot))
