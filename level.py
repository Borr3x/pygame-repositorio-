"""
=============================================================================
GESTOR Y DISEÑO DEL NIVEL: GEOMETRY DASH
=============================================================================
Este módulo construye el trazado del nivel, gestiona los obstáculos y dibuja
el fondo cyberpunk con cuadrícula animada en perspectiva y barra de progreso.
"""

import pygame
from settings import (
    ANCHO_PANTALLA, ALTO_PANTALLA, Y_SUELO, ALTURA_SUELO,
    COLOR_FONDO_1, COLOR_FONDO_2, COLOR_SUELO, COLOR_LINEA_SUELO,
    COLOR_BARRA_PROGRESO, TAMANO_CUBO
)
from obstacles import Spike, Block, JumpPad, JumpOrb, FinishPortal

class Level:
    def __init__(self):
        self.obstaculos = []
        self.orbes = []
        self.x_inicio = 100
        self.x_final = 5200  # Longitud total del recorrido
        self.construir_nivel()

    def construir_nivel(self):
        self.obstaculos.clear()
        self.orbes.clear()

        suelo = Y_SUELO
        t = TAMANO_CUBO

        # =====================================================================
        # SECCIÓN 1: Calentamiento y Pinchos Simples
        # =====================================================================
        # Pincho individual para aprender el salto
        self.obstaculos.append(Spike(550, suelo - t))
        self.obstaculos.append(Spike(850, suelo - t))

        # Doble pincho (requiere salto preciso)
        self.obstaculos.append(Spike(1200, suelo - t))
        self.obstaculos.append(Spike(1200 + t, suelo - t))

        # =====================================================================
        # SECCIÓN 2: Escalones de Bloques y Foso de Pinchos
        # =====================================================================
        x_sec2 = 1600
        # Escalón 1
        self.obstaculos.append(Block(x_sec2, suelo - t))
        # Escalón 2
        self.obstaculos.append(Block(x_sec2 + 180, suelo - t))
        self.obstaculos.append(Block(x_sec2 + 180, suelo - 2 * t))
        # Foso de pinchos debajo
        self.obstaculos.append(Spike(x_sec2 + 90, suelo - t))

        # Caída sobre plataforma elevada
        self.obstaculos.append(Block(x_sec2 + 360, suelo - 2 * t))
        self.obstaculos.append(Block(x_sec2 + 360 + t, suelo - 2 * t))
        self.obstaculos.append(Spike(x_sec2 + 280, suelo - t))

        # =====================================================================
        # SECCIÓN 3: Jump Pad (Impulso Automático Amarillo)
        # =====================================================================
        x_sec3 = 2300
        # Pad en el suelo que lanza sobre una pared alta de 3 bloques
        self.obstaculos.append(JumpPad(x_sec3, suelo - 14))
        # Pared alta que se supera gracias al pad
        self.obstaculos.append(Block(x_sec3 + 180, suelo - t))
        self.obstaculos.append(Block(x_sec3 + 180, suelo - 2 * t))
        self.obstaculos.append(Block(x_sec3 + 180, suelo - 3 * t))
        # Pincho en la cima de la pared
        self.obstaculos.append(Spike(x_sec3 + 180, suelo - 4 * t))

        # Plataforma de aterrizaje segura tras el vuelo
        self.obstaculos.append(Block(x_sec3 + 340, suelo - 2 * t))
        self.obstaculos.append(Block(x_sec3 + 340 + t, suelo - 2 * t))

        # =====================================================================
        # SECCIÓN 4: Orbe en el Aire (Jump Orb)
        # =====================================================================
        x_sec4 = 2950
        # Gran foso de 3 pinchos que no se puede saltar normal
        self.obstaculos.append(Spike(x_sec4, suelo - t))
        self.obstaculos.append(Spike(x_sec4 + t, suelo - t))
        self.obstaculos.append(Spike(x_sec4 + 2 * t, suelo - t))
        
        # Orbe amarillo flotante en medio del foso: pulsar salto en el aire
        orb1 = JumpOrb(x_sec4 + int(1.5 * t), suelo - 2 * t)
        self.orbes.append(orb1)
        self.obstaculos.append(orb1)

        # =====================================================================
        # SECCIÓN 5: Pista de Bloques Elevada con Pinchos Inferiores
        # =====================================================================
        x_sec5 = 3450
        # Salto hacia plataforma elevada
        self.obstaculos.append(Block(x_sec5, suelo - t))
        for i in range(1, 6):
            self.obstaculos.append(Block(x_sec5 + i * t, suelo - t))
            # Pincho en la mitad de la plataforma
            if i == 3:
                self.obstaculos.append(Spike(x_sec5 + i * t, suelo - 2 * t))

        # Pincho al final al bajar
        self.obstaculos.append(Spike(x_sec5 + 7 * t, suelo - t))

        # =====================================================================
        # SECCIÓN 6: Combo JumpPad + Orbe + Meta Final
        # =====================================================================
        x_sec6 = 4100
        # Pad que impulsa hacia el orbe
        self.obstaculos.append(JumpPad(x_sec6, suelo - 14))
        orb2 = JumpOrb(x_sec6 + 220, suelo - 3 * t)
        self.orbes.append(orb2)
        self.obstaculos.append(orb2)

        # Plataforma final de llegada
        self.obstaculos.append(Block(x_sec6 + 420, suelo - t))
        self.obstaculos.append(Block(x_sec6 + 420 + t, suelo - t))
        self.obstaculos.append(Block(x_sec6 + 420 + 2 * t, suelo - t))

        # Doble pincho de último desafío antes de la gloria
        self.obstaculos.append(Spike(x_sec6 + 680, suelo - t))
        self.obstaculos.append(Spike(x_sec6 + 680 + t, suelo - t))

        # Portal de Final de Nivel (Victoria)
        self.x_final = x_sec6 + 920
        self.obstaculos.append(FinishPortal(self.x_final, suelo))

    def reiniciar(self):
        # Reiniciar estado de orbes
        for orb in self.orbes:
            orb.activado = False

    def update(self, dt):
        for o in self.obstaculos:
            if hasattr(o, 'update'):
                o.update(dt)

    def draw_fondo(self, pantalla, camara_x):
        # Gradiente vertical de fondo
        pantalla.fill(COLOR_FONDO_1)
        pygame.draw.rect(pantalla, COLOR_FONDO_2, (0, 0, ANCHO_PANTALLA, Y_SUELO // 2))

        # Cuadrícula de fondo con efecto Parallax sutil
        offset_grid_bg = int(camara_x * 0.25) % 60
        for x in range(-offset_grid_bg, ANCHO_PANTALLA + 60, 60):
            pygame.draw.line(pantalla, (25, 33, 58), (x, 0), (x, Y_SUELO), 1)
        for y in range(0, Y_SUELO, 60):
            pygame.draw.line(pantalla, (25, 33, 58), (0, y), (ANCHO_PANTALLA, y), 1)

        # Suelo sólido
        pygame.draw.rect(pantalla, COLOR_SUELO, (0, Y_SUELO, ANCHO_PANTALLA, ALTURA_SUELO))
        # Línea de neón superior del suelo
        pygame.draw.line(pantalla, COLOR_LINEA_SUELO, (0, Y_SUELO), (ANCHO_PANTALLA, Y_SUELO), 3)

        # Cuadrícula rítmica del suelo en movimiento rápido
        offset_suelo = int(camara_x) % 50
        for x in range(-offset_suelo, ANCHO_PANTALLA + 50, 50):
            pygame.draw.line(pantalla, (20, 40, 70), (x, Y_SUELO), (x, ALTO_PANTALLA), 1)
        for y in range(Y_SUELO + 30, ALTO_PANTALLA, 30):
            pygame.draw.line(pantalla, (20, 40, 70), (0, y), (ANCHO_PANTALLA, y), 1)

    def draw_obstaculos(self, pantalla, camara_x):
        for obs in self.obstaculos:
            # Solo dibujar los que están cerca de la pantalla visible para optimizar
            if obs.rect.right - camara_x >= -50 and obs.rect.left - camara_x <= ANCHO_PANTALLA + 50:
                obs.draw(pantalla, camara_x)

    def calcular_porcentaje(self, x_jugador):
        distancia_total = self.x_final - self.x_inicio
        recorrido = x_jugador - self.x_inicio
        pct = (recorrido / distancia_total) * 100.0
        return max(0.0, min(100.0, pct))
