import pygame
import random

# Définition des constantes
WIDTH = 1000
HEIGHT = 700
FPS = 60
g = 9.81
viscosity = 0.1

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Classe de particule
class Particle:
    def __init__(self, x, y, vx, vy, m):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.m = m

    def update(self, dt):
        # Calcul des forces
        fx = 0
        fy = self.m * g - self.m * viscosity * self.vy
        
        # Mise à jour de la vitesse et de la position
        self.vx += fx / self.m * dt
        self.vy += fy / self.m * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 10)

# Liste de particules
particles = []

# Boucle principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Création d'une particule aléatoire
                x = random.uniform(0, WIDTH)
                y = random.uniform(0, HEIGHT)
                vx = random.uniform(-10, 10)
                vy = random.uniform(-10, 10)
                m = random.uniform(1, 10)
                p = Particle(x, y, vx, vy, m)
                particles.append(p)

    # Effacement de l'écran
    screen.fill((0, 0, 0))

    # Mise à jour et dessin des particules
    for p in particles:
        p.update(1/FPS)
        p.draw()

    # Affichage
    pygame.display.flip()
    clock.tick(FPS)

# Fermeture de Pygame
pygame.quit()
