"""
    This module will manage all the sprites
    logic and behavior
"""
import arcade
from pathlib import Path
from .sprites_utils import SpritesStock


actual_dir = Path(__file__).parent
sprites_dir = actual_dir / "assets/sprites"
walls_dir = actual_dir / "assets/walls"

arcade.resources.add_resource_handle(
    handle="sprites-characters",
    path=str(sprites_dir)
)
arcade.resources.add_resource_handle(
    handle="sprites-walls",
    path=str(walls_dir)
)


class SpriteItem(arcade.Sprite):
    def __init__(self, texture_list: list[arcade.Texture], item_frame: int):
        super().__init__(texture_list[0], scale=0.6)
        self.time_elapsed = 0
        self.textures = texture_list
        self.cur_texture_index = 0
        self.item_frame = item_frame

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.time_elapsed += delta_time

        if self.time_elapsed > 0.1:
            if self.cur_texture_index < len(self.textures):
                self.set_texture(self.cur_texture_index)
                self.cur_texture_index += 1
            self.time_elapsed = 0

        if self.cur_texture_index == self.item_frame:
            self.cur_texture_index = 0


class SpritesManager():
    def __init__(self, debug: bool = False) -> None:
        self.debug = debug
        self.sprites_dicts = SpritesStock()
        self.sprites_list = []
        print(self.sprites_list)

        # walls initialisation
        self.walls_list = arcade.SpriteList()
        x = 500
        y = 360
        for path in self.sprites_dicts.walls_path:
            sprites = arcade.Sprite(path, scale=0.5)
            sprites.position = x, y
            x += 100
            if x > 1100:
                y += 100
                x = 500
            self.walls_list.append(sprites)

    def create_sprite_list(self):
        for sprite in self.sprites_dicts.paths_dict:
            name = sprite["name"]
            path = sprite["path"]
            frame_count = sprite["frame_count"]
            frame_size = sprite["frame_size"]
            pos = sprite["position"]
            lst = arcade.SpriteList()
            sheet = arcade.load_spritesheet(path)
            texture_list = sheet.get_texture_grid(
                size=frame_size,
                columns=frame_count,
                count=frame_count
            )
            sprite_item = SpriteItem(
                texture_list,
                item_frame=frame_count
            )
            sprite_item.position = pos
            lst.append(sprite_item)
            self.sprites_list.append(lst)
            if self.debug:
                print(
                    f"Created {name}, with path: {path} frame_count: {frame_count} "
                    f"and frame_size: {frame_size} at {pos}"
                )
