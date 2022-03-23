# https://github.com/aqeelanwar/Snake-And-Apple

from tkinter import Canvas, TclError, Tk
import random
import time
import numpy as np

size_of_board = 600
rows = 10
cols = 10
DELAY = 100
snake_initial_length = 3
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 2
RED_COLOR = '#EE4035'
BLUE_COLOR = '#0492CF'
GREEN_COLOR = '#7BC043'
RED_COLOR_LIGHT = '#EE7E77'
BLUE_COLOR_LIGHT = '#67B0CF'


class SnakeAndApple:

    def __init__(self):
        self.window = Tk()
        self.window.title('Snake and Apples')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()

        # User input via clicks and keyboard
        self.window.bind('<Key>', self.key_input)
        self.window.bind('<Button-1>', self.mouse_input)
        self.play_again()
        self.begin = False

    def initialize_board(self):
        self.board = []
        self.apple_obj = []
        self.old_apple_cell = []

        for i in range(rows):
            for j in range(cols):
                self.board.append((i, j))

        for i in range(rows):
            self.canvas.create_line(
                i * size_of_board / rows, 0,
                i * size_of_board / rows, size_of_board
            )

        for i in range(cols):
            self.canvas.create_line(
                0, i * size_of_board / cols,
                size_of_board, i * size_of_board / cols
            )

    def initialize_snake(self):
        self.snake = []
        self.crashed = False
        self.snake_heading = 'right'
        self.last_key = self.snake_heading
        self.forbidden_actions = {
            "right": "left",
            "left": "right",
            "up": "down",
            "down": "up",
        }
        self.snake_objects = []
        for i in range(snake_initial_length):
            self.snake.append((i, 0))

    def play_again(self):
        self.canvas.delete('all')
        self.initialize_board()
        self.initialize_snake()
        self.place_apple()
        self.display_snake(mode='complete')
        self.begin_time = time.time()

    def mainloop(self):
        try:
            while True:
                self.window.update()
                if self.begin:
                    if not self.crashed:
                        self.window.after(DELAY, self.update_snake(self.last_key))
                    else:
                        self.begin = False
                        self.display_gameover()
        except TclError:
            pass

    ###################
    # Drawing Functions
    ###################

    def display_gameover(self):
        score = len(self.snake)
        self.canvas.delete('all')
        score_text = 'Scores\n'

        self.canvas.create_text(
            size_of_board / 2, 3 * size_of_board / 8,
            font='cmr 40 bold', fill=GREEN_COLOR, text=score_text
        )
        score_text = str(score)
        self.canvas.create_text(
            size_of_board / 2, size_of_board / 2,
            font='cmr 50 bold', fill=BLUE_COLOR, text=score_text
        )
        time_spent = str(np.round(time.time() - self.begin_time, 1)) + 'sec'
        self.canvas.create_text(
            size_of_board / 2, 3 * size_of_board / 4,
            font='cmr 20 bold', fill=BLUE_COLOR, text=time_spent
        )
        score_text = "Click to play again\n"
        self.canvas.create_text(
            size_of_board / 2, 15 * size_of_board / 16,
            font='cmr 20 bold', fill='gray', text=score_text
        )

    def place_apple(self):
        # Place apple randomly anywhere except at cells occupied by snake
        unoccupied_cells = set(self.board) - set(self.snake)
        self.apple_cell = random.choice(list(unoccupied_cells))
        row_h = int(size_of_board / rows)
        col_w = int(size_of_board / cols)
        x1 = self.apple_cell[0] * row_h
        y1 = self.apple_cell[1] * col_w
        x2 = x1 + row_h
        y2 = y1 + col_w
        self.apple_obj = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=RED_COLOR, outline=BLUE_COLOR
        )

    def display_snake(self, mode=''):
        # Remove tail from display if it exists
        if self.snake_objects != []:
            self.canvas.delete(self.snake_objects.pop(0))
        if mode == 'complete':
            for i, cell in enumerate(self.snake):
                row_h = int(size_of_board / rows)
                col_w = int(size_of_board / cols)
                x1 = cell[0] * row_h
                y1 = cell[1] * col_w
                x2 = x1 + row_h
                y2 = y1 + col_w
                self.snake_objects.append(
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=BLUE_COLOR, outline=BLUE_COLOR
                    )
                )
        else:
            # only update head
            cell = self.snake[-1]
            row_h = int(size_of_board / rows)
            col_w = int(size_of_board / cols)
            x1 = cell[0] * row_h
            y1 = cell[1] * col_w
            x2 = x1 + row_h
            y2 = y1 + col_w
            self.snake_objects.append(
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=BLUE_COLOR, outline=BLUE_COLOR
                )
            )
            if self.snake[0] == self.old_apple_cell:
                self.snake.insert(0, self.old_apple_cell)
                self.old_apple_cell = []
                tail = self.snake[0]
                row_h = int(size_of_board / rows)
                col_w = int(size_of_board / cols)
                x1 = tail[0] * row_h
                y1 = tail[1] * col_w
                x2 = x1 + row_h
                y2 = y1 + col_w
                self.snake_objects.insert(
                    0,
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=BLUE_COLOR, outline=BLUE_COLOR
                    )
                )
            self.window.update()

    ###################
    # Logical Functions
    ###################
    
    def update_snake(self, key):
        # Check if snake hit the wall or itself
        tail = self.snake[0]
        head = self.snake[-1]
        if tail != self.old_apple_cell:
            self.snake.pop(0)
        if key == 'left':
            self.snake.append((head[0] - 1, head[1]))
        elif key == 'right':
            self.snake.append((head[0] + 1, head[1]))
        elif key == 'up':
            self.snake.append((head[0], head[1] - 1))
        elif key == 'down':
            self.snake.append((head[0], head[1] + 1))

        head = self.snake[-1]
        if (
            head[0] > cols - 1
            or head[0] < 0
            or head[1] > rows - 1
            or head[1] < 0
            or len(set(self.snake)) != len(self.snake)
        ):
            # Hit the wall / hit self
            self.crashed = True
        elif self.apple_cell == head:
            # Got the apple
            self.old_apple_cell = self.apple_cell
            self.canvas.delete(self.apple_obj)
            self.place_apple()
            self.display_snake()
        else:
            self.snake_heading = key
            self.display_snake()

    def check_if_key_valid(self, key):
        valid_keys = ['up', 'down', 'left', 'right']
        if key in valid_keys and self.forbidden_actions[self.snake_heading] != key:
            return True
        return False

    def mouse_input(self, event):
        self.play_again()

    def key_input(self, event):
        if not self.crashed:
            key_pressed = event.keysym.lower()
            # Check if the key pressed is a valid key
            if self.check_if_key_valid(key_pressed):
                self.begin = True
                self.last_key = key_pressed

if __name__ == '__main__':
    game_instance = SnakeAndApple()
    game_instance.mainloop()
