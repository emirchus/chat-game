import asyncio
from external.kick import monitor_chatroom
import engine.commands as commands
from engine.game_controller import add_command, execute_command, clear_histories, clear_commands
from prompt_toolkit import prompt
from halo import Halo
from keyboard import is_pressed
from time import sleep as wait
import sys
from os import system as bash
from concurrent.futures import ThreadPoolExecutor as tpe 
import signal

# Variables globales
canal = ""
spinner = Halo(text='Cargando navegador...', spinner='dots')
loop = asyncio.new_event_loop()
thread_pool = tpe(max_workers=100)
should_exit = False

async def handle_control_keys(channel: str, link: str):
    """
    Maneja las teclas de control de manera asíncrona
    """
    global should_exit
    while not should_exit:
        await asyncio.sleep(0.1)
        if is_pressed('q'):
            print("⭕ Tecla 'q' presionada. Cerrando el programa...")
            should_exit = True
            break
        elif is_pressed('c'):
            bash("cls")
            print("🚀 Escuchando a " + channel + " en " + link)
            print("Presiona 'q' para cerrar el programa.")
            print("Presiona 'r' para resetear los comandos.")
            print("Presiona 'c' para limpiar la pantalla.")
        elif is_pressed('r'):
            await clear_commands()
            await clear_histories()

def ready_event(channel: str, link: str):
    """
    Evento que se dispara cuando el monitor de chat está listo
    """
    spinner.stop()
    print("🚀 Escuchando a " + channel + " en " + link)
    print("Presiona 'q' para cerrar el programa.")
    print("Presiona 'r' para resetear los comandos.")
    print("Presiona 'c' para limpiar la pantalla.")
    
    # Iniciar el manejador de teclas de control en el loop de eventos
    asyncio.run_coroutine_threadsafe(handle_control_keys(channel, link), loop)

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
        canal = prompt("🟩 Ingresá el nombre del canal de Kick: ")
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
    finally:
        await on_exit()

async def on_exit():
    """
    Limpieza asíncrona al salir
    """
    print("\nCerrando el programa...")
    print("La despedida del papu :v")
    
    # Limpieza de recursos
    thread_pool.shutdown(wait=True)
    tasks = [t for t in asyncio.all_tasks(loop) if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
    loop.close()

def main():
    """
    Punto de entrada principal
    """
    try:
        asyncio.set_event_loop(loop)
        loop.run_until_complete(async_main())
    except KeyboardInterrupt:
        pass
    finally:
        if not loop.is_closed():
            loop.close()

if __name__ == "__main__":
    main()