import discord
from discord import ui
from datetime import datetime

INVITE_URL = "https://discord.com/oauth2/authorize?client_id=1410066380593692702"

class InviteSelect(ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(
                label="🔗 Link de Invitación",
                description="Obtén el link para invitar a Lux a tu servidor",
                emoji="🎉",
                value="invite_link"
            ),
            discord.SelectOption(
                label="ℹ️ Información del Bot",
                description="Información sobre Lux✨",
                emoji="📖",
                value="bot_info"
            ),
        ]
        super().__init__(
            placeholder="📋 Selecciona una opción...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        option = self.values[0]
        
        if option == "invite_link":
            embed = discord.Embed(
                title="🎉 **INVITAR A LUX✨**",
                description="Haz clic en el botón de abajo para invitar a Lux a tu servidor",
                color=0x5865f2,
                timestamp=datetime.now()
            )
            embed.add_field(
                name="🔗 Link de Invitación",
                value=INVITE_URL,
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
            
            view = discord.ui.View()
            view.add_item(discord.ui.Button(
                label="Invitar a Lux",
                style=discord.ButtonStyle.link,
                url=INVITE_URL,
                emoji="🎉"
            ))
            
            await interaction.response.edit_message(embed=embed, view=view)
            
        elif option == "bot_info":
            embed = discord.Embed(
                title="ℹ️ **INFORMACIÓN DE LUX✨**",
                description="Tu bot de recompensas de rol basado en Mee6",
                color=0x9b59b6,
                timestamp=datetime.now()
            )
            embed.add_field(
                name="🎯 Objetivo",
                value="Replicar las recompensas premium de Mee6 de forma gratuita",
                inline=False
            )
            embed.add_field(
                name="✨ Características",
                value="🎖️ Recompensas automáticas\n📊 Estadísticas\n💾 Backup/Restore\n🔔 Notificaciones\n📝 Logs",
                inline=False
            )
            embed.add_field(
                name="👨‍💻 Creador",
                value="_.aari._",
                inline=True
            )
            embed.add_field(
                name="🔧 Framework",
                value="py-cord 2.6.1",
                inline=True
            )
            
            if self.bot.user and self.bot.user.banner:
                embed.set_image(url=self.bot.user.banner.url)
            
            embed.set_footer(text="✨ • Lux By _.aari._")
            await interaction.response.edit_message(embed=embed, view=None)


class InviteView(ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        self.add_item(InviteSelect(bot))
