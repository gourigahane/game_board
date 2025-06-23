import tkinter as tk
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.master.geometry("500x500")
        self.master.bind("<Key>", self.handle_key)

        self.grid_size = 4
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0

        self.tiles = []
        self.init_grid()
        self.add_tile()
        self.add_tile()
        self.update_grid()

    def init_grid(self):
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                tile = tk.Label(self.master, text="", font=("Helvetica", 32), width=4, height=2, relief="raised")
                tile.grid(row=i, column=j, padx=5, pady=5)
                row.append(tile)
            self.tiles.append(row)

    def add_tile(self):
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def update_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.grid[i][j]
                if value == 0:
                    self.tiles[i][j].config(text="", bg="lightgray")
                else:
                    self.tiles[i][j].config(text=str(value), bg="lightblue")
        self.master.update_idletasks()

    def handle_key(self, event):
        if event.keysym in ("Up", "Down", "Left", "Right"):
            prev_grid = [row[:] for row in self.grid]
            self.move_tiles(event.keysym)
            if self.grid != prev_grid:
                self.add_tile()
            self.update_grid()
            if self.check_game_over():
                self.show_game_over()

    def move_tiles(self, direction):
        if direction == 'Up':
            self.grid = self.transpose(self.grid)
            self.grid = self.merge_tiles(self.grid)
            self.grid = self.transpose(self.grid)
        elif direction == 'Down':
            self.grid = self.transpose(self.grid)
            self.grid = self.reverse(self.grid)
            self.grid = self.merge_tiles(self.grid)
            self.grid = self.reverse(self.grid)
            self.grid = self.transpose(self.grid)
        elif direction == 'Left':
            self.grid = self.merge_tiles(self.grid)
        elif direction == 'Right':
            self.grid = self.reverse(self.grid)
            self.grid = self.merge_tiles(self.grid)
            self.grid = self.reverse(self.grid)

    def merge_tiles(self, grid):
        new_grid = []
        for row in grid:
            tight = [i for i in row if i != 0]
            merged = []
            skip = False
            for j in range(len(tight)):
                if skip:
                    skip = False
                    continue
                if j + 1 < len(tight) and tight[j] == tight[j + 1]:
                    merged.append(tight[j] * 2)
                    self.score += tight[j] * 2
                    skip = True
                else:
                    merged.append(tight[j])
            merged += [0] * (self.grid_size - len(merged))
            new_grid.append(merged)
        return new_grid

    def check_game_over(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    return False
                if j < self.grid_size - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if i < self.grid_size - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        return True

    def show_game_over(self):
        game_over_label = tk.Label(self.master, text="Game Over!", font=("Helvetica", 24), bg="red", fg="white")
        game_over_label.place(relx=0.5, rely=0.5, anchor="center")

    def transpose(self, matrix):
        return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

    def reverse(self, matrix):
        return [row[::-1] for row in matrix]

def main():
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()

if __name__ == "__main__":
    main()
