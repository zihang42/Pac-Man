from pathlib import Path

import arcade

from src.ghost import Ghost, GhostState
from src.level import Level
from src.parser import Config
from src.utils import DIRECTION

from . import sprites as _sprites  # noqa: F401

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

SPRITE_SCALE = 0.72
PACGUM_RADIUS = 0.10
SUPER_PACGUM_RADIUS = 0.22
ANIMATION_FRAME_TIME = 0.12

assets_path = Path().absolute().resolve() / Path("visualizer/views/assets")
arcade.resources.add_resource_handle("my-assets", assets_path)
arcade.load_font(":my-assets:fonts/ARCADECLASSIC.TTF")


class TestView(arcade.View):
    def __init__(
        self,
        config: Config,
        pacman_visu: arcade.Window,
        level_index: int = 0,
        player_speed: int = 5,
        ghost_speed: int = 3,
        is_cheat_mode: bool = False,
    ) -> None:
        super().__init__()
        self.pacman_visu = pacman_visu
        self.config = config
        self.level_index = level_index
        self.player_speed = player_speed
        self.ghost_speed = ghost_speed
        self.is_cheat_mode = is_cheat_mode
        self.finished_game = False
        self.level = self._create_level(level_index)
        self.next_level = self._create_next_level()
        self._sync_level_refs()
        self.margin = 10
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

        self.score_text = arcade.Text(
            f"Score {self.pacman_visu.score}",
            0,
            780,
            arcade.color.GREEN,
            20,
            anchor_x="left",
            font_name="ARCADECLASSIC",
        )
        self.lives_text = arcade.Text(
            f"Lives {self.player.lives}",
            790,
            780,
            arcade.color.RED,
            20,
            anchor_x="right",
            font_name="ARCADECLASSIC",
        )
        self.pause_text = arcade.Text(
            "PAUSE",
            330,
            400,
            arcade.color.YELLOW,
            40,
            font_name="ARCADECLASSIC",
        )
        self.is_paused = False
        self.ragequit_text = arcade.Text(
            "To  Quit  Press  Q",
            250,
            350,
            arcade.color.YELLOW,
            30,
            font_name="ARCADECLASSIC",
        )
        self.remaining_time = float(self.config.level_max_time)

        self.time_text = arcade.Text(
            f"Time {int(self.remaining_time)}",
            400,
            780,
            arcade.color.WHITE,
            20,
            anchor_x="center",
            font_name="ARCADECLASSIC",
        )

    def on_draw(self) -> None:
        self.clear()
        left, bottom, cell_size = self._layout()
        self._draw_maze(left, bottom, cell_size)
        self._draw_pacgums(left, bottom, cell_size)
        self._draw_player(left, bottom, cell_size)
        self._draw_ghosts(left, bottom, cell_size)

        self.score_text.draw()
        self.lives_text.draw()
        self.time_text.draw()
        if self.is_paused:
            self.pause_text.draw()
            self.ragequit_text.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            self.is_paused = not self.is_paused
            return
        direction = KEY_DIRECTIONS.get(symbol)
        if direction is not None:
            self.player.set_direction(direction)
        if symbol == arcade.key.Q:
            self.pacman_visu.view_menu()
        if symbol == arcade.key.F1:
            self.is_cheat_mode = not self.is_cheat_mode
            self.level.is_cheat_mode = self.is_cheat_mode
            print(f"Cheat mode: {self.is_cheat_mode}")

    def on_update(self, delta_time: float) -> None:
        if self.is_paused:
            return
        self._update_animation(delta_time)
        if self.finished_game:
            return

        self.level.on_update(delta_time)
        if self.level.win:
            self._load_next_level()
        self.pacman_visu.score = self.player.score
        self.score_text.text = f"Score {self.pacman_visu.score}"
        self.lives_text.text = f"Lives {self.player.lives}"
        self.remaining_time -= delta_time

        if self.remaining_time <= 0:
            self.remaining_time = 0
            self.game_over = True
            self.pacman_visu.view_game_over()
            return

        self.time_text.text = f"Time {int(self.remaining_time)}"

    def _create_level(self, level_index: int) -> Level:
        return Level(
            lvl=level_index,
            config=self.config,
            player_speed=self.player_speed,
            ghost_speed=self.ghost_speed,
            is_cheat_mode=self.is_cheat_mode,
            pacman_visu=self.pacman_visu,
        )

    def _create_next_level(self) -> Level | None:
        next_level = self.level_index + 1
        if next_level >= len(self.config.levels):
            return None
        return self._create_level(next_level)

    def _sync_level_refs(self) -> None:
        self.maze = self.level.maze
        self.player = self.level.player
        self.ghosts = self.level.ghosts

    def _load_next_level(self) -> None:
        if self.next_level is None:
            self.finished_game = True
            return

        score = self.player.score
        lives = self.player.lives
        self.level_index += 1
        self.level = self.next_level
        self.player = self.level.player
        self.player.score += score
        self.player.lives = lives
        self._sync_level_refs()
        self.next_level = self._create_next_level()
        self.remaining_time = float(self.config.level_max_time)

    def _draw_player(
        self,
        left: float,
        bottom: float,
        cell_size: float,
    ) -> None:
        texture = self._get_player_texture()
        center = self._cell_center(
            self.player.row,
            self.player.col,
            left,
            bottom,
            cell_size,
        )
        self._place_sprite(self.player_sprite, texture, center, cell_size)
        self.player_sprites.draw(pixelated=True)

    def _draw_ghosts(
        self,
        left: float,
        bottom: float,
        cell_size: float,
    ) -> None:
        for ghost, sprite, color in zip(
            self.ghosts,
            self.ghost_sprites,
            self.ghost_colors,
        ):
            texture_key = self._get_ghost_texture_key(ghost, color)
            textures = self.ghost_textures[texture_key]
            texture = textures[self.frame % len(textures)]
            center = self._cell_center(
                ghost.row,
                ghost.col,
                left,
                bottom,
                cell_size,
            )
            self._place_sprite(sprite, texture, center, cell_size)
        self.ghost_sprites.draw(pixelated=True)

    def _draw_pacgums(
        self,
        left: float,
        bottom: float,
        cell_size: float,
    ) -> None:
        radius = max(2.0, cell_size * PACGUM_RADIUS)
        for pacgum in self.level.pacgums:
            center = self._cell_center(
                pacgum.pos.x,
                pacgum.pos.y,
                left,
                bottom,
                cell_size,
            )
            arcade.draw_circle_filled(
                center[0],
                center[1],
                radius,
                arcade.color.WHITE,
            )

        radius = max(4.0, cell_size * SUPER_PACGUM_RADIUS)
        for super_pacgum in self.level.super_pacgums:
            center = self._cell_center(
                super_pacgum.pos.x,
                super_pacgum.pos.y,
                left,
                bottom,
                cell_size,
            )
            arcade.draw_circle_filled(
                center[0],
                center[1],
                radius,
                arcade.color.WHITE,
            )

    def _place_sprite(
        self,
        sprite: arcade.Sprite,
        texture: arcade.Texture,
        center: tuple[float, float],
        cell_size: float,
    ) -> None:
        sprite.texture = texture
        sprite.scale = (
            cell_size * SPRITE_SCALE / texture.width,
            cell_size * SPRITE_SCALE / texture.height,
        )
        sprite.position = center

    def _cell_center(
        self,
        row: float,
        col: float,
        left: float,
        bottom: float,
        cell_size: float,
    ) -> tuple[float, float]:
        center_x = left + (col + 0.5) * cell_size
        center_y = bottom + (self.maze.height - row - 0.5) * cell_size
        return center_x, center_y

    def _update_animation(self, delta_time: float) -> None:
        self.frame_time += delta_time
        if self.frame_time < ANIMATION_FRAME_TIME:
            return

        self.frame += 1
        self.frame_time = 0.0

    def _get_player_texture(self) -> arcade.Texture:
        textures = self.player_textures[self.player.direction]
        return textures[self.frame % len(textures)]

    def _get_ghost_texture_key(self, ghost: Ghost, color: str) -> str:
        if ghost.state == GhostState.FRIGHTEN:
            return "frighten"
        if ghost.state == GhostState.EATEN:
            return "eaten"
        return color

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
        for direction, file_name in (
            (DIRECTION.UP, "pacman_up.png"),
            (DIRECTION.DOWN, "pacman_down.png"),
            (DIRECTION.LEFT, "pacman_left.png"),
            (DIRECTION.RIGHT, "pacman_right.png"),
        ):
            textures[direction] = self._load_texture_grid(
                file_name,
                size=(101, 90),
                columns=2,
                count=2,
            )
        return textures

    def _load_ghost_textures(self) -> dict[str, list[arcade.Texture]]:
        textures = {}
        for name, file_name, size, frame_count in (
            ("cyan", "cyan_ghost.png", (101, 90), 2),
            ("orange", "orange_ghost.png", (101, 90), 2),
            ("pink", "pink_ghost.png", (101, 90), 2),
            ("red", "red_ghost.png", (101, 90), 2),
            ("frighten", "bluewhite_ghost.png", (125, 122), 4),
            ("eaten", "dead_ghost.png", (125, 122), 4),
        ):
            textures[name] = self._load_texture_grid(
                file_name,
                size=size,
                columns=frame_count,
                count=frame_count,
            )
        return textures

    def _load_texture_grid(
        self,
        file_name: str,
        size: tuple[int, int],
        columns: int,
        count: int,
    ) -> list[arcade.Texture]:
        sheet = arcade.load_spritesheet(f":sprites-characters:{file_name}")
        return sheet.get_texture_grid(
            size=size,
            columns=columns,
            count=count,
        )
