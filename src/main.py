import msvcrt
import asyncio
from external.kick import monitor_chatroom
import engine.commands as commands
from engine.game_controller import add_command, execute_command, clear_histories, clear_commands
from prompt_toolkit import PromptSession
from halo import Halo
import sys
from os import system as bash
from concurrent.futures import ThreadPoolExecutor as tpe
import signal
import time
# Variables globales
canal = ""
spinner = Halo(text='Cargando navegador...', spinner='dots')

# Creación del pool de hilos para manejar operaciones asíncronas
loop = asyncio.new_event_loop()
thread_pool = tpe(max_workers=100)
should_exit = False

def get_key_nonblocking():
    """
    Lee una tecla de manera no bloqueante para Windows
    Retorna None si no hay tecla presionada
    """
    if msvcrt.kbhit():
        return msvcrt.getch().decode('utf-8', errors='ignore')
    return None

async def handle_control_keys(channel: str, link: str, control_key: str):
    """
    Maneja las teclas de control de manera asíncrona
    """
    global should_exit
    match control_key:
        case 'q':
            print("⭕ Tecla 'q' presionada. Cerrando el programa...")
            should_exit = True
            return
        case 'c':
            bash("cls")
            print("🚀 Escuchando a " + channel + " en " + link)
            print("Presiona 'q' para cerrar el programa.")
            print("Presiona 'r' para resetear los comandos.")
            print("Presiona 'c' para limpiar la pantalla.")
            return
        case 'r':
            await clear_commands()
            await clear_histories()
            return

def ready_event(channel: str, link: str):
    """
    Evento que se dispara cuando el monitor de chat está listo
    """
    global should_exit

    spinner.stop()
    print("🚀 Escuchando a " + channel + " en " + link)
    print("Presiona 'q' para cerrar el programa.")
    print("Presiona 'r' para resetear los comandos.")
    print("Presiona 'c' para limpiar la pantalla.")

    def check_keys():
        while not should_exit:
            key = get_key_nonblocking()
            if key:
                asyncio.run_coroutine_threadsafe(
                    handle_control_keys(channel, link, key),
                    loop
                )
            time.sleep(0.1)

    # Ejecutamos el checker de teclas en un thread separado
    thread_pool.submit(check_keys)

async def process_message(author: str, command: str):
    """
    Procesa los mensajes de manera asíncrona
    """
    if command in commands.KEY_MAP:
        await add_command(author, command, commands.KEY_MAP[command])

def message_event(msg: list[str]):
    """
    Procesa los mensajes nuevos del chat
    """
    author = msg[0]
    content = msg[1].lower().strip()
    print(f"{author} executed: {content}")

    # Ejecutar el procesamiento de mensaje en el loop de eventos
    asyncio.run_coroutine_threadsafe(process_message(author, content), loop)

async def tick_async():
    """
    Versión asíncrona del tick
    """
    if(should_exit):
        await on_exit();
    await execute_command()

def tick():
    """
    Se ejecuta en cada ciclo del monitor
    """
    asyncio.run_coroutine_threadsafe(tick_async(), loop)

def signal_handler(signum, frame):
    """
    Manejador de señales para cierre graceful
    """
    global should_exit
    should_exit = True
    print("\n⭕ Programa interrumpido")
    sys.exit(0)

async def async_main():
    """
    Función principal asíncrona
    """
    try:
        global canal
        session = PromptSession()
        canal = await session.prompt_async("🟩 Ingresá el nombre del canal de Kick: ")
        spinner.start()
        await clear_histories()

        # Configurar el manejador de señales
        signal.signal(signal.SIGINT, signal_handler)

        # Iniciar el monitor en un thread separado
        await loop.run_in_executor(
            thread_pool,
            monitor_chatroom,
            thread_pool,
            canal,
            ready_event,
            message_event,
            tick,
            0.5
        )
    except Exception as e:
        print(f"⭕ Error: {e}")
        # Asegúrate de manejar las excepciones
        sys.exit(1)
    finally:
        await on_exit()

async def on_exit():
    """
    Limpieza asíncrona al salir
    """
    print("\nCerrando el programa...")
    print("La despedida del papu :v")

    try:
        # Cancelar tareas activas sin recursión infinita
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()

        # Esperar que todas las tareas se cancelen
        await asyncio.gather(*tasks, return_exceptions=True)
    finally:
        # Cerrar el pool de hilos
        thread_pool.shutdown(wait=True)

        # Detener el loop si está corriendo
        if not loop.is_closed():
            loop.stop()

        print("Programa cerrado correctamente.")


def main():
    """
    Punto de entrada principal
    """
    global loop
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(async_main())
    except KeyboardInterrupt:
        pass
    finally:
        if not loop.is_closed():
            loop.stop()
            loop.close()

# Punto de entrada del programa
if __name__ == "__main__":
    main()