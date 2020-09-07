#!/usr/bin/env python3
import copy
import tcod
import color

from engine import Engine
import entity_factories
from procgen import generate_dive_site


def main() -> None:
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 43
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    max_creatures_per_cave = 2
    
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    #Create starting locations for player and npc
    #ocean_surface = copy.deepcopy(entity_factories.ocean_surface)
    #boat = copy.deepcopy(entity_factories.boat)
    player = copy.deepcopy(entity_factories.player)
    engine = Engine(player=player)

    engine.game_map = generate_dive_site(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_creatures_per_cave=max_creatures_per_cave,
        engine=engine,
    )

    engine.update_fov()
    
    engine.message_log.add_message(
        "Hello and welcome. Happy diving", color.welcome_text
    )
    
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Fathom",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            
            #Ocean surface
            #for i in range(0,screen_width):
                #root_console.print(x=i, y=5, string="~", fg=(0,255,0))
            
            engine.render(console=root_console, context=context)
            engine.event_handler.handle_events()


if __name__ == "__main__":
    main()
