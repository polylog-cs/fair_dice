import random
import math
import numpy as np
from manim import *
from solarized import *
from functools import cmp_to_key
import copy
import itertools

text_color = GRAY
background_color = config.background_color
under_shift = 0.3* DOWN
over_shift = 0.3*UP
default_sep = 0.4

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

def rotate(vec, angle):
    return [
        vec[0]*np.cos(angle) - vec[1]*np.sin(angle),
        vec[0]*np.sin(angle) + vec[1]*np.cos(angle)
    ]


class FairString:
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
                            cleanup_anims += [
                                self.letters[i].animate.set_color(text_color),
                                self.letters[j].animate.set_color(text_color)
                            ]
                        scene.play(
                            AnimationGroup(
                                *anims,
                                run_time = 1
                            )
                        )
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

    def create_buckets(self, scene, bucket_names, bucket_letters):
        positions = [(1.5*(i+0.5))*RIGHT + 2*DOWN for i in range(-3, 3)]
        self.counter_letters = bucket_letters

        for i, (name, pos) in enumerate(zip(bucket_names, positions)):
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
        
    def delete_buckets(self, scene):
        scene.play(
            *[FadeOut(bucket) for bucket in self.counters],
            *[FadeOut(bucket_title) for bucket_title in self.counter_titles]
        )
        self.counters = []
        self.counter_titles = []

    def delete(self, scene):
        scene.play(
            *[FadeOut(l) for l in self.letters],
            *[FadeOut(bucket) for bucket in self.counters],
            *[FadeOut(bucket_title) for bucket_title in self.counter_titles]
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
            run_time = 0.1
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
            run_time = 0.1
        )
    
    def add(self, sp):
        self.letters += sp.letters
        self.str += sp.str

class Construction1(Scene):
    def construct(self):
        skip = False
        self.next_section(skip_animations = skip)
        #OK, so here is how we do it. First, we really just think about the formulation of the problem with strings where we do not need to think in terms of probabilities. We just want to construct a string such that every permutation of letters occurs the same number of times in it.
        #[znovu ukázka nějakého stringu pro tři a počítání trojic] 
        s = FairString("ABCBCACABCBAACBBAC")
        s.write(self)

        if not skip:
            s.create_buckets(
                self, 
                ["\#ABC", "\#ACB", "\#BAC", "\#BCA", "\#CAB", "\#CBA"],
                [['A', 'B', 'C'], ['A', 'C', 'B'], ['B', 'A', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B'], ['C', 'B', 'A']]
            )
            self.wait()
            s.find_triplets(self, [0, 1, 2, 3, 4, 5])
            self.wait()
            s.delete_buckets(self)
            self.wait()

        #It is always good to start with something concrete so let’s look at those six solutions we found for 6-sided dice and three players. 
        #[znovu se objeví 6 řešení]
        skip = False
        self.next_section(skip_animations = skip)

        six_fair_strings = [s]
        for i in range(1, 6):
            new_s = FairString(fair_strings[i])
            new_s.letters[0].align_to(
                six_fair_strings[i-1].letters[0], LEFT
            ).next_to(
                six_fair_strings[i-1].letters[0], DOWN
            )
            new_s.write(self)
            six_fair_strings.append(new_s)
        
        self.wait()

        #The first two solutions are actually kind of interesting, because they are just the triplet ABC concatenated six times, each time with its letters permuted differently. 
        #[nechají se jen první 2 řešení, udělají se mezery po částech]
        skip = False
        self.next_section(skip_animations = skip)

        self.play(
            *[FadeOut(l) for l in six_fair_strings[2].letters],
            *[FadeOut(l) for l in six_fair_strings[3].letters],
            *[FadeOut(l) for l in six_fair_strings[4].letters],
            *[FadeOut(l) for l in six_fair_strings[5].letters]
        )

        shifts = [0]*18
        big_sep = 0.4
        for i in range(18):
            if i in range(9):
                shifts[i] = big_sep*LEFT * (1/2.0 + (2 - (i//3)))
            else:
                shifts[i] = big_sep*RIGHT * (1/2.0 + ((i//3) - 3))
        self.play(
            *[l.animate.shift(sh) for l, sh in zip(six_fair_strings[0].letters, shifts)],
            *[l.animate.shift(sh) for l, sh in zip(six_fair_strings[1].letters, shifts)]
        )
        self.wait()

        #So maybe this is the way to approach the problem? But then again, if you just take the six permutations of the triplet ABC and concatenate them in some arbitrary way, for example we reshuffle them like this, let’s compute it … no, not fair. 
        #[druhý string se ztratí a u prvního se reshufflují části, pak se spočítají trojice]

        six_fair_strings[1].delete(self)

        radius = 3
        parts = [
            *[Group(*s.letters[3*i:3*(i+1)]) for i in range(0, 6)]
        ]
        old_positions = [
            g.get_center() for g in parts
        ]
        sixgon = [
            [*rotate([radius, 0], (-2*math.pi/6.0)*(i-2)), 0]
            for i in range(6)
        ]
        self.play(
            parts[0].animate.move_to(sixgon[0]),
            parts[1].animate.move_to(sixgon[3]),
            parts[2].animate.move_to(sixgon[4]),
            parts[3].animate.move_to(sixgon[5]),
            parts[4].animate.move_to(sixgon[1]),
            parts[5].animate.move_to(sixgon[2])
        )
        self.wait()

        self.play(
            parts[0].animate.move_to(old_positions[1]),
            parts[1].animate.move_to(old_positions[2]),
            parts[2].animate.move_to(old_positions[3]),
            parts[3].animate.move_to(old_positions[4]),
            parts[4].animate.move_to(old_positions[5]),
            parts[5].animate.move_to(old_positions[0])
        )

        s.reorganize_by_left_coordinate()


        skip = False
        self.next_section(skip_animations = skip)
        if not skip:
            s.create_buckets(
                self, 
                ["\#ABC", "\#ACB", "\#BAC", "\#BCA", "\#CAB", "\#CBA"],
                [['A', 'B', 'C'], ['A', 'C', 'B'], ['B', 'A', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B'], ['C', 'B', 'A']]
            )
            self.wait()
            s.find_triplets(self, [0, 1, 2, 3, 4, 5])
            self.wait()
            s.delete_buckets(self)
            self.wait()

        self.wait()

        #Well it turns out that although we do not have the same number of all triplets, we at least have the same number of all pairs. So, let’s compute those numbers:
        #[udělají se šuplíky AB,AC,BA, BC, CA, CB, pak se spočítá]
        #Nice, they are the same. And this actually works independently on how we concatenate the permutations of the original string. 

        skip = False
        self.next_section(skip_animations = skip)
        
        s.create_buckets(
            self, 
            ["\#AB", "\#AC", "\#BA", "\#BC", "\#CA", "\#CB"],
            [['A', 'B'], ['A', 'C'], ['B', 'A'], ['B', 'C'], ['C', 'A'], ['C', 'B']]
        )
        if not skip:
            s.find_pairs(self, [0, 1, 2, 3, 4, 5])
            s.clear_counters(self)
            self.wait()

        # Why is it so? Well, let’s look at what contributes to the count of ABs and then compare it to the count of for example CAs.
        # [highlight AB, CA, pak se zresetují countery] 
        # There are two types of AB pairs. First, there are those where A is in one of the six short parts of the string and B is in another one. Whenever you take two different parts, they will generate exactly one AB pair. 
        # [nahoře ve stringu se udělají mezery mezi částmi, pak se udělá první výpočet, na nadčárami je napsáno A a B]

        skip = False
        self.next_section(skip_animations = skip)
        
        overscore1 = Line(start = -0.5*RIGHT + over_shift, end = 0.5*RIGHT + over_shift, color = text_color)
        overscore2 = overscore1.copy()
        overscore1.move_to(s.letters[1].get_center() + over_shift)
        overscore2.move_to(s.letters[1+3].get_center() + over_shift)
        overletter1 = Tex("A", color = text_color).move_to(overscore1.get_center()).next_to(overscore1, UP)
        overletter2 = Tex("B", color = text_color).move_to(overscore2.get_center()).next_to(overscore2, UP)
        
        for ind in [0, 4]:
            if ind == 4:
                overscore1.move_to(s.letters[1].get_center() + over_shift)
                overscore2.move_to(s.letters[1+3].get_center() + over_shift)
                overletter1 = Tex("C", color = text_color).move_to(overscore1.get_center()).next_to(overscore1, UP)
                overletter2 = Tex("A", color = text_color).move_to(overscore2.get_center()).next_to(overscore2, UP)
                
            #pairs from different parts
            self.next_section(skip_animations = False)
            for i in range(0, 6):
                for j in range(i+1, 6):
                    if i == 0 and j == 1:
                        self.play(
                            AnimationGroup(
                                Create(overscore1),
                                Create(overscore2),
                                Write(overletter1),
                                Write(overletter2)
                            ),
                            run_time = 0.1
                        )
                    else:
                        shft1 = s.letters[i*3+1].get_center() + over_shift - overscore1.get_center()
                        shft2 = s.letters[j*3+1].get_center() + over_shift - overscore2.get_center()
                        self.play(
                            AnimationGroup(
                                overscore1.animate.shift(shft1),
                                overscore2.animate.shift(shft2),
                                overletter1.animate.shift(shft1),
                                overletter2.animate.shift(shft2),
                                run_time = 0.1
                            )
                        )
                    s.find_pairs(self,[ind],[[3*i, 3*i+3], [3*j, 3*j+3]])
            self.play(
                FadeOut(overscore1),
                FadeOut(overscore2),
                FadeOut(overletter1),
                FadeOut(overletter2)
            )
            #And then there are also three more ABs where both A and B are from the same part, in fact these three. 
            #[udělá se druhý výpočet, obarví se AB a pak zmizí]
            #But if we now look at the counts of CAs, we see that, yet again, every two parts generate just one. And then there are again three CAs that are fully in one part. The parts that give us AB are not the same as those that give us CA, but it does not really matter. It is kind of clear that if there are in total three ABs generated inside one part, there have to be the same number of CAs generated inside one part, because in the end the parts are just six permuted versions of the same thing, so they cannot favor AB over CA. 
            #[to samé pro CA]

            self.next_section(skip_animations=False)
            overscore1.move_to(s.letters[1].get_center() + over_shift)
            overletter1 = Tex("AB", color = text_color).move_to(overscore1.get_center()).next_to(overscore1, UP)
            if ind == 4:
                overletter1 = Tex("CA", color = text_color).move_to(overscore1.get_center()).next_to(overscore1, UP)
            cleanup_anims = []

            for i in range(0, 6):
                if i == 0:
                    self.play(
                        FadeIn(overscore1)
                    )
                else:
                    shft = s.letters[i*3+1].get_center() + over_shift - overscore1.get_center()
                    self.play(
                        overscore1.animate.shift(shft),
                        overletter1.animate.shift(shft)
                    )

                cleanup_anims += s.find_pairs(self, [ind], [[3*i, 3*i+3], [3*i, 3*i+3]], highlight_color = RED)

            #print(cleanup_anims)
            self.play(
                FadeOut(overscore1),
                FadeOut(overletter1),
                *cleanup_anims
            )
        
        # In general, we can see that it does not matter how you order the six triplets, you will always get the same counts of ABs, BCs, and ACs. 
        # [zase se přehází string, pak znovu celý výpočet]


        self.wait(10)

class Construction2(Scene):
    def construct(self):
        skip = True
        self.next_section(skip_animations= skip)
        #But it turns out that this argument is quite general, so do you see how we can build a fair string this way? Well, here is how we can do it. First, we start with the triplet ABC. Then, we do this construction, where we write it six times, we create the six versions of it and concatenate them in an arbitrary order to get a new string. And then … well we just do it one more time!
        # [ABC, napíše se 6x pod sebe, propermutuje, zkonkatenuje, pak to samý]

        sc = 0.6
        base = FairString("ABC")
        permutations = [
            [],
            [["A", "B"], ["B", "A"]],
            [["A", "C"], ["C", "A"]],
            [["C", "B"], ["B", "C"]],
            [["A", "B"], ["B", "C"], ["C", "A"]],
            [["A", "C"], ["C", "B"], ["B", "A"]],
        ]

        for it in range(2):
            parts = [base] + [base.copy() for i in range(5)]
            if it == 0:
                parts[0].letters[0].shift(2*UP)
                parts[0].write(self)
            if it == 1:
                parts[0].animate_shift(
                    self,
                    (parts[0].letters[0].get_center() + parts[0].letters[len(parts[0].letters)-1].get_center())/2 * LEFT
                )
            for i in range(1, 6):
                parts[i].letters[0].align_to(
                    parts[i-1].letters[0], LEFT
                ).next_to(
                    parts[i-1].letters[0], DOWN
                )
                parts[i].write(self)

            # the triangle with A,B,C
            rad = 0.75
            
            pA = Tex("A", color = text_color).shift(rad * (0.5 * DOWN + math.sqrt(3)/2 * LEFT))
            pB = Tex("B", color = text_color).shift(rad * (0.5 * DOWN + math.sqrt(3)/2 * RIGHT))
            pC = Tex("C", color = text_color).shift(rad * UP)

            permutation_triangle = Group(pA, pB, pC).move_to(
                parts[0].letters[0].get_center()
            ).next_to(
                parts[0].letters[0],
                LEFT
            ).shift(
                0.5*LEFT
            )

            #Then we do the six transforms
            for i in range(6):
                if i == 0:
                    self.play(FadeIn(permutation_triangle))
                else:
                    # first shift the triangle
                    self.play(
                        permutation_triangle.animate.shift(parts[i].letters[0].get_center() - parts[i-1].letters[0].get_center())
                    )

                    ar_width = 1
                    arrows_to_create = Group()
                    if i == 1:
                        arrows_to_create.add(DoubleArrow(start = pA.get_center(), end = pB.get_center(), color = text_color, stroke_width = ar_width))
                    if i == 2:
                        arrows_to_create.add(DoubleArrow(start = pA.get_center(), end = pC.get_center(), color = text_color, stroke_width = ar_width))
                    if i == 3:
                        arrows_to_create.add(DoubleArrow(start = pB.get_center(), end = pC.get_center(), color = text_color, stroke_width = ar_width))
                    if i == 4:
                        arrows_to_create.add(Arrow(start = pA.get_center(), end = pB.get_center(), color = text_color, stroke_width = ar_width))
                        arrows_to_create.add(Arrow(start = pB.get_center(), end = pC.get_center(), color = text_color, stroke_width = ar_width))
                        arrows_to_create.add(Arrow(start = pC.get_center(), end = pA.get_center(), color = text_color, stroke_width = ar_width))
                    if i == 5:
                        arrows_to_create.add(Arrow(start = pA.get_center(), end = pC.get_center(), color = text_color, stroke_width = ar_width))
                        arrows_to_create.add(Arrow(start = pC.get_center(), end = pB.get_center(), color = text_color, stroke_width = ar_width))
                        arrows_to_create.add(Arrow(start = pB.get_center(), end = pA.get_center(), color = text_color, stroke_width = ar_width))

                    self.play(
                        *[FadeIn(arrow) for arrow in arrows_to_create]                
                    )
                    parts[i].animated_permute(self, permutations[i])
                    self.play(
                        *[FadeOut(arrow) for arrow in arrows_to_create] 
                    )
            self.play(
                FadeOut(pA),
                FadeOut(pB),
                FadeOut(pC)
            )
            #Then we form one long string
            if it == 0:
                parts[0].animate_shift(self, 1*LEFT)
                for i in range(1, 6):
                    parts[i].animate_shift(
                        self,
                        parts[i-1].letters[len(parts[i-1].letters)-1].get_center()
                        + default_sep * RIGHT
                        - parts[i].letters[0].get_center()
                    )
            else:
                parts[0].animate_shift_rescale(self, 3*LEFT, sc, default_sep * sc)
                for i in range(1, 6):
                    if i == 3:
                        parts[i].animate_shift_rescale(
                            self,
                            parts[0].letters[0].get_center()
                            + 0.5 * DOWN
                            - parts[i].letters[0].get_center(),
                            sc,
                            default_sep * sc
                        )
                    else:
                        parts[i].animate_shift_rescale(
                            self,
                            parts[i-1].letters[len(parts[i-1].letters)-1].get_center()
                            + default_sep *  RIGHT
                            - parts[i].letters[0].get_center(),
                            sc,
                            default_sep * sc
                        )

            #merge into one fair string
            base = parts[0]
            for i in range(1,6):
                base.add(parts[i])

        # So, we take this string of 18 letters and write all six versions of it with permuted letters. By that I mean, that first we just write this string six times. We leave the first string as it is. Then we swap all As and Bs. Then, we swap all As and Cs. Then Bs and Cs, then, we change A for B, B for C, C for A, and finally A for C, C for B, B for A. OK, now take all those strings and concatenate them, in an arbitrary order. We get this beauty. Ufff. Ok, I claim that this is a fair string. Let’s compute the counts of all six possible triplets in it… 
        # [udělá se jeden dlouhý string (asi na dvě řádky) a pak výpočet]
        # Nice, it works. 

        skip = True
        self.next_section(skip_animations= skip)
        base.create_buckets(
            self, 
            ["\#ABC", "\#ACB", "\#BAC", "\#BCA", "\#CAB", "\#CBA"],
            [['A', 'B', 'C'], ['A', 'C', 'B'], ['B', 'A', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B'], ['C', 'B', 'A']]
        )

        self.wait()
        base.find_triplets(self, [0, 1, 2, 3, 4, 5], scale = sc, cheap_after_steps=2, prob = 1e-4)
        self.wait()
        base.clear_counters(self)
        self.wait()
        
        #So why is it so? Well, it is basically the same argument as before. 
        # [vyresetují se countery]
        # Let’s look for example on the counts of ABC and CAB. First, there are a lot of contributions to the count of ABC such that for example AB is from this part and C is from that part. 
        # [mezi částmi se udělá mezera, pak výpočet kde nad nadčárami je AB a C]
        # Their number is just the product of the number of ABs here and the number of Cs here. 
        # [circumbscribe the two parts]

        i = 1
        j = 2
        overscore1 = Line(
            start = parts[i].letters[0].get_center() + over_shift*sc,
            end = parts[i].letters[len(parts[i].letters) - 1].get_center() + over_shift * sc,
            color = text_color
        )
        overtext1 = Tex(
            "AB",
            color = text_color
        ).move_to(
            overscore1.get_center()
        ).next_to(
            overscore1,
            UP
        )

        overscore2 = Line(
            start = parts[j].letters[0].get_center() + over_shift*sc,
            end = parts[j].letters[len(parts[j].letters) - 1].get_center() + over_shift * sc,
            color = text_color
        )
        overtext2 = Tex(
            "C",
            color = text_color
        ).move_to(
            overscore2.get_center()
        ).next_to(
            overscore2,
            UP
        )

        self.play(
            Circumscribe(Group(base.counters[i], base.counter_titles[i])),
            #Circumscribe(Group(base.counters[j], base.counter_titles[j])),
        )

        self.play(
            FadeIn(overscore1),
            FadeIn(overtext1)
        )
        self.wait()

        self.play(
            FadeIn(overscore2),
            FadeIn(overtext2),
        )

        base.find_triplets(self, [0], ranges = [[18*i, 18*(i+1)], [18*i, 18*(i+1)], [18*j, 18*(j+1)]] , scale = sc, cheap_after_steps=2, prob = 1e-2)
        self.wait()       



        self.next_section(skip_animations= True)

        self.play(
            Circumscribe(Group(overscore1, overtext1, parts[i].letters[0], parts[i].letters[len(parts[i].letters)-1]))
        ) 
        self.wait()
        self.play(
            Circumscribe(Group(overscore2, overtext2, parts[j].letters[0], parts[j].letters[len(parts[j].letters)-1]))
        ) 
        self.wait()

        #But look, the six parts of our string already have the same counts of ABs and CAs and of course the same counts of C as B. So the contribution to the bucket with ABC is the same as to the bucket with CAB.  
        #[napíše se #AB=#CA, #C=#B, pak ten samý výpočet pro CAB, rovnice se nahradí CA, B]

        self.play(
            Transform(overtext1, Tex("\#AB = \#CA", color = text_color).move_to(overtext1.get_center())),
        )
        self.wait()

        self.play(
            Transform(overtext2, Tex("\#C = \#B", color = text_color).move_to(overtext2.get_center())),
        )
        self.wait()

        self.play(
            Transform(overtext1, Tex("CA", color = text_color).move_to(overtext1.get_center())),
            Transform(overtext2, Tex("B", color = text_color).move_to(overtext2.get_center())),
        )
        self.wait()

        base.find_triplets(self, [4], ranges = [[18*i, 18*(i+1)], [18*i, 18*(i+1)], [18*j, 18*(j+1)]] , scale = sc, cheap_after_steps=2, prob = 1e-2)
        self.wait()


        #You can also consider the contributions like A coming from this part, B from this part, and C from this part. But again, the contribution to the bucket with ABCs is the same as the contribution to the bucket with CAB. 
        #[to samý]

        self.play(
            FadeOut(overscore1),
            FadeOut(overscore2),
            FadeOut(overtext1),
            FadeOut(overtext2)
        )

        self.play(
            *[l.animate.shift(1*DOWN) for l in base.letters[18*3 : 18*6]]
        )
        self.wait()

        i = 0
        j = 1
        k = 5
        self.next_section(skip_animations= True)

        overscore1 = Line(
            start = parts[i].letters[0].get_center() + over_shift*sc,
            end = parts[i].letters[17].get_center() + over_shift * sc,
            color = text_color
        )
        overtext1 = Tex(
            "A",
            color = text_color
        ).move_to(
            overscore1.get_center()
        ).next_to(
            overscore1,
            UP
        )

        overscore2 = Line(
            start = parts[j].letters[0].get_center() + over_shift*sc,
            end = parts[j].letters[len(parts[j].letters) - 1].get_center() + over_shift * sc,
            color = text_color
        )
        overtext2 = Tex(
            "B",
            color = text_color
        ).move_to(
            overscore2.get_center()
        ).next_to(
            overscore2,
            UP
        )

        overscore3 = Line(
            start = parts[k].letters[0].get_center() + over_shift*sc,
            end = parts[k].letters[len(parts[k].letters) - 1].get_center() + over_shift * sc,
            color = text_color
        )
        overtext3 = Tex(
            "C",
            color = text_color
        ).move_to(
            overscore3.get_center()
        ).next_to(
            overscore3,
            UP
        )

        self.play(
            FadeIn(overscore1),
            FadeIn(overtext1)
        )
        self.wait()

        self.play(
            FadeIn(overscore2),
            FadeIn(overtext2),
        )
        self.wait()

        self.play(
            FadeIn(overscore3),
            FadeIn(overtext3),
        )
        self.wait()


        base.find_triplets(self, [0], ranges = [[18*i, 18*(i+1)], [18*j, 18*(j+1)], [18*k, 18*(k+1)]] , scale = sc, cheap_after_steps=2, prob = 1e-2)
        self.wait()


        self.play(
            Transform(overtext1, Tex("C", color = text_color).move_to(overtext1.get_center())),
            Transform(overtext2, Tex("A", color = text_color).move_to(overtext2.get_center())),
            Transform(overtext3, Tex("B", color = text_color).move_to(overtext3.get_center())),
        )
        self.wait()

        base.find_triplets(self, [4], ranges = [[18*i, 18*(i+1)], [18*j, 18*(j+1)], [18*k, 18*(k+1)]] , scale = sc, cheap_after_steps=2, prob = 1e-2)
        self.wait()

        self.play(
            FadeOut(overscore1),
            FadeOut(overscore2),
            FadeOut(overscore3),
            FadeOut(overtext1),
            FadeOut(overtext2),
            FadeOut(overtext3)
        )

        #base.clear_counters(self)

        # The only contributions that are different are those where all ABCs are coming from the same bucket. There are … from the first bucket, then it is … 
        # [nové county pro každou část]
        # But if you look at the CAB contributions, these are the same six numbers just in a different order, which follows from the fact that the six strings are really just six permuted versions of the same thing. 
        #[zase to samý pro CAB, je vidět že to sou stejný čísla]

        self.next_section(skip_animations= False)

        overscore1 = Line(
            start = parts[0].letters[0].get_center() + over_shift*sc,
            end = parts[0].letters[18 - 1].get_center() + over_shift * sc,
            color = text_color
        )
        overtext1 = Tex(
            "ABC",
            color = text_color
        ).move_to(
            overscore1.get_center()
        ).next_to(
            overscore1,
            UP
        )

        partial_counters = []
        for i in range(0, 6):
            if i == 0:
                self.play(
                    FadeIn(overscore1),
                    FadeIn(overtext1)
                )
            else:
                shft = (parts[i].letters[0].get_center() + parts[i].letters[len(parts[i].letters)-1].get_center())/2 + over_shift - overscore1.get_center()
                self.play(
                    overscore1.animate.shift(shft),
                    overtext1.animate.shift(shft)
                )
            partial_counters.append(
                Integer(0, color = text_color).move_to(
                    parts[i].letters[0].get_center() + 0.5*UP
                )
            )
            orig_val = base.counters[0].get_value()
            partial_counters[i].add_updater(
                lambda m : m.set_value(
                    base.counters[0].get_value() - orig_val
                )
            )
            self.play(
                FadeIn(partial_counters[i])
            )
            base.find_triplets(self, [0], ranges = [[18*i, 18*(i+1)], [18*i, 18*(i+1)], [18*i, 18*(i+1)]] , scale = sc, cheap_after_steps=3, prob = 1e-2)
            self.wait()
            self.add(
                Integer(
                    partial_counters[i].get_value(),
                    color = text_color
                ).move_to(partial_counters[i].get_center())
            )
            self.remove(partial_counters[i])
        self.play(
            FadeOut(overscore1),
            FadeOut(overtext1)
        )
        self.wait()

        #the same for CAB
        overscore1 = Line(
            start = parts[0].letters[0].get_center() + over_shift*sc,
            end = parts[0].letters[18 - 1].get_center() + over_shift * sc,
            color = text_color
        )
        overtext1 = Tex(
            "CAB",
            color = text_color
        ).move_to(
            overscore1.get_center()
        ).next_to(
            overscore1,
            UP
        )

        partial_counters = []
        for i in range(0, 6):
            if i == 0:
                self.play(
                    FadeIn(overscore1),
                    FadeIn(overtext1)
                )
            else:
                shft = (parts[i].letters[0].get_center() + parts[i].letters[len(parts[i].letters)-1].get_center())/2 + over_shift - overscore1.get_center()
                self.play(
                    overscore1.animate.shift(shft),
                    overtext1.animate.shift(shft)
                )
            partial_counters.append(
                Integer(0, color = text_color).move_to(
                    parts[i].letters[17].get_center() + 0.5*UP + 0.3*LEFT
                )
            )
            orig_val = base.counters[4].get_value()
            partial_counters[i].add_updater(
                lambda m : m.set_value(
                    base.counters[4].get_value() - orig_val
                )
            )
            self.play(
                FadeIn(partial_counters[i])
            )
            base.find_triplets(self, [4], ranges = [[18*i, 18*(i+1)], [18*i, 18*(i+1)], [18*i, 18*(i+1)]] , scale = sc, cheap_after_steps=3, prob = 1e-2)
            self.wait()
            self.add(
                Integer(
                    partial_counters[i].get_value(),
                    color = text_color
                ).move_to(partial_counters[i].get_center())
            )
            self.remove(partial_counters[i])

        self.wait()
        self.play(
            *[FadeOut(obj) for obj in self.mobjects]
        )

class Construction3(Scene):
    def construct(self):
        base = FairString("ABCD")
        sc1 = 0.5
        sc2 = 0.3
        sc3 = 0.1

        permutations = []
        for perm in itertools.permutations(["A", "B", "C", "D"]):
            permutations.append(
                [["A", perm[0]], ["B", perm[1]], ["C", perm[2]], ["D", perm[3]]]
            )
        
        #prvni iterace
        parts = []
        for i in range(24):
            parts.append(base.copy())
            if i == 0:
                parts[i].write(self,3.5*UP,scale=sc1)
            else:
                parts[i].letters[0].move_to(parts[i-1].letters[0].get_center()).shift(0.3*DOWN)
                parts[i].write(self, scale = sc1)
            
        for i in range(24):
            parts[i].animated_permute(self,permutations[i], scale = sc1)
        self.wait()
        
        for i in range(24):
            if i == 0:
                parts[i].animate_shift_rescale(self, 5.5 * LEFT, sc2/sc1, sep = default_sep * sc2)
            else:
                parts[i].animate_shift_rescale(
                    self, 
                    parts[i-1].letters[3].get_center() + sc2 * default_sep * RIGHT - parts[i].letters[0].get_center(),
                    sc2/sc1, sep = default_sep * sc2
                )

        #druha iterace
        base = FairString("")
        for i in range(24):
            base.add(parts[i])

        parts = [base]
        for i in range(1, 24):
            parts.append(base.copy())
            parts[i].letters[0].move_to(parts[i-1].letters[0].get_center()).shift(0.2*DOWN)
            parts[i].write(self, center = False, scale = sc2)
            
        for i in range(24):
            parts[i].animated_permute(self,permutations[i], scale = sc2)
        self.wait()

        for i in range(24):
            if i == 0:
                parts[i].animate_shift_rescale(self, 0.5 * LEFT + 0.5 * UP, sc3/sc2, sep = default_sep * sc3)
            else:
                if i % 3 == 0:
                    parts[i].animate_shift_rescale(
                        self,
                        parts[i-3].letters[0].get_center() + parts[i-3].letters[0].get_bottom() - parts[i-3].letters[0].get_top() - parts[i].letters[0].get_center(),
                         sc3/sc2, sep = default_sep * sc3
                    )
                else:
                    parts[i].animate_shift_rescale(
                        self, 
                        parts[i-1].letters[4*24-1].get_center() + sc3 * default_sep * RIGHT - parts[i].letters[0].get_center(),
                        sc3/sc2, sep = default_sep * sc3
                    )
         
        #treti iterace
        base = FairString("")
        for i in range(24):
            base.add(parts[i])

        parts = [base]
        for i in range(1, 24):
            parts.append(base.copy())
            parts[i].letters[0].move_to(parts[i-1].letters[23*(4*24)].get_center()).shift(0.1*DOWN)
            parts[i].write(self, center = False, scale = sc2)
            
        for i in range(24):
            parts[i].animated_permute(self,permutations[i], scale = sc2)
        self.wait()


        self.play(
            FadeIn(
                Tex("55296 letters", color = text_color).shift(2*UP)
            )
        )
        self.wait()
        self.play(
            FadeIn(
                Tex(fair_strings4[0], color = text_color)
            )
        )
        
        self.wait()
        
        # self.play(
        #     *[FadeOut(obj) for obj in self.mobjects]
        # )
        # self.wait()


