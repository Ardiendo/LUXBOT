import os
import sys
import discord
from pathlib import Path
from discord.ext import commands
from datetime import datetime

# Importaciones de tus herramientas (ajusta según tu estructura)
from src.utils.discord_tools.embeds import create_success_embed, create_error_embed, set_footer_with_author

DEVELOPER_ID = 819080793447333918

class RestartCog(commands.Cog, name="Sistema de Reinicio"):
    def __init__(self, bot):
        self.bot = bot

    def _get_cogs_directory(self) -> Path:
        """Obtiene la ruta absoluta al directorio de cogs."""
        return Path(__file__).resolve().parent.parent / 'cogs'

    def _restart_program(self):
        """Reinicia el proceso actual de Python."""
        # sys.executable es la ruta al intérprete de Python en uso
        # sys.argv son los argumentos usados para iniciar el script
        python = sys.executable
        os.execl(python, python, *sys.argv)

    @discord.slash_command(
        name="restart",
        description="Gestión de reinicio del bot (Solo Developer)"
    )
    async def restart(
        self, 
        ctx: discord.ApplicationContext,
        mode: discord.Option(
            str, 
            description="Elige el tipo de reinicio", 
            choices=["Recargar Extensiones (Cogs)", "Reinicio de Sistema (Full)"],
            default="Recargar Extensiones (Cogs)"
        )
    ):
        # 1. Verificación de permisos
        if ctx.author.id != DEVELOPER_ID:
            embed = create_error_embed(
                self.bot,
                "❌ **ACCESO DENEGADO**",
                f"Solo el desarrollador (<@{DEVELOPER_ID}>) puede ejecutar este comando."
            )
            return await ctx.respond(embed=set_footer_with_author(embed), ephemeral=True)

        # --- OPCIÓN A: REINICIO COMPLETO DEL SISTEMA ---
        if mode == "Reinicio de Sistema (Full)":
            embed = create_success_embed(
                self.bot,
                "🔌 **REINICIANDO SISTEMA**",
                "El proceso del bot se detendrá y se iniciará de nuevo."
            )
            embed.add_field(
                name="⚠️ Aviso", 
                value="El bot estará desconectado unos segundos. No recibirás confirmación de 'listo' aquí.", 
                inline=False
            )
            embed = set_footer_with_author(embed)

            await ctx.respond(embed=embed)

            print(f"--- REINICIO DE SISTEMA SOLICITADO POR {ctx.author.name} ---")

            # Ejecutamos el reinicio
            self._restart_program()
            return # El código deja de ejecutarse aquí porque el proceso muere

        # --- OPCIÓN B: RECARGA DE EXTENSIONES (HOT RELOAD) ---
        start_time = datetime.now()
        loading_embed = create_success_embed(
            self.bot,
            "🔄 **RECARGANDO EXTENSIONES**",
            "Escaneando directorio y actualizando comandos..."
        )
        loading_embed.add_field(name="⏱️ Inicio", value=f"<t:{int(start_time.timestamp())}:T>", inline=True)

        interaction = await ctx.respond(embed=set_footer_with_author(loading_embed))

        loaded_count = 0
        failed_extensions = []
        cogs_path = self._get_cogs_directory()

        if not cogs_path.exists():
            try:
                return await interaction.edit_original_response(content=f"❌ Directorio no encontrado: `{cogs_path}`")
            except discord.NotFound:
                return await ctx.respond(content=f"❌ Directorio no encontrado: `{cogs_path}`", ephemeral=True)

        for file in cogs_path.glob("*.py"):
            if file.name.startswith("_"):
                continue

            extension_name = f"src.cogs.{file.stem}"

            try:
                self.bot.reload_extension(extension_name)
            except commands.ExtensionNotLoaded:
                try:
                    self.bot.load_extension(extension_name)
                except Exception as e:
                    failed_extensions.append((file.stem, str(e)))
                    continue
            except Exception as e:
                failed_extensions.append((file.stem, str(e)))
                continue

            loaded_count += 1

        # Construcción del reporte final
        duration = (datetime.now() - start_time).total_seconds()

        if not failed_extensions:
            result_embed = create_success_embed(
                self.bot,
                "✅ **EXTENSIONES RECARGADAS**",
                "Hot Reload completado exitosamente."
            )
            result_embed.color = discord.Color.green()
        else:
            result_embed = create_error_embed(
                self.bot,
                "⚠️ **RECARGA PARCIAL**",
                "Algunas extensiones fallaron."
            )
            result_embed.color = discord.Color.orange()

        result_embed.add_field(
            name="📊 Resumen", 
            value=f"✅ **{loaded_count}** OK | ❌ **{len(failed_extensions)}** Error", 
            inline=True
        )
        result_embed.add_field(name="⏱️ Tiempo", value=f"`{duration:.2f}s`", inline=True)

        if failed_extensions:
            error_msg = "\n".join([f"**{name}:** `{err[:50]}...`" for name, err in failed_extensions[:5]])
            result_embed.add_field(name="📋 Errores", value=error_msg, inline=False)

        result_embed = set_footer_with_author(result_embed)
        try:
            await interaction.edit_original_response(embed=result_embed)
        except discord.NotFound:
            await ctx.respond(embed=result_embed, ephemeral=True)

def setup(bot):
    bot.add_cog(RestartCog(bot))
