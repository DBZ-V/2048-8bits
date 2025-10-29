import random

class Board:
    def __init__(self, size=4):
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.score = 0
        self.spawn_tile()
        self.spawn_tile()

    # ============== Apparition d'une nouvelle tuile ==============
    def spawn_tile(self):
        empty = [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == 0]
        if not empty:
            return False
        r, c = random.choice(empty)
        self.grid[r][c] = random.choice([2] * 9 + [4])
        return True

    # ============== Vérifie si un mouvement est possible ==============
    def can_move(self):
        for row in self.grid:
            if 0 in row:
                return True
        for r in range(self.size):
            for c in range(self.size):
                if c + 1 < self.size and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r + 1 < self.size and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False

    # ============== Décale les nombres non nuls à gauche ==============
    def compress(self, row):
        new_row = [n for n in row if n != 0]
        new_row += [0] * (self.size - len(new_row))
        return new_row

    # ============== Fusionne les tuiles adjacentes identiques ==============
    def merge(self, row):
        merged = False
        for i in range(self.size - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0
                self.score += row[i]
                merged = True
        return self.compress(row), merged

    # ============== Mouvements ==============
    def move_left(self):
        moved = False
        merged_any = False
        new_grid = []
        for i in range(self.size):
            compressed = self.compress(self.grid[i])
            merged_row, merged = self.merge(compressed)
            if merged or merged_row != self.grid[i]:
                moved = True
            if merged:
                merged_any = True
            new_grid.append(merged_row)
        self.grid = new_grid
        if moved:
            self.spawn_tile()
        return moved, merged_any

    def move_right(self):
        self.grid = [row[::-1] for row in self.grid]
        moved, merged = self.move_left()
        self.grid = [row[::-1] for row in self.grid]
        return moved, merged

    def move_up(self):
        self.grid = [list(row) for row in zip(*self.grid)]
        moved, merged = self.move_left()
        self.grid = [list(row) for row in zip(*self.grid)]
        return moved, merged

    def move_down(self):
        # Transpose la grille (lignes → colonnes)
        self.grid = [list(row) for row in zip(*self.grid)]
        # Inverse chaque ligne (pour faire le bas)
        self.grid = [row[::-1] for row in self.grid]
        moved, merged = self.move_left()
        # Re-inverser et re-transposer pour revenir à l'état normal
        self.grid = [row[::-1] for row in self.grid]
        self.grid = [list(row) for row in zip(*self.grid)]
        return moved, merged

