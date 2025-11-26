import discord
from discord import ui
from datetime import datetime, timedelta, timezone

class ModActionSelect(ui.Select):
    def __init__(self, target_user: discord.Member, moderator: discord.User | discord.Member, razon: str = "Sin razón especificada"):
        self.target_user = target_user
        self.moderator = moderator
        self.razon = razon
        
        options = [
            discord.SelectOption(
                label="🚪 Kick",
                description="Expulsar al usuario del servidor",
                emoji="👢",
                value="kick"
            ),
            discord.SelectOption(
                label="🔨 Ban",
                description="Banear permanentemente al usuario",
                emoji="⛔",
                value="ban"
            ),
            discord.SelectOption(
                label="⚠️ Warn",
                description="Advertir al usuario",
                emoji="📋",
                value="warn"
            ),
            discord.SelectOption(
                label="🔇 Mute",
                description="Silenciar al usuario temporalmente",
                emoji="🤐",
                value="mute"
            ),
            discord.SelectOption(
                label="🔓 Unban",
                description="Remover ban del usuario",
                emoji="✅",
                value="unban"
            ),
            discord.SelectOption(
                label="🔊 Unmute",
                description="Remover silencio del usuario",
                emoji="🎤",
                value="unmute"
            ),
            discord.SelectOption(
                label="❌ Remover Warn",
                description="Remover advertencia del usuario",
                emoji="🗑️",
                value="remove_warn"
            ),
            discord.SelectOption(
                label="📝 Cambiar Apodo",
                description="Cambiar el apodo del usuario",
                emoji="✏️",
                value="nickname"
            ),
            discord.SelectOption(
                label="👑 Crear Rol",
                description="Crear un nuevo rol en el servidor",
                emoji="🆕",
                value="create_role"
            ),
            discord.SelectOption(
                label="🗑️ Eliminar Rol",
                description="Eliminar un rol del servidor",
                emoji="❌",
                value="delete_role"
            ),
        ]
        super().__init__(
            placeholder="📋 Selecciona una acción de moderación...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        action = self.values[0]
        guild = interaction.guild
        
        if action == "kick":
            try:
                await self.target_user.kick(reason=f"Moderación por {interaction.user} - Razón: {self.razon}")
                embed = discord.Embed(
                    title="👢 **USUARIO EXPULSADO**",
                    description=f"{self.target_user.mention} ha sido expulsado del servidor",
                    color=0xff9800,
                    timestamp=datetime.now()
                )
                embed.add_field(name="👤 Usuario", value=f"{self.target_user}", inline=True)
                embed.add_field(name="👮 Moderador", value=f"{interaction.user}", inline=True)
                embed.add_field(name="📝 Acción", value="Kick", inline=True)
                embed.add_field(name="📋 Razón", value=self.razon, inline=False)
                embed.set_footer(text="✨ • Lux By _.aari._")
                await interaction.response.edit_message(embed=embed, view=None)
            except Exception as e:
                embed = discord.Embed(
                    title="❌ **ERROR**",
                    description=f"No se pudo expulsar al usuario: {str(e)[:100]}",
                    color=0xe74c3c,
                    timestamp=datetime.now()
                )
                embed.set_footer(text="✨ • Lux By _.aari._")
                await interaction.response.edit_message(embed=embed, view=None)
        
        elif action == "ban":
            try:
                if guild and guild.me:
                    await guild.ban(self.target_user, reason=f"Moderación por {interaction.user} - Razón: {self.razon}")
                embed = discord.Embed(
                    title="⛔ **USUARIO BANEADO**",
                    description=f"{self.target_user.mention} ha sido baneado del servidor",
                    color=0xe74c3c,
                    timestamp=datetime.now()
                )
                embed.add_field(name="👤 Usuario", value=f"{self.target_user}", inline=True)
                embed.add_field(name="👮 Moderador", value=f"{interaction.user}", inline=True)
                embed.add_field(name="📝 Acción", value="Ban", inline=True)
                embed.add_field(name="📋 Razón", value=self.razon, inline=False)
                embed.set_footer(text="✨ • Lux By _.aari._")
                await interaction.response.edit_message(embed=embed, view=None)
            except Exception as e:
                embed = discord.Embed(
                    title="❌ **ERROR**",
                    description=f"No se pudo banear al usuario: {str(e)[:100]}",
                    color=0xe74c3c,
                    timestamp=datetime.now()
                )
                embed.set_footer(text="✨ • Lux By _.aari._")
                await interaction.response.edit_message(embed=embed, view=None)
        
        elif action == "warn":
            embed = discord.Embed(
                title="⚠️ **ADVERTENCIA REGISTRADA**",
                description=f"{self.target_user.mention} ha recibido una advertencia",
                color=0xf39c12,
                timestamp=datetime.now()
            )
            embed.add_field(name="👤 Usuario", value=f"{self.target_user}", inline=True)
            embed.add_field(name="👮 Moderador", value=f"{interaction.user}", inline=True)
            embed.add_field(name="📝 Acción", value="Warn", inline=True)
            embed.add_field(name="📋 Razón", value=self.razon, inline=False)
            embed.set_footer(text="✨ • Lux By _.aari._")
            await interaction.response.edit_message(embed=embed, view=None)
        
        elif action == "mute":
            if interaction.user and isinstance(interaction.user, discord.Member):
                embed = discord.Embed(
                    title="🔇 **SELECCIONA DURACIÓN**",
                    description=f"¿Por cuánto tiempo quieres silenciar a {self.target_user.mention}?",
                    color=0x3498db,
                    timestamp=datetime.now()
                )
                embed.add_field(name="📋 Razón", value=self.razon, inline=False)
                embed.set_footer(text="✨ • Lux By _.aari._")
                view = MuteDurationView(self.target_user, interaction.user, self.razon)
                await interaction.response.edit_message(embed=embed, view=view)
        
        elif action == "unban":
            try:
                if not guild:
                    embed = discord.Embed(title="❌ **ERROR**", description="No se pudo obtener el servidor", color=0xe74c3c)
                    embed.set_footer(text="✨ • Lux By _.aari._")
                    return await interaction.response.edit_message(embed=embed, view=None)
                
                # Verificar si el usuario está baneado
                try:
                    bans = await guild.bans()
                    is_banned = any(ban_entry.user.id == self.target_user.id for ban_entry in bans)
                    if not is_banned:
                        embed = discord.Embed(
                            title="❌ **NO ESTÁ BANEADO**",
                            description=f"{self.target_user.mention} no está baneado del servidor",
                            color=0xe74c3c,
                            timestamp=datetime.now()
                        )
                        embed.set_footer(text="✨ • Lux By _.aari._")
                        return await interaction.response.edit_message(embed=embed, view=None)
                except Exception as e:
                    print(f"Error al verificar bans: {e}")
                
                await guild.unban(self.target_user, reason=f"Revocación por {interaction.user} - Razón: {self.razon}")
                embed = discord.Embed(
                    title="✅ **BAN REMOVIDO**",
                    description=f"El ban de {self.target_user.mention} ha sido removido",
                    color=0x2ecc71,
                    timestamp=datetime.now()
                )
                embed.add_field(name="👤 Usuario", value=f"{self.target_user}", inline=True)
                embed.add_field(name="👮 Moderador", value=f"{interaction.user}", inline=True)
                embed.add_field(name="📝 Acción", value="Unban", inline=True)
                embed.add_field(name="📋 Razón", value=self.razon, inline=False)
                embed.set_footer(text="✨ • Lux By _.aari._")
                await interaction.response.edit_message(embed=embed, view=None)
            except Exception as e:
                embed = discord.Embed(
                    title="❌ **ERROR**",
                    description=f"No se pudo remover el ban: {str(e)[:100]}",
                    color=0xe74c3c,
                    timestamp=datetime.now()
                )
                embed.set_footer(text="✨ • Lux By _.aari._")
                await interaction.response.edit_message(embed=embed, view=None)
        
        elif action == "unmute":
            try:
                # Verificar si el usuario está muteado
                if self.target_user.timed_out_until is None or self.target_user.timed_out_until <= datetime.now(timezone.utc):
                    embed = discord.Embed(
                        title="❌ **NO ESTÁ MUTEADO**",
                        description=f"{self.target_user.mention} no está muteado en el servidor",
                        color=0xe74c3c,
                        timestamp=datetime.now()
                    )
                    embed.set_footer(text="✨ • Lux By _.aari._")
                    return await interaction.response.edit_message(embed=embed, view=None)
                
                await self.target_user.timeout(None, reason=f"Revocación por {interaction.user} - Razón: {self.razon}")
                embed = discord.Embed(
                    title="🔊 **SILENCIO REMOVIDO**",
                    description=f"{self.target_user.mention} ha sido desilenciado",
                    color=0x2ecc71,
                    timestamp=datetime.now()
                )
                embed.add_field(name="👤 Usuario", value=f"{self.target_user}", inline=True)
                embed.add_field(name="👮 Moderador", value=f"{interaction.user}", inline=True)
                embed.add_field(name="📝 Acción", value="Unmute", inline=True)
                embed.add_field(name="📋 Razón", value=self.razon, inline=False)
                embed.set_footer(text="✨ • Lux By _.aari._")
                await interaction.response.edit_message(embed=embed, view=None)
            except Exception as e:
                embed = discord.Embed(
                    title="❌ **ERROR**",
                    description=f"No se pudo remover el silencio: {str(e)[:100]}",
                    color=0xe74c3c,
                    timestamp=datetime.now()
                )
                embed.set_footer(text="✨ • Lux By _.aari._")
                await interaction.response.edit_message(embed=embed, view=None)
        
        elif action == "remove_warn":
            embed = discord.Embed(
                title="❌ **ADVERTENCIA REMOVIDA**",
                description=f"La advertencia de {self.target_user.mention} ha sido removida",
                color=0x2ecc71,
                timestamp=datetime.now()
            )
            embed.add_field(name="👤 Usuario", value=f"{self.target_user}", inline=True)
            embed.add_field(name="👮 Moderador", value=f"{interaction.user}", inline=True)
            embed.add_field(name="📝 Acción", value="Remove Warn", inline=True)
            embed.add_field(name="📋 Razón", value=self.razon, inline=False)
            embed.set_footer(text="✨ • Lux By _.aari._")
            await interaction.response.edit_message(embed=embed, view=None)
        
        elif action == "nickname":
            if not guild or not guild.me:
                embed = discord.Embed(title="❌ **ERROR**", description="No puedo acceder al servidor", color=0xe74c3c)
                embed.set_footer(text="✨ • Lux By _.aari._")
                return await interaction.response.edit_message(embed=embed, view=None)
            
            if not guild.me.guild_permissions.manage_nicknames:
                embed = discord.Embed(
                    title="❌ **PERMISOS INSUFICIENTES**",
                    description="No tengo permiso para cambiar apodos",
                    color=0xe74c3c,
                    timestamp=datetime.now()
                )
                embed.set_footer(text="✨ • Lux By _.aari._")
                return await interaction.response.edit_message(embed=embed, view=None)
            
            if isinstance(interaction.user, discord.Member) and not interaction.user.guild_permissions.manage_nicknames:
                embed = discord.Embed(
                    title="❌ **PERMISOS INSUFICIENTES**",
                    description="No tienes permiso para cambiar apodos",
                    color=0xe74c3c,
                    timestamp=datetime.now()
                )
                embed.set_footer(text="✨ • Lux By _.aari._")
                return await interaction.response.edit_message(embed=embed, view=None)
            
            modal = NicknameModal(self.target_user, interaction.user, self.razon)
            await interaction.response.send_modal(modal)
        
        elif action == "create_role":
            if not guild or not guild.me:
                embed = discord.Embed(title="❌ **ERROR**", description="No puedo acceder al servidor", color=0xe74c3c)
                embed.set_footer(text="✨ • Lux By _.aari._")
                return await interaction.response.edit_message(embed=embed, view=None)
            
            if not guild.me.guild_permissions.manage_roles:
                embed = discord.Embed(
                    title="❌ **PERMISOS INSUFICIENTES**",
                    description="No tengo permiso para crear roles",
                    color=0xe74c3c,
                    timestamp=datetime.now()
                )
                embed.set_footer(text="✨ • Lux By _.aari._")
                return await interaction.response.edit_message(embed=embed, view=None)
            
            if isinstance(interaction.user, discord.Member) and not interaction.user.guild_permissions.manage_roles:
                embed = discord.Embed(
                    title="❌ **PERMISOS INSUFICIENTES**",
                    description="No tienes permiso para crear roles",
                    color=0xe74c3c,
                    timestamp=datetime.now()
                )
                embed.set_footer(text="✨ • Lux By _.aari._")
                return await interaction.response.edit_message(embed=embed, view=None)
            
            modal = CreateRoleModal(interaction.user, self.razon)
            await interaction.response.send_modal(modal)
        
        elif action == "delete_role":
            if not guild or not guild.me:
                embed = discord.Embed(title="❌ **ERROR**", description="No puedo acceder al servidor", color=0xe74c3c)
                embed.set_footer(text="✨ • Lux By _.aari._")
                return await interaction.response.edit_message(embed=embed, view=None)
            
            if not guild.me.guild_permissions.manage_roles:
                embed = discord.Embed(
                    title="❌ **PERMISOS INSUFICIENTES**",
                    description="No tengo permiso para eliminar roles",
                    color=0xe74c3c,
                    timestamp=datetime.now()
                )
                embed.set_footer(text="✨ • Lux By _.aari._")
                return await interaction.response.edit_message(embed=embed, view=None)
            
            if isinstance(interaction.user, discord.Member) and not interaction.user.guild_permissions.manage_roles:
                embed = discord.Embed(
                    title="❌ **PERMISOS INSUFICIENTES**",
                    description="No tienes permiso para eliminar roles",
                    color=0xe74c3c,
                    timestamp=datetime.now()
                )
                embed.set_footer(text="✨ • Lux By _.aari._")
                return await interaction.response.edit_message(embed=embed, view=None)
            
            modal = DeleteRoleModal(interaction.user, self.razon)
            await interaction.response.send_modal(modal)


class MuteDurationSelect(ui.Select):
    def __init__(self, target_user: discord.Member, moderator: discord.User | discord.Member, razon: str = "Sin razón especificada"):
        self.target_user = target_user
        self.moderator = moderator
        self.razon = razon
        
        options = [
            discord.SelectOption(label="5 minutos", value="5m", emoji="⏰"),
            discord.SelectOption(label="15 minutos", value="15m", emoji="⏰"),
            discord.SelectOption(label="1 hora", value="1h", emoji="🕐"),
            discord.SelectOption(label="1 día", value="1d", emoji="📅"),
            discord.SelectOption(label="1 semana", value="7d", emoji="📆"),
        ]
        super().__init__(
            placeholder="⏰ Selecciona la duración del mute...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        duration_str = self.values[0]
        
        try:
            duration: timedelta | None = None
            duration_display: str = ""
            
            if duration_str == "5m":
                duration = timedelta(minutes=5)
                duration_display = "5 minutos"
            elif duration_str == "15m":
                duration = timedelta(minutes=15)
                duration_display = "15 minutos"
            elif duration_str == "1h":
                duration = timedelta(hours=1)
                duration_display = "1 hora"
            elif duration_str == "1d":
                duration = timedelta(days=1)
                duration_display = "1 día"
            elif duration_str == "7d":
                duration = timedelta(days=7)
                duration_display = "1 semana"
            
            if duration:
                until = datetime.now(timezone.utc) + duration
                await self.target_user.timeout(until, reason=f"Moderación por {interaction.user} - Razón: {self.razon}")
            
            embed = discord.Embed(
                title="🔇 **USUARIO SILENCIADO**",
                description=f"{self.target_user.mention} ha sido silenciado",
                color=0x3498db,
                timestamp=datetime.now()
            )
            embed.add_field(name="👤 Usuario", value=f"{self.target_user}", inline=True)
            embed.add_field(name="👮 Moderador", value=f"{interaction.user}", inline=True)
            embed.add_field(name="⏰ Duración", value=duration_display, inline=True)
            embed.add_field(name="📝 Acción", value="Mute", inline=False)
            embed.add_field(name="📋 Razón", value=self.razon, inline=False)
            embed.set_footer(text="✨ • Lux By _.aari._")
            await interaction.response.edit_message(embed=embed, view=None)
        except Exception as e:
            embed = discord.Embed(
                title="❌ **ERROR**",
                description=f"No se pudo silenciar al usuario: {str(e)[:100]}",
                color=0xe74c3c,
                timestamp=datetime.now()
            )
            embed.set_footer(text="✨ • Lux By _.aari._")
            await interaction.response.edit_message(embed=embed, view=None)


class MuteDurationView(ui.View):
    def __init__(self, target_user: discord.Member, moderator: discord.User | discord.Member, razon: str = "Sin razón especificada"):
        super().__init__(timeout=300)
        self.target_user = target_user
        self.moderator = moderator
        self.razon = razon
        self.add_item(MuteDurationSelect(target_user, moderator, razon))


class NicknameModal(ui.Modal):
    def __init__(self, target_user: discord.Member, moderator: discord.User | discord.Member, razon: str):
        super().__init__(title="Cambiar Apodo")
        self.target_user = target_user
        self.moderator = moderator
        self.razon = razon
        self.add_item(ui.InputText(label="Nuevo apodo", placeholder="Ingresa el nuevo apodo", max_length=32))
    
    async def callback(self, interaction: discord.Interaction) -> None:
        new_nickname = self.children[0].value
        try:
            await self.target_user.edit(nick=new_nickname)
            embed = discord.Embed(
                title="📝 **APODO CAMBIADO**",
                description=f"El apodo de {self.target_user.mention} ha sido cambiado",
                color=0x3498db,
                timestamp=datetime.now()
            )
            embed.add_field(name="👤 Usuario", value=f"{self.target_user}", inline=True)
            embed.add_field(name="👮 Moderador", value=f"{interaction.user}", inline=True)
            embed.add_field(name="📝 Nuevo Apodo", value=f"`{new_nickname}`", inline=False)
            embed.add_field(name="📋 Razón", value=self.razon, inline=False)
            embed.set_footer(text="✨ • Lux By _.aari._")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title="❌ **ERROR**",
                description=f"No se pudo cambiar el apodo: {str(e)[:100]}",
                color=0xe74c3c,
                timestamp=datetime.now()
            )
            embed.set_footer(text="✨ • Lux By _.aari._")
            await interaction.response.send_message(embed=embed, ephemeral=True)


class CreateRoleModal(ui.Modal):
    def __init__(self, moderator: discord.User | discord.Member, razon: str):
        super().__init__(title="Crear Rol")
        self.moderator = moderator
        self.razon = razon
        self.add_item(ui.InputText(label="Nombre del rol", placeholder="Ej: Miembros VIP", max_length=100))
    
    async def callback(self, interaction: discord.Interaction) -> None:
        role_name = self.children[0].value
        if not role_name:
            embed = discord.Embed(title="❌ **ERROR**", description="El nombre no puede estar vacío", color=0xe74c3c)
            embed.set_footer(text="✨ • Lux By _.aari._")
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        try:
            guild = interaction.guild
            if not guild:
                return
            new_role = await guild.create_role(name=role_name, reason=f"Creado por {interaction.user} - {self.razon}")
            embed = discord.Embed(
                title="👑 **ROL CREADO**",
                description=f"Se ha creado el rol {new_role.mention}",
                color=0x9b59b6,
                timestamp=datetime.now()
            )
            embed.add_field(name="👮 Moderador", value=f"{interaction.user}", inline=True)
            embed.add_field(name="📝 Nombre", value=f"`{role_name}`", inline=True)
            embed.add_field(name="🆔 ID", value=f"`{new_role.id}`", inline=True)
            embed.add_field(name="📋 Razón", value=self.razon, inline=False)
            embed.set_footer(text="✨ • Lux By _.aari._")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title="❌ **ERROR**",
                description=f"No se pudo crear el rol: {str(e)[:100]}",
                color=0xe74c3c,
                timestamp=datetime.now()
            )
            embed.set_footer(text="✨ • Lux By _.aari._")
            await interaction.response.send_message(embed=embed, ephemeral=True)


class DeleteRoleModal(ui.Modal):
    def __init__(self, moderator: discord.User | discord.Member, razon: str):
        super().__init__(title="Eliminar Rol")
        self.moderator = moderator
        self.razon = razon
        self.add_item(ui.InputText(label="ID del rol", placeholder="Ej: 123456789", max_length=30))
    
    async def callback(self, interaction: discord.Interaction) -> None:
        role_id_str = self.children[0].value
        if not role_id_str:
            embed = discord.Embed(title="❌ **ERROR**", description="El ID no puede estar vacío", color=0xe74c3c)
            embed.set_footer(text="✨ • Lux By _.aari._")
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        try:
            guild = interaction.guild
            if not guild:
                return
            role_id = int(role_id_str)
            role = guild.get_role(role_id)
            if not role:
                embed = discord.Embed(
                    title="❌ **ROL NO ENCONTRADO**",
                    description=f"No encontré el rol con ID: {role_id}",
                    color=0xe74c3c,
                    timestamp=datetime.now()
                )
                embed.set_footer(text="✨ • Lux By _.aari._")
                return await interaction.response.send_message(embed=embed, ephemeral=True)
            
            role_name = role.name
            await role.delete(reason=f"Eliminado por {interaction.user} - {self.razon}")
            embed = discord.Embed(
                title="🗑️ **ROL ELIMINADO**",
                description=f"Se ha eliminado el rol",
                color=0xe74c3c,
                timestamp=datetime.now()
            )
            embed.add_field(name="👮 Moderador", value=f"{interaction.user}", inline=True)
            embed.add_field(name="📝 Nombre", value=f"`{role_name}`", inline=True)
            embed.add_field(name="🆔 ID", value=f"`{role_id}`", inline=True)
            embed.add_field(name="📋 Razón", value=self.razon, inline=False)
            embed.set_footer(text="✨ • Lux By _.aari._")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except ValueError:
            embed = discord.Embed(
                title="❌ **ID INVÁLIDO**",
                description="El ID del rol debe ser un número",
                color=0xe74c3c,
                timestamp=datetime.now()
            )
            embed.set_footer(text="✨ • Lux By _.aari._")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title="❌ **ERROR**",
                description=f"No se pudo eliminar el rol: {str(e)[:100]}",
                color=0xe74c3c,
                timestamp=datetime.now()
            )
            embed.set_footer(text="✨ • Lux By _.aari._")
            await interaction.response.send_message(embed=embed, ephemeral=True)


class ModView(ui.View):
    def __init__(self, target_user: discord.Member, moderator: discord.Member, razon: str = "Sin razón especificada"):
        super().__init__(timeout=300)
        self.target_user = target_user
        self.moderator = moderator
        self.razon = razon
        self.add_item(ModActionSelect(target_user, moderator, razon))
