import discord
from discord import ui
from datetime import datetime
import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'newembed_config.json')

def load_newembed_config():
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        default_config = {}
        with open(CONFIG_PATH, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config

def save_newembed_config(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

class EmbedBuilderModal(ui.Modal):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(
            title="Crear Embed Personalizado",
            timeout=600
        )
        
        self.title_input = ui.InputText(
            label="Título del Embed",
            placeholder="Ej: Anuncio Importante",
            min_length=1,
            max_length=256,
            required=True
        )
        self.description_input = ui.InputText(
            label="Descripción",
            placeholder="Ej: Este es el contenido del embed",
            min_length=1,
            max_length=4000,
            required=True,
            style=discord.InputTextStyle.long
        )
        self.color_input = ui.InputText(
            label="Color Hexadecimal",
            placeholder="Ej: FF5733 (sin #)",
            min_length=6,
            max_length=6,
            required=False
        )
        
        self.add_item(self.title_input)
        self.add_item(self.description_input)
        self.add_item(self.color_input)
    
    async def callback(self, interaction: discord.Interaction):
        try:
            title = self.title_input.value
            description = self.description_input.value
            color_hex = self.color_input.value or "9b59b6"
            
            try:
                color = int(color_hex, 16)
            except ValueError:
                color = 0x9b59b6
            
            embed = discord.Embed(
                title=title,
                description=description,
                color=color,
                timestamp=datetime.now()
            )
            
            if self.bot.user and self.bot.user.banner:
                embed.set_image(url=self.bot.user.banner.url)
            
            embed.set_footer(text="✨ • Lux By _.aari._")
            
            view = ChannelSelectView(self.bot, embed)
            await interaction.response.send_message(
                content="✅ **Embed creado exitosamente!**\n\nSelecciona el canal donde deseas enviar este embed:",
                embed=embed,
                view=view,
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                content=f"❌ Error al crear el embed: {str(e)[:100]}",
                ephemeral=True
            )


class ChannelSelect(ui.Select):
    def __init__(self, bot, embed):
        self.bot = bot
        self.embed = embed
        
        options = []
        for guild_channel in bot.get_all_channels():
            if isinstance(guild_channel, discord.TextChannel) and len(options) < 25:
                options.append(
                    discord.SelectOption(
                        label=guild_channel.name,
                        value=str(guild_channel.id),
                        description=f"Servidor: {guild_channel.guild.name}",
                        emoji="💬"
                    )
                )
        
        if not options:
            options.append(discord.SelectOption(label="Sin canales disponibles", value="none"))
        
        super().__init__(
            placeholder="📋 Selecciona un canal...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "none":
            await interaction.response.edit_message(
                content="❌ No hay canales disponibles",
                view=None
            )
            return
        
        try:
            channel_id = int(self.values[0]) if isinstance(self.values[0], str) else self.values[0]
            channel = self.bot.get_channel(channel_id)
            if not channel:
                raise ValueError("Canal no encontrado")
            
            await channel.send(embed=self.embed)
            
            success_embed = discord.Embed(
                title="✅ **EMBED ENVIADO**",
                description=f"El embed ha sido enviado exitosamente a {channel.mention}",
                color=0x2ecc71,
                timestamp=datetime.now()
            )
            success_embed.set_footer(text="✨ • Lux By _.aari._")
            
            await interaction.response.edit_message(
                content="",
                embed=success_embed,
                view=None
            )
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ **ERROR**",
                description=f"No se pudo enviar el embed: {str(e)[:100]}",
                color=0xe74c3c,
                timestamp=datetime.now()
            )
            error_embed.set_footer(text="✨ • Lux By _.aari._")
            
            await interaction.response.edit_message(
                embed=error_embed,
                view=None
            )


class ChannelSelectView(ui.View):
    def __init__(self, bot, embed):
        super().__init__(timeout=600)
        self.bot = bot
        self.embed = embed
        self.add_item(ChannelSelect(bot, embed))
