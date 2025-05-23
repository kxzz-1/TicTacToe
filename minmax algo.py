import tkinter as tk
from tkinter import messagebox
import math

# Constants for the players
PLAYER_X = "X"
PLAYER_O = "O"
EMPTY = " "

# Colors for the game
BG_COLOR = "#2c3e50"  # Dark background
BUTTON_COLOR = "#ecf0f1"  # Light button background
PLAYER_X_COLOR = "#e74c3c"  # Red for Player X
PLAYER_O_COLOR = "#3498db"  # Blue for Player O
DISABLED_COLOR = "#95a5a6"  # Gray for disabled buttons
STATUS_COLOR = "#f39c12"  # Orange for status text

# Check if the game is over
def is_winner(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    return any(all(board[i] == player for i in line) for line in win_conditions)

# Check if the board is full (draw)
def is_draw(board):
    return all(cell != EMPTY for cell in board)

# Evaluate the board state
def evaluate(board):
    if is_winner(board, PLAYER_X):
        return 10  # Favorable for Player X
    if is_winner(board, PLAYER_O):
        return -10  # Favorable for Player O
    return 0  # Neutral state

# Minimax algorithm to find the best move
def minimax(board, depth, is_maximizing):
    score = evaluate(board)
    if score == 10 or score == -10:
        return score
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = PLAYER_X
                best_score = max(best_score, minimax(board, depth + 1, False))
                board[i] = EMPTY
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = PLAYER_O
                best_score = min(best_score, minimax(board, depth + 1, True))
                board[i] = EMPTY
        return best_score

# Find the best move using Minimax
def find_best_move(board, is_maximizing):
    best_move = -1
    best_score = -math.inf if is_maximizing else math.inf

    for i in range(9):
        if board[i] == EMPTY:
            board[i] = PLAYER_X if is_maximizing else PLAYER_O
            move_score = minimax(board, 0, not is_maximizing)
            board[i] = EMPTY

            if is_maximizing and move_score > best_score:
                best_score = move_score
                best_move = i
            elif not is_maximizing and move_score < best_score:
                best_score = move_score
                best_move = i

    return best_move

# GUI Implementation
class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg=BG_COLOR)
        self.board = [EMPTY] * 9
        self.buttons = []
        self.is_maximizing = True  # Player X (Computer) starts

        # Create a title label
        self.title_label = tk.Label(root, text="Tic-Tac-Toe", font=("Arial", 24, "bold"), bg=BG_COLOR, fg="#f1c40f")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Create buttons for the board
        for i in range(9):
            button = tk.Button(root, text=" ", font=("Arial", 20, "bold"), height=2, width=5,
                               bg=BUTTON_COLOR, activebackground=DISABLED_COLOR,
                               command=lambda i=i: self.human_move(i))
            button.grid(row=(i // 3) + 1, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)

        # Create a status label
        self.status_label = tk.Label(root, text="Your turn (Player O)", font=("Arial", 16), bg=BG_COLOR, fg=STATUS_COLOR)
        self.status_label.grid(row=4, column=0, columnspan=3, pady=10)

    def update_status(self, message):
        self.status_label.config(text=message)

    def human_move(self, index):
        if self.board[index] == EMPTY:
            self.board[index] = PLAYER_O
            self.buttons[index].config(text=PLAYER_O, state=tk.DISABLED, disabledforeground=PLAYER_O_COLOR)
            if self.check_game_over():
                return
            self.computer_move()

    def computer_move(self):
        self.update_status("Computer's turn (Player X)")
        self.root.update()
        move = find_best_move(self.board, True)
        if move != -1:
            self.board[move] = PLAYER_X
            self.buttons[move].config(text=PLAYER_X, state=tk.DISABLED, disabledforeground=PLAYER_X_COLOR)
        if not self.check_game_over():
            self.update_status("Your turn (Player O)")

    def check_game_over(self):
        if is_winner(self.board, PLAYER_X):
            self.update_status("Game Over: Player X (Computer) wins!")
            messagebox.showinfo("Game Over", "Player X (Computer) wins!")
            self.disable_all_buttons()
            return True
        elif is_winner(self.board, PLAYER_O):
            self.update_status("Game Over: Player O (You) win!")
            messagebox.showinfo("Game Over", "Player O (You) win!")
            self.disable_all_buttons()
            return True
        elif is_draw(self.board):
            self.update_status("Game Over: It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
            self.disable_all_buttons()
            return True
        return False

    def disable_all_buttons(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
