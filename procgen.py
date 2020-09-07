from __future__ import annotations
import random
from typing import Tuple, List, Iterator, TYPE_CHECKING
import entity_factories
from game_map import GameMap
import tcod
import tile_types

if TYPE_CHECKING:
    from engine import Engine


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        
    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        
        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as 2d array index"""
        return slice(self.x1 +1, self.x2), slice(self.y1 +1, self.y2)


    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom"""
        return (self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1)


def place_entities(
    room: RectangularRoom, dive_site: GameMap, maximum_creatures: int,
) -> None:
    number_of_creatures = random.randint(0, maximum_creatures)

    for i in range(number_of_creatures):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dive_site.entities):
            if random.random() < 0.8:
                entity_factories.fish.spawn(dive_site, x, y)
            else:
                entity_factories.shark.spawn(dive_site, x, y)

                       

def tunnel_between(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    """Return L-shaped tunnel between 2 points"""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5: #50% chance
        # move horizontally, then vertically
        corner_x, corner_y = x2, y1
    else:
        # move vertically, then horizontally
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y
    


def generate_dive_site(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    engine: Engine,
    max_creatures_per_cave: int,
    ) -> GameMap:

    """
    Generate random dive site
    """
    player = engine.player
    dive_site = GameMap(engine, map_width, map_height, entities=[player])
    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dive_site.width - room_width - 1)
        y = random.randint(0, dive_site.height - room_height - 1)

        # RectangularRoom
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue #This room intersects, so go to next attempt
        #If no intersections, then room is valid

        # Dig out this room's inner area
        dive_site.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # The first room, starting area is center of room
            player.place(*new_room.center, dive_site)
        else: # all other rooms
            # Dig out a tunnel between this room and previous one
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dive_site.tiles[x, y] = tile_types.floor

        place_entities(new_room, dive_site, max_creatures_per_cave)

        # Finally, append the new room to the list
        rooms.append(new_room)

    return dive_site
