import os
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import ui, SlashCommandGroup, Option
from datetime import datetime


class PurgeAmountSelect(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="5 mensajes",
                description="Eliminar los últimos 5 mensajes",
                emoji="5️⃣",
                value="5"
            ),
            discord.SelectOption(
                label="10 mensajes",
                description="Eliminar los últimos 10 mensajes",
                emoji="🔟",
                value="10"
            ),
            discord.SelectOption(
                label="25 mensajes",
                description="Eliminar los últimos 25 mensajes",
                emoji="📝",
                value="25"
            ),
            discord.SelectOption(
                label="50 mensajes",
                description="Eliminar los últimos 50 mensajes",
                emoji="📋",
                value="50"
            ),
            discord.SelectOption(
                label="100 mensajes",
                description="Eliminar los últimos 100 mensajes",
                emoji="💯",
                value="100"
            ),
            discord.SelectOption(
                label="Cancelar",
                description="Cancelar la operación",
                emoji="❌",
                value="cancel"
            )
        ]
        super().__init__(
            placeholder="🗑️ Selecciona la cantidad de mensajes a eliminar...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        
        if selected == "cancel":
            cancel_embed = discord.Embed(
                title="❌ **Operación Cancelada**",
                description="No se eliminaron mensajes.",
                color=0xe74c3c,
                timestamp=datetime.now()
            )
            cancel_embed.set_footer(text="✨ • Lux By _.aari._")
            await interaction.response.edit_message(embed=cancel_embed, view=None)
            self.view.stop()
            return
        
        amount = int(selected)
        
        processing_embed = discord.Embed(
            title="⏳ **Procesando...**",
            description=f"Eliminando **{amount}** mensajes...",
            color=0xf39c12,
            timestamp=datetime.now()
        )
        processing_embed.set_footer(text="✨ • Lux By _.aari._")
        await interaction.response.edit_message(embed=processing_embed, view=None)
        
        try:
            await interaction.message.delete()
            deleted = await interaction.channel.purge(limit=amount)
            
            success_embed = discord.Embed(
                title="✅ **Mensajes Eliminados**",
                description=f"Se han eliminado **{len(deleted)}** mensajes correctamente.",
                color=0x2ecc71,
                timestamp=datetime.now()
            )
            success_embed.add_field(
                name="📊 Detalles",
                value=f"**Canal:** {interaction.channel.mention}\n**Ejecutado por:** {interaction.user.mention}",
                inline=False
            )
            success_embed.set_footer(text="✨ • Lux By _.aari._")
            
            confirmation = await interaction.channel.send(embed=success_embed)
            await confirmation.delete(delay=5)
            
        except discord.Forbidden:
            error_embed = discord.Embed(
                title="⚠️ **Error de Permisos**",
                description="No tengo permisos para eliminar mensajes en este canal.",
                color=0xe74c3c,
                timestamp=datetime.now()
            )
            error_embed.set_footer(text="✨ • Lux By _.aari._")
            await interaction.channel.send(embed=error_embed, delete_after=5)
            
        except discord.HTTPException as e:
            error_embed = discord.Embed(
                title="⚠️ **Error**",
                description=f"Ocurrió un error al eliminar mensajes.\n```{str(e)[:100]}```",
                color=0xe74c3c,
                timestamp=datetime.now()
            )
            error_embed.set_footer(text="✨ • Lux By _.aari._")
            await interaction.channel.send(embed=error_embed, delete_after=5)
        
        self.view.stop()


class PurgeView(ui.View):
    def __init__(self, author_id: int, timeout: float = 60):
        super().__init__(timeout=timeout)
        self.author_id = author_id
        self.add_item(PurgeAmountSelect())
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            error_embed = discord.Embed(
                title="⚠️ **Acceso Denegado**",
                description="Solo el usuario que ejecutó el comando puede usar este menú.",
                color=0xe74c3c
            )
            error_embed.set_footer(text="✨ • Lux By _.aari._")
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return False
        return True
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True


class PurgeCog(commands.Cog, name="purge command"):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="purge",
        description="Eliminar mensajes del canal"
    )
    @discord.default_permissions(manage_messages=True)
    async def slash_purge(
        self, 
        ctx: discord.ApplicationContext,
        cantidad: Option(
            int,
            description="Número de mensajes a eliminar (1-100). Deja vacío para ver el menú.",
            required=False,
            min_value=1,
            max_value=100
        ) = None
    ):
        if cantidad is not None:
            await ctx.defer()
            deleted = await ctx.channel.purge(limit=cantidad)
            
            success_embed = discord.Embed(
                title="✅ **Mensajes Eliminados**",
                description=f"Se han eliminado **{len(deleted)}** mensajes correctamente.",
                color=0x2ecc71,
                timestamp=datetime.now()
            )
            success_embed.add_field(
                name="📊 Detalles",
                value=f"**Canal:** {ctx.channel.mention}\n**Ejecutado por:** {ctx.author.mention}",
                inline=False
            )
            success_embed.set_footer(text="✨ • Lux By _.aari._")
            await ctx.respond(embed=success_embed, delete_after=5)
            return
        
        embed = discord.Embed(
            title="🗑️ **Eliminar Mensajes**",
            description="Selecciona la cantidad de mensajes que deseas eliminar del canal.",
            color=0x9b59b6,
            timestamp=datetime.now()
        )
        embed.add_field(
            name="📌 Información",
            value=(
                "• Usa el menú desplegable para seleccionar la cantidad\n"
                "• Los mensajes de más de 14 días no pueden ser eliminados\n"
                "• Esta acción es irreversible"
            ),
            inline=False
        )
        embed.add_field(
            name="💡 Uso Alternativo",
            value="También puedes usar: `/purge cantidad:15`",
            inline=False
        )
        embed.set_footer(text="✨ • Lux By _.aari._ • Expira en 60 segundos")
        
        view = PurgeView(author_id=ctx.author.id)
        await ctx.respond(embed=embed, view=view)

    @commands.command(name='purge', aliases=['clear', 'limpiar', 'borrar', 'eliminar'])
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = None):
        if amount is not None:
            if amount < 1:
                error_embed = discord.Embed(
                    title="⚠️ **Error**",
                    description="La cantidad debe ser mayor a 0.",
                    color=0xe74c3c
                )
                error_embed.set_footer(text="✨ • Lux By _.aari._")
                return await ctx.send(embed=error_embed, delete_after=5)
            
            if amount > 100:
                error_embed = discord.Embed(
                    title="⚠️ **Error**",
                    description="Solo puedes eliminar hasta 100 mensajes a la vez.",
                    color=0xe74c3c
                )
                error_embed.set_footer(text="✨ • Lux By _.aari._")
                return await ctx.send(embed=error_embed, delete_after=5)
            
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=amount)
            
            success_embed = discord.Embed(
                title="✅ **Mensajes Eliminados**",
                description=f"Se han eliminado **{len(deleted)}** mensajes correctamente.",
                color=0x2ecc71,
                timestamp=datetime.now()
            )
            success_embed.add_field(
                name="📊 Detalles",
                value=f"**Canal:** {ctx.channel.mention}\n**Ejecutado por:** {ctx.author.mention}",
                inline=False
            )
            success_embed.set_footer(text="✨ • Lux By _.aari._")
            confirmation = await ctx.send(embed=success_embed)
            await confirmation.delete(delay=5)
            return
        
        embed = discord.Embed(
            title="🗑️ **Eliminar Mensajes**",
            description="Selecciona la cantidad de mensajes que deseas eliminar del canal.",
            color=0x9b59b6,
            timestamp=datetime.now()
        )
        embed.add_field(
            name="📌 Información",
            value=(
                "• Usa el menú desplegable para seleccionar la cantidad\n"
                "• Los mensajes de más de 14 días no pueden ser eliminados\n"
                "• Esta acción es irreversible"
            ),
            inline=False
        )
        embed.add_field(
            name="💡 Uso Alternativo",
            value=f"También puedes usar: `{self.bot.command_prefix}purge <cantidad>`\nEjemplo: `{self.bot.command_prefix}purge 15`",
            inline=False
        )
        embed.set_footer(text="✨ • Lux By _.aari._ • Expira en 60 segundos")
        
        view = PurgeView(author_id=ctx.author.id)
        await ctx.message.delete()
        message = await ctx.send(embed=embed, view=view)
        
        await view.wait()
        
        try:
            await message.edit(view=None)
        except discord.NotFound:
            pass


def setup(bot):
    bot.add_cog(PurgeCog(bot))
