import random

class Board:
    def __init__(self, size=4):
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.score = 0
        self.spawn_tile()
        self.spawn_tile()

    def spawn_tile(self):
        empty = [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == 0]
        if not empty:
            return False
        r, c = random.choice(empty)
        self.grid[r][c] = random.choice([2] * 9 + [4])
        return True

    def can_move(self):
        # Si au moins une case vide
        for row in self.grid:
            if 0 in row:
                return True

        # Si deux tuiles adjacentes sont identiques
        for r in range(self.size):
            for c in range(self.size):
                if c + 1 < self.size and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r + 1 < self.size and self.grid[r][c] == self.grid[r + 1][c]:
                    return True

        return False

    def compress(self, row):
        """Déplace toutes les tuiles non nulles à gauche."""
        new_row = [n for n in row if n != 0]
        new_row += [0] * (self.size - len(new_row))
        return new_row

    def merge(self, row):
        """Fusionne les tuiles identiques à gauche."""
        for i in range(self.size - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0
                self.score += row[i]
        return self.compress(row)

    def move_left(self):
        moved = False
        for i in range(self.size):
            new_row = self.merge(self.compress(self.grid[i]))
            if new_row != self.grid[i]:
                moved = True
            self.grid[i] = new_row
        if moved:
            self.spawn_tile()
        return moved

    def move_right(self):
        self.grid = [row[::-1] for row in self.grid]
        moved = self.move_left()
        self.grid = [row[::-1] for row in self.grid]
        return moved

    def move_up(self):
        self.grid = [list(row) for row in zip(*self.grid)]
        moved = self.move_left()
        self.grid = [list(row) for row in zip(*self.grid)]
        return moved

    def move_down(self):
        self.grid = [list(row[::-1]) for row in zip(*self.grid)]
        moved = self.move_left()
        self.grid = [list(row) for row in zip(*self.grid[::-1])]
        return moved
