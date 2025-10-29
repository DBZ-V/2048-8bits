import pygame
from game.board import Board
from game.sounds import play_sequence,make_wave , get_slide_note
import random
import os
from game.highscore import load_highscores, is_highscore, save_highscores, enter_initials
import math
import time

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

def draw_retro_gradient(screen, top_color, bottom_color, step=15):
    """Dégradé horizontal en bandes visibles (style années 90)."""
    width, height = screen.get_size()
    for x in range(0, width, step):
        ratio = x / width
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.rect(screen, (r, g, b), (x, 0, step, height))

TILE_SIZE = 100
PADDING = 10
WINDOW_SIZE = TILE_SIZE * 4 + PADDING * 5
FONT_NAME = "Courier New"

SIDE_PANEL = 200
WINDOW_WIDTH = WINDOW_SIZE + SIDE_PANEL
WINDOW_HEIGHT = WINDOW_SIZE                 # Augmenter la taille de la fenêtre

# def load_highscores(filepath="game/highscores.txt", max_entries=6):
#     """Lit un fichier texte et retourne une liste [(nom, score_str, score_int), ...]"""
#     scores = []
#     try:
#         with open(filepath, "r") as f:
#             for line in f:
#                 parts = line.strip().split()
#                 if len(parts) == 2 and parts[1].isdigit():
#                     name, score_str = parts
#                     score_int = int(score_str)
#                     scores.append((name.upper(), score_str, score_int))
#     except FileNotFoundError:
#         # ============== fichier manquant => scores vides ==============
#         scores = [("AAA", "0000", 0)] * max_entries
# 
#     # ============== Tri sur la valeur numérique ==============
#     scores.sort(key=lambda x: x[2], reverse=True)
# 
#     # ============== Ne renvoyer que nom + score texte ==============
#     return [(n, s) for n, s, _ in scores[:max_entries]]




def draw_board(screen, board, font):
    # ============== Zone de jeu principale ==============
    # screen.fill((0, 164, 164))
    draw_retro_gradient(screen,(0, 164, 164),(0, 100, 100), step = 25)

    # ============== valeur la plus haute actuelle ==============
    max_val = 0
    for row in board.grid:
        for cell in row:
            if cell > max_val:
                max_val = cell

    # for r in range(board.size):
    #     for c in range(board.size):
    #         val = board.grid[r][c]
    #         color = COLORS.get(val, (255, 255, 255))
    #         x = PADDING + c * (TILE_SIZE + PADDING)
    #         y = PADDING + r * (TILE_SIZE + PADDING)
    #         pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
    #         pygame.draw.rect(screen, (0, 0, 0), (x, y, TILE_SIZE, TILE_SIZE), 2)

    #         if val != 0:
    #             text = font.render(str(val), True, (0, 0, 0))
    #             text_rect = text.get_rect(center=(x + TILE_SIZE / 2, y + TILE_SIZE / 2))
    #             screen.blit(text, text_rect)

      # ============== Dessine la grille ==============
    for r in range(board.size):
        for c in range(board.size):
            val = board.grid[r][c]
            base_color = COLORS.get(val, (255, 255, 255))

            x = PADDING + c * (TILE_SIZE + PADDING)
            y = PADDING + r * (TILE_SIZE + PADDING)

            # ============== Par défaut sans d'offset ni pulse ==============
            draw_x = x
            draw_y = y
            fill_color = base_color
            border_color = (0, 0, 0)
            do_glitch_rgb_outline = False

            if val == max_val and val != 0:
                # ============== Effet GLITCH pour la tuile la plus haute ==============

                # ============== tremblement ==============
                jitter_x = random.randint(-1, 1)
                jitter_y = random.randint(-1, 1)
                draw_x = x + jitter_x
                draw_y = y + jitter_y

                # ============== pulsation de luminosité ==============
                pulse = (math.sin(time.time() *5) + 1) / 2  # oscille entre 0 et 1

                # ============== booste couleur ==============
                fill_color = tuple(
                    min(255, int(ch * (0.8 + 0.4 * pulse)))
                    for ch in base_color
                )

                # ============== contour ==============
                do_glitch_rgb_outline = True
                border_color = (255, 255, 255)

            # ============== Dessin du bloc principal ==============
            pygame.draw.rect(screen, fill_color, (draw_x, draw_y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, border_color, (draw_x, draw_y, TILE_SIZE, TILE_SIZE), 2)

            # # ============== Effet contour RGB décalé ==============
            # if do_glitch_rgb_outline:
            #     pygame.draw.rect(screen, (255, 0, 0),
            #                      (draw_x - 2, draw_y, TILE_SIZE, TILE_SIZE), 2)
            #     pygame.draw.rect(screen, (0, 255, 255),
            #                      (draw_x + 2, draw_y, TILE_SIZE, TILE_SIZE), 2)

            # ============== Texte dans la tuile ==============
            if val != 0:
                text = font.render(str(val), True, (0, 0, 0))
                text_rect = text.get_rect(center=(draw_x + TILE_SIZE / 2, draw_y + TILE_SIZE / 2))
                screen.blit(text, text_rect)


    # ============== Panneau latéral droit ==============
    panel_x = WINDOW_SIZE + PADDING
    panel_y = PADDING
    panel_width = SIDE_PANEL - 2 * PADDING
    panel_height = WINDOW_HEIGHT - 2 * PADDING

    # ============== fond gris avec bord noir ==============
    pygame.draw.rect(screen, (192, 192, 192), (panel_x, panel_y, panel_width, panel_height))
    pygame.draw.rect(screen, (0, 0, 0), (panel_x, panel_y, panel_width, panel_height), 2)

    # ============== Texte du score ==============
    score_text = font.render("SCORE", True, (0, 0, 255))
    value_text = font.render(str(board.score), True, (0, 0, 150))
    score_rect = score_text.get_rect(center=(panel_x + panel_width / 2, panel_y + 40))
    value_rect = value_text.get_rect(center=(panel_x + panel_width / 2, panel_y + 100))
    screen.blit(score_text, score_rect)
    screen.blit(value_text, value_rect)

     # ============== Texte du score ==============
    score_text = font.render("SCORE", True, (255, 255, 255))
    value_text = font.render(str(board.score), True, (0, 255, 0))
    score_rect = score_text.get_rect(center=(panel_x + panel_width / 2, panel_y + 38))
    value_rect = value_text.get_rect(center=(panel_x + panel_width / 2, panel_y + 98))
    screen.blit(score_text, score_rect)
    screen.blit(value_text, value_rect)

    # ============== Highscores ==============
    highscores = load_highscores()
    y_offset = panel_y + 162
    title_text = font.render("HIGHSCORES", True, (255, 100, 0))
    title_rect = title_text.get_rect(center=(panel_x + panel_width / 2, y_offset))
    screen.blit(title_text, title_rect)
    y_offset += 40

    # ============== for name, score in highscores ==============
    for name, score_str, _ in highscores:
        entry_text = font.render(f"{name}  {score_str}", True, (0, 0, 0))
        entry_rect = entry_text.get_rect(center=(panel_x + panel_width / 2, y_offset))
        screen.blit(entry_text, entry_rect)
        y_offset += 40

        # ============== Highscores ==============
    highscores = load_highscores()
    y_offset = panel_y + 160
    title_text = font.render("HIGHSCORES", True, (255, 255, 0))
    title_rect = title_text.get_rect(center=(panel_x + panel_width / 2, y_offset))
    screen.blit(title_text, title_rect)
    y_offset += 40

    # ============== for name, score in highscores: ==============
    for name, score_str, _ in highscores:
    
        entry_text = font.render(f"{name}  {score_str}", True, (0, 164, 164))
        entry_rect = entry_text.get_rect(center=(panel_x + panel_width / 2, y_offset))
        screen.blit(entry_text, entry_rect)
        y_offset += 40

    pygame.display.flip()

def draw_game_over(screen, font, alpha):
    """Affiche 'GAME OVER' avec ombre portée et transparence."""
    # ============== Surface transparente pour surimpression ==============
    overlay = pygame.Surface((WINDOW_SIZE, WINDOW_HEIGHT), pygame.SRCALPHA)

    # ============== Texte principal ==============
    text = font.render("GAME OVER", True, (255, 255, 255))
    text.set_alpha(alpha)
    text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_HEIGHT // 3))

    # ============== Ombre portée noire (contour léger autour du texte) ==============
    outline = font.render("GAME OVER", True, (0, 0, 0))
    outline.set_alpha(alpha)

    # ============== Positions autour du texte (ombre de 2 pixels) ==============
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        overlay.blit(outline, (text_rect.x + dx, text_rect.y + dy))

    # ============== Texte blanc par-dessus ==============
    overlay.blit(text, text_rect)

    # ============== Surimpression finale ==============
    screen.blit(overlay, (0, 0))
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


            for i in range(40):
                draw_board(screen, b, font)
                alpha = abs(int(255 * (i % 10) / 10 - 128)) + 100
                draw_game_over(screen, font, alpha)
                pygame.time.wait(100)

            pygame.time.wait(1500)

        

            # ============== Gestion du highscore ==============
            highscores = load_highscores()

            sequence =  [
                ('do', 100),
                ('mi', 100),
                ('sol', 100),
                ('do', 150),
                ('silence', 50),
                ('sol', 80),
                ('la', 80),
                ('si', 80),
                ('do', 200)
            ]
            
            sequence_end = [
                ('do', 100), ('mi', 100), ('sol', 100),
                ('do', 150), ('silence', 50),
                ('mi', 80), ('fa', 80), ('sol', 80),
                ('la', 100), ('si', 100), ('do', 200),
                ('sol', 100), ('mi', 100), ('do', 300)
            ]


            if is_highscore(b.score, highscores):
                play_sequence(sequence)
                name = enter_initials(screen, font, b.score)
                play_sequence(sequence_end)
                if name:
                    # ============== Ajoute et trie le nouveau score ==============
                    highscores.append((name, f"{b.score:04d}", b.score))
                    highscores.sort(key=lambda x: x[2], reverse=True)
                    save_highscores(highscores[:6])

            pygame.time.wait(1000)



            running = False

        clock.tick(30)

#    ============== pygame.quit() ==============

if __name__ == "__main__":
    main()
