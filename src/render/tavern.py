from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Surface

from components.crew import occupation_stats
from constants.colors import colors
from constants.constants import margin, game_font
from constants.images import cargo_icons
from render.utilities import render_border

if TYPE_CHECKING:
    from entity import Entity
    from time_of_day import Time
    from ui import DisplayInfo


def tavern_render(console: Surface,
                  player: Entity,
                  time: Time,
                  ui_layout: DisplayInfo) -> None:
    """
    creates the crew config display screen
    :param console: Surface to blit to
    :param player: player Entity
    :param time: current game Time
    :param ui_layout: DisplayInfo
    :return: None
    """
    crew_surf = Surface((ui_layout.viewport_width, ui_layout.viewport_height))
    count = 0
    height = margin * 2
    spacer = 35
    
    tavern_coins = player.game_map.port.tavern.temp_coins
    crew_roster = player.crew.roster
    tavern_roster = player.game_map.port.tavern.roster
    full_roster = []
    for crewman in crew_roster:
        full_roster.append(crewman)
    for crewman in tavern_roster:
        full_roster.append(crewman)
    
    coins = cargo_icons['coins']
    crew_surf.blit(coins, (margin * 2, height))
    surf = game_font.render(f"{player.cargo.coins - tavern_coins}", True, colors['mountain'])
    crew_surf.blit(surf, (spacer, height))
    current_count = len(crew_roster) + len(player.crew.hire_list) - len(player.crew.release_list)
    if current_count <= player.crew.max_count:
        color = colors['mountain']
    else:
        color = colors['red']
    surf = game_font.render(f"Crew Count: {current_count}/{player.crew.max_count} ", True, color)
    crew_surf.blit(surf, ((ui_layout.viewport_width - surf.get_width()) // 2, height))
    crew_surf.blit(coins, (crew_surf.get_width() - coins.get_width() - margin * 2, height))
    surf = game_font.render(f"{tavern_coins}", True, colors['red'])
    crew_surf.blit(surf, (crew_surf.get_width() - surf.get_width() - coins.get_width() - margin * 4, height))
    height += game_font.get_height() + margin
    
    game_font.set_underline(True)
    surf = game_font.render(f"Assign", True, colors['mountain'])
    crew_surf.blit(surf, (margin * 2, height))
    surf = game_font.render(f"Crewman", True, colors['mountain'])
    crew_surf.blit(surf, (70, height))
    surf = game_font.render(f"Occupation", True, colors['mountain'])
    crew_surf.blit(surf, (300, height))
    surf = game_font.render(f"Location", True, colors['mountain'])
    crew_surf.blit(surf, (425, height))
    surf = game_font.render(f"Monthly", True, colors['cyan'])
    crew_surf.blit(surf, (535, height))
    height += game_font.get_height() + margin
    game_font.set_underline(False)
    
    for crewman in full_roster:
        if count == player.crew.selected:
            text_color = colors['black']
            background = colors['mountain']
        else:
            text_color = colors['mountain']
            background = colors['black']
        if crewman.assignment:
            assign_surf = game_font.render(f"{crewman.assignment.name.lower().capitalize()}", True, colors['mountain'])
            crew_surf.blit(assign_surf, (margin * 2, height))
        name_surf = game_font.render(f"{crewman.name}", True, text_color, background)
        crew_surf.blit(name_surf, (70, height))
        occupation_surf = game_font.render(f"{crewman.occupation.capitalize()}", True, colors['mountain'])
        crew_surf.blit(occupation_surf, (300, height))
        if crewman in player.crew.release_list:
            location = "Tavern"
            color = colors['red']
        elif crewman in player.crew.hire_list:
            location = "Crew"
            color = colors['grass']
        elif crewman in crew_roster:
            location = "Crew"
            color = colors['mountain']
        else:
            location = "Tavern"
            color = colors['pink']
        surf = game_font.render(location, True, color)
        crew_surf.blit(surf, (435, height))
        surf = game_font.render(f"{occupation_stats[crewman.occupation]['cost']}", True, colors['cyan'])
        crew_surf.blit(surf, (575 - surf.get_width(), height))
        
        height += game_font.get_height() + margin
        count += 1
    
    time.tint_render(crew_surf)
    render_border(crew_surf, time.get_sky_color)
    console.blit(crew_surf, (ui_layout.mini_width, 0))
