"""
=============================================================================
EJEMPLO 04: Interacción con el Ratón (Mouse), Botones y Arrastre (Drag & Drop)
=============================================================================
Este script muestra cómo gestionar el puntero del ratón en Pygame:
1. Lectura de posición del cursor (`pygame.mouse.get_pos()`).
2. Detección de clics mediante eventos (`MOUSEBUTTONDOWN`, `MOUSEBUTTONUP`).
3. Construcción de una clase `Boton` reutilizable con efectos hover y callback.
4. Mecánica de arrastrar y soltar (Drag and Drop) con detección `collidepoint`.
5. Cambio dinámico del cursor del sistema.
"""

import sys
import pygame

class Boton:
    """Clase para crear botones UI interactivos."""
    def __init__(self, x, y, ancho, alto, texto, color_base, color_hover, color_click, callback=None):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_base = color_base
        self.color_hover = color_hover
        self.color_click = color_click
        self.callback = callback
        self.esta_hover = False
        self.esta_presionado = False

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEMOTION:
            self.esta_hover = self.rect.collidepoint(evento.pos)
        
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                self.esta_presionado = True

        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            if self.esta_presionado and self.rect.collidepoint(evento.pos):
                if self.callback:
                    self.callback()
            self.esta_presionado = False

    def dibujar(self, pantalla, fuente):
        if self.esta_presionado:
            color = self.color_click
        elif self.esta_hover:
            color = self.color_hover
        else:
            color = self.color_base

        pygame.draw.rect(pantalla, color, self.rect, border_radius=10)
        pygame.draw.rect(pantalla, (255, 255, 255), self.rect, width=2, border_radius=10)

        superficie_texto = fuente.render(self.texto, True, (255, 255, 255))
        pos_texto = superficie_texto.get_rect(center=self.rect.center)
        pantalla.blit(superficie_texto, pos_texto)


def main():
    pygame.init()
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("04 - Mouse, Botones UI y Drag & Drop")

    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Arial", 16)
    fuente_boton = pygame.font.SysFont("Arial", 18, bold=True)

    # Estado del programa
    contador_clics = 0
    color_fondo_actual = (24, 24, 27)

    def incrementar_contador():
        nonlocal contador_clics
        contador_clics += 1

    def cambiar_color_fondo():
        nonlocal color_fondo_actual
        if color_fondo_actual == (24, 24, 27):
            color_fondo_actual = (15, 32, 67)
        else:
            color_fondo_actual = (24, 24, 27)

    # Crear botones
    boton_sumar = Boton(
        50, 80, 200, 50, "¡Haz Clic Aquí!", 
        (79, 70, 229), (99, 102, 241), (67, 56, 202), 
        callback=incrementar_contador
    )
    boton_color = Boton(
        50, 150, 200, 50, "Cambiar Fondo", 
        (13, 148, 136), (20, 184, 166), (15, 118, 110), 
        callback=cambiar_color_fondo
    )

    # Objeto arrastrable (Drag and Drop)
    caja_arrastrable = pygame.Rect(450, 180, 120, 120)
    arrastrando = False
    offset_x = 0
    offset_y = 0

    while True:
        pos_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Pasar eventos a los botones
            boton_sumar.manejar_evento(evento)
            boton_color.manejar_evento(evento)

            # Lógica de arrastre
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if caja_arrastrable.collidepoint(evento.pos):
                    arrastrando = True
                    offset_x = caja_arrastrable.x - evento.pos[0]
                    offset_y = caja_arrastrable.y - evento.pos[1]

            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                arrastrando = False

            elif evento.type == pygame.MOUSEMOTION:
                if arrastrando:
                    caja_arrastrable.x = evento.pos[0] + offset_x
                    caja_arrastrable.y = evento.pos[1] + offset_y

        # Cambiar el cursor del ratón según el contexto
        if arrastrando or caja_arrastrable.collidepoint(pos_mouse):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
        elif boton_sumar.esta_hover or boton_color.esta_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Renderizado
        pantalla.fill(color_fondo_actual)

        # Título
        lbl_titulo = fuente_boton.render("Demostración de Mouse: Botones Interactivos y Drag & Drop", True, (255, 255, 255))
        pantalla.blit(lbl_titulo, (50, 30))

        # Dibujar botones
        boton_sumar.dibujar(pantalla, fuente_boton)
        boton_color.dibujar(pantalla, fuente_boton)

        # Contador de clics
        lbl_contador = fuente.render(f"Clics registrados: {contador_clics}", True, (226, 232, 240))
        pantalla.blit(lbl_contador, (50, 220))

        # Objeto arrastrable
        color_caja = (234, 88, 12) if arrastrando else (249, 115, 22)
        pygame.draw.rect(pantalla, color_caja, caja_arrastrable, border_radius=12)
        pygame.draw.rect(pantalla, (255, 237, 213), caja_arrastrable, width=2, border_radius=12)
        
        lbl_arrastre = fuente.render("¡Arrástrame!", True, (255, 255, 255))
        pantalla.blit(lbl_arrastre, (caja_arrastrable.centerx - lbl_arrastre.get_width() // 2,
                                     caja_arrastrable.centery - lbl_arrastre.get_height() // 2))

        # Coordenadas del mouse en pantalla
        lbl_coordenadas = fuente.render(f"Posición del cursor: X={pos_mouse[0]} | Y={pos_mouse[1]}", True, (148, 163, 184))
        pantalla.blit(lbl_coordenadas, (50, ALTO - 40))

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main()
