"""
Display spectrogram of audio.
"""

import argparse
import math
import subprocess
import time
import wave

import numpy as np

from display import Display


def display_spectrogram(disp: Display, audio: np.ndarray, sample_rate: float, min_freq=100, max_freq=1000):
    """
    Display spectrogram of a single audio sample.
    """
    dft = []
    freq_step = (max_freq / min_freq) ** (1 / 80)
    for i in range(81):
        freq = min_freq * (freq_step ** i)
        x = np.linspace(0, len(audio) / sample_rate, len(audio)) * 2 * np.pi * freq
        amp = math.hypot(np.mean(audio * np.sin(x)), np.mean(audio * np.cos(x)))
        #amp = math.log(amp + 1)
        dft.append(amp)

    dft = np.array(dft) / 1e-3
    dft = np.clip(dft, 0, 27)
    dft = dft.astype(int)

    disp.board[:] = False
    for i in range(81):
        if dft[i] > 0:
            disp.board[-dft[i]:, i] = True


def display_audio(disp: Display, audio: np.ndarray, sample_rate: float, fps=15, repeat=False):
    """
    Automatically chunk audio and display spectrogram of each chunk sequentially.
    """
    chunk_size = int(sample_rate / fps)
    while True:
        for i in range(0, len(audio), chunk_size):
            if not disp.run:
                break
            chunk = audio[i:i + chunk_size]
            display_spectrogram(disp, chunk, sample_rate)
            time.sleep(1 / fps)

        if not repeat or not disp.run:
            break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str)
    args = parser.parse_args()

    subprocess.run([
        "ffmpeg", "-y",
        "-i", args.file,
        "-c:a", "pcm_s16le",
        "/tmp/apt33_audio.wav"
    ], check=True)

    with wave.open("/tmp/apt33_audio.wav", "rb") as wf:
        sample_rate = wf.getframerate()
        n_frames = wf.getnframes()
        audio = wf.readframes(n_frames)
        audio = np.frombuffer(audio, dtype=np.int16)
        audio = audio / 32768.0

    disp = Display()
    disp.add_daemon(display_audio, (disp, audio, sample_rate, 15, True))
    disp.start()


if __name__ == "__main__":
    main()
