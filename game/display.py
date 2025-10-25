import pygame
from game.board import Board
from game.sounds import play_sequence,make_wave , get_slide_note
import random
import os

COLORS = {
    0:  (64, 64, 64),
    2:  (255, 0, 255),     # magenta 
    4:  (0, 255, 255),     # cyan 
    8:  (255, 255, 0),     # jaune 
    16: (255, 0, 0),       # rouge 
    32: (0, 255, 0),       # vert 
    64: (0, 0, 255),       # bleu 
    128: (255, 128, 0),    # orange 
    256: (255, 0, 128),    # rose 
    512: (128, 0, 255),    # violet 
    1024:(0, 255, 128),    # vert 
    2048:(255, 255, 255)   # blanc 
}

NOTE_BY_MOVE = {
    pygame.K_UP: 'slide_sound',
    pygame.K_DOWN: 'slide_sound',
    pygame.K_LEFT: 'slide_sound',
    pygame.K_RIGHT: 'slide_sound'
}

TILE_SIZE = 100
PADDING = 10
WINDOW_SIZE = TILE_SIZE * 4 + PADDING * 5
FONT_NAME = "Courier New"

SIDE_PANEL = 200
WINDOW_WIDTH = WINDOW_SIZE + SIDE_PANEL
WINDOW_HEIGHT = WINDOW_SIZE                 # Augmenter la taille de la fenêtre

def load_highscores(filepath="game/highscores.txt", max_entries=6):
    """Lit un fichier texte et retourne une liste [(nom, score_str, score_int), ...]"""
    scores = []
    try:
        with open(filepath, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2 and parts[1].isdigit():
                    name, score_str = parts
                    score_int = int(score_str)
                    scores.append((name.upper(), score_str, score_int))
    except FileNotFoundError:
        # fichier manquant => scores vides
        scores = [("AAA", "0000", 0)] * max_entries

    # Tri sur la valeur numérique
    scores.sort(key=lambda x: x[2], reverse=True)

    # Ne renvoyer que nom + score texte
    return [(n, s) for n, s, _ in scores[:max_entries]]




def draw_board(screen, board, font):
    # --- Zone de jeu principale ---
    screen.fill((0, 128, 128))
    for r in range(board.size):
        for c in range(board.size):
            val = board.grid[r][c]
            color = COLORS.get(val, (255, 255, 255))
            x = PADDING + c * (TILE_SIZE + PADDING)
            y = PADDING + r * (TILE_SIZE + PADDING)
            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (x, y, TILE_SIZE, TILE_SIZE), 2)

            if val != 0:
                text = font.render(str(val), True, (0, 0, 0))
                text_rect = text.get_rect(center=(x + TILE_SIZE / 2, y + TILE_SIZE / 2))
                screen.blit(text, text_rect)

    # --- Panneau latéral droit ---
    panel_x = WINDOW_SIZE + PADDING
    panel_y = PADDING
    panel_width = SIDE_PANEL - 2 * PADDING
    panel_height = WINDOW_HEIGHT - 2 * PADDING

    # fond gris avec bord noir
    pygame.draw.rect(screen, (192, 192, 192), (panel_x, panel_y, panel_width, panel_height))
    pygame.draw.rect(screen, (0, 0, 0), (panel_x, panel_y, panel_width, panel_height), 2)

    # --- Texte du score ---
    score_text = font.render("SCORE", True, (0, 0, 255))
    value_text = font.render(str(board.score), True, (0, 0, 255))
    score_rect = score_text.get_rect(center=(panel_x + panel_width / 2, panel_y + 40))
    value_rect = value_text.get_rect(center=(panel_x + panel_width / 2, panel_y + 100))
    screen.blit(score_text, score_rect)
    screen.blit(value_text, value_rect)

     # --- Texte du score ---
    score_text = font.render("SCORE", True, (255, 255, 255))
    value_text = font.render(str(board.score), True, (255, 255, 0))
    score_rect = score_text.get_rect(center=(panel_x + panel_width / 2, panel_y + 38))
    value_rect = value_text.get_rect(center=(panel_x + panel_width / 2, panel_y + 98))
    screen.blit(score_text, score_rect)
    screen.blit(value_text, value_rect)

    # --- Highscores ---
    highscores = load_highscores()
    y_offset = panel_y + 162
    title_text = font.render("HIGHSCORES", True, (0, 0, 255))
    title_rect = title_text.get_rect(center=(panel_x + panel_width / 2, y_offset))
    screen.blit(title_text, title_rect)
    y_offset += 40

    for name, score in highscores:
        entry_text = font.render(f"{name}  {score}", True, (0, 0, 0))
        entry_rect = entry_text.get_rect(center=(panel_x + panel_width / 2, y_offset))
        screen.blit(entry_text, entry_rect)
        y_offset += 40

        # --- Highscores ---
    highscores = load_highscores()
    y_offset = panel_y + 160
    title_text = font.render("HIGHSCORES", True, (255, 255, 0))
    title_rect = title_text.get_rect(center=(panel_x + panel_width / 2, y_offset))
    screen.blit(title_text, title_rect)
    y_offset += 40

    for name, score in highscores:
        entry_text = font.render(f"{name}  {score}", True, (0, 164, 164))
        entry_rect = entry_text.get_rect(center=(panel_x + panel_width / 2, y_offset))
        screen.blit(entry_text, entry_rect)
        y_offset += 40

    pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_caption("2048 - 8bit Edition")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    font = pygame.font.SysFont(FONT_NAME, 28, bold=True)

    b = Board()
    clock = pygame.time.Clock()
    running = True

    while running:
        draw_board(screen, b, font)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                moved = False
                merged = False

                if event.key == pygame.K_UP:
                    moved, merged = b.move_up()
                elif event.key == pygame.K_DOWN:
                    moved, merged = b.move_down()
                elif event.key == pygame.K_LEFT:
                    moved, merged = b.move_left()
                elif event.key == pygame.K_RIGHT:
                    moved, merged = b.move_right()

                if moved:
                    freq = get_slide_note()
                    sound = make_wave(freq, 100, waveform='square')
                    sound.play()
                else:
                    play_sequence([('do', 100), ('silence', 50), ('do', 100)])
        if not b.can_move():
            # Game over
            draw_board(screen, b, font)
            pygame.time.wait(300)
            sequence = [
                ('do', 100), ('silence', 70),
                ('do', 100), ('silence', 50),
                ('fa', 100), ('mi', 100),
                ('re', 100), ('do', 200)
            ]
            play_sequence(sequence)
            pygame.time.wait(1500)
            running = False

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
