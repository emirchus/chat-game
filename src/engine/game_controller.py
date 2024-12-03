import asyncio
import keyboard

from time import sleep as wait
from pynput.mouse import Button as MouseButton, Controller as MouseController

from engine import commands

mouse = MouseController()

command_queue = asyncio.Queue()


async def add_command(command):
    print(f"✨ Añadiendo comando a la cola: {command}")
    await command_queue.put(command)



def execute_command():
    if not command_queue.empty():
        print("🕛 Esperando comando en la cola...")
        command = command_queue.get_nowait()  # Espera el siguiente comando
        print(f"🕛 Procesando comando: {command}")
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
        elif command in commands.HOLD_COMMANDS.values():
            if keyboard.is_pressed(command):
                keyboard.release(command)
                print(f"⌨️ Tecla {command} mantenida presionada.")
            else:
                keyboard.send(command, do_press=True, do_release=False)
                print(f"⌨️ Tecla {command} presionada.")
        else:
            keyboard.send(command, do_press=True, do_release=False)
            wait(1)
            keyboard.release(command)
            print(f"⌨️ Tecla {command} presionada y soltada.")
        print(f"✅ Comando ejecutado: {command}")
        wait(1)
