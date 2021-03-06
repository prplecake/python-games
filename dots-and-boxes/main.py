# https://github.com/aqeelanwar/Dots-and-Boxes

from tkinter import Canvas, Tk
import numpy as np

size_of_board = 600
number_of_dots = 6
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
dot_color = '#7BC043'
player1_color = '#0492CF'
player1_color_light = '#67B0CF'
player2_color = '#EE4035'
player2_color_light = '#EE7E77'
green_color = '#7BC043'
dot_width = 0.25 * size_of_board / number_of_dots
edge_width = 0.1 * size_of_board / number_of_dots
distance_between_dots = size_of_board / number_of_dots


class DotsAndBoxes:
    def __init__(self):
        self.window = Tk()
        self.window.title('Dots and Boxes')
        self.canvas = Canvas(
            self.window,
            width=size_of_board,
            height=size_of_board
        )
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.player1_starts = True
        self.player1_turn = self.player1_starts
        self.turntext_handle = []
        self.reset_board = False
        self.refresh_board()
        self.play_again()

    def play_again(self):
        self.refresh_board()
        self.board_status = np.zeros(
            shape=(number_of_dots - 1, number_of_dots - 1)
        )
        self.row_status = np.zeros(shape=(number_of_dots, number_of_dots - 1))
        self.col_status = np.zeros(shape=(number_of_dots - 1, number_of_dots))

        # Input from user by clicks
        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        self.display_turn_text()

    def mainloop(self):
        self.window.mainloop()

    ###################
    # Drawing Functions
    ###################

    def make_edge(self, type, logical_position):
        # pylint: disable=line-too-long
        if type == 'row':
            start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_x = start_x + distance_between_dots
            start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_y = start_y
        elif type == 'col':
            start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_y = start_y + distance_between_dots
            start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_x = start_x

        if self.player1_turn:
            color = player1_color
        else:
            color = player2_color

        self.canvas.create_line(start_x, start_y, end_x, end_y,
                                fill=color, width=edge_width)

    def refresh_board(self):
        for i in range(number_of_dots):
            x = i * distance_between_dots + distance_between_dots / 2
            self.canvas.create_line(x, distance_between_dots / 2, x,
                                    size_of_board - distance_between_dots / 2,
                                    fill='gray', dash=(2, 2))
            self.canvas.create_line(distance_between_dots / 2, x,
                                    size_of_board - distance_between_dots / 2,
                                    x,
                                    fill='gray', dash=(2, 2))

        for i in range(number_of_dots):
            for j in range(number_of_dots):
                start_x = i * distance_between_dots + distance_between_dots / 2
                end_x = j * distance_between_dots + distance_between_dots / 2
                self.canvas.create_oval(
                    start_x - dot_width / 2, end_x - dot_width / 2,
                    start_x + dot_width / 2, end_x + dot_width / 2,
                    fill=dot_color, outline=dot_color
                )

    def display_turn_text(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = player1_color
        else:
            text += 'Player2'
            color = player2_color

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(
            size_of_board - 5 * len(text),
            size_of_board - distance_between_dots / 8,
            font='cmr 15 bold', text=text, fill=color
        )

    def display_gameover(self):
        player1_score = len(np.argwhere(self.board_status == -4))
        player2_score = len(np.argwhere(self.board_status == 4))

        if player1_score > player2_score:
            # Player 1 wins
            text = 'Winner: Player 1 '
            color = player1_color
        elif player2_score > player1_score:
            # Player 2 wins
            text = 'Winnder: Player 2 '
            color = player2_color
        else:
            # It's a tie
            text = 'It\'s a tie'
            color = 'gray'

        self.canvas.delete('all')
        self.canvas.create_text(
            size_of_board / 2, size_of_board / 3,
            font='cmr 60 bold', fill=color, text=text
        )

        score_text = 'Scores\n'
        self.canvas.create_text(
            size_of_board / 2, 5 * size_of_board / 8,
            font='cmr 40 bold', fill=green_color, text=score_text
        )

        score_text = f'Player 1: {player1_score}\n'
        score_text += f'Player 2: {player2_score}\n'
        self.canvas.create_text(
            size_of_board / 2, 15 * size_of_board / 16,
            font='cmr 20 bold', fill='gray', text=score_text
        )

    def shade_box(self, box, color):
        # pylint: disable=line-too-long
        start_x = distance_between_dots / 2 + box[1] * distance_between_dots + edge_width / 2
        start_y = distance_between_dots / 2 + box[0] * distance_between_dots + edge_width / 2
        end_x = start_x + distance_between_dots - edge_width
        end_y = start_y + distance_between_dots - edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    ###################
    # Logical Functions
    ###################

    @staticmethod
    def convert_grid_to_logical_position(grid_position):
        grid_position = np.array(grid_position)
        position = (grid_position - distance_between_dots / 4)//(distance_between_dots / 2)

        type = False
        logical_position = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0]-1)//2)
            c = int(position[1]//2)
            logical_position = [r, c]
            type = 'row'
        elif position[0] % 2 == 0 and (position[1] - 1) %2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'

        return logical_position, type

    def is_grid_occupied(self, logical_position, type):
        r = logical_position[0]
        c = logical_position[1]
        occupied = True

        if type == 'row' and self.row_status[c][r] == 0:
            occupied = False
        if type == 'col' and self.col_status[c][r] == 0:
            occupied = False

        return occupied

    def mark_box(self):
        boxes = np.argwhere(self.board_status == -4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box):
                self.already_marked_boxes.append(list(box))
                color = player1_color_light
                self.shade_box(box, color)

        boxes = np.argwhere(self.board_status == 4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box):
                self.already_marked_boxes.append(list(box))
                color = player2_color_light
                self.shade_box(box, color)

    def update_board(self, type, logical_position):
        r = logical_position[0]
        c = logical_position[1]
        val = 1
        if self.player1_turn:
            val = -1

        if c < (number_of_dots - 1) and r < (number_of_dots - 1):
            self.board_status[c][r] += val

        if type == 'row':
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c-1][r] += val

        elif type == 'col':
            self.col_status[c][r] = 1
            if r >= 1:
                self.board_status[c][r-1] += val

    def is_gameover(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()

    def click(self, event):
        if not self.reset_board:
            grid_position = [event.x, event.y]
            logical_position, valid_input = self.convert_grid_to_logical_position(grid_position)
            if valid_input and not self.is_grid_occupied(logical_position, valid_input):
                self.update_board(valid_input, logical_position)
                self.make_edge(valid_input, logical_position)
                self.mark_box()
                self.refresh_board()
                self.player1_turn = not self.player1_turn

                if self.is_gameover():
                    self.display_gameover()
                else:
                    self.display_turn_text()

        else:
            self.canvas.delete('all')
            self.play_again()
            self.reset_board = False


if __name__ == '__main__':
    game_instance = DotsAndBoxes()
    game_instance.mainloop()
