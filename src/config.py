"""
Módulo de configuración para el chat-game
Maneja la carga y actualización de configuraciones
"""
import json
import os
import threading

# Lock para operaciones de configuración
config_lock = threading.Lock()

# Valores por defecto
DEFAULT_CONFIG = {
    "command_cooldown_seconds": 200,
    "command_history_limit": 10
}

# Variable global para almacenar la configuración cargada
_config_cache = None

def get_config_path() -> str:
    """
    Obtiene la ruta del archivo de configuración
    Guarda en AppData para que sea accesible al usuario final

    Returns:
        str: Ruta absoluta al archivo config.json
    """
    # Obtener ruta de AppData (mismo lugar donde se guarda el historial)
    appdata = os.getenv('APPDATA')

    if appdata:
        # Usuario final (Windows) - guardar en AppData
        game_dir = os.path.join(appdata, 'chat-game')
        os.makedirs(game_dir, exist_ok=True)
        config_path = os.path.join(game_dir, 'config.json')
    else:
        # Desarrollo o sistemas sin AppData - guardar en la raíz del proyecto
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        config_path = os.path.join(project_root, 'config.json')

    return config_path

def load_config() -> dict:
    """
    Carga la configuración desde el archivo config.json
    Si no existe, crea uno con valores por defecto

    Returns:
        dict: Diccionario con la configuración
    """
    global _config_cache

    with config_lock:
        config_path = get_config_path()

        try:
            # Intentar cargar el archivo de configuración
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Validar que tenga las claves necesarias
            for key in DEFAULT_CONFIG:
                if key not in config:
                    config[key] = DEFAULT_CONFIG[key]

            _config_cache = config
            return config

        except FileNotFoundError:
            # Si no existe, crear el archivo con valores por defecto
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_CONFIG, f, indent=2)
            _config_cache = DEFAULT_CONFIG.copy()
            return _config_cache

        except json.JSONDecodeError:
            # Si el archivo está corrupto, usar valores por defecto
            print("⚠️  Archivo de configuración corrupto, usando valores por defecto")
            _config_cache = DEFAULT_CONFIG.copy()
            return _config_cache

def get_config() -> dict:
    """
    Obtiene la configuración actual (usa caché si está disponible)

    Returns:
        dict: Diccionario con la configuración
    """
    global _config_cache

    if _config_cache is None:
        return load_config()
    return _config_cache

def get_command_cooldown() -> float:
    """
    Obtiene el tiempo de cooldown configurado para los comandos

    Returns:
        float: Tiempo en segundos
    """
    config = get_config()
    return float(config.get("command_cooldown_seconds", DEFAULT_CONFIG["command_cooldown_seconds"]))

def get_command_history_limit() -> int:
    """
    Obtiene el límite de comandos en el historial

    Returns:
        int: Número máximo de comandos en el historial
    """
    config = get_config()
    return int(config.get("command_history_limit", DEFAULT_CONFIG["command_history_limit"]))

def update_config(key: str, value) -> bool:
    """
    Actualiza un valor de configuración y lo guarda en el archivo

    Args:
        key: Clave de configuración a actualizar
        value: Nuevo valor

    Returns:
        bool: True si se actualizó correctamente, False en caso contrario
    """
    global _config_cache

    with config_lock:
        try:
            config = get_config()
            config[key] = value

            # Guardar en el archivo
            config_path = get_config_path()
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)

            _config_cache = config
            return True

        except Exception as e:
            print(f"⚠️  Error al actualizar configuración: {e}")
            return False

def reload_config():
    """
    Recarga la configuración desde el archivo
    Útil si se modificó el archivo manualmente
    """
    global _config_cache
    _config_cache = None
    load_config()

def print_config_location():
    """
    Muestra la ubicación del archivo de configuración
    Útil para que el usuario sepa dónde editarlo
    """
    config_path = get_config_path()
    print(f"📋 Archivo de configuración: {config_path}")
    return config_path
