'''
    The view of our main menu
    This view will be display at the
    game start's
'''
import arcade
from .sprites import SpritesManager


class MainMenuView(arcade.View):
    def __init__(self, debug: bool = False) -> None:
        super().__init__()
        self.debug = debug
        self.sprites = SpritesManager(debug)
        self.sprites.create_sprite_list()

    def on_draw(self) -> None:
        self.clear()
        if self.debug:
            for lst in self.sprites.sprites_list:
                lst.draw()
            self.sprites.walls_list.draw()

    def on_update(self, delta_time: float) -> None:
        for lst in self.sprites.sprites_list:
            lst.update()
