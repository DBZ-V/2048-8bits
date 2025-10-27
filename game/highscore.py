import os
import pygame

HIGHSCORE_FILE = os.path.join(os.path.dirname(__file__), "highscores.txt")





def load_highscores(filepath=HIGHSCORE_FILE, max_entries=6):
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
        scores = [("AAA", "0000", 0)] * max_entries

    scores.sort(key=lambda x: x[2], reverse=True)
    return scores[:max_entries]



# def is_highscore(current_score, highscores):
#    """Vérifie si le score actuel entre dans la liste des meilleurs scores."""
#    if not highscores:
#        return True
#    lowest = highscores[-1][2]
#    return current_score > lowest

def is_highscore(current_score, highscores):
    """Vérifie si le score actuel entre dans la liste des meilleurs scores."""
    if not highscores:
        return True

    last = highscores[-1]
    # Gère les anciens formats à 2 champs
    lowest = int(last[2]) if len(last) > 2 else int(last[1])
    return current_score > lowest

def save_highscores(highscores, filepath=HIGHSCORE_FILE):
    with open(filepath, "w") as f:
        for name, score_str, _ in highscores:
            f.write(f"{name} {score_str}\n")
            

# def enter_initials(screen, font, current_score):
   #  """Fenêtre de saisie des 3 lettres du joueur en surimpression cyan."""
   #  initials = ["A", "A", "A"]
   #  index = 0
   #  done = False

   #  overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
   #  overlay.fill((0, 164, 164, 220))  # fond cyan semi-transparent

   #  while not done:
        # for event in pygame.event.get():
            # if event.type == pygame.QUIT:
                # return None
            # elif event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_RETURN:
                    # done = True
                # elif event.key == pygame.K_LEFT and index > 0:
                    # index -= 1
                # elif event.key == pygame.K_RIGHT and index < 2:
                    # index += 1
                # elif event.key == pygame.K_UP:
                    # initials[index] = chr(((ord(initials[index]) - 65 + 1) % 26) + 65)
                # elif event.key == pygame.K_DOWN:
                    # initials[index] = chr(((ord(initials[index]) - 65 - 1) % 26) + 65)

        # screen.blit(overlay, (0, 0))
        # title = font.render("ENTER YOUR INITIALS", True, (0, 0, 0))
        # title_rect = title.get_rect(center=(screen.get_width() // 2, 200))
        # screen.blit(title, title_rect)

        # display = "".join(initials)
        # entry = font.render(display, True, (255, 255, 255))
        # rect = entry.get_rect(center=(screen.get_width() // 2, 300))
        # screen.blit(entry, rect)

        # # Curseur visuel sous la lettre sélectionnée
        # cursor_x = rect.x + index * (rect.width / 3)
        # pygame.draw.rect(screen, (0, 0, 0), (cursor_x, rect.y + rect.height + 5, rect.width / 3, 5))

        # pygame.display.flip()
        # pygame.time.wait(50)

    # return "".join(initials)

def enter_initials(screen, font, current_score,
                   window_size=450, side_panel=200, padding=10):
    """Saisie des 3 lettres dans le panneau droit (cyan opaque, bien aligné)."""
    initials = ["A", "A", "A"]
    index = 0
    done = False

    # Même taille et position que le panneau droit défini dans display.py
    panel_x = window_size + padding
    panel_y = padding
    panel_width = side_panel - 2 * padding
    panel_height = screen.get_height() - 2 * padding

    # Surface de saisie : panneau girs opaque
    overlay = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    overlay.fill((192, 192, 192, 255))  # fond gris opaque
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True
                elif event.key == pygame.K_LEFT and index > 0:
                    index -= 1
                elif event.key == pygame.K_RIGHT and index < 2:
                    index += 1
                elif event.key == pygame.K_UP:
                    initials[index] = chr(((ord(initials[index]) - 65 + 1) % 26) + 65)
                elif event.key == pygame.K_DOWN:
                    initials[index] = chr(((ord(initials[index]) - 65 - 1) % 26) + 65)

        # Dessin du panneau
        screen.blit(overlay, (panel_x, panel_y))
        pygame.draw.rect(screen, (255, 255, 255), panel_rect, 3)  # contour blanc

        # Texte "ENTER YOUR INITIALS"
        title = font.render("NEW RECORD", True, (0, 0, 0))
        title_rect = title.get_rect(center=(panel_x + panel_width // 2, panel_y + 60))
        screen.blit(title, title_rect)

        # Texte "ENTER YOUR INITIALS"
        title = font.render("NEW RECORD", True, (0, 255, 0))
        title_rect = title.get_rect(center=(panel_x + panel_width // 2 - 2, panel_y + 60 - 2))
        screen.blit(title, title_rect)

        # Score affiché
        # Texte "SCORE:"
        score_text = font.render("SCORE:", True, (255, 0, 0))
        score_rect = score_text.get_rect(center=(panel_x + panel_width // 2, panel_y + 120))
        screen.blit(score_text, score_rect)

        # Texte "SCORE:"
        score_text = font.render("SCORE:", True, (255, 255, 0))
        score_rect = score_text.get_rect(center=(panel_x + panel_width // 2 - 2, panel_y + 120 - 2))
        screen.blit(score_text, score_rect)


        # Valeur du score (juste en dessous)
        score_val = font.render(str(current_score), True, (0, 0, 164))
        val_rect = score_val.get_rect(center=(panel_x + panel_width // 2, panel_y + 160))
        screen.blit(score_val, val_rect)

        # Valeur du score (juste en dessous)
        score_val = font.render(str(current_score), True, (0, 255, 255))
        val_rect = score_val.get_rect(center=(panel_x + panel_width // 2 - 2, panel_y + 160 - 2))
        screen.blit(score_val, val_rect)

        # Lettres du joueur
        display = "".join(initials)
        entry = font.render(display, True, (0, 0, 0))
        rect = entry.get_rect(center=(panel_x + panel_width // 2, panel_y + 220))
        screen.blit(entry, rect)

        # Curseur sous la lettre sélectionnée
        cursor_x = rect.x + index * (rect.width / 3)
        pygame.draw.rect(screen, (255, 255, 255),
                         (cursor_x, rect.y + rect.height + 5, rect.width / 3, 5))

        pygame.display.flip()
        pygame.time.wait(50)

    return "".join(initials)

if __name__ == "__main__":
    print("Chemin du fichier :", HIGHSCORE_FILE)
    print("Contenu :", load_highscores())
