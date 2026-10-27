"""
=============================================================================
EJEMPLO 02: Dibujo de Formas Geométricas y Transparencias
=============================================================================
Este script demuestra cómo utilizar el módulo `pygame.draw` y superficies con
canal Alfa (transparencia) para crear gráficos vectoriales 2D:
1. Rectángulos (con esquinas redondeadas y bordes).
2. Círculos y arcos.
3. Líneas y polilíneas con grosor configurable.
4. Polígonos (triángulos, estrellas).
5. Superficies con transparencia (SRCALPHA) para efectos de iluminación/sombras.
"""

import sys
import math
import pygame

def main():
    pygame.init()
    ANCHO, ALTO = 900, 650
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("02 - Dibujo de Primitivas Geométricas y Transparencias")

    reloj = pygame.time.Clock()

    # Paleta de Colores
    COLOR_FONDO = (20, 24, 34)
    BLANCO = (255, 255, 255)
    GRIS_TEXTO = (160, 174, 192)
    ROJO_NEON = (255, 75, 92)
    VERDE_NEON = (72, 226, 144)
    AZUL_CIELO = (56, 189, 248)
    AMARILLO_ORO = (251, 191, 36)
    PURPURA = (168, 85, 247)

    fuente_titulo = pygame.font.SysFont("Arial", 22, bold=True)
    fuente_etiqueta = pygame.font.SysFont("Arial", 14)

    angulo_animacion = 0.0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        angulo_animacion += 0.03

        # Limpieza de pantalla
        pantalla.fill(COLOR_FONDO)

        # Encabezado
        titulo = fuente_titulo.render("Demostración de Dibujo con pygame.draw y Alpha", True, BLANCO)
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 20))

        # -------------------------------------------------------------
        # 1. RECTÁNGULOS (Sólido y con bordes redondeados)
        # -------------------------------------------------------------
        # Rectángulo relleno con bordes redondeados
        rect_1 = pygame.Rect(50, 90, 160, 100)
        pygame.draw.rect(pantalla, AZUL_CIELO, rect_1, border_radius=15)
        
        # Rectángulo solo contorno con bordes
        rect_2 = pygame.Rect(50, 210, 160, 100)
        pygame.draw.rect(pantalla, VERDE_NEON, rect_2, width=4, border_radius=8)

        # -------------------------------------------------------------
        # 2. CÍRCULOS Y ELIPSES
        # -------------------------------------------------------------
        # Círculo relleno
        centro_circulo = (320, 140)
        pygame.draw.circle(pantalla, ROJO_NEON, centro_circulo, 50)

        # Círculo hueco con pulsación animada
        radio_pulsante = int(45 + math.sin(angulo_animacion * 2) * 8)
        pygame.draw.circle(pantalla, AMARILLO_ORO, (320, 260), radio_pulsante, width=3)

        # Elipse
        rect_elipse = pygame.Rect(260, 330, 120, 70)
        pygame.draw.ellipse(pantalla, PURPURA, rect_elipse, width=3)

        # -------------------------------------------------------------
        # 3. POLÍGONOS (Triángulo y Estrella giratoria)
        # -------------------------------------------------------------
        # Triángulo equilátero
        puntos_triangulo = [(530, 90), (470, 190), (590, 190)]
        pygame.draw.polygon(pantalla, AMARILLO_ORO, puntos_triangulo)

        # Estrella de 5 puntas calculada trigonométricamente
        cx, cy = 530, 260
        r_ext, r_int = 45, 20
        puntos_estrella = []
        for i in range(10):
            r = r_ext if i % 2 == 0 else r_int
            theta = angulo_animacion + i * (math.pi / 5)
            puntos_estrella.append((cx + r * math.cos(theta), cy + r * math.sin(theta)))
        pygame.draw.polygon(pantalla, VERDE_NEON, puntos_estrella)

        # -------------------------------------------------------------
        # 4. LÍNEAS Y POLILÍNEAS
        # -------------------------------------------------------------
        # Línea antialiased con grosor
        pygame.draw.line(pantalla, AZUL_CIELO, (680, 100), (840, 140), 4)

        # Onda senoidal usando draw.lines (lista de puntos continuos)
        puntos_onda = []
        for x in range(680, 850, 4):
            y = 260 + math.sin((x * 0.05) + angulo_animacion * 3) * 25
            puntos_onda.append((x, y))
        pygame.draw.lines(pantalla, ROJO_NEON, False, puntos_onda, 3)

        # -------------------------------------------------------------
        # 5. SUPERFICIE CON CANAL ALFA (TRANSPARENCIA)
        # -------------------------------------------------------------
        # Para transparencias reales en Pygame se crea una Surface con SRCALPHA
        superficie_transparente = pygame.Surface((380, 150), pygame.SRCALPHA)
        # Color RGBA con valor alfa (ejemplo: 120 de 255)
        superficie_transparente.fill((56, 178, 172, 120))
        
        # Dibujar un círculo interior totalmente opaco dentro de la capa transparente
        pygame.draw.circle(superficie_transparente, (255, 255, 255, 200), (70, 75), 40)
        
        # Posición de la superficie transparente superpuesta sobre otros elementos
        pos_superficie = (50, 440)
        # Dibujamos un fondo de referencia debajo para notar la transparencia
        pygame.draw.rect(pantalla, (255, 100, 100), (30, 460, 420, 40))
        pantalla.blit(superficie_transparente, pos_superficie)
        pygame.draw.rect(pantalla, BLANCO, (*pos_superficie, 380, 150), width=1)

        # -------------------------------------------------------------
        # ETIQUETAS EXPLICATIVAS
        # -------------------------------------------------------------
        etiquetas = [
            ("Rectángulos (fill & border)", (50, 320)),
            ("Círculos y Elipses", (270, 410)),
            ("Polígonos y Estrellas", (460, 330)),
            ("Líneas y Ondas", (710, 310)),
            ("Superficie Alpha Transparente (SRCALPHA)", (50, 600)),
        ]
        for texto, pos in etiquetas:
            lbl = fuente_etiqueta.render(texto, True, GRIS_TEXTO)
            pantalla.blit(lbl, pos)

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main()
