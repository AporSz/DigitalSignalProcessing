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

MAIN_HEIGHTS_CM = [i * 5 for i in range(20)]


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
    print(f"  Temperature Plot — First {N:,} Data Points")
    print("=" * 60)

    print("\nLoading data...")
    data = load_csv('data/1_CO2_raw_data/data.csv', limit=N)
    dates = timestamps_to_dates(data["Timestamp"])
    print(f"  Loaded {len(dates):,} data points")
    print(f"  Time range: {dates[0].strftime('%Y-%m-%d %H:%M')} to {dates[-1].strftime('%Y-%m-%d %H:%M')}")

    # ── Figure 1: Main Stack Temperature (20 sensors) ──
    print("\n  [1/3] Temperature Main Stack (20 sensors)...")
    fig1, ax1 = plt.subplots(figsize=(16, 7))

    cmap = plt.colormaps['coolwarm']
    for i in range(20):
        color = cmap(i / 19)
        ax1.plot(dates, data["Temperature_main"][i], color=color, linewidth=0.3, alpha=0.85)

    ax1.set_title(f'Temperature — Main Stack (20 sensors) — First {N:,} samples')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Temperature (°C)')
    setup_date_axis(ax1)

    # Colorbar
    norm = mcolors.Normalize(vmin=0, vmax=95)
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig1.colorbar(sm, ax=ax1, pad=0.02, aspect=30)
    cbar.set_label('Sensor height (cm)', fontsize=12)

    save_figure(fig1, 'temp_1M_main_stack')

    # ── Figure 2: Side Tube Temperature (4 sensors) ──
    print("  [2/3] Temperature Side Tube (4 sensors)...")
    fig2, ax2 = plt.subplots(figsize=(16, 7))

    side_colors = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63']
    side_labels = ['Side 1 (top)', 'Side 2', 'Side 3', 'Side 4 (bottom)']
    for i in range(4):
        ax2.plot(dates, data["Temperature_side"][i], color=side_colors[i],
                 linewidth=0.4, alpha=0.8, label=side_labels[i])

    ax2.set_title(f'Temperature — Side Tube (4 sensors) — First {N:,} samples')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Temperature (°C)')
    ax2.legend(loc='upper right', framealpha=0.9, edgecolor='#cccccc')
    setup_date_axis(ax2)

    save_figure(fig2, 'temp_1M_side_tube')

    # ── Figure 3: Ambient Temperature (BMP280 top & bottom) ──
    print("  [3/3] Ambient Temperature (top & bottom)...")
    fig3, ax3 = plt.subplots(figsize=(16, 7))

    ax3.plot(dates, data["Temperature_Top"], color='#C62828', linewidth=0.4,
             alpha=0.8, label='Top sensor (BMP280)')
    ax3.plot(dates, data["Temperature_Bottom"], color='#1565C0', linewidth=0.4,
             alpha=0.8, label='Bottom sensor (BMP280)')

    ax3.set_title(f'Ambient Temperature — Top & Bottom — First {N:,} samples')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Temperature (°C)')
    ax3.legend(loc='upper right', framealpha=0.9, edgecolor='#cccccc')
    setup_date_axis(ax3)

    save_figure(fig3, 'temp_1M_ambient')

    print(f"\n{'=' * 60}")
    print(f"  All 3 temperature figures saved to '{PLOT_DIR}/'")
    print(f"  Displaying interactive plots — close windows when done.")
    print(f"{'=' * 60}")

    plt.show()
