"""
=============================================================================
EJEMPLO 03: Control de Teclado, Movimiento y Delta Time
=============================================================================
Este script explica las dos formas esenciales de capturar teclado en Pygame:
1. `pygame.key.get_pressed()`: Consulta en tiempo real de qué teclas están
   pulsadas (ideal para movimiento suave continuo como flechas o WASD).
2. Eventos `pygame.KEYDOWN`: Se dispara exactamente una vez por pulsación
   (ideal para acciones discretas como saltar, pausar o disparar).
3. Uso de Delta Time (`dt`): Asegura que la velocidad del personaje sea
   independiente de la tasa de cuadros (evita que corra más rápido en 144Hz que en 60Hz).
4. Restricción de movimiento dentro de los límites de la ventana.
"""

import sys
import pygame

def main():
    pygame.init()
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("03 - Teclado, Movimiento Suave y Delta Time")

    reloj = pygame.time.Clock()
    FPS = 60

    # Colores
    FONDO = (17, 24, 39)
    BLANCO = (255, 255, 255)
    COLOR_JUGADOR = (59, 130, 246)
    COLOR_BORDE_JUGADOR = (147, 197, 253)
    COLOR_PULSO = (244, 63, 94)
    COLOR_PANEL = (31, 41, 55)

    fuente = pygame.font.SysFont("Arial", 16)
    fuente_titulo = pygame.font.SysFont("Arial", 20, bold=True)

    # Variables del jugador
    tamano = 48
    pos_x = ANCHO // 2 - tamano // 2
    pos_y = ALTO // 2 - tamano // 2
    velocidad = 350.0  # Pixeles por segundo

    # Variables para evento KEYDOWN discreto
    contador_saltos = 0
    radio_onda_salto = 0

    while True:
        # Calcular delta time en segundos (ej. a 60 FPS, dt ≈ 0.0166s)
        dt = reloj.tick(FPS) / 1000.0

        # -------------------------------------------------------------
        # 1. EVENTOS DISCRETOS (pygame.KEYDOWN)
        # -------------------------------------------------------------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                # Barra espaciadora: Acción discreta
                if evento.key == pygame.K_SPACE:
                    contador_saltos += 1
                    radio_onda_salto = 10  # Inicia efecto visual

        # -------------------------------------------------------------
        # 2. TECLADO CONTINUO (pygame.key.get_pressed())
        # -------------------------------------------------------------
        teclas = pygame.key.get_pressed()
        dir_x, dir_y = 0, 0

        # Soporte para flechas y teclas WASD
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dir_x -= 1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dir_x += 1
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dir_y -= 1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dir_y += 1

        # Normalizar vector de movimiento diagonal para evitar exceso de velocidad
        if dir_x != 0 and dir_y != 0:
            dir_x *= 0.7071
            dir_y *= 0.7071

        # Aplicar movimiento usando Delta Time (dx = velocidad * dt)
        pos_x += dir_x * velocidad * dt
        pos_y += dir_y * velocidad * dt

        # Mantener al jugador dentro de los límites de la pantalla
        pos_x = max(0, min(ANCHO - tamano, pos_x))
        pos_y = max(0, min(ALTO - tamano, pos_y))

        # -------------------------------------------------------------
        # RENDERIZADO
        # -------------------------------------------------------------
        pantalla.fill(FONDO)

        # Efecto visual de onda al presionar Espacio
        if radio_onda_salto > 0 and radio_onda_salto < 70:
            centro_jugador = (int(pos_x + tamano // 2), int(pos_y + tamano // 2))
            pygame.draw.circle(pantalla, COLOR_PULSO, centro_jugador, int(radio_onda_salto), 3)
            radio_onda_salto += 120 * dt

        # Dibujar al jugador (cuadrado estilizado)
        rect_jugador = pygame.Rect(int(pos_x), int(pos_y), tamano, tamano)
        pygame.draw.rect(pantalla, COLOR_JUGADOR, rect_jugador, border_radius=8)
        pygame.draw.rect(pantalla, COLOR_BORDE_JUGADOR, rect_jugador, width=3, border_radius=8)

        # Panel de información inferior
        pygame.draw.rect(pantalla, COLOR_PANEL, (0, ALTO - 100, ANCHO, 100))
        pygame.draw.line(pantalla, (75, 85, 99), (0, ALTO - 100), (ANCHO, ALTO - 100), 1)

        txt_controles = fuente_titulo.render("Controles: [W, A, S, D] o [Flechas] para mover | [Espacio] para acción", True, BLANCO)
        txt_pos = fuente.render(f"Posición Jugador: ({pos_x:.1f}, {pos_y:.1f}) | Delta Time: {dt:.4f}s", True, (209, 213, 219))
        txt_evento = fuente.render(f"Acciones discretas registradas con [Espacio]: {contador_saltos}", True, COLOR_PULSO)

        pantalla.blit(txt_controles, (20, ALTO - 90))
        pantalla.blit(txt_pos, (20, ALTO - 60))
        pantalla.blit(txt_evento, (20, ALTO - 35))

        pygame.display.flip()

if __name__ == "__main__":
    main()
