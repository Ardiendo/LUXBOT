import discord
from discord.ext import commands
from discord import ui
from src.utils.lux_quotes import (
    get_error_quote, get_success_quote, get_warning_quote, 
    get_loading_quote, get_tag_quote, get_fast_quote
)


class TestSelect(ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="💥 Simular Error", value="error", emoji="💥"),
            discord.SelectOption(label="✅ Simular Éxito", value="success", emoji="✅"),
            discord.SelectOption(label="⚠️ Simular Advertencia", value="warning", emoji="⚠️"),
            discord.SelectOption(label="🔄 Simular Carga", value="loading", emoji="🔄"),
            discord.SelectOption(label="🏃 Simular Rápido", value="fast", emoji="🏃"),
            discord.SelectOption(label="🎤 Ver Frase Random", value="random_quote", emoji="🎤"),
            discord.SelectOption(label="📊 Info del Bot", value="bot_info", emoji="📊"),
            discord.SelectOption(label="🧪 Division by Zero", value="div_zero", emoji="🧪"),
        ]
        super().__init__(
            placeholder="🛠️ Selecciona un test...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        test_type = self.values[0]
        
        if test_type == "error":
            embed = discord.Embed(
                title="💥 **Error de Prueba**",
                description=get_error_quote(),
                color=0xe74c3c
            )
            embed.add_field(name="Tipo", value="`ValueError`", inline=True)
            embed.add_field(name="Mensaje", value="Este es un error de prueba", inline=True)
            embed.set_footer(text="✨ • Lux By _.aari._ | Sistema de Test Activado")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        elif test_type == "success":
            embed = discord.Embed(
                title="✅ **Éxito Confirmado**",
                description=get_success_quote(),
                color=0x2ecc71
            )
            embed.add_field(name="Estado", value="`Operación Completada`", inline=True)
            embed.add_field(name="Tiempo", value="`0.05s`", inline=True)
            embed.set_footer(text="✨ • Lux By _.aari._ | Test Exitoso")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        elif test_type == "warning":
            embed = discord.Embed(
                title="⚠️ **Advertencia**",
                description=get_warning_quote(),
                color=0xf39c12
            )
            embed.add_field(name="Severidad", value="`Baja`", inline=True)
            embed.add_field(name="Acción", value="`Revisar Configuración`", inline=True)
            embed.set_footer(text="✨ • Lux By _.aari._ | Precaución Recomendada")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        elif test_type == "loading":
            embed = discord.Embed(
                title="🔄 **Procesando Magia**",
                description=get_loading_quote(),
                color=0x3498db
            )
            embed.add_field(name="Progreso", value="`████████░░ 80%`", inline=False)
            embed.set_footer(text="✨ • Lux By _.aari._ | Por favor espera...")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        elif test_type == "fast":
            embed = discord.Embed(
                title="⚡ **Velocidad de Luz**",
                description=get_fast_quote(),
                color=0xf1c40f
            )
            embed.add_field(name="Tiempo", value="`0.001s`", inline=True)
            embed.add_field(name="Velocidad", value="`Instantánea`", inline=True)
            embed.set_footer(text="✨ • Lux By _.aari._ | Completado Instantáneamente")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        elif test_type == "random_quote":
            quotes_to_show = {
                "Error": get_error_quote(),
                "Éxito": get_success_quote(),
                "Advertencia": get_warning_quote(),
                "Carga": get_loading_quote(),
                "Tag": get_tag_quote(),
                "Rápido": get_fast_quote(),
            }
            
            description = "\n".join([f"**{key}:**\n{value}\n" for key, value in quotes_to_show.items()])
            
            embed = discord.Embed(
                title="🎤 **Frases Aleatorias de Lux**",
                description=description,
                color=0x9b59b6
            )
            embed.set_footer(text="✨ • Lux By _.aari._ | Tú eres el buscador de la verdad")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        elif test_type == "bot_info":
            embed = discord.Embed(
                title="📊 **Información del Bot Lux**",
                description="Sistema de pruebas del bot Lux",
                color=0x9b59b6
            )
            embed.add_field(name="👑 Creador", value="_.aari._", inline=True)
            embed.add_field(name="📦 Versión", value="V1.5.1", inline=True)
            embed.add_field(name="🎮 Base", value="League of Legends", inline=True)
            embed.add_field(name="💾 Cogs Cargados", value=f"`{len(self.bot.cogs)}`", inline=True)
            embed.add_field(name="⚙️ Comandos", value="40+", inline=True)
            embed.add_field(name="🌟 Característica", value="Sistema de Roles + Economía", inline=True)
            embed.set_footer(text="✨ • Lux By _.aari._ | El brillo definitivo")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        elif test_type == "div_zero":
            try:
                raise ZeroDivisionError("División por cero intencional para test")
            except ZeroDivisionError as e:
                from src.utils.discord_tools.error_logger import log_error_to_channel
                await log_error_to_channel(
                    self.bot,
                    e,
                    context="Test Command: Division by Zero",
                    user=interaction.user if isinstance(interaction.user, discord.User) else None,
                    guild=interaction.guild if isinstance(interaction.guild, discord.Guild) else None
                )
                
                embed = discord.Embed(
                    title="🧪 **Test de Error Ejecutado**",
                    description="El error ha sido registrado en el canal de logs",
                    color=0x3498db
                )
                embed.add_field(name="Tipo", value="`ZeroDivisionError`", inline=True)
                embed.add_field(name="Estado", value="`Registrado`", inline=True)
                embed.set_footer(text="✨ • Lux By _.aari._ | Revisa el canal de errores")
                await interaction.response.send_message(embed=embed, ephemeral=True)


class TestView(ui.View):
    def __init__(self, bot):
        super().__init__()
        self.add_item(TestSelect(bot))


class AriTestingCog(commands.Cog, name="ari testing"):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command(
        name="aritest",
        description="🔧 Panel de testing del bot (Solo para Ari)"
    )
    async def testing_menu(self, ctx: discord.ApplicationContext):
        DEVELOPER_ID = 819080793447333918
        
        if ctx.author.id != DEVELOPER_ID:
            embed = discord.Embed(
                title="❌ **Acceso Denegado**",
                description="Este comando es solo para _.aari._",
                color=0xe74c3c
            )
            embed.set_footer(text="✨ • Lux By _.aari._")
            return await ctx.respond(embed=embed, ephemeral=True)
        
        embed = discord.Embed(
            title="🔧 **Panel de Testing - Lux**",
            description="Selecciona un test para ejecutar",
            color=0x9b59b6
        )
        embed.add_field(
            name="Opciones Disponibles",
            value="""
💥 - Simular Error
✅ - Simular Éxito
⚠️ - Simular Advertencia
🔄 - Simular Carga
🏃 - Simular Rápido
🎤 - Ver Frases Aleatorias
📊 - Info del Bot
🧪 - Test de Error Real
            """,
            inline=False
        )
        embed.set_footer(text="✨ • Lux By _.aari._ | Usa este panel para testear funcionalidades")
        
        await ctx.respond(embed=embed, view=TestView(self.bot), ephemeral=True)


def setup(bot):
    bot.add_cog(AriTestingCog(bot))
