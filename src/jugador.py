import pygame
import math
# EN src/jugador.py
# ANTES: from .base import Personaje
# AHORA:
from src.base import Personaje

class Macaco(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Superficie transparente para el sprite del personaje
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 165, 0), (15, 15), 15) # Naranja chango sonidero
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.vida = 3

    def update(self):
        # Interpolación lineal (Lerp) hacia el mouse para un movimiento fluido y rápido
        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        self.pos += (mouse_pos - self.pos) * 0.15
        self.rect.center = (int(self.pos.x), int(self.pos.y))


class Espada(pygame.sprite.Sprite):
    def __init__(self, jugador):
        super().__init__()
        self.jugador = jugador
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 255, 200), (8, 8), 8) # Cyan/Neón brillante
        self.rect = self.image.get_rect()
        self.radio_orbita = 50

    def update(self):
        # Obtener la dirección desde Macaco hacia el puntero del mouse
        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        vector_direccion = mouse_pos - self.jugador.pos
        
        if vector_direccion.length() > 0:
            vector_direccion.normalize_ip()
        else:
            vector_direccion = pygame.math.Vector2(1, 0)
            
        # Posicionar la espada de manera matemática orbitando en el ángulo del mouse
        pos_espada = self.jugador.pos + (vector_direccion * self.radio_orbita)
        self.rect.center = (int(pos_espada.x), int(pos_espada.y))