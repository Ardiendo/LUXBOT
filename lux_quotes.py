"""
Sistema de frases graciosas de Lux (League of Legends)
Frases temáticas para errores, eventos y menciones del bot
"""

import random

# Frases de ERROR - cuando algo sale mal
ERROR_QUOTES = [
    "¡Ay! Parece que mi brillo se ha apagado... 🌟⚫",
    "Mi magia no fue suficiente esta vez... 💫😞",
    "¡Oh no! La oscuridad ha ganado... 🌑💔",
    "Mi forma final falló... ¿Qué pasó? 😭⚡",
    "¡Luz dissipada! Un error ha ocurrido... ⚡✨",
    "¡Prisma roto! El sistema necesita reparación 💎🔨",
    "La magia falló... Mi poder es insuficiente 😔🌑",
    "¡Rayos! Algo no salió según el plan... ⚠️🔥",
    "Mi poder ha sido bloqueado por un error... 🚫⛓️",
    "¡La luz se apagó! Error crítico detectado 💥🌑",
]

# Frases de ÉXITO - cuando algo funciona bien
SUCCESS_QUOTES = [
    "¡Finalización perfecta! ✨🌟🎉",
    "¡Luz radiante! Todo está perfecto ✨💫",
    "¡Forma final activada! Misión cumplida 🔮💎",
    "¡Prisma de poder liberado! Éxito garantizado 🎯⚡",
    "¡Mi brillo ilumina el camino! ✅🌠",
    "¡Soy la luz eterna! Objetivo completado 🔆🌟",
    "¡La oscuridad retrocede! Victoria asegurada 🏆✨",
    "¡Poder absoluto! Todo funciona perfectamente ⚡💫",
    "¡El brillo triunfa! Éxito confirmado 🌠🎆",
    "¡Destello de genio! Perfección lograda 🎨✨",
]

# Frases de ADVERTENCIA - cuando hay un problema menor
WARNING_QUOTES = [
    "Cuidado... Siento algo extraño en el aire 👀🔮",
    "¡Espera! Algo no se ve bien... 🤔💡",
    "Precaución recomendada, amigo mío 📍⚠️",
    "Hmm... algo podría salir mal aquí ⚠️😰",
    "Mi instinto mágico me advierte... 🔮💫",
    "¡Alto! Verifica esto dos veces 🛑✋",
    "El brillo parpadea... ten cuidado 💡⚡",
    "¡Atención! Las sombras se ciernen 🌑👁️",
    "Algo me dice que esto podría fallar 😰🌑",
    "¡Detén! Posible peligro detectado ⚡🚫",
]

# Frases de CARGA - eventos largos
LOADING_QUOTES = [
    "Estoy canalizando mi poder... espera 🔄✨",
    "Mi magia está trabajando... 💫🔮",
    "Cargando el prisma de poder... 💎⚡",
    "Las dimensiones se están alineando... 🌌✨",
    "Mi forma final está casi lista... ⚡🔥",
    "Los rayos están convergiendo... 🔆💫",
    "Reuniendo la esencia de la luz... 💎🌟",
    "Canalizando poder cósmico... 🌠✨",
    "Mi brillo se intensifica... 🌟💥",
    "El prisma se está formando... 🎆💎",
]

# Frases para menciones/tags
TAG_QUOTES = [
    "Aquí está tu luz radiante 🌟✨",
    "¿Me llamaste? Aquí estoy ✨🔮",
    "¡Tu ayudante mágica al rescate! 💫🌠",
    "Brillas con tu llamada... 🔆⭐",
    "¡Mi turno de brillar! ⚡✨",
    "¡Finalización perfecta, tu hora ha llegado! 🎯🌟",
    "Respondiendo a tu llamada... 🌠💫",
    "¡La luz te ilumina! 💡🌈",
    "Mi prisma está listo para ti 🔮💎",
    "¡Genio a tu servicio! 🧠✨",
]

# Frases para cuando algo se ejecuta rápido
FAST_QUOTES = [
    "¡Velocidad de la luz! 💨⚡",
    "¡Instantáneamente perfecto! ⚡✨",
    "¡Más rápido que un destello! 🔆💫",
    "¡Rayos en acción! ¡Bang! 💥⚡",
    "¡Instantáneo como mi poder! 🌟💨",
    "¡Velocidad mágica activada! 🏃✨",
    "¡Rápido como la luz! 🌠⚡",
    "¡En un abrir y cerrar de ojos! 👁️✨",
]

def get_error_quote() -> str:
    """Obtiene una frase aleatoria de error"""
    return random.choice(ERROR_QUOTES)

def get_success_quote() -> str:
    """Obtiene una frase aleatoria de éxito"""
    return random.choice(SUCCESS_QUOTES)

def get_warning_quote() -> str:
    """Obtiene una frase aleatoria de advertencia"""
    return random.choice(WARNING_QUOTES)

def get_loading_quote() -> str:
    """Obtiene una frase aleatoria de carga"""
    return random.choice(LOADING_QUOTES)

def get_tag_quote() -> str:
    """Obtiene una frase aleatoria para menciones"""
    return random.choice(TAG_QUOTES)

def get_fast_quote() -> str:
    """Obtiene una frase aleatoria para ejecuciones rápidas"""
    return random.choice(FAST_QUOTES)
