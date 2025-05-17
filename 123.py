import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("井字遊戲")
        
        self.current_player = 'X'  # 玩家 X 先行
        self.board = [' ' for _ in range(9)]  # 初始化棋盤
        self.buttons = []  # 按鈕列表
        self.x_wins = 0  # 'X' 勝利次數
        self.o_wins = 0  # 'O' 勝利次數
        self.total_games = 0  # 總遊戲次數
        self.mode = None  # 對戰模式（None，'human'，'computer'）
        
        # 創建選擇模式的按鈕
        self.mode_label = tk.Label(self.root, text="選擇對戰模式：", font=('normal', 15))
        self.mode_label.grid(row=0, column=0, columnspan=3)

        self.human_button = tk.Button(self.root, text="玩家對戰", width=20, command=self.set_human_mode)
        self.human_button.grid(row=1, column=0, columnspan=3)

        self.computer_button = tk.Button(self.root, text="玩家 vs 電腦", width=20, command=self.set_computer_mode)
        self.computer_button.grid(row=2, column=0, columnspan=3)

        # 隱藏棋盤，直到選擇了對戰模式
        self.board_frame = tk.Frame(self.root)
        self.board_frame.grid(row=3, column=0, columnspan=3)

        # 設置遊戲開始按鈕
        self.start_button = tk.Button(self.root, text="開始遊戲", width=20, command=self.start_game)
        self.start_button.grid(row=4, column=0, columnspan=3)

    def set_human_mode(self):
        """設置玩家對戰模式"""
        self.mode = 'human'
        self.mode_label.config(text="對戰模式：玩家對戰")
        self.enable_start_button()

    def set_computer_mode(self):
        """設置玩家 vs 電腦模式"""
        self.mode = 'computer'
        self.mode_label.config(text="對戰模式：玩家 vs 電腦")
        self.enable_start_button()

    def enable_start_button(self):
        """啟用開始遊戲按鈕"""
        self.start_button.config(state=tk.NORMAL)

    def start_game(self):
        """開始遊戲，隱藏模式選擇，顯示棋盤"""
        self.mode_label.grid_forget()
        self.human_button.grid_forget()
        self.computer_button.grid_forget()
        self.start_button.grid_forget()

        # 創建棋盤按鈕
        for i in range(9):
            button = tk.Button(self.board_frame, text=' ', width=10, height=3, font=('normal', 20),
                               command=lambda i=i: self.on_click(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)
        
        # 顯示得分
        self.score_label = tk.Label(self.root, text=f"X: {self.x_wins} - O: {self.o_wins}", font=('normal', 15))
        self.score_label.grid(row=5, column=0, columnspan=3)

        # 重設遊戲按鈕
        self.reset_button = tk.Button(self.root, text="重新開始遊戲", width=20, command=self.reset_game)
        self.reset_button.grid(row=6, column=0, columnspan=3)

        # 開始第一局
        self.reset_board()

    def reset_board(self):
        """重設棋盤，清空所有按鈕和棋盤狀態"""
        self.board = [' ' for _ in range(9)]
        for button in self.buttons:
            button.config(text=' ')
        self.current_player = 'X'
        self.total_games += 1
        if self.mode == 'computer' and self.current_player == 'O':
            self.computer_move()

    def on_click(self, index):
        """玩家點擊格子"""
        if self.board[index] != ' ':
            return  # 如果該格已經被佔用，則忽略
        
        # 更新棋盤
        self.board[index] = self.current_player
        self.buttons[index].config(text=self.current_player)
        
        # 檢查遊戲結果
        if self.check_winner():
            messagebox.showinfo("遊戲結束", f"玩家 {self.current_player} 獲勝！")
            self.update_score(self.current_player)
            self.reset_board()
        elif ' ' not in self.board:  # 棋盤滿了且沒有勝者，則為平局
            messagebox.showinfo("遊戲結束", "遊戲平局！")
            self.reset_board()
        else:
            # 換玩家
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            if self.mode == 'computer' and self.current_player == 'O':
                self.computer_move()

    def check_winner(self):
        """檢查是否有勝者"""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 行
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 列
            [0, 4, 8], [2, 4, 6]              # 斜線
        ]
        
        # 檢查每個勝利組合
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return True
        return False

    def update_score(self, winner):
        """更新玩家得分"""
        if winner == 'X':
            self.x_wins += 1
        elif winner == 'O':
            self.o_wins += 1
        self.score_label.config(text=f"X: {self.x_wins} - O: {self.o_wins}")

        # 如果達到五戰三勝，顯示結果並重設遊戲
        if self.x_wins == 3:
            messagebox.showinfo("遊戲結束", "玩家 X 獲得三勝！")
            self.reset_game()
        elif self.o_wins == 3:
            messagebox.showinfo("遊戲結束", "玩家 O 獲得三勝！")
            self.reset_game()

    def computer_move(self):
        """電腦隨機選擇一個位置"""
        available_moves = [i for i, spot in enumerate(self.board) if spot == ' ']
        move = random.choice(available_moves)  # 隨機選擇空格
        self.board[move] = 'O'
        self.buttons[move].config(text='O')

        # 檢查遊戲結果
        if self.check_winner():
            messagebox.showinfo("遊戲結束", "玩家 O 獲勝！")
            self.update_score('O')
            self.reset_board()
        elif ' ' not in self.board:  # 平局
            messagebox.showinfo("遊戲結束", "遊戲平局！")
            self.reset_board()
        else:
            self.current_player = 'X'  # 換回玩家 X

    def reset_game(self):
        """重設遊戲，將勝利次數清零"""
        self.x_wins = 0
        self.o_wins = 0
        self.total_games = 0
        self.reset_board()
        self.score_label.config(text=f"X: {self.x_wins} - O: {self.o_wins}")

# 創建主視窗
root = tk.Tk()
game = TicTacToe(root)

# 啟動遊戲
root.mainloop()
