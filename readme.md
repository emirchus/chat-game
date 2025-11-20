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

### Configuración del Cooldown y Sistema

Ahora puedes configurar fácilmente el tiempo de cooldown entre comandos y otros parámetros editando el archivo `config.json`.

#### 📍 ¿Dónde encuentro el archivo de configuración?

**Para usuarios finales (.exe):**
El archivo se encuentra en: `%APPDATA%\chat-game\config.json`

Para acceder rápidamente:
1. Presiona `Win + R`
2. Escribe `%APPDATA%\chat-game`
3. Presiona Enter
4. Edita el archivo `config.json` con un editor de texto

**Para desarrolladores:**
El programa muestra la ubicación del archivo al iniciar. También puedes encontrarlo en la raíz del proyecto o en AppData.

#### ⚙️ Parámetros configurables:

```json
{
  "command_cooldown_seconds": 200,
  "command_history_limit": 10
}
```

**Parámetros disponibles:**
- `command_cooldown_seconds`: Tiempo en segundos que debe esperar un usuario entre comandos (por defecto: 200 segundos)
- `command_history_limit`: Número máximo de comandos a guardar en el historial (por defecto: 10)

> 💡 **Tip:** El programa muestra la ubicación exacta del archivo y el cooldown actual cada vez que se inicia.

### Personalización de Comandos

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

- Los usuarios tienen un timeout configurable entre comandos para evitar spam (por defecto: 200 segundos)
- El historial guarda los últimos comandos ejecutados (configurable en `config.json`)
- El programa utiliza técnicas anti-detección para funcionar con Kick.com
- Puedes modificar el archivo `config.json` en cualquier momento para ajustar los parámetros del sistema

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría realizar.
