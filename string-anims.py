
from util import *



class Equivalence(Scene):
    def construct(self):
        for i in range(3):
            three_dice[i].append(99)
        labels = [
            Tex("A:", color = text_color),
            Tex("B:", color = text_color),
            Tex("C:", color = text_color),
        ]
        labels[1].shift(5*LEFT)
        labels[0].move_to(labels[1].get_center()).next_to(labels[1], UP)
        labels[2].move_to(labels[1].get_center()).next_to(labels[1], DOWN)

        numbers = []
        for i in range(3):
            numbers.append([])
            for j in range(6):
                numbers[i].append(
                    Tex(three_dice[i][j], color = text_color)
                )
                if j == 0:
                    numbers[i][j].next_to(labels[i], RIGHT).shift(3*RIGHT)
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
            act_vals = [three_dice[0][iss[0]], three_dice[1][iss[1]], three_dice[2][iss[2]]]
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

        #only used at the end
        smart_text = Tex(
            r"like duality in linear programming, Fourier transform, generating functions, $\dots$", 
            color = text_color
            ).shift(3*DOWN).scale(0.7)
        self.play(
            FadeIn(smart_text)
        )
        self.wait()
        self.play(
            FadeOut(smart_text)
        )
        self.wait()

        # highlighting one triplet
        rec_highlights = [
            Rectangle(color = RED, height = 0.5, width = 0.5).move_to(lab.get_center())
            for lab in [dice_labels[0][5], dice_labels[1][11], dice_labels[2][1]]
        ]
        # above_note = Tex("$6^3 = 216$ possibilities", color = text_color).next_to(dice_labels[0], UP).shift(0.5*UP)
        # self.play(
        #     Create(above_note)
        # )
        # self.wait()

        rec_highlights2 = [
            Rectangle(color = RED, height = 0.5, width = 0.5).move_to(numbers_sorted[it].get_center())
            for it in [8-1, 16-1, 3-1]            
        ]
        self.play(
            Succession(
                AnimationGroup(
                    Create(rec_highlights[0]),
                    Create(rec_highlights2[0]),
                ),
                AnimationGroup(
                    Create(rec_highlights[1]),
                    Create(rec_highlights2[1]),
                ),
                AnimationGroup(
                    Create(rec_highlights[2]),
                    Create(rec_highlights2[2]),
                ),
            )
        )

        self.wait()
        
        note = Tex(r"$\textrm{C} < \textrm{A} < \textrm{B}$", color = text_color).next_to(dice_labels[2], DOWN).shift(0.3*DOWN)
        shft = 1*DOWN
        AA = Tex("A", color = text_color).next_to(numbers_sorted[8-1], DOWN).shift(shft)
        BB = Tex("B", color = text_color).next_to(numbers_sorted[16-1], DOWN).shift(shft)
        CC = Tex("C", color = text_color).next_to(numbers_sorted[3-1], DOWN).shift(shft)
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
            #FadeOut(above_note),
            *[FadeOut(rec) for rec in rec_highlights + rec_highlights2],
            FadeOut(lrarrow),
            *[FadeOut(str) for str in dice_labels],
            FadeOut(note),
            *[FadeOut(l) for l in [AA, BB, CC]],
            *[num.animate.shift((numbers_sorted[0].get_center() + numbers_sorted[17].get_center())/2*LEFT+1*UP) for num in numbers_sorted]
        )
        self.wait()

class Construction1(Scene):
    def construct(self):
        skip = False
        self.next_section(skip_animations = skip)
        #OK, so here is how we do it. First, we really just think about the formulation of the problem with strings where we do not need to think in terms of probabilities. We just want to construct a string such that every permutation of letters occurs the same number of times in it.
        #[znovu ukázka nějakého stringu pro tři a počítání trojic] 
        s = FairString("ABCBCACABCBAACBBAC")
        s.write(self)

        if not skip:
            s.create_counters(
                self, 
                ["\#ABC", "\#ACB", "\#BAC", "\#BCA", "\#CAB", "\#CBA"],
                [['A', 'B', 'C'], ['A', 'C', 'B'], ['B', 'A', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B'], ['C', 'B', 'A']]
            )
            self.wait()
            s.find_triplets(self, [0, 1, 2, 3, 4, 5], cheap_after_steps=5, prob = 1e-4)
            self.wait()
            s.delete_counters(self)
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
            s.create_counters(
                self, 
                ["\#ABC", "\#ACB", "\#BAC", "\#BCA", "\#CAB", "\#CBA"],
                [['A', 'B', 'C'], ['A', 'C', 'B'], ['B', 'A', 'C'], ['B', 'C', 'A'], ['C', 'A', 'B'], ['C', 'B', 'A']]
            )
            self.wait()
            s.find_triplets(self, [0, 1, 2, 3, 4, 5], cheap_after_steps=5, prob = 1e-4)
            self.wait()
            s.delete_counters(self)
            self.wait()

        self.wait()

        #Well it turns out that although we do not have the same number of all triplets, we at least have the same number of all pairs. So, let’s compute those numbers:
        #[udělají se šuplíky AB,AC,BA, BC, CA, CB, pak se spočítá]
        #Nice, they are the same. And this actually works independently on how we concatenate the permutations of the original string. 

        skip = False
        self.next_section(skip_animations = skip)
        
        s.create_counters(
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
        skip = False
        self.next_section(skip_animations= skip)
        #But it turns out that this argument is quite general, so do you see how we can build a fair string this way? Well, here is how we can do it. First, we start with the triplet ABC. Then, we do this construction, where we write it six times, we create the six versions of it and concatenate them in an arbitrary order to get a new string. And then … well we just do it one more time!
        # [ABC, napíše se 6x pod sebe, propermutuje, zkonkatenuje, pak to samý]

        sc = 0.6
        base = FairString("ABC")
        permutations = []
        for perm in itertools.permutations(["A", "B", "C"]):
            permutations.append(
                [["A", perm[0]], ["B", perm[1]], ["C", perm[2]]]
            )

        for it in range(2):
            parts = [base] + [base.copy() for i in range(5)]
            if it == 0:
                parts[0].letters[0].shift(2*UP)
                parts[0].write(self)
            if it == 1:
                print((parts[0].letters[0].get_center() + parts[0].letters[len(parts[0].letters)-1].get_center())/2 * LEFT)
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
            rad = 0.5

            sc_lab = 0.7            
            pA = Tex("A", color = text_color).scale(sc_lab).shift(rad * (0.5 * DOWN + math.sqrt(3)/2 * LEFT))
            pB = Tex("B", color = text_color).scale(sc_lab).shift(rad * (0.5 * DOWN + math.sqrt(3)/2 * RIGHT))
            pC = Tex("C", color = text_color).scale(sc_lab).shift(rad * UP)

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
                        arrows_to_create.add(DoubleArrow(start = pB.get_center(), end = pC.get_center(), color = text_color, stroke_width = ar_width))
                    if i == 2:
                        arrows_to_create.add(DoubleArrow(start = pA.get_center(), end = pB.get_center(), color = text_color, stroke_width = ar_width))
                    if i == 3:
                        arrows_to_create.add(Arrow(start = pA.get_center(), end = pB.get_center(), color = text_color, stroke_width = ar_width))
                        arrows_to_create.add(Arrow(start = pB.get_center(), end = pC.get_center(), color = text_color, stroke_width = ar_width))
                        arrows_to_create.add(Arrow(start = pC.get_center(), end = pA.get_center(), color = text_color, stroke_width = ar_width))
                    if i == 4:
                        arrows_to_create.add(Arrow(start = pA.get_center(), end = pC.get_center(), color = text_color, stroke_width = ar_width))
                        arrows_to_create.add(Arrow(start = pC.get_center(), end = pB.get_center(), color = text_color, stroke_width = ar_width))
                        arrows_to_create.add(Arrow(start = pB.get_center(), end = pA.get_center(), color = text_color, stroke_width = ar_width))
                    if i == 5:
                        arrows_to_create.add(DoubleArrow(start = pA.get_center(), end = pC.get_center(), color = text_color, stroke_width = ar_width))

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
                parts[0].animate_shift(self, 3*LEFT)
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

        skip = False
        self.next_section(skip_animations= skip)
        base.create_counters(
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
            Circumscribe(Group(base.counters[0], base.counter_titles[0]), color = RED),
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



        self.next_section(skip_animations= False)

        self.play(
            Circumscribe(Group(overscore1, overtext1, parts[i].letters[0], parts[i].letters[len(parts[i].letters)-1]), color = RED)
        ) 
        self.wait()
        self.play(
            Circumscribe(Group(overscore2, overtext2, parts[j].letters[0], parts[j].letters[len(parts[j].letters)-1]), color = RED)
        ) 
        self.wait()

        #But look, the six parts of our string already have the same counts of ABs and CAs and of course the same counts of C as B. So the contribution to the counter with ABC is the same as to the counter with CAB.  
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
            Circumscribe(Group(base.counters[4], base.counter_titles[4]), color = RED),
        )

        self.play(
            Transform(overtext1, Tex("CA", color = text_color).move_to(overtext1.get_center())),
            Transform(overtext2, Tex("B", color = text_color).move_to(overtext2.get_center())),
        )
        self.wait()

        base.find_triplets(self, [4], ranges = [[18*i, 18*(i+1)], [18*i, 18*(i+1)], [18*j, 18*(j+1)]] , scale = sc, cheap_after_steps=2, prob = 1e-2)
        self.wait()


        #You can also consider the contributions like A coming from this part, B from this part, and C from this part. But again, the contribution to the counter with ABCs is the same as the contribution to the counter with CAB. 
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
        self.next_section(skip_animations= False)

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
            Transform(overtext1, Tex("\#A = \#C", color = text_color).move_to(overtext1.get_center())),
            Transform(overtext2, Tex("\#B = \#A", color = text_color).move_to(overtext2.get_center())),
            Transform(overtext3, Tex("\#C = \#B", color = text_color).move_to(overtext3.get_center())),
        )
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

        # The only contributions that are different are those where all ABCs are coming from the same counter. There are … from the first counter, then it is … 
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

class ConstructABCD(Scene):
    def construct(self):
        base = FairString("ABCD")
        sc1 = 0.5
        sc2 = 0.35
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
                parts[i].animate_shift_rescale(self, 
                6.7*LEFT + 3.8*UP - parts[i].letters[0].get_center(),
                sc2/sc1, sep = default_sep * sc2)
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

        #treti iterace
        base = FairString("")
        for i in range(24):
            base.add(parts[i])

        base2 = base.copy()
        for l, l2 in zip(base.letters, base2.letters):
            l2.scale(sc2).move_to(l.get_center()).shift(24*(parts[1].letters[0].get_center() - parts[0].letters[0].get_center()))
        self.play(
            *[FadeIn(l) for l in base2.letters]
        )
        self.wait()
        base2.animated_permute(self, permutations[1], scale = sc2)        
        self.wait()
        return

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

class Scrolling(Scene):
    def construct(self):
        sc = 0.35
        
        #TODO change
        L = 50
        #L = 1
        up_shift = 3*UP
        test = 0
        
        strings = []
        f = open("ABCD.txt", "r")
        for _ in range(L):
            letters = []
            line = f.readline().strip()
            for i in range(len(line)):
                letters.append(
                    Tex(line[i], color = text_color).scale(sc)
                )
            strings.append(letters)

        for i in range(L):
            for j in range(len(strings[i])):
                if j == 0:
                    if i == 0:
                        strings[i][0].move_to(6.7*LEFT + 3.8*UP+test*5*DOWN)
                    else:
                        strings[i][0].move_to(strings[i-1][0].get_center()).shift(0.2*DOWN)
                else:
                    strings[i][j].move_to(strings[i][j-1].get_center()).shift(default_sep*sc*RIGHT)

        all_letters = []
        for str in strings:
            all_letters += str

        self.add(
            *all_letters
        )


        self.play(
            AnimationGroup(
                AnimationGroup(
                    *[l.animate.shift(up_shift) for l in all_letters],
                    run_time = 16
                ),
                Succession(
                    Wait(2),
                    Write(Tex("55296 letters: ", color = DARK_GRAY).shift(2*UP).set_z_index(100).scale(2))
                ),
                Succession(
                    Wait(4),
                    AnimationGroup(
                        Write(Tex(list_to_string(four_dice), color = DARK_GRAY).shift(3*DOWN).scale(0.8).set_z_index(100)),
                        Write(Tex("48 letters: ", color = DARK_GRAY).shift(2*DOWN).scale(2).set_z_index(100))
                    )
                ),
            )
        )

        # length_label = Tex("55296 letters", color = text_color).shift(2*UP).set_z_index(100)
        # self.add(
        #     length_label                
        # )
        # self.play(
        #     AnimationGroup(
        #         *[l.animate.shift(up_shift) for l in all_letters],
        #         rate_func = linear,
        #         run_time = 2
        #     )
        # )
        # self.add(
        #     Tex(fair_strings4[0], color = text_color).set_z_index(100)
        # )
        # self.play(
        #     AnimationGroup(
        #         *[l.animate.shift(up_shift) for l in all_letters],
        #         rate_func = linear,
        #         run_time = 2
        #     )
        # )
        
        self.wait()

