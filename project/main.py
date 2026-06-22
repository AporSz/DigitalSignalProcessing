import sys
import argparse
import subprocess

def run_script(script_name):
    print(f"\n[{script_name}] Starting...")
    subprocess.run([sys.executable, script_name])
    print(f"[{script_name}] Finished.\n")

def main():
    print("=" * 60)
    print("  CO2 Mofette Dynamics — Main Entry Point")
    print("=" * 60)
    
    parser = argparse.ArgumentParser(description="Run the DSP project scripts.")
    parser.add_argument('--dsp', action='store_true', help='Run the main DSP analysis (filtering, Welch, spectrogram)')
    parser.add_argument('--co2', action='store_true', help='Run the CO2 main stack heatmap')
    parser.add_argument('--temp', action='store_true', help='Run the Temperature main stack heatmap')
    parser.add_argument('--all', action='store_true', help='Run all scripts sequentially')

    args = parser.parse_args()

    if not any([args.dsp, args.co2, args.temp, args.all]):
        print("\nPlease select a script to run, or run all of them:\n")
        parser.print_help()
        print("\nExample: python main.py --all")
        sys.exit(0)

    if args.dsp or args.all:
        run_script('filtering/dsp_analysis.py')
    
    if args.co2 or args.all:
        run_script('plotting/plot_co2_1M.py')

    if args.temp or args.all:
        run_script('plotting/plot_temperature_1M.py')

if __name__ == '__main__':
    main()
