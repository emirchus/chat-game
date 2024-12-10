# Importaciones necesarias
import asyncio
from external.kick import monitor_chatroom
import engine.commands as commands
from engine.game_controller import add_command, execute_command
from prompt_toolkit import prompt
from halo import Halo  # Para mostrar spinner de carga
from keyboard import is_pressed
from time import sleep as wait
import sys
from os import system as bash
from concurrent.futures import ThreadPoolExecutor as tpe

# Variables globales
canal = ""
spinner = Halo(text='Cargando navegador...', spinner='dots')

# Creación del pool de hilos para manejar operaciones asíncronas
thread = tpe(max_workers=100)

def ready_event(channel: str, link: str):
    """
    Evento que se dispara cuando el monitor de chat está listo
    Maneja los controles del programa y muestra información al usuario
    """
    spinner.stop()
    print("🚀 Escuchando a " + channel + " en " + link)
    print("Presiona 'q' para cerrar el programa.")
    print("Presiona 'r' para resetear los comandos.")
    print("Presiona 'c' para limpiar la pantalla.")

    # Loop principal para detectar teclas de control
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


def message_event(msg: list[str]):
    """
    Procesa los mensajes nuevos del chat

    Args:
        msg: Lista que contiene [autor, contenido, id, user_id]
    """
    author = msg[0]
    content = msg[1]

    command = content.lower().strip()
    print(f"{author} executed: {command}")

    # Si el mensaje es un comando válido, lo añade a la cola de ejecución
    if command in commands.KEY_MAP:
        asyncio.run(add_command(author, command, commands.KEY_MAP[command]))

def tick():
    """
    Se ejecuta en cada ciclo del monitor
    Procesa los comandos pendientes
    """
    run_command_game()
    pass


def run_command_game():
    """
    Ejecuta los comandos pendientes en la cola
    """
    asyncio.run(execute_command())

def main():
    """
    Función principal del programa
    Inicia el monitor de chat y maneja excepciones
    """
    try:
        # Solicita el nombre del canal al usuario
        canal = prompt("🟩 Ingresá el nombre del canal de Kick: ")
        spinner.start()
        # Inicia el monitor de chat con un intervalo de 0.5 segundos
        monitor_chatroom(thread, canal, ready_event, message_event, .5)
    except KeyboardInterrupt:
        print("\n⭕Programa interrumpido por el usuario")
    except Exception as e:
        print(f"⭕ Error: {e}")
    finally:
        on_exit()


def on_exit():
    """
    Función que se ejecuta al cerrar el programa
    Muestra mensajes de despedida
    """
    print("\nCerrando el programa...")
    print("La despedida del papu :v")

# Punto de entrada del programa
if __name__ == "__main__":
    main()