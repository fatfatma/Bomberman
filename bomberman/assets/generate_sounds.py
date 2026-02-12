# generate_sounds.py
"""
Generate simple sound effects for the game
Run this once to create placeholder sounds
"""

import numpy as np
import wave
import os
os.makedirs("assets/sounds", exist_ok=True)



def generate_beep(filename, frequency, duration, volume=0.3):
    """
    Generate a simple beep sound.

    Args:
        filename (str): Output filename
        frequency (int): Frequency in Hz
        duration (float): Duration in seconds
        volume (float): Volume (0.0 to 1.0)
    """
    sample_rate = 22050

    # Generate sine wave
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave_data = np.sin(2 * np.pi * frequency * t)

    # Apply envelope (fade in/out)
    envelope = np.ones_like(wave_data)
    fade_samples = int(0.01 * sample_rate)  # 10ms fade
    envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
    envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)

    wave_data *= envelope * volume

    # Convert to 16-bit integers
    wave_data = (wave_data * 32767).astype(np.int16)

    # Save as WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())

    print(f"✅ Generated: {filename}")


def generate_explosion(filename, duration=0.5, volume=0.4):
    """Generate explosion sound (white noise with envelope)"""
    sample_rate = 22050
    samples = int(sample_rate * duration)

    # Generate white noise
    noise = np.random.uniform(-1, 1, samples)

    # Apply exponential decay envelope
    envelope = np.exp(-5 * np.linspace(0, 1, samples))

    wave_data = noise * envelope * volume
    wave_data = (wave_data * 32767).astype(np.int16)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())

    print(f"✅ Generated: {filename}")


def generate_powerup(filename, duration=0.3, volume=0.3):
    """Generate power-up sound (ascending notes)"""
    sample_rate = 22050

    # Three ascending notes
    notes = [523, 659, 784]  # C, E, G
    note_duration = duration / len(notes)

    wave_data = np.array([], dtype=np.int16)

    for freq in notes:
        t = np.linspace(0, note_duration, int(sample_rate * note_duration))
        note = np.sin(2 * np.pi * freq * t) * volume
        note = (note * 32767).astype(np.int16)
        wave_data = np.concatenate([wave_data, note])

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())

    print(f"✅ Generated: {filename}")


def generate_death(filename, duration=0.4, volume=0.3):
    """Generate death sound (descending tone)"""
    sample_rate = 22050
    samples = int(sample_rate * duration)

    # Descending frequency from 440Hz to 110Hz
    frequencies = np.linspace(440, 110, samples)
    phase = np.cumsum(2 * np.pi * frequencies / sample_rate)

    wave_data = np.sin(phase) * volume

    # Apply fade out
    envelope = np.linspace(1, 0, samples)
    wave_data *= envelope

    wave_data = (wave_data * 32767).astype(np.int16)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())

    print(f"✅ Generated: {filename}")


def generate_wall_break(filename, duration=0.2, volume=0.3):
    """Generate wall break sound (short noise burst)"""
    sample_rate = 22050
    samples = int(sample_rate * duration)

    # Filtered noise
    noise = np.random.uniform(-1, 1, samples)

    # Apply sharp envelope
    envelope = np.exp(-10 * np.linspace(0, 1, samples))

    wave_data = noise * envelope * volume
    wave_data = (wave_data * 32767).astype(np.int16)

    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())

    print(f"✅ Generated: {filename}")


def main():
    """Generate all sound effects"""
    print("=" * 60)
    print("🔊 SOUND GENERATOR")
    print("=" * 60)

    # Create assets/sounds directory
    os.makedirs('sounds', exist_ok=True)

    print("\nGenerating sound effects...\n")

    # Generate sounds
    generate_beep('assets/sounds/bomb_place.wav', frequency=440, duration=0.1)
    generate_explosion('assets/sounds/explosion.wav')
    generate_powerup('assets/sounds/powerup.wav')
    generate_death('assets/sounds/death.wav')
    generate_wall_break('assets/sounds/wall_break.wav')

    print("\n✅ All sounds generated successfully!")
    print("\nSound files created in: assets/sounds/")
    print("  - bomb_place   .wav")
    print("  - explosion.wav")
    print("  - powerup.wav")
    print("  - death.wav")
    print("  - wall_break.wav")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()