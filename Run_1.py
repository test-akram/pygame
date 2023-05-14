from univers import Univers
from particule import Particule
import random

g = 9.81  # accélération due à la gravité
scene_width = 10  # largeur de la scène en mètres
scene_height = 7  # hauteur de la scène en mètres

# Création de 10 particules aléatoires
particules = []
for i in range(10):
    # Positions aléatoires dans la scène
    x = random.uniform(-scene_width/2, scene_width/2)
    y = random.uniform(-scene_height/2, scene_height/2)
    z = random.uniform(0, 10)
    pos0 = (x, y, z)
    
    # Masses aléatoires entre 1 et 10 kg
    masse = random.uniform(1, 10)
    
    # Vitesse initiale nulle
    vit0 = (0, 0, 0)
    
    # Création de la particule
    p = Particule(masse, pos0, vit0, name=f'particule{i}', color='blue')
    particules.append(p)

univers = Univers(name='univers_question_1', dim=(scene_width, scene_height), scale=10, step=0.00001)

# Ajout des particules à l'univers
for p in particules:
	univers.addAgent(p)

# Ajout de force attractive
force_attractive = univers.ForceAttractive(position=(scene_width/2, scene_height/2, -5), univers=univers)

univers.addSource(force_attractive)

univers.gameDraw()
