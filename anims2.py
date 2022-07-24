
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