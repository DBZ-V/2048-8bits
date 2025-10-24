# test_board.py
from game.board import Board
import os

b = Board()

while b.can_move():
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in b.grid:
        print(row)
    move = input("Move (z/q/s/d): ").lower()
    if move == 'z': b.move_up()
    elif move == 's': b.move_down()
    elif move == 'q': b.move_left()
    elif move == 'd': b.move_right()
print("Game over! Score:", b.score)
