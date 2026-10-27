"""
=============================================================================
EJEMPLO 06: Detección de Colisiones (Rectángulos vs Máscaras por Píxel)
=============================================================================
Este script compara las distintas formas de detectar colisiones en Pygame:
1. `colliderect`: Rápida y eficiente basada en cajas envolventes (AABB).
   Falla en formas no rectangulares (detecta falsos positivos en las esquinas vacías).
2. `pygame.mask.from_surface`: Genera una máscara de bits binaria de los píxeles
   opacos.
3. `mascara.overlap()`: Detección de colisión perfecta a nivel de píxel (Pixel-Perfect).
   Mueve el ratón para ver la diferencia visual entre colisión de caja vs colisión real.
"""

import sys
import pygame

def crear_superficie_estrella(tamano, color):
    """Crea una superficie con una estrella irregular."""
    surf = pygame.Surface((tamano, tamano), pygame.SRCALPHA)
    # Dibujar forma no rectangular con esquinas vacías
    puntos = [
        (tamano // 2, 0),
        (int(tamano * 0.65), int(tamano * 0.35)),
        (tamano, int(tamano * 0.40)),
        (int(tamano * 0.75), int(tamano * 0.65)),
        (int(tamano * 0.85), tamano),
        (tamano // 2, int(tamano * 0.80)),
        (int(tamano * 0.15), tamano),
        (int(tamano * 0.25), int(tamano * 0.65)),
        (0, int(tamano * 0.40)),
        (int(tamano * 0.35), int(tamano * 0.35)),
    ]
    pygame.draw.polygon(surf, color, puntos)
    return surf

def main():
    pygame.init()
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("06 - Colisiones: Bounding Box (AABB) vs Máscara Pixel-Perfect")

    reloj = pygame.time.Clock()
    fuente_titulo = pygame.font.SysFont("Arial", 18, bold=True)
    fuente_info = pygame.font.SysFont("Arial", 15)

    # Objeto estático en el centro: Una estrella grande
    tamano_fijo = 180
    surf_fija = crear_superficie_estrella(tamano_fijo, (168, 85, 247))
    rect_fijo = surf_fija.get_rect(center=(ANCHO // 2, ALTO // 2))
    mascara_fija = pygame.mask.from_surface(surf_fija)

    # Objeto controlado por el ratón: Un triángulo
    tamano_movil = 90
    surf_movil = pygame.Surface((tamano_movil, tamano_movil), pygame.SRCALPHA)
    puntos_triangulo = [(tamano_movil // 2, 0), (tamano_movil, tamano_movil), (0, tamano_movil)]
    pygame.draw.polygon(surf_movil, (56, 189, 248), puntos_triangulo)
    mascara_movil = pygame.mask.from_surface(surf_movil)

    while True:
        pos_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Actualizar rectángulo móvil con la posición del mouse
        rect_movil = surf_movil.get_rect(center=pos_mouse)

        # -------------------------------------------------------------
        # 1. Detección por Bounding Box (AABB)
        # -------------------------------------------------------------
        colision_caja = rect_fijo.colliderect(rect_movil)

        # -------------------------------------------------------------
        # 2. Detección por Máscara de Píxeles (Pixel-Perfect)
        # -------------------------------------------------------------
        # Calculamos el desplazamiento relativo (offset) entre ambas figuras
        offset_x = rect_movil.x - rect_fijo.x
        offset_y = rect_movil.y - rect_fijo.y
        
        # punto_impacto será una tupla (x, y) si hay colisión o None si no la hay
        punto_impacto = mascara_fija.overlap(mascara_movil, (offset_x, offset_y))
        colision_mascara = punto_impacto is not None

        # -------------------------------------------------------------
        # RENDERIZADO
        # -------------------------------------------------------------
        pantalla.fill((15, 23, 42))

        # Dibujar cajas delimitadoras (Bounding Boxes) en líneas punteadas
        color_borde_fijo = (239, 68, 68) if colision_caja else (75, 85, 99)
        pygame.draw.rect(pantalla, color_borde_fijo, rect_fijo, width=1)
        pygame.draw.rect(pantalla, color_borde_fijo, rect_movil, width=1)

        # Dibujar las superficies
        pantalla.blit(surf_fija, rect_fijo.topleft)
        pantalla.blit(surf_movil, rect_movil.topleft)

        # Si hay colisión por píxel, dibujar un punto amarillo en el punto exacto de contacto
        if punto_impacto:
            impacto_pantalla_x = rect_fijo.x + punto_impacto[0]
            impacto_pantalla_y = rect_fijo.y + punto_impacto[1]
            pygame.draw.circle(pantalla, (250, 204, 21), (impacto_pantalla_x, impacto_pantalla_y), 7)
            pygame.draw.circle(pantalla, (255, 255, 255), (impacto_pantalla_x, impacto_pantalla_y), 3)

        # Panel informativo
        panel = pygame.Rect(20, 20, 480, 130)
        pygame.draw.rect(pantalla, (30, 41, 59), panel, border_radius=8)
        pygame.draw.rect(pantalla, (100, 116, 139), panel, width=1, border_radius=8)

        lbl_titulo = fuente_titulo.render("Comparativa de Colisiones (Mueve el mouse)", True, (255, 255, 255))
        pantalla.blit(lbl_titulo, (35, 30))

        # Indicador Bounding Box
        c_caja = (239, 68, 68) if colision_caja else (148, 163, 184)
        txt_caja = f"1. Bounding Box Rect: {'¡HAY CONTACTO DE CAJAS!' if colision_caja else 'Sin contacto'}"
        pantalla.blit(fuente_info.render(txt_caja, True, c_caja), (35, 62))

        # Indicador Pixel Perfect
        c_mask = (34, 197, 94) if colision_mascara else (148, 163, 184)
        txt_mask = f"2. Máscara Pixel-Perfect: {'¡COLISIÓN REAL DE PÍXELES!' if colision_mascara else 'Sin contacto real'}"
        pantalla.blit(fuente_info.render(txt_mask, True, c_mask), (35, 90))

        # Nota explicativa
        if colision_caja and not colision_mascara:
            aviso = fuente_info.render("-> Las cajas chocan pero los gráficos no (Falso Positivo evitado)", True, (251, 191, 36))
            pantalla.blit(aviso, (35, 118))

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main()
