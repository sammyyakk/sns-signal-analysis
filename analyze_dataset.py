"""
Analyze All Dataset Files - Batch Signal Classification
========================================================

Author: Samyak Jain
Roll No: 07611502824
Branch: ECE-2, 2nd Year
Unit I: Classification of Real-Life Signals

Description:
-----------
This script automatically processes all audio files in the dataset directory
and performs comprehensive signal analysis including:
    - Periodicity detection (Periodic vs Aperiodic)
    - Energy/Power signal classification
    - Time-domain and frequency-domain analysis
    - Generation of detailed visualization plots
    - Statistical summary reports

The script is designed to handle multiple audio formats and generate
professional reports suitable for academic assignments.
"""

# ============================================================================
# Import Required Libraries
# ============================================================================
import os                      # For file and directory operations
from signal_classifier import SignalClassifier, load_signal_from_wav
from pathlib import Path       # For modern path handling
import matplotlib.pyplot as plt  # For plotting (imported but mainly used in classifier)


# ============================================================================
# Helper Functions
# ============================================================================

def convert_mp3_to_wav(mp3_file):
    """
    Convert MP3 audio file to WAV format for processing.
    
    Purpose:
    --------
    WAV files are easier to process for signal analysis as they store
    uncompressed audio data. This function converts MP3 files to WAV
    format using the pydub library.
    
    Parameters:
    -----------
    mp3_file : str
        Path to the MP3 file to be converted
    
    Returns:
    --------
    str or None
        Path to the converted WAV file if successful, None otherwise
    
    Technical Note:
    ---------------
    MP3 uses lossy compression which can affect signal analysis.
    Converting to WAV ensures we have access to the complete waveform data.
    """
    try:
        # Import AudioSegment for audio file conversion
        from pydub import AudioSegment
        
        # Generate output WAV filename
        wav_file = mp3_file.replace('.mp3', '.wav')
        
        # Check if WAV file already exists to avoid redundant conversion
        if not os.path.exists(wav_file):
            print(f"  Converting {os.path.basename(mp3_file)} to WAV...")
            
            # Load MP3 file and convert to WAV format
            audio = AudioSegment.from_mp3(mp3_file)
            audio.export(wav_file, format="wav")
            
            print(f"  ✓ Converted to WAV")
        
        return wav_file
        
    except ImportError:
        # pydub library is not installed
        print(f"  ⚠ pydub not installed, skipping MP3 file: {os.path.basename(mp3_file)}")
        print("    Install with: pip install pydub")
        return None
        
    except Exception as e:
        # Handle any other errors during conversion
        print(f"  ✗ Error converting {mp3_file}: {e}")
        return None


def analyze_all_dataset_files(dataset_dir="dataset"):
    """
    Main function to analyze all audio files in the dataset directory.
    
    Purpose:
    --------
    This function performs batch processing of all audio files found in the
    dataset directory. For each file, it performs signal classification and
    generates comprehensive analysis reports.
    
    Parameters:
    -----------
    dataset_dir : str
        Path to the directory containing audio files (default: "dataset")
    
    Process Flow:
    -------------
    1. Scan dataset directory for audio files (.wav, .mp3)
    2. Convert MP3 files to WAV if necessary
    3. Load and analyze each signal
    4. Classify signals as Periodic/Aperiodic and Energy/Power
    5. Generate visualization plots
    6. Compile statistical summary report
    
    Returns:
    --------
    None (generates output files and prints results)
    """
    
    # ========================================================================
    # Display Header Information
    # ========================================================================
    print("\n" + "="*70)
    print("DATASET ANALYSIS - Signal Classification Project")
    print("Author: Samyak Jain (07611502824)")
    print("="*70)
    
    # ========================================================================
    # Step 1: Discover All Audio Files in Dataset Directory
    # ========================================================================
    # Define supported audio file extensions
    audio_extensions = ['.wav', '.mp3']
    audio_files = []
    
    # Walk through all subdirectories to find audio files
    # os.walk() returns (directory_path, subdirectories, files) for each directory
    for root, dirs, files in os.walk(dataset_dir):
        for file in files:
            # Check if file has a supported audio extension (case-insensitive)
            if any(file.lower().endswith(ext) for ext in audio_extensions):
                # Store the complete path to the audio file
                audio_files.append(os.path.join(root, file))
    
    # Check if any audio files were found
    if not audio_files:
        print(f"\n⚠ No audio files found in '{dataset_dir}' directory")
        print("Run 'python download_dataset.py' first to download sample files.")
        return
    
    print(f"\nFound {len(audio_files)} audio files to analyze\n")
    
    # ========================================================================
    # Step 2: Prepare Output Directory
    # ========================================================================
    output_dir = "output"
    # Create output directory if it doesn't exist
    # exist_ok=True prevents error if directory already exists
    os.makedirs(output_dir, exist_ok=True)
    
    # ========================================================================
    # Step 3: Initialize Results Storage
    # ========================================================================
    results = []      # List to store classification results for all files
    successful = 0    # Counter for successfully analyzed files
    
    # ========================================================================
    # Step 4: Process Each Audio File
    # ========================================================================
    for i, audio_file in enumerate(audio_files, 1):
        # Display progress header for current file
        print(f"\n{'='*70}")
        print(f"[{i}/{len(audio_files)}] Analyzing: {os.path.basename(audio_file)}")
        print('='*70)
        
        try:
            # ----------------------------------------------------------------
            # Step 4.1: Handle MP3 Files (Convert to WAV if needed)
            # ----------------------------------------------------------------
            if audio_file.lower().endswith('.mp3'):
                wav_file = convert_mp3_to_wav(audio_file)
                # Skip this file if conversion failed
                if wav_file is None:
                    continue
                # Use the converted WAV file for analysis
                audio_file = wav_file
            
            # ----------------------------------------------------------------
            # Step 4.2: Load Signal from Audio File
            # ----------------------------------------------------------------
            # This creates a SignalClassifier object with the audio data
            classifier = load_signal_from_wav(audio_file)
            
            # Display basic signal properties
            print(f"Duration: {classifier.duration:.2f} seconds")
            print(f"Sampling Rate: {classifier.fs} Hz")
            
            # ----------------------------------------------------------------
            # Step 4.3: Perform Signal Classification
            # ----------------------------------------------------------------
            # Get comprehensive classification summary
            # This includes periodicity, energy/power classification, etc.
            summary = classifier.get_classification_summary()
            
            # ----------------------------------------------------------------
            # Step 4.4: Display Classification Results
            # ----------------------------------------------------------------
            print(f"\n{'─'*70}")
            print("CLASSIFICATION RESULTS:")
            print('─'*70)
            
            # Display periodicity classification
            print(f"Periodicity: {'PERIODIC' if summary['is_periodic'] else 'APERIODIC'}")
            
            # If signal is periodic, display period and frequency
            if summary['period']:
                print(f"  → Period: {summary['period']:.4f} seconds")
                print(f"  → Frequency: {summary['frequency']:.2f} Hz")
            
            # Display energy/power classification
            print(f"\nType: {summary['classification']}")
            print(f"  → Energy: {summary['energy']:.6e}")
            print(f"  → Power: {summary['power']:.6e}")
            
            # ----------------------------------------------------------------
            # Step 4.5: Generate and Save Visualization Plot
            # ----------------------------------------------------------------
            # Extract filename without extension for output file naming
            base_name = os.path.splitext(os.path.basename(audio_file))[0]
            output_file = os.path.join(output_dir, f"{base_name}_analysis.png")
            
            # Generate comprehensive 6-panel analysis plot
            classifier.plot_analysis(output_file)
            
            # ----------------------------------------------------------------
            # Step 4.6: Store Results for Summary Report
            # ----------------------------------------------------------------
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
            
            # Increment successful analysis counter
            successful += 1
            
        except Exception as e:
            # Handle any errors during analysis
            print(f"\n✗ Error analyzing {os.path.basename(audio_file)}: {e}")
            continue  # Skip to next file
    
    # ========================================================================
    # Step 5: Generate Summary Report
    # ========================================================================
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print(f"Successfully analyzed: {successful}/{len(audio_files)} files")
    print(f"Results saved to: {os.path.abspath(output_dir)}/")
    
    # ========================================================================
    # Step 6: Create Summary Table
    # ========================================================================
    if results:
        print("\n" + "="*70)
        print("SUMMARY TABLE")
        print("="*70)
        
        # Print table header with column names
        print(f"{'File':<30} {'Periodic':<10} {'Type':<15} {'Duration':<10}")
        print("-"*70)
        
        # Print each signal's classification results in tabular format
        for result in results:
            # Convert boolean to YES/NO for better readability
            periodic = "YES" if result['is_periodic'] else "NO"
            # Remove 'Signal' suffix to shorten classification name
            classification = result['classification'].replace(' Signal', '')
            # Print row with formatted columns
            print(f"{result['filename']:<30} {periodic:<10} {classification:<15} {result['duration']:.2f}s")
        
        # ====================================================================
        # Step 7: Calculate and Display Statistics
        # ====================================================================
        print("\n" + "="*70)
        print("STATISTICS")
        print("="*70)
        
        # Count periodic vs aperiodic signals
        # Uses list comprehension to count signals where is_periodic is True
        periodic_count = sum(1 for r in results if r['is_periodic'])
        aperiodic_count = len(results) - periodic_count
        
        # Count energy vs power signals
        # Checks if 'Energy' is in the classification string
        energy_count = sum(1 for r in results if 'Energy' in r['classification'])
        power_count = len(results) - energy_count
        
        # Display statistics with counts and percentages
        print(f"Periodic Signals:   {periodic_count}/{len(results)} ({periodic_count/len(results)*100:.1f}%)")
        print(f"Aperiodic Signals: {aperiodic_count}/{len(results)} ({aperiodic_count/len(results)*100:.1f}%)")
        print(f"Energy Signals:    {energy_count}/{len(results)} ({energy_count/len(results)*100:.1f}%)")
        print(f"Power Signals:     {power_count}/{len(results)} ({power_count/len(results)*100:.1f}%)")
        
        # ====================================================================
        # Step 8: Save Summary Report to Text File
        # ====================================================================
        summary_file = os.path.join(output_dir, "analysis_summary.txt")
        
        # Open file in write mode and save formatted report
        with open(summary_file, 'w') as f:
            # Write header section
            f.write("="*70 + "\n")
            f.write("SIGNAL CLASSIFICATION ANALYSIS SUMMARY\n")
            f.write("Author: Samyak Jain (07611502824)\n")
            f.write("Branch: ECE-2, 2nd Year\n")
            f.write("Unit I: Classification of Real-Life Signals\n")
            f.write("="*70 + "\n\n")
            
            # Write total files count
            f.write(f"Total Files Analyzed: {len(results)}\n\n")
            
            # Write detailed results table
            f.write(f"{'File':<30} {'Periodic':<10} {'Type':<15} {'Duration':<10}\n")
            f.write("-"*70 + "\n")
            
            # Write each signal's results
            for result in results:
                periodic = "YES" if result['is_periodic'] else "NO"
                classification = result['classification'].replace(' Signal', '')
                f.write(f"{result['filename']:<30} {periodic:<10} {classification:<15} {result['duration']:.2f}s\n")
            
            # Write statistics section
            f.write("\n" + "="*70 + "\n")
            f.write("STATISTICS\n")
            f.write("="*70 + "\n")
            f.write(f"Periodic Signals:   {periodic_count}/{len(results)} ({periodic_count/len(results)*100:.1f}%)\n")
            f.write(f"Aperiodic Signals: {aperiodic_count}/{len(results)} ({aperiodic_count/len(results)*100:.1f}%)\n")
            f.write(f"Energy Signals:    {energy_count}/{len(results)} ({energy_count/len(results)*100:.1f}%)\n")
            f.write(f"Power Signals:     {power_count}/{len(results)} ({power_count/len(results)*100:.1f}%)\n")
        
        print(f"\nSummary report saved to: {summary_file}")
    
    print("\n" + "="*70)


# ============================================================================
# Main Execution
# ============================================================================
if __name__ == "__main__":
    """
    Entry point for the script when run directly.
    
    This block only executes when the script is run directly (not imported).
    It calls the main analysis function to process all dataset files.
    """
    analyze_all_dataset_files()
