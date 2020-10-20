from __future__ import annotations

from typing import TYPE_CHECKING

from constants.enums import Location, GameStates, KeyMod, MenuKeys
from utilities import get_cone_target_hexes_at_location

if TYPE_CHECKING:
    from entity import Entity


def get_keys(key_mod: KeyMod, game_state: GameStates, player: Entity):
    arrow_keys = []
    text_keys = []
    
    items = player.game_map.get_items_at_location(player.x, player.y)
    port = (player.x, player.y) == player.parent.game_map.port.location
    
    if game_state == GameStates.ACTION:
        if key_mod == KeyMod.COMMAND:  # sails, etc.
            if player.sails:
                if player.sails.raised:
                    arrow_keys.append({'rotation': 0, 'text': 'Trim Sails'})
                elif player.sails.hp > 0:
                    arrow_keys.append({'rotation': 0, 'text': 'Raise Sails'})
            arrow_keys.append({'rotation': 90, 'text': 'Cargo Config'})
            arrow_keys.append({'rotation': 270, 'text': 'Crew Config'})
            arrow_keys.append({'rotation': 180, 'text': 'Weapon Config'})
        
        elif not port:
            # TODO logic below mirrors rendering targeting hexes and attacking... combine this somehow?
            if key_mod == KeyMod.SHIFT:
                ammo = {'arrows': len(player.crew.roster) // 4}
                enough_ammo = True
                for ammo_type in ammo.keys():
                    if ammo_type not in player.cargo.manifest.keys():
                        enough_ammo = False
                    elif player.cargo.manifest[ammo_type] - ammo[ammo_type] < 0:
                        enough_ammo = False
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
                
                if enough_ammo and enough_targets:
                    arrow_keys.append({'rotation': 0, 'text': 'Shoot Arrows'})
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
                            hexes = get_cone_target_hexes_at_location(player.x,
                                                                      player.y,
                                                                      player.facing,
                                                                      side,
                                                                      distance)
                            for x, y in hexes:
                                if (x, y) in player.view.fov:
                                    targets.extend(player.game_map.get_targets_at_location(x, y))
                            if player in targets:
                                targets.remove(player)
                            if len(targets) < 1:
                                enough_targets = False
                            if enough_targets:
                                if side == Location.STARBOARD:
                                    arrow_keys.append({'rotation': 90, 'text': 'Starboard Guns'})
                                else:
                                    arrow_keys.append({'rotation': 270, 'text': 'Port Guns'})
                if player.cargo.item_type_in_manifest("mines"):
                    arrow_keys.append({'rotation': 180, 'text': 'Drop Mines'})
            elif key_mod == KeyMod.OPTION:  # crew actions
                up = [crewman for crewman in player.crew.roster if crewman.assignment == MenuKeys.UP]
                right = [crewman for crewman in player.crew.roster if crewman.assignment == MenuKeys.RIGHT]
                left = [crewman for crewman in player.crew.roster if crewman.assignment == MenuKeys.LEFT]
                down = [crewman for crewman in player.crew.roster if crewman.assignment == MenuKeys.DOWN]
                
                if len(up) > 0:
                    cooldown = f" ({up[0].cooldown})" if up[0].cooldown > 0 else " (ok)"
                    arrow_keys.append({'rotation': 0, 'text': f"{up[0].occupation.capitalize()} {cooldown}"})
                if len(right) > 0:
                    cooldown = f" ({right[0].cooldown})" if right[0].cooldown > 0 else " (ok)"
                    arrow_keys.append({'rotation': 90, 'text': f"{right[0].occupation.capitalize()} {cooldown}"})
                if len(left) > 0:
                    cooldown = f" ({left[0].cooldown})" if left[0].cooldown > 0 else " (ok)"
                    arrow_keys.append({'rotation': 270, 'text': f"{left[0].occupation.capitalize()} {cooldown}"})
                if len(down) > 0:
                    cooldown = f" ({down[0].cooldown})" if down[0].cooldown > 0 else " (ok)"
                    arrow_keys.append({'rotation': 180, 'text': f"{down[0].occupation.capitalize()} {cooldown}"})
            
            elif player.is_alive:  # standard actions
                arrow_keys = [{'rotation': 0, 'text': 'Row'},
                              {'rotation': 90, 'text': 'Turn Port'},
                              {'rotation': 270, 'text': 'Turn Starboard'}]
                text_keys.append({'name': 'Shift', 'text': 'Targeting'})
                
                down_text = 'Wait'
                if player.sails:
                    text_keys.append({'name': 'Cmd', 'text': 'Ship Actions'})
                    if player.sails.raised:
                        down_text = 'Coast'
                if len(items) > 0:
                    down_text = 'Salvage'
                arrow_keys.append({'rotation': 180, 'text': down_text})
                
                assignments = [crewman.assignment for crewman in player.crew.roster
                               if crewman.assignment is not None]
                if len(assignments) > 0:
                    text_keys.append({'name': 'Opt', 'text': 'Crew Actions'})
                text_keys.append({'name': 'Esc', 'text': 'Main Menu'})
        
        else:  # Player is in port
            if key_mod == KeyMod.SHIFT:
                arrow_keys = [{'rotation': 0, 'text': 'Repair Sails    (15)'},
                              {'rotation': 90, 'text': 'Repair Hull    (20)'},
                              # {'rotation': 270, 'text': 'Hire Crew'},
                              {'rotation': 180, 'text': 'Fix Weapons  (25)'}]
            elif key_mod == KeyMod.COMMAND:
                if player.sails.raised:
                    arrow_keys.append({'rotation': 0, 'text': 'Trim Sails'})
                elif player.sails.hp > 0:
                    arrow_keys.append({'rotation': 0, 'text': 'Raise Sails'})
            elif key_mod == KeyMod.OPTION:
                arrow_keys = [{'rotation': 0, 'text': 'Shipyard'},
                              {'rotation': 90, 'text': 'Merchant'},
                              {'rotation': 270, 'text': 'Tavern'},
                              {'rotation': 180, 'text': 'Smithy'}]
            else:
                down_text = 'Wait'
                if len(items) > 0:
                    down_text = 'Salvage'
                arrow_keys = [{'rotation': 0, 'text': 'Row'},
                              {'rotation': 90, 'text': 'Turn Port'},
                              {'rotation': 270, 'text': 'Turn Starboard'},
                              {'rotation': 180, 'text': down_text}]
                
                text_keys.append({'name': 'Shift', 'text': 'Repair Actions'})
                if player.sails:
                    text_keys.append({'name': 'Cmd', 'text': 'Ship Actions'})
                text_keys.append({'name': 'Opt', 'text': 'Port Actions'})
                text_keys.append({'name': 'Esc', 'text': 'Main Menu'})
    
    elif game_state == GameStates.WEAPON_CONFIG:
        if key_mod == KeyMod.COMMAND:
            arrow_keys = [{'rotation': 90, 'text': 'Cargo Config'},
                          {'rotation': 270, 'text': 'Crew Config'},
                          {'rotation': 180, 'text': 'Exit Config'}]
        elif key_mod == KeyMod.SHIFT:
            selected = player.broadsides.selected
            location, weapon = player.broadsides.all_weapons[selected]
            arrow_keys.append({'rotation': 0, 'text': 'Move Up'})
            if player.is_alive:
                if location == Location.PORT:
                    arrow_keys.append({'rotation': 270, 'text': 'Remove'})
                elif location == Location.STARBOARD:
                    arrow_keys.append({'rotation': 90, 'text': 'Remove'})
                else:
                    if len(player.broadsides.starboard) < player.broadsides.slot_count:
                        arrow_keys.append({'rotation': 90, 'text': 'Assign Starboard'})
                    if len(player.broadsides.port) < player.broadsides.slot_count:
                        arrow_keys.append({'rotation': 270, 'text': 'Assign Port'})
            arrow_keys.append({'rotation': 180, 'text': 'Move Down'})
        else:
            arrow_keys = [{'rotation': 0, 'text': 'Move Up'},
                          {'rotation': 180, 'text': 'Move Down'}]
            if player.is_alive:
                text_keys = [{'name': 'Shift', 'text': 'Assign Weapon'}]
            text_keys.extend([{'name': 'Cmd', 'text': 'Config Menu'},
                              {'name': 'Esc', 'text': 'Exit Config'}])
    
    elif game_state == GameStates.CREW_CONFIG:
        if key_mod == KeyMod.COMMAND:
            arrow_keys = [{'rotation': 90, 'text': 'Cargo Config'},
                          {'rotation': 270, 'text': 'Exit Config'},
                          {'rotation': 180, 'text': 'Weapon Config'}]
        elif key_mod == KeyMod.SHIFT and player.is_alive:
            arrow_keys = [{'rotation': 0, 'text': 'Assign Crew Up'},
                          {'rotation': 90, 'text': 'Assign Crew Right'},
                          {'rotation': 270, 'text': 'Assign Crew Left'},
                          {'rotation': 180, 'text': 'Assign Crew Down'}]
        else:
            arrow_keys = [{'rotation': 0, 'text': 'Move Up'},
                          {'rotation': 180, 'text': 'Move Down'}]
            if player.is_alive:
                text_keys = [{'name': 'Shift', 'text': 'Assign Crewman'}]
            text_keys.extend([{'name': 'Cmd', 'text': 'Config Menu'},
                              {'name': 'Esc', 'text': 'Exit Config'}])
    
    elif game_state == GameStates.CARGO_CONFIG:
        if key_mod == KeyMod.SHIFT and player.is_alive:
            arrow_keys = [{'rotation': 90, 'text': 'Confirm'},
                          {'rotation': 270, 'text': 'Cancel'}]
        elif key_mod == KeyMod.COMMAND:
            arrow_keys = [{'rotation': 90, 'text': 'Exit Config'},
                          {'rotation': 270, 'text': 'Crew Config'},
                          {'rotation': 180, 'text': 'Weapon Config'}]
        else:
            arrow_keys = [{'rotation': 0, 'text': 'Move Up'},
                          {'rotation': 90, 'text': 'Decrease Drop'},
                          {'rotation': 270, 'text': 'Increase Drop'},
                          {'rotation': 180, 'text': 'Move Down'}]
            if player.is_alive:
                text_keys = [{'name': 'Shift', 'text': 'Finished'}]
            text_keys.extend([{'name': 'Cmd', 'text': 'Config Menu'},
                              {'name': 'Esc', 'text': 'Exit Config'}])
    
    elif game_state == GameStates.MERCHANT:
        if key_mod == KeyMod.SHIFT:
            arrow_keys = [{'rotation': 90, 'text': 'Confirm'},
                          {'rotation': 270, 'text': 'Cancel'}]
        else:
            arrow_keys = [{'rotation': 0, 'text': 'Move Up'},
                          {'rotation': 90, 'text': 'Sell'},
                          {'rotation': 270, 'text': 'Buy'},
                          {'rotation': 180, 'text': 'Move Down'}]
            text_keys = [{'name': 'Shift', 'text': 'Finished'},
                         {'name': 'Esc', 'text': 'Exit'}]
    
    elif game_state == GameStates.SMITHY:
        if key_mod == KeyMod.SHIFT:
            arrow_keys = [{'rotation': 90, 'text': 'Confirm'},
                          {'rotation': 270, 'text': 'Cancel'}]
        else:
            weapon_list = []
            for weapon in player.broadsides.storage:
                weapon_list.append(weapon)
            for weapon in player.game_map.port.smithy.manifest:
                weapon_list.append(weapon)
            selected = player.broadsides.selected
            if len(weapon_list) > 1:
                arrow_keys = [{'rotation': 0, 'text': 'Move Up'}]
                if weapon_list[selected] in player.broadsides.sell_list:
                    arrow_keys.append({'rotation': 270, 'text': 'Return'})
                elif weapon_list[selected] in player.broadsides.storage:
                    arrow_keys.append({'rotation': 90, 'text': 'Sell'})
                elif weapon_list[selected] in player.game_map.port.smithy.manifest:
                    arrow_keys.append({'rotation': 270, 'text': 'Buy'})
                elif weapon_list[selected] in player.broadsides.buy_list:
                    arrow_keys.append({'rotation': 90, 'text': 'Return'})
                arrow_keys.append({'rotation': 180, 'text': 'Move Down'})
            text_keys = [{'name': 'Shift', 'text': 'Finished'},
                         {'name': 'Esc', 'text': 'Exit'}]
    
    elif game_state == GameStates.TAVERN:
        if key_mod == KeyMod.SHIFT:
            arrow_keys = [{'rotation': 90, 'text': 'Confirm'},
                          {'rotation': 270, 'text': 'Cancel'}]
        else:
            full_roster = []
            for crewman in player.crew.roster:
                full_roster.append(crewman)
            for crewman in player.game_map.port.tavern.roster:
                full_roster.append(crewman)
            
            arrow_keys = [{'rotation': 0, 'text': 'Move Up'}]
            if full_roster[player.crew.selected] in player.crew.hire_list:
                arrow_keys.append({'rotation': 90, 'text': 'To Tavern'})
            elif full_roster[player.crew.selected] in player.crew.release_list:
                arrow_keys.append({'rotation': 270, 'text': 'To Crew'})
            elif full_roster[player.crew.selected] in player.game_map.port.tavern.roster:
                arrow_keys.append({'rotation': 270, 'text': 'To Crew'})
            elif full_roster[player.crew.selected] in player.crew.roster:
                arrow_keys.append({'rotation': 90, 'text': 'To Tavern'})
            arrow_keys.append({'rotation': 180, 'text': 'Move Down'})
            text_keys = [{'name': 'Shift', 'text': 'Finished'},
                         {'name': 'Esc', 'text': 'Exit'}]
    
    elif game_state == GameStates.PLAYER_DEAD:
        if key_mod == KeyMod.COMMAND:
            arrow_keys = [{'rotation': 90, 'text': 'Cargo Config'},
                          {'rotation': 270, 'text': 'Crew Config'},
                          {'rotation': 180, 'text': 'Weapon Config'}]
        else:
            text_keys = [{'name': 'Cmd', 'text': 'Config Actions'},
                         {'name': 'Esc', 'text': 'Main Menu'}]
    
    return arrow_keys, text_keys
