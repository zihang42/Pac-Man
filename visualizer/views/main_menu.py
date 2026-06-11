"""
The view of our main menu
This view will be display at the
game start's
6 -> pacman
"""

import sys
from pathlib import Path

import arcade


def get_resource_path(relative_path: str) -> Path:
    """Return the correct resource path in development and PyInstaller."""
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).resolve().parents[2] / relative_path


assets_path = get_resource_path("visualizer/views/assets")
arcade.resources.add_resource_handle("my-assets", str(assets_path))


class MainMenuView(arcade.View):
    def __init__(self, pacman_visu: arcade.Window) -> None:
        super().__init__()

        self.menu_sprite = arcade.Sprite(
            ":my-assets:tile_maps/main_menu/main_menu.png",
            1.1,
            400,
            400,
        )
        self.control = arcade.Sprite(
            ":my-assets:tile_maps/control/control.png",
            1,
            400,
            400,
        )
        self.quit = arcade.Text(
            "To  Get  Back  To  Menu  Press  Esc",
            130,
            200,
            arcade.color.YELLOW,
            30,
            font_name="ARCADECLASSIC",
        )
        self.sprite_list: arcade.SpriteList[arcade.Sprite] = (
            arcade.SpriteList()
        )
        self.sprite_list.append(self.menu_sprite)
        self.control_list: arcade.SpriteList[arcade.Sprite] = (
            arcade.SpriteList()
        )
        self.control_list.append(self.control)
        self.pacman_visu = pacman_visu
        self.show_control = False

    def on_draw(self) -> None:
        self.clear()
        self.sprite_list.draw()
        if self.show_control:
            self.control_list.draw()
            self.quit.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            if self.show_control:
                self.show_control = False
            else:
                sys.exit()
        if symbol == arcade.key.C:
            self.show_control = True
        if symbol == arcade.key.P:
            self.pacman_visu.view_game_instance()
        if symbol == arcade.key.S:
            self.pacman_visu.view_score_board(from_menu=True)

    def on_update(self, delta_time: float) -> None:
        pass
