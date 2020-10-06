from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Surface

from constants.constants import margin, game_font
from constants.colors import colors
from render.utilities import render_border

if TYPE_CHECKING:
    from components.crew import Crew
    from weather import Time
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
    height = margin
    
    for crewman in crew.roster:
        if count == crew.selected:
            text_color = colors['black']
            background = colors['mountain']
        else:
            text_color = colors['mountain']
            background = colors['black']
        occupation_surf = game_font.render(f"{crewman.occupation.capitalize()}", True, colors['mountain'])
        crew_surf.blit(occupation_surf, (margin, height))
        name_surf = game_font.render(f"{crewman.name}", True, text_color, background)
        crew_surf.blit(name_surf, (margin + 200, height))
        for key in crew.assignments.keys():
            if crew.assignments[key] == crewman:
                assign_surf = game_font.render(f"{str(key).capitalize()}", True, colors['mountain'])
                crew_surf.blit(assign_surf, (margin + 120, height))
        height += game_font.get_height()
        count += 1
    
    time.tint_render(crew_surf)
    render_border(crew_surf, time.get_sky_color)
    console.blit(crew_surf, (ui_layout.mini_width, 0))
