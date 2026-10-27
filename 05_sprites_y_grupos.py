"""
=============================================================================
EJEMPLO 05: Arquitectura de Sprites y Grupos (POO en Pygame)
=============================================================================
Este script muestra el estándar de Programación Orientada a Objetos en Pygame:
1. Creación de clases que heredan de `pygame.sprite.Sprite`.
2. Requisitos de un Sprite: poseer `self.image` (Surface) y `self.rect` (Rect).
3. Uso de `pygame.sprite.Group` para gestionar colecciones de entidades.
4. Llamadas por lotes a `grupo.update()` y `grupo.draw()`.
5. Destrucción limpia de objetos con `sprite.kill()` cuando salen de pantalla.
"""

import sys
import random
import pygame

class Asteroide(pygame.sprite.Sprite):
    """Sprite de asteroide que cae desde la parte superior."""
    def __init__(self, limite_ancho, limite_alto):
        super().__init__()
        self.limite_alto = limite_alto
        self.radio = random.randint(15, 30)
        self.diametro = self.radio * 2

        # 1. Crear la superficie (self.image) con canal alfa
        self.image = pygame.Surface((self.diametro, self.diametro), pygame.SRCALPHA)
        color = random.choice([(239, 68, 68), (245, 158, 11), (139, 92, 246), (16, 185, 129)])
        pygame.draw.circle(self.image, color, (self.radio, self.radio), self.radio)
        pygame.draw.circle(self.image, (255, 255, 255), (self.radio, self.radio), self.radio, width=2)

        # 2. Definir el rectángulo delimitador (self.rect)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, limite_ancho - self.diametro)
        self.rect.y = random.randint(-100, -40)

        self.vel_y = random.uniform(2.0, 5.5)
        self.vel_x = random.uniform(-1.0, 1.0)

    def update(self):
        """Actualizar posición del asteroide."""
        self.rect.y += int(self.vel_y)
        self.rect.x += int(self.vel_x)

        # Si el asteroide sale por la parte inferior, se auto-elimina del grupo
        if self.rect.top > self.limite_alto:
            self.kill()


class NaveJugador(pygame.sprite.Sprite):
    """Sprite controlado por el usuario."""
    def __init__(self, x, y):
        super().__init__()
        self.ancho, self.alto = 50, 40
        self.image = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        
        # Dibujar una nave triangular
        puntos = [(self.ancho // 2, 0), (self.ancho, self.alto), (0, self.alto)]
        pygame.draw.polygon(self.image, (56, 189, 248), puntos)
        pygame.draw.polygon(self.image, (255, 255, 255), puntos, width=2)

        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 6

    def update(self):
        """Mover la nave horizontalmente con el teclado."""
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidad

        # Limitar dentro de los bordes de la pantalla (800 px)
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(800, self.rect.right)


def main():
    pygame.init()
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("05 - Arquitectura de Sprites y Grupos")

    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Arial", 16)

    # Crear grupo de sprites
    grupo_asteroides = pygame.sprite.Group()
    jugador = NaveJugador(ANCHO // 2, ALTO - 60)
    grupo_jugador = pygame.sprite.GroupSingle(jugador)

    # Temporizador de evento personalizado para generar asteroides
    EVENTO_SPAWN = pygame.USEREVENT + 1
    pygame.time.set_timer(EVENTO_SPAWN, 250)  # Cada 250 ms

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Evento periódico de generación
            elif evento.type == EVENTO_SPAWN:
                if len(grupo_asteroides) < 40:
                    grupo_asteroides.add(Asteroide(ANCHO, ALTO))

        # -------------------------------------------------------------
        # ACTUALIZACIÓN POR LOTES
        # -------------------------------------------------------------
        grupo_jugador.update()
        grupo_asteroides.update()

        # Detección de colisiones grupales (jugador contra cualquier asteroide)
        asteroides_colisionados = pygame.sprite.spritecollide(jugador, grupo_asteroides, True)

        # -------------------------------------------------------------
        # DIBUJADO POR LOTES
        # -------------------------------------------------------------
        pantalla.fill((15, 23, 42))

        # Dibujar todos los sprites en una sola línea
        grupo_asteroides.draw(pantalla)
        grupo_jugador.draw(pantalla)

        # Información en pantalla
        info_txt = [
            "Controles: [A] / [D] o [Flechas Izquierda / Derecha]",
            f"Sprites activos en grupo_asteroides: {len(grupo_asteroides)}",
            f"Impactos recibidos: {len(asteroides_colisionados)}"
        ]
        for i, txt in enumerate(info_txt):
            lbl = fuente.render(txt, True, (241, 245, 249))
            pantalla.blit(lbl, (20, 20 + i * 26))

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main()
