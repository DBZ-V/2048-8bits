import pygame
from game.display import main as start_game
from game.highscore import load_highscores
from game.sounds import play_sequence

WINDOW_WIDTH = 650
WINDOW_HEIGHT = 450
FONT_NAME = "Courier New"

def draw_retro_gradient(screen, top_color, bottom_color, step=15):
    """Dégradé horizontal en bandes visibles (style années 90)."""
    width, height = screen.get_size()
    for x in range(0, width, step):
        ratio = x / width
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.rect(screen, (r, g, b), (x, 0, step, height))
        

def draw_menu(screen, font, title_font, highscores):
    # screen.fill((0, 164, 164))  # fond turquoise

    draw_retro_gradient(screen,(0, 164, 164),(0, 100, 100), step = 25)

    # ============== Titre du jeu ==============
    title = title_font.render("2048  -  PYTHON 95'", True, (255, 150, 0))
    title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 40 + 2))
    screen.blit(title, title_rect)

    title = title_font.render("2048  -  PYTHON 95'", True, (255, 255, 0))
    title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 40))
    screen.blit(title, title_rect)


    # ============== Instructions ==============

    text = font.render("PRESS [SPACE] TO START", True, (164, 0, 164))
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 100 + 2))
    screen.blit(text, text_rect)


    text = font.render("PRESS [SPACE] TO START", True, (0, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 100))
    screen.blit(text, text_rect)

    # ============== Highscores ==============
    y = 150

    hs_title = font.render("HIGHSCORES", True, (0, 100, 155))
    hs_rect = hs_title.get_rect(center=(WINDOW_WIDTH // 2, y + 2))
    screen.blit(hs_title, hs_rect)

    hs_title = font.render("HIGHSCORES", True, (0, 255, 0))
    hs_rect = hs_title.get_rect(center=(WINDOW_WIDTH // 2, y))
    screen.blit(hs_title, hs_rect)    

    for name, score_str, _ in highscores:
        entry = font.render(f"{name}   {score_str}", True, (0, 0, 0))
        entry_rect = entry.get_rect(center=(WINDOW_WIDTH // 2, y + 50 + 2))
        screen.blit(entry, entry_rect)
        y += 40

    y = 150

    for name, score_str, _ in highscores:
        entry = font.render(f"{name}   {score_str}", True, (255, y - 100, 0))
        entry_rect = entry.get_rect(center=(WINDOW_WIDTH // 2, y + 50))
        screen.blit(entry, entry_rect)
        y += 40

    pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_caption("2048 - Main Menu")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    font = pygame.font.SysFont(FONT_NAME, 28, bold=True)
    title_font = pygame.font.SysFont(FONT_NAME, 48, bold=True)

    highscores = load_highscores()

    running = True
    while running:
        draw_menu(screen, font, title_font, highscores)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Petit jingle de démarrage
                    start_jingle = [
                        ('do', 100), ('mi', 100), ('sol', 150),
                        ('do', 150), ('sol', 150), ('do', 300)
                    ]
                    play_sequence(start_jingle)
                    # Lancer le jeu
                    start_game()
                    highscores = load_highscores()  # recharger après la partie

        pygame.time.wait(50)



if __name__ == "__main__":
    main()
