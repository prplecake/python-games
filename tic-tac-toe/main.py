from tkinter import *
import numpy as np

size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
green_color = '#7BC043'


class TicTacToe:

    def __init__(self):
        self.window = Tk()
        self.window.title('Tic Tac Toe')
        self.canvas = Canvas(
            self.window,
            width=size_of_board,
            height=size_of_board
        )
        self.canvas.pack()

        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wind = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0
    
    def mainloop(self):
        self.window.mainloop()
    
    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)
        
        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)
    
    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))

    ###################
    # Drawing Functions
    ###################

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)

    def display_gameover(self):
        if self.X_wins:
            self.X_score += 1
            text = 'Winner: Player 1 (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: Player 2 (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'It\'s a tie'
            color = 'gray'

        self.canvas.delete('all')
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font='cmr 60 bold', fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font='cmr 40 bold', fill=green_color, text=score_text)

        score_text = f'Player 1 (X): {self.X_score}\n'
        score_text += f'Player 2 (O): {self.O_score}\n'
        score_text += f'Tie: {self.tie_score}'
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font='cmr 30 bold', fill=green_color, text=score_text)
        self.reset_board = True

        score_text = 'Click to play again\n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font='cmr 20 bold', fill='gray', text=score_text)

    def click(self, event):
        grid_position = 

if __name__ == '__main__':
    game_instance = TicTacToe()
    game_instance.mainloop()
