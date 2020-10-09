from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import display, Surface

from constants.constants import view_port, tile_size, margin
from constants.enums import GameStates, Location, KeyMod
from constants.images import entity_icons, terrain_icons
from constants.sprites import sprites
from render.utilities import map_to_surface_coords, get_rotated_image, render_border, create_ship_icon
from utilities import get_cone_target_hexes_at_location

if TYPE_CHECKING:
    from camera import Camera
    from game_map import GameMap
    from ui import DisplayInfo
    from weather import Weather


def viewport_render(game_map: GameMap,
                    main_display: display,
                    weather: Weather,
                    ui_layout: DisplayInfo,
                    camera: Camera) -> None:
    player = game_map.engine.player
    overlap = 3
    view_size = 2 * view_port + 1
    view_extra = 2 * view_port + 1 + 2 * overlap
    
    left = player.x - view_port - overlap
    right = left + view_size + 2 * overlap
    
    top = player.y - view_port - overlap
    bottom = top + view_size + 2 * overlap
    
    map_surf = Surface((view_extra * tile_size, view_extra * tile_size))
    
    for x in range(left, right):
        for y in range(top, bottom):
            if game_map.in_bounds(x, y) and game_map.terrain[x][y].explored:
                map_surf.blit(terrain_icons[game_map.terrain[x][y].elevation.name.lower()],
                              map_to_surface_coords(x, y, left, top, overlap, player, camera))
                if game_map.terrain[x][y].decoration:
                    map_surf.blit(terrain_icons[game_map.terrain[x][y].decoration],
                                  map_to_surface_coords(x, y, left, top, overlap, player, camera, entity=True))
                # coord_text = game_font.render(f"{x}:{y}", False, (0, 0, 0))
                # map_surf.blit(coord_text,
                #               ((x - left) * tile_size,
                #                (y - top - 1) * tile_size + (x % 2) * half_tile + half_tile - offset))
    
    for x in range(left, right):
        for y in range(top, bottom):
            if (x, y) not in player.view.fov:
                map_surf.blit(terrain_icons["fog_of_war"],
                              map_to_surface_coords(x, y, left, top, overlap, player, camera))
    
    if game_map.engine.key_mod and game_map.engine.game_state == GameStates.ACTION:
        if game_map.engine.key_mod == KeyMod.SHIFT and not (player.x, player.y) == game_map.port.location:
            target_tiles = []
            ammo = {'arrows': player.crew.count // 4}
            enough_ammo = True
            for ammo_type in ammo.keys():
                if ammo_type not in player.cargo.manifest.keys():
                    enough_ammo = False
                elif player.cargo.manifest[ammo_type] - ammo[ammo_type] < 0:
                    enough_ammo = False
            if enough_ammo:
                enough_targets = True
                targets = []
                neighbor_tiles = player.game_map.get_neighbors_at_elevations(player.x,
                                                                             player.y,
                                                                             elevations='all')
                neighbor_tiles.append((player.x, player.y))
                for tile_x, tile_y in neighbor_tiles:
                    targets.extend(player.game_map.get_targets_at_location(tile_x, tile_y))
                if player in targets:
                    targets.remove(player)
                if len(targets) < 1:
                    enough_targets = False
                
                if enough_targets:
                    target_tiles.extend(neighbor_tiles)
            
            for side in [Location.PORT, Location.STARBOARD]:
                guns_ready = True
                distance = player.broadsides.get_active_range(side)
                if distance is None or distance < 1:
                    guns_ready = False
                if guns_ready:
                    enough_ammo = True
                    ammo = player.broadsides.get_active_weapon_ammo_types(side)
                    for ammo_type in ammo.keys():
                        if ammo_type not in player.cargo.manifest.keys():
                            enough_ammo = False
                        elif player.cargo.manifest[ammo_type] - ammo[ammo_type] < 0:
                            enough_ammo = False
                    if enough_ammo:
                        enough_targets = True
                        targets = []
                        hexes = get_cone_target_hexes_at_location(player.x, player.y, player.facing, side, distance)
                        for x, y in hexes:
                            if (x, y) in player.view.fov:
                                targets.extend(player.game_map.get_targets_at_location(x, y))
                        if player in targets:
                            targets.remove(player)
                        if len(targets) < 1:
                            enough_targets = False
                        if enough_targets:
                            if side == Location.STARBOARD:
                                target_tiles.extend(hexes)
                            else:
                                target_tiles.extend(hexes)
            if player.cargo.item_type_in_manifest("mines"):
                target_tiles.append((player.x, player.y))
            
            for (x, y) in target_tiles:
                if game_map.in_bounds(x, y) and (x, y) in player.view.fov:
                    map_surf.blit(terrain_icons["highlight"],
                                  map_to_surface_coords(x, y, left, top, overlap, player, camera))
    
    entities_sorted_for_rendering = sorted(
        game_map.entities, key=lambda i: i.render_order.value
    )
    
    for entity in entities_sorted_for_rendering:
        if entity.sprite and (entity.x, entity.y) in player.view.fov:
            entity.sprite.update(game_map.engine.clock.get_fps())
            map_surf.blit(get_rotated_image(sprites[entity.sprite.sprite_name][entity.sprite.pointer], entity.facing),
                          map_to_surface_coords(entity.x, entity.y, left, top, overlap, player, camera, entity=True))
        elif (entity.x, entity.y) in player.view.fov \
                and entity.icon is not None \
                and entity.is_alive \
                and entity.fighter and entity.fighter.name == 'hull':
            ship_icon = create_ship_icon(entity)
            map_surf.blit(get_rotated_image(ship_icon, entity.facing),
                          map_to_surface_coords(entity.x, entity.y, left, top, overlap, player, camera, entity=True))
        elif (entity.x, entity.y) in player.view.fov \
                and entity.icon is not None \
                and entity.is_alive:
            map_surf.blit(get_rotated_image(entity_icons[entity.icon], entity.facing),
                          map_to_surface_coords(entity.x, entity.y, left, top,
                                                overlap, player, camera, entity=True))
        elif (entity.x, entity.y) in game_map.engine.player.view.fov \
                and entity.icon is not None:
            map_surf.blit(entity_icons[entity.icon],
                          map_to_surface_coords(entity.x, entity.y, left, top, overlap, player, camera, entity=True))
    
    for x, y in player.view.fov:
        if game_map.in_bounds(x, y) and game_map.terrain[x][y].mist:
            map_surf.blit(terrain_icons["mist"],
                          map_to_surface_coords(x, y, left, top, overlap, player, camera))
    
    if weather.rain:
        weather.rain.render(console=map_surf, conditions=weather.conditions)
    
    game_map.engine.time.tint_render(map_surf)
    view_surf = map_surf.subsurface((0,
                                     player.x % 2 * tile_size // 2),
                                    (ui_layout.viewport_width - 2 * margin,
                                     ui_layout.viewport_height - 2 * margin))
    border_surf = Surface((ui_layout.viewport_width, ui_layout.viewport_height))
    render_border(border_surf, game_map.engine.time.get_sky_color)
    border_surf.blit(view_surf, (margin, margin))
    main_display.blit(border_surf, (ui_layout.mini_width, 0))
