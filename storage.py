import json
import os
from datetime import datetime

TICKETS_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'tickets_config.json')
TICKETS_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'tickets_data.json')

def ensure_files_exist():
    """Crear archivos si no existen"""
    os.makedirs(os.path.dirname(TICKETS_CONFIG_PATH), exist_ok=True)
    
    if not os.path.exists(TICKETS_CONFIG_PATH):
        with open(TICKETS_CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump({"guilds": {}}, f, indent=4, ensure_ascii=False)
    
    if not os.path.exists(TICKETS_DATA_PATH):
        with open(TICKETS_DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump({"tickets": []}, f, indent=4, ensure_ascii=False)

def load_ticket_config():
    """Cargar configuración de tickets"""
    ensure_files_exist()
    try:
        with open(TICKETS_CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"guilds": {}}

def save_ticket_config(config):
    """Guardar configuración de tickets"""
    ensure_files_exist()
    with open(TICKETS_CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def load_tickets_data():
    """Cargar datos de tickets"""
    ensure_files_exist()
    try:
        with open(TICKETS_DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"tickets": []}

def save_tickets_data(data):
    """Guardar datos de tickets"""
    ensure_files_exist()
    with open(TICKETS_DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def set_ticket_channel(guild_id, channel_id):
    """Configurar canal de tickets para un servidor"""
    config = load_ticket_config()
    if "guilds" not in config:
        config["guilds"] = {}
    config["guilds"][str(guild_id)] = {"channel_id": channel_id}
    save_ticket_config(config)

def get_ticket_channel(guild_id):
    """Obtener canal de tickets configurado"""
    config = load_ticket_config()
    return config.get("guilds", {}).get(str(guild_id), {}).get("channel_id")

def create_ticket(guild_id, channel_id, user_id, reason):
    """Crear nuevo ticket"""
    data = load_tickets_data()
    ticket_id = len(data["tickets"]) + 1
    
    ticket = {
        "ticket_id": ticket_id,
        "guild_id": guild_id,
        "channel_id": channel_id,
        "user_id": user_id,
        "reason": reason,
        "status": "open",
        "created_at": datetime.now().isoformat(),
        "closed_at": None,
        "claimed_by": None
    }
    
    data["tickets"].append(ticket)
    save_tickets_data(data)
    return ticket_id

def close_ticket(channel_id):
    """Cerrar un ticket"""
    data = load_tickets_data()
    for ticket in data["tickets"]:
        if ticket["channel_id"] == channel_id and ticket["status"] == "open":
            ticket["status"] = "closed"
            ticket["closed_at"] = datetime.now().isoformat()
            break
    save_tickets_data(data)

def claim_ticket(channel_id, staff_id):
    """Reclamar un ticket para un staff"""
    data = load_tickets_data()
    for ticket in data["tickets"]:
        if ticket["channel_id"] == channel_id and ticket["status"] == "open":
            ticket["claimed_by"] = staff_id
            break
    save_tickets_data(data)

def get_ticket_by_channel(channel_id):
    """Obtener ticket por canal"""
    data = load_tickets_data()
    for ticket in data["tickets"]:
        if ticket["channel_id"] == channel_id:
            return ticket
    return None
