"""
The view of the victory screen
This view will be display when
the player win
"""

import sys
import time
from pathlib import Path

import arcade


def get_resource_path(relative_path: str) -> Path:
    """Return the correct resource path in development and PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).resolve().parents[2] / relative_path


assets_path = get_resource_path("visualizer/views/assets")
arcade.resources.add_resource_handle("my-assets", str(assets_path))


class VictoryView(arcade.View):
    def __init__(self, pacman_visu: arcade.Window) -> None:
        super().__init__()

        self.menu_sprite = arcade.Sprite(
            ":my-assets:tile_maps/winner/win_screen.png",
            1.1,
            400,
            400,
        )
        self.sprite_list: arcade.SpriteList[arcade.Sprite] = (
            arcade.SpriteList()
        )
        self.sprite_list.append(self.menu_sprite)
        self.pacman_visu = pacman_visu

    def on_draw(self) -> None:
        self.clear()
        self.sprite_list.draw()

    def on_update(self, delta_time: float) -> None:
        time.sleep(4)
        self.pacman_visu.view_score_board()
