"""
Main Script for Signal Classification
Author: Samyak Jain
Roll No: 07611502824
Branch: ECE-2, 2nd Year

This script demonstrates signal recording, analysis, and classification.
"""

from signal_classifier import (
    SignalClassifier, 
    record_signal, 
    load_signal_from_wav,
    generate_test_signals
)
import os


def main():
    """Main function to demonstrate signal classification"""
    
    print("\n" + "="*60)
    print("SIGNAL CLASSIFICATION PROJECT")
    print("Unit I: Classification of Real-Life Signals")
    print("="*60)
    
    print("\nThis program will classify signals as:")
    print("1. Periodic or Aperiodic")
    print("2. Energy Signal or Power Signal")
    
    print("\n" + "-"*60)
    print("SELECT MODE:")
    print("-"*60)
    print("1. Test with generated signals")
    print("2. Record signals (fan noise, clapping, traffic, music)")
    print("3. Load signal from WAV file")
    print("4. Exit")
    print("-"*60)
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        # Test with generated signals
        print("\nGenerating test signals...")
        test_signals = generate_test_signals()
        
        print(f"\nGenerated {len(test_signals)} test signals")
        print("\nAnalyzing each signal...\n")
        
        # Create output directory
        os.makedirs('output', exist_ok=True)
        
        for i, classifier in enumerate(test_signals, 1):
            print(f"\n{'='*60}")
            print(f"Signal {i}: {classifier.name}")
            print('='*60)
            
            # Get classification
            summary = classifier.get_classification_summary()
            
            print(f"\nDuration: {summary['duration']:.3f} seconds")
            print(f"Sampling Rate: {summary['sampling_rate']} Hz")
            print(f"\nPERIODICITY: {'PERIODIC' if summary['is_periodic'] else 'APERIODIC'}")
            if summary['period']:
                print(f"  → Period: {summary['period']:.4f} seconds")
                print(f"  → Frequency: {summary['frequency']:.2f} Hz")
            print(f"\nENERGY/POWER: {summary['classification']}")
            print(f"  → Total Energy: {summary['energy']:.6e}")
            print(f"  → Average Power: {summary['power']:.6e}")
            
            # Plot and save
            save_path = f"output/signal_{i}_{classifier.name.replace(' ', '_')}.png"
            classifier.plot_analysis(save_path)
    
    elif choice == '2':
        # Record real-life signals
        print("\n" + "="*60)
        print("RECORD REAL-LIFE SIGNALS")
        print("="*60)
        
        signal_types = [
            ("Fan Noise", 5),
            ("Clapping", 3),
            ("Traffic Sound", 5),
            ("Music", 5)
        ]
        
        print("\nYou will be asked to record the following signals:")
        for i, (name, duration) in enumerate(signal_types, 1):
            print(f"{i}. {name} ({duration} seconds)")
        
        proceed = input("\nReady to start recording? (y/n): ").strip().lower()
        
        if proceed == 'y':
            os.makedirs('output', exist_ok=True)
            os.makedirs('recordings', exist_ok=True)
            
            for i, (name, duration) in enumerate(signal_types, 1):
                print(f"\n{'='*60}")
                print(f"Signal {i}/{len(signal_types)}: {name}")
                print('='*60)
                
                input(f"Press Enter when ready to record {name}...")
                
                # Record signal
                classifier = record_signal(duration, 44100, name)
                
                # Save recording
                import sounddevice as sd
                from scipy.io import wavfile
                wav_path = f"recordings/{name.replace(' ', '_').lower()}.wav"
                wavfile.write(wav_path, classifier.fs, classifier.signal)
                print(f"Recording saved to: {wav_path}")
                
                # Analyze
                summary = classifier.get_classification_summary()
                
                print(f"\nCLASSIFICATION RESULTS:")
                print(f"→ Periodicity: {'PERIODIC' if summary['is_periodic'] else 'APERIODIC'}")
                if summary['period']:
                    print(f"  Period: {summary['period']:.4f} s, Frequency: {summary['frequency']:.2f} Hz")
                print(f"→ Type: {summary['classification']}")
                print(f"  Energy: {summary['energy']:.6e}, Power: {summary['power']:.6e}")
                
                # Plot
                save_path = f"output/{name.replace(' ', '_').lower()}_analysis.png"
                classifier.plot_analysis(save_path)
                
                print(f"\nAnalysis plot saved to: {save_path}")
        else:
            print("Recording cancelled.")
    
    elif choice == '3':
        # Load from WAV file
        print("\n" + "="*60)
        print("LOAD SIGNAL FROM WAV FILE")
        print("="*60)
        
        filepath = input("\nEnter path to WAV file: ").strip()
        
        if os.path.exists(filepath):
            try:
                classifier = load_signal_from_wav(filepath)
                
                print(f"\nLoaded: {classifier.name}")
                print(f"Duration: {classifier.duration:.3f} seconds")
                print(f"Sampling Rate: {classifier.fs} Hz")
                
                # Analyze
                summary = classifier.get_classification_summary()
                
                print(f"\nCLASSIFICATION RESULTS:")
                print(f"→ Periodicity: {'PERIODIC' if summary['is_periodic'] else 'APERIODIC'}")
                if summary['period']:
                    print(f"  Period: {summary['period']:.4f} s, Frequency: {summary['frequency']:.2f} Hz")
                print(f"→ Type: {summary['classification']}")
                print(f"  Energy: {summary['energy']:.6e}, Power: {summary['power']:.6e}")
                
                # Plot
                os.makedirs('output', exist_ok=True)
                save_path = f"output/{os.path.splitext(classifier.name)[0]}_analysis.png"
                classifier.plot_analysis(save_path)
                
            except Exception as e:
                print(f"Error loading file: {e}")
        else:
            print(f"File not found: {filepath}")
    
    elif choice == '4':
        print("\nExiting program. Goodbye!")
        return
    
    else:
        print("\nInvalid choice. Please run the program again.")
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print("\nAll plots and recordings saved in 'output/' and 'recordings/' directories")


if __name__ == "__main__":
    main()
