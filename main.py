#!/usr/bin/env python3

import os
import sys

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))))

import discord
import json
from datetime import datetime
from discord.ext import commands, tasks
from src.utils.discord_tools.error_logger import log_error_to_channel

config_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config',
    'configuration.json')
with open(config_path, "r") as roleFile:
    data = json.load(roleFile)

token = os.environ.get("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents)
bot.remove_command("help")

cogs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cogs')
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Buscar recursivamente todos los archivos .py en cogs/ e incluir subcarpetas
initial_extensions3 = []
# Archivos que NO son Cogs (módulos de utilidad)
SKIP_FILES = {'views.py', 'storage.py', '__init__.py'}

for root, dirs, files in os.walk(cogs_path):
    for file in files:
        if file.endswith(
                '.py') and not file.startswith('_') and file not in SKIP_FILES:
            # Obtener la ruta relativa del archivo desde la raíz del workspace
            file_path = os.path.join(root, file)
            # Convertir a module path: src.cogs.filename o src.cogs.subfolder.filename
            rel_path = os.path.relpath(file_path, workspace_root)
            # Convertir \ a / y .py a nada
            module_path = rel_path.replace(os.sep, '.').replace('.py', '')
            if module_path not in initial_extensions3:
                initial_extensions3.append(module_path)

PRESENCE_STATES = [
    (discord.ActivityType.listening, "/help 📖"),
    (discord.ActivityType.competing, "V1.5.1 🏆"),
    (discord.ActivityType.watching, "New economy 📈✨"),
    (discord.ActivityType.playing, "Lux✨ - by AriDev"),
    (discord.ActivityType.watching, "usuarios ganando XP ✨"),
    (discord.ActivityType.playing, "con recompensas de rol 👑"),
    (discord.ActivityType.listening, "comandos slash /help 🔮"),
    (discord.ActivityType.competing, "mejor bot de roles 💎"),
]

current_presence = 0


@tasks.loop(minutes=5)
async def change_presence_task():
    global current_presence
    if bot.user:
        activity_type, activity_name = PRESENCE_STATES[current_presence %
                                                       len(PRESENCE_STATES)]
        activity = discord.Activity(type=activity_type, name=activity_name)
        await bot.change_presence(activity=activity)
        current_presence += 1


@change_presence_task.before_loop
async def before_change_presence():
    await bot.wait_until_ready()


@bot.event
async def on_ready():
    print('╔═══════════════════════════════════════════╗')
    print(f'║  ✨ Lux Bot Online - {bot.user}')
    print(
        f'║  Discord.py Version: {discord.version_info.major}.{discord.version_info.minor}.{discord.version_info.micro}'
    )
    if bot.user:
        print(f'║  Bot ID: {bot.user.id}')
        print('║  Bot Version: V1.5.1')
    print('╚═══════════════════════════════════════════╝')

    # Sincronizar comandos globalmente (elimina y re-registra automáticamente)
    try:
        print(
            '📡 Sincronizando comandos globalmente (eliminando anteriores y registrando nuevos)...'
        )
        synced_commands = await bot.sync_commands()

        # Contar comandos sincronizados
        cmd_count = 0
        if synced_commands:
            cmd_count = len(synced_commands)

        # Verificar que todos los Cogs estén cargados
        total_cogs = len(bot.cogs)
        print('✅ Sincronización completada')
        print(f'🎉 {cmd_count} comandos registrados globalmente')
        print(f'📊 Verificación: {total_cogs} cogs cargados')
        print('📋 Cogs registrados:')
        for cog_name in sorted(bot.cogs.keys()):
            print(f'   • {cog_name}')
    except Exception as e:
        print(f'❌ Error sincronizando comandos: {e}')

    if not change_presence_task.is_running():
        change_presence_task.start()

    activity = discord.Activity(type=discord.ActivityType.watching,
                                name="usuarios ganando XP ✨")
    await bot.change_presence(activity=activity)


def load_maintenance_config():
    """Cargar configuración de mantenimiento"""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config',
        'maintenance_config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"enabled": False, "message": "El bot está en mantenimiento"}


@bot.event
async def on_interaction(interaction: discord.Interaction):
    """Interceptar TODAS las interacciones antes de procesarlas"""
    if interaction.type == discord.InteractionType.application_command:
        if interaction.user:
            config = load_maintenance_config()
            DEVELOPER_ID = 819080793447333918

            # Verificar si está en mantenimiento y si el usuario NO es el desarrollador
            if config.get("enabled",
                          False) and interaction.user.id != DEVELOPER_ID:
                embed = discord.Embed(
                    title="🔧 **Lux Esta dormida | Modo mantenimiento**",
                    description=config.get("message",
                                           "El bot está en mantenimiento"),
                    color=0xf39c12,
                    timestamp=datetime.now())
                embed.set_footer(text="✨ • Lux By _.aari._")
                try:
                    await interaction.response.send_message(embed=embed,
                                                            ephemeral=True)
                except Exception:
                    pass
                return

    # Permitir que se procesen otros listeners y comandos normalmente
    await bot.process_application_commands(interaction)


@bot.event
async def on_command_error(ctx: commands.Context, error: Exception):
    cmd_name = ctx.command.name if ctx.command else 'Unknown'
    await log_error_to_channel(
        bot,
        error,
        context=f"Command: {cmd_name}",
        user=ctx.author if isinstance(ctx.author, discord.User) else None,
        guild=ctx.guild if isinstance(ctx.guild, discord.Guild) else None)
    print(f"❌ Command error: {error}")


@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext,
                                       error: Exception):
    cmd_name = ctx.command.qualified_name if ctx.command else 'Unknown'
    await log_error_to_channel(
        bot,
        error,
        context=f"Slash Command: {cmd_name}",
        user=ctx.author if isinstance(ctx.author, discord.User) else None,
        guild=ctx.guild if isinstance(ctx.guild, discord.Guild) else None)
    print(f"❌ Slash command error: {error}")


if __name__ == '__main__':
    for extension in initial_extensions3:
        try:
            bot.load_extension(extension)
            print(f'✓ Loaded extension {extension}')
        except Exception as e:
            print(f'✗ Failed to load extension {extension}.', file=sys.stderr)
            print(e)

    bot.run(token)
