import pygame
import random
import math

class BalaEnemiga(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion_vector, tipo="recta"):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 100), (5, 5), 5) # Proyectil rosa neón original
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.vel = direccion_vector * 4
        self.reflejada = False
        self.tipo = tipo
        self.tiempo = 0 # Usado para calcular la onda del disparo curvo

    def update(self):
        # Si es una bala de Alien y no ha sido reflejada, oscila en su trayectoria
        if not self.reflejada and self.tipo == "curva":
            self.tiempo += 0.1
            # Crear un vector perpendicular para distorsionar la trayectoria recta
            perpendicular = pygame.math.Vector2(-self.vel.y, self.vel.x).normalize()
            movimiento_final = self.vel + perpendicular * math.sin(self.tiempo) * 2.5
            self.pos += movimiento_final
        else:
            # Movimiento lineal estándar para balas normales o reflejadas
            self.pos += self.vel
            
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        
        # Auto-destrucción fuera de los márgenes para liberar memoria
        if self.rect.x < -50 or self.rect.x > 850 or self.rect.y < -50 or self.rect.y > 650:
            self.kill()


class Momia(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (200, 200, 150), (0, 0, 32, 32)) # Cuadrado ocre/momia
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.cooldown_disparo = random.randint(60, 120)

    def update(self, jugador_pos, grupo_balas, todos_los_sprites):
        # Persecución lenta y constante
        dir_jugador = (jugador_pos - self.pos)
        if dir_jugador.length() > 0:
            dir_jugador.normalize_ip()
        
        self.pos += dir_jugador * 0.8
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # Cadencia de fuego
        self.cooldown_disparo -= 1
        if self.cooldown_disparo <= 0:
            self.cooldown_disparo = 90
            # Se inyecta en ambos grupos para actualizar lógica Y dibujar en pantalla
            bala = BalaEnemiga(self.pos.x, self.pos.y, dir_jugador, "recta")
            grupo_balas.add(bala)
            todos_los_sprites.add(bala)


class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (50, 200, 80), (0, 0, 28, 28)) # Verde zombie radioactivo
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)

    def update(self, jugador_pos, grupo_balas, todos_los_sprites):
        # El zombie no dispara, su única arma es interceptarte rápido (Cuerpo a cuerpo)
        dir_jugador = (jugador_pos - self.pos)
        if dir_jugador.length() > 0:
            dir_jugador.normalize_ip()
        
        self.pos += dir_jugador * 2.2 # Velocidad agresiva de horda
        self.rect.center = (int(self.pos.x), int(self.pos.y))


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (240, 50, 240), (15, 15), 15) # Alienígena magenta
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.cooldown_disparo = random.randint(80, 150)

    def update(self, jugador_pos, grupo_balas, todos_los_sprites):
        dir_jugador = (jugador_pos - self.pos)
        distancia = dir_jugador.length()
        
        if dir_jugador.length() > 0:
            dir_jugador.normalize_ip()
            
        # IA de mantener distancia: Se acerca si estás lejos, huye si estás encima
        if distancia > 250:
            self.pos += dir_jugador * 1.2
        elif distancia < 150:
            self.pos -= dir_jugador * 1.5
            
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # Disparo con ráfaga curva/sinusoidal
        self.cooldown_disparo -= 1
        if self.cooldown_disparo <= 0:
            self.cooldown_disparo = 110
            bala = BalaEnemiga(self.pos.x, self.pos.y, dir_jugador, "curva")
            grupo_balas.add(bala)
            todos_los_sprites.add(bala)