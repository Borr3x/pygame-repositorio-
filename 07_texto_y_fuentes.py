"""
=============================================================================
EJEMPLO 07: Renderizado de Texto, Fuentes y Creación de un HUD
=============================================================================
Este script muestra cómo manejar tipografía y crear una interfaz HUD para juegos:
1. Uso de `pygame.font.SysFont` para cargar fuentes instaladas en el sistema.
2. Renderizado con Antialiasing (suavizado de bordes) vs texto pixelado.
3. Posicionamiento dinámico de texto utilizando rectángulos (`center`, `topright`).
4. Construcción de un HUD interactivo completo:
   - Puntuación con animación de incremento.
   - Cronómetro de juego formateado en MM:SS.
   - Barra de salud dinámica (HP) con degradado según el daño.
"""

import sys
import pygame

def main():
    pygame.init()
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("07 - Fuentes, Renderizado de Texto y HUD")

    reloj = pygame.time.Clock()

    # Carga de diferentes fuentes y estilos
    fuente_hud_num = pygame.font.SysFont("Consolas", 26, bold=True)
    fuente_etiquetas = pygame.font.SysFont("Arial", 16, bold=True)
    fuente_retro = pygame.font.SysFont("Courier New", 20, bold=True)
    fuente_grande = pygame.font.SysFont("Arial", 36, bold=True)

    # Variables dinámicas del juego simulado
    puntuacion = 1450
    salud_max = 100
    salud_actual = 85
    tiempo_ms = 0

    while True:
        dt = reloj.tick(60)
        tiempo_ms += dt

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Teclas para interactuar con el HUD
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    puntuacion += 100
                elif evento.key == pygame.K_DOWN:
                    puntuacion = max(0, puntuacion - 100)
                elif evento.key == pygame.K_RIGHT:
                    salud_actual = min(salud_max, salud_actual + 10)
                elif evento.key == pygame.K_LEFT:
                    salud_actual = max(0, salud_actual - 10)

        pantalla.fill((18, 20, 29))

        # -------------------------------------------------------------
        # 1. COMPARATIVA DE ANTIALIASING
        # -------------------------------------------------------------
        # Suavizado activo (Recomendado para fuentes normales)
        surf_aa_on = fuente_grande.render("Texto con Antialiasing (antialias=True)", True, (255, 255, 255))
        pantalla.blit(surf_aa_on, (50, 40))

        # Sin suavizado (aspecto pixel / retro)
        surf_aa_off = fuente_grande.render("Texto sin Antialiasing (antialias=False)", False, (148, 163, 184))
        pantalla.blit(surf_aa_off, (50, 90))

        # -------------------------------------------------------------
        # 2. PANEL HUD (Head-Up Display)
        # -------------------------------------------------------------
        hud_rect = pygame.Rect(40, 180, ANCHO - 80, 200)
        pygame.draw.rect(pantalla, (30, 41, 59), hud_rect, border_radius=12)
        pygame.draw.rect(pantalla, (71, 85, 105), hud_rect, width=2, border_radius=12)

        # A) PUNTUACIÓN
        lbl_score_txt = fuente_etiquetas.render("SCORE", True, (148, 163, 184))
        pantalla.blit(lbl_score_txt, (70, 210))
        val_score = fuente_hud_num.render(f"{puntuacion:06d}", True, (250, 204, 21))
        pantalla.blit(val_score, (70, 240))

        # B) CRONÓMETRO FORMATEADO (MM:SS:CS)
        total_segundos = tiempo_ms // 1000
        minutos = total_segundos // 60
        segundos = total_segundos % 60
        centisegundos = (tiempo_ms % 1000) // 10
        txt_cronometro = f"{minutos:02d}:{segundos:02d}.{centisegundos:02d}"

        lbl_tiempo = fuente_etiquetas.render("TIEMPO", True, (148, 163, 184))
        pantalla.blit(lbl_tiempo, (290, 210))
        val_tiempo = fuente_retro.render(txt_cronometro, True, (56, 189, 248))
        pantalla.blit(val_tiempo, (290, 243))

        # C) BARRA DE SALUD (HP)
        lbl_salud = fuente_etiquetas.render("VIDA (HP)", True, (148, 163, 184))
        pantalla.blit(lbl_salud, (500, 210))

        # Fondo barra
        ancho_barra_total = 220
        alto_barra = 26
        x_barra, y_barra = 500, 245
        pygame.draw.rect(pantalla, (15, 23, 42), (x_barra, y_barra, ancho_barra_total, alto_barra), border_radius=6)

        # Relleno proporcional
        pct_salud = salud_actual / salud_max
        ancho_relleno = int(ancho_barra_total * pct_salud)

        # Color según vida: Verde (>50%), Amarillo (20%-50%), Rojo (<20%)
        if pct_salud > 0.5:
            color_hp = (34, 197, 94)
        elif pct_salud > 0.2:
            color_hp = (234, 179, 8)
        else:
            color_hp = (239, 68, 68)

        if ancho_relleno > 0:
            pygame.draw.rect(pantalla, color_hp, (x_barra, y_barra, ancho_relleno, alto_barra), border_radius=6)
        pygame.draw.rect(pantalla, (255, 255, 255), (x_barra, y_barra, ancho_barra_total, alto_barra), width=2, border_radius=6)

        # Texto numérico de salud dentro de la barra
        txt_hp_num = fuente_etiquetas.render(f"{salud_actual} / {salud_max}", True, (255, 255, 255))
        rect_hp_txt = txt_hp_num.get_rect(center=(x_barra + ancho_barra_total // 2, y_barra + alto_barra // 2))
        pantalla.blit(txt_hp_num, rect_hp_txt)

        # -------------------------------------------------------------
        # INSTRUCCIONES DE CONTROL
        # -------------------------------------------------------------
        panel_instrucciones = pygame.Rect(40, 420, ANCHO - 80, 130)
        pygame.draw.rect(pantalla, (24, 30, 43), panel_instrucciones, border_radius=10)

        instrucciones = [
            "Controles interactivos para probar el renderizado dinámico:",
            "  [Flecha Arriba / Abajo]: Subir / Bajar Puntuación",
            "  [Flecha Izquierda / Derecha]: Reducir / Aumentar Salud",
            "  [ESC]: Salir"
        ]
        for i, inst in enumerate(instrucciones):
            lbl_inst = fuente_etiquetas.render(inst, True, (226, 232, 240) if i == 0 else (148, 163, 184))
            pantalla.blit(lbl_inst, (60, 435 + i * 26))

        pygame.display.flip()

if __name__ == "__main__":
    main()
