import sys
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import numpy as np
import pygame
import math
from pygame.locals import *

matplotlib.use("Agg")



class Univers:
    def __init__(self, name, step, dim, scale):
        self.name = name
        self.step = step
        self.scale = scale
        self.dim = dim
        self.width, self.height = dim
        self.pop = []
        self.sources = []
        self.generators = []
        self.t = 0
        self.fps = 60
        self.clock = pygame.time.Clock()
        pygame.init()
        self.screen = pygame.display.set_mode(self.dim)
        pygame.display.set_caption(self.name)
    
    def addGenerateurs(self, *new_generators):
        for generator in new_generators:
            self.generators.append(generator)

    def addAgent(self, *agents):
        for agent in agents:
            self.pop.append(agent)
    
    def addSource(self, *generators):
        for source in generators:
            self.sources.append(source)
    
    def simule(self):
        for p in self.pop:
            for s in self.sources:
                s.apply(p, self.t)
            p.simule(self.step)
            new_pos = p.pos
            p.update_pos(new_pos)
        self.t += self.step
    
    def simuleAll(self, time):
        n = int(time/self.step)
        for i in range(n):
            self.simule()


####################################################
    def plot3D(self, plot):
        print(self.pop)
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
        for p in self.pop: 
            ax.scatter([pos[0] for pos in p.pos], [pos[1] for pos in p.pos], [
                pos[2] for pos in p.pos], color=p.color, label=p.name, s=2)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        
        ax.legend(loc='upper left')


        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.buffer_rgba()

        # convert the plot buffer to a Pygame surface
        size = canvas.get_width_height()
        surf = pygame.image.frombuffer(raw_data, size, "RGBA")
        # plt.show()

        return surf


    def plot2D(self, plot):
        # set up matplotlib
        # print(self.pos)
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
        for p in self.pop: 
            ax.scatter([pos[0] for pos in p.pos], [pos[1] for pos in p.pos], color=p.color, label=p.name, s=2)
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


    def gameDraw(self, screen=pygame.display.set_mode((800, 600))):
        screen.fill((0, 0, 0))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # generate new positions for particles

            self.simuleAll(0.01)
          

            surf = self.plot2D(plt)

            # blit the plot to the screen
            screen.blit(surf, (0, 0))

            pygame.display.update()
            plt.close()

####################################################
            
    def gameInit(self):
        self.gameRunning = True

# classes generateurs nested parce que en a besoin des particules! 
    class ForceAttractive   :
        def __init__(self, position, strength=1000, *particles, univers):
            self.position = position
            self.strength = strength
            self.particles = particles
            self.univers = univers

        def apply(self, particles, t):

            if not self.particles:
                self.particles = self.univers.pop
            for particle in self.particles:
                if particle.active:
                    distance = math.sqrt((particle.pos[-1][0] - self.position[0])**2 +
                                         (particle.pos[-1][1] - self.position[1])**2 +
                                         (particle.pos[-1][2] - self.position[2])**2)
                    direction = [(self.position[0] - particle.pos[-1][0]) / distance,
                                 (self.position[1] - particle.pos[-1][1]) / distance,
                                 (self.position[2] - particle.pos[-1][2]) / distance]
                    force = [self.strength * direction[i] for i in range(3)]
                    
                    particle.addForce(force)


    class ForceConst:
        def __init__(self, value, *particles):
            self.value = value
            self.particles = particles
            self.active = True

            if not self.particles:
                particles = self.pops
            else:
                particles = self.particles

        def apply(self, t):
            for particle in self.particles:
                if particle.active:
                    particle.addForce(self.value)

    class ForceHarmonic:
        def __init__(self, value, pulsation, *particles):
            self.value = value
            self.pulsation = pulsation
            self.particles = particles
            self.active = True
        def apply(self, t):
            if not self.active:
                return
            for particle in self.particles:
                force = self.value * math.cos(self.pulsation * t)
                particle.addForce(force)

    class Viscosity:
        def __init__(self, coef, *particles):
            self.coef = coef
            self.particles = particles
            self.active = True
            
        def apply(self, particle, t):
            if not self.active:
                return
            v = particle.vit[-1]
            f_damp = -self.coef * v
            particle.addForce(f_damp)

    class ForceField:
        def __init__(self, pos, amplitude, *particles):
            self.pos = pos[-1]
            self.amplitude = amplitude
            self.particles = particles
            self.active = True

        def apply(self, particle, t):
            if not self.active:
                return
            delta_pos = [particle.pos[-1][i] - self.pos[i] for i in range(len(particle.pos[-1]))]
            force = self.amplitude * delta_pos[-1]
            particle.addForce(force)

    class SpringDumper:
        def __init__(self, stiffness, dumping, length, particule1, particule2):
            self.stiffness = stiffness
            self.dumping = dumping
            self.length = length
            self.particule1 = particule1
            self.particule2 = particule2
            self.active = True

        def apply(self, t):
            if not self.active:
                return

            # Calculate the vector between the two particles
            delta_pos[-1] = self.particule2.pos[-1] - self.particule1.pos[-1]

            # Calculate the length of the vector
            delta_length = np.linalg.norm(delta_pos[-1])

            # Calculate the spring force using Hooke's law
            spring_force = -self.stiffness * (delta_length - self.length) * (delta_pos[-1] / delta_length)

            # Calculate the damping force
            delta_vel = self.particule2.vit - self.particule1.vit
            damping_force = -self.dumping * np.dot(delta_vel, delta_pos[-1] / delta_length) * (delta_pos[-1] / delta_length)

            # Apply the forces to the particles
            self.particule1.addForce(spring_force + damping_force)
            self.particule2.addForce(-(spring_force + damping_force))

    class Rod:
        def __init__(self, particule1, particule2):
            dx = particule2.pos[-1][0] - particule1.pos[-1][0]
            dy = particule2.pos[-1][1] - particule1.pos[-1][1]
            dz = particule2.pos[-1][2] - particule1.pos[-1][2]
            self.length = math.sqrt(dx**2 + dy**2 + dz**2)
            self.stiffness = (particule1.masse * particule2.masse) / (particule1.masse + particule2.masse)
            self.dumping = 0
            self.particule1 = particule1
            self.particule2 = particule2
            self.active = True
        
        def apply(self, t):
            if not self.active:
                return
            delta_pos = [self.particule2.pos[-1][i] - self.particule1.pos[-1][i] for i in range(len(self.particule1.pos[-1]))]
            dist = math.sqrt(delta_pos[0]**2 + delta_pos[1]**2 + delta_pos[2]**2)
            delta_vel = [self.particule2.vit[i] - self.particule1.vit[i] for i in range(len(self.particule1.vit))]
            spring_force = self.stiffness * (dist - self.length)
            damping_force = self.dumping * (delta_vel[0]*delta_pos[0] + delta_vel[1]*delta_pos[1] + delta_vel[2]*delta_pos[2]) / dist
            total_force = (spring_force + damping_force) * np.array(delta_pos) / dist
            self.particule1.addForce(total_force)
            self.particule2.addForce(-total_force)




    class PrismJoint:
        def __init__(self, axis, particule):
            self.axis = axis
            self.particule = particule
            self.active = True

        def apply(self, particle, t):
            if not self.active:
                return
            p1 = self.particule.pos
            p2 = particle.pos
            delta_pos = [p2[i] - p1[i] for i in range(len(p1))]
            delta_dot = [particle.vit[i] for i in self.axis]
            delta = math.sqrt(sum([delta_pos[i]**2 for i in self.axis]))
            dist = delta - self.particule.rayon
            n = [delta_pos[i] / delta for i in self.axis]
            force = [dist*n[i]*self.particule.elasticite for i in self.axis]
            damp = [self.particule.damping * delta_dot[i] for i in self.axis]
            f_damp = [damp[i] * n[i] for i in self.axis]
            particle.addForce(force)
            particle.addForce(f_damp)


    class ConstantVelocitySource:
        def __init__(self, vit):
            self.vit = vit
            
        def apply(self, particle, time):
            particle.vit = self.vit
