"""
Dataset Downloader for Signal Classification
Author: Samyak Jain
Roll No: 07611502824
Branch: ECE-2, 2nd Year

This script downloads sample audio files from various sources
so you don't need to record your own signals.
"""

import os
import urllib.request
import zipfile
import tarfile
from pathlib import Path
import shutil


class DatasetDownloader:
    """Downloads and prepares audio datasets for signal classification"""
    
    def __init__(self, data_dir="dataset"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
    def download_file(self, url, filename):
        """Download a file from URL with progress"""
        filepath = os.path.join(self.data_dir, filename)
        
        if os.path.exists(filepath):
            print(f"  ✓ File already exists: {filename}")
            return filepath
        
        print(f"  Downloading {filename}...")
        try:
            def reporthook(block_num, block_size, total_size):
                downloaded = block_num * block_size
                percent = min(downloaded * 100.0 / total_size, 100)
                print(f"\r  Progress: {percent:.1f}%", end='', flush=True)
            
            urllib.request.urlretrieve(url, filepath, reporthook=reporthook)
            print(f"\n  ✓ Downloaded: {filename}")
            return filepath
        except Exception as e:
            print(f"\n  ✗ Error downloading {filename}: {e}")
            return None
    
    def download_freesound_samples(self):
        """
        Download sample audio files from direct URLs
        These are Creative Commons licensed audio samples
        """
        print("\n" + "="*60)
        print("Downloading Sample Audio Files")
        print("="*60)
        
        # Direct download links for various audio samples
        samples = {
            "fan_noise": "https://freesound.org/data/previews/270/270156_4062622-lq.mp3",
            "clapping": "https://freesound.org/data/previews/415/415209_7989882-lq.mp3",
            "traffic": "https://freesound.org/data/previews/387/387232_7255534-lq.mp3",
            "music_piano": "https://freesound.org/data/previews/413/413169_6943248-lq.mp3",
            "bird_chirp": "https://freesound.org/data/previews/449/449069_8935037-lq.mp3",
            "door_knock": "https://freesound.org/data/previews/264/264981_3263906-lq.mp3",
            "water_drip": "https://freesound.org/data/previews/394/394414_7290452-lq.mp3",
            "bell": "https://freesound.org/data/previews/411/411749_6185989-lq.mp3",
        }
        
        downloaded_files = []
        
        for name, url in samples.items():
            print(f"\n{name.replace('_', ' ').title()}:")
            filename = f"{name}.mp3"
            filepath = self.download_file(url, filename)
            if filepath:
                downloaded_files.append(filepath)
        
        return downloaded_files
    
    def download_esc50_samples(self):
        """
        Download sample from ESC-50 dataset (Environmental Sound Classification)
        This is a subset for demonstration purposes
        """
        print("\n" + "="*60)
        print("Downloading ESC-50 Dataset Samples")
        print("="*60)
        print("Note: Downloading a subset for demonstration...")
        
        # GitHub repository with sample audio files
        base_url = "https://github.com/karoldvl/ESC-50/raw/master/audio/"
        
        sample_files = [
            "1-100032-A-0.wav",  # Dog bark
            "1-100210-A-36.wav", # Vacuum cleaner
            "1-116765-A-41.wav", # Chainsaw
            "1-27934-A-17.wav",  # Clock tick
            "1-30226-A-12.wav",  # Helicopter
        ]
        
        downloaded_files = []
        
        for filename in sample_files:
            url = base_url + filename
            print(f"\n{filename}:")
            filepath = self.download_file(url, filename)
            if filepath:
                downloaded_files.append(filepath)
        
        return downloaded_files
    
    def create_synthetic_signals(self):
        """
        Create synthetic audio signals for testing
        """
        print("\n" + "="*60)
        print("Creating Synthetic Audio Signals")
        print("="*60)
        
        import numpy as np
        from scipy.io import wavfile
        
        fs = 44100  # Sampling rate
        synthetic_dir = os.path.join(self.data_dir, "synthetic")
        os.makedirs(synthetic_dir, exist_ok=True)
        
        signals = []
        
        # 1. Pure sine wave (periodic)
        print("\n  Creating: Pure Sine Wave (440 Hz)")
        duration = 3
        t = np.linspace(0, duration, int(fs * duration))
        signal = np.sin(2 * np.pi * 440 * t)
        signal = (signal * 32767).astype(np.int16)
        filepath = os.path.join(synthetic_dir, "sine_440hz.wav")
        wavfile.write(filepath, fs, signal)
        signals.append(filepath)
        print(f"  ✓ Created: sine_440hz.wav")
        
        # 2. Square wave (periodic)
        print("\n  Creating: Square Wave")
        from scipy import signal as sp_signal
        square = sp_signal.square(2 * np.pi * 100 * t)
        square = (square * 32767).astype(np.int16)
        filepath = os.path.join(synthetic_dir, "square_wave.wav")
        wavfile.write(filepath, fs, square)
        signals.append(filepath)
        print(f"  ✓ Created: square_wave.wav")
        
        # 3. White noise (aperiodic, power signal)
        print("\n  Creating: White Noise")
        noise = np.random.randn(len(t))
        noise = (noise / np.max(np.abs(noise)) * 32767 * 0.3).astype(np.int16)
        filepath = os.path.join(synthetic_dir, "white_noise.wav")
        wavfile.write(filepath, fs, noise)
        signals.append(filepath)
        print(f"  ✓ Created: white_noise.wav")
        
        # 4. Chirp signal (aperiodic)
        print("\n  Creating: Chirp Signal")
        chirp = sp_signal.chirp(t, f0=100, f1=2000, t1=duration, method='linear')
        chirp = (chirp * 32767).astype(np.int16)
        filepath = os.path.join(synthetic_dir, "chirp_signal.wav")
        wavfile.write(filepath, fs, chirp)
        signals.append(filepath)
        print(f"  ✓ Created: chirp_signal.wav")
        
        # 5. AM modulated signal
        print("\n  Creating: AM Modulated Signal")
        carrier = np.sin(2 * np.pi * 500 * t)
        modulator = 0.5 * (1 + np.sin(2 * np.pi * 10 * t))
        am_signal = carrier * modulator
        am_signal = (am_signal * 32767).astype(np.int16)
        filepath = os.path.join(synthetic_dir, "am_modulated.wav")
        wavfile.write(filepath, fs, am_signal)
        signals.append(filepath)
        print(f"  ✓ Created: am_modulated.wav")
        
        # 6. Damped oscillation (energy signal)
        print("\n  Creating: Damped Oscillation")
        damped = np.exp(-2 * t) * np.sin(2 * np.pi * 200 * t)
        damped = (damped / np.max(np.abs(damped)) * 32767).astype(np.int16)
        filepath = os.path.join(synthetic_dir, "damped_oscillation.wav")
        wavfile.write(filepath, fs, damped)
        signals.append(filepath)
        print(f"  ✓ Created: damped_oscillation.wav")
        
        # 7. Multi-frequency signal (periodic)
        print("\n  Creating: Multi-Frequency Signal")
        multi_freq = (np.sin(2 * np.pi * 200 * t) + 
                     0.5 * np.sin(2 * np.pi * 400 * t) + 
                     0.3 * np.sin(2 * np.pi * 600 * t))
        multi_freq = (multi_freq / np.max(np.abs(multi_freq)) * 32767).astype(np.int16)
        filepath = os.path.join(synthetic_dir, "multi_frequency.wav")
        wavfile.write(filepath, fs, multi_freq)
        signals.append(filepath)
        print(f"  ✓ Created: multi_frequency.wav")
        
        # 8. Pulse signal (energy signal)
        print("\n  Creating: Pulse Signal")
        pulse = np.zeros(len(t))
        pulse_width = int(0.1 * fs)
        pulse[int(0.5*fs):int(0.5*fs)+pulse_width] = 1
        pulse[int(1.5*fs):int(1.5*fs)+pulse_width] = 1
        pulse[int(2.5*fs):int(2.5*fs)+pulse_width] = 1
        pulse = (pulse * 32767).astype(np.int16)
        filepath = os.path.join(synthetic_dir, "pulse_signal.wav")
        wavfile.write(filepath, fs, pulse)
        signals.append(filepath)
        print(f"  ✓ Created: pulse_signal.wav")
        
        return signals
    
    def get_all_audio_files(self):
        """Get list of all audio files in dataset directory"""
        audio_extensions = ['.wav', '.mp3', '.ogg', '.flac']
        audio_files = []
        
        for root, dirs, files in os.walk(self.data_dir):
            for file in files:
                if any(file.lower().endswith(ext) for ext in audio_extensions):
                    audio_files.append(os.path.join(root, file))
        
        return audio_files
    
    def download_all(self):
        """Download all available datasets"""
        print("\n" + "="*70)
        print("DATASET DOWNLOADER - Signal Classification Project")
        print("Author: Samyak Jain (07611502824)")
        print("="*70)
        
        all_files = []
        
        # Create synthetic signals (always works, no internet needed)
        print("\n[1/3] Creating Synthetic Signals...")
        synthetic_files = self.create_synthetic_signals()
        all_files.extend(synthetic_files)
        print(f"\n✓ Created {len(synthetic_files)} synthetic audio files")
        
        # Try to download real audio samples
        print("\n[2/3] Downloading Sample Audio Files...")
        try:
            downloaded_files = self.download_freesound_samples()
            all_files.extend(downloaded_files)
            print(f"\n✓ Downloaded {len(downloaded_files)} audio samples")
        except Exception as e:
            print(f"\n⚠ Could not download samples: {e}")
            print("  (This is okay, synthetic signals are available)")
        
        # Try to download ESC-50 samples
        print("\n[3/3] Downloading ESC-50 Dataset Samples...")
        try:
            esc_files = self.download_esc50_samples()
            all_files.extend(esc_files)
            print(f"\n✓ Downloaded {len(esc_files)} ESC-50 samples")
        except Exception as e:
            print(f"\n⚠ Could not download ESC-50 samples: {e}")
            print("  (This is okay, other signals are available)")
        
        print("\n" + "="*70)
        print(f"DOWNLOAD COMPLETE - {len(all_files)} audio files ready!")
        print("="*70)
        print(f"\nAll files saved to: {os.path.abspath(self.data_dir)}")
        
        return all_files


def main():
    """Main function to download datasets"""
    downloader = DatasetDownloader()
    
    print("\nThis will download/create audio samples for your project.")
    print("No recording needed!\n")
    
    choice = input("Download datasets now? (y/n): ").strip().lower()
    
    if choice == 'y':
        files = downloader.download_all()
        
        print("\n" + "-"*70)
        print("AVAILABLE AUDIO FILES:")
        print("-"*70)
        for i, file in enumerate(files, 1):
            print(f"{i:2d}. {os.path.basename(file)}")
        
        print("\n" + "-"*70)
        print("NEXT STEPS:")
        print("-"*70)
        print("1. Run 'python analyze_dataset.py' to analyze all downloaded files")
        print("2. Or run 'python main.py' and choose option 3 to analyze individual files")
        print("-"*70)
    else:
        print("\nDownload cancelled.")


if __name__ == "__main__":
    main()
