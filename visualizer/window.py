'''
    The main window of arcade where
    everything will be display
'''
import arcade
from .views.main_menu import MainMenuView
from .views.game_over import GameOverView
from .views.score_board import ScoreBoardView
from .views.victory import VictoryView


class Pacman():
    '''
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
    '''
    def __init__(self) -> None:
        self.window = arcade.Window(
            width=1280,
            height=720,
            title='PacMan',
            fullscreen=False,
            center_window=True,
            enable_polling=True
        )
        self.menu = MainMenuView()
        self.score_board = ScoreBoardView()
        self.game_over = GameOverView()
        self.victory = VictoryView()

    def view_menu(self) -> None:
        '''
            This method is called to display the
            main menu
        '''
        self.window.show_view(self.menu)

    def view_score_board(self) -> None:
        '''
            This method is called to display the
            score board
        '''
        self.window.show_view(self.score_board)

    def view_game_over(self) -> None:
        '''
            This method is called to display the
            game over screen
        '''
        self.window.show_view(self.game_over)

    def view_victory(self) -> None:
        '''
            This method is called to display the
            victory screen
        '''
        self.window.show_view(self.victory)

    def start(self) -> None:
        '''
            This method is called to start the arcade
            and to display the main menu
        '''
        self.window.show_view(self.menu)
        arcade.run()
