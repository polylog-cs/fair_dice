import random
import math
import numpy as np
from manim import *
from solarized import *
from functools import cmp_to_key
import copy
import itertools
import string

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

four_dice = [
    [3, 4, 13, 14, 20, 21, 28, 29, 35, 36, 45, 46],
    [7, 8, 9, 10, 17, 18, 31, 32, 39, 40, 41, 42],
    [1, 6, 11, 16, 23, 24, 25, 26, 33, 38, 43, 48],
    [2, 5, 12, 15, 19, 22, 27, 30, 34, 37, 44, 47],
]

colors = [GREEN, CYAN, BLUE, VIOLET, MAGENTA, RED, ORANGE] # TODO restrict to 6 colors
text_color = GRAY
background_color = config.background_color


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

fair_strings4 = [
    "????????????????"
]

def string_to_list(str):
    l = []
    for _ in range(len(set(str))):
        l.append([])
    for i in range(len(str)):
        l[ord(str[i]) - ord('A')].append(i+1)
    return l

def list_to_string(dice):
    l = []
    for die, let in zip(dice, string.ascii_uppercase):
        l += list(zip(die, [let]*len(die)))
    l.sort()
    str = ""
    for _, let in l:
        str += let
    return str

def list_to_lines(l, pos = 0*LEFT, scale = 1, commas = True):
    lines = []
    for i, die in enumerate(l):
        s = r"{{" + string.ascii_uppercase[i] + r": }}"
        for j in range(len(die)):
            s += r"{{" + str(die[j]) + r"}}"
            if j != len(die)-1:
                if commas == True:
                    s += r"{{, }}"
                else:
                    s += r"{{ }}"
        lines.append(
            Tex(s, color = text_color).scale(scale)
        )
        if i == 0:
            lines[i].move_to(pos)
        else:
            lines[i].next_to(lines[i-1], DOWN).align_to(lines[i-1], LEFT)
    return lines

def rotate(vec, angle):
    return [
        vec[0]*np.cos(angle) - vec[1]*np.sin(angle),
        vec[0]*np.sin(angle) + vec[1]*np.cos(angle)
    ]

under_shift = 0.3* DOWN
over_shift = 0.3*UP
default_sep = 0.4


class FairBase:
    def create_counters(self, scene, counter_names, counter_letters):
        positions = [(2*(i+0.5))*RIGHT + 2*DOWN for i in range(-3, 3)]
        self.counter_letters = counter_letters

        for i, (name, pos) in enumerate(zip(counter_names, positions)):
            counter = Integer(
                    number = 0,
                    color = text_color
                ).move_to(
                    pos
                )
            counter_title = Tex(
                name,
                color = text_color
            ).move_to(counter.get_center()).next_to(counter, DOWN)

            #tracker = ValueTracker(0)

            self.counters.append(counter)
            self.counter_titles.append(counter_title)
            

            scene.play(
                Write(counter),
                Write(counter_title)
            )

    def clear_counters(self, scene):
        scene.play(
            *[counter.animate.set_value(0) for counter in self.counters]
        )
        
    def delete_counters(self, scene):
        scene.play(
            *[FadeOut(counter) for counter in self.counters],
            *[FadeOut(counter_title) for counter_title in self.counter_titles]
        )
        self.counters = []
        self.counter_titles = []


class FairString(FairBase):
    def __init__(self, str_, pos_ = 0*LEFT):
        self.str = str_
        self.letters = [
            Tex(l, color = text_color)
            for l in self.str
        ]
        self.counters = []
        self.counter_titles = []

    def write(self, scene, pos_ = None, sep = default_sep, center = True, scale = 1):
        if pos_ is None:
            pos_ = self.letters[0].get_center()        

        for i, l in enumerate(self.letters):
            l.scale(scale)
            if i == 0:
                l.move_to(pos_)
            else:
                l.move_to(self.letters[i-1].get_center() + sep * scale * RIGHT)
        
        if center == True:
            off = (self.letters[0].get_center() + self.letters[len(self.letters) - 1].get_center())/2
            for l in self.letters:
                l.shift(off * LEFT)

        scene.play(
            AnimationGroup(
                *[FadeIn(l) for l in self.letters],
            ),
            run_time = 0.1
        )

    def create_from_list_of_letters(self, letters):
        self.letters = letters
        self.str = ""
        for l in self.letters:
            self.str += l.get_tex_string()
        self.counters = []
        self.counter_titles = []

    def find_pairs(self, scene, match_set, ranges = [None, None], highlight_color = None):
        underscore1 = Line(start = -0.1*RIGHT + under_shift, end = 0.1*RIGHT + under_shift, color = text_color)
        underscore2 = underscore1.copy()
        #anims = []
        beg = True
        if ranges[0] == None:
            ranges = [[0, len(self.str)], [0, len(self.str)]]
        cleanup_anims = []

        for i in range(ranges[0][0], ranges[0][1]):
            for j in range(max(i+1, ranges[1][0]), ranges[1][1]):
                for mi in match_set:
                    if self.str[i] == self.counter_letters[mi][0] and self.str[j] == self.counter_letters[mi][1]:
                        if beg == True:
                            underscore1.move_to(self.letters[i].get_center() + under_shift)
                            underscore2.move_to(self.letters[j].get_center() + under_shift)
                            scene.play(
                                AnimationGroup(
                                    Create(underscore1),
                                    Create(underscore2)
                                ),
                                run_time = 0.1
                            )
                            beg = False
                        else:
                            scene.play(
                                AnimationGroup(
                                    underscore1.animate.move_to(self.letters[i].get_center() + under_shift),
                                    underscore2.animate.move_to(self.letters[j].get_center() + under_shift),
                                    run_time = 0.1
                                )
                            )
                        flying_letter1 = self.letters[i].copy()
                        flying_letter2 = self.letters[j].copy()
                        end_dot = Dot(radius = 0.00, color = background_color).move_to(self.counters[mi].get_center())
                        anims = [
                            self.counters[mi].animate.increment_value(1),
                            Transform(flying_letter1, end_dot),
                            Transform(flying_letter2, end_dot),
                        ]
                        if highlight_color != None:
                            anims += [
                                self.letters[i].animate.set_color(highlight_color),
                                self.letters[j].animate.set_color(highlight_color)
                            ]
                        scene.play(
                            AnimationGroup(
                                *anims,
                                run_time = 1
                            )
                        )
                        if highlight_color != None:
                            cleanup_anims += [
                                self.letters[i].animate.set_color(text_color),
                                self.letters[j].animate.set_color(text_color)
                            ]

        if beg == False:
            scene.play(
                Uncreate(underscore1),
                Uncreate(underscore2),
                run_time = 0.1
            )
        return cleanup_anims

    def find_triplets(self, scene, match_set, ranges = [None, None, None], scale = 1, cheap_after_steps = None, prob = 1):
        underscore1 = Line(start = -0.1*RIGHT + under_shift, end = 0.1*RIGHT + under_shift, color = text_color)
        underscore2 = underscore1.copy()
        underscore3 = underscore1.copy()
        #anims = []
        beg = True
        if ranges[0] == None:
            ranges = [[0, len(self.str)], [0, len(self.str)], [0, len(self.str)]]
        cnt = 0
        fst_cheap = True
        counter_changes_to_do = [0] * len(self.counters)

        for i in range(ranges[0][0], ranges[0][1]):
            for j in range(max(i+1, ranges[1][0]), ranges[1][1]):
                for k in range(max(j+1, ranges[2][0]), ranges[2][1]):
                    for mi in match_set:
                        if self.str[i] == self.counter_letters[mi][0] and self.str[j] == self.counter_letters[mi][1] and self.str[k] == self.counter_letters[mi][2]:
                            if cheap_after_steps == None or cheap_after_steps > cnt:
                                if beg == True:
                                    underscore1.move_to(self.letters[i].get_center() + under_shift * scale)
                                    underscore2.move_to(self.letters[j].get_center() + under_shift * scale)
                                    underscore3.move_to(self.letters[k].get_center() + under_shift * scale)
                                    scene.play(
                                        AnimationGroup(
                                            Create(underscore1),
                                            Create(underscore2),
                                            Create(underscore3)
                                        ),
                                        run_time = 0.1
                                    )
                                    beg = False
                                else:
                                    scene.play(
                                        AnimationGroup(
                                            underscore1.animate.move_to(self.letters[i].get_center() + under_shift * scale),
                                            underscore2.animate.move_to(self.letters[j].get_center() + under_shift * scale),
                                            underscore3.animate.move_to(self.letters[k].get_center() + under_shift * scale),
                                            run_time = 0.1
                                        )
                                    )
                                flying_letter1 = self.letters[i].copy()
                                flying_letter2 = self.letters[j].copy()
                                flying_letter3 = self.letters[k].copy()
                                end_dot = Dot(radius = 0.00, color = background_color).move_to(self.counters[mi].get_center())
                                scene.play(
                                    AnimationGroup(
                                        self.counters[mi].animate.increment_value(1),
                                        Transform(flying_letter1, end_dot),
                                        Transform(flying_letter2, end_dot),
                                        Transform(flying_letter3, end_dot),
                                        run_time = 1
                                    )
                                )
                            else: #cheap steps, only with probability prob
                                # if fst_cheap == True:
                                #     fst_cheap = False
                                #     scene.play(
                                #         Uncreate(underscore2),
                                #         Uncreate(underscore3)
                                #     )
                                counter_changes_to_do[mi] += 1
                                if random.random() < prob:
                                    scene.play(
                                        AnimationGroup(
                                            underscore1.animate.move_to(self.letters[i].get_center() + under_shift * scale),
                                            underscore2.animate.move_to(self.letters[j].get_center() + under_shift * scale),
                                            underscore3.animate.move_to(self.letters[k].get_center() + under_shift * scale),
                                            run_time = 0.1
                                        )
                                    )
                                    flying_letter1 = self.letters[i].copy()
                                    flying_letter2 = self.letters[j].copy()
                                    flying_letter3 = self.letters[k].copy()
                                    end_dot = Dot(radius = 0.00, color = background_color).move_to(self.counters[mi].get_center())
                                    scene.play(
                                        AnimationGroup(
                                            *[self.counters[it].animate.increment_value(counter_changes_to_do[it]) for it in range(len(self.counters))],
                                            Transform(flying_letter1, end_dot),
                                            Transform(flying_letter2, end_dot),
                                            Transform(flying_letter3, end_dot),
                                            run_time = 1
                                        )
                                    )
                                    counter_changes_to_do = [0]*len(self.counters)
                            cnt += 1
        if counter_changes_to_do != [0]*len(self.counters):
            for it in range(len(self.counters)):
                self.counters[it].increment_value(counter_changes_to_do[it])
                scene.add(self.counters[it])

        if beg == False:
            # if fst_cheap == True:
            scene.play(
                Uncreate(underscore1),
                Uncreate(underscore2),
                Uncreate(underscore3),
            )

    def delete(self, scene):
        scene.play(
            *[FadeOut(l) for l in self.letters],
            *[FadeOut(counter) for counter in self.counters],
            *[FadeOut(counter_title) for counter_title in self.counter_titles]
        )
        self.counters = []
        self.counter_titles = []

    def update_string(self):
        self.str = ""
        for l in self.letters:
            self.str += l.get_tex_string()

    def reorganize_by_left_coordinate(self):
        #change the order of letters based on their current position on the screen
        self.letters.sort(key = cmp_to_key(lambda l1, l2: l1.get_center()[0] - l2.get_center()[0]))
        self.update_string()

    def animated_permute(self, scene, perm_list, scale = 1):
        anims = []
        for i in range(len(self.letters)):
            for f, t in perm_list:
                if self.str[i] == f:
                    self.str = self.str[:i] + t + self.str[i+1:]
                    anims.append(
                        Transform(
                            self.letters[i], 
                            Tex(t, color = text_color).scale(scale).move_to(self.letters[i].get_center())
                        )
                    )
                    break
        scene.play(
            *anims,
            run_time = 0.1
        )
    
    def copy(self):
        return FairString(self.str, self.letters[0])
         
    def animate_shift(self, scene, shft):
        scene.play(
            *[l.animate.shift(shft) for l in self.letters],
        )

    def animate_shift_rescale(self, scene, shft, scale, sep):
        for i in range(len(self.letters)):
            self.letters[i].generate_target()
            self.letters[i].target.scale(scale)
            if i == 0:
                self.letters[i].target.shift(shft)
            else:
                self.letters[i].target.move_to(self.letters[i-1].target.get_center() + sep * RIGHT)

        scene.play(
            *[MoveToTarget(l) for l in self.letters],
        )
    
    def add(self, sp):
        self.letters += sp.letters
        self.str += sp.str


# class FairDice(FairBase):
#     def __init__(self, vals_, pos_ = 0*LEFT):
#         self.dice = vals_
#         self.lines = []
#         for i, die in enumerate(self.dice):
#             str = r"{{" + string.ascii_uppercase[i] + r": }}"
#             for j in len(die):
#                 str.append(r"{{" + str(j) + r"}}")
#                 if j != len(die)-1:
#                     str.append(r"{{, }}")
#             self.lines.append(
#                 Tex(str, color = text_color)
#             )
#             if i == 0:
#                 self.lines[i].move_to(pos_)
#             else:
#                 self.lines[i].next_to(self.lines[i-1], DOWN)
#         self.counters = []
#         self.counter_titles = []

#     def find_triplets(self, scene, match_set, ranges = [None, None, None], scale = 1, cheap_after_steps = None, prob = 1):
#         underscore1 = Line(start = -0.1*RIGHT + under_shift, end = 0.1*RIGHT + under_shift, color = text_color)
#         underscore2 = underscore1.copy()
#         underscore3 = underscore1.copy()
#         #anims = []
#         beg = True
#         if ranges[0] == None:
#             ranges = [[0, len(self.dice[0])], [0, len(self.dice[1])], [0, len(self.dice[2])]]
#         cnt = 0
#         fst_cheap = True
#         counter_changes_to_do = [0] * len(self.counters)

#         for i in range(ranges[0][0], ranges[0][1]):
#             for j in range(ranges[1][0], ranges[1][1]):
#                 for k in range(ranges[2][0], ranges[2][1]):
#                     if cheap_after_steps == None or cheap_after_steps > cnt:
#                         if beg == True:
#                             underscore1.move_to(self.lines[i].get_center() + under_shift * scale)
#                             underscore2.move_to(self.letters[j].get_center() + under_shift * scale)
#                             underscore3.move_to(self.letters[k].get_center() + under_shift * scale)
#                             scene.play(
#                                 AnimationGroup(
#                                     Create(underscore1),
#                                     Create(underscore2),
#                                     Create(underscore3)
#                                 ),
#                                 run_time = 0.1
#                             )
#                             beg = False
#                         else:
#                             scene.play(
#                                 AnimationGroup(
#                                     underscore1.animate.move_to(self.letters[i].get_center() + under_shift * scale),
#                                     underscore2.animate.move_to(self.letters[j].get_center() + under_shift * scale),
#                                     underscore3.animate.move_to(self.letters[k].get_center() + under_shift * scale),
#                                     run_time = 0.1
#                                 )
#                             )
#                         flying_letter1 = self.letters[i].copy()
#                         flying_letter2 = self.letters[j].copy()
#                         flying_letter3 = self.letters[k].copy()
#                         end_dot = Dot(radius = 0.00, color = background_color).move_to(self.counters[mi].get_center())
#                         scene.play(
#                             AnimationGroup(
#                                 self.counters[mi].animate.increment_value(1),
#                                 Transform(flying_letter1, end_dot),
#                                 Transform(flying_letter2, end_dot),
#                                 Transform(flying_letter3, end_dot),
#                                 run_time = 1
#                             )
#                         )
#                     else: #cheap steps, only with probability prob
#                         # if fst_cheap == True:
#                         #     fst_cheap = False
#                         #     scene.play(
#                         #         Uncreate(underscore2),
#                         #         Uncreate(underscore3)
#                         #     )
#                         counter_changes_to_do[mi] += 1
#                         if random.random() < prob:
#                             scene.play(
#                                 AnimationGroup(
#                                     underscore1.animate.move_to(self.letters[i].get_center() + under_shift * scale),
#                                     underscore2.animate.move_to(self.letters[j].get_center() + under_shift * scale),
#                                     underscore3.animate.move_to(self.letters[k].get_center() + under_shift * scale),
#                                     run_time = 0.1
#                                 )
#                             )
#                             flying_letter1 = self.letters[i].copy()
#                             flying_letter2 = self.letters[j].copy()
#                             flying_letter3 = self.letters[k].copy()
#                             end_dot = Dot(radius = 0.00, color = background_color).move_to(self.counters[mi].get_center())
#                             scene.play(
#                                 AnimationGroup(
#                                     *[self.counters[it].animate.increment_value(counter_changes_to_do[it]) for it in range(len(self.counters))],
#                                     Transform(flying_letter1, end_dot),
#                                     Transform(flying_letter2, end_dot),
#                                     Transform(flying_letter3, end_dot),
#                                     run_time = 1
#                                 )
#                             )
#                             counter_changes_to_do = [0]*len(self.counters)
#                     cnt += 1
#         if counter_changes_to_do != [0]*len(self.counters):
#             for it in range(len(self.counters)):
#                 self.counters[it].increment_value(counter_changes_to_do[it])
#                 scene.add(self.counters[it])

#         if beg == False:
#             # if fst_cheap == True:
#             scene.play(
#                 Uncreate(underscore1),
#                 Uncreate(underscore2),
#                 Uncreate(underscore3),
#             )
