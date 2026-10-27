"""
=============================================================================
CLASE JUGADOR (CUBO): GEOMETRY DASH
=============================================================================
Este módulo define la física, animación de rotación, saltos y colisiones
del cubo característico de Geometry Dash:
- Avance horizontal constante.
- Gravedad y salto plataformero.
- Rotación continua en el aire con alineación automática a 90° al aterrizar.
- Interacción con bloques (aterrizar sobre ellos o estrellarse contra sus lados).
- Impulsos con Pads y Orbes.
"""

import math
import pygame
from settings import (
    TAMANO_CUBO, VELOCIDAD_SCROLL, GRAVEDAD, FUERZA_SALTO,
    FUERZA_JUMP_PAD, FUERZA_ORB, VELOCIDAD_ROTACION, Y_SUELO,
    COLOR_CUBO, COLOR_CUBO_BORDE, COLOR_CUBO_OJOS
)

class Player(pygame.sprite.Sprite):
    def __init__(self, x=100, y=Y_SUELO - TAMANO_CUBO):
        super().__init__()
        self.tamano = TAMANO_CUBO
        self.x = float(x)
        self.y = float(y)
        self.vx = VELOCIDAD_SCROLL
        self.vy = 0.0

        self.en_suelo = False
        self.vivo = True
        self.ha_ganado = False
        self.angulo = 0.0  # Ángulo de rotación

        # Construir la textura base del cubo con su cara icónica
        self.image_base = self._crear_textura_cubo()
        self.image = self.image_base
        self.rect = pygame.Rect(int(self.x), int(self.y), self.tamano, self.tamano)
        self.mask = pygame.mask.from_surface(self.image)

        # Contador para emitir partículas de estela
        self.temporizador_estela = 0.0

    def _crear_textura_cubo(self):
        surf = pygame.Surface((self.tamano, self.tamano), pygame.SRCALPHA)
        # Relleno neón
        pygame.draw.rect(surf, COLOR_CUBO, (0, 0, self.tamano, self.tamano), border_radius=4)
        # Borde exterior blanco
        pygame.draw.rect(surf, COLOR_CUBO_BORDE, (0, 0, self.tamano, self.tamano), width=3, border_radius=4)

        # Ojos / Rostro geométrico icónico
        ojo_w, ojo_h = 7, 10
        # Ojo izquierdo
        pygame.draw.rect(surf, COLOR_CUBO_OJOS, (10, 12, ojo_w, ojo_h), border_radius=2)
        # Ojo derecho
        pygame.draw.rect(surf, COLOR_CUBO_OJOS, (25, 12, ojo_w, ojo_h), border_radius=2)
        # Pupilas brillantes
        pygame.draw.rect(surf, (255, 255, 255), (12, 14, 3, 3))
        pygame.draw.rect(surf, (255, 255, 255), (27, 14, 3, 3))
        # Boca / ranura
        pygame.draw.rect(surf, COLOR_CUBO_OJOS, (12, 28, 18, 4), border_radius=2)

        return surf

    def reiniciar(self, x=100, y=Y_SUELO - TAMANO_CUBO):
        self.x = float(x)
        self.y = float(y)
        self.vx = VELOCIDAD_SCROLL
        self.vy = 0.0
        self.en_suelo = False
        self.vivo = True
        self.ha_ganado = False
        self.angulo = 0.0
        self.rect.topleft = (int(self.x), int(self.y))
        self.mask = pygame.mask.from_surface(self.image_base)

    def saltar(self, audio_manager, particle_manager):
        """Intenta saltar si está en el suelo."""
        if not self.vivo or self.ha_ganado:
            return False

        if self.en_suelo:
            self.vy = FUERZA_SALTO
            self.en_suelo = False
            audio_manager.play_salto()
            particle_manager.crear_polvo(self.rect.centerx, self.rect.bottom, (255, 255, 255), 8)
            return True
        return False

    def intentar_orbe(self, grupo_orbes, audio_manager, particle_manager):
        """Activa un salto en el aire si está en rango de un orbe amarillo."""
        if not self.vivo or self.ha_ganado:
            return False

        for orb in grupo_orbes:
            if not orb.activado and self.rect.colliderect(orb.rect):
                dist = math.hypot(self.rect.centerx - orb.rect.centerx, self.rect.centery - orb.rect.centery)
                if dist < orb.radio + self.tamano // 2:
                    self.vy = FUERZA_ORB
                    self.en_suelo = False
                    orb.activado = True
                    audio_manager.play_orb()
                    particle_manager.crear_polvo(orb.rect.centerx, orb.rect.centery, (255, 230, 0), 14)
                    return True
        return False

    def update(self, dt, grupo_obstaculos, audio_manager, particle_manager):
        if not self.vivo or self.ha_ganado:
            return

        y_previa = self.y

        # 1. Movimiento horizontal
        self.x += self.vx * dt

        # 2. Aplicar gravedad
        self.vy += GRAVEDAD * dt
        self.y += self.vy * dt

        # 3. Rotación: mientras esté en el aire gira suavemente hacia adelante
        if not self.en_suelo:
            self.angulo -= VELOCIDAD_ROTACION * dt
        else:
            # Al tocar suelo o bloque, alinear al múltiplo de 90° más próximo
            angulo_cercano = round(self.angulo / 90.0) * 90.0
            self.angulo = self.angulo + (angulo_cercano - self.angulo) * min(1.0, 15.0 * dt)

        # 4. Colisión con el suelo principal
        if self.y >= Y_SUELO - self.tamano:
            self.y = Y_SUELO - self.tamano
            if not self.en_suelo and self.vy > 100:
                particle_manager.crear_polvo(self.rect.centerx, self.rect.bottom, (200, 255, 255), 4)
            self.vy = 0.0
            self.en_suelo = True
        else:
            self.en_suelo = False

        # Actualizar rectángulo de colisión provisional
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # 5. Colisión con Bloques, Pads, Pinchos y Portales
        for obs in grupo_obstaculos:
            if not self.rect.colliderect(obs.rect):
                continue

            if obs.tipo == "spike":
                # Colisión por máscara con el pincho
                offset_x = obs.rect.x - self.rect.x
                offset_y = obs.rect.y - self.rect.y
                # Reducir ligeramente la caja de colisión para que sea justo
                if self.mask.overlap(obs.mask, (offset_x, offset_y)):
                    self._morir(audio_manager, particle_manager)
                    return

            elif obs.tipo == "block":
                # Tolerancia para aterrizar en la cara superior del bloque
                aterrizaje_valido = (y_previa + self.tamano <= obs.rect.top + 16) and (self.vy >= 0)

                if aterrizaje_valido:
                    self.y = obs.rect.top - self.tamano
                    self.vy = 0.0
                    self.en_suelo = True
                    self.rect.y = int(self.y)
                else:
                    # Choque frontal o inferior con el bloque
                    self._morir(audio_manager, particle_manager)
                    return

            elif obs.tipo == "pad":
                # Al pisar el pad se impulsa de forma automática
                self.vy = FUERZA_JUMP_PAD
                self.en_suelo = False
                audio_manager.play_pad()
                particle_manager.crear_polvo(obs.rect.centerx, obs.rect.top, (255, 215, 0), 12)

            elif obs.tipo == "portal":
                # Llegó a la meta
                self.ha_ganado = True
                audio_manager.play_victoria()
                particle_manager.crear_explosion(self.rect.centerx, self.rect.centery, (180, 50, 255), 50)
                return

        # 6. Partículas de estela
        self.temporizador_estela += dt
        if self.temporizador_estela >= 0.04:
            self.temporizador_estela = 0.0
            particle_manager.crear_estela(
                self.rect.centerx, self.rect.centery,
                self.tamano, COLOR_CUBO, self.angulo
            )

        # 7. Actualizar rotación del sprite
        self._actualizar_superficie_rotada()

    def _morir(self, audio_manager, particle_manager):
        self.vivo = False
        audio_manager.play_muerte()
        particle_manager.crear_explosion(self.rect.centerx, self.rect.centery, COLOR_CUBO, 45)

    def _actualizar_superficie_rotada(self):
        # Rotar la imagen base alrededor del centro
        self.image = pygame.transform.rotate(self.image_base, self.angulo)
        self.rect = self.image.get_rect(center=(int(self.x + self.tamano / 2), int(self.y + self.tamano / 2)))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, pantalla, camara_x):
        if self.vivo:
            pantalla.blit(self.image, (self.rect.x - camara_x, self.rect.y))
