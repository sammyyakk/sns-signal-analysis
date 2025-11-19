# 🚀 QUICK START GUIDE

**No Recording Needed!** Just run these commands:

## Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 2: Download/Create Sample Audio Files
```bash
python download_dataset.py
```
**What this does:**
- Creates 8 synthetic audio signals (sine waves, chirps, noise, etc.)
- Optionally downloads real audio samples from the internet
- Saves everything to `dataset/` folder

## Step 3: Analyze All Signals at Once
```bash
python analyze_dataset.py
```
**What this does:**
- Processes all audio files in the dataset
- Classifies each as Periodic/Aperiodic
- Classifies each as Energy/Power signal
- Generates detailed plots for each signal
- Creates a summary report with statistics

## That's It! 🎉

Your results will be in:
- `output/` - Analysis plots (PNG files)
- `output/analysis_summary.txt` - Summary report

## Optional: Interactive Mode
```bash
python main.py
```
Choose option 1 to test with generated signals, or option 3 to analyze specific files.

---

**Author:** Samyak Jain (07611502824)  
**Branch:** ECE-2, 2nd Year
