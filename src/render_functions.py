from enum import auto, Enum
from math import floor

import pygame.transform as transform
from pygame import Surface, draw

from constants import colors, view_port, margin, game_font, images
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
        render_border(info_surf, colors["white"])
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


def status_panel_render(console: Surface, entity, ui_layout: DisplayInfo):
    status_panel = Surface((ui_layout.status_width, ui_layout.status_height))
    render_border(status_panel, colors["white"])
    health_bar = render_hp_bar(text=f"{entity.fighter.name.capitalize()}",
                               current=entity.fighter.hp,
                               maximum=entity.fighter.max_hp,
                               bar_width=status_panel.get_width() - margin * 2)
    status_panel.blit(health_bar, (margin, margin))
    if entity.sails:
        sail_bar = render_hp_bar(text=f"{entity.sails.name.capitalize()}",
                                 current=entity.sails.hp,
                                 maximum=entity.sails.max_hp,
                                 bar_width=status_panel.get_width() - margin * 2,
                                 font_color="bar_text" if entity.sails.raised else "black",
                                 top_color="bar_filled" if entity.sails.raised else "impossible")
        status_panel.blit(sail_bar, (margin, margin + margin // 2 + game_font.get_height()))
    console.blit(status_panel, (0, ui_layout.mini_height))
    if entity.crew:
        crew_bar = render_hp_bar(text=f"{entity.crew.name.capitalize()}",
                                 current=entity.crew.count,
                                 maximum=entity.crew.max_count,
                                 bar_width=status_panel.get_width() - margin * 2)
        status_panel.blit(crew_bar, (margin, margin + 2 * (margin // 2 + game_font.get_height())))
    console.blit(status_panel, (0, ui_layout.mini_height))
    # TODO render weapons damage/cool-downs, and cargo


def control_panel_render(console: Surface, status, player, ui_layout: DisplayInfo):
    control_panel = Surface((ui_layout.control_width, ui_layout.control_height))
    arrow_keys = []
    text_keys = []
    
    if status == "shift":  # targeting
        arrow_keys = [{'rotation': 0, 'text': 'Shoot Arrows'},
                      {'rotation': 180, 'text': 'Shoot Arrows'}]
        space_keys = {'name': 'Space', 'text': 'Drop Mines'}
        # modify space_keys['text'] for other options (get items, visit port, etc.)
        text_keys.append(space_keys)
    elif status == "control_command":  # sails, etc.
        arrow_keys = [{'rotation': 0, 'text': 'Raise Sails'},
                      {'rotation': 180, 'text': 'Lower Sails'}]
    elif status == "alt_option":  # inventory / other?
        pass
    elif player.is_alive:  # standard actions
        arrow_keys = [{'rotation': 0, 'text': 'Row'},
                      {'rotation': 90, 'text': 'Turn Port'},
                      {'rotation': 270, 'text': 'Turn Starboard'}]
        text_keys = [{'name': 'Shift', 'text': 'Targeting'}]
        if player.sails:
            text_keys.append({'name': 'Cmd', 'text': 'Sails'})
        # text_keys.append({'name': 'Opt', 'text': 'Special'})
        space_keys = {'name': 'Space', 'text': 'Wait'}
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
    render_border(control_panel, colors["white"])
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
    draw.lines(panel, (0, 0, 0), True,
               ((2, 2),
                (panel.get_width() - 3, 2),
                (panel.get_width() - 3, panel.get_height() - 3),
                (2, panel.get_height() - 3)), 5)  # Black band 5 wide
    draw.lines(panel, color, True,
               ((2, 2),
                (panel.get_width() - 3, 2),
                (panel.get_width() - 3, panel.get_height() - 3),
                (2, panel.get_height() - 3)), 1)  # White line 1 wide
