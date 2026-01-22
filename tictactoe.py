import time
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import font

EMPTY = ' '
# Players
playerOne = 'X'
playerTwo = 'O'


class TTTGUI:
    def __init__(self):
        self.board = self.createBoard()
        self.current_player = playerOne
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.configure(bg="white")
        self._cells = {}
        self.createWidge()

    def createBoard(self):
        return [[EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY]]

    def createWidge(self):
        self.display = tk.Label(self.root, text = f"{self.current_player}'s Turn", font = font.Font(size = 28, weight = "bold"), fg = "black", bg = "white")
        self.display.pack()
        grid_frame = tk.Frame(self.root, bg = "white")
        grid_frame.pack()

        for row in range(3):
            for col in range(3):
                button = tk.Button(grid_frame, text = EMPTY, font = font.Font(size = 36, weight = "bold"), width = 3, height = 2, bg = "white", highlightbackground = "lightblue")
                button.grid(row = row, column = col, padx = 5, pady = 5, sticky = "nsew")
                button.bind("<Button-1>", lambda event, r = row, c = col: self.make_move(r, c))
                self._cells[(row, col)] = button

        play_again_button = tk.Button(self.root, text = "Play Again!", font = font.Font(size = 18, weight = "bold"), command = self.reset_board, fg = "black", bg = "white", highlightbackground = "lightblue" )
        play_again_button.pack(pady = 10)

    def update_display(self, message):
        self.display.config(text = message)

    def make_move(self, row, col):
        if self.board[row][col] != EMPTY or check_winner(self.board):
            return

        self.board[row][col] = self.current_player

        if self.current_player == playerOne:
            self._cells[(row, col)].config(text = self.current_player, fg = "red") #X
        else:
            self._cells[(row, col)].config(text = self.current_player, fg = "blue") #O

        winner = check_winner(self.board)
        if winner:
            if winner == "Tie":
                self.update_display("You tied! :P")
            else:
                self.update_display(f"{winner} wins! ^_^")
            self.end_game()
        else:
            self.switch_player()
            self.update_display(f"{self.current_player}'s turn! ^o^")

            if self.current_player == playerTwo:  
                self.ai_move()

    def switch_player(self):
        self.current_player = playerTwo if self.current_player == playerOne else playerOne

    def reset_board(self):
        global time_w_prune, time_wo_prune
        time_w_prune = []
        time_wo_prune = []
        self.board = self.createBoard()
        self.current_player = playerOne
        self.update_display(f"{self.current_player}'s turn! ^o^")
        for button in self._cells.values():
            button.config(text=EMPTY)

    def ai_move(self):
        use_prune = (len(time_w_prune) <= len(time_wo_prune))
        move = best_move(self.board, playerTwo, playerOne, use_prune)
        if move:
            row, col = move
            makeMove(self.board, row, col, playerTwo)
            self._cells[(row, col)].config(text = playerTwo, fg = "blue")
        
        winner = check_winner(self.board)
        if winner:
            if winner == "Tie":
                self.update_display("You tied! :P")
            else:
                self.update_display(f"{winner} wins! ^_^")
            self.end_game()
        else:
            self.switch_player()
            self.update_display(f"{self.current_player}'s turn ^o^")

    def end_game(self):
        graph()
        self.reset_board() 

    def run(self):
        self.root.mainloop()

def validMove(board, row, col):
    return board[row][col] == EMPTY

def makeMove(board, row, col, player):
    if validMove(board, row, col):
        board[row][col] = player
        return True
    return False

def check_winner(board):
    for i in range(3):
        # Check rows and columns
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    for row in board:
        if EMPTY in row:
            return None
    return "Tie"

#minimax implementation
'''
def is_full(board):
    for row in board:
        if EMPTY in row:
            return False
    return True
'''
time_w_prune = []
time_wo_prune = []

def minimax(board, depth, is_maximizing, player, opponent, alpha, beta, use_prune=True, top=True):
    startt = time.time() if top else None
    winner = check_winner(board)
    if winner == player:
        return 10 - depth
    elif winner == opponent:
        return depth - 10
    elif winner == "Tie":
        return 0

    if is_maximizing:
        best_score = float('-inf') 
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    board[row][col] = player
                    score = minimax(board, depth + 1, False, player, opponent, alpha, beta, use_prune, False)
                    board[row][col] = EMPTY
                    best_score = max(best_score, score)
                    if use_prune:
                        alpha = max(alpha, best_score)
                        if beta <= alpha: #beta prune
                            break
        if top:
            endt = time.time()
            (time_w_prune if use_prune else time_wo_prune).append(endt - startt)
        return best_score
    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == EMPTY:
                    board[row][col] = opponent
                    score = minimax(board, depth + 1, True, player, opponent, alpha, beta, use_prune, False)
                    board[row][col] = EMPTY
                    best_score = min(best_score, score)
                    if use_prune:
                        beta = min(beta, best_score)
                        if beta <= alpha: #alpha prune
                            break
        if top:
            endt = time.time()
            (time_w_prune if use_prune else time_wo_prune).append(endt - startt)
        return best_score

def best_move(board, player, opponent, use_prune):
    best_score = float('-inf')
    move = None
    alpha = float('-inf')
    beta = float('inf')

    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                board[row][col] = player
                score = minimax(board, 0, False, player, opponent, alpha, beta, use_prune)
                board[row][col] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (row, col)
                    alpha = max(alpha, best_score) 

    return move

def graph():
    plt.figure(figsize=(10, 5))
    plt.plot(range(len(time_w_prune)), time_w_prune, label="With Pruning", marker='o')
    plt.plot(range(len(time_wo_prune)), time_wo_prune, label="Without Pruning", marker='x')
    plt.xlabel("Move Number")
    plt.ylabel("Execution Time (seconds)")
    plt.title("AI Move Execution Time Comparison")
    plt.legend()
    plt.grid(True)
    plt.show()

#game play 
'''
def play():
    board = createBoard()
    currPlayer = playerOne

    while True:
        print_board(board)
        winner = check_winner(board)

        if winner:
            if winner == "Tie":
                print("You tied! :P")
            else:
                print(f"{winner} wins! ^_^")
            break

        if currPlayer == playerOne:
            while True:
                try:
                    print("Your turn! Enter row and column ^o^")
                    row = int(input("Row (0-2): "))
                    col = int(input("Column (0-2): "))
                    if 0 <= row < 3 and 0 <= col < 3 and makeMove(board, row, col, playerOne):
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Enter numbers between 0 and 2.")
            currPlayer = playerTwo
        else:
            print("AI's turn...")
            use_prune = (len(time_w_prune) <= len(time_wo_prune))
            ai_move(board, use_prune)
            currPlayer = playerOne
'''

def main():
    game = TTTGUI()
    game.run()

if __name__ == "__main__":
    main()