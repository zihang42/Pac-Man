"""
The main window of arcade where
everything will be display
"""

import arcade

from .views.maze_test import TestView
from typing import Any
from .views.game_over import GameOverView
from .views.main_menu import MainMenuView
from .views.score_board import ScoreBoardView
from .views.victory import VictoryView
from src.parser import Config


class Window:
    """
    This class will be like the manager of
    the game

    It can switch the view of the game
    and start the visualisation from the main
    program

    Attributes:
        window:     This is the Window class of arcade
                    basicly this use the pyglet GE to
                    display our window
        menu:       Our main menu class that will be called
                    when we need to display it on the window
        score_board:Same thing but for the score board
        game_over:  Same for the game over
        victory:    Same for the victory

    Exemple:
        In our pac_man.py we'll instanciate this class
        then we'll be able to call differant method to manage
        the game such as the start static method
    """

    def __init__(self, window: int, height: int,
                 fps: int, config: Config) -> None:
        self.window = arcade.Window(
            width=window,
            height=height,
            title="PacMan",
            fullscreen=False,
            enable_polling=True,
            update_rate=1 / fps,
        )
        self.config = config
        self.score = 0
        '''
        self.game_instance = TestView(
            config,
            level_index=0,
            player_speed=4,
            ghost_speed=3,
            is_cheat_mode=True
        )
        '''

    def view_menu(self) -> None:
        """
        This method is called to display the
        main menu
        """
        self.window.show_view(MainMenuView(self.pacman_visu))

    def view_score_board(self, from_menu: bool = False) -> None:
        """
        This method is called to display the
        score board
        """
        self.window.show_view(ScoreBoardView(
            self.pacman_visu, from_menu
        ))

    def view_game_over(self) -> None:
        """
        This method is called to display the
        game over screen
        """
        self.window.show_view(GameOverView(self.pacman_visu))

    def view_victory(self) -> None:
        """
        This method is called to display the
        victory screen
        """
        self.window.show_view(VictoryView(self.pacman_visu))

    def view_game_instance(self) -> None:
        """
        This method is called to display
        the game instance
        """
        self.window.show_view(TestView(
            self.config,
            level_index=0,
            player_speed=4,
            ghost_speed=3,
            is_cheat_mode=False,
            pacman_visu=self.pacman_visu
        ))

    def start(self, pacman_visu: Any) -> None:
        """
        This method is called to start the arcade
        and to display the main menu
        """
        self.pacman_visu = pacman_visu
        self.window.show_view(MainMenuView(pacman_visu))
        arcade.run()
