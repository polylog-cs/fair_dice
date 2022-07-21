import random
import math
import numpy as np
from manim import *
from solarized import *
from functools import cmp_to_key

text_color = GRAY
background_color = config.background_color
under_shift = 0.3* DOWN
over_shift = 0.3*UP

fair_strings = [
"ABCBCACABCBAACBBAC",
"ABCCBABCAACBCABBAC",
"ABCCBABACCABCABBAC",
"ABCCBABACCABCBAABC",
"ABCCBACABBACBACCAB",
"ABCCABCBBAACABCCAB"
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
        self.n = len(self.letters)
        self.counters = []
        self.counter_titles = []

    def write(self, scene, pos_ = None, sep_ = 0.4, center = True):
        if pos_ is None:
            pos_ = self.letters[0].get_center()        
        self.sep = sep_

        for i, l in enumerate(self.letters):
            if i == 0:
                l.move_to(pos_)
            else:
                l.move_to(self.letters[i-1].get_center() + self.sep * RIGHT)
        
        if center == True:
            off = (self.letters[0].get_center() + self.letters[self.n - 1].get_center())/2
            for l in self.letters:
                l.shift(off * LEFT)

        scene.play(
            AnimationGroup(
                *[Write(l) for l in self.letters],
                lag_ratio = 0.1
            )
        )

    def create_from(self):
        pass

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

    def find_triplets(self, scene, match_set, ranges = [None, None, None]):
        underscore1 = Line(start = -0.1*RIGHT + under_shift, end = 0.1*RIGHT + under_shift, color = text_color)
        underscore2 = underscore1.copy()
        underscore3 = underscore1.copy()
        #anims = []
        beg = True
        if ranges[0] == None:
            ranges = [[0, len(self.str)], [0, len(self.str)], [0, len(self.str)]]

        for i in range(ranges[0][0], ranges[0][1]):
            for j in range(max(i+1, ranges[1][0]), ranges[1][1]):
                for k in range(max(j+1, ranges[2][0]), ranges[2][1]):
                    for mi in match_set:
                        if self.str[i] == self.counter_letters[mi][0] and self.str[j] == self.counter_letters[mi][1] and self.str[k] == self.counter_letters[mi][2]:
                            if beg == True:
                                underscore1.move_to(self.letters[i].get_center() + under_shift)
                                underscore2.move_to(self.letters[j].get_center() + under_shift)
                                underscore3.move_to(self.letters[k].get_center() + under_shift)
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
                                        underscore1.animate.move_to(self.letters[i].get_center() + under_shift),
                                        underscore2.animate.move_to(self.letters[j].get_center() + under_shift),
                                        underscore3.animate.move_to(self.letters[k].get_center() + under_shift),
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
        if beg == False:
            scene.play(
                Uncreate(underscore1),
                Uncreate(underscore2),
                Uncreate(underscore3),
                run_time = 0.1
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

    def clear_buckets(self, scene):
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

    def reorganize_by_left_coordinate(self):
        #change the order of letters based on their current position on the screen
        self.letters.sort(key = cmp_to_key(lambda l1, l2: l1.get_center()[0] - l2.get_center()[0]))
        self.str = ""
        for l in self.letters:
            self.str += l.get_tex_string()

class Construction(Scene):
    def construct(self):
        skip = True
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
            new_s.write(self, pos_ = new_s.letters[0].get_center())
            six_fair_strings.append(new_s)
        
        self.wait()

        #The first two solutions are actually kind of interesting, because they are just the triplet ABC concatenated six times, each time with its letters permuted differently. 
        #[nechají se jen první 2 řešení, udělají se mezery po částech]
        skip = True
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


        skip = True
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

        skip = True
        self.next_section(skip_animations = skip)
        
        s.create_buckets(
            self, 
            ["\#AB", "\#AC", "\#BA", "\#BC", "\#CA", "\#CB"],
            [['A', 'B'], ['A', 'C'], ['B', 'A'], ['B', 'C'], ['C', 'A'], ['C', 'B']]
        )
        if not skip:
            s.find_pairs(self, [0, 1, 2, 3, 4, 5])
            s.clear_buckets(self)
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
                overletter1 = Tex("C", color = text_color).move_to(overscore1.get_center()).next_to(overscore1, UP)
                overletter2 = Tex("A", color = text_color).move_to(overscore2.get_center()).next_to(overscore1, UP)
                
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

                cleanup_anims.append(
                    s.find_pairs(self, [ind], [[3*i, 3*i+3], [3*i, 3*i+3]], highlight_color = RED)
                )                   
            self.play(
                FadeOut(overscore1),
                FadeOut(overletter1),
                *cleanup_anims
            )
        self.wait(10)

class Permuting(Scene):
    def construct(self):
        def sw(s, l1, l2):
            return s.replace(l1, "Z").replace(l2, l1).replace("Z", l2)
        
        example_string = "ABCBCACABCBAACBBAC"
        s_versions = [
            example_string,
            sw(example_string, "A", "B"),
            sw(example_string, "A", "C"),
            sw(example_string, "B", "C"),
            sw(sw(example_string, "A", "B"), "A", "C"),
            sw(sw(example_string, "A", "C"), "A", "B"),
        ]

        texts = []
        for i in range(6):
            texts.append(Tex(
                example_string,
                color = text_color
            ))
            if i == 0:
                texts[i].shift(2*UP)
            else:
                texts[i].next_to(texts[i-1], DOWN)#.shift(0.5*DOWN)
        
        # first, the texts appear
        self.play(
            AnimationGroup(
                *[Write(t) for t in texts],
                lag_ratio = 0.5
            )
        )

        # the triangle with A,B,C
        rad = 0.75
        
        pA = Tex("A", color = text_color).shift(rad * (0.5 * DOWN + math.sqrt(3)/2 * LEFT))
        pB = Tex("B", color = text_color).shift(rad * (0.5 * DOWN + math.sqrt(3)/2 * RIGHT))
        pC = Tex("C", color = text_color).shift(rad * UP)

        permutation_triangle = Group(pA, pB, pC).move_to(
            texts[0].get_center()
        ).next_to(
            texts[0],
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
                    permutation_triangle.animate.shift(texts[i].get_center() - texts[i-1].get_center())
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

                anims = []
                anims.append(
                    Transform(texts[i], Tex(s_versions[i], color = text_color).move_to(texts[i].get_center()))
                )
                self.play(
                    *anims,
                    *[FadeIn(arrow) for arrow in arrows_to_create]                
                )
                self.play(
                    *[FadeOut(arrow) for arrow in arrows_to_create] 
                )

        #Then we form one long string
        #new_fair_string = 