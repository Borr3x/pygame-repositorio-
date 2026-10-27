"""
=============================================================================
GEOMETRY DASH - PYGAME EDITION
=============================================================================
Punto de entrada principal del videojuego:
- Gestión de estados de juego (MENÚ, JUGANDO, GAME OVER, VICTORIA).
- Cámara fluida que sigue al cubo.
- Efecto de sacudida de pantalla (Screen Shake) al colisionar.
- HUD superior con barra de progreso porcentual del nivel (0% a 100%).
- Contador de intentos y persistencia de mejor porcentaje alcanzado.
- Música rítmica generada por software y efectos de sonido procedurales.

Controles:
  - [ESPACIO], [FLECHA ARRIBA] o [CLIC IZQUIERDO]: Saltar / Activar Orbe
  - [R]: Reinicio rápido
  - [P]: Pausar / Reanudar
  - [ESC]: Volver al menú o salir
"""

import sys
import random
import pygame

from settings import (
    ANCHO_PANTALLA, ALTO_PANTALLA, FPS, TITULO,
    COLOR_TEXTO, COLOR_TEXTO_MUTED, COLOR_BARRA_PROGRESO,
    COLOR_CUBO, COLOR_PINCHO, Y_SUELO
)
from audio_manager import AudioManager
from particles import ParticleManager
from player import Player
from level import Level

class GeometryDashGame:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()

        # Fuentes tipográficas
        self.fuente_logo = pygame.font.SysFont("Arial", 52, bold=True)
        self.fuente_grande = pygame.font.SysFont("Arial", 32, bold=True)
        self.fuente_media = pygame.font.SysFont("Arial", 20, bold=True)
        self.fuente_pequena = pygame.font.SysFont("Arial", 16)

        # Módulos del juego
        self.audio = AudioManager()
        self.particles = ParticleManager()
        self.level = Level()
        self.player = Player()

        # Estados: "MENU", "JUGANDO", "GAME_OVER", "VICTORIA"
        self.estado = "MENU"

        # Estadísticas
        self.intentos = 1
        self.mejor_porcentaje = 0.0
        self.porcentaje_actual = 0.0

        # Efecto de sacudida de pantalla (Screen Shake)
        self.shake_tiempo = 0.0
        self.shake_magnitud = 0

        # Animación del menú
        self.tiempo_menu = 0.0

    def iniciar_partida(self):
        self.player.reiniciar()
        self.level.reiniciar()
        self.particles.reiniciar()
        self.estado = "JUGANDO"
        self.audio.reproducir_musica()

    def procesar_entrada_salto(self):
        """Maneja el intento de salto o activación de orbe."""
        if self.estado == "JUGANDO":
            # 1. Intentar activar orbe en el aire
            orbe_usado = self.player.intentar_orbe(self.level.orbes, self.audio, self.particles)
            # 2. Si no tocó un orbe, intentar salto normal si está en el suelo
            if not orbe_usado:
                self.player.saltar(self.audio, self.particles)

        elif self.estado in ("GAME_OVER", "VICTORIA"):
            self.intentos += 1
            self.iniciar_partida()

        elif self.estado == "MENU":
            self.iniciar_partida()

    def trigger_shake(self, duracion=0.25, magnitud=7):
        self.shake_tiempo = duracion
        self.shake_magnitud = magnitud

    def actualizar(self, dt):
        self.particles.update(dt)

        # Actualizar sacudida de pantalla
        if self.shake_tiempo > 0:
            self.shake_tiempo -= dt
        else:
            self.shake_magnitud = 0

        if self.estado == "MENU":
            self.tiempo_menu += dt

        elif self.estado == "JUGANDO":
            self.level.update(dt)
            self.player.update(dt, self.level.obstaculos, self.audio, self.particles)

            self.porcentaje_actual = self.level.calcular_porcentaje(self.player.x)
            if self.porcentaje_actual > self.mejor_porcentaje:
                self.mejor_porcentaje = self.porcentaje_actual

            # Verificar si murió
            if not self.player.vivo:
                self.estado = "GAME_OVER"
                self.trigger_shake(duracion=0.35, magnitud=10)
                self.audio.detener_musica()

            # Verificar si ganó
            elif self.player.ha_ganado:
                self.estado = "VICTORIA"
                self.mejor_porcentaje = 100.0
                self.audio.detener_musica()

    def dibujar_hud(self):
        """Dibuja la barra de progreso y las estadísticas superiores."""
        ancho_barra = 400
        alto_barra = 14
        x_barra = ANCHO_PANTALLA // 2 - ancho_barra // 2
        y_barra = 20

        # Fondo de la barra
        pygame.draw.rect(self.pantalla, (20, 25, 45), (x_barra, y_barra, ancho_barra, alto_barra), border_radius=6)
        
        # Relleno del progreso actual
        pct = self.porcentaje_actual / 100.0
        ancho_progreso = int(ancho_barra * pct)
        if ancho_progreso > 0:
            pygame.draw.rect(self.pantalla, COLOR_BARRA_PROGRESO, (x_barra, y_barra, ancho_progreso, alto_barra), border_radius=6)
        pygame.draw.rect(self.pantalla, (255, 255, 255), (x_barra, y_barra, ancho_barra, alto_barra), width=2, border_radius=6)

        # Texto del porcentaje
        lbl_pct = self.fuente_media.render(f"{int(self.porcentaje_actual)}%", True, COLOR_TEXTO)
        self.pantalla.blit(lbl_pct, (x_barra + ancho_barra + 15, y_barra - 4))

        # Indicador de Intento actual
        lbl_intento = self.fuente_pequena.render(f"Intento {self.intentos}", True, COLOR_TEXTO_MUTED)
        self.pantalla.blit(lbl_intento, (25, 20))

    def renderizar(self):
        # Desplazamiento por sacudida de pantalla
        offset_shake_x = 0
        offset_shake_y = 0
        if self.shake_tiempo > 0:
            offset_shake_x = random.randint(-self.shake_magnitud, self.shake_magnitud)
            offset_shake_y = random.randint(-self.shake_magnitud, self.shake_magnitud)

        # Superficie de render con posible shake
        camara_x = self.player.x - 220 if self.estado != "MENU" else 0

        # Dibujar fondo y suelo
        self.level.draw_fondo(self.pantalla, camara_x)

        # Dibujar obstáculos del nivel
        self.level.draw_obstaculos(self.pantalla, camara_x)

        # Dibujar partículas (estelas, explosiones, polvo)
        self.particles.draw(self.pantalla, camara_x)

        # Dibujar al cubo si sigue vivo
        self.player.draw(self.pantalla, camara_x)

        # Superposiciones según el estado
        if self.estado == "JUGANDO":
            self.dibujar_hud()

        elif self.estado == "MENU":
            self.dibujar_menu()

        elif self.estado == "GAME_OVER":
            self.dibujar_game_over()

        elif self.estado == "VICTORIA":
            self.dibujar_victoria()

        # Aplicar el offset si hay sacudida activa
        if offset_shake_x != 0 or offset_shake_y != 0:
            copia = self.pantalla.copy()
            self.pantalla.fill((0, 0, 0))
            self.pantalla.blit(copia, (offset_shake_x, offset_shake_y))

        pygame.display.flip()

    def dibujar_menu(self):
        # Cubo demostrativo saltando y girando en el menú
        y_cubo_demo = (Y_SUELO - 42) - abs(int(45 * pygame.math.Vector2(0, 1).rotate(self.tiempo_menu * 220).y))
        rot_cubo_demo = self.tiempo_menu * 180
        cubo_rot = pygame.transform.rotate(self.player.image_base, rot_cubo_demo)
        self.pantalla.blit(cubo_rot, (ANCHO_PANTALLA // 2 - cubo_rot.get_width() // 2, y_cubo_demo))

        # Título estilo neón
        txt_titulo = self.fuente_logo.render("GEOMETRY DASH", True, (0, 245, 255))
        rect_t = txt_titulo.get_rect(center=(ANCHO_PANTALLA // 2, 130))
        # Sombra de neón
        txt_sombra = self.fuente_logo.render("GEOMETRY DASH", True, (0, 100, 150))
        self.pantalla.blit(txt_sombra, (rect_t.x + 3, rect_t.y + 3))
        self.pantalla.blit(txt_titulo, rect_t)

        sub_titulo = self.fuente_media.render("PYTHON & PYGAME EDITION", True, COLOR_CUBO)
        self.pantalla.blit(sub_titulo, sub_titulo.get_rect(center=(ANCHO_PANTALLA // 2, 185)))

        # Botón / Aviso parpadeante
        if int(self.tiempo_menu * 2.5) % 2 == 0:
            txt_play = self.fuente_grande.render("PRESIONA [ESPACIO] O CLIC PARA JUGAR", True, (255, 255, 255))
            self.pantalla.blit(txt_play, txt_play.get_rect(center=(ANCHO_PANTALLA // 2, 280)))

        # Estadísticas previas
        txt_record = self.fuente_pequena.render(f"Mejor Marca: {int(self.mejor_porcentaje)}% | Intentos: {self.intentos}", True, COLOR_TEXTO_MUTED)
        self.pantalla.blit(txt_record, txt_record.get_rect(center=(ANCHO_PANTALLA // 2, 330)))

        # Guía de controles
        txt_guia = self.fuente_pequena.render("[ESPACIO] / [CLIC]: Saltar  |  Toca los Orbes Amarillos en el aire para impulsarte", True, (180, 200, 220))
        self.pantalla.blit(txt_guia, txt_guia.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA - 40)))

    def dibujar_game_over(self):
        self.dibujar_hud()

        # Panel semitransparente
        overlay = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.pantalla.blit(overlay, (0, 0))

        txt_fallo = self.fuente_grande.render("¡INTENTO FALLIDO!", True, COLOR_PINCHO)
        self.pantalla.blit(txt_fallo, txt_fallo.get_rect(center=(ANCHO_PANTALLA // 2, 210)))

        txt_pct = self.fuente_media.render(f"Progreso alcanzado: {int(self.porcentaje_actual)}%", True, COLOR_TEXTO)
        self.pantalla.blit(txt_pct, txt_pct.get_rect(center=(ANCHO_PANTALLA // 2, 260)))

        txt_reintentar = self.fuente_pequena.render("Presiona [ESPACIO], [R] o [CLIC] para reintentar", True, (200, 220, 240))
        self.pantalla.blit(txt_reintentar, txt_reintentar.get_rect(center=(ANCHO_PANTALLA // 2, 310)))

    def dibujar_victoria(self):
        self.dibujar_hud()

        overlay = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)
        overlay.fill((10, 25, 40, 150))
        self.pantalla.blit(overlay, (0, 0))

        txt_vic = self.fuente_logo.render("¡NIVEL COMPLETADO! 100%", True, (57, 255, 20))
        self.pantalla.blit(txt_vic, txt_vic.get_rect(center=(ANCHO_PANTALLA // 2, 200)))

        txt_stats = self.fuente_media.render(f"Superado en el intento #{self.intentos}", True, COLOR_TEXTO)
        self.pantalla.blit(txt_stats, txt_stats.get_rect(center=(ANCHO_PANTALLA // 2, 260)))

        txt_restart = self.fuente_pequena.render("Presiona [ESPACIO] o [R] para jugar de nuevo", True, (200, 220, 240))
        self.pantalla.blit(txt_restart, txt_restart.get_rect(center=(ANCHO_PANTALLA // 2, 310)))

    def ejecutar(self):
        ejecutando = True

        while ejecutando:
            dt = self.reloj.tick(FPS) / 1000.0
            dt = min(dt, 0.05)  # Clamping para evitar saltos bruscos en caídas de frames

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False

                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        if self.estado == "JUGANDO":
                            self.estado = "MENU"
                            self.audio.detener_musica()
                        else:
                            ejecutando = False

                    elif evento.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                        self.procesar_entrada_salto()

                    elif evento.key == pygame.K_r:
                        if self.estado in ("JUGANDO", "GAME_OVER", "VICTORIA"):
                            self.intentos += 1
                            self.iniciar_partida()

                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self.procesar_entrada_salto()

            self.actualizar(dt)
            self.renderizar()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    juego = GeometryDashGame()
    juego.ejecutar()
