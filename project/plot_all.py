import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np
from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.data_utils import get_data_by_minute


PLOT_DIR = 'plots'
DPI = 300
FIGSIZE_SINGLE = (16, 7)
FIGSIZE_COMBO = (16, 12)
FIGSIZE_HEATMAP = (18, 6)

# Publication-quality style
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
    'lines.linewidth': 0.6,
})

# Sensor physical positions
MAIN_HEIGHTS_CM = [i * 5 for i in range(20)]  # 0, 5, 10, ..., 95 cm
SIDE_LABELS = ['Side 1 (top)', 'Side 2', 'Side 3', 'Side 4 (bottom)']

# Custom yellow-to-blue colormap for CO2 main stack
# bottom sensors (high CO2, top of graph) = yellow, top sensors (low CO2, bottom of graph) = blue
BLUE_YELLOW_CMAP = mcolors.LinearSegmentedColormap.from_list(
    'yellow_blue',
    ['#FFAB00', '#FFD600', '#FFEE58', '#66BB6A',  # yellows → greens
     '#42A5F5', '#1565C0', '#0D47A1', '#081D58'],  # → dark navy
    N=256
)


def timestamps_to_dates(timestamps):
    return [datetime.utcfromtimestamp(t) for t in timestamps]


def setup_date_axis(ax, weekly_grid=True):
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')
    if weekly_grid:
        ax.grid(which='minor', axis='x', alpha=0.15, linestyle=':', color='#666666')
        ax.tick_params(axis='x', which='minor', length=3, color='#999999')


def save_figure(fig, name):
    os.makedirs(PLOT_DIR, exist_ok=True)
    path = os.path.join(PLOT_DIR, f'{name}.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    print(f'  Saved: {path}')


def add_height_colorbar(fig, ax, cmap_name, n_sensors, heights, label='Sensor height (cm)'):
    norm = mcolors.Normalize(vmin=min(heights), vmax=max(heights))
    cmap = plt.colormaps[cmap_name]
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, pad=0.02, aspect=30)
    cbar.set_label(label, fontsize=12)
    return cbar



def plot_co2_main(dates, data):
    print("  [1/10] CO2 Main Stack...")
    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    for i in range(20):
        color = BLUE_YELLOW_CMAP(i / 19)
        ax.plot(dates, data["CO2_main"][i], color=color, linewidth=0.4, alpha=0.85)

    ax.set_title(r'CO$_2$ Concentration — Main Stack (20 sensors)')
    ax.set_xlabel('Date')
    ax.set_ylabel(r'CO$_2$ Concentration (%)')
    setup_date_axis(ax)

    # Colorbar with the custom blue→yellow colormap
    norm = mcolors.Normalize(vmin=min(MAIN_HEIGHTS_CM), vmax=max(MAIN_HEIGHTS_CM))
    sm = cm.ScalarMappable(cmap=BLUE_YELLOW_CMAP, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, pad=0.02, aspect=30)
    cbar.set_label('Sensor height (cm)', fontsize=12)

    save_figure(fig, '01_CO2_main_stack')
    return fig


def plot_co2_side(dates, data):
    print("  [2/10] CO2 Side Tube...")
    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    colors = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63']
    for i in range(4):
        ax.plot(dates, data["CO2_side"][i], color=colors[i], linewidth=0.5,
                alpha=0.8, label=SIDE_LABELS[i])

    ax.set_title(r'CO$_2$ Concentration — Side Tube (4 sensors)')
    ax.set_xlabel('Date')
    ax.set_ylabel(r'CO$_2$ Concentration (%)')
    ax.legend(loc='upper right', framealpha=0.9, edgecolor='#cccccc')
    setup_date_axis(ax)

    save_figure(fig, '02_CO2_side_tube')
    return fig


def plot_temp_main(dates, data):
    print("  [3/10] Temperature Main Stack...")
    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    cmap = plt.colormaps['coolwarm']
    for i in range(20):
        color = cmap(i / 19)
        ax.plot(dates, data["Temperature_main"][i], color=color, linewidth=0.4, alpha=0.85)

    ax.set_title('Temperature — Main Stack (20 sensors)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature (°C)')
    setup_date_axis(ax)
    add_height_colorbar(fig, ax, 'coolwarm', 20, MAIN_HEIGHTS_CM)

    save_figure(fig, '03_Temperature_main_stack')
    return fig


def plot_temp_side(dates, data):
    print("  [4/10] Temperature Side Tube...")
    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    colors = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63']
    for i in range(4):
        ax.plot(dates, data["Temperature_side"][i], color=colors[i], linewidth=0.5,
                alpha=0.8, label=SIDE_LABELS[i])

    ax.set_title('Temperature — Side Tube (4 sensors)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature (°C)')
    ax.legend(loc='upper right', framealpha=0.9, edgecolor='#cccccc')
    setup_date_axis(ax)

    save_figure(fig, '04_Temperature_side_tube')
    return fig


def plot_pressure(dates, data):
    print("  [5/10] Barometric Pressure...")
    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    ax.plot(dates, data["Pressure_Top"], color='#1565C0', linewidth=0.5,
            alpha=0.8, label='Top sensor (BMP280)')
    ax.plot(dates, data["Pressure_Bottom"], color='#E65100', linewidth=0.5,
            alpha=0.8, label='Bottom sensor (BMP280)')

    ax.set_title('Barometric Pressure')
    ax.set_xlabel('Date')
    ax.set_ylabel('Pressure (Pa)')
    ax.legend(loc='upper right', framealpha=0.9, edgecolor='#cccccc')
    setup_date_axis(ax)

    save_figure(fig, '05_Pressure')
    return fig


def plot_humidity(dates, data):
    print("  [6/10] Humidity...")
    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    ax.plot(dates, data["Humidity_Top"], color='#00838F', linewidth=0.5,
            alpha=0.8, label='Top sensor (DHT11)')
    ax.plot(dates, data["Humidity_Bottom"], color='#AD1457', linewidth=0.5,
            alpha=0.8, label='Bottom sensor (DHT11)')

    ax.set_title('Relative Humidity')
    ax.set_xlabel('Date')
    ax.set_ylabel('Humidity (%RH)')
    ax.legend(loc='upper right', framealpha=0.9, edgecolor='#cccccc')
    setup_date_axis(ax)

    save_figure(fig, '06_Humidity')
    return fig


def plot_ambient_temp(dates, data):
    print("  [7/10] Ambient Temperature...")
    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)

    ax.plot(dates, data["Temperature_Top"], color='#C62828', linewidth=0.5,
            alpha=0.8, label='Top sensor (BMP280)')
    ax.plot(dates, data["Temperature_Bottom"], color='#283593', linewidth=0.5,
            alpha=0.8, label='Bottom sensor (BMP280)')

    ax.set_title('Ambient Temperature')
    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature (°C)')
    ax.legend(loc='upper right', framealpha=0.9, edgecolor='#cccccc')
    setup_date_axis(ax)

    save_figure(fig, '07_Ambient_temperature')
    return fig


def plot_co2_vs_pressure(dates, data):
    print("  [8/10] CO2 vs Pressure...")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=FIGSIZE_COMBO, sharex=True,
                                    gridspec_kw={'height_ratios': [2, 1], 'hspace': 0.08})

    # CO2 — sensor 10 (middle of stack, 50 cm height)
    sensor_idx = 9
    ax1.plot(dates, data["CO2_main"][sensor_idx], color='#D32F2F', linewidth=0.5, alpha=0.8)
    ax1.set_ylabel(r'CO$_2$ Concentration (%)')
    ax1.set_title(r'CO$_2$ (Main Stack, sensor 10 at 50 cm) vs Barometric Pressure')
    ax1.grid(True, alpha=0.3, linestyle='--')

    # Pressure
    ax2.plot(dates, data["Pressure_Top"], color='#1565C0', linewidth=0.5, alpha=0.8)
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Pressure (Pa)')
    ax2.grid(True, alpha=0.3, linestyle='--')
    setup_date_axis(ax2)

    save_figure(fig, '08_CO2_vs_Pressure')
    return fig


def plot_co2_vs_temperature(dates, data):
    print("  [9/10] CO2 vs Temperature...")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=FIGSIZE_COMBO, sharex=True,
                                    gridspec_kw={'height_ratios': [1, 1], 'hspace': 0.08})

    sensors = [0, 9, 19]
    colors = ['#1565C0', '#2E7D32', '#D32F2F']
    labels = ['Bottom (0 cm)', 'Middle (50 cm)', 'Top (95 cm)']

    for idx, s in enumerate(sensors):
        ax1.plot(dates, data["CO2_main"][s], color=colors[idx], linewidth=0.4,
                 alpha=0.7, label=labels[idx])
    ax1.set_ylabel(r'CO$_2$ Concentration (%)')
    ax1.set_title(r'CO$_2$ Concentration vs Temperature — Selected Main Stack Sensors')
    ax1.legend(loc='upper right', framealpha=0.9, fontsize=9, edgecolor='#cccccc')
    ax1.grid(True, alpha=0.3, linestyle='--')

    for idx, s in enumerate(sensors):
        ax2.plot(dates, data["Temperature_main"][s], color=colors[idx], linewidth=0.4,
                 alpha=0.7, label=labels[idx])
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Temperature (°C)')
    ax2.legend(loc='upper right', framealpha=0.9, fontsize=9, edgecolor='#cccccc')
    ax2.grid(True, alpha=0.3, linestyle='--')
    setup_date_axis(ax2)

    save_figure(fig, '09_CO2_vs_Temperature')
    return fig


def plot_co2_heatmap(dates, data):
    print("  [10/10] CO2 Heatmap (this may take a moment)...")

    timestamps = np.array(data["Timestamp"])
    co2_matrix = np.array(data["CO2_main"])  # shape: (20, n_points)

    # Compute hourly bins
    start_time = timestamps[0]
    end_time = timestamps[-1]
    hour_seconds = 3600
    n_hours = int((end_time - start_time) / hour_seconds) + 1

    # Assign each data point to an hour bin
    bin_indices = ((timestamps - start_time) / hour_seconds).astype(int)
    bin_indices = np.clip(bin_indices, 0, n_hours - 1)

    # Compute hourly averages per sensor using fast bincount
    heatmap_data = np.full((20, n_hours), np.nan)
    for s in range(20):
        sums = np.bincount(bin_indices, weights=co2_matrix[s], minlength=n_hours)
        counts = np.bincount(bin_indices, minlength=n_hours)
        mask = counts > 0
        heatmap_data[s, mask] = sums[mask] / counts[mask]

    # Create date array for x-axis
    hour_dates = [datetime.utcfromtimestamp(start_time + h * hour_seconds) for h in range(n_hours)]
    hour_dates_num = mdates.date2num(hour_dates)

    # Build coordinate edges for pcolormesh
    # X edges: midpoints between hours, plus boundary edges
    x_edges = np.zeros(n_hours + 1)
    x_edges[0] = hour_dates_num[0] - 0.5 * (hour_dates_num[1] - hour_dates_num[0]) if n_hours > 1 else hour_dates_num[0] - 0.02
    x_edges[-1] = hour_dates_num[-1] + 0.5 * (hour_dates_num[-1] - hour_dates_num[-2]) if n_hours > 1 else hour_dates_num[-1] + 0.02
    for i in range(1, n_hours):
        x_edges[i] = (hour_dates_num[i - 1] + hour_dates_num[i]) / 2

    # Y edges: sensor height bin edges (sensors at 0, 5, ..., 95 cm)
    y_edges = np.array([-2.5] + [h + 2.5 for h in MAIN_HEIGHTS_CM])

    fig, ax = plt.subplots(figsize=FIGSIZE_HEATMAP)

    im = ax.pcolormesh(x_edges, y_edges, heatmap_data, cmap='inferno', shading='flat')

    ax.set_title(r'CO$_2$ Concentration — Vertical Profile Over Time (Hourly Averages)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sensor Height (cm)')
    ax.xaxis_date()
    setup_date_axis(ax)

    cbar = fig.colorbar(im, ax=ax, pad=0.02, aspect=30)
    cbar.set_label(r'CO$_2$ Concentration (%)', fontsize=12)

    save_figure(fig, '10_CO2_heatmap')
    return fig


if __name__ == '__main__':
    print("=" * 60)
    print("  CO2 Mofette Data — Publication-Quality Plots")
    print("=" * 60)

    # Load data (every 60th sample = ~1 per minute)
    print("\nLoading data...")
    data = get_data_by_minute('data/1_CO2_raw_data/data.csv')
    dates = timestamps_to_dates(data["Timestamp"])
    print(f"  Loaded {len(dates):,} data points")
    print(f"  Time range: {dates[0].strftime('%Y-%m-%d %H:%M')} to {dates[-1].strftime('%Y-%m-%d %H:%M')}")

    # Generate all figures
    print(f"\nGenerating 10 figures...\n")
    figures = []
    figures.append(plot_co2_main(dates, data))
    figures.append(plot_co2_side(dates, data))
    figures.append(plot_temp_main(dates, data))
    figures.append(plot_temp_side(dates, data))
    figures.append(plot_pressure(dates, data))
    figures.append(plot_humidity(dates, data))
    figures.append(plot_ambient_temp(dates, data))
    figures.append(plot_co2_vs_pressure(dates, data))
    figures.append(plot_co2_vs_temperature(dates, data))
    figures.append(plot_co2_heatmap(dates, data))

    print(f"\n{'=' * 60}")
    print(f"  All {len(figures)} figures saved to '{PLOT_DIR}/'")
    print(f"  Displaying interactive plots — close windows when done.")
    print(f"{'=' * 60}")

    plt.show()
