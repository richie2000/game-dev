from components.ai import HostileEnemy
from components.fighter import Fighter
from entity import Actor

player = Actor(
    char="@", 
    color=(255,255,255), 
    name="Player", 
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, defense=2, power=5),
)

fish = Actor(
    char="F", 
    color=(63,127,63), 
    name="Fish", 
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=3),
)

shark = Actor(
    char="S", 
    color=(0,127,0), 
    name="Shark", 
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defense=1, power=4),
)

#boat = Entity(char="<==>", color=(255,255,255), name="Boat", blocks_movement=True)
#ocean_surface = Entity(char="~", color=(255,255,255), name="Ocean Surface", blocks_movement=False)

