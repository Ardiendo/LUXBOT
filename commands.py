import discord
from discord.ext import commands
from datetime import datetime
from src.cogs.tickets.storage import set_ticket_channel, get_ticket_channel, load_tickets_data
from src.cogs.tickets.views import CreateTicketView
from src.utils.lux_emojis import SPARKLE_EMOJIS, PRESETS

class TicketCommandsCog(commands.Cog, name="tickets commands"):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command(name="ticketsetup", description="Configurar el canal de tickets del servidor")
    async def ticketsetup(self, ctx: discord.ApplicationContext, channel: discord.TextChannel):
        """Configura el canal donde aparecerá el botón de crear tickets"""
        try:
            if not isinstance(ctx.author, discord.Member) or not ctx.author.guild_permissions.administrator:
                await ctx.respond("❌ Solo administradores pueden usar este comando", ephemeral=True)
                return
            
            guild = ctx.guild
            if not guild:
                return
            
            set_ticket_channel(guild.id, channel.id)
            
            embed = discord.Embed(
                title="🎫 **SISTEMA DE TICKETS**",
                description="Haz click en el botón de abajo para abrir un nuevo ticket y resolver tu problema",
                color=0x3498db,
                timestamp=datetime.now()
            )
            embed.add_field(
                name="📋 ¿Cómo funcionan los tickets?",
                value="1️⃣ Haz click en 'Abrir Ticket'\n2️⃣ Describe tu problema\n3️⃣ El staff te ayudará en un canal privado\n4️⃣ Cierra el ticket cuando termine",
                inline=False
            )
            embed.set_image(url="https://media.giphy.com/media/l0HlzJRVWGVGvlA1G/giphy.gif")
            embed.set_footer(text=f"✨ • Lux By _.aari._ {PRESETS['light_mage']}")
            
            view = CreateTicketView()
            await channel.send(embed=embed, view=view)
            
            response = discord.Embed(
                title="✅ **TICKETS CONFIGURADOS**",
                description=f"Sistema de tickets activado en {channel.mention}",
                color=0x00ff00,
                timestamp=datetime.now()
            )
            response.set_footer(text=f"✨ • Lux By _.aari._")
            await ctx.respond(embed=response)
        except Exception as e:
            print(f"❌ Error en ticketsetup: {e}")
            await ctx.respond(f"❌ Error: {str(e)}", ephemeral=True)
    
    @discord.slash_command(name="ticketstats", description="Ver estadísticas de tickets")
    async def ticketstats(self, ctx: discord.ApplicationContext):
        """Muestra estadísticas de tickets del servidor"""
        try:
            if not isinstance(ctx.author, discord.Member) or not ctx.author.guild_permissions.administrator:
                await ctx.respond("❌ Solo administradores pueden usar este comando", ephemeral=True)
                return
            
            guild = ctx.guild
            if not guild:
                return
            
            data = load_tickets_data()
            tickets = [t for t in data["tickets"] if t["guild_id"] == guild.id]
            
            total = len(tickets)
            open_tickets = len([t for t in tickets if t["status"] == "open"])
            closed_tickets = len([t for t in tickets if t["status"] == "closed"])
            
            embed = discord.Embed(
                title="📊 **ESTADÍSTICAS DE TICKETS**",
                description=f"Estadísticas del servidor {guild.name}",
                color=0x9b59b6,
                timestamp=datetime.now()
            )
            embed.add_field(name="📈 Total de Tickets", value=f"`{total}`", inline=True)
            embed.add_field(name="🟢 Abiertos", value=f"`{open_tickets}`", inline=True)
            embed.add_field(name="🔴 Cerrados", value=f"`{closed_tickets}`", inline=True)
            
            if tickets:
                embed.add_field(
                    name="📋 Últimos Tickets",
                    value="\n".join([f"**#{t['ticket_id']}** - {t['reason'][:30] if len(t['reason']) > 30 else t['reason']}{'...' if len(t['reason']) > 30 else ''}" for t in tickets[-5:]]),
                    inline=False
                )
            
            embed.set_footer(text=f"✨ • Lux By _.aari._")
            await ctx.respond(embed=embed)
        except Exception as e:
            print(f"❌ Error en ticketstats: {e}")
            await ctx.respond(f"❌ Error: {str(e)}", ephemeral=True)

def setup(bot):
    bot.add_cog(TicketCommandsCog(bot))
