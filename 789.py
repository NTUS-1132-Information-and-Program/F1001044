import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("井字遊戲")

        # 初始化遊戲狀態
        self.board = [' ' for _ in range(9)]
        self.buttons = []
        self.x_wins = 0  # X 勝場數
        self.o_wins = 0  # O 勝場數
        self.mode = None
        self.current_player = None
        self.game_active = True
        self.winning_combo = None
        self.win_limit = 2  # 三戰兩勝

        # 選擇對戰模式
        self.mode_label = tk.Label(root, text="選擇對戰模式：", font=('normal', 15))
        self.mode_label.grid(row=0, column=0, columnspan=3)

        self.human_button = tk.Button(root, text="玩家對戰", width=20, command=self.set_human_mode)
        self.human_button.grid(row=1, column=0, columnspan=3)

        self.computer_button = tk.Button(root, text="玩家 vs 電腦", width=20, command=self.set_computer_mode)
        self.computer_button.grid(row=2, column=0, columnspan=3)

        self.start_button = tk.Button(root, text="開始遊戲", width=20, state=tk.DISABLED, command=self.start_game)
        self.start_button.grid(row=3, column=0, columnspan=3)

        # 棋盤區域
        self.board_frame = tk.Frame(root)

        # 狀態標籤
        self.status_label = tk.Label(self.root, text="", font=('normal', 14))
        self.score_label = tk.Label(self.root, text=f"X: {self.x_wins} - O: {self.o_wins}", font=('normal', 15))

        # 重新開始與回到選項按鈕
        self.reset_button = tk.Button(self.root, text="重新開始遊戲", width=20, command=self.reset_game)
        self.back_button = tk.Button(self.root, text="回到選項", width=20, command=self.back_to_options)

    def set_human_mode(self):
        self.mode = 'human'
        self.mode_label.config(text="對戰模式：玩家對戰")
        self.start_button.config(state=tk.NORMAL)

    def set_computer_mode(self):
        self.mode = 'computer'
        self.mode_label.config(text="對戰模式：玩家 vs 電腦")
        self.start_button.config(state=tk.NORMAL)

    def start_game(self):
        # 隱藏選項區塊
        self.mode_label.grid_forget()
        self.human_button.grid_forget()
        self.computer_button.grid_forget()
        self.start_button.grid_forget()

        # 顯示棋盤
        self.board_frame.grid(row=4, column=0, columnspan=3)

        # 只建立一次按鈕
        if not self.buttons:
            for i in range(9):
                button = tk.Button(self.board_frame, text=' ', width=10, height=3, font=('normal', 20),
                                   command=lambda i=i: self.on_click(i))
                button.grid(row=i // 3, column=i % 3, padx=2, pady=2)
                self.buttons.append(button)

        # 顯示狀態與分數
        self.status_label.grid(row=5, column=0, columnspan=3)
        self.score_label.grid(row=6, column=0, columnspan=3)
        self.reset_button.grid(row=7, column=0, columnspan=3)
        self.back_button.grid(row=8, column=0, columnspan=3)

        self.reset_board()  # 初始化遊戲

    def reset_board(self):
        self.board = [' '] * 9
        for button in self.buttons:
            button.config(text=' ', bg='SystemButtonFace', state=tk.NORMAL)
        self.current_player = random.choice(['X', 'O'])
        self.status_label.config(text=f"目前輪到：{self.current_player}")
        self.game_active = True
        if self.mode == 'computer' and self.current_player == 'O':
            self.root.after(500, self.computer_move)

    def on_click(self, index):
        if not self.game_active or self.board[index] != ' ':
            return

        self.make_move(index, self.current_player)

        if self.check_winner():
            self.end_game(f"玩家 {self.current_player} 獲勝！")
            self.update_score(self.current_player)
        elif ' ' not in self.board:
            self.end_game("遊戲平局！")
        else:
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.status_label.config(text=f"目前輪到：{self.current_player}")
            if self.mode == 'computer' and self.current_player == 'O':
                self.root.after(500, self.computer_move)

    def make_move(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player)

    def check_winner(self):
        self.winning_combo = None
        combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in combos:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                self.winning_combo = combo
                return True
        return False

    def highlight_winner(self):
        if self.winning_combo:
            for i in self.winning_combo:
                self.buttons[i].config(bg='lightgreen')

    def end_game(self, message):
        self.highlight_winner()
        self.status_label.config(text=message)
        self.game_active = False
        for button in self.buttons:
            button.config(state=tk.DISABLED)

    def update_score(self, winner):
        if winner == 'X':
            self.x_wins += 1
        elif winner == 'O':
            self.o_wins += 1
        self.score_label.config(text=f"X: {self.x_wins} - O: {self.o_wins}")

        # 檢查是否有玩家達成 2 勝
        if self.x_wins == self.win_limit:
            messagebox.showinfo("遊戲結束", f"玩家 X 率先達到 2 勝！")
            self.reset_game()  # 遊戲結束後重置
        elif self.o_wins == self.win_limit:
            messagebox.showinfo("遊戲結束", f"玩家 O 率先達到 2 勝！")
            self.reset_game()  # 遊戲結束後重置

    def computer_move(self):
        if not self.game_active:
            return
        move = self.best_move()
        self.make_move(move, 'O')
        if self.check_winner():
            self.end_game("玩家 O 獲勝！")
            self.update_score('O')
        elif ' ' not in self.board:
            self.end_game("遊戲平局！")
        else:
            self.current_player = 'X'
            self.status_label.config(text=f"目前輪到：{self.current_player}")

    def best_move(self):
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                if self.check_winner():
                    self.board[i] = ' '
                    return i
                self.board[i] = ' '
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'X'
                if self.check_winner():
                    self.board[i] = ' '
                    return i
                self.board[i] = ' '
        return random.choice([i for i, x in enumerate(self.board) if x == ' '])

    def reset_game(self):
        # 重置棋盤，但保留玩家對戰模式和勝場數
        self.board = [' '] * 9
        for button in self.buttons:
            button.config(text=' ', bg='SystemButtonFace', state=tk.NORMAL)
        self.current_player = random.choice(['X', 'O'])
        self.status_label.config(text=f"目前輪到：{self.current_player}")
        self.game_active = True

        # 如果未達成三戰兩勝，則不清空分數
        if self.x_wins < self.win_limit and self.o_wins < self.win_limit:
            self.score_label.config(text=f"X: {self.x_wins} - O: {self.o_wins}")
        else:
            # 清空分數，準備開始新的一輪
            self.x_wins = 0
            self.o_wins = 0
            self.score_label.config(text=f"X: {self.x_wins} - O: {self.o_wins}")

    def back_to_options(self):
        self.board_frame.grid_forget()
        self.status_label.grid_forget()
        self.score_label.grid_forget()
        self.reset_button.grid_forget()
        self.back_button.grid_forget()

        for button in self.buttons:
            button.grid_forget()
        self.buttons.clear()

        self.mode_label.grid(row=0, column=0, columnspan=3)
        self.human_button.grid(row=1, column=0, columnspan=3)
        self.computer_button.grid(row=2, column=0, columnspan=3)
        self.start_button.grid(row=3, column=0, columnspan=3)
        self.start_button.config(state=tk.DISABLED)  # 返回選項後禁止開始，需重新選模式


if __name__ == '__main__':
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
