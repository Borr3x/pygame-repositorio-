"""
=============================================================================
SISTEMA DE PARTÍCULAS: EFECTOS VISUALES PARA GEOMETRY DASH
=============================================================================
Este módulo maneja:
1. Partículas de estela (Trail) detrás del cubo en movimiento.
2. Partículas de polvo al saltar y aterrizar.
3. Partículas de fragmentación / explosión cuando el cubo choca y es destruido.
"""

import math
import random
import pygame

class ParticulaEstela:
    """Partícula que deja el cubo a su paso."""
    def __init__(self, x, y, tamano, color, angulo):
        self.x = x
        self.y = y
        self.tamano_inicial = tamano
        self.tamano = tamano
        self.color = color
        self.angulo = angulo
        self.vida = 1.0  # De 1.0 a 0.0
        self.velocidad_desvanecimiento = random.uniform(3.5, 5.0)

    def update(self, dt):
        self.vida -= self.velocidad_desvanecimiento * dt
        self.tamano = max(1, self.tamano_inicial * self.vida)
        return self.vida > 0

    def draw(self, pantalla, camara_x):
        if self.vida <= 0:
            return
        px = self.x - camara_x
        py = self.y
        alpha = int(self.vida * 160)
        
        surf = pygame.Surface((int(self.tamano), int(self.tamano)), pygame.SRCALPHA)
        color_rgba = (*self.color, alpha)
        pygame.draw.rect(surf, color_rgba, (0, 0, int(self.tamano), int(self.tamano)), border_radius=3)
        
        # Rotar si es necesario
        if abs(self.angulo) > 1:
            surf_rot = pygame.transform.rotate(surf, self.angulo)
            rect = surf_rot.get_rect(center=(px, py))
            pantalla.blit(surf_rot, rect)
        else:
            rect = surf.get_rect(center=(px, py))
            pantalla.blit(surf, rect)


class ParticulaExplosion:
    """Fragmento que sale disparado en todas direcciones al morir."""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        angulo = random.uniform(0, 2 * math.pi)
        rapidez = random.uniform(150, 600)
        self.vx = math.cos(angulo) * rapidez
        self.vy = math.sin(angulo) * rapidez
        self.gravedad = 1200.0
        self.tamano = random.uniform(4, 10)
        self.vida = 1.0
        self.desvanecimiento = random.uniform(1.2, 2.5)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravedad * dt
        self.vida -= self.desvanecimiento * dt
        return self.vida > 0

    def draw(self, pantalla, camara_x):
        if self.vida <= 0:
            return
        px = self.x - camara_x
        py = self.y
        alpha = int(max(0, min(255, self.vida * 255)))
        
        surf = pygame.Surface((int(self.tamano * 2), int(self.tamano * 2)), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, alpha), (int(self.tamano), int(self.tamano)), int(self.tamano))
        pantalla.blit(surf, (px - self.tamano, py - self.tamano))


class ParticulaPolvo:
    """Pequeñas chispas/polvo que emergen al despegar o tocar suelo."""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-100, -20)
        self.vy = random.uniform(-60, 10)
        self.color = color
        self.radio = random.uniform(2, 5)
        self.vida = 1.0
        self.desvanecimiento = random.uniform(3.0, 5.0)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vida -= self.desvanecimiento * dt
        return self.vida > 0

    def draw(self, pantalla, camara_x):
        if self.vida <= 0:
            return
        px = self.x - camara_x
        py = self.y
        alpha = int(self.vida * 200)
        surf = pygame.Surface((int(self.radio * 2), int(self.radio * 2)), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, alpha), (int(self.radio), int(self.radio)), int(self.radio))
        pantalla.blit(surf, (px - self.radio, py - self.radio))


class ParticleManager:
    """Administrador centralizado de partículas."""
    def __init__(self):
        self.estelas = []
        self.explosiones = []
        self.polvo = []

    def crear_estela(self, x, y, tamano, color, angulo):
        self.estelas.append(ParticulaEstela(x, y, tamano, color, angulo))

    def crear_polvo(self, x, y, color=(255, 255, 255), cantidad=5):
        for _ in range(cantidad):
            self.polvo.append(ParticulaPolvo(x, y, color))

    def crear_explosion(self, x, y, color=(57, 255, 20), cantidad=40):
        for _ in range(cantidad):
            self.explosiones.append(ParticulaExplosion(x, y, color))
            # Añadir fragmentos de color blanco / contraste
            if random.random() < 0.35:
                self.explosiones.append(ParticulaExplosion(x, y, (255, 255, 255)))

    def update(self, dt):
        self.estelas = [p for p in self.estelas if p.update(dt)]
        self.polvo = [p for p in self.polvo if p.update(dt)]
        self.explosiones = [p for p in self.explosiones if p.update(dt)]

    def draw(self, pantalla, camara_x):
        for p in self.estelas:
            p.draw(pantalla, camara_x)
        for p in self.polvo:
            p.draw(pantalla, camara_x)
        for p in self.explosiones:
            p.draw(pantalla, camara_x)

    def reiniciar(self):
        self.estelas.clear()
        self.polvo.clear()
        self.explosiones.clear()
