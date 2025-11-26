import os
import discord
from discord.ext import commands
from discord import Option
from datetime import datetime
import json
import random
from src.utils.discord_tools.embeds import create_banner_embed, set_footer_with_author
from src.utils.discord_tools.stats_view import StatsView


class StatsCog(commands.Cog, name="stats command"):
    def __init__(self, bot):
        self.bot = bot
    
    async def get_role_counts(self, ctx):
        try:
            roles_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "roles.json")
            with open(roles_path, "r") as f:
                data = json.load(f)
            
            if "guilds" not in data:
                data["guilds"] = {}
            
            guild_id_str = str(ctx.guild.id)
            guild_roles = data["guilds"].get(guild_id_str, [])
            
            role_counts = {}
            for reward in guild_roles:
                role = ctx.guild.get_role(reward["id"])
                if role:
                    count = len([m for m in ctx.guild.members if role in m.roles])
                    role_counts[reward["level"]] = {
                        "role": role,
                        "count": count
                    }
            return role_counts
        except Exception as e:
            print(f"Error getting role counts: {e}")
            return {}
    
    @discord.slash_command(
        name="stats",
        description="Ver estadísticas del servidor"
    )
    async def slash_stats(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        
        if not ctx.guild:
            return
        
        role_counts = await self.get_role_counts(ctx)
        
        random_color = random.randint(0x000000, 0xFFFFFF)
        
        embed = discord.Embed(
            title="📊 **ESTADÍSTICAS DEL SERVIDOR**",
            description=f"Detalles de **{ctx.guild.name}**",
            color=random_color,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="👥 Miembros",
            value=f"**{ctx.guild.member_count:,}**",
            inline=True
        )
        embed.add_field(
            name="🎭 Roles",
            value=f"**{len(ctx.guild.roles):,}**",
            inline=True
        )
        embed.add_field(
            name="📢 Canales",
            value=f"**{len(ctx.guild.channels):,}**",
            inline=True
        )
        
        embed.add_field(
            name="━━━━━━━━━━━━━━━━━━━━━━",
            value="",
            inline=False
        )
        
        if role_counts:
            sorted_rewards = sorted(role_counts.items(), key=lambda x: x[0])
            total_with_rewards = sum(data["count"] for _, data in sorted_rewards)
            
            rewards_text = ""
            for level, data in sorted_rewards[:10]:
                role = data["role"]
                count = data["count"]
                rewards_text += f"**Nivel {level}** → {role.mention} `({count})`\n"
            
            embed.add_field(
                name="🏆 Recompensas de Nivel",
                value=rewards_text,
                inline=False
            )
            
            embed.add_field(
                name="📈 Total con Recompensas",
                value=f"**{total_with_rewards}** usuarios tienen roles de recompensa",
                inline=False
            )
        else:
            embed.add_field(
                name="🏆 Recompensas de Nivel",
                value="⚠️ No hay recompensas configuradas.\nUsa `/add` para añadir recompensas.",
                inline=False
            )
        
        embed.add_field(
            name="━━━━━━━━━━━━━━━━━━━━━━",
            value="",
            inline=False
        )
        
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        
        if self.bot.user and self.bot.user.banner:
            embed.set_image(url=self.bot.user.banner.url)
        
        embed = set_footer_with_author(embed)
        
        view = StatsView(self.bot, ctx)
        await ctx.respond(embed=embed, view=view)


def setup(bot):
    bot.add_cog(StatsCog(bot))
