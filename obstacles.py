"""
=============================================================================
OBSTÁCULOS Y ENTIDADES DEL NIVEL: GEOMETRY DASH
=============================================================================
Este módulo define los elementos interactivos del nivel:
- `Spike`: Pincho mortal triangular con máscara precisa.
- `Block`: Bloque sólido (se puede aterrizar encima, chocar de frente destruye).
- `JumpPad`: Plataforma de lanzamiento automático al pisarla.
- `JumpOrb`: Orbe en el aire que impulsa si se presiona salto al pasar por él.
- `FinishPortal`: Portal vortex de final de nivel que activa la victoria.
"""

import math
import pygame
from settings import (
    COLOR_PINCHO, COLOR_PINCHO_BORDE, COLOR_BLOQUE, COLOR_BLOQUE_BORDE,
    COLOR_PAD_AMARILLO, COLOR_ORB_AMARILLO, COLOR_PORTAL
)

class Spike(pygame.sprite.Sprite):
    """Pincho triangular mortal."""
    def __init__(self, x, y, ancho=42, alto=42):
        super().__init__()
        self.ancho = ancho
        self.alto = alto
        self.image = pygame.Surface((ancho, alto), pygame.SRCALPHA)

        # Dibujar triángulo
        puntos = [(ancho // 2, 2), (ancho - 2, alto - 1), (2, alto - 1)]
        pygame.draw.polygon(self.image, COLOR_PINCHO, puntos)
        pygame.draw.polygon(self.image, COLOR_PINCHO_BORDE, puntos, width=2)

        # Borde interior decorativo
        puntos_int = [(ancho // 2, 12), (ancho - 10, alto - 5), (10, alto - 5)]
        pygame.draw.polygon(self.image, (255, 120, 120), puntos_int, width=1)

        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.tipo = "spike"

    def draw(self, pantalla, camara_x):
        pantalla.blit(self.image, (self.rect.x - camara_x, self.rect.y))


class Block(pygame.sprite.Sprite):
    """Bloque sólido de plataforma."""
    def __init__(self, x, y, ancho=42, alto=42):
        super().__init__()
        self.ancho = ancho
        self.alto = alto
        self.image = pygame.Surface((ancho, alto), pygame.SRCALPHA)

        # Relleno y borde estilo Geometry Dash
        pygame.draw.rect(self.image, COLOR_BLOQUE, (0, 0, ancho, alto))
        pygame.draw.rect(self.image, COLOR_BLOQUE_BORDE, (0, 0, ancho, alto), width=2)
        # Detalle cuadrícula interior
        pygame.draw.rect(self.image, (50, 65, 105), (6, 6, ancho - 12, alto - 12), width=1)

        self.rect = self.image.get_rect(topleft=(x, y))
        self.tipo = "block"

    def draw(self, pantalla, camara_x):
        pantalla.blit(self.image, (self.rect.x - camara_x, self.rect.y))


class JumpPad(pygame.sprite.Sprite):
    """Pad en el suelo/bloque que impulsa automáticamente al contacto."""
    def __init__(self, x, y, ancho=42, alto=14):
        super().__init__()
        self.ancho = ancho
        self.alto = alto
        self.image = pygame.Surface((ancho, alto), pygame.SRCALPHA)

        # Dibujar pad elíptico / curvo
        pygame.draw.ellipse(self.image, COLOR_PAD_AMARILLO, (0, 2, ancho, alto - 2))
        pygame.draw.ellipse(self.image, (255, 255, 255), (0, 2, ancho, alto - 2), width=2)
        # Flecha indicadora hacia arriba
        pygame.draw.line(self.image, (255, 255, 255), (ancho // 2, 4), (ancho // 2 - 5, 9), 2)
        pygame.draw.line(self.image, (255, 255, 255), (ancho // 2, 4), (ancho // 2 + 5, 9), 2)

        self.rect = self.image.get_rect(topleft=(x, y))
        self.tipo = "pad"

    def draw(self, pantalla, camara_x):
        pantalla.blit(self.image, (self.rect.x - camara_x, self.rect.y))


class JumpOrb(pygame.sprite.Sprite):
    """Orbe flotante que da impulso al saltar dentro de su radio."""
    def __init__(self, x, y, radio=22):
        super().__init__()
        self.radio = radio
        self.diametro = radio * 2
        self.image = pygame.Surface((self.diametro, self.diametro), pygame.SRCALPHA)
        self.anim_pulso = 0.0

        self.rect = self.image.get_rect(center=(x, y))
        self.tipo = "orb"
        self.activado = False

    def update(self, dt):
        self.anim_pulso += dt * 4.0

    def draw(self, pantalla, camara_x):
        px = self.rect.centerx - camara_x
        py = self.rect.centery

        # Anillo exterior pulsante
        r_exterior = int(self.radio + math.sin(self.anim_pulso) * 3)
        color_anillo = (255, 255, 200) if not self.activado else (100, 100, 100)
        color_nucleo = COLOR_ORB_AMARILLO if not self.activado else (80, 80, 80)

        pygame.draw.circle(pantalla, color_anillo, (px, py), r_exterior, width=2)
        pygame.draw.circle(pantalla, color_nucleo, (px, py), self.radio - 4)
        pygame.draw.circle(pantalla, (255, 255, 255), (px, py), max(2, self.radio - 10))


class FinishPortal(pygame.sprite.Sprite):
    """Portal de final de nivel que otorga la victoria."""
    def __init__(self, x, y, ancho=45, alto=140):
        super().__init__()
        self.ancho = ancho
        self.alto = alto
        self.rect = pygame.Rect(x, y - alto, ancho, alto)
        self.tipo = "portal"
        self.tiempo = 0.0

    def update(self, dt):
        self.tiempo += dt * 5.0

    def draw(self, pantalla, camara_x):
        px = self.rect.x - camara_x
        py = self.rect.y

        # Dibujar anillo elíptico vertical con pulso de color
        surf = pygame.Surface((self.ancho + 20, self.alto + 20), pygame.SRCALPHA)
        centro = ((self.ancho + 20) // 2, (self.alto + 20) // 2)

        # Brillo exterior
        radio_w = int((self.ancho // 2) + math.sin(self.tiempo) * 4)
        rect_elipse = pygame.Rect(centro[0] - radio_w, 10, radio_w * 2, self.alto)
        
        pygame.draw.ellipse(surf, (*COLOR_PORTAL, 120), rect_elipse)
        pygame.draw.ellipse(surf, (255, 255, 255), rect_elipse, width=3)
        
        # Núcleo brillante
        rect_core = pygame.Rect(centro[0] - radio_w // 2, 20, radio_w, self.alto - 20)
        pygame.draw.ellipse(surf, (255, 200, 255, 180), rect_core)

        pantalla.blit(surf, (px - 10, py - 10))
