"""
=============================================================================
GESTOR DE AUDIO Y EFECTOS PROCEDURALES: GEOMETRY DASH
=============================================================================
Este módulo genera todos los efectos de sonido y la música rítmica de fondo
en memoria de forma 100% matemática y procedural.
No requiere descargar ni enlazar archivos externos .mp3 o .wav.
"""

import math
import struct
import io
import wave
import pygame

class AudioManager:
    """Manejador central de efectos sonoros y música sintética."""
    def __init__(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.pre_init(44100, -16, 2, 512)
                pygame.mixer.init()
            pygame.mixer.set_num_channels(12)
            self.disponible = True
        except Exception:
            self.disponible = False
            return

        # Generar efectos sonoros procedurales
        self.sfx_salto = self._crear_sonido("salto", 0.14, 300)
        self.sfx_orb = self._crear_sonido("orb", 0.20, 650)
        self.sfx_pad = self._crear_sonido("pad", 0.24, 420)
        self.sfx_muerte = self._crear_sonido("muerte", 0.38)
        self.sfx_victoria = self._crear_sonido("victoria", 0.60, 520)

        # Generar música electrónica en bucle
        self.musica_fondo = self._generar_musica_ritmica()
        self.canal_musica = pygame.mixer.Channel(0)
        self.canal_musica.set_volume(0.55)

    def _crear_sonido(self, tipo, duracion, frecuencia=440.0):
        if not self.disponible:
            return None

        samplerate = 44100
        num_muestras = int(samplerate * duracion)
        buffer = io.BytesIO()

        with wave.open(buffer, 'w') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(samplerate)
            datos = bytearray()

            for i in range(num_muestras):
                t = i / samplerate
                p = i / num_muestras

                if tipo == "salto":
                    f = frecuencia + (600.0 * p)
                    amp = (1.0 - p) * 0.55
                    s = math.sin(2.0 * math.pi * f * t)
                elif tipo == "orb":
                    f = frecuencia * (1.0 + 0.5 * math.sin(p * math.pi))
                    amp = (1.0 - p) * 0.6
                    s = math.sin(2.0 * math.pi * f * t) + 0.3 * math.sin(4.0 * math.pi * f * t)
                elif tipo == "pad":
                    f = frecuencia + (900.0 * (p ** 0.5))
                    amp = (1.0 - p) * 0.65
                    s = 1.0 if math.sin(2.0 * math.pi * f * t) > 0 else -1.0
                elif tipo == "muerte":
                    amp = (1.0 - p) * 0.8
                    ruido = ((i * 1103515245 + 12345) & 0x7FFFFFFF) / 0x7FFFFFFF * 2.0 - 1.0
                    s = ruido
                elif tipo == "victoria":
                    # Arpegio ascendente triple
                    segmento = int(p * 3)
                    factor = [1.0, 1.25, 1.5][min(2, segmento)]
                    f = frecuencia * factor
                    amp = (1.0 - p) * 0.6
                    s = math.sin(2.0 * math.pi * f * t)
                else:
                    amp = 0.5
                    s = math.sin(2.0 * math.pi * frecuencia * t)

                val = int(max(-1.0, min(1.0, s * amp)) * 32767)
                datos.extend(struct.pack('<h', val))

            wav.writeframes(datos)

        buffer.seek(0)
        return pygame.mixer.Sound(buffer)

    def _generar_musica_ritmica(self):
        """Genera un loop de música electrónica estilo chiptune techno."""
        if not self.disponible:
            return None

        samplerate = 44100
        bpm = 135
        beat_duracion = 60.0 / bpm
        duracion_total = beat_duracion * 16  # 16 beats = 4 compases
        num_muestras = int(samplerate * duracion_total)

        buffer = io.BytesIO()
        with wave.open(buffer, 'w') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(samplerate)
            datos = bytearray()

            notas_bajo = [110.0, 110.0, 130.81, 146.83, 110.0, 98.0, 130.81, 123.47]

            for i in range(num_muestras):
                t = i / samplerate
                beat_actual = t / beat_duracion
                beat_frac = beat_actual - int(beat_actual)

                # 1. Bombo rítmico (Kick) en cada beat
                kick_env = max(0.0, 1.0 - (beat_frac * 3.5))
                kick_freq = 150.0 * (1.0 - beat_frac * 0.8)
                kick = math.sin(2.0 * math.pi * max(35.0, kick_freq) * beat_frac) * kick_env * 0.45

                # 2. Platillo (Hi-hat) a contratiempo (cada 0.5 beat)
                medio_beat_frac = (beat_actual * 2.0) % 1.0
                hat_env = max(0.0, 1.0 - (medio_beat_frac * 8.0))
                ruido = (((i * 1664525 + 1013904223) & 0x7FFFFFFF) / 0x7FFFFFFF * 2.0 - 1.0)
                hat = ruido * hat_env * 0.15

                # 3. Línea de bajo sintetizado
                indice_nota = int(beat_actual * 2) % len(notas_bajo)
                f_bajo = notas_bajo[indice_nota]
                sub_beat_frac = (beat_actual * 2.0) % 1.0
                bajo_env = max(0.0, 1.0 - (sub_beat_frac * 1.5))
                # Onda de sierra suave
                fase = (f_bajo * t) % 1.0
                bajo = (2.0 * fase - 1.0) * bajo_env * 0.28

                muestra_final = kick + hat + bajo
                val = int(max(-1.0, min(1.0, muestra_final)) * 32767)
                datos.extend(struct.pack('<h', val))

            wav.writeframes(datos)

        buffer.seek(0)
        return pygame.mixer.Sound(buffer)

    def reproducir_musica(self):
        if self.disponible and self.musica_fondo and not self.canal_musica.get_busy():
            self.canal_musica.play(self.musica_fondo, loops=-1)

    def pausar_musica(self):
        if self.disponible and self.canal_musica.get_busy():
            self.canal_musica.pause()

    def reanudar_musica(self):
        if self.disponible:
            if not self.canal_musica.get_busy():
                self.canal_musica.play(self.musica_fondo, loops=-1)
            else:
                self.canal_musica.unpause()

    def detener_musica(self):
        if self.disponible and self.canal_musica.get_busy():
            self.canal_musica.stop()

    def play_salto(self):
        if self.disponible and self.sfx_salto:
            self.sfx_salto.play()

    def play_orb(self):
        if self.disponible and self.sfx_orb:
            self.sfx_orb.play()

    def play_pad(self):
        if self.disponible and self.sfx_pad:
            self.sfx_pad.play()

    def play_muerte(self):
        if self.disponible and self.sfx_muerte:
            self.sfx_muerte.play()

    def play_victoria(self):
        if self.disponible and self.sfx_victoria:
            self.sfx_victoria.play()
