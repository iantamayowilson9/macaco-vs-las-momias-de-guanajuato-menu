import pygame

class Personaje(pygame.sprite.Sprite):
    def __init__(self, velocidad, vida, habilidad):
        super().__init__()
        self.velocidad = velocidad
        self.vida = vida
        self.habilidad = habilidad