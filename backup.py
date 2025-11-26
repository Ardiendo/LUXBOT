import os
import discord
from discord.ext import commands
from discord import Option
from datetime import datetime
import json
import io
from src.utils.discord_tools.embeds import create_banner_embed, create_success_embed, create_error_embed, set_footer_with_author


class BackupCog(commands.Cog, name="backup command"):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command(
        name="backup",
        description="Exportar la configuración de recompensas"
    )
    @discord.default_permissions(administrator=True)
    async def slash_backup(self, ctx: discord.ApplicationContext):
        await ctx.defer(ephemeral=True)
        
        if not ctx.guild:
            return
        
        try:
            roles_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "roles.json")
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "configuration.json")
            
            with open(roles_path, "r") as f:
                roles_data = json.load(f)
            with open(config_path, "r") as f:
                config_data = json.load(f)
            
            guild_id_str = str(ctx.guild.id)
            guild_roles = roles_data.get("guilds", {}).get(guild_id_str, [])
            
            backup_data = {
                "guild_id": ctx.guild.id,
                "guild_name": ctx.guild.name,
                "exported_at": datetime.now().isoformat(),
                "roles": {guild_id_str: guild_roles},
                "configuration": config_data
            }
            
            backup_json = json.dumps(backup_data, indent=2, default=str)
            file = discord.File(
                io.BytesIO(backup_json.encode()),
                filename=f"lux_backup_{ctx.guild.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            embed = create_success_embed(
                self.bot,
                "💾 **Backup Creado**",
                "Se ha exportado la configuración del bot."
            )
            embed.add_field(
                name="📊 Contenido",
                value=f"• **{len(guild_roles)}** recompensas de rol\n• Configuración del servidor",
                inline=False
            )
            embed.add_field(
                name="📝 Instrucciones",
                value="Guarda este archivo para restaurar la configuración en el futuro con `/restore`",
                inline=False
            )
            embed = set_footer_with_author(embed)
            
            await ctx.respond(embed=embed, file=file, ephemeral=True)
            
        except Exception as e:
            embed = create_error_embed(
                self.bot,
                "⚠️ **Error**",
                f"No se pudo crear el backup.\n```{str(e)[:200]}```"
            )
            embed = set_footer_with_author(embed)
            await ctx.respond(embed=embed, ephemeral=True)
    
    @discord.slash_command(
        name="restore",
        description="Restaurar la configuración desde un archivo de backup"
    )
    @discord.default_permissions(administrator=True)
    async def slash_restore(
        self,
        ctx: discord.ApplicationContext,
        archivo: discord.Attachment = Option(
            description="Archivo de backup JSON",
            required=True
        )
    ):
        await ctx.defer(ephemeral=True)
        
        if not archivo or not archivo.filename.endswith('.json'):
            embed = create_error_embed(
                self.bot,
                "⚠️ **Error**",
                "El archivo debe ser un JSON de backup."
            )
            embed = set_footer_with_author(embed)
            return await ctx.respond(embed=embed, ephemeral=True)
        
        try:
            content = await archivo.read()
            backup_data = json.loads(content.decode())
            
            roles_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "roles.json")
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "configuration.json")
            
            if "roles" in backup_data:
                with open(roles_path, "r") as f:
                    current_roles = json.load(f)
                
                if "guilds" not in current_roles:
                    current_roles["guilds"] = {}
                
                current_roles["guilds"].update(backup_data["roles"])
                
                with open(roles_path, "w") as f:
                    json.dump(current_roles, f, indent=2)
            
            if "configuration" in backup_data:
                with open(config_path, "w") as f:
                    json.dump(backup_data["configuration"], f, indent=2)
            
            embed = create_success_embed(
                self.bot,
                "✅ **Backup Restaurado**",
                "La configuración ha sido restaurada correctamente."
            )
            
            if "exported_at" in backup_data:
                embed.add_field(
                    name="📅 Fecha del Backup",
                    value=backup_data["exported_at"][:19].replace("T", " "),
                    inline=True
                )
            
            if "guild_name" in backup_data:
                embed.add_field(
                    name="🏠 Servidor Original",
                    value=backup_data["guild_name"],
                    inline=True
                )
            
            embed = set_footer_with_author(embed)
            await ctx.respond(embed=embed, ephemeral=True)
            
        except json.JSONDecodeError:
            embed = create_error_embed(
                self.bot,
                "⚠️ **Error**",
                "El archivo no es un JSON válido."
            )
            embed = set_footer_with_author(embed)
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            embed = create_error_embed(
                self.bot,
                "⚠️ **Error**",
                f"No se pudo restaurar el backup.\n```{str(e)[:200]}```"
            )
            embed = set_footer_with_author(embed)
            await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(BackupCog(bot))
