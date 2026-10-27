# 🎮 Pygame Mastery & Geometry Dash Clone

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#licencia)

Repositorio completo y didáctico para dominar el desarrollo de videojuegos 2D en Python utilizando la librería **Pygame**. Incluye **8 guías prácticas modulares** que exploran desde los fundamentos hasta técnicas avanzadas, junto con un **videojuego completo al estilo *Geometry Dash*** con físicas, partículas, música rítmica y diseño de niveles.

---

## 📁 Estructura del Repositorio

```text
├── 01_conceptos_basicos/           # Colección didáctica de fundamentos de Pygame
│   ├── 01_ventana_y_bucle.py       # Estructura del Game Loop, reloj y control de FPS
│   ├── 02_dibujo_y_formas.py       # Primitivas gráficas (rect, circle, polygon) y canal Alfa
│   ├── 03_movimiento_y_teclado.py  # Teclado continuo vs discreto, Delta Time (dt)
│   ├── 04_mouse_y_botones.py       # Botones UI interactivos, hover, clics y Drag & Drop
│   ├── 05_sprites_y_grupos.py      # POO en Pygame: pygame.sprite.Sprite y Group
│   ├── 06_colisiones_y_mascaras.py # Comparativa AABB vs Máscara de píxeles (Pixel-Perfect)
│   ├── 07_texto_y_fuentes.py       # Tipografías SysFont, antialiasing y diseño de HUD
│   └── 08_audio_y_musica.py        # Síntesis procedural de SFX con pygame.mixer
│
├── 02_juego_geometry_dash/         # Videojuego completo Geometry Dash
│   ├── settings.py                 # Constantes globales, física, dimensiones y paletas
│   ├── audio_manager.py            # Generador procedural de música techno y SFX
│   ├── particles.py                # Sistema de partículas (estela, polvo, explosión)
│   ├── player.py                   # Cubo jugador, física de gravedad y rotación en salto
│   ├── obstacles.py                # Pinchos, bloques, pads de impulso, orbes y portal
│   ├── level.py                    # Diseño del nivel rítmico, fondo parallax y progreso
│   └── main.py                     # Bucle principal, estados (Menú, Juego, Over, Victoria)
│
├── requirements.txt                # Dependencias del proyecto
├── .gitignore                      # Exclusiones estándar para proyectos Python
└── README.md                       # Documentación y guía de uso
```

---

## 🚀 Instalación y Puesta en Marcha

### 1. Clonar el repositorio o abrir la carpeta
Si descargaste o clonaste este repositorio:
```bash
git clone <URL_DE_TU_REPOSITORIO>
cd "pygame tarea"
```

### 2. Crear y activar un entorno virtual
*En Windows (PowerShell):*
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

*En macOS / Linux:*
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

---

## 📚 Módulos Didácticos de Pygame (`01_conceptos_basicos/`)

Cada archivo en esta carpeta es completamente autónomo y ejecutable:

| Script | Tema Principal | Conceptos Clave Demostrados |
|---|---|---|
| `01_ventana_y_bucle.py` | **Ventana y Bucle** | `pygame.init()`, `display.set_mode()`, `time.Clock()`, bucle de eventos, control de FPS y salida limpia. |
| `02_dibujo_y_formas.py` | **Primitivas y Alfa** | Rectángulos con bordes redondeados, círculos, elipses, polígonos, estrellas trigonométricas y superficies translúcidas `SRCALPHA`. |
| `03_movimiento_y_teclado.py` | **Teclado y Delta Time** | `pygame.key.get_pressed()` para movimiento fluido vs `KEYDOWN` para acciones discretas, normalización de diagonales y uso de `dt` para velocidad independiente de frames. |
| `04_mouse_y_botones.py` | **Ratón y UI** | Eventos del mouse, clase `Boton` con efectos *hover* y *clic*, cambio del cursor del sistema y mecánica *Drag & Drop* con `collidepoint`. |
| `05_sprites_y_grupos.py` | **Sprites y Grupos** | Programación Orientada a Objetos: herencia de `pygame.sprite.Sprite`, `image`, `rect`, grupos de actualización masiva y autodestrucción con `.kill()`. |
| `06_colisiones_y_mascaras.py` | **Colisiones Avanzadas** | Diferencias visuales e interactivas entre colisión por caja envolvente (`colliderect`) y colisión exacta por píxel (`pygame.mask.from_surface`). |
| `07_texto_y_fuentes.py` | **Texto y HUD** | `font.SysFont()`, antialiasing, posicionamiento de cajas de texto, formateo de cronómetro (MM:SS) y barra de salud dinámica. |
| `08_audio_y_musica.py` | **Audio Procedural** | Canales independientes (`pygame.mixer.Channel`), control de volumen y síntesis de ondas sinusoidales/ruido en memoria sin necesidad de archivos externos. |

**Para ejecutar cualquier ejemplo:**
```bash
python 01_conceptos_basicos/01_ventana_y_bucle.py
python 01_conceptos_basicos/06_colisiones_y_mascaras.py
```

---

## 🕹️ Videojuego: Geometry Dash (Pygame Edition)

El juego replica fielmente la jugabilidad adictiva y rítmica del clásico **Geometry Dash**.

![Geometry Dash Preview](https://img.shields.io/badge/Genre-Rhythm%20Platformer-ff007f?style=for-the-badge)

### 🌟 Características del Juego
- **Física del Cubo Fiel:**
  - Avance horizontal constante.
  - Gravedad y salto ajustados al milímetro.
  - **Rotación icónica de 90°:** mientras está en el aire, el cubo gira continuamente hacia adelante, y al aterrizar en el suelo o sobre una plataforma se alinea perfectamente a la superficie plana.
- **Obstáculos y Mecánicas Interactivas:**
  - 🔺 **Pinchos (Spikes):** Letales al contacto, evaluados con máscara de precisión.
  - ⬛ **Bloques (Blocks):** Plataformas sobre las que puedes aterrizar; chocar de frente o desde abajo provoca la destrucción inmediata del cubo.
  - 🟡 **Pads Amarillos (Jump Pads):** Plataformas de impulso en suelo que catapultan al cubo a gran altura automáticamente al pisarlas.
  - 🔘 **Orbes Amarillos (Jump Orbs):** Anillos flotantes en el aire; si pulsas salto mientras estás dentro de su radio, ejecutas un segundo salto en pleno vuelo.
  - 🌀 **Portal de Victoria (Finish Portal):** Vortex al final del circuito que activa la secuencia de nivel superado.
- **Efectos Visuales ("Juice"):**
  - **Partículas de Estela (Trail):** Siluetas translúcidas que el cubo proyecta a gran velocidad.
  - **Partículas de Polvo:** Se dispersan al saltar y al aterrizar.
  - **Explosión al Morir:** Decenas de fragmentos fluorescentes expulsados con físicas de gravedad.
  - **Sacudida de Pantalla (Screen Shake):** Impacto visual contundente cada vez que se produce un choque.
- **Audio Procedural Autónomo:**
  - Efectos de sonido sintetizados matemáticamente (salto, rebote de pad, orbe cristalino y explosión de derrota).
  - Música rítmica retro techno con bombo a tempo, platillo y línea de bajo que acompaña la partida sin requerir descargas pesadas de audio.

---

### 🎮 Controles

| Tecla / Acción | Función |
|---|---|
| <kbd>ESPACIO</kbd> / <kbd>FLECHA ARRIBA</kbd> / <kbd>W</kbd> | Saltar desde el suelo / Activar Orbe en el aire |
| <kbd>CLIC IZQUIERDO</kbd> | Saltar desde el suelo / Activar Orbe en el aire |
| <kbd>R</kbd> | Reinicio instantáneo del nivel |
| <kbd>P</kbd> | Pausar / Reanudar la música |
| <kbd>ESC</kbd> | Volver al Menú Principal / Salir |

### 🚀 Cómo Ejecutar el Juego:
```bash
python 02_juego_geometry_dash/main.py
```

---

## 📤 Cómo Subir este Proyecto a GitHub

Si deseas publicar este repositorio en tu cuenta de GitHub, sigue estos sencillos pasos:

1. Crea un nuevo repositorio vacío en [GitHub.com](https://github.com/new) (por ejemplo: `pygame-geometry-dash`).
2. En tu terminal o consola dentro de esta carpeta, vincula tu repositorio remoto y haz push:

```bash
# Agregar todos los archivos al control de versiones
git add .

# Crear el primer commit
git commit -m "feat: proyecto completo con ejemplos didácticos de pygame y clon de geometry dash"

# Conectar con tu repositorio remoto (reemplaza con tu usuario y repo)
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git

# Subir los cambios a la rama principal (main)
git push -u origin main
```

---

## 📜 Licencia

Este proyecto está bajo la Licencia **MIT**. Eres libre de usar, modificar, aprender y distribuir este código para fines educativos y personales.
