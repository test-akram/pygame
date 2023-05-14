import sys
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import numpy as np
import pygame
from pygame.locals import *


matplotlib.use("Agg")


class Particule:
    def __init__(self, masse, pos0=(0, 0, 0), vit0=(0, 0, 0), name='init', color='white', fix=0):
        self.masse = masse
        self.pos = [pos0]
        self.vit = [vit0]
        self.name = name
        self.color = color
        self.fix = fix
        self.forces_ext = [0, 0, 0]

    def PFD(self, forces_ext, step):
        if not self.fix:
            self.forces_ext = forces_ext  # mettre à jour la somme des forces extérieures
            
            # add gravitational force
            # you can comment this code if you don't want gravity
            g = 9.81 # m/s^2
            F_gravity = [0, 0, -self.masse * g]
            forces_ext = [forces_ext[i] + F_gravity[i] for i in range(3)]
            # till here
        
            ax = forces_ext[0] / self.masse  # calcul de l'accélération selon x
            ay = forces_ext[1] / self.masse  # calcul de l'accélération selon y
            az = forces_ext[2] / self.masse  # calcul de l'accélération selon z

            # calcul de la nouvelle vitesse selon x
            vx = self.vit[-1][0] + ax * step
            # calcul de la nouvelle vitesse selon y
            vy = self.vit[-1][1] + ay * step
            # calcul de la nouvelle vitesse selon z
            vz = self.vit[-1][2] + az * step
            self.vit.append([vx, vy, vz])  # mise à jour de la vitesse
            # calcul de la nouvelle position selon x
            px = self.pos[-1][0] + vx * step
            # calcul de la nouvelle position selon y
            py = self.pos[-1][1] + vy * step
            # calcul de la nouvelle position selon z
            pz = self.pos[-1][2] + vz * step
            # mise à jour de la positiondef getSpeed(self):
            self.pos.append([px, py, pz])

    def simule(self, step):
        self.PFD(self.forces_ext, step)

    def update_pos(self, new_pos):
        self.pos.append(new_pos[-1])

    def setSpeed(self, speed):
        self.vit = speed

    def setForce(self, force):
        self.forces_ext = force

    def addForce(self, force):
        self.forces_ext = [self.forces_ext[i] + force[i] for i in range(3)]

    def setPosition(self, position):
        self.pos = position

    def __repr__(self):
        return f'Particule({self.masse}, {self.pos[-1]}, {self.vit[-1]}, {self.name}, {self.color}, {self.fix})'

    def __str__(self):
        return f'Particule {self.name}: m={self.masse}, pos={self.pos[-1]}, vit={self.vit[-1]}'

    def plot2D(self, plot):
        # set up matplotlib
        plt.rcParams.update({
            "lines.marker": "o",
            "lines.linewidth": "1",
            "axes.prop_cycle": plt.cycler('color', ['white']),
            "text.color": "white",
            "axes.facecolor": "black",
            "axes.edgecolor": "lightgray",
            "axes.labelcolor": "white",
            "axes.grid": "True",
            "grid.linestyle": "--",
            "xtick.color": "white",
            "ytick.color": "white",
            "grid.color": "lightgray",
            "figure.facecolor": "black",
            "figure.edgecolor": "black",
        })

        fig = plt.figure(figsize=[4, 2], dpi=100)
        ax = fig.gca()

        # clear the previous plot
        ax.clear()

        # plot the particules
        ax.scatter([pos[0] for pos in self.pos], [pos[1]
                   for pos in self.pos], color=self.color, label=self.name, s=2)
        # save the plot to a buffer
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.buffer_rgba()

        # convert the plot buffer to a Pygame surface
        size = canvas.get_width_height()
        surf = pygame.image.frombuffer(raw_data, size, "RGBA")
        # plt.show()

        return surf

    def plot3D(self, plot):

        plt.rcParams.update({
            "lines.marker": "o",
            "lines.linewidth": "1",
            "axes.prop_cycle": plt.cycler('color', ['white']),
            "text.color": "white",
            "axes.facecolor": "black",
            "axes.edgecolor": "lightgray",
            "axes.labelcolor": "white",
            "axes.grid": "True",
            "grid.linestyle": "--",
            "xtick.color": "white",
            "ytick.color": "white",
            "grid.color": "lightgray",
            "figure.facecolor": "black",
            "figure.edgecolor": "black",
        })

        # dessiner une figure 3D pour visualiser les trajectoires des particules
        fig = plot.figure()

        ax = fig.add_subplot(111, projection='3d')

        ax.scatter([pos[0] for pos in self.pos], [pos[1] for pos in self.pos], [
            pos[2] for pos in self.pos], color=self.color, label=self.name, s=2)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.legend()

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.buffer_rgba()

        # convert the plot buffer to a Pygame surface
        size = canvas.get_width_height()
        surf = pygame.image.frombuffer(raw_data, size, "RGBA")
        # plt.show()

        return surf

    def gameDraw(self, screen=pygame.display.set_mode((800, 600))):
        screen.fill((0, 0, 0))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # generate new positions for particles

            self.simule(0.1)
            new_pos = self.pos

            # update the positions of the particles

            self.update_pos(new_pos)

            surf = self.plot3D(plt)

            # blit the plot to the screen
            screen.blit(surf, (0, 0))

            pygame.display.update()
            plt.close()


p = Particule(masse=5, pos0=[0, 100, 7], vit0=[
              10, 20, -1], name='p3', color='blue')

# p.gameDraw()
