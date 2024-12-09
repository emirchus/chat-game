import asyncio

from external.kick import monitor_chatroom
import engine.commands as commands
from engine.game_controller import add_command, execute_command
from prompt_toolkit import prompt
from halo import Halo
from keyboard import is_pressed
from time import sleep as wait
import sys
from os import system as bash
from concurrent.futures import ThreadPoolExecutor as tpe

canal = ""
spinner = Halo(text='Cargando navegador...', spinner='dots')


thread = tpe(max_workers=100)

def ready_event(channel, link):
    spinner.stop()
    print("🚀 Escuchando a " + channel + " en " + link)
    print("Presiona 'q' para cerrar el programa.")
    print("Presiona 'r' para resetear los comandos.")
    print("Presiona 'c' para limpiar la pantalla.")

    while True:
        wait(0.1)
        if is_pressed('q'):
            print("⭕ Tecla 'q' presionada. Cerrando el programa...")
            thread.shutdown()
            sys.exit()
            break;
        if is_pressed('c'):
            bash("cls")
            print("🚀 Escuchando a " + channel + " en " + link)
            print("Presiona 'q' para cerrar el programa.")
            print("Presiona 'r' para resetear los comandos.")
            print("Presiona 'c' para limpiar la pantalla.")


def message_event(msg):
    author = msg[0]
    content = msg[1]

    command = content.lower().strip()
    print(f"{author} executed: {command}")

    if command in commands.KEY_MAP:
        asyncio.run(add_command(author, command, commands.KEY_MAP[command]))

def tick():
    run_command_game()

    pass


def run_command_game():
    asyncio.run(execute_command())

def main():
    try:
        canal = prompt("🟩 Ingresá el nombre del canal de Kick: ")
        spinner.start()
        monitor_chatroom(thread, canal, ready_event, message_event, tick, .5)
    except KeyboardInterrupt:
        print("\n⭕Programa interrumpido por el usuario")
    except Exception as e:
        print(f"⭕ Error: {e}")
    finally:
        on_exit()


def on_exit():
    print("\nCerrando el programa...")
    print("La despedida del papu :v")

if __name__ == "__main__":
    main()