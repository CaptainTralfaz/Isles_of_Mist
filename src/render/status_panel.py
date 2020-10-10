from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Surface

from constants.colors import colors
from constants.constants import game_font, margin, tile_size
from constants.images import cargo_icons, misc_icons
from render.utilities import render_border, render_hp_bar, rot_center, colorize
from utilities import direction_angle

if TYPE_CHECKING:
    from ui import DisplayInfo
    from weather import Weather
    from entity import Entity
    from time_of_day import Time


def status_panel_render(console: Surface,
                        entity: Entity,
                        weather: Weather,
                        time: Time,
                        ui_layout: DisplayInfo) -> None:
    """
    Generates the status panel of player information. Calls weather and wind render functions
    :param console: surface to blit to
    :param entity: the player
    :param weather: the current game Weather
    :param time: the current game Time
    :param ui_layout: layout for where to blit
    :return: None
    """
    status_panel = Surface((ui_layout.status_width, ui_layout.status_height))
    render_border(status_panel, time.get_sky_color)
    
    render_weather(time, weather, status_panel)
    vertical = render_wind(weather.wind_direction, status_panel, ui_layout) + 2 * margin
    
    w_text = game_font.render(f"{weather.conditions.name.lower().capitalize()}", True, colors['mountain'])
    status_panel.blit(w_text, (status_panel.get_width() // 2 - w_text.get_width() // 2, vertical))
    vertical += game_font.get_height() + margin
    
    months = str(time.month) if len(str(time.month)) == 2 else "0" + str(time.month)
    days = str(time.day) if len(str(time.day)) == 2 else "0" + str(time.day)
    hrs = str(time.hrs) if len(str(time.hrs)) == 2 else "0" + str(time.hrs)
    mins = str(time.mins) if len(str(time.mins)) == 2 else "0" + str(time.mins)
    t_text = game_font.render(f"{time.year}.{months}.{days} {hrs}:{mins}:00", True, colors['mountain'])
    status_panel.blit(t_text, (status_panel.get_width() // 2 - t_text.get_width() // 2, vertical))
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
                                 font_color="mountain" if entity.sails.raised else "gray",
                                 top_color="bar_filled" if entity.sails.raised else "dark_green",
                                 bottom_color="bar_empty" if entity.sails.raised else "dark")
        status_panel.blit(sail_bar, (margin, vertical))
        vertical += sail_bar.get_height() + margin // 2
    if entity.crew:
        crew_bar = render_hp_bar(text=f"{entity.crew.name.capitalize()}",
                                 current=entity.crew.count,
                                 maximum=entity.crew.max_count,
                                 bar_width=status_panel.get_width() - margin * 2)
        status_panel.blit(crew_bar, (margin, vertical))
        vertical += crew_bar.get_height()
    vertical += margin
    if entity.broadsides:
        text = game_font.render(f"Broadsides", True, colors['mountain'])
        status_panel.blit(text, ((ui_layout.status_width - text.get_width()) // 2, vertical))
        vertical += game_font.get_height() + margin // 2
        if len(entity.broadsides.port) > 0:
            status_panel.blit(game_font.render(f"Port", True, colors['mountain']), (margin, vertical))
            cd = max([weapon.cooldown for weapon in entity.broadsides.port])
            cd_color = colors['mountain'] if cd == 0 else colors['gray']
            cd_text = game_font.render(f"[{cd}]", True, cd_color)
            status_panel.blit(cd_text, (ui_layout.status_width - margin - cd_text.get_width(), vertical))
            vertical += game_font.get_height() + margin // 2
            for weapon in entity.broadsides.port:
                if weapon.cooldown == 0:
                    weapon_bar = render_hp_bar(text=f"{weapon.name.capitalize()}",
                                               current=weapon.hp,
                                               maximum=weapon.max_hp,
                                               bar_width=status_panel.get_width() - margin * 2)
                else:
                    weapon_bar = render_hp_bar(text=f"{weapon.name.capitalize()}",
                                               current=weapon.hp,
                                               maximum=weapon.max_hp,
                                               bar_width=status_panel.get_width() - margin * 2,
                                               font_color="gray",
                                               top_color="dark_green",
                                               bottom_color="dark")
                status_panel.blit(weapon_bar, (margin, vertical))
                vertical += weapon_bar.get_height() + margin // 2
        vertical += margin
        if len(entity.broadsides.starboard) > 0:
            status_panel.blit(game_font.render(f"Starboard", True, colors['mountain']), (margin, vertical))
            cd = max([weapon.cooldown for weapon in entity.broadsides.starboard])
            cd_color = colors['mountain'] if cd == 0 else colors['gray']
            cd_text = game_font.render(f"[{cd}]", True, cd_color)
            status_panel.blit(cd_text, (ui_layout.status_width - margin - cd_text.get_width(), vertical))
            vertical += game_font.get_height() + margin // 2
            for weapon in entity.broadsides.starboard:
                if weapon.cooldown == 0:
                    weapon_bar = render_hp_bar(text=f"{weapon.name.capitalize()}",
                                               current=weapon.hp,
                                               maximum=weapon.max_hp,
                                               bar_width=status_panel.get_width() - margin * 2)
                else:
                    weapon_bar = render_hp_bar(text=f"{weapon.name.capitalize()}",
                                               current=weapon.hp,
                                               maximum=weapon.max_hp,
                                               bar_width=status_panel.get_width() - margin * 2,
                                               font_color="mountain" if entity.sails.raised else "gray",
                                               top_color="bar_filled" if entity.sails.raised else "dark_green",
                                               bottom_color="bar_empty" if entity.sails.raised else "dark")
                status_panel.blit(weapon_bar, (margin, vertical))
                vertical += weapon_bar.get_height() + margin // 2
    
    if entity.cargo:
        names = []
        icons = []
        counts = []
        ammo_list = ['arrows', 'mines']
        ammo_list.extend(entity.broadsides.get_attached_weapon_ammo_types())
        for ammo in sorted(ammo_list):
            if entity.cargo.item_type_in_manifest(ammo):
                names.append(game_font.render(f"{ammo.capitalize()}", True, colors['mountain']))
                icons.append(cargo_icons[ammo])
                counts.append(game_font.render(f"{entity.cargo.manifest[ammo]}", True, colors['mountain']))
        height = len(names)
        if height > 0:
            ammo_surf = Surface((ui_layout.status_width - 2 * margin,
                                 height * game_font.get_height()))
            for i in range(0, height):
                ammo_surf.blit(names[i], (0, i * game_font.get_height()))
                ammo_surf.blit(icons[i], (ammo_surf.get_width() - icons[i].get_width(),
                                          i * game_font.get_height()))
                ammo_surf.blit(counts[i],
                               (ammo_surf.get_width() - icons[i].get_width() - counts[i].get_width(),
                                i * game_font.get_height()))
            status_panel.blit(ammo_surf, (margin, status_panel.get_height() - ammo_surf.get_height() - margin))
    console.blit(status_panel, (0, ui_layout.mini_height))


def render_wind(direction: int, display_surf: Surface, ui: DisplayInfo) -> int:
    """
    Render the wind information
    :param direction: direction the wind is blowing
    :param display_surf: Surface to render on
    :param ui: display info
    :return: None
    """
    compass = misc_icons['compass']
    display_surf.blit(compass, (ui.status_width - compass.get_width() - 3 * margin, margin * 2))
    if direction is not None:
        display_surf.blit(rot_center(image=misc_icons['pointer'], angle=direction_angle[direction]),
                          (ui.status_width - compass.get_width() - 3 * margin, margin * 2))
    return compass.get_height() + margin


def render_weather(time: Time, weather: Weather, display_surf: Surface) -> None:
    """
    Render the weather information
    :param time: current game Time
    :param weather: current map Weather
    :param display_surf: Surface to render on
    :return: None
    """
    weather_dict = weather.get_weather_info
    
    if 6 <= time.hrs < 18:
        icon = misc_icons['sun']
    else:
        icon = misc_icons['moon']
    
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
        moon_shadow_icon = misc_icons['moon_shadow']
        moon_shadow_icon = colorize(image=moon_shadow_icon, new_color=time.get_sky_color)
        
        if numeric_time >= 1800:  # account for day change in middle of night
            offset = 0
        else:
            offset = 1
        sky_surf.blit(moon_shadow_icon, (icon_x - abs(time.day - 15 - offset) - 8, icon_y))
    
    icon = misc_icons[weather_dict['name'].lower()]
    for x in range(sky_surf.get_width() // icon.get_width()):
        sky_surf.blit(icon, (x * icon.get_width(), (x + 1) % 2))
    
    display_surf.blit(sky_surf, (margin * 3, 2 * margin))
