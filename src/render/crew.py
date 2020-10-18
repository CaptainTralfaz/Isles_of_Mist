from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Surface

from constants.colors import colors
from constants.constants import margin, game_font
from constants.stats import occupation_stats
from render.utilities import render_border

if TYPE_CHECKING:
    from components.crew import Crew
    from time_of_day import Time
    from ui import DisplayInfo


def crew_render(console: Surface,
                crew: Crew,
                time: Time,
                ui_layout: DisplayInfo) -> None:
    """
    creates the crew config display screen
    :param console: Surface to blit to
    :param crew: player's Crew component
    :param time: current game Time
    :param ui_layout: DisplayInfo
    :return: None
    """
    crew_surf = Surface((ui_layout.viewport_width, ui_layout.viewport_height))
    count = 0
    height = margin * 2
    
    game_font.set_underline(True)
    surf = game_font.render(f"Assign", True, colors['mountain'])
    crew_surf.blit(surf, (margin * 2, height))
    surf = game_font.render(f"Crewman", True, colors['mountain'])
    crew_surf.blit(surf, (70, height))
    surf = game_font.render(f"Occupation", True, colors['mountain'])
    crew_surf.blit(surf, (300, height))
    surf = game_font.render(f"Cooldown", True, colors['mountain'])
    crew_surf.blit(surf, (425, height))
    surf = game_font.render(f"Monthly", True, colors['cyan'])
    crew_surf.blit(surf, (535, height))
    height += game_font.get_height() + margin
    
    game_font.set_underline(False)
    
    for crewman in crew.roster:
        if count == crew.selected:
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
        if crewman.cooldown > 0:
            surf = game_font.render(f"{crewman.cooldown}", True, colors['red'])
            crew_surf.blit(surf, (470 - surf.get_width(), height))
        surf = game_font.render(f"{occupation_stats[crewman.occupation]['cost']}", True, colors['cyan'])
        crew_surf.blit(surf, (575 - surf.get_width(), height))
        
        height += game_font.get_height() + margin
        count += 1
    
    crewman = crew.roster[crew.selected]
    surf = game_font.render(f"{crewman.occupation.capitalize()}: {occupation_stats[crewman.occupation]['description']}",
                            True, colors['mountain'])
    crew_surf.blit(surf, ((ui_layout.viewport_width - surf.get_width()) // 2,
                          ui_layout.viewport_height - game_font.get_height() - margin * 2))
    
    time.tint_render(crew_surf)
    render_border(crew_surf, time.get_sky_color)
    console.blit(crew_surf, (ui_layout.mini_width, 0))
