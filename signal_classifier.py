"""
Signal Classification System
Author: Samyak Jain
Roll No: 07611502824
Branch: ECE-2, 2nd Year

This module classifies real-life signals as:
- Periodic or Aperiodic
- Energy Signal or Power Signal
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as sp_signal
from scipy.fft import fft, fftfreq
import sounddevice as sd
from scipy.io import wavfile
import os


class SignalClassifier:
    """Class to analyze and classify signals"""
    
    def __init__(self, signal_data, sampling_rate, signal_name="Signal"):
        """
        Initialize the classifier with signal data
        
        Parameters:
        -----------
        signal_data : array-like
            The signal samples
        sampling_rate : int
            Sampling rate in Hz
        signal_name : str
            Name of the signal for labeling
        """
        self.signal = np.array(signal_data)
        self.fs = sampling_rate
        self.name = signal_name
        self.duration = len(self.signal) / self.fs
        self.time = np.linspace(0, self.duration, len(self.signal))
        
    def check_periodicity(self, threshold=0.3):
        """
        Check if signal is periodic using autocorrelation
        
        Returns:
        --------
        is_periodic : bool
        period : float or None
        """
        # Normalize signal
        normalized_signal = (self.signal - np.mean(self.signal)) / np.std(self.signal)
        
        # Compute autocorrelation
        autocorr = np.correlate(normalized_signal, normalized_signal, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        autocorr = autocorr / autocorr[0]  # Normalize
        
        # Find peaks in autocorrelation (excluding the first peak at lag=0)
        peaks, properties = sp_signal.find_peaks(autocorr[1:], height=threshold)
        
        if len(peaks) > 0:
            # Periodic signal - first peak indicates period
            period_samples = peaks[0] + 1
            period_time = period_samples / self.fs
            return True, period_time
        else:
            # Aperiodic signal
            return False, None
    
    def calculate_energy(self):
        """
        Calculate signal energy
        Energy = sum of |x(t)|^2
        """
        energy = np.sum(np.abs(self.signal)**2)
        return energy
    
    def calculate_power(self):
        """
        Calculate average power
        Power = (1/T) * sum of |x(t)|^2
        """
        power = np.mean(np.abs(self.signal)**2)
        return power
    
    def classify_energy_power(self):
        """
        Classify signal as Energy or Power signal
        
        Energy Signal: Finite energy, zero average power
        Power Signal: Infinite energy, finite non-zero average power
        
        Returns:
        --------
        classification : str
        """
        energy = self.calculate_energy()
        power = self.calculate_power()
        
        # For finite duration signals:
        # - Energy signals have energy proportional to duration
        # - Power signals have constant average power
        
        # Normalize by duration
        normalized_energy = energy / self.duration
        
        # Classification criteria
        if power > 0 and np.isfinite(power):
            if normalized_energy < 1e6:  # Threshold for energy signal
                return "Energy Signal"
            else:
                return "Power Signal"
        else:
            return "Energy Signal"
    
    def compute_fft(self):
        """
        Compute FFT of the signal
        
        Returns:
        --------
        frequencies : array
        magnitude : array
        """
        N = len(self.signal)
        fft_values = fft(self.signal)
        frequencies = fftfreq(N, 1/self.fs)
        magnitude = np.abs(fft_values)
        
        # Return only positive frequencies
        positive_freq_idx = frequencies >= 0
        return frequencies[positive_freq_idx], magnitude[positive_freq_idx]
    
    def plot_analysis(self, save_path=None):
        """
        Create comprehensive analysis plots
        """
        fig = plt.figure(figsize=(15, 10))
        fig.suptitle(f'Signal Analysis: {self.name}', fontsize=16, fontweight='bold')
        
        # 1. Time domain plot
        ax1 = plt.subplot(3, 2, 1)
        ax1.plot(self.time, self.signal, 'b-', linewidth=0.5)
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Amplitude')
        ax1.set_title('Time Domain Signal')
        ax1.grid(True, alpha=0.3)
        
        # 2. Frequency domain plot (FFT)
        ax2 = plt.subplot(3, 2, 2)
        frequencies, magnitude = self.compute_fft()
        ax2.plot(frequencies, magnitude, 'r-', linewidth=0.5)
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Magnitude')
        ax2.set_title('Frequency Spectrum (FFT)')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim([0, self.fs/2])  # Show up to Nyquist frequency
        
        # 3. Autocorrelation
        ax3 = plt.subplot(3, 2, 3)
        normalized_signal = (self.signal - np.mean(self.signal)) / np.std(self.signal)
        autocorr = np.correlate(normalized_signal, normalized_signal, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        autocorr = autocorr / autocorr[0]
        lags = np.arange(len(autocorr)) / self.fs
        ax3.plot(lags[:len(lags)//4], autocorr[:len(autocorr)//4], 'g-')
        ax3.set_xlabel('Lag (s)')
        ax3.set_ylabel('Autocorrelation')
        ax3.set_title('Autocorrelation Function')
        ax3.grid(True, alpha=0.3)
        ax3.axhline(y=0.3, color='r', linestyle='--', label='Threshold')
        ax3.legend()
        
        # 4. Power Spectral Density
        ax4 = plt.subplot(3, 2, 4)
        frequencies_psd, psd = sp_signal.welch(self.signal, self.fs)
        ax4.semilogy(frequencies_psd, psd, 'm-')
        ax4.set_xlabel('Frequency (Hz)')
        ax4.set_ylabel('PSD (V²/Hz)')
        ax4.set_title('Power Spectral Density')
        ax4.grid(True, alpha=0.3)
        
        # 5. Classification Results
        ax5 = plt.subplot(3, 2, 5)
        ax5.axis('off')
        
        # Get classifications
        is_periodic, period = self.check_periodicity()
        energy = self.calculate_energy()
        power = self.calculate_power()
        energy_power_class = self.classify_energy_power()
        
        classification_text = f"""
SIGNAL CLASSIFICATION RESULTS
{'='*40}

Signal Name: {self.name}
Duration: {self.duration:.3f} seconds
Sampling Rate: {self.fs} Hz

PERIODICITY:
{'→'} Type: {'PERIODIC' if is_periodic else 'APERIODIC'}
{'→'} Period: {f'{period:.4f} seconds' if period else 'N/A'}
{'→'} Frequency: {f'{1/period:.2f} Hz' if period else 'N/A'}

ENERGY/POWER:
{'→'} Classification: {energy_power_class}
{'→'} Total Energy: {energy:.6e}
{'→'} Average Power: {power:.6e}
        """
        
        ax5.text(0.1, 0.5, classification_text, fontsize=10, 
                family='monospace', verticalalignment='center')
        
        # 6. Spectrogram
        ax6 = plt.subplot(3, 2, 6)
        if len(self.signal) > 256:
            frequencies_spec, times_spec, Sxx = sp_signal.spectrogram(
                self.signal, self.fs, nperseg=256
            )
            im = ax6.pcolormesh(times_spec, frequencies_spec, 10 * np.log10(Sxx), 
                               shading='gouraud', cmap='viridis')
            ax6.set_ylabel('Frequency (Hz)')
            ax6.set_xlabel('Time (s)')
            ax6.set_title('Spectrogram')
            plt.colorbar(im, ax=ax6, label='Power (dB)')
        else:
            ax6.text(0.5, 0.5, 'Signal too short\nfor spectrogram', 
                    ha='center', va='center', transform=ax6.transAxes)
            ax6.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to: {save_path}")
        
        plt.show()
    
    def get_classification_summary(self):
        """
        Get a text summary of the classification
        """
        is_periodic, period = self.check_periodicity()
        energy = self.calculate_energy()
        power = self.calculate_power()
        energy_power_class = self.classify_energy_power()
        
        summary = {
            'signal_name': self.name,
            'duration': self.duration,
            'sampling_rate': self.fs,
            'is_periodic': is_periodic,
            'period': period,
            'frequency': 1/period if period else None,
            'energy': energy,
            'power': power,
            'classification': energy_power_class
        }
        
        return summary


def record_signal(duration=5, sampling_rate=44100, signal_name="Recording"):
    """
    Record audio signal from microphone
    
    Parameters:
    -----------
    duration : float
        Recording duration in seconds
    sampling_rate : int
        Sampling rate in Hz
    signal_name : str
        Name for the recording
    
    Returns:
    --------
    SignalClassifier object
    """
    print(f"\nRecording '{signal_name}' for {duration} seconds...")
    print("Recording will start in 1 second...")
    sd.sleep(1000)
    print("Recording NOW!")
    
    recording = sd.rec(int(duration * sampling_rate), 
                      samplerate=sampling_rate, 
                      channels=1, 
                      dtype='float64')
    sd.wait()
    print("Recording complete!")
    
    # Flatten to 1D array
    signal_data = recording.flatten()
    
    return SignalClassifier(signal_data, sampling_rate, signal_name)


def load_signal_from_wav(filepath):
    """
    Load signal from WAV file
    
    Parameters:
    -----------
    filepath : str
        Path to WAV file
    
    Returns:
    --------
    SignalClassifier object
    """
    sampling_rate, signal_data = wavfile.read(filepath)
    
    # Convert to float and normalize
    if signal_data.dtype == np.int16:
        signal_data = signal_data.astype(np.float64) / 32768.0
    elif signal_data.dtype == np.int32:
        signal_data = signal_data.astype(np.float64) / 2147483648.0
    
    # If stereo, convert to mono
    if len(signal_data.shape) > 1:
        signal_data = np.mean(signal_data, axis=1)
    
    signal_name = os.path.basename(filepath)
    return SignalClassifier(signal_data, sampling_rate, signal_name)


def generate_test_signals():
    """
    Generate test signals for demonstration
    
    Returns:
    --------
    list of SignalClassifier objects
    """
    fs = 8000  # Sampling rate
    duration = 2  # Duration in seconds
    t = np.linspace(0, duration, int(fs * duration))
    
    signals = []
    
    # 1. Periodic signal (sine wave) - Energy Signal
    signal1 = np.sin(2 * np.pi * 50 * t)
    signals.append(SignalClassifier(signal1, fs, "Sine Wave (50 Hz)"))
    
    # 2. Periodic signal (combination) - Energy Signal
    signal2 = np.sin(2 * np.pi * 100 * t) + 0.5 * np.sin(2 * np.pi * 200 * t)
    signals.append(SignalClassifier(signal2, fs, "Multi-frequency Periodic"))
    
    # 3. Aperiodic signal (exponential decay) - Energy Signal
    signal3 = np.exp(-2 * t) * np.sin(2 * np.pi * 50 * t)
    signals.append(SignalClassifier(signal3, fs, "Exponential Decay"))
    
    # 4. Aperiodic signal (random noise) - Power Signal
    signal4 = np.random.randn(len(t))
    signals.append(SignalClassifier(signal4, fs, "White Noise"))
    
    # 5. Aperiodic signal (chirp) - Energy Signal
    signal5 = sp_signal.chirp(t, f0=20, f1=500, t1=duration, method='linear')
    signals.append(SignalClassifier(signal5, fs, "Chirp Signal"))
    
    return signals


if __name__ == "__main__":
    print("="*60)
    print("SIGNAL CLASSIFICATION SYSTEM")
    print("Author: Samyak Jain (07611502824)")
    print("Branch: ECE-2, 2nd Year")
    print("="*60)
