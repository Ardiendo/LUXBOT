import discord
from discord import ui
import json
import os
from datetime import datetime


class StatsSelect(ui.Select):
    def __init__(self, bot, ctx):
        self.bot = bot
        self.ctx = ctx
        options = [
            discord.SelectOption(
                label="📊 Información General",
                description="Miembros, roles, canales y más",
                emoji="👥",
                value="general"
            ),
            discord.SelectOption(
                label="🏆 Recompensas de Nivel",
                description="Ver todas las recompensas configuradas",
                emoji="🎖️",
                value="rewards"
            ),
            discord.SelectOption(
                label="👤 Información del Servidor",
                description="Dueño, región, verificación y más",
                emoji="🏠",
                value="server_info"
            ),
            discord.SelectOption(
                label="📈 Estadísticas de Miembros",
                description="Actividad y distribución de miembros",
                emoji="📊",
                value="member_stats"
            ),
        ]
        super().__init__(
            placeholder="📋 Selecciona qué estadísticas ver...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        option = self.values[0]
        
        if option == "general":
            embed = discord.Embed(
                title="📊 **INFORMACIÓN GENERAL**",
                description=f"Estadísticas de **{self.ctx.guild.name}**",
                color=0x3498db,
                timestamp=datetime.now()
            )
            embed.add_field(
                name="👥 Miembros",
                value=f"**{self.ctx.guild.member_count:,}** miembros totales",
                inline=False
            )
            embed.add_field(
                name="🎭 Roles",
                value=f"**{len(self.ctx.guild.roles):,}** roles",
                inline=False
            )
            embed.add_field(
                name="📢 Canales",
                value=f"**{len(self.ctx.guild.channels):,}** canales",
                inline=False
            )
            embed.add_field(
                name="📁 Categorías",
                value=f"**{len([c for c in self.ctx.guild.channels if isinstance(c, discord.CategoryChannel)]):,}** categorías",
                inline=False
            )
            
        elif option == "rewards":
            try:
                roles_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                    "config", "roles.json"
                )
                with open(roles_path, "r") as f:
                    data = json.load(f)
                
                embed = discord.Embed(
                    title="🏆 **RECOMPENSAS DE NIVEL**",
                    description=f"Configuración de {self.ctx.guild.name}",
                    color=0x2ecc71,
                    timestamp=datetime.now()
                )
                
                if data.get("roles"):
                    rewards_text = ""
                    for reward in sorted(data["roles"], key=lambda x: x["level"]):
                        role = self.ctx.guild.get_role(reward["id"])
                        if role:
                            count = len([m for m in self.ctx.guild.members if role in m.roles])
                            rewards_text += f"**Nivel {reward['level']}** → {role.mention} (`{count}` usuarios)\n"
                        else:
                            rewards_text += f"**Nivel {reward['level']}** → ID: `{reward['id']}` (❌ Rol no encontrado)\n"
                    
                    embed.add_field(
                        name="📋 Recompensas Configuradas",
                        value=rewards_text if rewards_text else "No hay recompensas",
                        inline=False
                    )
                else:
                    embed.add_field(
                        name="📋 Recompensas",
                        value="⚠️ No hay recompensas configuradas",
                        inline=False
                    )
            except Exception as e:
                embed = discord.Embed(
                    title="❌ Error",
                    description=f"Error al cargar recompensas: {str(e)[:100]}",
                    color=0xe74c3c
                )
            
        elif option == "server_info":
            embed = discord.Embed(
                title="🏠 **INFORMACIÓN DEL SERVIDOR**",
                description=f"{self.ctx.guild.name}",
                color=0x9b59b6,
                timestamp=datetime.now()
            )
            embed.add_field(
                name="👑 Dueño",
                value=f"{self.ctx.guild.owner.mention if self.ctx.guild.owner else 'Desconocido'}",
                inline=False
            )
            embed.add_field(
                name="🌍 Región",
                value=str(self.ctx.guild.region) if hasattr(self.ctx.guild, 'region') else "No disponible",
                inline=True
            )
            embed.add_field(
                name="✅ Verificación",
                value=str(self.ctx.guild.verification_level).title(),
                inline=True
            )
            embed.add_field(
                name="📅 Creación",
                value=f"<t:{int(self.ctx.guild.created_at.timestamp())}:F>",
                inline=False
            )
            embed.add_field(
                name="🆔 ID del Servidor",
                value=f"`{self.ctx.guild.id}`",
                inline=False
            )
            
        elif option == "member_stats":
            embed = discord.Embed(
                title="📈 **ESTADÍSTICAS DE MIEMBROS**",
                description=f"{self.ctx.guild.name}",
                color=0xe74c3c,
                timestamp=datetime.now()
            )
            
            online = len([m for m in self.ctx.guild.members if m.status == discord.Status.online])
            idle = len([m for m in self.ctx.guild.members if m.status == discord.Status.idle])
            dnd = len([m for m in self.ctx.guild.members if m.status == discord.Status.dnd])
            offline = len([m for m in self.ctx.guild.members if m.status == discord.Status.offline])
            bots = len([m for m in self.ctx.guild.members if m.bot])
            
            embed.add_field(
                name="👥 Distribución",
                value=f"🟢 Online: **{online}**\n🟡 Idle: **{idle}**\n🔴 DND: **{dnd}**\n⚫ Offline: **{offline}**",
                inline=False
            )
            embed.add_field(
                name="🤖 Bots",
                value=f"**{bots}** bots en el servidor",
                inline=False
            )
            embed.add_field(
                name="👤 Usuarios",
                value=f"**{self.ctx.guild.member_count - bots}** usuarios",
                inline=False
            )
        
        if self.bot.user and self.bot.user.banner:
            embed.set_image(url=self.bot.user.banner.url)
        
        embed.set_footer(text="✨ • Lux By _.aari._")
        await interaction.response.edit_message(embed=embed)


class StatsView(ui.View):
    def __init__(self, bot, ctx):
        super().__init__(timeout=300)
        self.bot = bot
        self.ctx = ctx
        self.add_item(StatsSelect(bot, ctx))
