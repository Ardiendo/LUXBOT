import discord
from discord.ext import commands
from datetime import datetime
import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'maintenance_config.json')
DEVELOPER_ID = 819080793447333918

def load_maintenance_config():
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        default_config = {"enabled": False, "message": "El bot está en mantenimiento"}
        with open(CONFIG_PATH, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config

def save_maintenance_config(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

class MaintenanceCog(commands.Cog, name="maintenance command"):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="maintenance",
        description="Activar/desactivar modo mantenimiento (solo dev)"
    )
    async def maintenance(self, ctx: discord.ApplicationContext, activar: bool, mensaje: str = "El bot está en mantenimiento"):
        if ctx.author.id != DEVELOPER_ID:
            embed = discord.Embed(
                title="❌ **ACCESO DENEGADO**",
                description=f"Solo el desarrollador (<@{DEVELOPER_ID}>) puede usar este comando.",
                color=0xe74c3c,
                timestamp=datetime.now()
            )
            embed.set_footer(text="✨ • Lux By _.aari._")
            return await ctx.respond(embed=embed, ephemeral=True)
        
        config = load_maintenance_config()
        config["enabled"] = activar
        config["message"] = mensaje
        save_maintenance_config(config)
        
        estado = "🔧 **ACTIVADO**" if activar else "✅ **DESACTIVADO**"
        descripcion = f"Modo mantenimiento {estado}\nMensaje: {config['message']}" if activar else "El bot está nuevamente en línea"
        
        embed = discord.Embed(
            title="⚙️ **MODO MANTENIMIENTO**",
            description=descripcion,
            color=0xf39c12 if activar else 0x2ecc71,
            timestamp=datetime.now()
        )
        embed.set_footer(text="✨ • Lux By _.aari._")
        await ctx.respond(embed=embed, ephemeral=True)
        
        # Enviar DMs a usuarios
        try:
            users_notified = 0
            for guild in self.bot.guilds:
                for member in guild.members:
                    if not member.bot:
                        try:
                            dm_embed = discord.Embed(
                                title="🔧 **NOTIFICACIÓN - MODO MANTENIMIENTO**" if activar else "✅ **NOTIFICACIÓN - BOT ONLINE**",
                                description=config.get("message", "El bot está en mantenimiento") if activar else "¡El bot está nuevamente en línea!",
                                color=0xf39c12 if activar else 0x2ecc71,
                                timestamp=datetime.now()
                            )
                            dm_embed.set_footer(text="✨ • Lux By _.aari._")
                            await member.send(embed=dm_embed)
                            users_notified += 1
                        except:
                            pass
            
            # Confirmar en el servidor
            confirm_embed = discord.Embed(
                title="📨 **NOTIFICACIONES ENVIADAS**",
                description=f"Se enviaron {users_notified} mensajes directos a los usuarios",
                color=0x3498db,
                timestamp=datetime.now()
            )
            confirm_embed.set_footer(text="✨ • Lux By _.aari._")
            await ctx.followup.send(embed=confirm_embed, ephemeral=True)
        except Exception as e:
            print(f"Error enviando DMs: {e}")


def setup(bot):
    bot.add_cog(MaintenanceCog(bot))
