import discord
from discord.ext import commands
from discord import ui
from datetime import datetime
from discord.utils import utcnow
import os
import json


class UserInfoSelect(ui.Select):
    def __init__(self, user: discord.User, member: discord.Member, bot):
        self.user = user
        self.member = member
        self.bot = bot
        
        options = [
            discord.SelectOption(
                label="📋 Perfil",
                value="profile",
                emoji="📋",
                description="Información básica del usuario"
            ),
            discord.SelectOption(
                label="📊 Estadísticas",
                value="stats",
                emoji="📊",
                description="XP, nivel y datos de juego"
            ),
            discord.SelectOption(
                label="👑 Roles",
                value="roles",
                emoji="👑",
                description="Roles en el servidor"
            ),
            discord.SelectOption(
                label="💰 Economía",
                value="economy",
                emoji="💰",
                description="Balance, items e inventario"
            ),
            discord.SelectOption(
                label="🎫 Tickets",
                value="tickets",
                emoji="🎫",
                description="Historial de tickets"
            ),
            discord.SelectOption(
                label="🏆 Logros",
                value="achievements",
                emoji="🏆",
                description="Badges y logros especiales"
            ),
        ]
        
        super().__init__(
            placeholder="Selecciona qué información ver...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        view_type = self.values[0]
        
        if view_type == "profile":
            embed = self.get_profile_embed()
        elif view_type == "stats":
            embed = self.get_stats_embed()
        elif view_type == "roles":
            embed = self.get_roles_embed()
        elif view_type == "economy":
            embed = self.get_economy_embed()
        elif view_type == "tickets":
            embed = self.get_tickets_embed()
        elif view_type == "achievements":
            embed = self.get_achievements_embed()
        else:
            embed = self.get_profile_embed()
        
        try:
            await interaction.followup.send(embed=embed, ephemeral=True)
        except discord.NotFound:
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    def get_profile_embed(self) -> discord.Embed:
        try:
            embed = discord.Embed(
                title=f"📋 **Perfil de {self.user.name}**",
                color=0x3498db,
                timestamp=utcnow()
            )
            
            embed.add_field(
                name="👤 Nombre de Usuario",
                value=f"{self.user.mention}\n`{self.user.name}#{self.user.discriminator}`",
                inline=False
            )
            embed.add_field(
                name="🆔 ID de Usuario",
                value=f"`{self.user.id}`",
                inline=True
            )
            embed.add_field(
                name="📅 Cuenta Creada",
                value=f"<t:{int(self.user.created_at.timestamp())}:R>",
                inline=True
            )
            
            if self.member:
                embed.add_field(
                    name="🔗 Se unió al Servidor",
                    value=f"<t:{int(self.member.joined_at.timestamp())}:R>",
                    inline=True
                )
                days_in_server = (utcnow() - self.member.joined_at).days
                embed.add_field(
                    name="⏱️ Antigüedad",
                    value=f"{days_in_server} días",
                    inline=True
                )
            
            embed.add_field(
                name="🤖 Tipo",
                value="Bot" if self.user.bot else "Usuario",
                inline=True
            )
            
            embed.add_field(
                name="✅ Verificado",
                value="Sí" if self.user.system else "No",
                inline=True
            )
            
            if self.user.avatar:
                embed.set_thumbnail(url=self.user.avatar.url)
            
            embed.set_footer(text="✨ • Lux By _.aari._")
            return embed
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"No se pudo cargar el perfil: {str(e)[:100]}",
                color=0xe74c3c
            )
            embed.set_footer(text="✨ • Lux By _.aari._")
            return embed
    
    def get_stats_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=f"📊 **Estadísticas de {self.user.name}**",
            description="Datos de actividad y progresión",
            color=0xf39c12,
            timestamp=utcnow()
        )
        
        try:
            from src.cogs.economy.storage import get_user_xp, get_user_balance
            
            xp_data = get_user_xp(self.user.id)
            level = xp_data.get("level", 0)
            total_xp = xp_data.get("total_xp", 0)
            level_xp = xp_data.get("level_xp", 0)
            
            embed.add_field(
                name="⭐ Nivel",
                value=str(level),
                inline=True
            )
            embed.add_field(
                name="💫 XP Total",
                value=f"{total_xp:,}",
                inline=True
            )
            embed.add_field(
                name="🎯 XP Este Nivel",
                value=f"{level_xp}",
                inline=True
            )
            
            # Calcular progreso
            next_level_xp = (level + 1) * 100
            progress = int((level_xp / next_level_xp) * 10)
            bar = "█" * progress + "░" * (10 - progress)
            embed.add_field(
                name="📈 Progreso",
                value=f"`{bar}` {progress * 10}%",
                inline=False
            )
            
        except:
            embed.add_field(
                name="❌ Error",
                value="No se pudo cargar el sistema de economía",
                inline=False
            )
        
        embed.set_footer(text="✨ • Lux By _.aari._")
        return embed
    
    def get_roles_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=f"👑 **Roles de {self.user.name}**",
            description="Roles en este servidor",
            color=0x9b59b6,
            timestamp=utcnow()
        )
        
        if not self.member:
            embed.description = "Este usuario no está en el servidor"
            embed.set_footer(text="✨ • Lux By _.aari._")
            return embed
        
        if not self.member.roles[1:]:
            embed.add_field(
                name="Sin Roles",
                value="Este usuario no tiene roles asignados",
                inline=False
            )
        else:
            roles_list = ", ".join([role.mention for role in self.member.roles[1:]])
            embed.add_field(
                name=f"Total: {len(self.member.roles) - 1} rol(es)",
                value=roles_list[:1024],
                inline=False
            )
        
        if self.member.top_role != self.member.guild.default_role:
            embed.add_field(
                name="👑 Rol Más Alto",
                value=self.member.top_role.mention,
                inline=True
            )
        
        embed.add_field(
            name="🎖️ Color del Rol",
            value=f"{self.member.color}" if self.member.color else "Sin color",
            inline=True
        )
        
        embed.set_footer(text="✨ • Lux By _.aari._")
        return embed
    
    def get_economy_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=f"💰 **Economía de {self.user.name}**",
            description="Balance e inventario",
            color=0x2ecc71,
            timestamp=utcnow()
        )
        
        try:
            from src.cogs.economy.storage import get_user_balance, get_user_inventory
            
            balance = get_user_balance(self.user.id)
            inventory = get_user_inventory(self.user.id)
            
            embed.add_field(
                name="💵 Balance",
                value=f"{balance:,} coins 🪙",
                inline=True
            )
            embed.add_field(
                name="🎁 Items",
                value=str(len(inventory)),
                inline=True
            )
            
            if inventory:
                items_text = ""
                for item_id, count in list(inventory.items())[:5]:
                    items_text += f"• {item_id}: **{count}x**\n"
                
                if len(inventory) > 5:
                    items_text += f"... y {len(inventory) - 5} más"
                
                embed.add_field(
                    name="📦 Inventario (Top 5)",
                    value=items_text,
                    inline=False
                )
            else:
                embed.add_field(
                    name="📦 Inventario",
                    value="Vacío",
                    inline=False
                )
            
        except:
            embed.add_field(
                name="❌ Error",
                value="No se pudo cargar los datos de economía",
                inline=False
            )
        
        embed.set_footer(text="✨ • Lux By _.aari._")
        return embed
    
    def get_achievements_embed(self) -> discord.Embed:
        try:
            embed = discord.Embed(
                title=f"🏆 **Logros de {self.user.name}**",
                description="Badges y reconocimientos especiales",
                color=0xf1c40f,
                timestamp=utcnow()
            )
            achievements = []

            # Badge de antigüedad
            if self.member:
                days_in_server = (utcnow() - self.member.joined_at).days
                if days_in_server >= 30:
                    achievements.append("🎖️ **Miembro Veterano** - En el servidor 30+ días")

            # Badge de nivel
            try:
                from src.cogs.economy.storage import get_user_xp
                xp_data = get_user_xp(self.user.id)
                level = xp_data.get("level", 0)
                if level >= 10:
                    achievements.append(f"⭐ **Nivel {level}** - Alcanzó nivel {level}")
                if level >= 25:
                    achievements.append("💫 **Progresista** - Alcanzó nivel 25+")
                if level >= 50:
                    achievements.append("✨ **Leyenda** - Alcanzó nivel 50+")
            except Exception:
                pass

            # Badge de roles
            if self.member and len(self.member.roles) > 5:
                achievements.append(f"👑 **Coleccionista de Roles** - Tiene {len(self.member.roles) - 1} roles")
            # Badge de verificación
            if not self.user.bot:
                achievements.append("✅ **Miembro Verificado** - Usuario real de Discord")

            if achievements:
                for achievement in achievements:
                    embed.add_field(
                        name="🏅",
                        value=achievement,
                        inline=False
                    )
            else:
                embed.add_field(
                    name="🎯 Próximos Logros",
                    value="Continúa siendo activo para desbloquear logros especiales",
                    inline=False
                )

            embed.set_footer(text="✨ • Lux By _.aari._")
            return embed
        except Exception as e:
            embed = discord.Embed(
                title="❌ Error",
                description=f"No se pudieron cargar los logros: {str(e)[:100]}",
                color=0xe74c3c
            )
            embed.set_footer(text="✨ • Lux By _.aari._")
            return embed


class UserInfoView(ui.View):
    def __init__(self, user: discord.User, member: discord.Member, bot):
        super().__init__()
        self.add_item(UserInfoSelect(user, member, bot))


class UserInfoCog(commands.Cog, name="userinfo command"):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command(
        name="userinfo",
        description="Ver información detallada de un usuario"
    )
    async def userinfo(self, ctx: discord.ApplicationContext, usuario: discord.User = None):
        """Muestra información detallada de un usuario con opciones interactivas"""
        
        if usuario is None:
            usuario = ctx.author
        
        # Obtener miembro si está en el servidor
        member = None
        if ctx.guild:
            member = ctx.guild.get_member(usuario.id)
        
        # Embed principal
        main_embed = discord.Embed(
            title=f"👤 **Información de {usuario.name}**",
            description="Selecciona qué información deseas ver",
            color=0x3498db,
            timestamp=utcnow()
        )
        
        main_embed.add_field(
            name="📋 Opciones Disponibles",
            value="Usa el menú desplegable de abajo para explorar:",
            inline=False
        )
        main_embed.add_field(
            name="📋 Perfil",
            value="Información básica y fechas importantes",
            inline=True
        )
        main_embed.add_field(
            name="📊 Estadísticas",
            value="Nivel, XP y progresión",
            inline=True
        )
        main_embed.add_field(
            name="👑 Roles",
            value="Roles del servidor",
            inline=True
        )
        main_embed.add_field(
            name="💰 Economía",
            value="Balance e inventario",
            inline=True
        )
        main_embed.add_field(
            name="🎫 Tickets",
            value="Historial de tickets",
            inline=True
        )
        main_embed.add_field(
            name="🏆 Logros",
            value="Badges y reconocimientos",
            inline=True
        )
        
        if usuario.avatar:
            main_embed.set_thumbnail(url=usuario.avatar.url)
        
        main_embed.set_footer(text="✨ • Lux By _.aari._")
        
        view = UserInfoView(usuario, member, self.bot)
        await ctx.respond(embed=main_embed, view=view, ephemeral=False)


def setup(bot):
    bot.add_cog(UserInfoCog(bot))
