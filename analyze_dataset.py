"""
Analyze All Dataset Files
Author: Samyak Jain
Roll No: 07611502824
Branch: ECE-2, 2nd Year

This script analyzes all audio files in the dataset directory
and generates comprehensive classification reports.
"""

import os
from signal_classifier import SignalClassifier, load_signal_from_wav
from pathlib import Path
import matplotlib.pyplot as plt


def convert_mp3_to_wav(mp3_file):
    """Convert MP3 to WAV using pydub if available"""
    try:
        from pydub import AudioSegment
        
        wav_file = mp3_file.replace('.mp3', '.wav')
        if not os.path.exists(wav_file):
            print(f"  Converting {os.path.basename(mp3_file)} to WAV...")
            audio = AudioSegment.from_mp3(mp3_file)
            audio.export(wav_file, format="wav")
            print(f"  ✓ Converted to WAV")
        return wav_file
    except ImportError:
        print(f"  ⚠ pydub not installed, skipping MP3 file: {os.path.basename(mp3_file)}")
        print("    Install with: pip install pydub")
        return None
    except Exception as e:
        print(f"  ✗ Error converting {mp3_file}: {e}")
        return None


def analyze_all_dataset_files(dataset_dir="dataset"):
    """Analyze all audio files in the dataset directory"""
    
    print("\n" + "="*70)
    print("DATASET ANALYSIS - Signal Classification Project")
    print("Author: Samyak Jain (07611502824)")
    print("="*70)
    
    # Find all audio files
    audio_extensions = ['.wav', '.mp3']
    audio_files = []
    
    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in audio_extensions):
                audio_files.append(os.path.join(root, file))
    
    if not audio_files:
        print(f"\n⚠ No audio files found in '{dataset_dir}' directory")
        print("Run 'python download_dataset.py' first to download sample files.")
        return
    
    print(f"\nFound {len(audio_files)} audio files to analyze\n")
    
    # Create output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    successful = 0
    
    for i, audio_file in enumerate(audio_files, 1):
        print(f"\n{'='*70}")
        print(f"[{i}/{len(audio_files)}] Analyzing: {os.path.basename(audio_file)}")
        print('='*70)
        
        try:
            # Convert MP3 to WAV if needed
            if audio_file.lower().endswith('.mp3'):
                wav_file = convert_mp3_to_wav(audio_file)
                if wav_file is None:
                    continue
                audio_file = wav_file
            
            # Load and analyze signal
            classifier = load_signal_from_wav(audio_file)
            
            print(f"Duration: {classifier.duration:.2f} seconds")
            print(f"Sampling Rate: {classifier.fs} Hz")
            
            # Get classification
            summary = classifier.get_classification_summary()
            
            # Display results
            print(f"\n{'─'*70}")
            print("CLASSIFICATION RESULTS:")
            print('─'*70)
            print(f"Periodicity: {'PERIODIC' if summary['is_periodic'] else 'APERIODIC'}")
            if summary['period']:
                print(f"  → Period: {summary['period']:.4f} seconds")
                print(f"  → Frequency: {summary['frequency']:.2f} Hz")
            print(f"\nType: {summary['classification']}")
            print(f"  → Energy: {summary['energy']:.6e}")
            print(f"  → Power: {summary['power']:.6e}")
            
            # Generate plot
            base_name = os.path.splitext(os.path.basename(audio_file))[0]
            output_file = os.path.join(output_dir, f"{base_name}_analysis.png")
            classifier.plot_analysis(output_file)
            
            # Store results
            results.append({
                'filename': os.path.basename(audio_file),
                'duration': summary['duration'],
                'is_periodic': summary['is_periodic'],
                'period': summary['period'],
                'frequency': summary['frequency'],
                'classification': summary['classification'],
                'energy': summary['energy'],
                'power': summary['power']
            })
            
            successful += 1
            
        except Exception as e:
            print(f"\n✗ Error analyzing {os.path.basename(audio_file)}: {e}")
            continue
    
    # Generate summary report
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print(f"Successfully analyzed: {successful}/{len(audio_files)} files")
    print(f"Results saved to: {os.path.abspath(output_dir)}/")
    
    # Create summary table
    if results:
        print("\n" + "="*70)
        print("SUMMARY TABLE")
        print("="*70)
        print(f"{'File':<30} {'Periodic':<10} {'Type':<15} {'Duration':<10}")
        print("-"*70)
        for result in results:
            periodic = "YES" if result['is_periodic'] else "NO"
            classification = result['classification'].replace(' Signal', '')
            print(f"{result['filename']:<30} {periodic:<10} {classification:<15} {result['duration']:.2f}s")
        
        # Statistics
        print("\n" + "="*70)
        print("STATISTICS")
        print("="*70)
        periodic_count = sum(1 for r in results if r['is_periodic'])
        aperiodic_count = len(results) - periodic_count
        energy_count = sum(1 for r in results if 'Energy' in r['classification'])
        power_count = len(results) - energy_count
        
        print(f"Periodic Signals:   {periodic_count}/{len(results)} ({periodic_count/len(results)*100:.1f}%)")
        print(f"Aperiodic Signals: {aperiodic_count}/{len(results)} ({aperiodic_count/len(results)*100:.1f}%)")
        print(f"Energy Signals:    {energy_count}/{len(results)} ({energy_count/len(results)*100:.1f}%)")
        print(f"Power Signals:     {power_count}/{len(results)} ({power_count/len(results)*100:.1f}%)")
        
        # Save summary to file
        summary_file = os.path.join(output_dir, "analysis_summary.txt")
        with open(summary_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write("SIGNAL CLASSIFICATION ANALYSIS SUMMARY\n")
            f.write("Author: Samyak Jain (07611502824)\n")
            f.write("Branch: ECE-2, 2nd Year\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Total Files Analyzed: {len(results)}\n\n")
            
            f.write(f"{'File':<30} {'Periodic':<10} {'Type':<15} {'Duration':<10}\n")
            f.write("-"*70 + "\n")
            for result in results:
                periodic = "YES" if result['is_periodic'] else "NO"
                classification = result['classification'].replace(' Signal', '')
                f.write(f"{result['filename']:<30} {periodic:<10} {classification:<15} {result['duration']:.2f}s\n")
            
            f.write("\n" + "="*70 + "\n")
            f.write("STATISTICS\n")
            f.write("="*70 + "\n")
            f.write(f"Periodic Signals:   {periodic_count}/{len(results)} ({periodic_count/len(results)*100:.1f}%)\n")
            f.write(f"Aperiodic Signals: {aperiodic_count}/{len(results)} ({aperiodic_count/len(results)*100:.1f}%)\n")
            f.write(f"Energy Signals:    {energy_count}/{len(results)} ({energy_count/len(results)*100:.1f}%)\n")
            f.write(f"Power Signals:     {power_count}/{len(results)} ({power_count/len(results)*100:.1f}%)\n")
        
        print(f"\nSummary report saved to: {summary_file}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    analyze_all_dataset_files()
