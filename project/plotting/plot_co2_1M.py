import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np
from datetime import datetime, timezone
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_processing.loaders import load_csv

# ============================================================
# CONFIGURATION
# ============================================================
PLOT_DIR = 'plots'
DPI = 300
N = 1_000_000

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif', 'serif'],
    'font.size': 12,
    'axes.titlesize': 16,
    'axes.titleweight': 'bold',
    'axes.labelsize': 13,
    'legend.fontsize': 9,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'figure.dpi': 100,
    'savefig.dpi': DPI,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    'figure.facecolor': 'white',
    'axes.facecolor': '#fafafa',
    'axes.edgecolor': '#444444',
    'axes.linewidth': 0.8,
    'lines.linewidth': 0.4,
})

# Custom yellow-to-blue colormap (bottom sensors = yellow = high CO2, top = blue = low CO2)
BLUE_YELLOW_CMAP = mcolors.LinearSegmentedColormap.from_list(
    'yellow_blue',
    ['#FFAB00', '#FFD600', '#FFEE58', '#66BB6A',
     '#42A5F5', '#1565C0', '#0D47A1', '#081D58'],
    N=256
)


def timestamps_to_dates(timestamps):
    return [datetime.fromtimestamp(t, tz=timezone.utc) for t in timestamps]


def setup_date_axis(ax):
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')
    ax.grid(which='minor', axis='x', alpha=0.15, linestyle=':', color='#666666')


def save_figure(fig, name):
    os.makedirs(PLOT_DIR, exist_ok=True)
    path = os.path.join(PLOT_DIR, f'{name}.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    print(f'  Saved: {path}')


# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print(f"  CO2 Main Stack Plot — First {N:,} Data Points")
    print("=" * 60)

    print("\nLoading data...")
    data = load_csv('data/1_CO2_raw_data/data.csv', limit=N)
    dates = timestamps_to_dates(data["Timestamp"])
    print(f"  Loaded {len(dates):,} data points")
    print(f"  Time range: {dates[0].strftime('%Y-%m-%d %H:%M')} to {dates[-1].strftime('%Y-%m-%d %H:%M')}")

    print("\n  Plotting CO2 Main Stack (20 sensors)...")
    fig, ax = plt.subplots(figsize=(16, 7))

    for i in range(20):
        color = BLUE_YELLOW_CMAP(i / 19)
        ax.plot(dates, data["CO2_main"][i], color=color, linewidth=0.3, alpha=0.85)

    ax.set_title(r'CO$_2$ Concentration — Main Stack (20 sensors) — First {:,} samples'.format(N))
    ax.set_xlabel('Date')
    ax.set_ylabel(r'CO$_2$ Concentration (%)')
    setup_date_axis(ax)

    # Colorbar
    norm = mcolors.Normalize(vmin=0, vmax=95)
    sm = cm.ScalarMappable(cmap=BLUE_YELLOW_CMAP, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, pad=0.02, aspect=30)
    cbar.set_label('Sensor height (cm)', fontsize=12)

    save_figure(fig, 'co2_1M_main_stack')

    print(f"\n{'=' * 60}")
    print(f"  Figure saved to '{PLOT_DIR}/'")
    print(f"  Displaying interactive plot — close window when done.")
    print(f"{'=' * 60}")

    plt.show()
