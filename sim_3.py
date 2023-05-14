import pygame
import matplotlib.pyplot as plt
import numpy as np

# Paramètres physiques du système
m = 1  # masse
k = 10  # constante de raideur du ressort
c = 1  # coefficient d'amortissement

# Conditions initiales
x0 = 0.5  # position initiale
v0 = 0  # vitesse initiale

# Temps d'échantillonnage pour l'affichage
dt = 0.01

# Création de la fenêtre Pygame
pygame.init()
win_size = (800, 600)
win = pygame.display.set_mode(win_size)

# Initialisation du graphique Matplotlib
fig = plt.figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(111)
ax.set_xlim([0, 10])
ax.set_ylim([-1, 1])
ax.set_xlabel('Temps (s)')
ax.set_ylabel('Position (m)')
line, = ax.plot([], [], lw=2)

# Fonction pour mettre à jour le graphique Matplotlib
def update_plot(t, x):
    line.set_data(t, x)
    plt.draw()

# Fonction pour calculer l'évolution du système
def update_system(x, v, F, dt):
    a = (F(x) - k*x - c*v)/m
    v = v + a*dt
    x = x + v*dt
    return x, v

# Fonction pour calculer la force appliquée
def force(t):
    return np.sin(t)

# Boucle principale
clock = pygame.time.Clock()
t = 0
x = x0
v = v0

# Define constant force
F = 10

# Define harmonic force
omega = 2*np.pi   # Angular frequency
A = 10            # Amplitude
F = lambda t: A*np.sin(omega*t)

while True:
    # Gestion des événements Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                F = lambda x: force(t)
    
    # Mise à jour de l'état du système
    x, v = update_system(x, v, F, dt)
    t += dt
    
    # Mise à jour du graphique Matplotlib
    update_plot(np.linspace(0, t, int(t/dt)), np.linspace(0, x, int(t/dt)))
    plt.pause(0.001)
    fig.canvas.draw()
    
    # Mise à jour de la fenêtre Pygame
    win.fill((255, 255, 255))
    pygame.display.update()
    
    # Limitation de la boucle principale à 60 images par seconde
    clock.tick(60)
