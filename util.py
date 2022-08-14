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


colors = [RED, MAGENTA, VIOLET, BLUE, CYAN, GREEN]

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
                if commas:
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


def dice_table(l, scale = 1, col_widths = None):
    objects = []
    for i, die in enumerate(l):
        objects.append(r"{{" + string.ascii_uppercase[i] + r": }}")
        for j in range(len(die)):
            objects.append(r"{{" + str(die[j]) + r"}}")

    group = VGroup(*[Tex(s, color=text_color).scale(scale) for s in objects])
    group.arrange_in_grid(rows=len(l), cell_alignment=RIGHT, buff=MED_SMALL_BUFF*scale, col_widths = col_widths, col_alignments="c"*(len(l[0])+1))

    return group


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

        anims = []
        for i, (name, pos) in enumerate(zip(counter_names, positions)):
            counter = Integer(
                    number = 0,
                    color = colors[i]
                ).move_to(
                    pos
                )
            counter_title = Tex(
                name,
                color = colors[i]
            ).move_to(counter.get_center()).next_to(counter, DOWN)

            #tracker = ValueTracker(0)

            self.counters.append(counter)
            self.counter_titles.append(counter_title)
            
            anims.append(AnimationGroup(
                Write(counter),
                Write(counter_title),
            ))

        scene.play(
            AnimationGroup(*anims, lag_ratio=0.15)
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

    def write(self, scene, pos_ = None, sep = default_sep, center = True, scale = 1, do = True, run_time=1.0):
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
        if do:
            scene.play(
                AnimationGroup(
                    *[FadeIn(l) for l in self.letters],
                ),
                run_time = run_time
            )

    def create_from_list_of_letters(self, letters):
        self.letters = letters
        self.str = ""
        for l in self.letters:
            self.str += l.get_tex_string()
        self.counters = []
        self.counter_titles = []

    def find_pairs(self, scene, match_set, ranges = [None, None], highlight_color = None, flying_color = text_color):
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
                        flying_letter1 = self.letters[i].copy().set_color(colors[mi])
                        flying_letter2 = self.letters[j].copy().set_color(colors[mi])

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
                        scene.add_sound(random_click_file())
                        scene.play(
                            AnimationGroup(
                                *anims,
                                run_time = 0.5
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

    def find_triplets(
        self, scene, match_set, ranges = [None, None, None], scale = 1, cheap_after_steps = None, skip_factor = 1, flying_color = text_color,
        sec_per_step_1=0.3, sec_per_step_2=0.15, anims_list = None, sound_good = None
    ):
        underscore1 = Line(start = -0.1*RIGHT + under_shift, end = 0.1*RIGHT + under_shift, color = text_color)
        underscore2 = underscore1.copy()
        underscore3 = underscore1.copy()
        #anims = []
        beg = True
        if ranges[0] == None:
            ranges = [[0, len(self.str)], [0, len(self.str)], [0, len(self.str)]]
        cnt = 0
        skip_cnt = 0
        fst_cheap = True
        counter_changes_to_do = [0] * len(self.counters)
        lasti, lastj, lastk = 0,0,0
        for i in range(ranges[0][0], ranges[0][1]):
            for j in range(max(i+1, ranges[1][0]), ranges[1][1]):
                for k in range(max(j+1, ranges[2][0]), ranges[2][1]):
                    for mi in match_set:
                        if self.str[i] == self.counter_letters[mi][0] and self.str[j] == self.counter_letters[mi][1] and self.str[k] == self.counter_letters[mi][2]:
                            play_anim = False
                            run_time_current = sec_per_step_1
                            counter_changes_to_do[mi] += 1
                            lasti, lastj, lastk = i,j,k

                            if cheap_after_steps == None or cheap_after_steps > cnt:
                                play_anim = True
                                
                            else: #cheap steps, only with probability prob
                                # if fst_cheap == True:
                                #     fst_cheap = False
                                #     scene.play(
                                #         Uncreate(underscore2),
                                #         Uncreate(underscore3)
                                #     )
                                run_time_current = sec_per_step_2
                                skip_cnt += 1
                                if skip_cnt == skip_factor:
                                    play_anim = True

                            if play_anim:
                                skip_cnt = 0

                                if beg:
                                    underscore1.move_to(self.letters[i].get_center() + under_shift * scale)
                                    underscore2.move_to(self.letters[j].get_center() + under_shift * scale)
                                    underscore3.move_to(self.letters[k].get_center() + under_shift * scale)
                                    scene.play(
                                        AnimationGroup(
                                            Create(underscore1),
                                            Create(underscore2),
                                            Create(underscore3)
                                        ),
                                        run_time = 0.2 * run_time_current
                                    )
                                    beg = False
                                else:
                                    scene.play(
                                        AnimationGroup(
                                            underscore1.animate.move_to(self.letters[i].get_center() + under_shift * scale),
                                            underscore2.animate.move_to(self.letters[j].get_center() + under_shift * scale),
                                            underscore3.animate.move_to(self.letters[k].get_center() + under_shift * scale),
                                            run_time = 0.2 * run_time_current
                                        )
                                    )

                                if cnt == 9 and anims_list != None:
                                    scene.wait()
                                    for anims in anims_list:
                                        scene.play(*anims)
                                        scene.wait()


                                flying_letter1 = self.letters[i].copy().set_color(colors[mi])
                                flying_letter2 = self.letters[j].copy().set_color(colors[mi])
                                flying_letter3 = self.letters[k].copy().set_color(colors[mi])
                                end_dot = Dot(radius = 0.00, color = background_color).move_to(self.counters[mi].get_center())
                                scene.add_sound(random_click_file())
                                scene.play(
                                    AnimationGroup(
                                        *[self.counters[it].animate.increment_value(counter_changes_to_do[it]) for it in range(len(self.counters))],
                                        Transform(flying_letter1, end_dot),
                                        Transform(flying_letter2, end_dot),
                                        Transform(flying_letter3, end_dot),
                                        run_time = run_time_current
                                    )
                                )
                                counter_changes_to_do = [0]*len(self.counters)
                            cnt += 1
        if counter_changes_to_do != [0]*len(self.counters):
            anims = []
            for it in range(len(self.counters)):
                anims.append(
                    self.counters[it].animate.increment_value(counter_changes_to_do[it])
                )

            anims += [
                underscore1.animate.move_to(self.letters[lasti].get_center() + under_shift * scale),
                underscore2.animate.move_to(self.letters[lastj].get_center() + under_shift * scale),
                underscore3.animate.move_to(self.letters[lastk].get_center() + under_shift * scale),
            ]

            scene.play(*anims, run_time=run_time_current)
            scene.wait()

        # if beg == False:
        #     if sound_good == "good":
        #         scene.add_sound(f"audio/polylog_succes.wav")
        #     if sound_good == "bad":
        #         scene.add_sound(f"audio/polylog_failure.wav")
        #     scene.play(
        #         Uncreate(underscore1),
        #         Uncreate(underscore2),
        #         Uncreate(underscore3),
        #     )

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

    def animated_permute(self, scene, perm_list, scale = 1, run_time=1.0):
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
            run_time = run_time
        )
    
    def copy(self):
        return FairString(self.str, self.letters[0])
         
    def animate_shift(self, scene, shft):
        scene.play(
            *[l.animate.shift(shft) for l in self.letters],
        )

    def animate_shift_rescale(self, scene, shft, scale, sep, run_time = 1):
        for i in range(len(self.letters)):
            self.letters[i].generate_target()
            self.letters[i].target.scale(scale)
            if i == 0:
                self.letters[i].target.shift(shft)
            else:
                self.letters[i].target.move_to(self.letters[i-1].target.get_center() + sep * RIGHT)

        scene.play(
            *[MoveToTarget(l) for l in self.letters],
            run_time = run_time
        )
    
    def add(self, sp):
        self.letters += sp.letters
        self.str += sp.str


def random_click_file():
	return f"audio/click/click_{random.randint(0, 3)}.wav"


def random_pop_file():
	return f"audio/pop/pop_{random.randint(0, 6)}.wav"


def random_whoosh_file():
	return f"audio/whoosh/whoosh_{random.randint(0, 3)}.wav"


def create_bubble(pos, scale = 1.0, color = text_color, length_scale = 1):
    scale = scale / 200.0
    pos = np.array(pos) - np.array([489.071, 195.644, 0.0])*scale
    ret_objects = []

    c1 = Circle(
        radius = 28.5689 * scale,
        color = color
    ).move_to(np.array([489.071, 195.644, 0.0])*scale).shift(pos + 0.3*UP)
    print(c1.get_center())

    c2 = Circle(
        radius = 39.7392 * scale,
        color = color
    ).move_to(np.array([409.987, 274.728, 0.0])*scale).shift(pos + 0.15*UP)
    ret_objects += [c1, c2]

    pnts = [
        (373.367*RIGHT +  366.776 * UP) * scale + pos,
        (503.717*RIGHT +  453.873 * UP) * scale + pos,
        (464.612*RIGHT +  613.847 * UP) * scale + pos,
        (340.78*RIGHT +  643.472 * UP) * scale + pos,
        (131.628*RIGHT +  596.072 * UP) * scale + pos,
        (174.288*RIGHT +  388.106 * UP) * scale + pos,
    ]

    center = 0*LEFT
    for i in range(len(pnts)):
        pnts[i] += (length_scale - 1)*(pnts[i] - pnts[0])[0]*RIGHT
        center += pnts[i]
    center /= len(pnts)

    angles = np.array([120, 170, 120, 120, 180, 120])*1.5707963267/90.0


    for i in range(len(pnts)):
        ret_objects.append(
            ArcBetweenPoints(pnts[i], pnts[(i+1)%len(pnts)], angle = angles[i], color = color)
        )

    return ret_objects, center


def create_cube(pos, scale = 1, color = text_color):

    scale = scale /200.0

    vec = [
        (227.927 - 235.63)*RIGHT + (489.666 - 188.085)*UP,
        (483.886 - 235.63)*RIGHT + (262.739 - 188.085)*UP,
        (122.462 - 235.63)*RIGHT + (308.362 - 188.085)*UP,
    ]
    for v in vec:
        v *= scale
        v *= 1/5.0
    pos -= (vec[0] + vec[1] + vec[2])*5.0/2

    ret_objects = []

    for spos, d1, d2 in [(pos, 0, 1), (pos, 1, 0), (pos, 0, 2), (pos, 2, 0), (pos + vec[0]*5, 1, 2), (pos + vec[0]*5, 2, 1)]:
        for i in range(6):
            ret_objects.append(
                Line(
                    start = spos + vec[d1] * i,
                    end = spos + vec[d1] * i + vec[d2]*5,
                    color = color
                )
            )

    return ret_objects