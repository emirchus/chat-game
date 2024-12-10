import asyncio
import keyboard
import time
import os
from time import sleep as wait
from pynput.mouse import Button as MouseButton, Controller as MouseController
from engine import commands
import threading

# Controlador del mouse
mouse = MouseController()

# Cola de comandos asíncrona
command_queue = asyncio.Queue()

# Diccionario para manejar timeouts de usuarios
users_timeouts = {}

# Locks para operaciones concurrentes
users_timeout_lock = threading.Lock()
file_operation_lock = threading.Lock()

async def add_command(username: str, raw_command: str, command: str):
    """
    Añade un comando a la cola si el usuario no está en timeout
    """
    print(f"✨ Añadiendo comando a la cola: {command}")
    current_time = time.time()

    with users_timeout_lock:
        # Verificar si el usuario tiene un timeout
        if username in users_timeouts:
            last_command_time = users_timeouts[username]
            if current_time - last_command_time < 200:  # 600 segundos = 10 minutos
                print(f"⏳ {username} debe esperar antes de enviar otro comando")
                return

        # Actualizar el tiempo del último comando del usuario
        users_timeouts[username] = current_time

    # Agregar el comando a la cola
    await command_queue.put(command)
    await save_command_history(raw_command)

async def save_command_history(command: str):
    """
    Guarda el historial de comandos en un archivo
    """
    with file_operation_lock:
        # Obtener ruta de AppData
        appdata = os.getenv('APPDATA')
        game_dir = os.path.join(appdata, 'chat-game')
        history_file = os.path.join(game_dir, 'command_history.txt')

        # Crear directorio si no existe
        os.makedirs(game_dir, exist_ok=True)

        # Cargar historial existente o crear nuevo
        try:
            with open(history_file, 'r') as f:
                history = f.readlines()
        except (FileNotFoundError):
            history = []

        # Añadir nuevo comando
        history.append(f"{command}\n")

        # Mantener solo los últimos 10 comandos
        if len(history) > 10:
            history = history[-10:]

        # Guardar historial actualizado
        with open(history_file, 'w') as f:
            f.writelines(history)

async def execute_command():
    """
    Ejecuta el siguiente comando en la cola
    """
    if not command_queue.empty():
        print("🕛 Esperando comando en la cola...")
        command = await command_queue.get()  # Espera el siguiente comando
        print(f"🕛 Procesando comando: {command}")

        try:
            # Procesar comandos de mouse
            if command in commands.MOUSE_COMMANDS.values():
                if command in commands.CAMERA_COMMANDS.values():
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
                else:
                    keyboard.send(command, do_press=True, do_release=False)

            # Procesar teclas normales
            else:
                keyboard.send(command, do_press=True, do_release=False)
                await asyncio.sleep(1)
                keyboard.release(command)

            # Obtener el comando original
            original_command = next((k for k, v in commands.KEY_MAP.items() if v == command), None)
            if original_command:
                await save_last_executed_command(original_command)

        finally:
            command_queue.task_done()
            await asyncio.sleep(1)

async def save_last_executed_command(command: str):
    """
    Guarda el último comando ejecutado en un archivo
    """
    with file_operation_lock:
        appdata = os.getenv('APPDATA')
        game_dir = os.path.join(appdata, 'chat-game')
        history_file = os.path.join(game_dir, 'last_executed_command.txt')

        os.makedirs(game_dir, exist_ok=True)

        with open(history_file, 'w') as f:
            f.write(f"{command}\n")

async def clear_histories():
    """
    Limpia los archivos de historial
    """
    with file_operation_lock:
        appdata = os.getenv('APPDATA')
        game_dir = os.path.join(appdata, 'chat-game')
        
        try:
            os.remove(os.path.join(game_dir, 'command_history.txt'))
            os.remove(os.path.join(game_dir, 'last_executed_command.txt'))
        except FileNotFoundError:
            pass

async def clear_commands():
    """
    Limpia la cola de comandos
    """
    while not command_queue.empty():
        try:
            command_queue.get_nowait()
            command_queue.task_done()
        except asyncio.QueueEmpty:
            break