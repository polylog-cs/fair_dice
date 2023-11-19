from util import *


class Thumbnail(ThreeDScene):
    def construct(self):
        # ball = Sphere(center = 4.5*LEFT + 1.5*UP, radius = 2, resolution = (10,10)).set_color(BLUE)
        ball = ImageMobject("sphere.png").move_to(1 * DOWN).scale(0.3)
        self.add(ball)
        sc = 4.5
        txt = [
            Tex(r"this is a", color=text_color).scale(sc),
            Tex(r"$10^{60}$-sided die", color=text_color).scale(sc),
        ]
        txt = Group(*txt).arrange(DOWN).shift(0 * RIGHT + 3.5 * UP)
        txt[0].align_to(txt[1], RIGHT)

        arrow = ImageMobject("sipka.png").move_to(4.5 * RIGHT + 0.3 * DOWN)

        # arrow = Arrow(
        #     start = 1*RIGHT + 1 * DOWN,
        #     end = 1*LEFT + 1*UP,
        #     max_stroke_width_to_length_ratio=200,
        #     stroke_width = 10,
        #     color = text_color
        # )

        self.add_fixed_in_frame_mobjects(txt[1], arrow)


class Polylog(Scene):
    def construct(self):
        authors = Tex(
            r"\textbf{Tom Gavenčiak, Václav Rozhoň, Václav Volhejn}",
            color=text_color,
            font_size=40,
        ).shift(3 * DOWN + 0 * LEFT)

        channel_name = Tex(r"polylog", color=text_color)
        channel_name.scale(4).shift(1 * UP)

        self.play(Write(authors), Write(channel_name))

        self.wait()

        self.play(*[FadeOut(o) for o in self.mobjects])
        self.wait()


class DiceSquare(Scene):
    def construct(self):
        player_labels = [
            Tex("Player A: ", color=text_color),
            Tex("Player B: ", color=text_color),
        ]
        player_labels[0].move_to(3 * LEFT)
        player_labels[1].move_to(3 * RIGHT)
        self.play(FadeIn(player_labels[0]))
        self.wait()
        self.play(FadeIn(player_labels[1]))
        self.wait()

        dice_numbers = []
        for i in range(2):
            dice_numbers.append([])
            for j in range(len(example_dice_str[i])):
                dice_numbers[i].append(Tex(example_dice_str[i][j], color=text_color))
                if j == 0:
                    dice_numbers[i][j].next_to(player_labels[i], DOWN).align_to(
                        player_labels[i], LEFT
                    )
                else:
                    dice_numbers[i][j].next_to(dice_numbers[i][j - 1], RIGHT)
                    if j % 2 == 1:
                        dice_numbers[i][j].shift(0.2 * DOWN + 0.2 * LEFT)
                    else:
                        dice_numbers[i][j].shift(0.2 * UP + 0.1 * LEFT)

        self.play(
            AnimationGroup(*[FadeIn(nums) for nums in dice_numbers[0]], lag_ratio=0.15)
        )
        self.play(
            AnimationGroup(*[FadeIn(nums) for nums in dice_numbers[1]], lag_ratio=0.15)
        )
        self.wait()
        bad_number = (
            Tex("12", color=text_color)
            .next_to(dice_numbers[0][-1], RIGHT)
            .align_to(dice_numbers[0][-1], LEFT)
        )
        good_number = Tex("11", color=text_color).move_to(
            dice_numbers[0][-1].get_center()
        )

        sq = Square(
            side_length=dice_numbers[0][-1].get_right()[0]
            - dice_numbers[0][-1].get_left()[0]
            + 0.2,
            color=RED,
        ).move_to(dice_numbers[0][-1].get_center())

        self.play(
            Succession(
                Create(sq),
                Wait(),
                Transform(dice_numbers[0][-1], bad_number),
                Wait(),
                AnimationGroup(Circumscribe(dice_numbers[1][-1], color=RED)),
                Wait(),
                Transform(dice_numbers[0][-1], good_number),
                Uncreate(sq),
            )
        )
        self.wait()

        # create a grid and move everything around

        side_length = 0.8
        horizontal_lines = []
        vertical_lines = []
        shft = 0.5 * DOWN
        for i in range(7):
            horizontal_lines.append(
                Line(
                    3 * side_length * LEFT + (3 - i) * side_length * UP + shft,
                    3 * side_length * RIGHT + (3 - i) * side_length * UP + shft,
                    color=text_color,
                ),
            )
            vertical_lines.append(
                Line(
                    3 * side_length * UP + (3 - i) * side_length * LEFT + shft,
                    3 * side_length * DOWN + (3 - i) * side_length * LEFT + shft,
                    color=text_color,
                ),
            )

        anims = []
        dice_numbers_real = [[], []]
        for i in range(6):
            dice_numbers[0][2 * i].generate_target()
            dice_numbers[0][2 * i].target.move_to(
                (vertical_lines[i].get_top() + vertical_lines[i + 1].get_top()) / 2
            ).shift(0.4 * UP)
            anims.append(MoveToTarget(dice_numbers[0][2 * i]))
            dice_numbers_real[0].append(dice_numbers[0][2 * i])
        player_labels[0].generate_target()
        player_labels[0].target.next_to(horizontal_lines[0], UP).shift(0.6 * UP)
        anims.append(MoveToTarget(player_labels[0]))

        for i in range(6):
            dice_numbers[1][2 * i].generate_target()
            dice_numbers[1][2 * i].target.move_to(
                (horizontal_lines[i].get_left() + horizontal_lines[i + 1].get_left())
                / 2
            ).shift(0.4 * LEFT)
            anims.append(MoveToTarget(dice_numbers[1][2 * i]))
            dice_numbers_real[1].append(dice_numbers[1][2 * i])
        player_labels[1].generate_target()
        player_labels[1].target.next_to(vertical_lines[0], LEFT).shift(1 * LEFT)
        anims.append(MoveToTarget(player_labels[1]))

        for i in range(5):
            anims.append(FadeOut(dice_numbers[0][2 * i + 1]))
            anims.append(FadeOut(dice_numbers[1][2 * i + 1]))

        self.play(
            *[FadeIn(line) for line in horizontal_lines],
            *[FadeIn(line) for line in vertical_lines],
            *anims,
        )
        dice_numbers = dice_numbers_real
        self.wait()

        # show A<B and A>B
        squares = []
        blue_squares = []
        red_squares = []
        for i in range(6):
            squares.append([])
            for j in range(6):
                square = (
                    Square(side_length=0.8, fill_color=RED, stroke_color=RED)
                    .move_to(
                        2.5 * side_length * LEFT
                        + 2.5 * side_length * UP
                        + shft
                        + i * side_length * RIGHT
                        + j * side_length * DOWN
                    )
                    .set_fill(RED, opacity=1.0)
                    .set_z_index(-100)
                )
                if example_dice[0][i] > example_dice[1][j]:
                    square.set_color(BLUE)
                    square.set_fill(BLUE)
                    blue_squares.append(square)
                else:
                    red_squares.append(square)
                squares[i].append(square)

        AlB = (
            Tex(r"$A< B$", color=RED)
            .next_to(vertical_lines[-1], RIGHT)
            .shift(1 * RIGHT + 0.5 * UP)
        )
        AgB = (
            Tex(r"$A> B$", color=BLUE)
            .next_to(vertical_lines[-1], RIGHT)
            .shift(1 * RIGHT + 0.5 * DOWN)
        )

        # first just two examples
        sqab = squares[0][4]
        sqba = squares[3][1]
        txtab = Tex(r"$A<B$", color=DARK_GRAY).scale(0.5).move_to(sqab.get_center())
        txtba = Tex(r"$A>B$", color=DARK_GRAY).scale(0.5).move_to(sqba.get_center())

        self.play(
            FadeIn(sqab),
            FadeIn(txtab),
        )
        self.play(
            Circumscribe(dice_numbers[0][0], color=RED),
        )
        self.play(Circumscribe(dice_numbers[1][4], color=RED))
        self.wait()

        self.play(FadeIn(sqba), FadeIn(txtba))
        self.play(Circumscribe(dice_numbers[0][3], color=BLUE))
        self.play(
            Circumscribe(dice_numbers[1][1], color=BLUE),
        )
        self.wait()

        self.play(FadeOut(txtab), FadeOut(txtba), FadeOut(sqab), FadeOut(sqba))
        self.play(
            *[FadeIn(square) for line in squares for square in line],
            FadeIn(AlB),
            FadeIn(AgB),
        )
        self.wait()

        for square in red_squares:
            square.set_z_index(-50)
        self.play(*[Indicate(square, color=RED) for square in red_squares])
        self.wait()

        for square in blue_squares:
            square.set_z_index(-20)
        self.play(*[Indicate(square, color=BLUE) for square in blue_squares])
        self.wait()

        # One solution

        for i in [3, 4, 5]:
            dice_numbers[0][i].generate_target()
            dice_numbers[0][i].target.move_to(dice_numbers[1][i].get_center())
            dice_numbers[1][i].generate_target()
            dice_numbers[1][i].target.move_to(dice_numbers[0][i].get_center())

        self.add_sound(f"audio/tada.mp3")
        self.play(
            *[MoveToTarget(num) for num in dice_numbers[0][3:6] + dice_numbers[1][3:6]],
            *[
                square.animate.set_color(BLUE)
                for square in [squares[3][3], squares[4][4], squares[5][5]]
            ],
        )
        self.wait(2)
        for i in [0, 1]:
            for j in range(6):
                dice_numbers[i][j].generate_target()

        dice_numbers[0][0].target.move_to(dice_numbers[0][0].get_center())
        dice_numbers[0][1].target.move_to(dice_numbers[0][2].get_center())
        dice_numbers[0][2].target.move_to(dice_numbers[1][1].get_center())
        dice_numbers[0][3].target.move_to(dice_numbers[0][3].get_center())
        dice_numbers[0][4].target.move_to(dice_numbers[0][5].get_center())
        dice_numbers[0][5].target.move_to(dice_numbers[1][4].get_center())

        dice_numbers[1][0].target.move_to(dice_numbers[0][1].get_center())
        dice_numbers[1][1].target.move_to(dice_numbers[1][0].get_center())
        dice_numbers[1][2].target.move_to(dice_numbers[1][2].get_center())
        dice_numbers[1][3].target.move_to(dice_numbers[0][4].get_center())
        dice_numbers[1][4].target.move_to(dice_numbers[1][3].get_center())
        dice_numbers[1][5].target.move_to(dice_numbers[1][5].get_center())

        self.play(
            *[MoveToTarget(d) for d in dice_numbers[0] + dice_numbers[1]],
            *[
                square.animate.set_color(RED)
                for square in squares[0] + squares[1] + squares[2]
            ],
            *[
                square.animate.set_color(BLUE)
                for square in squares[3] + squares[4] + squares[5]
            ],
        )
        self.wait()

        self.play(*[FadeOut(o) for o in self.mobjects])
        self.wait()


# TODO put camera to the right place
pos_three_dice = 3 * UP
pos_fst_example = 4.5 * LEFT + 1.5 * UP
sc_examples = 0.9


class DiceCube(ThreeDScene):
    def construct(self):
        s = fair_strings[0]
        table = dice_table(string_to_list(s), scale=1, col_widths=[0.4] * 7)
        table.shift(2 * LEFT)

        self.add_fixed_in_frame_mobjects(*table)

        magic_pos = np.array([3.59 * DOWN + 1 * LEFT] * 3)
        magic_pos += np.array([0.2 * UP, 0.2 * UP, 0.15 * DOWN])
        print(magic_pos)
        magic_vec = [
            1.7 * LEFT + 1.8 * UP,
            3.7 * RIGHT + 1.15 * UP,
            5 * UP + 0.25 * LEFT,
        ]
        magic_sc = 0.85

        anims = []
        for i in range(3):
            for j in range(6):
                anims.append(
                    table[i * 7 + j + 1]
                    .animate.scale(magic_sc)
                    .move_to(magic_pos[i] + (j + 1) * magic_vec[i] / 6.0)
                )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    FadeOut(table[0]),
                    FadeOut(table[7]),
                    FadeOut(table[14]),
                ),
                AnimationGroup(
                    *anims[0:6],
                ),
                AnimationGroup(
                    *anims[6:12],
                ),
                AnimationGroup(
                    *anims[12:],
                ),
                lag_ratio=0.5,
            )
        )

        self.next_section(skip_animations=False)

        self.set_camera_orientation(
            phi=70 * DEGREES,  # pitch
            theta=-120 * DEGREES,  # yaw
        )
        self.move_camera(
            frame_center=np.array([0, 0, 2]),
            run_time=0.1,
            zoom=0.7,
        )

        n = 6
        nexts = [
            (LEFT + IN) * 0.5,
            (DOWN + IN) * 0.5,
            (LEFT + DOWN) * 0.5,
        ]
        dirs = [UP, RIGHT, OUT]
        global_shift = (n - 1) / 2 * (LEFT + DOWN)

        axes = ThreeDAxes(
            x_range=(0, n, 1),
            x_length=n,
            y_range=(0, n, 1),
            y_length=n,
            z_range=(0, n, 1),
            z_length=n,
        ).shift((dirs[0] + dirs[1]) * (n - 1) / 2 - dirs[2] * 0.5 + global_shift)

        axes.set_color(text_color)

        skeleton = Cube(
            side_length=6, fill_opacity=0, stroke_width=1, color=text_color
        ).shift(dirs[2] * 2.5)

        # self.add(
        #     base,
        #     Cube(side_length = 1, fill_color = RED).move_to(ORIGIN).shift(dirs[0]),
        #     Cube(side_length = 1, fill_color = GREEN).move_to(ORIGIN).shift(dirs[1]),
        #     Cube(side_length = 1, fill_color = BLUE).move_to(ORIGIN).shift(dirs[2]),
        # )

        labels = []
        labels_beg = []
        pos_beg = 2 * RIGHT + 2 * UP

        for i in range(3):
            labels.append([])
            labels_beg.append([])

            for j in range(len(dice[i])):
                l = Tex(
                    str(dice[i][j]) if j < len(dice[i]) else "ABC"[i],
                    # color = [RED, GREEN, BLUE][i],
                    color=text_color,
                ).scale(0.8)
                l_beg = l.copy()
                # if i == 1:
                #     l.rotate_about_origin(90*DEGREES,OUT)
                # if i == 2:
                #     l.rotate_about_origin(45*DEGREES, OUT).rotate_about_origin(90*DEGREES, RIGHT-DOWN)

                # labels[i].append(l.move_to(base.get_center()).shift(DOWN + LEFT + IN).shift(dirs[i] * (j + 1)))
                # continue
                if j == 0:
                    labels[i].append(
                        l.shift(nexts[i] + 0.5 * nexts[i] + global_shift)
                        # l.move_to(base.get_center())
                    )
                    if i == 0:
                        l_beg.move_to(pos_beg)
                    else:
                        l_beg.next_to(labels_beg[i - 1][0], DOWN)
                    labels_beg[i].append(l_beg)

                else:
                    labels[i].append(l.move_to(labels[i][j - 1].get_center() + dirs[i]))
                    labels_beg[i].append(l_beg.next_to(labels_beg[i][j - 1], RIGHT))

            l = Tex(
                "ABC"[i],
                color=text_color,
            )
            l_beg = l.copy()

            labels[i].append(l.move_to(labels[i][-1].get_center() + dirs[i] * 2))
            labels_beg[i].append(l_beg.next_to(labels_beg[i][0], LEFT))

        # TODO move labels to axes

        # self.add_fixed_in_frame_mobjects(
        #     *labels_beg[0],
        #     *labels_beg[1],
        #     *labels_beg[2],
        # )
        # self.wait()
        self.add_fixed_orientation_mobjects(
            *labels[0],
            *labels[1],
            *labels[2],
        )
        self.play(
            FadeIn(skeleton),
            FadeIn(axes),
            *[FadeIn(l) for lab in labels for l in lab],
            *[FadeOut(t) for t in table[1:7] + table[8:14] + table[15:]],
        )

        # self.play(
        #     Transform(
        #         labels_beg[0][0], labels[0][0]
        #     )
        # )

        self.begin_ambient_camera_rotation(rate=PI / 10, about="theta")
        T = 1
        self.wait()

        all_cubes = []
        order_labels = []

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
                                    fill_color=colors[it],
                                    fill_opacity=1.0,
                                )
                                .move_to(ORIGIN)
                                .shift(
                                    i * dirs[0]
                                    + j * dirs[1]
                                    + k * dirs[2]
                                    + global_shift
                                )
                            )

            all_cubes += cubes_to_appear

            if cubes_to_appear != []:
                letters = ["ABC"[p] for p in perm]
                order_label = Tex(
                    f"${letters[0]} < {letters[1]} < {letters[2]}$",
                    color=colors[it],
                ).shift(5 * RIGHT)
                self.add_fixed_in_frame_mobjects(order_label)

                self.play(
                    *[FadeIn(cube) for cube in cubes_to_appear],
                    FadeIn(order_label),
                    run_time=0.5,
                )
                self.wait(2.5)
                T += 3
                if len(order_labels) == 0:
                    anim_shift = order_label.animate.scale(0.7).move_to(
                        5 * RIGHT + 3 * UP
                    )
                else:
                    anim_shift = order_label.animate.scale(0.7).next_to(
                        order_labels[-1], DOWN
                    )
                order_labels.append(order_label)

                self.play(
                    *[FadeOut(cube) for cube in cubes_to_appear],
                    anim_shift,
                    run_time=0.5,
                )
                self.wait()
                T += 1.5

        self.next_section(skip_animations=False)

        self.play(*[FadeIn(cube) for cube in all_cubes])
        self.wait(1)
        calculation_text = Tex(r"$\frac{6^3}{3!} = 36$", color=BASE2).scale(2)
        self.add_fixed_in_frame_mobjects(calculation_text)
        self.play(FadeIn(calculation_text))
        T += 3

        # self.wait(3)
        # btw_str = [
        #     "Usually, when people say that a die is fair, ",
        #     "they mean that all its sides are equally likely. ",
        #     "For us, fairness is instead a property of ",
        #     r"a group of dice, so don’t be confused. \smiley "
        # ]
        # myTemplate = TexTemplate()
        # myTemplate.add_to_preamble(r"\usepackage{wasysym}")

        # btw_text_list = [
        #     Tex(str, color = text_color, tex_template = myTemplate).scale(0.6)
        #     for str in btw_str
        # ]
        # btw_text = Group(*btw_text_list).arrange(DOWN, buff = 0.05).shift(3.3*DOWN + 4.1*LEFT)
        # for txt in btw_text_list:
        #     txt.align_to(btw_text_list[0], LEFT)

        # self.add_fixed_in_frame_mobjects(*btw_text_list)
        # self.play(*[FadeIn(text) for text in btw_text_list])
        # self.wait()
        # self.play(*[FadeOut(text) for text in btw_text_list])
        self.wait(5)
        self.play(FadeOut(calculation_text))

        self.wait(70 - T)
        self.play(*[FadeOut(o) for o in self.mobjects])
        return

        s = fair_strings[0]
        ntable = dice_table(string_to_list(s), scale=1, col_widths=[0.4] * 7)
        ntable.shift(2 * LEFT)

        self.play(*[FadeIn(t) for t in table], run_time=0.01)

        move_anims = []
        for i in range(3):
            for j in range(6):
                move_anims.append(
                    table[i * 7 + j + 1].animate.move_to(
                        ntable[i * 7 + j + 1].get_center()
                    )
                )

        self.play(
            FadeOut(axes),
            FadeOut(skeleton),
            FadeOut(calculation_text),
            *[FadeOut(l) for l in order_labels],
            *[FadeOut(l) for l in labels[0] + labels[1] + labels[2]],
            *[FadeOut(cube) for cube in all_cubes],
            *move_anims,
        )
        self.wait()

        return


class Counting(Scene):
    def construct(self):
        # copy pasted from above

        s = fair_strings[0]
        table = dice_table(string_to_list(s), scale=1, col_widths=[0.4] * 7)
        table.shift(2 * LEFT)

        self.add(*table)

        anims = []
        numbers = [None] * 18
        for i in range(3):
            for j in range(6):
                n = three_dice[i][j]
                numbers[n - 1] = Tex(str(n), color=text_color).move_to(
                    table[i * 7 + j + 1].get_center()
                )
                numbers[n - 1].generate_target()
                numbers[n - 1].target.move_to(
                    2 * RIGHT
                    + 1 * UP
                    + ((n - 1) // 5) * 0.7 * DOWN
                    + ((n - 1) % 5) * 0.7 * RIGHT
                )

                anims.append(
                    Transform(
                        table[7 * i + j + 1],
                        Tex(r"$\_$", color=text_color)
                        .move_to(table[i * 7 + j + 1].get_center())
                        .shift(0.2 * DOWN)
                        .scale(1.5),
                    )
                )
        self.play(*[MoveToTarget(num) for num in numbers], *anims)
        self.wait()

        # change to primes and back

        primes = [
            2,
            3,
            5,
            7,
            11,
            13,
            17,
            19,
            23,
            29,
            31,
            37,
            41,
            43,
            47,
            53,
            59,
            61,
            67,
            71,
            73,
            79,
            83,
            89,
            97,
        ]

        anims1 = []
        anims2 = []
        for i in range(len(numbers)):
            anims1.append(
                Transform(
                    numbers[i],
                    Tex(str(primes[i]), color=text_color).move_to(
                        numbers[i].get_center()
                    ),
                )
            )
            anims2.append(
                Transform(
                    numbers[i],
                    Tex(str(i + 1), color=text_color).move_to(numbers[i].get_center()),
                )
            )

        lr = 0.1
        self.play(AnimationGroup(*anims1, lag_ratio=lr))
        self.wait()
        self.play(AnimationGroup(*anims2, lag_ratio=lr))
        self.wait()

        # computation

        sht = 0.1 * LEFT
        comp = []
        comp.append(
            Tex("${18 \choose 6}$", color=text_color).move_to(3 * LEFT + 3 * DOWN)
        )
        comp.append(
            Tex("$\cdot {12 \choose 6}$", color=text_color)
            .next_to(comp[0], RIGHT)
            .shift(sht)
        )
        comp.append(
            Tex("$\cdot {6 \choose 6}$", color=text_color)
            .next_to(comp[1], RIGHT)
            .shift(sht)
        )
        comp.append(Tex("$=  17\,153\,136$", color=text_color).next_to(comp[2], RIGHT))

        for i in range(3):
            anims = []
            for j in range(6):
                anims.append(
                    numbers[three_dice[i][j] - 1]
                    .animate.move_to(table[i * 7 + j + 1].get_center())
                    .shift(0.2 * UP)
                )
            # self.add_sound(random_whoosh_file())
            self.play(*anims, FadeIn(comp[i]))
            self.wait()

        self.play(FadeIn(comp[3]))
        self.wait()

        # fly letters to the position of next animation
        sc = sc_examples
        s = fair_strings[0]
        ntable = dice_table(string_to_list(s), scale=sc)
        ntable.shift(pos_fst_example)

        self.play(
            FadeOut(table[1 + 7 * 0 : 7 * 1]),
            FadeOut(table[1 + 7 * 1 : 7 * 2]),
            FadeOut(table[1 + 7 * 2 : 7 * 3]),
            *[FadeOut(c) for c in comp],
        )

        anims = []
        for i in range(3):
            anims.append(Transform(table[i * 7], ntable[7 * i]))
            for j in range(6):
                anims.append(
                    # numbers[three_dice[i][j]-1].animate.move_to(
                    Transform(numbers[three_dice[i][j] - 1], ntable[7 * i + j + 1])
                )

        self.play(*anims)
        self.wait()


class FairExamples(Scene):
    def construct(self):
        self.next_section(skip_animations=False)
        fair_dice = []

        sc = sc_examples
        tables = []
        for i, s in enumerate(fair_strings):
            table = dice_table(string_to_list(s), scale=sc)
            table.shift(pos_fst_example + (i // 3) * 3 * DOWN + (i % 3) * 4 * RIGHT)
            tables.append(table)
            # fair_dice.append(table)

        tables_group = VGroup(*tables).arrange_in_grid(rows=2, buff=0.8).center()
        tables_group.shift(pos_fst_example - tables[0].get_center())

        self.add(tables[0])
        self.play(AnimationGroup(*[FadeIn(t) for t in tables[1:]], lag_ratio=0.3))
        self.wait()

        msg = (
            Tex(
                "(up to permuting the dice or replacing each $x$ by $19-x$)",
                color=text_color,
            )
            .move_to(3.5 * DOWN)
            .scale(0.8)
        )
        self.play(FadeIn(msg))
        self.wait(2)
        self.play(FadeOut(msg))
        self.wait()
        self.play(Circumscribe(tables[0], color=RED))
        self.wait()
        self.play(
            AnimationGroup(
                *[FadeOut(t) for t in tables],
            )
        )
        self.wait()

        # solution for four dice
        fair_dice4 = dice_table(four_dice, scale=1.3).center()
        self.play(FadeIn(fair_dice4))
        self.wait()

        self.play(*[FadeOut(line) for line in fair_dice4])
        self.wait()

        # smileys

        smiley_table = [
            Tex("3 players: ", color=text_color),
            Tex("6 sides ", color=text_color),
            ImageMobject("s1.png"),
            Tex("4 players: ", color=text_color),
            Tex("12 sides ", color=text_color),
            ImageMobject("s2.png"),
            Tex("5 players: ", color=text_color),
            Tex("$\ge 30$ sides ", color=text_color),
            ImageMobject("s3.png"),
        ]
        smiley_table = Group(*smiley_table).arrange_in_grid(
            rows=3, buff=MED_LARGE_BUFF, col_widths=[2, 2, 2]
        )

        self.play(
            AnimationGroup(
                AnimationGroup(
                    *[FadeIn(o) for o in smiley_table[0:3]],
                ),
                AnimationGroup(
                    *[FadeIn(o) for o in smiley_table[3:6]],
                ),
                AnimationGroup(
                    *[FadeIn(o) for o in smiley_table[6:]],
                ),
                lag_ratio=0.6,
            )
        )
        self.wait()
        self.play(*[FadeOut(o) for o in smiley_table])
        self.wait()

        # explanation starts

        sc_title = 1.5
        ttl = Tex(r"{{three }}{{6}}{{-sided dic}}{{e}}", color=text_color).scale(2)
        ttl2 = Tex(r"{{three }}{{5}}{{-sided dic}}{{e??}}", color=text_color).scale(2)
        ttl3 = (
            Tex(r"{{three }}{{5}}{{-sided dic}}{{e??}}", color=text_color)
            .scale(sc_title)
            .shift(2.5 * UP + 1 * RIGHT)
        )
        self.play(FadeIn(ttl))
        self.wait()
        self.play(Transform(ttl, ttl2))
        self.wait()
        self.play(Transform(ttl, ttl3))
        self.wait()

        t1 = (
            Tex(r"{{$5^3=125$}}{{ possible outcomes}}", color=text_color)
            .next_to(ttl3, DOWN)
            .shift(DOWN)
        )
        t1new = Tex(r"{{$125$}}{{ possible outcomes}}", color=text_color).move_to(
            t1.get_center()
        )
        t2 = Tex(r"{{$3! = 6$ }}{{equally-sized groups}}", color=text_color).next_to(
            t1, DOWN
        )
        t3 = Tex(
            r"{{$\frac{125}{6}$}}{{ outcomes per group}}", color=text_color
        ).next_to(t2, DOWN)
        t3new = Tex(
            r"{{$20.833\dots$}}{{ outcomes per group}}", color=text_color
        ).move_to(t3.get_center())

        bubble, cent = create_bubble(
            t1.get_left() + 1.5 * LEFT, scale=1.3, color=text_color, length_scale=1.2
        )
        cube = create_cube(cent, scale=0.6, color=text_color)
        self.play(FadeIn(t1), *[FadeIn(b) for b in bubble], *[FadeIn(c) for c in cube])
        self.wait()

        self.play(
            FadeIn(t2),
            *[FadeOut(c) for c in cube],
        )
        self.play(
            *[
                b.animate.shift((t2.get_center() - t1.get_center())[1] * UP)
                for b in bubble
            ]
        )

        strs = [
            r"$A<B<C$",
            r"$A<C<B$",
            r"$B<A<C$",
            r"$B<C<A$",
            r"$C<A<B$",
            r"$C<B<A$",
        ]
        strs_tex = [Tex(s, color=c).scale(0.5) for s, c in zip(strs, colors[0:6])]
        strs_table = VGroup(*strs_tex).arrange_in_grid(rows=3, buff=0.2)
        newcent = (
            cent + (t2.get_center() - t1.get_center())[1] * UP + 0.7 * UP + 0.1 * LEFT
        )
        strs_table.shift(newcent)

        self.play(*[FadeIn(s) for s in strs_table])
        self.wait()

        self.play(FadeIn(t3), *[FadeOut(o) for o in strs_tex + bubble])
        self.wait()

        self.play(
            Transform(t3, t3new),
        )
        self.wait()

        ttl5 = (
            Tex(r"{{five }}{{$s$}}{{-sided dic}}{{e}}", color=text_color)
            .scale(sc_title)
            .move_to(ttl3.get_center())
            .shift(1 * LEFT)
        )
        t15 = (
            Tex(r"{{$s^5$}}{{ possible outcomes}}", color=text_color)
            .move_to(t1.get_center())
            .shift(1 * LEFT)
        )
        t15u = (
            Tex(r"{{\_ }}{{ possible outcomes}}", color=text_color)
            .move_to(t1.get_center())
            .shift(1 * LEFT)
        )
        t25 = (
            Tex(r"{{$5!$ }}{{equally-sized groups}}", color=text_color)
            .move_to(t2.get_center())
            .shift(1 * LEFT)
        )
        t25u = (
            Tex(r"{{\_ }}{{equally-sized groups}}", color=text_color)
            .move_to(t2.get_center())
            .shift(1 * LEFT)
        )
        t35 = (
            Tex(r"{{$\frac{s^5}{5!}$}}{{ outcomes per group}}", color=text_color)
            .move_to(t3.get_center())
            .shift(1 * LEFT)
        )
        t35u = (
            Tex(r"{{\_ }}{{ outcomes per group}}", color=text_color)
            .move_to(t3.get_center())
            .shift(1 * LEFT)
        )

        tdiv = (
            Tex(r"{{$5!$}}{{$\mid$}}{{$ s^5$}}", color=text_color)
            .next_to(t2, DOWN)
            .shift(1 * LEFT)
        )
        tdiv2 = Tex(
            r"{{$2\cdot 3 \cdot 4 \cdot 5$}}{{$\;\mid\;$}}{{$ s^5$}}", color=text_color
        ).move_to(tdiv.get_center())
        t4 = (
            Tex(r"{{$2, 3, 5$}}{{$\;\mid\;$}}{{$ s$}}", color=text_color)
            .next_to(tdiv2, DOWN)
            .shift(0.5 * DOWN)
        )
        tdiv2.move_to(t4.get_center())
        t5 = Tex(r"{{$s \ge $}}{{$\,2 \cdot 3 \cdot 5$}}", color=text_color).next_to(
            t4, DOWN
        )
        t52 = Tex(r"{{$s \ge $}}{{$\,30$}}", color=text_color).move_to(t5.get_center())

        self.play(
            Transform(ttl, ttl5),
            Transform(t1, t15u),
            Transform(t2, t25u),
            Transform(t3, t35u),
        )
        self.wait()
        self.play(Circumscribe(ttl[1], color=RED))
        self.wait()
        self.play(Transform(t1, t15))
        self.wait()
        self.play(Transform(t2, t25))
        self.wait()
        self.play(Transform(t3, t35))
        self.wait()
        self.play(FadeIn(tdiv2))
        self.wait()

        self.play(
            Transform(tdiv2[0][0:4], t4[0][0:4]),
            FadeOut(tdiv2[0][4:6]),
            Transform(tdiv2[0][-1], t4[0][-1]),
            Transform(tdiv2[1:], t4[1:]),
        )
        self.wait()
        self.wait()
        self.play(FadeIn(t5))
        self.wait()
        self.play(Transform(t5, t52))
        self.wait()

        # to same pro sedm

        ttl7 = (
            Tex(r"{{seven }}{{$s$}}{{-sided dic}}{{e}}", color=text_color)
            .scale(sc_title)
            .move_to(ttl3.get_center())
            .shift(1 * LEFT)
        )
        t17 = Tex(r"{{$s^7$}}{{ possible outcomes}}", color=text_color).move_to(
            t1.get_center()
        )
        t27 = Tex(r"{{$7!$ }}{{equally-sized groups}}", color=text_color).move_to(
            t2.get_center()
        )
        t37 = Tex(
            r"{{$\frac{s^7}{7!}$}}{{ outcomes per group}}", color=text_color
        ).move_to(t3.get_center())

        tdiv7 = Tex(
            r"{{$7 \cdot 6 \cdot 5\cdot 4 \cdot 3 \cdot 2$}}{{$\;\mid\;$}}{{$ s^7$}}",
            color=text_color,
        ).move_to(tdiv.get_center())
        t47 = Tex(r"{{$2, 3, 5, 7$}}{{$\;\mid\;$}}{{$ s$}}", color=text_color).move_to(
            t4.get_center()
        )
        t57 = Tex(r"{{$s \ge $}}{{$\,210$}}", color=text_color).move_to(t5.get_center())

        self.play(
            AnimationGroup(
                Transform(ttl, ttl7),
                Transform(t1, t17),
                Transform(t2, t27),
                Transform(t3, t37),
                AnimationGroup(
                    Transform(tdiv2[0][0:4], t47[0][0:4]),
                    Transform(tdiv2[0][-1], t47[0][4]),
                    FadeIn(t47[0][5:]),
                    Transform(tdiv2[1:], t47[1:]),
                ),
                Transform(t5, t57),
                lag_ratio=0.3,
            )
        )
        self.wait()
