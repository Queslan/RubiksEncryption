

class FullCube:
    def __init__(self, elements):
        self.elements = elements

    def make_invert(self, fun):
        for x in range(3):
            fun()

    def up(self):  # Upper Rotation
        c = self.elements
        c[9], c[10], c[11], \
        c[18], c[19], c[20], \
        c[27], c[28], c[29], \
        c[36], c[37], c[38], \
        c[0], c[1], c[2], \
        c[3], c[5], \
        c[6], c[7], c[8] \
        = \
        c[18], c[19], c[20], \
        c[27], c[28], c[29], \
        c[36], c[37], c[38], \
        c[9], c[10], c[11], \
        c[6], c[3], c[0], \
        c[7], c[1], \
        c[8], c[5], c[2]

    def up_invert(self):
        self.make_invert(self.up)

    def down(self):  # Down Rotation
        c = self.elements
        c[15], c[16], c[17], \
        c[24], c[25], c[26], \
        c[33], c[34], c[35], \
        c[42], c[43], c[44], \
        c[45], c[46], c[47], \
        c[48], c[50], \
        c[51], c[52], c[53] \
        = \
        c[42], c[43], c[44], \
        c[15], c[16], c[17], \
        c[24], c[25], c[26], \
        c[33], c[34], c[35], \
        c[51], c[48], c[45], \
        c[52], c[46], \
        c[53], c[50], c[47]

    def down_invert(self):
        self.make_invert(self.down)

    def front(self):  # Front Rotation
        c = self.elements
        c[6], c[7], c[8], \
        c[11], c[14], c[17], \
        c[27], c[30], c[33], \
        c[45], c[46], c[47], \
        c[18], c[19], c[20], \
        c[21], c[23], \
        c[24], c[25], c[26] \
        = \
        c[17], c[14], c[11], \
        c[45], c[46], c[47], \
        c[6], c[7], c[8], \
        c[33], c[30], c[27], \
        c[24], c[21], c[18], \
        c[25], c[19], \
        c[26], c[23], c[20]

    def front_invert(self):
        self.make_invert(self.front)

    def back(self):  # Front Rotation
        c = self.elements
        c[0], c[1], c[2], \
        c[29], c[32], c[35], \
        c[51], c[52], c[53], \
        c[9], c[12], c[15], \
        c[36], c[37], c[38], \
        c[39], c[41], \
        c[42], c[43], c[44] \
        = \
        c[29], c[32], c[35], \
        c[53], c[52], c[51], \
        c[9], c[12], c[15], \
        c[2], c[1], c[0], \
        c[42], c[39], c[36], \
        c[43], c[37], \
        c[44], c[41], c[38]

    def back_invert(self):
        self.make_invert(self.back)

    def right(self):  # Right Rotation
        c = self.elements
        c[8], c[5], c[2], \
        c[20], c[23], c[26], \
        c[47], c[50], c[53], \
        c[36], c[39], c[42], \
        c[27], c[28], c[29], \
        c[30], c[32], \
        c[33], c[34], c[35] \
        = \
        c[26], c[23], c[20], \
        c[47], c[50], c[53], \
        c[42], c[39], c[36], \
        c[8], c[5], c[2], \
        c[33], c[30], c[27], \
        c[34], c[28], \
        c[35], c[32], c[29]

    def right_invert(self):
        self.make_invert(self.right)

    def left(self):  # Left Rotation
        c = self.elements
        c[0], c[3], c[6], \
        c[18], c[21], c[24], \
        c[51], c[48], c[45], \
        c[38], c[41], c[44], \
        c[9], c[10], c[11], \
        c[12], c[14], \
        c[15], c[16], c[17] \
        = \
        c[44], c[41], c[38], \
        c[0], c[3], c[6], \
        c[24], c[21], c[18], \
        c[51], c[48], c[45], \
        c[15], c[12], c[9], \
        c[16], c[10],\
        c[17], c[14], c[11]

    def left_invert(self):
        self.make_invert(self.left)

    def middle_rotation(self):  # Middle Right Rotation
        c = self.elements
        c[21], c[22], c[23], \
        c[30], c[31], c[32], \
        c[39], c[40], c[41], \
        c[12], c[13], c[14], \
        = \
        c[30], c[31], c[32], \
        c[39], c[40], c[41], \
        c[12], c[13], c[14], \
        c[21], c[22], c[23]

    def change_front(self): # Change front to be color from the right
        self.up()
        self.middle_rotation()
        self.down_invert()

    def check_cross_positions(self):
        elements = self.elements
        upper_color = elements[4].color
        possible_moves = []
        if elements[1].color != upper_color:
            possible_moves.append('B')
        if elements[3].color != upper_color:
            possible_moves.append('L')
        if elements[5].color != upper_color:
            possible_moves.append('R')
        if elements[7].color != upper_color:
            possible_moves.append('F')

        return possible_moves

    def make_upper_cross(self):
        possible_moves = self.check_cross_positions()
        while len(possible_moves) != 0:
            self.one_movers()
            self.two_movers()
            self.up()
            possible_moves = self.check_cross_positions()
            self.move_cube(possible_moves)

    def one_movers(self):
        elements = self.elements
        upper_color = elements[4].color
        changes_flag = True
        possible_moves = self.check_cross_positions()

        while changes_flag:
            if 'B' in possible_moves and elements[32].color == upper_color:
                self.back()
            elif 'B' in possible_moves and elements[12].color == upper_color:
                self.back_invert()
            elif 'L' in possible_moves and elements[41].color == upper_color:
                self.left()
            elif 'L' in possible_moves and elements[21].color == upper_color:
                self.left_invert()
            elif 'R' in possible_moves and elements[23].color == upper_color:
                self.right()
            elif 'R' in possible_moves and elements[39].color == upper_color:
                self.right_invert()
            elif 'F' in possible_moves and elements[14].color == upper_color:
                self.front()
            elif 'F' in possible_moves and elements[30].color == upper_color:
                self.front_invert()

            if possible_moves == self.check_cross_positions():
                changes_flag = False
            possible_moves = self.check_cross_positions()

    def two_movers(self):
        elements = self.elements
        upper_color = elements[4].color
        changes_flag = True
        possible_moves = self.check_cross_positions()

        while changes_flag:
            if 'B' in possible_moves and elements[52].color == upper_color:
                self.back()
                self.back()
            elif 'L' in possible_moves and elements[48].color == upper_color:
                self.left()
                self.left()
            elif 'R' in possible_moves and elements[50].color == upper_color:
                self.right()
                self.right()
            elif 'F' in possible_moves and elements[46].color == upper_color:
                self.front()
                self.front()

            if possible_moves == self.check_cross_positions():
                changes_flag = False
            possible_moves = self.check_cross_positions()

    def move_cube(self, list_of_moves):
        for m in list_of_moves:
            if m == 'U':
                self.up()
            elif m == 'D':
                self.down()
            elif m == 'F':
                self.front()
            elif m == 'B':
                self.back()
            elif m == 'R':
                self.right()
            elif m == 'L':
                self.left()
            elif m == 'UI':
                self.up_invert()
            elif m == 'DI':
                self.down_invert()
            elif m == 'FI':
                self.front_invert()
            elif m == 'BI':
                self.back_invert()
            elif m == 'RI':
                self.right_invert()
            elif m == 'LI':
                self.left_invert()
            else:
                print("Wrong letter")

    def match_middles(self):
        elements = self.elements
        while elements[19].color != elements[22].color:
            self.up()

        while not self.middles_matches():
            if elements[19].color == elements[22].color and \
               elements[28].color == elements[31].color:
                self.move_cube(['F', 'U', 'FI', 'U', 'F', 'U', 'U', 'FI', 'U'])
            self.move_cube(['R', 'U', 'RI', 'U', 'R', 'U', 'U', 'RI'])

    def middles_matches(self):
        elements = self.elements

        if elements[19].color == elements[22].color and \
           elements[28].color == elements[31].color and \
           elements[37].color == elements[40].color and \
           elements[10].color == elements[13].color:
            return True
        return False

    def match_down_middles(self):
        elements = self.elements
        while elements[22].color != elements[25].color:
            self.down()
        while not self.down_middle_matches():
            if elements[22].color == elements[25].color and \
               elements[31].color == elements[34].color:
                self.move_cube(['F', 'D', 'FI', 'D', 'F', 'D', 'D', 'FI', 'D'])
            self.move_cube(['L', 'D', 'LI', 'D', 'L', 'D', 'D', 'LI'])

    def down_middle_matches(self):
        elements = self.elements

        if elements[22].color == elements[25].color and \
                elements[31].color == elements[34].color and \
                elements[40].color == elements[43].color and \
                elements[13].color == elements[16].color:
            return True
        return False

    def first_layer_not_complete(self):
        elements = self.elements
        up_color = elements[4].color
        if elements[0].color == elements[2].color == elements[6].color == elements[8].color == up_color:
            print("false")
            return False
        print("true")
        return True

    def match_corners(self):
        while self.first_layer_not_complete():
        #for i in range(8):
            elements = self.elements
            up_color = elements[4].color
            front_color = elements[22].color
            right_color = elements[31].color
            option0 = [elements[8].color, elements[20].color, elements[27].color]
            option1 = [elements[2].color, elements[29].color, elements[36].color]
            option2 = [elements[0].color, elements[38].color, elements[9].color]
            option3 = [elements[6].color, elements[11].color, elements[18].color]
            option4 = [elements[47].color, elements[26].color, elements[33].color]
            option5 = [elements[53].color, elements[35].color, elements[42].color]
            option6 = [elements[51].color, elements[44].color, elements[15].color]
            option7 = [elements[45].color, elements[24].color, elements[17].color]
            options = [option0, option1, option2, option3, option4, option5, option6, option7]

            for option in options:
                if up_color in option and front_color in option and right_color in option:
                    self.put_corner_in(option, options.index(option))
            self.change_front()

    def put_corner_in(self, option, option_number):
        elements = self.elements
        up_color = elements[4].color
        front_color = elements[22].color
        right_color = elements[31].color

        if option_number == 0:
            if up_color == option[0] and front_color == option[1] and right_color == option[2]:
                return
            else:
                self.move_cube(['RI', 'DI', 'R', 'D'])
        elif option_number == 1:
            self.move_cube(['BI', 'DI', 'B', 'D'])
        elif option_number == 2:
            self.move_cube(['LI', 'D', 'D', 'L'])
        elif option_number == 3:
            self.move_cube(['F', 'DI', 'FI', 'D', 'D'])
        elif option_number == 5:
            self.move_cube(['DI'])
        elif option_number == 6:
            self.move_cube(['D', 'D'])
        elif option_number == 7:
            self.move_cube(['D'])

        element_front = elements[26].color
        element_right = elements[33].color

        if element_front == up_color and element_right == right_color:
            self.move_cube(['DI', 'RI', 'D', 'R'])
        elif element_front == front_color and element_right == up_color:
            self.move_cube(['D', 'F', 'DI', 'FI'])
        else:
            self.move_cube(['D', 'F', 'DI', 'DI', 'FI'])
            self.move_cube(['D', 'F', 'DI', 'FI'])

    def match_middle_corners(self):
        for x in range(4):
            for i in range(2):
                elements = self.elements
                front_color = elements[22].color
                right_color = elements[31].color
                left_color = elements[13].color
                option0 = [elements[23].color, elements[30].color]
                option1 = [elements[32].color, elements[39].color]
                option2 = [elements[41].color, elements[12].color]
                option3 = [elements[14].color, elements[21].color]
                option4 = [elements[25].color, elements[46].color]
                option5 = [elements[34].color, elements[50].color]
                option6 = [elements[43].color, elements[52].color]
                option7 = [elements[16].color, elements[48].color]
                options = [option0, option1, option2, option3, option4, option5, option6, option7]
                for option in options:
                    if front_color in option and right_color in option and i == 0:
                        self.put_middle_corner(option, options.index(option))
                    elif front_color in option and left_color in option and i == 1:
                        self.put_middle_corner(option, options.index(option))
            self.change_front()

    def put_middle_corner(self, option, option_number):
        elements = self.elements
        front_color = elements[22].color
        right_color = elements[31].color
        left_color = elements[13].color
        if option_number == 0:
            if front_color == option[0] and right_color == option[1]:
                return
            else:
                self.move_cube(['DI', 'RI', 'D', 'R', 'D', 'F', 'DI', 'FI', 'D', 'D'])
        elif option_number == 1:
            self.move_cube(['DI', 'BI', 'D', 'B', 'D', 'R', 'DI', 'RI', 'D', 'D'])
        elif option_number == 2:
            self.move_cube(['D', 'B', 'DI', 'BI', 'DI', 'LI', 'D', 'L', 'D', 'D'])
        elif option_number == 3:
            if front_color == option[1] and left_color == option[0]:
                return
            else:
                self.move_cube(['D', 'L', 'DI', 'LI', 'DI',  'FI', 'D', 'F', 'D', 'D'])
        elif option_number == 5:
            self.move_cube(['DI'])
        elif option_number == 6:
            self.move_cube(['D', 'D'])
        elif option_number == 7:
            self.move_cube(['D'])

        element_bottom = elements[46].color
        element_front = elements[25].color

        if element_bottom == right_color:
            self.move_cube(['DI', 'RI', 'D', 'R', 'D', 'F', 'DI', 'FI', 'D', 'D'])
        elif element_bottom == left_color:
            self.move_cube(['D', 'L', 'DI', 'LI', 'DI', 'FI', 'D', 'F', 'D', 'D'])
        elif element_front == right_color:
            self.move_cube(['D', 'D', 'F', 'DI', 'FI', 'DI', 'RI', 'D', 'R'])
        elif element_front == left_color:
            self.move_cube(['DI', 'DI', 'FI', 'D', 'F', 'D', 'L', 'DI', 'LI'])

    def make_down_cross(self):
        elements = self.elements
        down_color = elements[49].color
        move = ['F', 'L', 'D', 'LI', 'DI', 'FI']

        if elements[46].color == elements[48].color == elements[49].color\
                == elements[50].color == elements[52].color:
            return
        if elements[46].color != down_color and elements[48].color != down_color\
           and elements[50].color != down_color and elements[52].color != down_color:
                self.move_cube(move)

        while elements[50].color != down_color and (elements[52].color != down_color
                                                    or elements[48].color != down_color):
            self.down()

        while not (elements[46].color == elements[48].color == elements[49].color
                   == elements[50].color == elements[52].color):
            self.move_cube(move)

    def get_starting_down_corner(self):
        rotation = 0
        while not self.good_down_corner():
            self.change_front()
            rotation += 1
            if rotation % 4 == 0:
                self.move_cube(['L', 'D', 'LI', 'DI', 'RI', 'D', 'L', 'DI', 'R', 'LI'])

    def good_down_corner(self):
        elements = self.elements
        corner_colors = [elements[49].color, elements[22].color, elements[13].color ]
        if elements[24].color in corner_colors and elements[17].color in corner_colors\
           and elements[45].color in corner_colors:
            return True
        return False

    def match_down_corners(self):
        while not self.down_corners_in_place():
            self.move_cube(['L', 'D', 'LI', 'DI', 'RI', 'D', 'L', 'DI', 'R', 'LI'])

    def down_corners_in_place(self):
        elements = self.elements
        left_color = elements[13].color
        front_color = elements[22].color
        down_color = elements[49].color
        right_color = elements[31].color
        back_color = elements[40].color
        c0 = [left_color, front_color, down_color]  # corner 0
        c1 = [right_color, back_color, down_color]   # corner 1
        # If three corners are correct then forth one must be correct
        if elements[17].color in c0 and elements[24].color in c0 and elements[45].color in c0\
           and elements[35].color in c1 and elements[42].color in c1 and elements[53].color in c1:
            return True
        return False

    def put_down_corners_in(self):
        for i in range(4):
            while not self.down_corner_in():
                self.move_cube(['LI', 'UI', 'L', 'U'])
            self.move_cube(['D'])

    def down_corner_in(self):
        elements = self.elements
        down_color = elements[49].color
        if elements[45].color == down_color:
            return True
        return False

    def finish_moves(self):
        elements = self.elements
        front_color = elements[22].color
        while elements[19].color != front_color:
            self.up()
        while elements[25].color != front_color:
            self.down()
        while front_color != 'yellow':
            self.change_front()
            front_color = self.elements[22].color
            print('Hey')

    def solve_cube(self):
        #first move
        self.make_upper_cross()
        #second move
        self.match_middles()
        #third move
        self.match_corners()
        #forth move
        self.match_middle_corners()
        #fifth move
        self.make_down_cross()
        #sixth move
        self.match_down_middles()
        #seventh move
        self.get_starting_down_corner()
        self.match_down_corners()
        #eight move
        self.put_down_corners_in()
        #finishing move
        self.finish_moves()

