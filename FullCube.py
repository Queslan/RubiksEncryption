

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

    def check_cross_positions(self):
        all_elements = self.elements
        upper_color = all_elements[4].color
        possible_moves = []
        if all_elements[1].color != upper_color:
            possible_moves.append('B')
        if all_elements[3].color != upper_color:
            possible_moves.append('L')
        if all_elements[5].color != upper_color:
            possible_moves.append('R')
        if all_elements[7].color != upper_color:
            possible_moves.append('F')

        return possible_moves

    def make_cross(self):
        possible_moves = self.check_cross_positions()
        my_flag = 0
        while len(possible_moves) != 0:
            self.one_movers()
            self.two_movers()
            self.up()
            possible_moves = self.check_cross_positions()
            self.move_cube(possible_moves)

    def one_movers(self):
        all_elements = self.elements
        upper_color = all_elements[4].color
        changes_flag = True
        possible_moves = self.check_cross_positions()

        while changes_flag:
            if 'B' in possible_moves and all_elements[32].color == upper_color:
                self.back()
            elif 'B' in possible_moves and all_elements[12].color == upper_color:
                self.back_invert()
            elif 'L' in possible_moves and all_elements[41].color == upper_color:
                self.left()
            elif 'L' in possible_moves and all_elements[21].color == upper_color:
                self.left_invert()
            elif 'R' in possible_moves and all_elements[23].color == upper_color:
                self.right()
            elif 'R' in possible_moves and all_elements[39].color == upper_color:
                self.right_invert()
            elif 'F' in possible_moves and all_elements[14].color == upper_color:
                self.front()
            elif 'F' in possible_moves and all_elements[30].color == upper_color:
                self.front_invert()

            if possible_moves == self.check_cross_positions():
                changes_flag = False
            possible_moves = self.check_cross_positions()

    def two_movers(self):
        all_elements = self.elements
        upper_color = all_elements[4].color
        changes_flag = True
        possible_moves = self.check_cross_positions()

        while changes_flag:
            if 'B' in possible_moves and all_elements[52].color == upper_color:
                self.back()
                self.back()
            elif 'L' in possible_moves and all_elements[48].color == upper_color:
                self.left()
                self.left()
            elif 'R' in possible_moves and all_elements[50].color == upper_color:
                self.right()
                self.right()
            elif 'F' in possible_moves and all_elements[46].color == upper_color:
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
        all_elements = self.elements
        while all_elements[19].color != all_elements[22].color:
            self.up()

        while not self.middles_matched():
            if all_elements[19].color != all_elements[22].color and \
               all_elements[28].color == all_elements[31].color:
                self.move_cube(['F', 'U', 'FI', 'U', 'F', 'U', 'U', 'FI'])
            self.move_cube(['R', 'U', 'RI', 'U', 'R', 'U', 'U', 'RI'])

    def middles_matched(self):
        all_elements = self.elements

        if all_elements[19].color == all_elements[22].color and \
           all_elements[28].color == all_elements[31].color and \
           all_elements[37].color == all_elements[40].color and \
           all_elements[10].color == all_elements[13].color:
            return True
        return False

    def solve_cube(self):
        self.make_cross()
        self.match_middles()
