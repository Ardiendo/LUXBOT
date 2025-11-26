import discord
from discord import ui


class HelpSelect(ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(
                label="Principal",
                description="Información general del bot",
                emoji="🏠",
                value="main"
            ),
            discord.SelectOption(
                label="Recompensas",
                description="Comandos de recompensas de rol",
                emoji="🏆",
                value="rewards"
            ),
            discord.SelectOption(
                label="Utilidades",
                description="Comandos de utilidad",
                emoji="🛠️",
                value="utilities"
            ),
            discord.SelectOption(
                label="Administración",
                description="Comandos de administración",
                emoji="⚙️",
                value="admin"
            ),
            discord.SelectOption(
                label="Sistema",
                description="Sistema de logs y notificaciones",
                emoji="📊",
                value="system"
            ),
            discord.SelectOption(
                label="Novedades",
                description="Últimas funcionalidades añadidas",
                emoji="✨",
                value="news"
            ),
        ]
        super().__init__(
            placeholder="📖 Selecciona una categoría de ayuda...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        embed = None
        
        if category == "main":
            embed = discord.Embed(
                title="🏠 **Información Principal**",
                description="Bienvenido a **Lux✨**",
                color=0xdeaa0c
            )
            embed.add_field(
                name="¿Qué es Lux?",
                value="Un bot que replica las recompensas premium de Mee6.\nAsigna roles automáticamente basándose en el nivel de Mee6 de cada usuario.",
                inline=False
            )
            embed.add_field(
                name="✨ Características",
                value="🎖️ Recompensas automáticas de rol\n📊 Tarjetas visuales de nivel\n📝 Sistema de logs\n🔔 Notificaciones\n💾 Backup y restauración\n📈 Estadísticas",
                inline=False
            )
            embed.add_field(
                name="🎯 Objetivo",
                value="Permitir que cualquier servidor pueda tener recompensas de nivel sin pagar por Mee6 premium.",
                inline=False
            )
            
        elif category == "rewards":
            embed = discord.Embed(
                title="🏆 **Comandos de Recompensas**",
                description="Gestiona las recompensas de nivel",
                color=0x2ecc71
            )
            embed.add_field(
                name="/add",
                value="Añade un nuevo rol como recompensa de nivel\n`/add nivel:5 rol:@Moderator`",
                inline=False
            )
            embed.add_field(
                name="/remove",
                value="Elimina una recompensa de nivel\n`/remove nivel:5`",
                inline=False
            )
            embed.add_field(
                name="/rolerewards",
                value="Lista todas las recompensas configuradas",
                inline=False
            )
            embed.add_field(
                name="/leaderboard",
                value="Actualiza los roles de todos los usuarios del servidor",
                inline=False
            )
            
        elif category == "utilities":
            embed = discord.Embed(
                title="🛠️ **Comandos de Utilidad**",
                description="Herramientas disponibles",
                color=0x3498db
            )
            embed.add_field(
                name="/rank",
                value="Ve tu nivel y XP de Mee6\n`/rank` o `/rank usuario:@Usuario`",
                inline=False
            )
            embed.add_field(
                name="/stats",
                value="Ver estadísticas del servidor con menú interactivo (info general, recompensas, servidor, miembros)",
                inline=False
            )
            embed.add_field(
                name="/purge",
                value="Elimina mensajes del canal con menú interactivo\n`/purge` o `/purge cantidad:15`",
                inline=False
            )
            embed.add_field(
                name="/invite",
                value="Obtén el link de invitación de Lux✨ con menú interactivo",
                inline=False
            )
            embed.add_field(
                name="/newembed",
                value="Crea un embed personalizado y envíalo a cualquier canal (requiere gestionar mensajes)",
                inline=False
            )
            embed.add_field(
                name="/newembedperms",
                value="Controla quién puede usar `/newembed` (solo admin)\n`/newembedperms permitir:true/false`",
                inline=False
            )
            
        elif category == "admin":
            embed = discord.Embed(
                title="⚙️ **Comandos Administrativos**",
                description="Solo para administradores",
                color=0xf39c12
            )
            embed.add_field(
                name="/setlogchannel",
                value="Configura el canal para recibir logs de roles\n`/setlogchannel canal:#logs`",
                inline=False
            )
            embed.add_field(
                name="/setnotifications",
                value="Configura el canal de notificaciones de nivel\n`/setnotifications canal:#notificaciones`",
                inline=False
            )
            embed.add_field(
                name="/backup",
                value="Exporta la configuración del bot a un archivo",
                inline=False
            )
            embed.add_field(
                name="/restore",
                value="Importa una configuración desde un archivo\n`/restore archivo:backup.json`",
                inline=False
            )
            embed.add_field(
                name="/mod",
                value="Herramientas de moderación con menú (kick, ban, warn, mute)\n`/mod usuario:@Usuario`",
                inline=False
            )
            embed.add_field(
                name="/restart",
                value="Reinicia el bot (solo para desarrollador)",
                inline=False
            )
            
        elif category == "system":
            embed = discord.Embed(
                title="📊 **Sistema de Logs y Notificaciones**",
                description="Monitoreo y alertas",
                color=0x9b59b6
            )
            embed.add_field(
                name="📝 Logs",
                value="Se registran:\n• Asignación de roles\n• Eliminación de roles\n• Cambios de configuración\n• Errores del sistema",
                inline=False
            )
            embed.add_field(
                name="🔔 Notificaciones",
                value="Se notifica cuando:\n• Un usuario sube de nivel\n• Se obtiene un nuevo rol de recompensa",
                inline=False
            )
            embed.add_field(
                name="/viewlogs",
                value="Ve los últimos logs registrados",
                inline=False
            )
        
        elif category == "news":
            embed = discord.Embed(
                title="✨ **Novedades Recientes**",
                description="Últimas funcionalidades añadidas a Lux✨",
                color=0xf1c40f
            )
            embed.add_field(
                name="🛡️ Sistema Robusto de Errores",
                value="El bot ahora registra automáticamente todos los errores en un canal privado con información detallada de debugging.",
                inline=False
            )
            embed.add_field(
                name="⚙️ Comandos de Moderación",
                value="Nuevo comando `/mod` con menú interactivo para kick, ban, warn y mute (con duración configurable).",
                inline=False
            )
            embed.add_field(
                name="🎉 Comando Invite Mejorado",
                value="El comando `/invite` ahora muestra un menú con opciones para obtener el link de invitación e información del bot.",
                inline=False
            )
            embed.add_field(
                name="📊 Stats Interactivo",
                value="El comando `/stats` ahora incluye un menú desplegable con 4 opciones de información.",
                inline=False
            )
            embed.add_field(
                name="🔄 Comando Restart para Dev",
                value="Solo desarrollador puede reiniciar el bot y recargar todas las extensiones con feedback detallado.",
                inline=False
            )
            embed.add_field(
                name="📝 Embeds Consistentes",
                value="Todos los embeds ahora incluyen la foto y banner del bot para una experiencia visual profesional.",
                inline=False
            )
            embed.add_field(
                name="🎨 Comando Embed Builder",
                value="Nuevo comando `/newembed` que permite crear embeds personalizados con título, descripción y color, eligiendo el canal de envío.",
                inline=False
            )
            embed.add_field(
                name="🔧 Modo Mantenimiento",
                value="Comando `/maintenance` que permite activar/desactivar modo mantenimiento del bot (solo dev).",
                inline=False
            )
            embed.add_field(
                name="🔓 Subcomandos de Revocación",
                value="Nuevas opciones en `/mod` para revocar acciones: Unban, Unmute, Remover Warn.",
                inline=False
            )
            embed.add_field(
                name="💰 Sistema de Economía Completo",
                value="Comandos públicos: `/balance`, `/work`, `/shop`, `/inventory`, `/transfer`, `/economyleaderboard`. Admin: `/economyadmin`. Dev: `/ecodev`",
                inline=False
            )
            embed.add_field(
                name="🎬 Gifs en Embeds",
                value="Todos los embeds de economía ahora incluyen gifs animados acordes a su función para mejor experiencia visual.",
                inline=False
            )
            embed.add_field(
                name="👑 Comandos Admin de Economía",
                value="Nuevos comandos para administradores: `/ecoadmin_give`, `/ecoadmin_remove`, `/ecoadmin_reset`, `/ecoadmin_check`",
                inline=False
            )
            embed.add_field(
                name="👑 Comandos Dev de Economía",
                value="Nuevos comandos para desarrollador (permisos de Dios): `/ecodev_give`, `/ecodev_remove`, `/ecodev_reset`, `/ecodev_clearall`, `/ecodev_stats`",
                inline=False
            )
            embed.add_field(
                name="📩 Notificaciones de Mantenimiento",
                value="El bot ahora envía mensajes directos a los usuarios cuando se activa o desactiva el modo mantenimiento.",
                inline=False
            )
            embed.add_field(
                name="✅ Razones en Moderación",
                value="Todos los comandos de moderación ahora soportan parámetro de razón personalizada.",
                inline=False
            )
            embed.add_field(
                name="⭐ Sistema de Experiencia",
                value="Los usuarios acumulan XP automáticamente al enviar mensajes. Comandos: `/xp` para ver tu XP y `/xprank` para ver ranking.",
                inline=False
            )
            embed.add_field(
                name="📢 Sistema de Anuncios Global",
                value="Comando dev `/announce` para enviar embeds editables a todos los servidores. Actualizar con `/updateannounce`. Perfecto para anunciar nuevas versiones.",
                inline=False
            )
            embed.add_field(
                name="🎮 Comando ItemList Interactivo",
                value="Nuevo comando `/itemlist` con menú desplegable para navegar entre categorías de rareza (Común, Raro, Épico, Legendario, Exclusiva). Staff ve item_id para gestión.",
                inline=False
            )
            embed.add_field(
                name="🛡️ Mod Command Mejorado",
                value="El comando `/mod` ahora valida el estado del usuario antes de ejecutar acciones: verifica si está muteado antes de unmute/unban.",
                inline=False
            )
            embed.add_field(
                name="🔱 Bastón de Lux Exclusivo",
                value="Nuevo item exclusivo dev-only: Bastón de Lux (🔱), único y con visibilidad especial en la tienda.",
                inline=False
            )
            embed.add_field(
                name="💎 Tienda Expandida",
                value="Sistema de economía ahora con 39 items distribuidos en todas las categorías de rareza, con sistema de colors y emojis temáticos.",
                inline=False
            )
            embed.add_field(
                name="✨ Emojis de Lux Integrados",
                value="Sistema completo de emojis temáticos de Lux (sparkles, crystals, elemental forms) organizados por contexto en toda la experiencia del bot.",
                inline=False
            )
        
        if embed is not None:
            if self.bot.user and self.bot.user.banner:
                embed.set_image(url=self.bot.user.banner.url)
            embed.set_footer(text="✨ • Lux By _.aari._")
            await interaction.response.edit_message(embed=embed)


class HelpView(ui.View):
    def __init__(self, bot):
        super().__init__(timeout=300)
        self.bot = bot
        self.add_item(HelpSelect(bot))
