import numpy as np
import pygame
import time

# --- Initialisation du mixeur ---
pygame.mixer.quit()  # reset propre
pygame.mixer.init(frequency=44100, size=-16, channels=2)
print("Mixer config:", pygame.mixer.get_init())

# --- Notes de base ---
NOTES = {
    'do': 130.81,
    're': 146.83,
    'mi': 164.81,
    'fa': 174.61,
    'sol': 196.00,
    'la': 220.00,
    'si': 246.94,
    'silence': 0
}


# --- Génération d'une onde 8-bit ---
def make_wave(freq, duration_ms, waveform='square', volume=0.02):
    """Génère une onde et s'adapte automatiquement au nombre de canaux du mixeur."""
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, n_samples, False)

    # Forme d’onde
    if freq == 0:
        wave = np.zeros(n_samples, dtype=np.float32)
    elif waveform == 'square':
        wave = np.sign(np.sin(2 * np.pi * freq * t))
    elif waveform == 'triangle':
        wave = 2 * np.abs(2 * (t * freq - np.floor(0.5 + t * freq))) - 1
    elif waveform == 'saw':
        wave = 2 * (t * freq - np.floor(0.5 + t * freq))
    else:
        wave = np.sin(2 * np.pi * freq * t)

    # Mise à l’échelle
    wave = (wave * 32767 * volume).astype(np.int16)

    # 🔧 Adapter automatiquement au nombre de canaux du mixeur
    mixer_info = pygame.mixer.get_init()
    n_channels = mixer_info[2] if mixer_info else 2  # fallback stéréo

    # On s'assure que l'onde a exactement n_channels colonnes
    if wave.ndim == 1:
        wave = np.repeat(wave[:, np.newaxis], n_channels, axis=1)
    elif wave.shape[1] != n_channels:
        # si le tableau a déjà 2 colonnes mais le mixeur en veut 8, on adapte
        wave = np.repeat(wave[:, [0]], n_channels, axis=1)

    # Debug optionnel
    # print("Wave shape:", wave.shape, "channels:", n_channels)

    return pygame.sndarray.make_sound(wave)


# --- Lecture d'une séquence ---
def play_sequence(sequence, waveform='square'):
    for note, dur in sequence:
        freq = NOTES.get(note.lower(), 0)
        sound = make_wave(freq, dur, waveform)
        sound.play()
        pygame.time.wait(dur)

# --- Test ---
if __name__ == "__main__":
    sequence = [
        ('do', 100),('silence', 70), ('do', 100), ('silence', 50),
        ('fa', 100), ('mi', 100), ('re', 100), ('do', 200)
    ]
    play_sequence(sequence, waveform='square')
    time.sleep(0.5)
