import asyncio

from external.kick import monitor_chatroom
import engine.commands as commands
from engine.game_controller import add_command, execute_command

from prompt_toolkit import prompt

def ready_event(channel, link):
    print("🚀 Escuchando a " + channel + " en " + link)

def message_event(msg):
    author = msg[0]
    content = msg[1]

    command = content.lower().strip()
    print(f"{author} executed: {command}")
    if command in commands.KEY_MAP:
        asyncio.run(add_command(commands.KEY_MAP[command]))

def tick():
    run_command_game()
    pass


def run_command_game():
    asyncio.run(execute_command())

def main():
    try:
        canal = prompt("🟩 Ingresá el nombre del canal de Kick: ")
        monitor_chatroom(canal, ready_event, message_event, tick, .5)
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