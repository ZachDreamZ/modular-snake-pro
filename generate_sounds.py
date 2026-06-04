import wave
import struct
import math
import random
import os

def generate_wav(filename, duration, sample_rate=44100, frequency=440, type='sine', decay=True):
    num_samples = int(duration * sample_rate)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            
            if type == 'sine':
                # basic sine wave
                sample = math.sin(2.0 * math.pi * frequency * t)
            elif type == 'sweep':
                # frequency sweep (rising)
                start_freq = frequency
                end_freq = frequency * 2
                current_freq = start_freq + (end_freq - start_freq) * (i / num_samples)
                sample = math.sin(2.0 * math.pi * current_freq * t)
            elif type == 'noise':
                # white noise
                sample = random.uniform(-1, 1)
            elif type == 'melody':
                # Simple victory melody: C, E, G
                notes = [440, 554, 659]
                note_idx = int((i / num_samples) * len(notes))
                freq = notes[note_idx]
                # Relative time within the note
                t_rel = t % (duration / len(notes))
                sample = math.sin(2.0 * math.pi * freq * t_rel)
            else:
                sample = 0
                
            # Apply decay to avoid clicks
            if decay:
                envelope = 1.0 - (i / num_samples)
                sample *= envelope
            
            # Scale to 16-bit signed integer
            val = int(sample * 32767)
            wav_file.writeframes(struct.pack('<h', val))

def main():
    os.makedirs('assets/sounds', exist_ok=True)
    
    print("Generating eat.wav...")
    generate_wav('assets/sounds/eat.wav', 0.1, frequency=880, type='sine')
    
    print("Generating powerup.wav...")
    generate_wav('assets/sounds/powerup.wav', 0.2, frequency=440, type='sweep')
    
    print("Generating crash.wav...")
    generate_wav('assets/sounds/crash.wav', 0.3, type='noise')
    
    print("Generating victory.wav...")
    generate_wav('assets/sounds/victory.wav', 0.6, type='melody', decay=False)

    print("Generating click.wav...")
    generate_wav('assets/sounds/click.wav', 0.05, frequency=1200, type='sine')
    
    print("All sounds generated successfully!")

if __name__ == "__main__":
    main()