# 📁 Estructura del Proyecto Lux Bot

## Organización del Proyecto

```
LUXBOT/
├── src/                          # Código fuente principal
│   ├── bot/                      # Bot principal
│   │   └── main.py              # Punto de entrada del bot
│   ├── cogs/                     # Módulos de comandos (Cogs)
│   │   ├── admin/                # Comandos de administración
│   │   │   ├── add.py           # Agregar recompensas de rol
│   │   │   ├── remove.py        # Eliminar recompensas
│   │   │   ├── roleRewards.py   # Listar recompensas
│   │   │   ├── backup.py        # Backup de configuración
│   │   │   ├── announce.py      # Anuncios globales
│   │   │   ├── maintenance.py  # Modo mantenimiento
│   │   │   ├── restart.py       # Reiniciar bot
│   │   │   └── removePreviousRewards.py
│   │   ├── economy/             # Sistema de economía
│   │   │   └── storage.py       # Almacenamiento de economía
│   │   ├── moderation/          # Comandos de moderación
│   │   │   ├── moderation.py   # Menú de moderación
│   │   │   └── purge.py        # Eliminar mensajes
│   │   ├── tickets/             # Sistema de tickets
│   │   │   ├── commands.py     # Comandos de tickets
│   │   │   └── storage.py       # Almacenamiento de tickets
│   │   └── utility/             # Comandos de utilidad
│   │       ├── help.py          # Sistema de ayuda
│   │       ├── invite.py        # Información del bot
│   │       ├── stats.py         # Estadísticas del servidor
│   │       ├── userinfo.py      # Información de usuario
│   │       ├── rules.py         # Reglas del servidor
│   │       ├── rank.py          # Ranking de usuarios
│   │       ├── leaderboard.py   # Tabla de clasificación
│   │       ├── onMessage.py     # Listener de mensajes
│   │       ├── task.py          # Tareas programadas
│   │       ├── notifications.py # Sistema de notificaciones
│   │       ├── logs.py          # Sistema de logs
│   │       ├── newembed.py      # Embeds personalizados
│   │       ├── events.py        # Eventos del bot
│   │       ├── error_handler.py # Manejo de errores
│   │       └── testing.py       # Comandos de prueba
│   └── utils/                    # Utilidades
│       ├── paths.py             # Gestión de rutas
│       ├── database.py          # Conexión a base de datos
│       ├── lux_emojis.py        # Emojis del bot
│       ├── lux_quotes.py        # Citas del bot
│       └── discord_tools/        # Herramientas de Discord
│           ├── error_logger.py   # Logger de errores
│           ├── embeds.py        # Utilidades de embeds
│           ├── views.py         # Vistas interactivas
│           ├── embed_builder.py # Constructor de embeds
│           ├── mod_view.py      # Vista de moderación
│           ├── invite_view.py   # Vista de invitación
│           └── stats_view.py    # Vista de estadísticas
├── config/                       # Archivos de configuración
│   ├── configuration.json       # Configuración principal
│   ├── roles.json               # Configuración de roles
│   ├── maintenance_config.json # Configuración de mantenimiento
│   ├── tickets_config.json     # Configuración de tickets
│   ├── tickets_data.json       # Datos de tickets
│   └── newembed_config.json    # Configuración de embeds
├── data/                         # Archivos de datos
│   ├── economy.json             # Datos de economía
│   └── shop.json               # Items de la tienda
├── requirements.txt             # Dependencias Python
├── README.md                    # Documentación principal
├── ESTRUCTURA.md                # Este archivo
├── Privacy & Policy.md          # Política de privacidad
└── Terms & Conditions.md        # Términos y condiciones
```

## Mejoras Implementadas

### 1. ✅ Estructura Organizada
- Separación clara de responsabilidades por carpetas
- Cogs organizados por funcionalidad (admin, economy, moderation, tickets, utility)
- Utilidades centralizadas en `src/utils/`

### 2. ✅ Gestión de Rutas Mejorada
- Módulo `src/utils/paths.py` para centralizar rutas
- Uso de `pathlib.Path` en lugar de concatenación de strings
- Rutas más mantenibles y menos propensas a errores

### 3. ✅ Sistema de Economía
- Archivo `src/cogs/economy/storage.py` creado
- Funciones para manejar balance, inventario y XP
- Integración con el sistema de mensajes

### 4. ✅ Archivos `__init__.py`
- Todos los paquetes Python tienen `__init__.py`
- Facilita imports y estructura modular

### 5. ✅ Mejoras en el Código
- Mejor manejo de errores con try/except específicos
- Encoding UTF-8 en todos los archivos JSON
- Documentación con docstrings
- Type hints donde es apropiado

## Próximos Pasos Recomendados

1. **Actualizar rutas restantes**: Algunos archivos aún usan rutas antiguas
2. **Mejorar manejo de errores**: Agregar logging más detallado
3. **Type hints completos**: Agregar type hints a todas las funciones
4. **Tests**: Crear tests unitarios para funciones críticas
5. **Documentación**: Expandir docstrings y comentarios

## Cómo Ejecutar

```bash
# Desde la raíz del proyecto
python src/bot/main.py
```

## Variables de Entorno Requeridas

- `DISCORD_BOT_TOKEN`: Token del bot de Discord
- `DATABASE_URL`: (Opcional) URL de conexión a PostgreSQL
