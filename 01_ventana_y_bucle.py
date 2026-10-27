"""
=============================================================================
EJEMPLO 01: Creación de Ventana, Bucle Principal y Manejo de FPS
=============================================================================
Este script muestra la estructura fundamental de cualquier videojuego con Pygame:
1. Inicialización de los módulos de Pygame.
2. Creación y configuración de la ventana (resolución y título).
3. El bucle principal (Game Loop) que procesa:
   - Eventos (cerrar ventana, teclado).
   - Lógica y actualización.
   - Renderizado en pantalla.
4. Control de fotogramas por segundo (FPS) con pygame.time.Clock.
"""

import sys
import pygame

def main():
    # 1. Inicializar todos los módulos importados de Pygame
    pygame.init()

    # 2. Configuración de dimensiones y creación de la ventana principal
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("01 - Estructura Básica y Bucle de Juego")

    # 3. Reloj para controlar los fotogramas por segundo (FPS)
    reloj = pygame.time.Clock()
    FPS = 60

    # Colores en formato RGB (Rojo, Verde, Azul)
    COLOR_FONDO = (26, 32, 44)       # Azul oscuro / pizarra
    COLOR_TEXTO = (237, 242, 247)     # Blanco brillante
    COLOR_ACENTO = (56, 178, 172)     # Turquesa neón

    # Fuente para mostrar información en pantalla
    fuente_titulo = pygame.font.SysFont("Arial", 28, bold=True)
    fuente_info = pygame.font.SysFont("Arial", 18)

    contador_frames = 0
    en_ejecucion = True

    # 4. Bucle principal del juego (Game Loop)
    while en_ejecucion:
        # --- A) GESTIÓN DE EVENTOS ---
        for evento in pygame.event.get():
            # Si el usuario hace clic en el botón de cerrar (X)
            if evento.type == pygame.QUIT:
                en_ejecucion = False
            
            # Si se presiona una tecla
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    en_ejecucion = False

        # --- B) LÓGICA Y ACTUALIZACIÓN ---
        contador_frames += 1
        fps_actuales = reloj.get_fps()

        # --- C) RENDERIZADO / DIBUJO ---
        # Limpiar la pantalla con un color de fondo
        pantalla.fill(COLOR_FONDO)

        # Renderizar textos informativos
        surf_titulo = fuente_titulo.render("¡Bienvenido a Pygame!", True, COLOR_ACENTO)
        pantalla.blit(surf_titulo, (ANCHO // 2 - surf_titulo.get_width() // 2, 180))

        lineas_info = [
            "Este es el bucle principal (Game Loop) ejecutándose de manera continua.",
            f"Fotogramas renderizados: {contador_frames}",
            f"FPS objetivo: {FPS} | FPS actuales: {fps_actuales:.1f}",
            "Presiona [ESC] o cierra la ventana para salir."
        ]

        for i, linea in enumerate(lineas_info):
            surf_linea = fuente_info.render(linea, True, COLOR_TEXTO)
            pantalla.blit(surf_linea, (ANCHO // 2 - surf_linea.get_width() // 2, 260 + i * 36))

        # Actualizar la pantalla completa (doble búfer)
        pygame.display.flip()

        # Limitar la tasa de refresco a 60 FPS
        reloj.tick(FPS)

    # 5. Salir limpiamente de Pygame y del programa
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
