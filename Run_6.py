import pygame
import numpy as np

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MASS = 1.0
K1 = 1.0
K2 = 1.0
L1 = 10.0
L2 = 10.0
L3 = 10.0
TIME_STEP = 0.01

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Positions, vitesses et accélérations initiales
x1 = SCREEN_WIDTH / 4
x2 = 3 * SCREEN_WIDTH / 4
v1 = 0
v2 = 0
a1 = 0
a2 = 0

# Fonction pour mettre à jour les variables du système
def update_system(f):
    global x1, x2, v1, v2, a1, a2
    a1 = (f - K1 * (x1 - L1) - K2 * (x1 - x2 - L2)) / MASS
    a2 = (-K2 * (x2 - x1 - L2) - K1 * (x2 - L3)) / MASS
    v1 += a1 * TIME_STEP
    v2 += a2 * TIME_STEP
    x1 += v1 * TIME_STEP
    x2 += v2 * TIME_STEP

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

    # Calcul des forces en fonction du temps
    f1 = np.sin(2 * np.pi * 0.5 * pygame.time.get_ticks() / 1000.0)
    f2 = np.sin(2 * np.pi * 1.5 * pygame.time.get_ticks() / 1000.0)

    # Mise à jour du système
    update_system(f1)
    update_system(f2)

    # Effacement de l'écran
    screen.fill(BLACK)

    # Dessin du système
    pygame.draw.line(screen, WHITE, (0, SCREEN_HEIGHT / 2), (SCREEN_WIDTH, SCREEN_HEIGHT / 2), 2)
    pygame.draw.circle(screen, RED, (int(x1), int(SCREEN_HEIGHT / 2)), 10)
    pygame.draw.circle(screen, RED, (int(x2), int(SCREEN_HEIGHT / 2)), 10)

    # Rafraîchissement de l'affichage
    pygame.display.flip()

    # Contrôle de la vitesse de la simulation
    clock.tick(1 / TIME_STEP)

# Fermeture de Pygame
pygame.quit()
