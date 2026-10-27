"""
=============================================================================
CONFIGURACIÓN Y CONSTANTES: GEOMETRY DASH PYGAME
=============================================================================
Este módulo define todas las constantes del juego:
- Dimensiones de la pantalla y tasa de refresco (FPS).
- Parámetros de física (gravedad, salto, velocidad horizontal).
- Paletas de colores neón temáticas.
"""

# Configuración de Ventana
ANCHO_PANTALLA = 960
ALTO_PANTALLA = 540
FPS = 60
TITULO = "Geometry Dash - Pygame Edition"

# Física del Jugador (Cubo)
TAMANO_CUBO = 42
VELOCIDAD_SCROLL = 380.0       # Píxeles por segundo de avance continuo
GRAVEDAD = 1900.0             # Aceleración hacia abajo
FUERZA_SALTO = -680.0         # Impulso de salto normal
FUERZA_JUMP_PAD = -880.0      # Impulso al tocar un Pad amarillo
FUERZA_ORB = -690.0           # Impulso al activar un Orbe en el aire
VELOCIDAD_ROTACION = 420.0    # Grados por segundo al estar en el aire

# Nivel y Suelo
ALTURA_SUELO = 110            # Distancia desde el fondo de la pantalla
Y_SUELO = ALTO_PANTALLA - ALTURA_SUELO

# Paleta de Colores Neón / Cyberpunk
COLOR_FONDO_1 = (13, 17, 34)       # Azul noche profundo
COLOR_FONDO_2 = (22, 27, 46)
COLOR_SUELO = (10, 12, 24)
COLOR_LINEA_SUELO = (0, 245, 255)  # Cyan neón
COLOR_CUBO = (57, 255, 20)         # Verde lima neón
COLOR_CUBO_BORDE = (255, 255, 255)
COLOR_CUBO_OJOS = (10, 15, 30)
COLOR_PINCHO = (255, 49, 49)       # Rojo brillante
COLOR_PINCHO_BORDE = (255, 255, 255)
COLOR_BLOQUE = (28, 35, 60)
COLOR_BLOQUE_BORDE = (0, 245, 255)
COLOR_ORB_AMARILLO = (255, 230, 0)
COLOR_PAD_AMARILLO = (255, 215, 0)
COLOR_PORTAL = (180, 50, 255)      # Violeta brillante
COLOR_TEXTO = (255, 255, 255)
COLOR_TEXTO_MUTED = (150, 165, 190)
COLOR_BARRA_PROGRESO = (57, 255, 20)
