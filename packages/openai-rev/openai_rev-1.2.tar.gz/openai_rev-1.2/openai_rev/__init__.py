import simpleaudio as sa
import random
import numpy as np


def play_notes(frequencies, duration):
  sample_rate = 44100
  audio_data = np.zeros(int(sample_rate * duration))

  for frequency in frequencies:
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    note_data = np.sin(frequency * t * 2 * np.pi)
    audio_data += note_data

  audio_data = (audio_data * 32767 / np.max(np.abs(audio_data))).astype(
    np.int16)

  play_obj = sa.play_buffer(audio_data, 1, 2, sample_rate)
  play_obj.wait_done()


def generate_chord_progression(progression, key_freqs):
  chords = []

  for chord_name in progression:
    if chord_name == "I":
      chord_freqs = [key_freqs[0], key_freqs[2], key_freqs[4]]
    elif chord_name == "IV":
      chord_freqs = [key_freqs[3], key_freqs[5], key_freqs[0] * 2]
    elif chord_name == "V":
      chord_freqs = [key_freqs[4], key_freqs[6], key_freqs[1] * 2]
    else:
      raise ValueError("Invalid chord progression symbol")

    chords.append(chord_freqs)

  return chords


def generate_melody(frequencies, length):
  melody = []

  for _ in range(length):
    freq = random.choice(frequencies)
    duration = random.choice([0.125, 0.25,
                              0.5])  # Add more duration options for variation
    melody.append((freq, duration))

  return melody


def generate_drum_pattern(length):
  bass_drum_freq = 55  # A1 frequency - this will act as our bass drum
  drum_silence = None
  drum_pattern = []

  for _ in range(length):
    if random.random() < 0.4:  # 40% chance of a bass drum hit
      drum_pattern.append([bass_drum_freq])
    else:
      drum_pattern.append(drum_silence)

  return drum_pattern


def random_song(length=120):
  c_major_pentatonic = [261.63, 293.66, 329.63, 392.00,
                        440.00]  # C4, D4, E4, G4, A4
  g_major_pentatonic = [392.00, 440.00, 493.88, 587.33,
                        659.25]  # G4, A4, B4, D5, E5
  e_minor_pentatonic = [329.63, 392.00, 440.00, 493.88,
                        587.33]  # E4, G4, A4, B4, D5

  scales = [c_major_pentatonic, g_major_pentatonic, e_minor_pentatonic]
  scale = random.choice(scales)

  melody_length = length  # Increase the length to make it faster
  melody1 = generate_melody(scale, melody_length)
  melody2 = generate_melody(scale, melody_length)

  drum_pattern = generate_drum_pattern(melody_length)

  for idx in range(melody_length):
    note1, duration1 = melody1[idx]
    note2, duration2 = melody2[idx]
    drum = drum_pattern[idx]

    play_notes([note1] or [] + drum or [], duration1)
    play_notes([note2] or [] + drum or [], duration2)
