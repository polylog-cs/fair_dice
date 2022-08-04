from util import *

class Polylog(Scene):
    def construct(self):
        authors = Tex(
            r"\textbf{Tom Gavenčiak, Václav Rozhoň, Václav Volhejn}", 
            color=text_color,
            font_size = 40,
        ).shift(
            3*DOWN + 0*LEFT
        )

        channel_name = Tex(r"polylog", color=text_color)
        channel_name.scale(4).shift(1 * UP)


        self.play(
           Write(authors),
           Write(channel_name)
        )

        self.wait()

        self.play(
            *[FadeOut(o) for o in self.mobjects]
        )
        self.wait()

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


        # first just two examples
        sqab = squares[0][4]
        sqba = squares[3][1]
        txtab = Tex(r"$A<B$", color = DARK_GRAY).scale(0.5).move_to(sqab.get_center())
        txtba = Tex(r"$A>B$", color = DARK_GRAY).scale(0.5).move_to(sqba.get_center())

        self.play(
            AnimationGroup(
                FadeIn(sqab),
                FadeIn(txtab),
            )
        )
        self.play(
            Circumscribe(dice_numbers[0][0], color = RED),
        )
        self.play(
            Circumscribe(dice_numbers[1][4], color = RED)
        )
        self.wait()

        self.play(
            FadeIn(sqba),
            FadeIn(txtba)
        )
        self.play(
            Circumscribe(dice_numbers[1][1], color = BLUE),
        )
        self.play(
            Circumscribe(dice_numbers[0][3], color = BLUE)
        )
        self.wait()

        self.play(
            FadeOut(txtab),
            FadeOut(txtba),
            FadeOut(sqab),
            FadeOut(sqba)
        )
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
        self.play(
            *[FadeOut(o) for o in self.mobjects]
        )
        self.wait()

        # the other solution

        # orig_positions = [
        #     [num.get_center() for num in dice_numbers[0]],
        #     [num.get_center() for num in dice_numbers[1]]
        # ]
        

        # dice_numbers_sorted = list(itertools.chain(*zip(dice_numbers[0], dice_numbers[1])))
        # for i, num in enumerate(dice_numbers_sorted):
        #     num.generate_target()
        #     if i == 0:
        #         num.target.move_to(6.5*LEFT + 3.3*UP)
        #     elif i == 6:
        #         num.target.move_to(dice_numbers[0][0].target.get_center()).next_to(dice_numbers[0][0].target, DOWN)
        #     else:
        #         num.target.move_to(dice_numbers_sorted[i-1].target.get_center()).next_to(dice_numbers_sorted[i-1].target, RIGHT).shift(0.2*RIGHT)

        # self.play(
        #     *[MoveToTarget(num) for num in dice_numbers_sorted],
        #     *[FadeOut(square) for line in squares for square in line]
        # )
        # self.wait()

        # self.play(
        #     AnimationGroup(
        #         dice_numbers_sorted[0].animate.move_to(orig_positions[0][0]),
        #         dice_numbers_sorted[1].animate.move_to(orig_positions[0][1]),
        #         dice_numbers_sorted[2].animate.move_to(orig_positions[0][2]),
        #         lag_ratio = 0.3
        #     )
        # )
        # self.wait()

        # self.play(
        #     AnimationGroup(
        #         dice_numbers_sorted[3].animate.move_to(orig_positions[1][0]),
        #         dice_numbers_sorted[4].animate.move_to(orig_positions[1][1]),
        #         dice_numbers_sorted[5].animate.move_to(orig_positions[1][2]),
        #         dice_numbers_sorted[6].animate.move_to(orig_positions[0][3]),
        #         dice_numbers_sorted[7].animate.move_to(orig_positions[0][4]),
        #         dice_numbers_sorted[8].animate.move_to(orig_positions[0][5]),
        #         lag_ratio = 0.3
        #     )
        # )
        # self.wait()

        # self.play(
        #     AnimationGroup(
        #         dice_numbers_sorted[9].animate.move_to(orig_positions[1][3]),
        #         dice_numbers_sorted[10].animate.move_to(orig_positions[1][4]),
        #         dice_numbers_sorted[11].animate.move_to(orig_positions[1][5]),
        #         lag_ratio = 0.3
        #     )
        # )
        # self.wait()

        # for i in range(3):
        #     for j in range(6):
        #         squares[i][j].set_color(RED)
        # for i in range(3, 6):
        #     for j in range(6):
        #         squares[i][j].set_color(BLUE)

        # self.play(
        #     *[FadeIn(square) for line in squares for square in line]
        # )
        # self.wait()

#TODO put camera to the right place
pos_three_dice = 3*UP
class DiceCubeLeft(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            phi = 70*DEGREES,  # pitch
            theta = -120*DEGREES,  # yaw
        )
        self.begin_ambient_camera_rotation(
            rate = PI/10,
            about = "theta"
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
            x_range=(0, n, 1), x_length=n,
            y_range=(0, n, 1), y_length=n,
            z_range=(0, n, 1), z_length=n,
        ).shift((dirs[0] + dirs[1]) * (n - 1) / 2 - dirs[2] * 0.5 + global_shift)
        
        axes.set_color(text_color)
        self.add(axes)
        base = Cube(side_length = 1, fill_color=BLACK).move_to(ORIGIN).shift(global_shift)

        # self.add(
        #     base,
        #     Cube(side_length = 1, fill_color = RED).move_to(ORIGIN).shift(dirs[0]),
        #     Cube(side_length = 1, fill_color = GREEN).move_to(ORIGIN).shift(dirs[1]),
        #     Cube(side_length = 1, fill_color = BLUE).move_to(ORIGIN).shift(dirs[2]),
        # )

        labels = []
        
        for i in range(3):
            labels.append([])
            for j in range(len(dice[i])):
                l = Tex(
                    str(dice[i][j]) if j < len(dice[i]) else "ABC"[i],
                    # color = [RED, GREEN, BLUE][i],
                    color=text_color,
                ).scale(0.8)
                # if i == 1:
                #     l.rotate_about_origin(90*DEGREES,OUT)
                # if i == 2:
                #     l.rotate_about_origin(45*DEGREES, OUT).rotate_about_origin(90*DEGREES, RIGHT-DOWN)
                
                # labels[i].append(l.move_to(base.get_center()).shift(DOWN + LEFT + IN).shift(dirs[i] * (j + 1)))
                # continue
                if j == 0:
                    labels[i].append(
                        l.shift(nexts[i] + 0.5*nexts[i] + global_shift)
                        # l.move_to(base.get_center())
                    )   
                else:
                    labels[i].append(
                        l.move_to(labels[i][j-1].get_center() + dirs[i])
                    )
            
            l = Tex(
                "ABC"[i],
                color=text_color,
            )

            labels[i].append(
                l.move_to(labels[i][-1].get_center() + dirs[i] * 2)
            )



        self.add_fixed_orientation_mobjects(
            *labels[0],
            *labels[1],
            *labels[2],
        )

        all_cubes = []

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
                                    fill_color = colors[it],
                                    fill_opacity=1.0,
                                ).move_to(ORIGIN).shift(i*dirs[0]+j*dirs[1]+k*dirs[2] + global_shift)
                            )
            
            all_cubes += cubes_to_appear

            if cubes_to_appear != []:
                letters = ["ABC"[p] for p in perm]
                order_label = Tex(
                    f"${letters[0]} < {letters[1]} < {letters[2]}$",
                    color=colors[it],
                ).shift(5*RIGHT + 3 * UP)
                self.add_fixed_in_frame_mobjects(order_label)

                self.play(
                    *[FadeIn(cube) for cube in cubes_to_appear],
                    FadeIn(order_label),
                    run_time = 0.5
                )
                self.wait(2.5)
                self.play(
                    *[FadeOut(cube) for cube in cubes_to_appear],
                    FadeOut(order_label),
                    run_time = 0.5
                )
                self.wait()

        self.play(*[FadeIn(cube) for cube in all_cubes])
        self.wait(1)
        calculation_text = Tex(r"$\frac{6^3}{3!} = 36$", color=BASE2).scale(2)
        self.add_fixed_in_frame_mobjects(calculation_text)
        self.play(FadeIn(calculation_text))
        self.wait(5)
        self.play(FadeOut(calculation_text))
        self.wait(15)

        # self.stop_ambient_camera_rotation()
        # self.play(*[FadeOut(cube) for cube in all_cubes])
        # self.move_camera(phi=90*DEGREES, theta=0)
        # self.wait(1)

class DiceCubeRight(Scene):
    def construct(self):
        
        lines = []
        for i, die in enumerate(three_dice):
            s = r"{{" + string.ascii_uppercase[i] + r": }}"
            for j in range(len(die)):
                s += r"{{" + str(dice[i][j]) + r"}}"
                if j != len(die)-1:
                    s += r"{{, }}"
            lines.append(
                Tex(s, color = text_color)
            )
            if i == 0:
                lines[i].move_to(pos_three_dice)
            else:
                lines[i].next_to(lines[i-1], DOWN)

        self.play(
            *[FadeIn(line) for line in lines]
        )
        self.wait()

        perms = [
            "$A < B < C$",
            "$A < C < B$",
            "$B < A < C$",
            "$B < C < A$",
            "$C < A < B$",
            "$C < B < A$",
        ]
        for i in range(6):
            self.play(
                FadeIn(
                    Tex(perms[i], color = colors[i]).move_to(
                        5*RIGHT + 1*DOWN + (i*DOWN + 2.5*UP)*0.8
                    )
                ),
                run_time = 0.5
            )
            self.wait(3)

class FairExamples(Scene):
    def construct(self):
        self.next_section(skip_animations=False)
        fair_dice = []
        sc = 0.9

        tables = []
        for i, s in enumerate(fair_strings):
            table = dice_table(string_to_list(s), scale=sc)
            table.shift(4.5*LEFT + 1.5*UP + (i//3)*3*DOWN + (i%3)*4*RIGHT)
            tables.append(table)
            # fair_dice.append(table)

        tables = VGroup(*tables).arrange_in_grid(rows=2, buff=0.8).center()

        self.play(
            FadeIn(tables)
            # AnimationGroup(
            #     *[FadeIn(str) for lines in fair_dice for str in lines],
            # )
        )
        self.wait()  

        msg = Tex("(up to permuting the dice or replacing each $x$ by $19-x$)", color = text_color).move_to(3.5*DOWN).scale(0.8)
        self.play(
            FadeIn(msg)
        )    
        self.wait()
        self.play(
            FadeOut(msg)
        )
        self.wait()
        self.play(
            FadeOut(tables)
            #*[str.animate.shift(4.5*RIGHT) for str in fair_dice[0]]
        )
        self.wait()

        # solution for four dice
        fair_dice4 = dice_table(four_dice, scale=1.3).center()
        self.play(
            FadeIn(fair_dice4)
        )
        self.wait()

        self.play(
            *[FadeOut(line) for line in fair_dice4]
        )
        self.wait()

        ttl = Tex(r"{{three }}{{6}}{{-sided dic}}{{e}}", color = text_color).scale(2)
        ttl2 = Tex(r"{{three }}{{5}}{{-sided dic}}{{e??}}", color = text_color).scale(2)
        ttl3 = Tex(r"{{three }}{{5}}{{-sided dic}}{{e??}}", color = text_color).shift(2*UP)
        self.play(
            FadeIn(ttl)
        )
        self.wait()
        self.play(
            Transform(ttl, ttl2)
        )
        self.wait()
        self.play(Transform(ttl, ttl3))
        self.wait()

        t1 = Tex("{{$5^3$}}{{ possible outcomes}}", color = text_color).next_to(ttl3, DOWN).shift(DOWN)
        t1new = Tex("{{$125$}}{{ possible outcomes}}", color = text_color).move_to(t1.get_center())
        t2 = Tex("{{6 }}{{equally-sized groups}}", color = text_color).next_to(t1, DOWN)
        t3 = Tex(r"{{$\frac{125}{6}$}}{{ outcomes per group}}", color = text_color).next_to(t2, DOWN)
        t3new = Tex(r"{{$20.833\dots$}}{{ outcomes per group}}", color = text_color).move_to(t3.get_center())

        self.play(
            Succession(
                FadeIn(t1),
                Wait(),
            )
        )
        self.play(
            Transform(t1, t1new)
        )
        self.wait()
        self.play(
            Succession(
                FadeIn(t2),
                Wait(),
                FadeIn(t3),
                Wait(),
            )
        )
        self.play(
            Transform(t3, t3new),
        )
        self.wait()

        ttl5 = Tex(r"{{five }}{{s}}{{-sided dic}}{{e}}", color = text_color).move_to(ttl3.get_center())
        t15 = Tex(r"{{$s^5$}}{{ possible outcomes}}", color = text_color).move_to(t1.get_center())
        t25 = Tex(r"{{$5!$ }}{{equally-sized groups}}", color = text_color).move_to(t2.get_center())
        t35 = Tex(r"{{$\frac{s^5}{5!}$}}{{ outcomes per group}}", color = text_color).move_to(t3.get_center())

        tdiv = Tex(r"{{$5!$}}{{$\mid$}}{{$ s^5$}}", color = text_color).next_to(t2, DOWN)
        tdiv2 = Tex(r"{{$5\cdot 4 \cdot 3 \cdot 2$}}{{$\mid$}}{{$ s^5$}}", color = text_color).move_to(tdiv.get_center())
        t4 = Tex(r"$2, 3, 5 \mid s$", color = text_color).next_to(tdiv2, DOWN).shift(0.5*DOWN)
        t5 = Tex(r"{{$s \ge $}}{{$\,2 \cdot 3 \cdot 5$}}", color = text_color).next_to(t4, DOWN)
        t52= Tex(r"{{$s \ge $}}{{$\,30$}}", color = text_color).move_to(t5.get_center())

        self.play(
            Transform(ttl, ttl5)
        )
        self.wait()
        self.play(
            Transform(t1, t15)
        )
        self.wait()
        self.play(
            Transform(t2, t25)
        )
        self.wait()
        self.play(
            Transform(t3, t35)
        )
        self.wait()
        self.play(
            Succession(
                FadeIn(t4),
                Wait(),
                FadeIn(t5),
                Wait()
            )
        )
        self.play(
            Transform(t5, t52)
        )
        self.wait()



        #to same pro sedm

        ttl7 = Tex(r"{{seven }}{{s}}{{-sided dic}}{{e}}", color = text_color).move_to(ttl3.get_center())
        t17 = Tex(r"{{$s^7$}}{{ possible outcomes}}", color = text_color).move_to(t1.get_center())
        t27 = Tex(r"{{$7!$ }}{{equally-sized groups}}", color = text_color).move_to(t2.get_center())
        t37 = Tex(r"{{$\frac{s^7}{7!}$}}{{ outcomes per group}}", color = text_color).move_to(t3.get_center())

        tdiv7 = Tex(r"{{$7 \cdot 6 \cdot 5\cdot 4 \cdot 3 \cdot 2$}}{{$\mid$}}{{$ s^7$}}", color = text_color).move_to(tdiv.get_center())
        t47 = Tex(r"{{$2, 3, 5$}}{{$, 7 $}}{{$\mid s$}}", color = text_color).next_to(tdiv2, DOWN).shift(0.5*DOWN)
        t57= Tex(r"{{$s \ge $}}{{$\,210$}}", color = text_color).move_to(t5.get_center())

        self.play(
            AnimationGroup(
                Transform(ttl, ttl7),
                Transform(t1, t17),
                Transform(t2, t27),
                Transform(t3, t37),
                Transform(t4, t47),
                Transform(t5, t57),
                lag_ratio = 0.3,
            )
        )
        self.wait()

        #problik
        self.play(
            *[FadeOut(o) for o in self.mobjects]
        )
        txt = r"\
            If you generalize this argument for general number of players $n$, \
            you can use a so-called prime number theorem which is basically saying that there are about $n/\textrm{ln}\, n$ primes smaller than n. \
            This implies that the product of primes less than $n$ (primorial) grows like the exponential function of $n$. \
            Hence the number of sides of same-sized fair dice grows exponentially. \
        "
        txt2 = r"\
            Can you show that at least one die has to have exponentially many sides even if the dice are allowed to have different numbers of sides? (hint in video description) \
            Can you show that in that case all dice have to have exponentially many sides? (we cannot) \
        "

        l1 = Tex(txt, color = text_color).scale(0.7).shift(1*UP)
        l2 = Tex(txt2, color = text_color).scale(0.7).next_to(l1, DOWN).shift(DOWN)

        self.play(
            AnimationGroup(
                FadeIn(l1),
                FadeIn(l2)
            ),
            run_time = 0.3
        )
        self.wait()
        self.play(
            AnimationGroup(
                FadeOut(l1),
                FadeOut(l2)
            ),
            run_time = 0.3
        )
        self.wait()







class Counting(Scene):
    def construct(self):
        #copy pasted from above
        lines = list_to_lines(three_dice, pos_three_dice)

        self.add(
            *lines
        )

        self.play(
            *[line.animate.shift(-pos_three_dice+ 2*LEFT) for line in lines]
        )
        self.wait()

        anims = []
        numbers = [None]*18
        for i in range(3):
            for j in range(6):
                n = three_dice[i][j]
                numbers[n-1] = Tex(str(n), color = text_color).move_to(lines[i][1+2*j].get_center())
                numbers[n-1].generate_target()
                numbers[n-1].target.move_to(2*RIGHT + 1*UP + ((n-1) // 5)*0.7*DOWN + ((n-1)%5)*0.7*RIGHT)

                anims.append(
                    Transform(lines[i][1 + 2*j], Tex(r"$\_$", color = text_color).move_to(lines[i][1+2*j].get_center()).shift(0.2*DOWN).scale(1.5))
                )
        self.play(
            *[MoveToTarget(num) for num in numbers],
            *anims
        )
        self.wait()

        #computation 

        sht = 0.1*LEFT
        comp = []
        comp.append(Tex("${18 \choose 6}$", color = text_color).move_to(3*LEFT + 3*DOWN))
        comp.append(Tex("$\cdot {12 \choose 6}$", color = text_color).next_to(comp[0], RIGHT).shift(sht))
        comp.append(Tex("$\cdot1$", color = text_color).next_to(comp[1], RIGHT).shift(sht))
        comp.append(Tex("$=  17\,153\,136$", color = text_color).next_to(comp[2], RIGHT))

        for i in range(3):
            anims = []
            for j in range(6):
                anims.append(
                    numbers[three_dice[i][j]-1].animate.move_to(
                        lines[i][1 + 2*j].get_center()
                    ).shift(0.2*UP)
                )
            self.play(
                *anims,
                FadeIn(comp[i])
            )
            self.wait()
        
        self.play(
            FadeIn(comp[3])
        )
        self.wait()




