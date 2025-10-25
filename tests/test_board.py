from game.board import Board
from game.sounds import play_sequence
import os
import time


b = Board()

NOTE_BY_MOVE = {
    'z': 'sol',
    's': 're',
    'q': 'mi',
    'd': 'fa'
}

while b.can_move():
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in b.grid:
        print(row)
    move = input("Move (z/q/s/d): ").lower()

    moved = False
    if move == 'z': moved, merged = b.move_up()
    elif move == 's': moved, merged = b.move_down()
    elif move == 'q': moved, merged = b.move_left()
    elif move == 'd': moved, merged = b.move_right()

    if merged:
        play_sequence([('re', 80), ('mi', 80), ('fa', 80)])  # fusion
    elif moved:
        note = NOTE_BY_MOVE.get(move, 'do')
        play_sequence([(note, 100)])  # mouvement simple
    else:
        play_sequence([('do', 100), ('silence', 50), ('do', 100)])  # buzzer


    # if moved:
    #     note = NOTE_BY_MOVE.get(move, 'do')
    #     sequence = [(note, 100)]
    #     play_sequence(sequence, waveform='square')

print("Game over! Score:", b.score)
sequence = [
    ('do', 100),('silence', 70), ('do', 100), ('silence', 50),
    ('fa', 100), ('mi', 100), ('re', 100), ('do', 200)
]
play_sequence(sequence, waveform='square')
time.sleep(0.5)
