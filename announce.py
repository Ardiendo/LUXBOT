import discord
from discord.ext import commands
from datetime import datetime

DEVELOPER_ID = 819080793447333918

class AnnounceCog(commands.Cog, name="announce command"):
    def __init__(self, bot):
        self.bot = bot
        self.current_announcement = None
    
    @discord.slash_command(
        name="announce",
        description="Crear y enviar anuncio global a todos los servidores (solo dev)"
    )
    async def announce(
        self, 
        ctx: discord.ApplicationContext, 
        titulo: str,
        descripcion: str,
        version: str = "1.5.1",
        color: str = "f1c40f"
    ):
        if ctx.author.id != DEVELOPER_ID:
            embed = discord.Embed(
                title="❌ **ACCESO DENEGADO**",
                description=f"Solo el desarrollador (<@{DEVELOPER_ID}>) puede usar este comando.",
                color=0xe74c3c,
                timestamp=datetime.now()
            )
            embed.set_footer(text="✨ • Lux By _.aari._")
            return await ctx.respond(embed=embed, ephemeral=True)
        
        # Convertir color hex
        try:
            color_int = int(color.replace("#", ""), 16)
        except:
            color_int = 0xf1c40f
        
        # Crear embed de anuncio
        announcement_embed = discord.Embed(
            title=f"📢 **{titulo}**",
            description=descripcion,
            color=color_int,
            timestamp=datetime.now()
        )
        announcement_embed.add_field(
            name="📌 Versión",
            value=f"v{version}",
            inline=True
        )
        if self.bot.user and self.bot.user.banner:
            announcement_embed.set_image(url=self.bot.user.banner.url)
        announcement_embed.set_footer(text="✨ • Lux By _.aari._")
        
        # Guardar anuncio actual
        self.current_announcement = announcement_embed
        
        # Enviar a todos los servidores
        sent_count = 0
        failed_count = 0
        
        for guild in self.bot.guilds:
            try:
                # Intentar enviar al primer canal de texto disponible
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        await channel.send(embed=announcement_embed)
                        sent_count += 1
                        break
                else:
                    failed_count += 1
            except Exception as e:
                failed_count += 1
                print(f"Error enviando anuncio a {guild.name}: {e}")
        
        # Confirmar envío
        confirmation = discord.Embed(
            title="📨 **ANUNCIO ENVIADO**",
            description=f"El anuncio ha sido distribuido globalmente",
            color=0x2ecc71,
            timestamp=datetime.now()
        )
        confirmation.add_field(name="✅ Exitosos", value=str(sent_count), inline=True)
        confirmation.add_field(name="❌ Fallos", value=str(failed_count), inline=True)
        confirmation.add_field(name="📌 Versión", value=f"v{version}", inline=True)
        confirmation.set_footer(text="✨ • Lux By _.aari._")
        
        await ctx.respond(embed=confirmation, ephemeral=True)
    
    @discord.slash_command(
        name="updateannounce",
        description="Actualizar el último anuncio enviado a todos los servidores (solo dev)"
    )
    async def updateannounce(
        self,
        ctx: discord.ApplicationContext,
        titulo: str | None = None,
        descripcion: str | None = None,
        version: str | None = None,
        color: str | None = None
    ):
        if ctx.author.id != DEVELOPER_ID:
            embed = discord.Embed(
                title="❌ **ACCESO DENEGADO**",
                description=f"Solo el desarrollador (<@{DEVELOPER_ID}>) puede usar este comando.",
                color=0xe74c3c,
                timestamp=datetime.now()
            )
            embed.set_footer(text="✨ • Lux By _.aari._")
            return await ctx.respond(embed=embed, ephemeral=True)
        
        if not self.current_announcement:
            embed = discord.Embed(
                title="⚠️ **SIN ANUNCIO**",
                description="No hay anuncio previo para actualizar. Crea uno primero con `/announce`",
                color=0xe67e22,
                timestamp=datetime.now()
            )
            embed.set_footer(text="✨ • Lux By _.aari._")
            return await ctx.respond(embed=embed, ephemeral=True)
        
        # Actualizar campos del embed
        if titulo:
            self.current_announcement.title = f"📢 **{titulo}**"
        if descripcion:
            self.current_announcement.description = descripcion
        if color:
            try:
                color_int = int(color.replace("#", ""), 16)
                self.current_announcement.color = color_int
            except:
                pass
        if version:
            self.current_announcement.set_field_at(
                0,
                name="📌 Versión",
                value=f"v{version}",
                inline=True
            )
        
        # Actualizar timestamp
        self.current_announcement.timestamp = datetime.now()
        
        # Enviar a todos los servidores nuevamente
        sent_count = 0
        failed_count = 0
        
        for guild in self.bot.guilds:
            try:
                for channel in guild.text_channels:
                    if channel.permissions_for(guild.me).send_messages:
                        await channel.send(embed=self.current_announcement)
                        sent_count += 1
                        break
                else:
                    failed_count += 1
            except Exception as e:
                failed_count += 1
                print(f"Error actualizando anuncio en {guild.name}: {e}")
        
        # Confirmar actualización
        confirmation = discord.Embed(
            title="📨 **ANUNCIO ACTUALIZADO**",
            description=f"El anuncio ha sido actualizado globalmente",
            color=0x2ecc71,
            timestamp=datetime.now()
        )
        confirmation.add_field(name="✅ Actualizados", value=str(sent_count), inline=True)
        confirmation.add_field(name="❌ Fallos", value=str(failed_count), inline=True)
        confirmation.set_footer(text="✨ • Lux By _.aari._")
        
        await ctx.respond(embed=confirmation, ephemeral=True)


def setup(bot):
    bot.add_cog(AnnounceCog(bot))
