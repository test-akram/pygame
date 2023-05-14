import pygame
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Pendulum properties
pendulums = [
    {"length": 10, "theta": math.pi / 4, "theta_vel": 0, "theta_acc": 0},
    {"length": 20, "theta": math.pi / 4, "theta_vel": 0, "theta_acc": 0},
    {"length": 30, "theta": math.pi / 4, "theta_vel": 0, "theta_acc": 0},
]
GRAVITY = 9.81
MASS = 1.0
TIME_STEP = 0.01

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Function to update pendulum properties
def update_pendulum(pendulum):
    pendulum["theta_acc"] = - (GRAVITY / pendulum["length"]) * math.sin(pendulum["theta"])
    pendulum["theta_vel"] += pendulum["theta_acc"] * TIME_STEP
    pendulum["theta"] += pendulum["theta_vel"] * TIME_STEP

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Update pendulum properties
    for pendulum in pendulums:
        update_pendulum(pendulum)

    # Clear the screen
    screen.fill(BLACK)

    # Draw the pendulums
    for i, pendulum in enumerate(pendulums):
        x = SCREEN_WIDTH / 2 + pendulum["length"] * math.sin(pendulum["theta"])
        y = SCREEN_HEIGHT / 2 + pendulum["length"] * math.cos(pendulum["theta"])
        pygame.draw.line(screen, WHITE, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (x, y), 2)
        pygame.draw.circle(screen, RED, (int(x), int(y)), 10)
        pygame.draw.circle(screen, WHITE, (int(x), int(y)), 2)
    
    # Refresh display
    pygame.display.flip()

    # Control simulation speed
    clock.tick(1 / TIME_STEP)

# Close pygame
pygame.quit()
