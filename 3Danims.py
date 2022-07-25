import random
import math
import numpy as np
from manim import *
#from solarized import *
from functools import cmp_to_key
import copy
import itertools

# pro testovani
dice = [
    [1, 2, 9],
    [4, 5, 7],
    [3, 6, 8]
]
# ferova kostka ABCBCA CABCBA ACBBAC
dice = [
    [1, 6, 8, 12, 13, 17],
    [2, 4, 9, 11, 15, 16],
    [3, 5, 7, 10, 14, 18]
]

VIOLET = BLUE
MAGENTA = BLUE
colors = [GREEN, TEAL, BLUE, VIOLET, MAGENTA, RED, ORANGE] # TODO restrict to 6 colors

class DiceCube(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi = 45*DEGREES, theta = -45*DEGREES)
        axes = ThreeDAxes(x_range = [0, 5, 1], y_range = [0, 5, 1], z_range = [0, 5, 1]).add_coordinates()
        #self.add(axes)
        base = Cube(side_length = 1).move_to(ORIGIN)
        # self.add(
        #     base,
        #     Cube(side_length = 1, fill_color = RED).move_to(ORIGIN).shift(1*LEFT),
        #     Cube(side_length = 1, fill_color = BLUE).move_to(ORIGIN).shift(1*UP),
        #     Cube(side_length = 1, fill_color = GREEN).move_to(ORIGIN).shift(1*OUT)
        # )

        labels = []
        nexts = [RIGHT, DOWN, RIGHT + DOWN + OUT]
        dirs = [UP, LEFT, OUT]
        for i in range(3):
            labels.append([])
            for j in range(len(dice[i])):
                l = Tex(str(dice[i][j]))
                if i == 1:
                    l.rotate_about_origin(90*DEGREES,OUT)
                if i == 2:
                    l.rotate_about_origin(45*DEGREES, OUT).rotate_about_origin(90*DEGREES, RIGHT-DOWN)
                
                if j == 0:
                    labels[i].append(
                        l.move_to(base.get_center()).next_to(base, nexts[i]).shift(0.5*nexts[i])
                    )   
                else:
                    labels[i].append(
                        l.move_to(labels[i][j-1].get_center() + dirs[i])
                    )
        self.add(
            *labels[0],
            *labels[1],
            *labels[2]
        )
    
        # self.add(
        #     Tex("right").move_to(base.get_center()).next_to(base, RIGHT),
        #     Tex("down").rotate_about_origin(90*DEGREES,OUT).move_to(base.get_center()).next_to(base, DOWN),
        #     Tex("out").rotate_about_origin(45*DEGREES, OUT).rotate_about_origin(90*DEGREES, RIGHT-DOWN).move_to(base.get_center()).next_to(base, RIGHT + DOWN + OUT),
        # )

        self.begin_ambient_camera_rotation(
            rate = PI/10,
            about = "theta"
        )

        for it, perm in enumerate(itertools.permutations([0, 1, 2])):
            cubes_to_appear = []            
            for i in range(len(dice[0])):
                for j in range(len(dice[1])):
                    for k in range(len(dice[2])):
                        vals = [dice[0][i], dice[1][j], dice[2][k]]
                        perm_vals = [vals[perm[0]], vals[perm[1]], vals[perm[2]]]
                        if perm_vals == sorted(perm_vals):
                            cubes_to_appear.append(
                                Cube(
                                    side_length=1,
                                    fill_color = colors[it]
                                ).move_to(ORIGIN).shift(i*dirs[0]+j*dirs[1]+k*dirs[2])
                            )
            if cubes_to_appear != []:
                self.add(
                    *cubes_to_appear
                )
                self.wait()
                self.remove(
                    *cubes_to_appear
                )
                self.wait()
                # self.play(
                #     *[FadeIn(cube) for cube in cubes_to_appear]
                # )
                # self.play(
                #     *[FadeOut(cube) for cube in cubes_to_appear]
                # )
        self.stop_ambient_camera_rotation()
        