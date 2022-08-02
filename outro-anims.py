from util import *


class Outro(Scene):
    def construct(self):
        permutations = []
        for perm in itertools.permutations(["A", "B", "C"]):
            permutations.append(
                [["A", perm[0]], ["B", perm[1]], ["C", perm[2]]]
            )
        def permute(str, perm):
            str_out = ""
            for i in range(len(str)):
                for j in range(len(perm)):
                    if str[i] == perm[j][0]:
                        str_out += perm[j][1]
            return str_out

        s1 = "ABC"

        s2 = ""
        for i in range(len(permutations)):
            s2 += permute(s1, permutations[i])

        s3 = ""
        for i in range(len(permutations)):
            s3 += permute(s2, permutations[i])

    
        sc = 0.7
        t1 = Tex(s1, color = text_color).shift(2*UP)
        t2 = Tex(s2, color = text_color)
        t3 = [  
            Tex(s3[0:3*18], color = text_color).shift(2*DOWN).scale(sc),
            Tex(s3[3*18:6*18], color = text_color).shift(2.5*DOWN).scale(sc)
        ]

        ar1 = Tex(r"$\downarrow$", color = text_color).move_to(
            (t1.get_center() + t2.get_center())/2
        )
        ar2 = Tex(r"$\downarrow$", color = text_color).move_to(
            (t2.get_center() + t3[0].get_center())/2
        )
        
        # write the first string
        self.play(
            FadeIn(t1),
        )
        self.wait()

        # first transform
        six_parts = []
        for i in range(len(permutations)):
            six_parts.append([
                Tex(s1, color = text_color).move_to(t1.get_center()),
                Tex(permute(s1, permutations[i]), color = text_color).move_to(t2[0][1 + 3*i].get_center())
            ])

        self.play(
            Succession(
                FadeIn(ar1),
                AnimationGroup(
                    *[Transform(beg, end) for [beg, end] in six_parts],
                    lag_ratio = 0.3            
                ),
            )
        )        
        self.wait()

        # second transform
        six_parts = []
        for i in range(len(permutations)):
            six_parts.append([
                Tex(s2, color = text_color).move_to(t2.get_center()),
                Tex(permute(s2, permutations[i]), color = text_color).scale(sc).move_to((t3[i//3][0][18*(i%3)].get_center() + t3[i//3][0][18*((i%3)+1)-1].get_center())/2)
            ])

        self.play(
            Succession(
                FadeIn(ar2),
                AnimationGroup(
                    *[Transform(beg, end) for [beg, end] in six_parts],
                    lag_ratio = 0.3            
                ),
            )
        )        
        self.wait()

        self.play(
            *[FadeOut(o) for o in self.mobjects]
        )
        self.wait()

class Thanks(Scene):
    def construct(self):
        s = [
            "Big thanks to",
            "organizers of SoME2,",
            "Manim Community,",
            "Bernhard \& ??? Haeupler, Hanka Rozhoňová"
        ]
        t = [
            Tex(ss, color = text_color) for ss in s
        ]
        for i in range(3, len(t)):
            t[i].scale(0.7)
        t[0].move_to(2*LEFT + 2*UP)
        for i in range(1, len(t)):
            t[i].next_to(t[i-1], DOWN).align_to(t[i-1], LEFT)
        t[0].shift(1*LEFT)

        self.play(
            *[FadeIn(tt) for tt in t]
        )
        self.wait()
        self.play(
            *[FadeOut(o) for o in self.mobjects]
        )
        self.wait()