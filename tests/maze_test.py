import arcade

from src.ghost import Ghost, GhostState
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

GHOST_COLORS = ("cyan", "orange", "pink", "red")
POINTS_PER_GHOST = 200
COLLISION_RADIUS = 0.35
SPRITE_SCALE = 0.72
ANIMATION_FRAME_TIME = 0.12
PLAYER_DEATH_FRAME_TIME = 0.08


class TestView(arcade.View):
    """Debug view for testing maze rendering and entity movement."""

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
        self.player_is_dying = False
        self.death_frame = 0
        self.death_frame_time = 0.0

        self.player_textures = self._load_player_textures()
        self.player_death_textures = self._load_player_death_textures()
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
        for color in GHOST_COLORS:
            sprite = arcade.Sprite(self.ghost_textures[color][0])
            self.ghost_sprites.append(sprite)

    def on_draw(self) -> None:
        self.clear()
        left, bottom, cell_size = self._layout()
        self._draw_maze(left, bottom, cell_size)
        self._draw_player(left, bottom, cell_size)
        self._draw_ghosts(left, bottom, cell_size)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        direction = KEY_DIRECTIONS.get(symbol)
        if direction is not None:
            self.player.set_direction(direction)

    def on_update(self, delta_time: float) -> None:
        self._update_animation(delta_time)
        if self.player_is_dying:
            self._update_player_death(delta_time)
            return

        self.player.on_update(delta_time)
        for ghost in self.ghosts:
            ghost.on_update(delta_time, self.player.pos)
        self._check_collisions()

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
            GHOST_COLORS,
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

    def _update_player_death(self, delta_time: float) -> None:
        self.death_frame_time += delta_time
        if self.death_frame_time < PLAYER_DEATH_FRAME_TIME:
            return

        self.death_frame_time = 0.0
        self.death_frame += 1
        if self.death_frame < len(self.player_death_textures):
            return

        self.player_is_dying = False
        self.death_frame = 0
        if self.player.lives > 0:
            self._reset_after_player_hit()

    def _check_collisions(self) -> None:
        for ghost in self.ghosts:
            if not self._is_colliding_with_player(ghost):
                continue

            if ghost.state == GhostState.FRIGHTEN:
                ghost.get_eaten()
                self.player.add_score(POINTS_PER_GHOST)
            elif ghost.state == GhostState.CHASE:
                self.player.lose_life()
                self._start_player_death()
                break

    def _is_colliding_with_player(self, ghost: Ghost) -> bool:
        return (
            abs(ghost.row - self.player.row) <= COLLISION_RADIUS
            and abs(ghost.col - self.player.col) <= COLLISION_RADIUS
        )

    def _start_player_death(self) -> None:
        self.player_is_dying = True
        self.player.is_alive = False
        self.death_frame = 0
        self.death_frame_time = 0.0

    def _reset_after_player_hit(self) -> None:
        self.player.respawn()
        for ghost in self.ghosts:
            ghost.respawn()

    def _get_player_texture(self) -> arcade.Texture:
        if self.player_is_dying:
            frame = min(self.death_frame, len(self.player_death_textures) - 1)
            return self.player_death_textures[frame]

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

    def _load_player_death_textures(self) -> list[arcade.Texture]:
        return self._load_texture_grid(
            "pacman_death.png",
            size=(79, 80),
            columns=12,
            count=12,
        )

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
