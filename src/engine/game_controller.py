# Importaciones necesarias
import asyncio
import keyboard
import time
import os
from time import sleep as wait
from pynput.mouse import Button as MouseButton, Controller as MouseController
from engine import commands

# Controlador del mouse
mouse = MouseController()

# Cola de comandos asíncrona
command_queue = asyncio.Queue()

# Diccionario para manejar timeouts de usuarios
users_timeouts = {}

async def add_command(username, raw_command, command):
    """
    Añade un comando a la cola si el usuario no está en timeout

    Args:
        username: Nombre del usuario que envió el comando
        raw_command: Comando original sin procesar
        command: Comando procesado a ejecutar
    """
    print(f"✨ Añadiendo comando a la cola: {command}")
    current_time = time.time()

    # Verificar si el usuario tiene un timeout
    if username in users_timeouts:
        last_command_time = users_timeouts[username]
        if current_time - last_command_time < 600:  # 600 segundos = 10 minutos
            print(f"⏳ {username} debe esperar antes de enviar otro comando")
            return

    # Actualizar el tiempo del último comando del usuario
    users_timeouts[username] = current_time

    # Agregar el comando a la cola
    await command_queue.put(command)
    save_command_history(raw_command)

def save_command_history(command):
    """
    Guarda el historial de comandos en un archivo

    Args:
        command: Comando a guardar en el historial
    """
    # Obtener ruta de AppData
    appdata = os.getenv('APPDATA')
    game_dir = os.path.join(appdata, 'chat-game')
    history_file = os.path.join(game_dir, 'command_history.txt')

    # Crear directorio si no existe
    if not os.path.exists(game_dir):
        os.makedirs(game_dir)

    # Cargar historial existente o crear nuevo
    try:
        with open(history_file, 'r') as f:
            history = f.readlines()
    except (FileNotFoundError):
        history = []

    # Añadir nuevo comando
    history.append(
        f"{command}\n"
    )

    # Mantener solo los últimos 10 comandos
    if len(history) > 10:
        history = history[-10:]

    # Guardar historial actualizado
    with open(history_file, 'w') as f:
        f.writelines(history)

def execute_command():
    """
    Ejecuta el siguiente comando en la cola
    Maneja comandos de mouse, teclas mantenidas y teclas normales
    """
    if not command_queue.empty():
        print("🕛 Esperando comando en la cola...")
        command = command_queue.get_nowait()  # Espera el siguiente comando
        print(f"🕛 Procesando comando: {command}")

        # Procesar comandos de mouse
        if command in commands.MOUSE_COMMANDS.values():
            if command in commands.CAMERA_COMMANDS.values():
                # Mapeo de comandos a coordenadas de movimiento
                movement_map = {
                    "mouse_up": (0, -50),
                    "mouse_down": (0, 50),
                    "mouse_left": (-50, 0),
                    "mouse_right": (50, 0)
                }

                x, y = movement_map[command]
                mouse.move(x, y)
                print(f"🔭 Cámara movida: {command}")
            elif command == "scroll_up":
                mouse.scroll(0, 1)
            elif command == "scroll_down":
                mouse.scroll(0, -1)
            elif command == "left":
                mouse.click(button=MouseButton.left, count=1)
            elif command == "right":
                mouse.press(MouseButton.right)

        # Procesar teclas que se mantienen presionadas
        elif command in commands.HOLD_COMMANDS.values():
            if keyboard.is_pressed(command):
                keyboard.release(command)
                print(f"⌨️ Tecla {command} mantenida presionada.")
            else:
                keyboard.send(command, do_press=True, do_release=False)
                print(f"⌨️ Tecla {command} presionada.")

        # Procesar teclas normales
        else:
            keyboard.send(command, do_press=True, do_release=False)
            wait(1)
            keyboard.release(command)
            print(f"⌨️ Tecla {command} presionada y soltada.")
        print(f"✅ Comando ejecutado: {command}")

        # Obtener el comando original a partir del valor ejecutado
        original_command = next((k for k, v in commands.KEY_MAP.items() if v == command), None)
        if original_command:
            print(f"🔄 Comando original: {original_command}")

        # Guardar el último comando ejecutado
        save_last_executed_command(original_command)
        wait(1)


def save_last_executed_command(command):
    """
    Guarda el último comando ejecutado en un archivo

    Args:
        command: Comando a guardar como último ejecutado
    """
    # Obtener ruta de AppData
    appdata = os.getenv('APPDATA')
    game_dir = os.path.join(appdata, 'chat-game')
    history_file = os.path.join(game_dir, 'last_executed_command.txt')

    # Crear directorio si no existe
    if not os.path.exists(game_dir):
        os.makedirs(game_dir)

    # Cargar historial existente o crear nuevo
    try:
        with open(history_file, 'r') as f:
            history = f.readlines()
    except (FileNotFoundError):
        history = []

    # Añadir nuevo comando
    history.clear()
    history.append(
        f"{command}\n"
    )

    # Guardar historial actualizado
    with open(history_file, 'w') as f:
        f.writelines(history)
