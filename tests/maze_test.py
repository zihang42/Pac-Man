import arcade

from src.ghost import Ghost
from src.maze import Maze
from src.player import Player
from src.utils import DIRECTION
from visualizer.views import sprites as _sprites  # noqa: F401

KEY_DIRECTIONS = {
    arcade.key.UP: DIRECTION.UP,
    arcade.key.W: DIRECTION.UP,
    arcade.key.DOWN: DIRECTION.DOWN,
    arcade.key.S: DIRECTION.DOWN,
    arcade.key.LEFT: DIRECTION.LEFT,
    arcade.key.A: DIRECTION.LEFT,
    arcade.key.RIGHT: DIRECTION.RIGHT,
    arcade.key.D: DIRECTION.RIGHT,
}


class TestView(arcade.View):
    """Debug view for testing maze rendering and player movement."""

    def __init__(
        self, maze: Maze, player: Player, ghosts: list[Ghost]
    ) -> None:
        super().__init__()
        self.maze = maze
        self.player = player
        self.ghosts = ghosts
        self.margin = 48
        self.frame = 0
        self.frame_time = 0.0
        self.player_textures = self._load_player_textures()
        self.ghost_textures = self._load_ghost_textures()
        self.player_sprite = arcade.Sprite(
            self.player_textures[self.player.direction][0]
        )
        self.player_sprites: arcade.SpriteList[arcade.Sprite] = (
            arcade.SpriteList()
        )
        self.player_sprites.append(self.player_sprite)
        self.ghost_sprites: arcade.SpriteList[arcade.Sprite] = (
            arcade.SpriteList()
        )

        self.ghost_colors = ["cyan", "orange", "pink", "red"]

        for color in self.ghost_colors:
            sprite = arcade.Sprite(self.ghost_textures[color][0])
            self.ghost_sprites.append(sprite)

    def on_draw(self) -> None:
        self.clear()
        left, bottom, cell_size = self._layout()

        self._draw_maze(left, bottom, cell_size)

        row, col = self.player.row, self.player.col
        center_x = left + (col + 0.5) * cell_size
        center_y = bottom + (self.maze.height - row - 0.5) * cell_size
        texture = self.player_textures[self.player.direction][self.frame]
        self.player_sprite.texture = texture
        self.player_sprite.scale = (
            cell_size * 0.72 / texture.width,
            cell_size * 0.72 / texture.height,
        )
        self.player_sprite.position = center_x, center_y
        self.player_sprites.draw(pixelated=True)

        for ghost, sprite, color in zip(
            self.ghosts,
            self.ghost_sprites,
            self.ghost_colors,
        ):
            row, col = ghost.row, ghost.col

            texture = self.ghost_textures[color][self.frame]
            sprite.texture = texture

            center_x = left + (col + 0.5) * cell_size
            center_y = bottom + (self.maze.height - row - 0.5) * cell_size

            sprite.scale = (
                cell_size * 0.72 / texture.width,
                cell_size * 0.72 / texture.height,
            )
            sprite.position = center_x, center_y
        self.ghost_sprites.draw(pixelated=True)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        direction = KEY_DIRECTIONS.get(symbol)
        if direction is not None:
            self.player.set_direction(direction)

    def on_update(self, delta_time: float) -> None:
        # For the animation
        self.frame_time += delta_time
        if self.frame_time >= 0.12:
            frame_count = len(self.player_textures[self.player.direction])
            self.frame = (self.frame + 1) % frame_count
            self.frame_time = 0.0
        self.player.on_update(delta_time)
        for ghost in self.ghosts:
            ghost.on_update(delta_time)

    def _layout(self) -> tuple[float, float, float]:
        usable_width = self.window.width - self.margin * 2
        usable_height = self.window.height - self.margin * 2
        cell_size = min(
            usable_width / self.maze.width,
            usable_height / self.maze.height,
        )
        maze_width = self.maze.width * cell_size
        maze_height = self.maze.height * cell_size
        left = self.margin + (usable_width - maze_width) / 2
        bottom = self.margin + (usable_height - maze_height) / 2
        return left, bottom, cell_size

    def _draw_maze(self, left: float, bottom: float, cell_size: float) -> None:
        for row, cells in enumerate(self.maze.cells):
            for col, cell in enumerate(cells):
                x1 = left + col * cell_size
                y1 = bottom + (self.maze.height - row - 1) * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                arcade.draw_lrbt_rectangle_filled(
                    x1, x2, y1, y2, arcade.color.BLACK
                )
                if cell.is_42_pattern:
                    arcade.draw_lrbt_rectangle_filled(
                        x1, x2, y1, y2, arcade.color.DARK_BLUE_GRAY
                    )
                if cell.north_wall:
                    arcade.draw_line(x1, y2, x2, y2, arcade.color.WHITE, 2)
                if cell.east_wall:
                    arcade.draw_line(x2, y1, x2, y2, arcade.color.WHITE, 2)
                if cell.south_wall:
                    arcade.draw_line(x1, y1, x2, y1, arcade.color.WHITE, 2)
                if cell.west_wall:
                    arcade.draw_line(x1, y1, x1, y2, arcade.color.WHITE, 2)

    def _load_player_textures(self) -> dict[DIRECTION, list[arcade.Texture]]:
        textures = {}
        for direction, name in (
            (DIRECTION.UP, "pacman_up.png"),
            (DIRECTION.DOWN, "pacman_down.png"),
            (DIRECTION.LEFT, "pacman_left.png"),
            (DIRECTION.RIGHT, "pacman_right.png"),
        ):
            sheet = arcade.load_spritesheet(f":sprites-characters:{name}")
            textures[direction] = sheet.get_texture_grid(
                size=(101, 90),
                columns=2,
                count=2,
            )
        return textures

    def _load_ghost_textures(self) -> dict[str, list[arcade.Texture]]:
        textures = {}
        for name, file in (
            ("cyan", "cyan_ghost.png"),
            ("orange", "orange_ghost.png"),
            ("pink", "pink_ghost.png"),
            ("red", "red_ghost.png"),
        ):
            sheet = arcade.load_spritesheet(f":sprites-characters:{file}")
            textures[name] = sheet.get_texture_grid(
                size=(101, 90),
                columns=2,
                count=2,
            )
        return textures
