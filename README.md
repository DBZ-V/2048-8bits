# 🕹️ 2048 - Python 95 Edition
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pygame](https://img.shields.io/badge/Library-Pygame-green)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

🇬🇧 🇨🇦 🇺🇸 [French version below]
📑 Jump to: [English](#-🕹️-2048---Python-95-Edition) | [Français](#-🕹️-2048---Python-95-Edition-)

A retro reinterpretation of the classic 2048, coded in Python with Pygame, 8-bit atmosphere and 90s-style interface.  
This project includes dynamic visual effects, real-time generated sounds, and a complete highscore system saved locally.

## 📁 Project Architecture
    2048-8bits/
    ├── .gitignore
    ├── requirements.txt
    ├── app/                     # sound tests and experiments
    ├── test/                    # basic unit tests
    └── game/
        ├── __init__.py
        ├── board.py             # game logic (movements, merges, score)
        ├── display.py           # display, interface and visual effects
        ├── highscore.py         # highscore management and initials input
        ├── highscore.txt        # saved scores text file
        ├── main_menu.py         # main menu (game entry point)
        └── sounds.py            # generation and playback of 8-bit sounds

## 🚀 Quick Launch
1. Install dependencies

    Make sure you have Python 3.10+ installed.  
    Then, from the project root:

    ```      
    pip install -r requirements.txt
### Main dependencies are:
- pygame
- numpy


2. Launch the game

    ```
    python -m game.main_menu
    ```
    This will open the main menu, where you can start a game with the Space key.

## 🎮 Game Controls
| Key   | Action |
|-------|------------------|
| `↑`      | Move up              |
| `↓`      | Move down            |
| `←`      | Move left            |
| `→`      | Move right           |
| `Space`  | Start game           |
| `Escape` | Quit                 |

## ✨ Features
### 🧩 Classic 2048 Game
-    4x4 grid, standard moves and merges.
-    Random tile appearance (2 or 4).
-    Automatic score calculation at each merge.

### 💾 Persistent Highscores
-   The top 6 scores are saved in game/highscore.txt.
-   If you beat a record, the game invites you to enter your initials (3 letters).

### 🔊 8-bit Sound Atmosphere
-   Dynamic sound generation via Numpy + Pygame (square wave).
-   Retro jingles for menus, moves, and game over.
-   Slight random frequency variations for an “old-school synth” effect.

### 🖥️ Retro Interface
-   Horizontal “CRT” gradient background.
-   Colored grid depending on tile values.
-   Pulsing and shaking effects on the highest tile.
-   Side panel showing current score and highscores.

## 🧠 Logical Structure
|File |Role |
|-----------|--------------------------------------------|
|`board.py`   |	Contains game logic: moves, merges, tile generation, endgame check.|
|`display.py` |	Manages graphic rendering with Pygame (tiles, score, and side panel display).|
|`highscore.py`|	Loads/saves scores, and manages initials input via Pygame.|
|`sounds.py`|	Generates real-time 8-bit sounds from square waves and plays musical sequences.|
|`main_menu.py`|	Game entry point: main menu with animation and highscore display.|

## 🧩 Example Sound Sequence
Sounds are generated on the fly with frequencies defined in `sounds.py`

```
sequence = [
    ('do', 100), ('mi', 100), ('sol', 150),
    ('do', 150), ('sol', 150), ('do', 300)
]
play_sequence(sequence)
```

## 🧱 About the Code
- The project uses a clear modular approach:
- Strict separation between `board.py` logic, `display.py` visuals, and `sounds.py` audio.
- Module calls are managed via `main_menu.py`, which centralizes the game flow.

## 💡 Possible Improvements
- Add a fullscreen mode or color themes.
- Export highscores to a JSON file.
- Add a 2-player mode or online leaderboard.
- Create an installer or .exe executable with pyinstaller.

## 📜 License

This project is provided under the MIT License — free to use, modify, and distribute.
"""

-------------------

# 🕹️ 2048 - Python 95 Edition
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pygame](https://img.shields.io/badge/Library-Pygame-green)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

Une réinterprétation rétro du classique 2048, codée en Python avec Pygame, ambiance 8-bit et interface façon années 90.
Ce projet intègre des effets visuels dynamiques, des sons générés en temps réel, et un système complet de highscores enregistrés localement.

## 📁 Architecture du projet
    2048-8bits/
    ├── .gitignore
    ├── requirements.txt
    ├── app/                     # tests et expérimentations sonores
    ├── test/                    # tests unitaires basiques
    └── game/
        ├── __init__.py
        ├── board.py             # logique du jeu (mouvements, fusions, score)
        ├── display.py           # affichage, interface et effets visuels
        ├── highscore.py         # gestion des meilleurs scores et saisie des initiales
        ├── highscore.txt        # fichier texte des scores sauvegardés
        ├── main_menu.py         # menu principal (point d’entrée du jeu)
        └── sounds.py            # génération et lecture des sons 8-bit

## 🚀 Lancement rapide
1. Installer les dépendances

    Assurez-vous d’avoir Python 3.10+ installé.    
    Puis, depuis la racine du projet :
      ```
   pip install -r requirements.txt
### Les dépendances principales sont :
- pygame
- numpy

2. Lancer le jeu
    ```
    python -m game.main_menu
    ```
    Cela ouvrira le menu principal, où vous pouvez lancer une partie avec la touche Espace.

## 🎮 Contrôles du jeu
| Touche   | Action |
|-------|------------------|
| `↑`      | Déplacer haut           |
| `↓`      | Déplacer bas            |
| `←`      | Déplacer gauche         |
| `→`      | Déplacer droite         |
| `Espace` | Démarrer la partie      |
| `Échap`  | Quitter                 |

## ✨ Fonctionnalités
### 🧩 Jeu 2048 classique
-    Grille 4x4, mouvements et fusions standard.
-    Apparition aléatoire de tuiles (2 ou 4).
-    Calcul automatique du score à chaque fusion.

### 💾 Highscores persistants
-   Les 6 meilleurs scores sont sauvegardés dans game/highscore.txt.
-   Si vous battez un record, le jeu vous invite à entrer vos initiales (3 lettres).

### 🔊 Ambiance sonore 8-bit
-   Génération dynamique des sons via Numpy + Pygame (onde carrée).
-   Jingles rétro pour les menus, mouvements, et fin de partie.
-   Variation aléatoire légère des fréquences pour un effet “old-school synth”.

### 🖥️ Interface rétro
-   Dégradé “CRT” horizontal en fond.
-   Grille colorée selon la valeur des tuiles.
-   Effets de pulsation et de tremblement sur la tuile la plus élevée.
-   Panneau latéral affichant le score actuel et les highscores.

## 🧠 Structure logique
|Fichier |Rôle |
|-----------|--------------------------------------------|
|`board.py`   |	Contient la logique du jeu : mouvements, fusions, génération des tuiles, vérification de fin de partie.|
|`display.py` |	Gère le rendu graphique avec Pygame (affichage des tuiles, du score et du panneau latéral).|
|`highscore.py`|	Charge/enregistre les scores, et gère la saisie des initiales via Pygame.
|`sounds.py`|	Génère des sons 8-bit en temps réel à partir d’ondes carrées et joue des séquences musicales.   |
|`main_menu.py`|	Point d’entrée du jeu : menu principal avec animation et affichage des meilleurs scores.|

## 🧩 Exemple de séquence sonore
Les sons sont générés à la volée avec des fréquences définies dans `sounds.py`

```
sequence = [
    ('do', 100), ('mi', 100), ('sol', 150),
    ('do', 150), ('sol', 150), ('do', 300)
]
play_sequence(sequence)
```
## 🧱 À propos du code
- Le projet utilise une approche modulaire claire :
- Séparation stricte entre logique `board.py`, affichage `display.py`, et audio `sounds.py`.
- Les appels entre modules sont gérés via `main_menu.py`, qui centralise le flux du jeu.

## 💡 Améliorations possibles
- Ajouter un mode plein écran ou thèmes de couleur.
- Exporter les highscores dans un fichier JSON.
- Ajouter un mode 2 joueurs ou classement en ligne.
- Créer un installeur ou exécutable .exe avec pyinstaller.

## 📜 Licence

Ce projet est proposé sous licence MIT — libre d’utilisation, de modification et de distribution.
