'''
    The view of the victory screen
    This view will be display when
    the player win
'''
import arcade
import time
from pathlib import Path

assets_path = Path().absolute().resolve() / Path("visualizer/views/assets")
arcade.resources.add_resource_handle("my-assets", assets_path)


class VictoryView(arcade.View):
    def __init__(self, pacman_visu: arcade.Window) -> None:
        super().__init__()

        self.menu_sprite = arcade.Sprite(
            ":my-assets:tile_maps/winner/win_screen.png",
            1.1,
            400,
            400,
        )
        self.sprite_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()
        self.sprite_list.append(self.menu_sprite)
        self.pacman_visu = pacman_visu

    def on_draw(self) -> None:
        self.clear()
        self.sprite_list.draw()

    def on_update(self, delta_time: float) -> None:
        time.sleep(4)
        self.pacman_visu.view_score_board()
