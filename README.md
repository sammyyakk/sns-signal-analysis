# Signal Classification System

**Unit I: Classification of Real-Life Signals**

**Author:** Samyak Jain  
**Roll No:** 07611502824  
**Branch:** ECE-2, 2nd Year  

## Project Overview

This project implements a comprehensive signal classification system that can:
- Record real-life signals (fan noise, clapping, traffic, music)
- Classify signals as **Periodic** or **Aperiodic**
- Classify signals as **Energy Signal** or **Power Signal**
- Generate detailed analysis plots including:
  - Time domain representation
  - Frequency spectrum (FFT)
  - Autocorrelation function
  - Power Spectral Density (PSD)
  - Spectrogram
  - Classification results

## Features

### Signal Classification Methods

#### 1. Periodicity Detection
- Uses **autocorrelation function** to detect periodic patterns
- Identifies period and fundamental frequency for periodic signals
- Threshold-based peak detection for robustness

#### 2. Energy/Power Classification
- **Energy Signal:** Finite energy, zero average power (e.g., transient signals)
- **Power Signal:** Infinite energy, finite non-zero average power (e.g., continuous signals)
- Calculates total energy and average power for each signal

### Signal Analysis Features
- Time-domain visualization
- Frequency-domain analysis (FFT)
- Autocorrelation analysis
- Power Spectral Density (Welch's method)
- Time-frequency analysis (Spectrogram)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. For audio recording support, you may need system dependencies:
   - **Linux:** `sudo apt-get install portaudio19-dev python3-pyaudio`
   - **macOS:** `brew install portaudio`
   - **Windows:** Usually works out of the box

## Usage

### Running the Main Program

```bash
python main.py
```

### Menu Options

1. **Test with generated signals**
   - Demonstrates classification with 5 different test signals
   - Includes: sine waves, multi-frequency signals, exponential decay, white noise, and chirp signals

2. **Record signals**
   - Record real-life signals:
     - Fan noise (5 seconds)
     - Clapping (3 seconds)
     - Traffic sound (5 seconds)
     - Music (5 seconds)
   - Automatically analyzes and saves recordings

3. **Load signal from WAV file**
   - Load and analyze existing WAV files
   - Supports mono and stereo audio

4. **Exit**

### Using the SignalClassifier Class

You can also use the `SignalClassifier` class directly in your code:

```python
from signal_classifier import SignalClassifier, record_signal
import numpy as np

# Example 1: Analyze a custom signal
fs = 8000  # Sampling rate
t = np.linspace(0, 1, fs)
signal = np.sin(2 * np.pi * 50 * t)  # 50 Hz sine wave

classifier = SignalClassifier(signal, fs, "My Signal")
summary = classifier.get_classification_summary()
classifier.plot_analysis(save_path="my_signal_analysis.png")

# Example 2: Record audio
classifier = record_signal(duration=3, sampling_rate=44100, signal_name="Test Recording")
summary = classifier.get_classification_summary()
```

## Output

The program creates two directories:

### `output/` Directory
Contains analysis plots (PNG images) for each signal with:
- Time domain plot
- Frequency spectrum
- Autocorrelation function
- Power Spectral Density
- Classification summary
- Spectrogram

### `recordings/` Directory
Contains WAV files of recorded signals for future analysis

## Signal Classification Theory

### Periodic vs Aperiodic Signals

**Periodic Signal:**
- Repeats after a fixed time interval (period T)
- x(t) = x(t + T) for all t
- Examples: pure sine waves, square waves, musical notes

**Aperiodic Signal:**
- Does not repeat in any regular pattern
- Examples: speech, noise, transient events

### Energy vs Power Signals

**Energy Signal:**
- Total energy is finite: E = ∫|x(t)|² dt < ∞
- Average power is zero: P = lim(T→∞) (1/T) ∫|x(t)|² dt = 0
- Examples: pulses, transient signals, time-limited signals

**Power Signal:**
- Total energy is infinite: E → ∞
- Average power is finite and non-zero: 0 < P < ∞
- Examples: periodic signals, random signals

## Technical Details

### Algorithms Used

1. **Autocorrelation for Periodicity:**
   - Computes normalized autocorrelation
   - Finds peaks above threshold (default: 0.3)
   - First significant peak indicates period

2. **Energy/Power Calculation:**
   - Energy: E = Σ|x[n]|²
   - Power: P = (1/N) Σ|x[n]|²
   - Classification based on normalized energy

3. **FFT for Frequency Analysis:**
   - Fast Fourier Transform for frequency spectrum
   - Welch's method for Power Spectral Density

## Example Results

### Expected Classifications:

| Signal Type | Periodicity | Energy/Power |
|-------------|-------------|--------------|
| Fan Noise | Periodic/Quasi-periodic | Power Signal |
| Clapping | Aperiodic | Energy Signal |
| Traffic Sound | Aperiodic | Power Signal |
| Music (sustained) | Periodic | Power Signal |
| Music (short clip) | Periodic | Energy Signal |

## Project Structure

```
sns-signal-analysis/
├── signal_classifier.py    # Main classification module
├── main.py                  # Interactive main script
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── output/                 # Generated analysis plots
└── recordings/             # Recorded audio files
```

## Troubleshooting

### Audio Recording Issues
- Ensure microphone permissions are granted
- Check `sounddevice` installation: `python -c "import sounddevice; print(sounddevice.query_devices())"`

### Plot Display Issues
- If plots don't display, check matplotlib backend
- Add `import matplotlib; matplotlib.use('TkAgg')` before importing pyplot

## References

- Signals and Systems: Alan V. Oppenheim
- Digital Signal Processing: Proakis & Manolakis
- SciPy Documentation: https://docs.scipy.org/

## License

This project is created for educational purposes as part of ECE coursework.

---

**Student Information:**
- Name: Samyak Jain
- Roll Number: 07611502824
- Branch: ECE-2
- Year: 2nd Year
- Course: Signals and Systems
