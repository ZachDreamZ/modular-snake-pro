import wave
import struct
import math
import os

def generate_bgm(filename, duration=4, sample_rate=44100):
    num_samples = int(duration * sample_rate)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        # Simple chiptune-style sequence
        # Frequencies for a simple loop: C4, G3, A3, F3
        melody = [261.63, 196.00, 220.00, 174.61]
        note_duration = duration / len(melody)
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            note_idx = int((t / note_duration) % len(melody))
            freq = melody[note_idx]
            
            # Square wave for that chiptune sound
            sample = 1.0 if math.sin(2.0 * math.pi * freq * t) > 0 else -1.0
            
            # Add some basic harmony/overtone
            sample += 0.5 * (1.0 if math.sin(2.0 * math.pi * freq * 2 * t) > 0 else -1.0)
            sample /= 1.5
            
            val = int(sample * 32767)
            wav_file.writeframes(struct.pack('<h', val))

if __name__ == "__main__":
    os.makedirs('assets', exist_ok=True)
    print("Generating bgm_main.wav...")
    generate_bgm('assets/bgm_main.wav')
    print("BGM generated successfully!")