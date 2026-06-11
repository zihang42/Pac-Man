import re
from pathlib import Path

import arcade

from .highscores import HighscoreEntry, load_highscores, save_highscores

assets_path = Path().absolute().resolve() / Path("visualizer/views/assets")
arcade.resources.add_resource_handle("my-assets", assets_path)
arcade.load_font(":my-assets:fonts/ARCADECLASSIC.TTF")


class ScoreBoardView(arcade.View):
    def __init__(
        self, pacman_visu: arcade.Window, from_menu: bool = False
    ) -> None:
        super().__init__()
        self.pacman_visu = pacman_visu

        self.menu_sprite = arcade.Sprite(
            ":my-assets:tile_maps/score/score_board.png",
            scale=1.1,
            center_x=400,
            center_y=400,
        )
        self.sprite_list: arcade.SpriteList[arcade.Sprite] = (
            arcade.SpriteList()
        )
        self.sprite_list.append(self.menu_sprite)
        self.from_menu = from_menu

        self.current_score = self.pacman_visu.score

        self.highscores = load_highscores()

        self.player_name = ""
        self.is_typing = not from_menu
        self.error_message = ""

        # text part
        self.great_text = arcade.Text(
            "GREAT JOB !",
            400,
            550,
            arcade.color.YELLOW,
            24,
            anchor_x="center",
            font_name="ARCADECLASSIC",
        )
        self.score1th_text = arcade.Text(
            f"Your Score  {self.current_score}",
            400,
            500,
            arcade.color.WHITE,
            20,
            anchor_x="center",
            font_name="ARCADECLASSIC",
        )
        self.name_prompt_text = arcade.Text(
            "Enter  Your  Name  10  chars  max",
            400,
            430,
            arcade.color.CYAN,
            16,
            anchor_x="center",
            font_name="ARCADECLASSIC",
        )
        self.enter_text = arcade.Text(
            "Press   Enter   When   Done",
            400,
            300,
            arcade.color.GRAY,
            12,
            anchor_x="center",
            font_name="ARCADECLASSIC",
        )
        self.error_text = arcade.Text(
            self.error_message,
            400,
            260,
            arcade.color.RED,
            12,
            anchor_x="center",
            font_name="ARCADECLASSIC",
        )
        self.quit_text = arcade.Text(
            "Pres   Esc   To   Get  \
Back   To   The   Main   Menu",
            400,
            50,
            arcade.color.WHITE,
            12,
            anchor_x="center",
            font_name="ARCADECLASSIC",
        )

    def on_draw(self) -> None:
        """
        The on_draw method that handle displaying

        It will display a prompt to the player when
        he need to type the name and then to display
        the other highscores
        """
        self.clear()

        if self.is_typing and not self.from_menu:
            self.great_text.draw()
            self.score1th_text.draw()
            self.name_prompt_text.draw()
            display_name = self.player_name if self.player_name else "_"
            text = arcade.Text(
                display_name,
                400,
                380,
                arcade.color.GREEN,
                28,
                anchor_x="center",
                font_name="ARCADECLASSIC",
            )
            text.draw()
            self.enter_text.draw()

            if self.error_message:
                self.error_text.draw()
        else:
            self.sprite_list.draw()
            start_y = 517  # I've put the values that's look the best
            line_height = 47
            for i, entry in enumerate(self.highscores):
                current_y = start_y - (i * line_height)
                score = arcade.Text(
                    str(entry.score),
                    380,
                    current_y,
                    arcade.color.WHITE,
                    27,
                    anchor_x="center",
                    font_name="ARCADECLASSIC",
                )
                score.draw()
                name = arcade.Text(
                    entry.name,
                    570,
                    current_y,
                    arcade.color.WHITE,
                    27,
                    anchor_x="left",
                    font_name="ARCADECLASSIC",
                )
                name.draw()
        self.quit_text.draw()

    def on_text(self, text: str) -> None:
        """
        The magic function that is handling in live
        the corectness of the typing

        Arguments:
            Text: The name that's beeing typed
        """
        if self.is_typing and not self.from_menu:
            if len(self.player_name) < 10 and re.match(
                r"^[a-zA-Z0-9 ]+$", text
            ):
                self.player_name += text

    def on_key_press(self, key: int, modifiers: int) -> None:
        """
        Key handling fonction

        Arguments:
            Key: The key that is pressed
            Modifiers: Check if there is key combinaison

        Exemples:
            Backspace: Remove the last char
            Enter: Validate the name
            Escape: Retrun to the main menu
        """
        if self.is_typing and not self.from_menu:
            if key == arcade.key.BACKSPACE:
                self.player_name = self.player_name[:-1]

            elif key == arcade.key.ENTER:
                if not self.player_name.strip():
                    self.error_message = "Name Can't Be Empty !"
                    return
                new_entry = HighscoreEntry(
                    name=self.player_name, score=self.current_score
                )
                self.highscores.append(new_entry)
                self.highscores.sort(key=lambda x: x.score, reverse=True)
                self.highscores = self.highscores[:10]
                save_highscores(self.highscores)
                self.is_typing = False
        if key == arcade.key.ESCAPE:
            self.pacman_visu.view_menu()
