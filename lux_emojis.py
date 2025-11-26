"""
Sistema de emojis temáticos de Lux (League of Legends)
Emojis organizados para representar a la Dama de Luminosidad
"""

# ✨ Core Light & Sparkle - Luz y Destellos
SPARKLE_EMOJIS = {
    "sparkles": "✨",
    "star_glow": "🌟",
    "star": "⭐",
    "dizzy": "💫",
    "shooting_star": "🌠",
    "lightning": "⚡",
    "boom": "💥",
    "sun_face": "🌞",
    "sun": "☀️",
    "rainbow": "🌈",
}

# 🔮 Crystal & Magic - Cristal y Magia
CRYSTAL_EMOJIS = {
    "gem": "💎",
    "crystal_ball": "🔮",
    "magic_wand": "🪄",
    "eight_star": "✴️",
    "milky_way": "🌌",
    "crescent_moon": "🌙",
    "first_quarter_moon": "🌛",
}

# 🕯️ Illumination & Light - Iluminación
LIGHT_EMOJIS = {
    "candle": "🕯️",
    "light_bulb": "💡",
    "bright_button": "🔆",
    "sunrise": "🌅",
    "lantern": "🏮",
}

# 🔥 Elementalist Lux Forms - Formas Elementales
ELEMENTALIST_EMOJIS = {
    "fire": "🔥",
    "water": "💧",
    "nature": "🌿",
    "leaf": "🍃",
    "ice": "❄️",
    "lightning_bolt": "⛈️",
    "dark": "🌑",
}

# 🎯 Status & Actions - Estados y Acciones
STATUS_EMOJIS = {
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "loading": "⏳",
    "clock": "🕐",
    "victory": "🏆",
    "shield": "🛡️",
    "sword": "⚔️",
}

# 🎨 Aesthetic & Decorative - Estética y Decoración
AESTHETIC_EMOJIS = {
    "sparkle_heart": "💖✨",
    "magic_emoji": "✨🌟",
    "light_show": "🎆",
    "fireworks": "🎇",
    "crown": "👑",
    "scroll": "📜",
    "book": "📖",
    "wand_spark": "🪄✨",
}

# 🎪 Cosmic & Mystical - Cósmico y Místico
COSMIC_EMOJIS = {
    "cosmic": "🌌✨",
    "nebula": "🌌",
    "dark_matter": "🌑",
    "galaxy": "🌠",
    "moonlight": "🌙✨",
}

# Combined presets for easy use
PRESETS = {
    "classic": f"{SPARKLE_EMOJIS['sparkles']}{SPARKLE_EMOJIS['star_glow']}{SPARKLE_EMOJIS['dizzy']}{SPARKLE_EMOJIS['star']}",
    "cosmic": f"{COSMIC_EMOJIS['cosmic']}{SPARKLE_EMOJIS['shooting_star']}{SPARKLE_EMOJIS['dizzy']}",
    "elementalist": f"{ELEMENTALIST_EMOJIS['fire']}{ELEMENTALIST_EMOJIS['water']}{ELEMENTALIST_EMOJIS['lightning_bolt']}{ELEMENTALIST_EMOJIS['ice']}",
    "final_spark": f"{SPARKLE_EMOJIS['lightning']}{SPARKLE_EMOJIS['boom']}{SPARKLE_EMOJIS['sparkles']}{SPARKLE_EMOJIS['rainbow']}",
    "light_mage": f"{LIGHT_EMOJIS['candle']}{SPARKLE_EMOJIS['sparkles']}{CRYSTAL_EMOJIS['gem']}{CRYSTAL_EMOJIS['crystal_ball']}",
    "power": f"{SPARKLE_EMOJIS['lightning']}{CRYSTAL_EMOJIS['gem']}{SPARKLE_EMOJIS['sparkles']}{SPARKLE_EMOJIS['boom']}",
}

def get_random_sparkle():
    """Obtener un emoji de destello aleatorio"""
    import random
    return random.choice(list(SPARKLE_EMOJIS.values()))

def get_random_element():
    """Obtener un emoji elemental aleatorio"""
    import random
    return random.choice(list(ELEMENTALIST_EMOJIS.values()))

def get_random_cosmic():
    """Obtener un emoji cósmico aleatorio"""
    import random
    return random.choice(list(COSMIC_EMOJIS.values()))

def get_lux_combo():
    """Obtener una combinación de emojis de Lux"""
    import random
    return random.choice(list(PRESETS.values()))
