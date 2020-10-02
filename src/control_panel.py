from game_states import GameStates


def get_keys(key_mod, game_state, player, ):
    arrow_keys = []
    text_keys = []
    
    items = player.game_map.get_items_at_location(player.x, player.y)
    port = (player.x, player.y) == player.parent.game_map.port
    
    if game_state == GameStates.ACTION:
        if key_mod == "command":  # sails, etc.
            if player.sails:
                if player.sails.raised:
                    arrow_keys.append({'rotation': 0, 'text': 'Trim Sails'})
                elif player.sails.hp > 0:
                    arrow_keys.append({'rotation': 0, 'text': 'Raise Sails'})
            arrow_keys.append({'rotation': 90, 'text': 'Cargo Config'})
            arrow_keys.append({'rotation': 270, 'text': 'Crew Config'})
            arrow_keys.append({'rotation': 180, 'text': 'Weapon Config'})
        elif not port:
            if key_mod == "shift":
                arrow_keys = [{'rotation': 0, 'text': 'Shoot Arrows'},
                              {'rotation': 90, 'text': 'Port Guns'},
                              {'rotation': 270, 'text': 'Starboard Guns'},
                              {'rotation': 180, 'text': 'Drop Mines'}]
            elif key_mod == "option":  # inventory / other?
                pass
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
                # text_keys.append({'name': 'Opt', 'text': 'Special'})
                text_keys.append({'name': 'Esc', 'text': 'Exit'})
        
        else:  # Player is in port
            if key_mod == "shift":
                arrow_keys = [{'rotation': 0, 'text': 'Repair Sails'},
                              {'rotation': 90, 'text': 'Repair Hull'},
                              {'rotation': 270, 'text': 'Hire Crew'},
                              {'rotation': 180, 'text': 'Fix Weapons'}]
            elif key_mod == "command":
                if player.sails.raised:
                    arrow_keys.append({'rotation': 0, 'text': 'Trim Sails'})
                elif player.sails.hp > 0:
                    arrow_keys.append({'rotation': 0, 'text': 'Raise Sails'})
            elif key_mod == "option":
                pass
            else:
                arrow_keys = [{'rotation': 0, 'text': 'Row'},
                              {'rotation': 90, 'text': 'Turn Port'},
                              {'rotation': 270, 'text': 'Turn Starboard'},
                              {'rotation': 180, 'text': 'Wait'}]
                text_keys.append({'name': 'Shift', 'text': 'Repair Actions'})
                if player.sails:
                    text_keys.append({'name': 'Cmd', 'text': 'Ship Actions'})
                text_keys.append({'name': 'Opt', 'text': 'Port Actions'})
                text_keys.append({'name': 'Esc', 'text': 'Exit'})
    elif game_state == GameStates.WEAPON_CONFIG:
        if key_mod == "command":
            arrow_keys = [{'rotation': 90, 'text': 'Cargo Config'},
                          {'rotation': 270, 'text': 'Crew Config'},
                          {'rotation': 180, 'text': 'Exit Config'}]
        elif key_mod == "shift":
            arrow_keys = [{'rotation': 0, 'text': 'Weapon Up'},
                          {'rotation': 90, 'text': 'Weapon Right'},
                          {'rotation': 270, 'text': 'Weapon Left'},
                          {'rotation': 180, 'text': 'Weapon Down'}]
        else:
            arrow_keys = [{'rotation': 0, 'text': 'Move Up'},
                          {'rotation': 90, 'text': 'Move Right'},
                          {'rotation': 270, 'text': 'Move Left'},
                          {'rotation': 180, 'text': 'Move Down'}]
            text_keys = [{'name': 'Shift', 'text': 'Select Weapon'}]
    elif game_state == GameStates.CREW_CONFIG:
        if key_mod == "command":
            arrow_keys = [{'rotation': 90, 'text': 'Cargo Config'},
                          {'rotation': 270, 'text': 'Exit Config'},
                          {'rotation': 180, 'text': 'Weapon Config'}]
        elif key_mod == "shift":
            arrow_keys = [{'rotation': 0, 'text': 'Set Crew Up'},
                          {'rotation': 90, 'text': 'Set Crew Right'},
                          {'rotation': 270, 'text': 'Set Crew Left'},
                          {'rotation': 180, 'text': 'Set Crew Down'}]
        else:
            arrow_keys = [{'rotation': 0, 'text': 'Move Up'},
                          {'rotation': 90, 'text': 'Move Right'},
                          {'rotation': 270, 'text': 'Move Left'},
                          {'rotation': 180, 'text': 'Move Down'}]
            text_keys = [{'name': 'Shift', 'text': 'Select Crewman'}]
    elif game_state == GameStates.CARGO_CONFIG:
        if key_mod == "command":
            arrow_keys = [{'rotation': 90, 'text': 'Exit Config'},
                          {'rotation': 270, 'text': 'Crew Config'},
                          {'rotation': 180, 'text': 'Weapon Config'}]
        else:
            arrow_keys = [{'rotation': 0, 'text': 'Move Up'},
                          {'rotation': 90, 'text': 'Move Right'},
                          {'rotation': 270, 'text': 'Move Left'},
                          {'rotation': 180, 'text': 'Move Down'}]
    elif game_state == GameStates.PLAYER_DEAD:
        text_keys = [{'name': 'Esc', 'text': 'Exit'}]
    return arrow_keys, text_keys
