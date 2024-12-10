# 🎮 Chat Game Controller

Este proyecto permite controlar juegos a través de comandos de chat en Kick.com, creando una experiencia interactiva entre streamers y espectadores.

## ✨ Características

- Control de juegos mediante comandos de chat
- Soporte para múltiples tipos de comandos:
  - Movimiento básico
  - Acciones
  - Control de cámara
  - Interacción con vehículos
  - Manejo de armas
- Sistema de timeouts para prevenir spam
- Historial de comandos
- Interfaz de control simple

## 🛠️ Requisitos

- Python 3.8+
- Chrome/Chromium
- Dependencias (se instalan automáticamente):
  - undetected_chromedriver
  - selenium
  - selenium-stealth
  - keyboard
  - prompt_toolkit
  - halo

## 📦 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/chat-game-controller.git
cd chat-game-controller
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## 🚀 Uso

1. Ejecuta el programa:

```bash
python src/main.py
```

2. Ingresa el nombre del canal de Kick.com que deseas monitorear
3. El programa comenzará a escuchar los comandos del chat

### Controles del programa:

- `q`: Cerrar el programa
- `r`: Resetear comandos
- `c`: Limpiar pantalla

## 🕛 Build

Hacer build del proyecto

### Unix

```bash
scripts/build.sh
```

### Windows

```bash
scripts/build.bat
```

## 🎮 Comandos disponibles

### Movimiento básico

- `!adelante`: W
- `!atras`: S
- `!izquierda`: A
- `!derecha`: D
- `!salta`: Espacio
- `!agacharse`: Ctrl

### Acciones

- `!corre`: Shift
- `!entrar`: F
- `!interactuar`: E
- `!recargar`: R

### Cámara

- `!cam_arriba`: Mover cámara arriba
- `!cam_abajo`: Mover cámara abajo
- `!cam_izq`: Mover cámara izquierda
- `!cam_der`: Mover cámara derecha
- `!cam_reset`: Resetear cámara

## 🔧 Configuración

Los comandos se pueden personalizar modificando el archivo:

```1:52:src/engine/commands.py
# Comandos que se mantienen presionados
HOLD_COMMANDS = {
    "!corre": "shift",
    "!apuntar": "right"
}

# Comandos de movimiento de cámara
CAMERA_COMMANDS = {
    "!cam_arriba": "mouse_up",
    "!cam_abajo": "mouse_down",
    "!cam_izq": "mouse_left",
    "!cam_der": "mouse_right",
    "!cam_reset": "numpad5"
}

# Comandos de mouse
MOUSE_COMMANDS = {
    "!dispara": "left",
    "!disparo": "left",
    "!apuntar": "right"
}

# Mapeo completo de comandos a teclas
KEY_MAP = {
    # Movimiento básico
    "!adelante": "w",
    "!atras": "s",
    "!izquierda": "a",
    "!derecha": "d",
    "!salta": "space",
    "!agacharse": "ctrl",

    # Acciones
    "!corre": "shift",
    "!entrar": "f",
    "!interactuar": "e",
    "!recargar": "r",

    # Vehículos
    "!acelerar": "w",
    "!frenar": "space",
    "!bocina": "h",

    # Armas
    "!arma1": "1",
    "!arma2": "2",

    # Cámara
    "!camara": "v",
    "!cam_arriba": "mouse_up",
    "!cam_abajo": "mouse_down",

```

## 📝 Notas

- Los usuarios tienen un timeout de 200 segundos entre comandos para evitar spam
- El historial guarda los últimos 10 comandos ejecutados
- El programa utiliza técnicas anti-detección para funcionar con Kick.com

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría realizar.
