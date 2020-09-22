from enum import auto, Enum
from math import floor

import pygame.transform as transform
from pygame import Surface, draw, BLEND_RGBA_MULT, BLEND_RGBA_ADD

from constants import colors, view_port, margin, game_font, images, tile_size
from ui import DisplayInfo
from utilities import direction_angle


class RenderOrder(Enum):
    CORPSE = auto()
    FLOATER = auto()
    SWIMMER = auto()
    PLAYER = auto()
    FLYER = auto()


def get_rotated_image(image: Surface, facing: int) -> Surface:
    return rot_center(image, direction_angle[facing])


def rot_center(image: Surface, angle: int) -> Surface:
    """
    Rotate an image while keeping its center and size - counter clockwise rotation converted to clockwise
    :param image: Surface icon
    :param angle: how much to rotate image
    :return: rotated icon as a Surface
    """
    orig_rect = image.get_rect()
    rot_image = transform.rotate(image, 360 - angle)  # 360 converts to clockwise
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def render_hp_bar(text: str,
                  current: int,
                  maximum: int,
                  bar_width: int,
                  font_color: str = "bar_text",
                  top_color: str = "bar_filled",
                  bottom_color: str = "bar_empty") -> Surface:
    """
    Renders a visual meter
    :param text: name of the values to render
    :param font_color: text color to render
    :param current: current value
    :param maximum: maximum value
    :param top_color: brighter top color of bar
    :param bottom_color: darker background color of bar
    :param bar_width: width of the bar surface
    :return: Surface to render
    """
    max_bar = Surface((bar_width, game_font.get_height()))
    max_bar.fill(colors[bottom_color])
    if maximum > 0:
        current_bar_length = floor(float(current / maximum * bar_width))
        if current_bar_length < 0:
            current_bar_length = 0
        current_bar = Surface((current_bar_length, game_font.get_height()))
        current_bar.fill(colors[top_color])
        max_bar.blit(current_bar, (0, 0))
    bar_text = game_font.render(f"{text}:", True, colors[font_color])
    bar_nums = game_font.render(f"{current}/{maximum}", True, colors[font_color])
    max_bar.blit(bar_text, (1, 1))
    max_bar.blit(bar_nums, (max_bar.get_width() - bar_nums.get_width(), 1))
    
    return max_bar


def render_simple_bar(current: int,
                      maximum: int,
                      bar_width: int,
                      top_color: str = "bar_filled",
                      bottom_color: str = "bar_empty") -> Surface:
    """
    Renders a visual meter
    :param current: current value
    :param maximum: maximum value
    :param top_color: brighter top color of bar
    :param bottom_color: darker background color of bar
    :param bar_width: width of the bar surface
    :return: Surface to render
    """
    max_bar = Surface((bar_width, game_font.get_height()))
    max_bar.fill(colors[bottom_color])
    if maximum > 0:
        current_bar_length = floor(float(current / maximum * bar_width))
        if current_bar_length < 0:
            current_bar_length = 0
        current_bar = Surface((current_bar_length, game_font.get_height()))
        current_bar.fill(colors[top_color])
        max_bar.blit(current_bar, (0, 0))
    
    return max_bar


def render_entity_info(console, game_map, player, mouse_x, mouse_y, ui):
    coord_x, coord_y = game_map.surface_to_map_coords(mouse_x, mouse_y, player.x)
    trans_x = coord_x + player.x - view_port
    trans_y = coord_y + player.y - view_port
    # print(f"{coord_x}:{coord_y} -> {trans_x}:{trans_y}")
    entities = game_map.get_targets_at_location(trans_x,
                                                trans_y,
                                                living_targets=False)
    if player in entities:
        entities.remove(player)
    
    visible_entities = []
    for entity in entities:
        if (entity.x, entity.y) in player.view.fov:
            visible_entities.append(entity)
    
    entities_sorted_for_rendering = sorted(
        visible_entities, key=lambda i: i.render_order.value, reverse=True
    )
    
    widths = []
    entity_list = []
    for entity in entities_sorted_for_rendering:
        name = game_font.render(f"{entity.name}", True, colors["white"])
        widths.append(name.get_width())
        if entity.fighter:
            entity_list.append((name, entity.fighter.hp, entity.fighter.max_hp))
        else:
            entity_list.append((name, None, None))
    if game_map.in_bounds(trans_x, trans_y) and game_map.terrain[trans_x][trans_y].explored:
        if game_map.terrain[trans_x][trans_y].mist and (trans_x, trans_y) in player.view.fov:
            name = game_font.render(f"Mist", True, colors["white"])
            widths.append(name.get_width())
            entity_list.append((name, None, None))
        if game_map.terrain[trans_x][trans_y].decoration:
            name = game_font.render(f"{game_map.terrain[trans_x][trans_y].decoration.capitalize()}",
                                    True, colors["white"])
            widths.append(name.get_width())
            entity_list.append((name, None, None))
        name = game_font.render(f"{game_map.terrain[trans_x][trans_y].elevation.name.lower().capitalize()}",
                                True, colors["white"])
        entity_list.append((name, None, None))
        widths.append(name.get_width())
    
    # print(f"{coord_x}:{coord_y} -> {trans_x}:{trans_y} ({entity.x}:{entity.y})")
    if len(entity_list) > 0:
        info_surf = Surface((max(widths) + margin * 2,
                             (len(entities) - 1) * 2 + len(entity_list) * game_font.get_height() + margin * 2))
        render_border(info_surf, game_map.engine.time.get_sky_color)
        height = 0
        for name, hp, max_hp in entity_list:
            if hp is not None and hp > 0:
                info_surf.blit(render_simple_bar(hp, max_hp, max(widths)),
                               (margin, margin + height * game_font.get_height() + 2 * height))
            info_surf.blit(name, (margin, margin + height * game_font.get_height() + 2 * height))
            height += 1
        
        blit_x = mouse_x + ui.mini_width + margin * 2
        if blit_x + info_surf.get_width() > ui.mini_width + ui.viewport_width:
            blit_x = ui.mini_width + ui.viewport_width - info_surf.get_width() - margin
        blit_y = mouse_y + margin * 2
        if blit_y > ui.viewport_height:
            blit_y = ui.viewport_height - info_surf.get_height() - margin
        
        console.blit(info_surf, (blit_x, blit_y))


def status_panel_render(console: Surface, entity, weather, time, ui_layout: DisplayInfo):
    status_panel = Surface((ui_layout.status_width, ui_layout.status_height))
    render_border(status_panel, time.get_sky_color)
    
    render_weather(time, weather, status_panel, ui_layout)
    vertical = render_wind(weather.wind_direction, status_panel, ui_layout) + 2 * margin

    w_text = game_font.render(f"{weather.conditions.name.lower().capitalize()}", True, colors['mountain'])
    t_text = game_font.render(f"{time.year}.{time.month}.{time.day} {time.hrs}:{time.mins}:00",
                              True, colors['mountain'])
    status_panel.blit(w_text, (margin, vertical))
    status_panel.blit(t_text, (status_panel.get_width() - t_text.get_width() - margin, vertical))
    vertical += game_font.get_height() + margin
    
    health_bar = render_hp_bar(text=f"{entity.fighter.name.capitalize()}",
                               current=entity.fighter.hp,
                               maximum=entity.fighter.max_hp,
                               bar_width=status_panel.get_width() - margin * 2)
    status_panel.blit(health_bar, (margin, vertical))
    vertical += health_bar.get_height() + margin // 2
    if entity.sails:
        sail_bar = render_hp_bar(text=f"{entity.sails.name.capitalize()}",
                                 current=entity.sails.hp,
                                 maximum=entity.sails.max_hp,
                                 bar_width=status_panel.get_width() - margin * 2,
                                 font_color="bar_text" if entity.sails.raised else "black",
                                 top_color="bar_filled" if entity.sails.raised else "impossible")
        status_panel.blit(sail_bar, (margin, vertical))
        vertical += sail_bar.get_height() + margin // 2
    if entity.crew:
        crew_bar = render_hp_bar(text=f"{entity.crew.name.capitalize()}",
                                 current=entity.crew.count,
                                 maximum=entity.crew.max_count,
                                 bar_width=status_panel.get_width() - margin * 2)
        status_panel.blit(crew_bar, (margin, vertical))
        vertical += crew_bar.get_height() + margin // 2

    console.blit(status_panel, (0, ui_layout.mini_height))
    # TODO render weapons damage/cool-downs, and cargo


def control_panel_render(console: Surface, status, player, ui_layout: DisplayInfo, sky):
    control_panel = Surface((ui_layout.control_width, ui_layout.control_height))
    arrow_keys = []
    text_keys = []
    
    if status == "shift":  # targeting
        arrow_keys = [{'rotation': 0, 'text': 'Shoot Arrows'},
                      {'rotation': 90, 'text': 'Port Guns'},
                      {'rotation': 270, 'text': 'Starboard Guns'},
                      {'rotation': 180, 'text': 'Drop Mines'}]
        # modify space_keys['text'] for other options (get items, visit port, etc.)
    elif status == "control_command":  # sails, etc.
        arrow_keys = [{'rotation': 0, 'text': 'Raise Sails'},
                      {'rotation': 180, 'text': 'Lower Sails'}]
    elif status == "alt_option":  # inventory / other?
        pass
    elif player.is_alive:  # standard actions
        arrow_keys = [{'rotation': 0, 'text': 'Row'},
                      {'rotation': 90, 'text': 'Turn Port'},
                      {'rotation': 270, 'text': 'Turn Starboard'}]
        if player.sails:
            text_keys.append({'name': 'Cmd', 'text': 'Sails'})
            if player.sails.raised:
                arrow_keys.append({'rotation': 180, 'text': 'Coast'})
            else:
                arrow_keys.append({'rotation': 180, 'text': 'Wait'})
        # text_keys.append({'name': 'Opt', 'text': 'Special'})
        space_keys = {'name': 'Space', 'text': 'Auto Action'}
        # modify space_keys['text'] for other options (get items, visit port, etc.)
        text_keys.append(space_keys)
        text_keys.append({'name': 'Esc', 'text': 'Exit'})
    else:
        text_keys.append({'name': 'Esc', 'text': 'Exit'})
    
    split = ui_layout.control_width // 4 + margin * 4
    vertical = margin * 2
    spacer = 3
    if arrow_keys:
        for key in arrow_keys:
            vertical = make_arrow_button(panel=control_panel,
                                         split=split,
                                         spacer=spacer,
                                         rotation=key['rotation'],
                                         text=key['text'],
                                         icon=images['arrow_key'],
                                         font=game_font,
                                         color=colors['mountain'],
                                         vertical=vertical)
    if text_keys:
        for key in text_keys:
            vertical = make_text_button(panel=control_panel,
                                        split=split,
                                        spacer=spacer,
                                        name=key['name'],
                                        text=key['text'],
                                        font=game_font,
                                        color=colors['mountain'],
                                        bkg_color=colors['black'],
                                        vertical=vertical)
    render_border(control_panel, sky)
    console.blit(control_panel, (0, ui_layout.mini_height + ui_layout.status_height))


def make_arrow_button(panel, split, spacer, rotation, text, icon, font, color, vertical):
    """
    Creates and renders an arrow button and description in control panel
    :param panel: Surface to render on
    :param split: vertical line - render button on one side, text on the other
    :param spacer: spacing between font heights
    :param rotation: degrees to rotate icon
    :param text: str action corresponding to the arrow button
    :param icon: arrow icon
    :param font: Font for rendering name
    :param color: color of the text to render
    :param vertical: int y value to render at
    :return: current vertical value
    """
    panel.blit(rot_center(image=icon, angle=rotation),
               (split - spacer - icon.get_width(), vertical))
    panel.blit(font.render(text, True, color),
               (split + spacer, vertical + 1))
    vertical += font.get_height() + spacer
    return vertical


def make_text_button(panel, split, spacer, name, text, font, color, bkg_color, vertical):
    """
    Creates and renders the key button and description in control panel
    :param panel: Surface to render on
    :param split: vertical line - render button on one side, text on the other
    :param spacer: spacing between font heights
    :param name: str name of the key
    :param text: str action corresponding to the text button
    :param font: Font for rendering name and key
    :param color: color of the text to render
    :param bkg_color: background color (for reversing the colors of the key name)
    :param vertical: int y value to render at
    :return: current vertical value
    """
    key_text = font.render(name, True, bkg_color)
    w, h = font.size(name)
    key_surf = Surface((w + 3, h))
    key_surf.fill(color)
    key_surf.blit(key_text, (1, 1))
    panel.blit(key_surf, (split - spacer - key_surf.get_width(), vertical))
    panel.blit(font.render(text, True, color),
               (split + spacer, vertical + 1))
    vertical += font.get_height() + spacer
    return vertical


def render_border(panel, color):
    """
    Draws a border around the edge of the given panel
    :param panel: Surface to draw on
    :param color: color of the border
    :return: None
    """
    draw.lines(panel, colors['black'], True,
               ((2, 2),
                (panel.get_width() - 3, 2),
                (panel.get_width() - 3, panel.get_height() - 3),
                (2, panel.get_height() - 3)), 5)  # Black band 5 wide
    draw.lines(panel, color, True,
               ((2, 2),
                (panel.get_width() - 3, 2),
                (panel.get_width() - 3, panel.get_height() - 3),
                (2, panel.get_height() - 3)), 1)  # White line 1 wide


def render_wind(direction: int, display_surf: Surface, ui: DisplayInfo) -> int:
    """
    Render the wind information
    :param direction: direction the wind is blowing
    :param display_surf: Surface to render on
    :param ui: display info
    :return: None
    """
    compass = images['compass']
    display_surf.blit(compass, (ui.status_width - compass.get_width() - 3 * margin, margin * 2))
    if direction is not None:
        display_surf.blit(rot_center(image=images['pointer'], angle=direction_angle[direction]),
                                    (ui.status_width - compass.get_width() - 3 * margin, margin * 2))
    return compass.get_height() + margin


def render_weather(time, weather, display_surf: Surface, ui: DisplayInfo):
    """
    Render the weather information
    :param time: current game Time
    :param weather: current map Weather
    :param display_surf: Surface to render on
    :param ui: display information
    :return: None
    """
    weather_dict = weather.get_weather_info
    time_dict = time.get_time_of_day_info
    
    if 6 <= time.hrs < 18:
        icon = images['sun']
    else:
        icon = images['moon']
    
    numeric_time = 100 * time.hrs + 100 * time.mins // 60  # Example: 6:45 = 675, 21:30 = 2150
    if numeric_time < 600:
        relative_time = 600 + numeric_time
    elif 600 <= numeric_time < 1800:
        relative_time = numeric_time - 600
    else:  # numeric_time >= 1800:
        relative_time = numeric_time - 1800
    
    icon_x = relative_time * (tile_size * 4) // 1200
    
    if relative_time <= 300:
        icon_y = tile_size - icon_x
    elif relative_time >= 900:
        icon_y = icon_x - (tile_size * 3)
    else:
        icon_y = 0
    
    # print(numeric_time, relative_time, icon_x, icon_y)
    sky_surf = Surface((4 * tile_size, tile_size))
    sky_surf.fill(time.get_sky_color)
    sky_surf.blit(icon, (icon_x - 8, icon_y))
    
    if not (600 <= numeric_time < 1800):
        moon_shadow_icon = images['moon_shadow']
        moon_shadow_icon = colorize(image=moon_shadow_icon, new_color=time.get_sky_color)
        
        if numeric_time >= 1800:  # account for day change in middle of night
            offset = 0
        else:
            offset = 1
        sky_surf.blit(moon_shadow_icon, (icon_x - abs(time.day - 15 - offset) - 8, icon_y))
    
    icon = images[weather_dict['name'].lower()]
    for x in range(sky_surf.get_width() // icon.get_width()):
        sky_surf.blit(icon, (x * icon.get_width(), (x + 1) % 2))

    display_surf.blit(sky_surf, (margin * 3, 2 * margin))


def colorize(image, new_color):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    :param image: Surface to create a colorized copy of
    :param new_color: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    image = image.copy()
    
    # zero out RGB values
    image.fill((0, 0, 0, 255), None, BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(new_color[0:3] + (0,), None, BLEND_RGBA_ADD)
    
    return image


