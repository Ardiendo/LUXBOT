"""
Sistema de almacenamiento para la economía del bot
Maneja balance, inventario y XP de usuarios
"""
import json
from datetime import datetime
from typing import Dict, List, Optional
from src.utils.paths import ECONOMY_DATA

ECONOMY_DATA_PATH = str(ECONOMY_DATA)

# Cooldown para ganar XP (en segundos)
XP_COOLDOWN = 60  # 1 minuto
_last_xp_gain: Dict[int, float] = {}


def ensure_economy_file():
    """Asegurar que el archivo de economía existe"""
    if not ECONOMY_DATA.exists():
        with open(ECONOMY_DATA, 'w', encoding='utf-8') as f:
            json.dump({"users": {}}, f, indent=4, ensure_ascii=False)


def load_economy_data() -> dict:
    """Cargar datos de economía"""
    ensure_economy_file()
    try:
        with open(ECONOMY_DATA, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"users": {}}


def save_economy_data(data: dict):
    """Guardar datos de economía"""
    ensure_economy_file()
    with open(ECONOMY_DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_user_data(user_id: int) -> dict:
    """Obtener datos de un usuario"""
    data = load_economy_data()
    user_id_str = str(user_id)
    
    if user_id_str not in data["users"]:
        data["users"][user_id_str] = {
            "balance": 0,
            "inventory": [],
            "xp": 0,
            "level": 0,
            "last_daily": None
        }
        save_economy_data(data)
    
    return data["users"][user_id_str]


def get_user_balance(user_id: int) -> int:
    """Obtener balance de un usuario"""
    user_data = get_user_data(user_id)
    return user_data.get("balance", 0)


def set_user_balance(user_id: int, balance: int):
    """Establecer balance de un usuario"""
    data = load_economy_data()
    user_id_str = str(user_id)
    
    if user_id_str not in data["users"]:
        get_user_data(user_id)
    
    data["users"][user_id_str]["balance"] = balance
    save_economy_data(data)


def add_balance(user_id: int, amount: int) -> int:
    """Agregar balance a un usuario"""
    current = get_user_balance(user_id)
    new_balance = current + amount
    set_user_balance(user_id, new_balance)
    return new_balance


def remove_balance(user_id: int, amount: int) -> bool:
    """Remover balance de un usuario (retorna True si fue exitoso)"""
    current = get_user_balance(user_id)
    if current >= amount:
        set_user_balance(user_id, current - amount)
        return True
    return False


def get_user_inventory(user_id: int) -> Dict[str, int]:
    """Obtener inventario de un usuario como diccionario {item_id: count}"""
    user_data = get_user_data(user_id)
    inventory = user_data.get("inventory", [])
    
    # Convertir lista a diccionario
    result = {}
    for item in inventory:
        item_id = item.get("id", "")
        if item_id:
            result[item_id] = result.get(item_id, 0) + 1
    
    return result


def add_item_to_inventory(user_id: int, item_id: str, item_name: str = "", item_emoji: str = ""):
    """Agregar item al inventario"""
    data = load_economy_data()
    user_id_str = str(user_id)
    
    if user_id_str not in data["users"]:
        get_user_data(user_id)
    
    if "inventory" not in data["users"][user_id_str]:
        data["users"][user_id_str]["inventory"] = []
    
    item = {
        "id": item_id,
        "name": item_name or item_id,
        "emoji": item_emoji,
        "acquired": datetime.now().isoformat()
    }
    
    data["users"][user_id_str]["inventory"].append(item)
    save_economy_data(data)


def can_gain_xp(user_id: int) -> bool:
    """Verificar si el usuario puede ganar XP (cooldown)"""
    import time
    current_time = time.time()
    
    if user_id not in _last_xp_gain:
        _last_xp_gain[user_id] = current_time
        return True
    
    time_since_last = current_time - _last_xp_gain[user_id]
    if time_since_last >= XP_COOLDOWN:
        _last_xp_gain[user_id] = current_time
        return True
    
    return False


def get_user_xp(user_id: int) -> dict:
    """Obtener datos de XP de un usuario"""
    user_data = get_user_data(user_id)
    xp = user_data.get("xp", 0)
    level = user_data.get("level", 0)
    
    # Calcular XP necesario para el siguiente nivel
    next_level_xp = (level + 1) * 100
    level_xp = xp % 100 if level > 0 else xp
    
    return {
        "level": level,
        "total_xp": xp,
        "level_xp": level_xp,
        "next_level_xp": next_level_xp
    }


def add_xp(user_id: int, amount: int) -> dict:
    """Agregar XP a un usuario y retornar información del nivel"""
    data = load_economy_data()
    user_id_str = str(user_id)
    
    if user_id_str not in data["users"]:
        get_user_data(user_id)
    
    current_xp = data["users"][user_id_str].get("xp", 0)
    current_level = data["users"][user_id_str].get("level", 0)
    
    new_xp = current_xp + amount
    new_level = new_xp // 100
    
    level_up = new_level > current_level
    
    data["users"][user_id_str]["xp"] = new_xp
    data["users"][user_id_str]["level"] = new_level
    
    save_economy_data(data)
    
    return {
        "level_up": level_up,
        "level": new_level,
        "total_xp": new_xp,
        "level_xp": new_xp % 100
    }
