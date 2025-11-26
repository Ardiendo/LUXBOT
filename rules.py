import discord
from discord.ext import commands
from discord import ui
from datetime import datetime

# Rules templates in Spanish and English
RULES_TEMPLATES = {
    "formal": {
        "es": {
            "title": "📋 **REGLAS DEL SERVIDOR** - Formal",
            "rules": [
                ("1️⃣ Respeto", "Trata a todos los miembros con respeto. No se tolera el acoso, insultos o discriminación de ningún tipo."),
                ("2️⃣ Lenguaje", "Usa un lenguaje apropiado. Se prohíben las palabras ofensivas, insultos y contenido explícito."),
                ("3️⃣ Spam", "No hagas spam. Evita mensajes repetitivos, menciones innecesarias y enlaces no autorizados."),
                ("4️⃣ Contenido", "No compartas contenido ilegal, pornográfico o violento. Respeta los derechos de autor."),
                ("5️⃣ Política", "Se permite discutir temas, pero de forma respetuosa. Evita conflictos relacionados con política."),
                ("6️⃣ Publicidad", "La publicidad no autorizada está prohibida. Contacta a los administradores para promociones."),
                ("7️⃣ Canales", "Respeta el propósito de cada canal. Lee las descripciones antes de publicar."),
                ("8️⃣ Bots", "No abuses de los bots del servidor. Úsalos de forma responsable en los canales correctos."),
            ]
        },
        "en": {
            "title": "📋 **SERVER RULES** - Formal",
            "rules": [
                ("1️⃣ Respect", "Treat all members with respect. Harassment, insults, and discrimination are not tolerated."),
                ("2️⃣ Language", "Use appropriate language. Offensive words, insults, and explicit content are prohibited."),
                ("3️⃣ Spam", "No spamming. Avoid repetitive messages, unnecessary mentions, and unauthorized links."),
                ("4️⃣ Content", "Do not share illegal, pornographic, or violent content. Respect intellectual property rights."),
                ("5️⃣ Politics", "Discussion is allowed, but respectfully. Avoid political conflicts and heated debates."),
                ("6️⃣ Advertising", "Unauthorized advertising is prohibited. Contact admins for promotions."),
                ("7️⃣ Channels", "Respect the purpose of each channel. Read descriptions before posting."),
                ("8️⃣ Bots", "Do not abuse server bots. Use them responsibly in the correct channels."),
            ]
        }
    },
    "permisiva": {
        "es": {
            "title": "😊 **REGLAS DEL SERVIDOR** - Permisiva",
            "rules": [
                ("1️⃣ Diversión", "¡Diviértete! Este es un lugar para relajarse y pasar un buen rato con amigos."),
                ("2️⃣ Respeto Básico", "Se amable. Todos merecemos ser tratados con consideración y sin burlas."),
                ("3️⃣ Sin Spam Extremo", "No hagas spam descontrolado. Los memes están permitidos en canales apropiados."),
                ("4️⃣ Contenido Sensible", "Evita compartir contenido muy gráfico. Avisa si vas a compartir algo potencialmente molesto."),
                ("5️⃣ Discusiones Relajadas", "Las opiniones son bienvenidas. Mantén un tono amigable incluso en desacuerdos."),
                ("6️⃣ Promociones Moderadas", "Puedes mencionar proyectos personales. Pregunta a los mods si tienes dudas."),
                ("7️⃣ Usa los Canales Correctos", "Intenta publicar en el canal apropiado, pero no es crítico."),
                ("8️⃣ Disfruta", "El objetivo es pasar un rato agradable. ¡Bienvenido al servidor!"),
            ]
        },
        "en": {
            "title": "😊 **SERVER RULES** - Permissive",
            "rules": [
                ("1️⃣ Have Fun", "Enjoy yourself! This is a place to relax and have a good time with friends."),
                ("2️⃣ Basic Respect", "Be kind. Everyone deserves to be treated with consideration and without mockery."),
                ("3️⃣ No Extreme Spam", "Don't go overboard with spam. Memes are allowed in appropriate channels."),
                ("4️⃣ Sensitive Content", "Avoid sharing very graphic content. Warn if you're sharing something potentially upsetting."),
                ("5️⃣ Relaxed Discussions", "Opinions are welcome. Keep a friendly tone even in disagreements."),
                ("6️⃣ Moderate Promotions", "You can mention personal projects. Ask mods if you have doubts."),
                ("7️⃣ Use Correct Channels", "Try to post in the appropriate channel, but it's not critical."),
                ("8️⃣ Enjoy", "The goal is to have a nice time. Welcome to the server!"),
            ]
        }
    },
    "estrictas": {
        "es": {
            "title": "🛡️ **REGLAS DEL SERVIDOR** - Estrictas",
            "rules": [
                ("1️⃣ Respeto Absoluto", "Trato respetuoso obligatorio. Cualquier falta causará acciones disciplinarias inmediatas."),
                ("2️⃣ Sin Excepciones", "El lenguaje ofensivo, bromas sobre grupos y discriminación resulta en expulsión."),
                ("3️⃣ Cero Tolerancia Spam", "Incluso un spam ligero puede resultar en silencio o expulsión según la gravedad."),
                ("4️⃣ Contenido Prohibido", "Contenido ilegal, NSFW o violento: expulsión permanente. No hay excepciones."),
                ("5️⃣ Debates Controlados", "Los debates deben ser constructivos. Los conflictos políticos resultan en sanciones."),
                ("6️⃣ Sin Publicidad", "La publicidad no autorizada resulta en expulsión inmediata. Sin advertencia previa."),
                ("7️⃣ Canales Designados", "Posteando fuera de canales designados: silencio automático y posible expulsión."),
                ("8️⃣ Vigilancia Activa", "Los mods supervisan constantemente. Las violaciones serán documentadas y ejecutadas."),
            ]
        },
        "en": {
            "title": "🛡️ **SERVER RULES** - Strict",
            "rules": [
                ("1️⃣ Absolute Respect", "Respectful treatment mandatory. Any violation will result in immediate disciplinary action."),
                ("2️⃣ No Exceptions", "Offensive language, jokes about groups, and discrimination result in removal."),
                ("3️⃣ Zero Tolerance Spam", "Even light spam can result in mute or removal depending on severity."),
                ("4️⃣ Prohibited Content", "Illegal, NSFW, or violent content: permanent ban. No exceptions."),
                ("5️⃣ Controlled Debates", "Debates must be constructive. Political conflicts result in sanctions."),
                ("6️⃣ No Advertising", "Unauthorized advertising results in immediate removal. No prior warning."),
                ("7️⃣ Designated Channels", "Posting outside designated channels: automatic mute and possible removal."),
                ("8️⃣ Active Monitoring", "Mods monitor constantly. Violations will be documented and enforced."),
            ]
        }
    }
}

class CustomTitleModal(ui.Modal):
    def __init__(self, rule_type: str, language: str):
        super().__init__(title="Personalizar Título")
        self.rule_type = rule_type
        self.language = language
        
        self.add_item(ui.InputText(
            label="Nuevo Título",
            placeholder="Ingresa el título personalizado para las reglas",
            required=True,
            max_length=256
        ))
    
    async def callback(self, interaction: discord.Interaction):
        custom_title = self.children[0].value
        await interaction.response.defer()
        await self.send_custom_rules(interaction, self.rule_type, self.language, custom_title)
    
    async def send_custom_rules(self, interaction: discord.Interaction, rule_type: str, language: str, custom_title: str):
        template = RULES_TEMPLATES[rule_type][language]
        
        embed = discord.Embed(
            title=custom_title,
            color=self._get_color(rule_type),
            timestamp=datetime.now()
        )
        
        for field_name, field_value in template["rules"]:
            embed.add_field(name=field_name, value=field_value, inline=False)
        
        embed.set_footer(text="✨ • Lux By _.aari._")
        
        try:
            await interaction.followup.send(embed=embed)
        except discord.NotFound:
            await interaction.response.send_message(embed=embed)
    
    def _get_color(self, rule_type: str) -> int:
        colors = {
            "formal": 0x3498db,
            "permisiva": 0xf1c40f,
            "estrictas": 0xe74c3c
        }
        return colors.get(rule_type, 0x9b59b6)

class RulesSelect(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Formal (ES/EN)",
                value="formal",
                emoji="📋",
                description="Reglas formales y estructuradas"
            ),
            discord.SelectOption(
                label="Permisiva (ES/EN)",
                value="permisiva",
                emoji="😊",
                description="Reglas relajadas y amigables"
            ),
            discord.SelectOption(
                label="Estrictas (ES/EN)",
                value="estrictas",
                emoji="🛡️",
                description="Reglas severas con cero tolerancia"
            ),
        ]
        
        super().__init__(
            placeholder="Selecciona el tipo de reglas...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        rule_type = self.values[0]
        view = LanguageView(rule_type)
        await interaction.followup.send("Ahora selecciona el idioma:", view=view, ephemeral=True)

class LanguageView(ui.View):
    def __init__(self, rule_type):
        super().__init__()
        self.rule_type = rule_type
    
    @ui.button(label="Español", emoji="🇪🇸", style=discord.ButtonStyle.primary)
    async def spanish_button(self, button: ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.send_rules(interaction, self.rule_type, "es")
    
    @ui.button(label="English", emoji="🇺🇸", style=discord.ButtonStyle.primary)
    async def english_button(self, button: ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.send_rules(interaction, self.rule_type, "en")
    
    @ui.button(label="Customizar Título", emoji="✏️", style=discord.ButtonStyle.secondary)
    async def customize_button(self, button: ui.Button, interaction: discord.Interaction):
        # Ask for language first
        view = CustomLanguageView(self.rule_type)
        await interaction.response.send_message("¿En qué idioma?", view=view, ephemeral=True)
    
    async def send_rules(self, interaction: discord.Interaction, rule_type: str, language: str):
        template = RULES_TEMPLATES[rule_type][language]
        
        embed = discord.Embed(
            title=template["title"],
            color=self._get_color(rule_type),
            timestamp=datetime.now()
        )
        
        for field_name, field_value in template["rules"]:
            embed.add_field(name=field_name, value=field_value, inline=False)
        
        embed.set_footer(text="✨ • Lux By _.aari._")
        
        try:
            await interaction.followup.send(embed=embed)
        except discord.NotFound:
            await interaction.response.send_message(embed=embed)
    
    def _get_color(self, rule_type: str) -> int:
        colors = {
            "formal": 0x3498db,      # Blue
            "permisiva": 0xf1c40f,   # Yellow
            "estrictas": 0xe74c3c    # Red
        }
        return colors.get(rule_type, 0x9b59b6)

class CustomLanguageView(ui.View):
    def __init__(self, rule_type):
        super().__init__()
        self.rule_type = rule_type
    
    @ui.button(label="Español", emoji="🇪🇸", style=discord.ButtonStyle.primary)
    async def spanish_custom(self, button: ui.Button, interaction: discord.Interaction):
        modal = CustomTitleModal(self.rule_type, "es")
        await interaction.response.send_modal(modal)
    
    @ui.button(label="English", emoji="🇺🇸", style=discord.ButtonStyle.primary)
    async def english_custom(self, button: ui.Button, interaction: discord.Interaction):
        modal = CustomTitleModal(self.rule_type, "en")
        await interaction.response.send_modal(modal)

class RulesView(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(RulesSelect())

class RulesCog(commands.Cog, name="rules command"):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command(
        name="rules",
        description="Display server rules with configurable style and language"
    )
    @discord.default_permissions(moderate_members=True)
    async def rules(self, ctx: discord.ApplicationContext):
        """Display server rules - Moderators can choose style and language"""
        embed = discord.Embed(
            title="📖 **SERVIDOR RULES**",
            description="Selecciona el tipo de reglas que deseas mostrar:",
            color=0x9b59b6,
            timestamp=datetime.now()
        )
        embed.add_field(
            name="📋 Formal",
            value="Reglas estructuradas y profesionales",
            inline=False
        )
        embed.add_field(
            name="😊 Permisiva",
            value="Reglas relajadas y amigables",
            inline=False
        )
        embed.add_field(
            name="🛡️ Estrictas",
            value="Reglas severas con cero tolerancia",
            inline=False
        )
        embed.set_footer(text="✨ • Lux By _.aari._")
        
        view = RulesView()
        await ctx.respond(embed=embed, view=view, ephemeral=True)

def setup(bot):
    bot.add_cog(RulesCog(bot))
