"""
=============================================================================
EJEMPLO 08: Sistema de Audio, Efectos Sonoros (SFX) y Síntesis Procedural
=============================================================================
Este script muestra el manejo del módulo `pygame.mixer`:
1. Inicialización adecuada de audio (`pygame.mixer.init`).
2. Creación de efectos de sonido procedurales en tiempo real sin requerir archivos
   externos (utilizando el módulo nativo `wave` y matemáticas para generar ondas de audio).
3. Reproducción en canales independientes (`pygame.mixer.Channel`).
4. Control de volumen dinámico y bucle de audio.
"""

import sys
import math
import struct
import io
import wave
import pygame

def generar_sonido_wav(tipo="salto", duracion=0.15, frecuencia=440.0):
    """
    Genera un archivo WAV en memoria usando exclusivamente librerías estándar
    de Python (wave, struct, math) para que funcione en cualquier equipo.
    """
    samplerate = 44100
    num_muestras = int(samplerate * duracion)
    buffer = io.BytesIO()

    with wave.open(buffer, 'w') as wav_file:
        wav_file.setnchannels(1)       # Mono
        wav_file.setsampwidth(2)       # 16 bits
        wav_file.setframerate(samplerate)

        datos = bytearray()
        for i in range(num_muestras):
            t = i / samplerate
            progreso = i / num_muestras

            if tipo == "salto":
                # Frecuencia ascendente (chirp agudo típico de salto en juegos de plataformas)
                f_actual = frecuencia + (800.0 * progreso)
                amplitud = (1.0 - progreso) * 0.6
                muestra = math.sin(2.0 * math.pi * f_actual * t)

            elif tipo == "moneda":
                # Arpegio rápido de 2 tonos
                f_actual = frecuencia if progreso < 0.5 else frecuencia * 1.5
                amplitud = 0.5 * (1.0 - progreso)
                muestra = math.sin(2.0 * math.pi * f_actual * t)

            elif tipo == "explosion":
                # Ruido pseudoaleatorio con caída de volumen
                amplitud = (1.0 - progreso) * 0.7
                # Algoritmo de congruencia lineal para generar ruido blanco sin módulos pesados
                ruido = ((i * 1103515245 + 12345) & 0x7FFFFFFF) / 0x7FFFFFFF * 2.0 - 1.0
                muestra = ruido

            elif tipo == "laser":
                # Frecuencia descendente rápida
                f_actual = max(80.0, frecuencia * (1.0 - progreso * 0.8))
                amplitud = (1.0 - progreso) * 0.6
                muestra = 1.0 if math.sin(2.0 * math.pi * f_actual * t) > 0 else -1.0  # Onda cuadrada retro

            else:
                muestra = math.sin(2.0 * math.pi * frecuencia * t) * 0.5

            valor_entero = int(max(-1.0, min(1.0, muestra * amplitud)) * 32767)
            datos.extend(struct.pack('<h', valor_entero))

        wav_file.writeframes(datos)

    buffer.seek(0)
    return pygame.mixer.Sound(buffer)


def main():
    # Inicializar Pygame y Mixer con baja latencia
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("08 - Audio y Efectos Sonoros Procedurales (pygame.mixer)")

    reloj = pygame.time.Clock()
    fuente_titulo = pygame.font.SysFont("Arial", 22, bold=True)
    fuente_info = pygame.font.SysFont("Arial", 16)
    fuente_tecla = pygame.font.SysFont("Consolas", 18, bold=True)

    # Generar efectos sonoros procedurales
    sfx_salto = generar_sonido_wav(tipo="salto", duracion=0.18, frecuencia=320)
    sfx_moneda = generar_sonido_wav(tipo="moneda", duracion=0.22, frecuencia=587)
    sfx_explosion = generar_sonido_wav(tipo="explosion", duracion=0.35)
    sfx_laser = generar_sonido_wav(tipo="laser", duracion=0.15, frecuencia=900)

    # Variables de retroalimentación visual
    ultimo_sonido = "Ninguno"
    tiempo_efecto_visual = 0
    volumen_global = 0.8

    pygame.mixer.set_num_channels(8)

    while True:
        dt = reloj.tick(60)
        if tiempo_efecto_visual > 0:
            tiempo_efecto_visual = max(0, tiempo_efecto_visual - dt)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1 or evento.key == pygame.K_SPACE:
                    sfx_salto.set_volume(volumen_global)
                    sfx_salto.play()
                    ultimo_sonido = "Salto Plataformero (Pitch ascendente)"
                    tiempo_efecto_visual = 200

                elif evento.key == pygame.K_2:
                    sfx_moneda.set_volume(volumen_global)
                    sfx_moneda.play()
                    ultimo_sonido = "Moneda / Pick-up (Arpegio doble)"
                    tiempo_efecto_visual = 200

                elif evento.key == pygame.K_3:
                    sfx_explosion.set_volume(volumen_global)
                    sfx_explosion.play()
                    ultimo_sonido = "Explosión / Impacto (Ruido blanco)"
                    tiempo_efecto_visual = 200

                elif evento.key == pygame.K_4:
                    sfx_laser.set_volume(volumen_global)
                    sfx_laser.play()
                    ultimo_sonido = "Disparo Láser (Onda cuadrada)"
                    tiempo_efecto_visual = 200

                elif evento.key == pygame.K_PLUS or evento.key == pygame.K_KP_PLUS:
                    volumen_global = min(1.0, volumen_global + 0.1)

                elif evento.key == pygame.K_MINUS or evento.key == pygame.K_KP_MINUS:
                    volumen_global = max(0.0, volumen_global - 0.1)

        # Renderizado
        pantalla.fill((15, 23, 42))

        # Título
        titulo = fuente_titulo.render("Demostración de Audio con pygame.mixer", True, (255, 255, 255))
        pantalla.blit(titulo, (50, 40))

        # Tarjetas de sonidos
        teclas_sfx = [
            ("[1] o [ESPACIO]", "Efecto de Salto", (56, 189, 248)),
            ("[2]", "Efecto de Moneda / Gema", (250, 204, 21)),
            ("[3]", "Efecto de Explosión", (239, 68, 68)),
            ("[4]", "Disparo Láser Retro", (168, 85, 247)),
        ]

        for i, (tecla, descripcion, color) in enumerate(teclas_sfx):
            y_base = 120 + i * 85
            rect_tarjeta = pygame.Rect(50, y_base, 500, 68)
            pygame.draw.rect(pantalla, (30, 41, 59), rect_tarjeta, border_radius=10)
            pygame.draw.rect(pantalla, color, rect_tarjeta, width=2, border_radius=10)

            txt_t = fuente_tecla.render(tecla, True, color)
            txt_d = fuente_info.render(descripcion, True, (241, 245, 249))
            pantalla.blit(txt_t, (70, y_base + 22))
            pantalla.blit(txt_d, (240, y_base + 24))

        # Panel de Estado y Volumen
        panel_estado = pygame.Rect(580, 120, 180, 320)
        pygame.draw.rect(pantalla, (24, 30, 43), panel_estado, border_radius=10)
        
        lbl_vol = fuente_info.render(f"Volumen: {int(volumen_global * 100)}%", True, (226, 232, 240))
        pantalla.blit(lbl_vol, (600, 140))
        lbl_cambio = fuente_info.render("[+] / [-] Modificar", True, (148, 163, 184))
        pantalla.blit(lbl_cambio, (600, 165))

        # Barra visual de volumen
        pygame.draw.rect(pantalla, (15, 23, 42), (600, 200, 140, 20), border_radius=4)
        pygame.draw.rect(pantalla, (34, 197, 94), (600, 200, int(140 * volumen_global), 20), border_radius=4)

        # Indicador visual reactivo a la pulsación
        if tiempo_efecto_visual > 0:
            pygame.draw.circle(pantalla, (34, 197, 94), (670, 280), 30)
            lbl_rep = fuente_info.render("¡SONANDO!", True, (255, 255, 255))
            pantalla.blit(lbl_rep, (635, 320))

        # Último sonido reproducido
        txt_ultimo = fuente_info.render(f"Último SFX disparado: {ultimo_sonido}", True, (56, 189, 248))
        pantalla.blit(txt_ultimo, (50, ALTO - 60))

        pygame.display.flip()

if __name__ == "__main__":
    main()
