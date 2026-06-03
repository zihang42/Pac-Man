'''
    various sprites utils
    like the sprites list
'''
#from enum import Enum


class SpritesStock():
    def __init__(self):
        self.paths_dict = [
            {
                "name":         "items",
                "path":         ":sprites-characters:items.png",
                "frame_count":   6,
                "frame_size":    (122, 122),
                "position":      (300, 100)
            },
            {
                "name":         "bluewhite_ghost",
                "path":         ":sprites-characters:bluewhite_ghost.png",
                "frame_count":   4,
                "frame_size":    (125, 122),
                "position":      (100, 100)
            },
            {
                "name":         "dead_ghost",
                "path":         ":sprites-characters:dead_ghost.png",
                "frame_count":   4,
                "frame_size":    (125, 122),
                "position":      (500, 100)
            },
            {
                "name":         "cyan_ghost",
                "path":         ":sprites-characters:cyan_ghost.png",
                "frame_count":   8,
                "frame_size":    (100, 101),
                "position":      (700, 100)
            },
            {
                "name":         "orange_ghost",
                "path":         ":sprites-characters:orange_ghost.png",
                "frame_count":   8,
                "frame_size":    (100, 101),
                "position":      (900, 100)
            },
            {
                "name":         "pink_ghost",
                "path":         ":sprites-characters:pink_ghost.png",
                "frame_count":   8,
                "frame_size":    (101, 103),
                "position":      (100, 300)
            },
            {
                "name":         "red_ghost",
                "path":         ":sprites-characters:red_ghost.png",
                "frame_count":   8,
                "frame_size":    (101, 103),
                "position":      (300, 300)
            },
            {
                "name":         "pacman_down",
                "path":         ":sprites-characters:pacman_down.png",
                "frame_count":   2,
                "frame_size":    (101, 90),
                "position":      (500, 300)
            },
            {
                "name":         "pacman_left",
                "path":         ":sprites-characters:pacman_left.png",
                "frame_count":   2,
                "frame_size":    (101, 90),
                "position":      (700, 300)
            },
            {
                "name":         "pacman_right",
                "path":         ":sprites-characters:pacman_right.png",
                "frame_count":   2,
                "frame_size":    (101, 90),
                "position":      (900, 300)
            },
            {
                "name":         "pacman_up",
                "path":         ":sprites-characters:pacman_up.png",
                "frame_count":   2,
                "frame_size":    (101, 90),
                "position":      (100, 500)
            },
            {
                "name":         "pacman_death",
                "path":         ":sprites-characters:pacman_death.png",
                "frame_count":   12,
                "frame_size":    (79, 80),
                "position":      (300, 500)
            }
        ]
        self.walls_path = [
            ":sprites-walls:left_border_wall.png",
            ":sprites-walls:lower_border_wall.png",
            ":sprites-walls:right_border_wall.png",
            ":sprites-walls:upper_border_wall.png",

            ":sprites-walls:lower_left_angle.png",
            ":sprites-walls:lower_right_angle.png",
            ":sprites-walls:upper_left_angle.png",
            ":sprites-walls:upper_right_angle.png",

            ":sprites-walls:lower_left_corner.png",
            ":sprites-walls:lower_right_corner.png",
            ":sprites-walls:upper_right_corner.png",
            ":sprites-walls:upper_left_corner.png",

            ":sprites-walls:lower_wall.png",
            ":sprites-walls:left_wall.png",
            ":sprites-walls:right_wall.png",
            ":sprites-walls:upper_wall.png",

            ":sprites-walls:upper_left_angle_border.png",
            ":sprites-walls:upper_right_angle_border.png",
            ":sprites-walls:lower_left_angle_border.png",
            ":sprites-walls:lower_right_angle_border.png",
        ]

