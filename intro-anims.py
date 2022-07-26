import random
import math
import numpy as np
from manim import *
from solarized import *
from functools import cmp_to_key
import copy
import itertools

import util

print(f"Util: {util.a}, {util.f(5)}")

example_dice = [
    [1, 3, 5, 7, 9, 11],
    [2, 4, 6, 8, 10, 12]
]
example_dice_str = [
    ["1", ", ", "3", ", ", "5", ", ", "7", ", ", "9", ", ", "11"],
    ["2", ", ", "4", ", ", "6", ", ", "8", ", ", "10", ", ", "12"]
]
text_color = GRAY
background_color = config.background_color

three_dice = [
    [1, 6, 8, 12, 13, 17],
    [2, 4, 9, 11, 15, 16],
    [3, 5, 7, 10, 14, 18]
]

arbitrary_dice = [
    [2, 6, 8, 13, 16, 20, 99],
    [5, 9, 11, 14, 15, 32, 99],
    [3, 5, 10, 18, 42, 47, 99]
]
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

#fstring = "ACBCAABCBABBACABCC"
equivalent_dice = [[], [], []]
fair_strings = [
"ABCBCACABCBAACBBAC",
"ABCCBABCAACBCABBAC",
"ABCCBABACCABCABBAC",
"ABCCBABACCABCBAABC",
"ABCCBACABBACBACCAB",
"ABCCABCBBAACABCCAB"
]

class DiceSquare(Scene):
    def construct(self):
        player_labels = [
            Tex("Player A die: ", color = text_color),
            Tex("Player B die: ", color = text_color)
        ]
        player_labels[0].move_to(3*LEFT)
        player_labels[1].move_to(3*RIGHT)

        dice_numbers = []
        for i in range(2):
            dice_numbers.append([])
            for j in range(len(example_dice_str[i])):
                dice_numbers[i].append(
                    Tex(example_dice_str[i][j], color = text_color)
                )
                if j == 0:
                    dice_numbers[i][j].next_to(player_labels[i], DOWN).align_to(player_labels[i], LEFT)
                else:
                    dice_numbers[i][j].next_to(dice_numbers[i][j-1], RIGHT)
                    if j %2 == 1:
                        dice_numbers[i][j].shift(0.2*DOWN + 0.2*LEFT)
                    else:
                        dice_numbers[i][j].shift(0.2*UP + 0.1*LEFT)

        self.play(
            *[FadeIn(labels) for labels in player_labels]
        )
        self.wait()
        self.play(
            AnimationGroup(
                *[FadeIn(nums) for nums in dice_numbers[0]],
                lag_ratio = 0.15
            )
        )
        self.wait()
        self.play(
            AnimationGroup(
                *[FadeIn(nums) for nums in dice_numbers[1]],
                lag_ratio = 0.15
            )
        )
        self.wait()
        bad_number = Tex("12", color = text_color).next_to(dice_numbers[0][-1], RIGHT).align_to(dice_numbers[0][-1], LEFT)
        good_number = Tex("11", color = text_color).move_to(dice_numbers[0][-1].get_center())

        self.play(
            Succession(
                Transform(dice_numbers[0][-1], bad_number),
                AnimationGroup(
                    Circumscribe(dice_numbers[0][-1], color = RED),
                    Circumscribe(dice_numbers[1][-1], color = RED)
                ),
                Transform(dice_numbers[0][-1], good_number)
            )
        )
        self.wait()

        # create a grid and move everything around

        side_length = 0.8
        horizontal_lines = []
        vertical_lines = []
        shft = 0.5*DOWN
        for i in range(7):
            horizontal_lines.append(
                Line(3*side_length*LEFT + (3-i)*side_length*UP + shft, 3*side_length*RIGHT + (3-i)*side_length*UP + shft, color = text_color),
            )
            vertical_lines.append(
                Line(3*side_length*UP + (3-i)*side_length*LEFT + shft, 3*side_length*DOWN + (3-i)*side_length*LEFT + shft, color = text_color),
            )

        anims = []
        dice_numbers_real = [[], []]
        for i in range(6):
            dice_numbers[0][2*i].generate_target()
            dice_numbers[0][2*i].target.move_to(
                (vertical_lines[i].get_top() + vertical_lines[i+1].get_top())/2
            ).shift(0.4*UP)
            anims.append(
                MoveToTarget(dice_numbers[0][2*i])
            )
            dice_numbers_real[0].append(dice_numbers[0][2*i])
        player_labels[0].generate_target()
        player_labels[0].target.next_to(horizontal_lines[0], UP).shift(0.6*UP)
        anims.append(MoveToTarget(player_labels[0]))

        for i in range(6):
            dice_numbers[1][2*i].generate_target()
            dice_numbers[1][2*i].target.move_to(
                (horizontal_lines[i].get_left() + horizontal_lines[i+1].get_left())/2
            ).shift(0.4*LEFT)
            anims.append(
                MoveToTarget(dice_numbers[1][2*i])
            )
            dice_numbers_real[1].append(dice_numbers[1][2*i])
        player_labels[1].generate_target()
        player_labels[1].target.next_to(vertical_lines[0], LEFT).shift(1*LEFT)
        anims.append(MoveToTarget(player_labels[1]))

        for i in range(5):
            anims.append(
                FadeOut(dice_numbers[0][2*i+1])
            )
            anims.append(
                FadeOut(dice_numbers[1][2*i+1])
            )

        self.play(
            *[FadeIn(line) for line in horizontal_lines],
            *[FadeIn(line) for line in vertical_lines],
            *anims
        )
        dice_numbers = dice_numbers_real
        self.wait()

        #show A<B and A>B
        squares = []
        blue_squares = []
        red_squares = []
        for i in range(6):
            squares.append([])
            for j in range(6):
                square = Square(side_length = 0.8, fill_color = RED, stroke_color = RED).move_to(
                    2.5*side_length*LEFT + 2.5*side_length*UP + shft + i*side_length*RIGHT + j * side_length * DOWN
                ).set_fill(RED, opacity=1.0).set_z_index(-100)
                if example_dice[0][i] > example_dice[1][j]:
                    square.set_color(BLUE)
                    square.set_fill(BLUE)
                    blue_squares.append(square)
                else:
                    red_squares.append(square)
                squares[i].append(square)

        AlB = Tex(r"$A< B$",color = RED).next_to(vertical_lines[-1], RIGHT).shift(1*RIGHT+0.5*UP)
        AgB = Tex(r"$A> B$",color = BLUE).next_to(vertical_lines[-1], RIGHT).shift(1*RIGHT+0.5*DOWN)

        self.play(
            *[FadeIn(square) for line in squares for square in line],
            FadeIn(AlB),
            FadeIn(AgB)
        )
        self.wait()

        for square in red_squares:
            square.set_z_index(-50)
        self.play(
            *[Indicate(square, color = RED) for square in red_squares]
        )
        self.wait()

        for square in blue_squares:
            square.set_z_index(-20)
        self.play(
            *[Indicate(square, color = BLUE) for square in blue_squares]
        )
        self.wait()

        #One solution

        for i in [3, 4, 5]:
            dice_numbers[0][i].generate_target()
            dice_numbers[0][i].target.move_to(dice_numbers[1][i].get_center())
            dice_numbers[1][i].generate_target()
            dice_numbers[1][i].target.move_to(dice_numbers[0][i].get_center())

        self.play(
            *[MoveToTarget(num) for num in dice_numbers[0][3:6] + dice_numbers[1][3:6]],
            *[square.animate.set_color(BLUE) for square in [squares[3][3], squares[4][4], squares[5][5]]]
        )
        self.wait()

        # the other solution

        orig_positions = [
            [num.get_center() for num in dice_numbers[0]],
            [num.get_center() for num in dice_numbers[1]]
        ]
        

        dice_numbers_sorted = list(itertools.chain(*zip(dice_numbers[0], dice_numbers[1])))
        for i, num in enumerate(dice_numbers_sorted):
            num.generate_target()
            if i == 0:
                num.target.move_to(6.5*LEFT + 3.3*UP)
            elif i == 6:
                num.target.move_to(dice_numbers[0][0].target.get_center()).next_to(dice_numbers[0][0].target, DOWN)
            else:
                num.target.move_to(dice_numbers_sorted[i-1].target.get_center()).next_to(dice_numbers_sorted[i-1].target, RIGHT).shift(0.2*RIGHT)

        self.play(
            *[MoveToTarget(num) for num in dice_numbers_sorted],
            *[FadeOut(square) for line in squares for square in line]
        )
        self.wait()

        self.play(
            AnimationGroup(
                dice_numbers_sorted[0].animate.move_to(orig_positions[0][0]),
                dice_numbers_sorted[1].animate.move_to(orig_positions[0][1]),
                dice_numbers_sorted[2].animate.move_to(orig_positions[0][2]),
                lag_ratio = 0.3
            )
        )
        self.wait()

        self.play(
            AnimationGroup(
                dice_numbers_sorted[3].animate.move_to(orig_positions[1][0]),
                dice_numbers_sorted[4].animate.move_to(orig_positions[1][1]),
                dice_numbers_sorted[5].animate.move_to(orig_positions[1][2]),
                dice_numbers_sorted[6].animate.move_to(orig_positions[0][3]),
                dice_numbers_sorted[7].animate.move_to(orig_positions[0][4]),
                dice_numbers_sorted[8].animate.move_to(orig_positions[0][5]),
                lag_ratio = 0.3
            )
        )
        self.wait()

        self.play(
            AnimationGroup(
                dice_numbers_sorted[9].animate.move_to(orig_positions[1][3]),
                dice_numbers_sorted[10].animate.move_to(orig_positions[1][4]),
                dice_numbers_sorted[11].animate.move_to(orig_positions[1][5]),
                lag_ratio = 0.3
            )
        )
        self.wait()

        for i in range(3):
            for j in range(6):
                squares[i][j].set_color(RED)
        for i in range(3, 6):
            for j in range(6):
                squares[i][j].set_color(BLUE)

        self.play(
            *[FadeIn(square) for line in squares for square in line]
        )
        self.wait()

class Aligning(Scene):
    def construct(self):
        labels = [
            Tex("Player A:", color = text_color),
            Tex("Player B:", color = text_color),
            Tex("Player C:", color = text_color),
        ]
        labels[1].shift(5*LEFT)
        labels[0].move_to(labels[1].get_center()).next_to(labels[1], UP)
        labels[2].move_to(labels[1].get_center()).next_to(labels[1], DOWN)

        numbers = []
        for i in range(3):
            numbers.append([])
            for j in range(6):
                numbers[i].append(
                    Tex(arbitrary_dice[i][j], color = text_color)
                )
                if j == 0:
                    numbers[i][j].next_to(labels[i], RIGHT).shift(4*RIGHT)
                else:
                    numbers[i][j].next_to(numbers[i][j-1], RIGHT).shift(0.3*RIGHT)
        
        self.play(
            *[FadeIn(lab) for lab in labels],
            *[FadeIn(num) for nums in numbers for num in nums],
        )
        self.wait()

        iss = [0, 0, 0]
        anims = []
        numbers_sorted = []
        for it in range(18):
            act_vals = [arbitrary_dice[0][iss[0]], arbitrary_dice[1][iss[1]], arbitrary_dice[2][iss[2]]]
            act = act_vals.index(min(*act_vals))
            target = Tex(str(it+1), color = text_color).next_to(labels[act], RIGHT).shift(0.55*RIGHT*it)
            anims.append(
                Transform(numbers[act][iss[act]], target)
            )
            equivalent_dice[act].append(it+1)
            numbers_sorted.append(numbers[act][iss[act]])
            iss[act] += 1
        self.play(
            AnimationGroup(
                *anims,
                lag_ratio = 0.3
            )
        )
        self.wait()

        #change numbers to letters
        anims = []
        lets = ["A", "B", "C"]
        for i in range(3):
            for j in range(6):
                anims.append(
                    Transform(
                        numbers[i][j],
                        Tex(lets[i], color = text_color).move_to(numbers[i][j].get_center())
                    )
                )

        self.play(
            Succession(
                AnimationGroup(
                    *[FadeOut(lab) for lab in labels],
                ),
                AnimationGroup(
                    *anims[0:6],
                ),
                AnimationGroup(
                    *anims[6:12],
                ),
                AnimationGroup(
                    *anims[12:18]
                )
            )
        )
        self.play(
            Succession(
                AnimationGroup(
                    *[num.animate.shift((num.get_center()[1] - numbers[1][0].get_center()[1])*DOWN) for num in numbers[0]]
                ),
                AnimationGroup(
                    *[num.animate.shift((num.get_center()[1] - numbers[1][0].get_center()[1])*DOWN) for num in numbers[2]]
                ),
            )
        )
        self.wait()

        # align to the right, create equivalent dice to the left
        for i in reversed(range(len(numbers_sorted))):
            numbers_sorted[i].generate_target()
            if i == 17:
                numbers_sorted[i].target.move_to(6.9*RIGHT)
            else:
                numbers_sorted[i].target.next_to(numbers_sorted[i+1].target, LEFT).shift(0.15*RIGHT)


        self.play(
            *[MoveToTarget(num) for num in numbers_sorted]
        )
        self.wait()

        strs = ["{{A: }}", "{{B: }}", "{{C: }}"]
        dice_labels = []
        for i in range(3):
            for j in range(6):
                strs[i] += "{{" + str(equivalent_dice[i][j]) + "}}"
                if j != 5:
                    strs[i] += str("{{, }}")
            dice_labels.append(Tex(strs[i], color = text_color))
        dice_labels[1].next_to(Dot().move_to(7.1*LEFT), RIGHT)
        dice_labels[0].align_to(dice_labels[1], LEFT).next_to(dice_labels[1], UP)
        dice_labels[2].align_to(dice_labels[1], LEFT).next_to(dice_labels[1], DOWN)

        lrarrow = Tex("$\longleftrightarrow$", color = text_color).shift(1.35*LEFT)
        self.play(
            *[FadeIn(lab) for lab in dice_labels],
            FadeIn(lrarrow)
        )
        self.wait()

        # highlighting one triplet
        rec_highlights = [
            Rectangle(color = RED, height = 0.5, width = 0.5).move_to(lab.get_center())
            for lab in [dice_labels[0][5], dice_labels[1][11], dice_labels[2][1]]
        ]
        above_note = Tex("$6^3 = 216$ possibilities", color = text_color).next_to(dice_labels[0], UP).shift(0.5*UP)
        self.play(
            Create(above_note)
        )
        self.wait()

        self.play(
            Succession(
                Create(rec_highlights[0]),
                Create(rec_highlights[1]),
                Create(rec_highlights[2]),
            )
        )

        self.wait()
        
        rec_highlights2 = [
            Rectangle(color = RED, height = 0.5, width = 0.5).move_to(numbers_sorted[it].get_center())
            for it in [6-1, 2-1, 16-1]            
        ]
        self.play(
            Succession(
                Create(rec_highlights2[0]),
                Create(rec_highlights2[1]),
                Create(rec_highlights2[2]),
            )
        )
        self.wait()
        
        note = Tex(r"$\textrm{C} < \textrm{A} < \textrm{B}$", color = text_color).next_to(dice_labels[2], DOWN).shift(0.3*DOWN)
        shft = 1*DOWN
        AA = Tex("A", color = text_color).next_to(numbers_sorted[6-1], DOWN).shift(shft)
        BB = Tex("B", color = text_color).next_to(numbers_sorted[16-1], DOWN).shift(shft)
        CC = Tex("C", color = text_color).next_to(numbers_sorted[2-1], DOWN).shift(shft)
        self.play(
            FadeIn(note)
        )
        self.play(
            AnimationGroup(
                FadeIn(CC),
                FadeIn(AA),
                FadeIn(BB),
                lag_ratio = 0.3
            )
        )
        self.wait()

        self.play(
            FadeOut(above_note),
            *[FadeOut(rec) for rec in rec_highlights + rec_highlights2],
            FadeOut(lrarrow),
            *[FadeOut(str) for str in dice_labels],
            FadeOut(note),
            *[FadeOut(l) for l in [AA, BB, CC]],
            *[num.animate.shift((numbers_sorted[0].get_center() + numbers_sorted[17].get_center())/2*LEFT+1*UP) for num in numbers_sorted]
        )
        self.wait()

        #TODO add buckets

        #create underscores and fly letters away
        underscores = [
            Tex(r"\_", color = text_color).next_to(num, DOWN).shift(0.2*UP).scale(1.5)
            for num in numbers_sorted
        ]
        print(underscores)

        self.play(
            *[FadeIn(score) for score in underscores]
        )
        self.wait()
        

        b_pos = 2.5*UP
        a_pos = b_pos + 4*LEFT
        c_pos = b_pos + 4*RIGHT
        seph = 0.5*RIGHT
        sepv = 0.4*DOWN

        self.play(
            numbers_sorted[0].animate.move_to(a_pos - seph/2 + 0*seph + 0*sepv),
            numbers_sorted[1].animate.move_to(c_pos - seph/2 + 0*seph + 0*sepv),
            numbers_sorted[2].animate.move_to(b_pos - seph/2 + 0*seph + 0*sepv),
            numbers_sorted[3].animate.move_to(c_pos - seph/2 + 1*seph + 0*sepv),
            numbers_sorted[4].animate.move_to(a_pos - seph/2 + 1*seph + 0*sepv),
            numbers_sorted[5].animate.move_to(a_pos - seph/2 + 2*seph + 0*sepv),
            numbers_sorted[6].animate.move_to(b_pos - seph/2 + 1*seph + 0*sepv),
            numbers_sorted[7].animate.move_to(c_pos - seph/2 + 2*seph + 0*sepv),
            numbers_sorted[8].animate.move_to(b_pos - seph/2 + 2*seph + 0*sepv),
            numbers_sorted[9].animate.move_to(a_pos - seph/2 + 0*seph + 1*sepv),
            numbers_sorted[10].animate.move_to(b_pos - seph/2 + 0*seph + 1*sepv),
            numbers_sorted[11].animate.move_to(b_pos - seph/2 + 1*seph + 1*sepv),
            numbers_sorted[12].animate.move_to(a_pos - seph/2 + 1*seph + 1*sepv),
            numbers_sorted[13].animate.move_to(c_pos - seph/2 + 0*seph + 1*sepv),
            numbers_sorted[14].animate.move_to(a_pos - seph/2 + 2*seph + 1*sepv),
            numbers_sorted[15].animate.move_to(b_pos - seph/2 + 2*seph + 1*sepv),
            numbers_sorted[16].animate.move_to(c_pos - seph/2 + 1*seph + 1*sepv),
            numbers_sorted[17].animate.move_to(c_pos - seph/2 + 2*seph + 1*sepv),
        )
        self.wait()

        #letters fly back
        new_a_pos = [0, 3, 4, 6, 9, 14]
        new_b_pos = [5, 8, 10, 11, 15, 17]
        new_c_pos = [1, 2, 7, 12, 13, 16]

        comp1 = Tex("${18 \choose 6}$", color = text_color).move_to(2*LEFT + 2*DOWN)
        comp2 = Tex("$\cdot {12 \choose 6}$", color = text_color).next_to(comp1, RIGHT)
        comp3 = Tex("$\cdot1$", color = text_color).next_to(comp2, RIGHT)
        comp4 = Tex("$=  17\,153\,136$", color = text_color).next_to(comp3, RIGHT)

        #A        
        shft = 0.3*UP
        self.play(
            *[numbers_sorted[pos - 1].animate.move_to(underscores[new_pos].get_center()).shift(shft) for (pos, new_pos) in zip(equivalent_dice[0], new_a_pos)],
            FadeIn(comp1)
        )
        self.wait()

        #B
        self.play(
            *[numbers_sorted[pos - 1].animate.move_to(underscores[new_pos].get_center()).shift(shft) for (pos, new_pos) in zip(equivalent_dice[1], new_b_pos)],
            FadeIn(comp2)
        )
        self.wait()

        #C
        self.play(
            *[numbers_sorted[pos - 1].animate.move_to(underscores[new_pos].get_center()).shift(shft) for (pos, new_pos) in zip(equivalent_dice[2], new_c_pos)],
            FadeIn(comp3)
        )
        self.wait()
        self.play(
            FadeIn(comp4)
        )
        self.play(
            *[FadeOut(obj) for obj in self.mobjects]
        )

class Aligning2(Scene):
    def construct(self):
        self.next_section(skip_animations=True)
        fairs_strs = [
            Tex(s, color = text_color)
            for s in fair_strings
        ]
        fairs_strs[0].shift(2*UP)
        for i in range(1, 6):
            fairs_strs[i].next_to(fairs_strs[i-1], DOWN)
        self.play(
            AnimationGroup(
                *[FadeIn(str) for str in fairs_strs],
                lag_ratio = 0.3
            )
        )
        self.wait()  
        msg = Tex("(up to permuting the letters in the string or writing it backwards)", color = text_color).move_to(3.5*DOWN).scale(0.8)
        self.play(
            FadeIn(msg)
        )    
        self.wait()
        self.play(
            *[FadeOut(o) for o in self.mobjects]
        )
        self.wait()

        #TODO strings for four players
        self.next_section(skip_animations=False)

        #TODO back to three players

        eq1 = Tex("$5! \mid $", color = text_color).move_to(2*DOWN + 0.3*LEFT)
        eq2 = Tex("$s^5$", color = text_color).next_to(eq1, RIGHT)

        self.play(
            FadeIn(eq2)
        )
        self.wait()



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