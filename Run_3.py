import pygame
import numpy as np

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MASS = 1.0
K = 1.0
B = 0.1
TIME_STEP = 0.01

f=0

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Position, vitesse et accélération initiales
x = SCREEN_WIDTH / 2
v = 0
a = 0

# Fonction pour mettre à jour les variables du système
def update_system(f):
    global x, v, a
    a = (f - B * v - K * x) / MASS
    v += a * TIME_STEP
    x += v * TIME_STEP

# Boucle principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                f = 1.0 # Force constante
            elif event.key == pygame.K_h:
                f = 0.5 * K * SCREEN_HEIGHT * np.sin(2 * np.pi * pygame.time.get_ticks() / 1000.0) # Force harmonique

    # Mise à jour du système
    update_system(f)

    # Effacement de l'écran
    screen.fill(BLACK)

    # Dessin du système
    pygame.draw.line(screen, WHITE, (0, SCREEN_HEIGHT / 2), (SCREEN_WIDTH, SCREEN_HEIGHT / 2), 2)
    pygame.draw.circle(screen, RED, (int(x), int(SCREEN_HEIGHT / 2)), 10)

    # Rafraîchissement de l'affichage
    pygame.display.flip()

    # Contrôle de la vitesse de la simulation
    clock.tick(1 / TIME_STEP)

# Fermeture de Pygame
pygame.quit()
