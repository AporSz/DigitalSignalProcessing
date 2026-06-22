"""
dsp_analysis.py — Digital Signal Processing analysis of CO2 Mofette data

Implements:
  1. Power Spectral Density (Welch's method) — detects daily periodicity
  2. FFT Frequency Spectrum — direct frequency view with annotations
  3. Lowpass Filter — extracts long-term seasonal trends
  4. Bandpass Filter — isolates the 24h oscillation component
  5. Spectrogram — time-frequency evolution over 7 months
  6. Cross-correlation: CO2 vs Pressure
  7. Cross-correlation: CO2 vs Temperature

Usage:
    python dsp_analysis.py
"""

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import numpy as np
from datetime import datetime, timezone
from scipy.signal import welch, butter, sosfiltfilt, spectrogram
from scipy import signal
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_processing.loaders import get_data_by_minute

# ============================================================
# CONFIGURATION
# ============================================================
PLOT_DIR = 'plots'
DPI = 300
FIGSIZE = (16, 7)
FIGSIZE_TALL = (16, 10)

# Publication-quality style
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif', 'serif'],
    'font.size': 12,
    'axes.titlesize': 16,
    'axes.titleweight': 'bold',
    'axes.labelsize': 13,
    'legend.fontsize': 10,
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
})

# Sensor to use for single-sensor analyses (sensor 10, at 50cm height)
PRIMARY_SENSOR = 9  # 0-indexed


# ============================================================
# HELPER FUNCTIONS
# ============================================================
def timestamps_to_dates(timestamps):
    """Convert UTC epoch timestamps to datetime objects."""
    return [datetime.fromtimestamp(t, tz=timezone.utc) for t in timestamps]


def setup_date_axis(ax):
    """Configure x-axis with human-readable month labels and weekly grid."""
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=0))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')
    ax.grid(which='minor', axis='x', alpha=0.15, linestyle=':', color='#666666')


def save_figure(fig, name):
    """Save figure as high-resolution PNG."""
    os.makedirs(PLOT_DIR, exist_ok=True)
    path = os.path.join(PLOT_DIR, f'{name}.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    print(f'  Saved: {path}')


def prepare_uniform_signal(timestamps, values):
    """
    Interpolate signal onto a uniform time grid.
    Required for FFT/filtering since the raw data may have gaps.
    Returns: (uniform_timestamps, uniform_values, sampling_interval_minutes)
    """
    t = np.array(timestamps)
    v = np.array(values, dtype=float)

    # Remove NaN/inf values
    valid = np.isfinite(v)
    t = t[valid]
    v = v[valid]

    # Create uniform grid with 1-minute spacing
    dt_minutes = 1.0  # 1 minute sampling interval
    dt_seconds = dt_minutes * 60
    t_uniform = np.arange(t[0], t[-1], dt_seconds)

    # Interpolate onto uniform grid
    v_uniform = np.interp(t_uniform, t, v)

    return t_uniform, v_uniform, dt_minutes


# ============================================================
# 1. POWER SPECTRAL DENSITY (Welch's Method)
# ============================================================
def plot_psd(data):
    """
    Power Spectral Density using Welch's method.
    Reveals periodic components — especially the 24h cycle.
    """
    print("  [1/7] Power Spectral Density (Welch)...")

    t_uniform, co2, dt_min = prepare_uniform_signal(
        data["Timestamp"], data["CO2_main"][PRIMARY_SENSOR]
    )

    # Sampling frequency in samples/minute
    fs = 1.0 / dt_min  # 1 sample/minute

    # Welch's PSD — use a segment length of ~7 days for good low-freq resolution
    # 7 days = 7 * 24 * 60 = 10080 minutes
    nperseg = min(10080, len(co2) // 4)

    freqs, psd = welch(co2, fs=fs, nperseg=nperseg, noverlap=nperseg // 2)

    # Convert frequency to period in hours for intuitive x-axis
    # freq is in cycles/minute, period = 1/freq in minutes, /60 = hours
    valid = freqs > 0
    freqs = freqs[valid]
    psd = psd[valid]
    period_hours = 1.0 / (freqs * 60)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.loglog(period_hours, psd, color='#1565C0', linewidth=0.8, alpha=0.9)

    # Mark the 24h peak
    idx_24h = np.argmin(np.abs(period_hours - 24))
    ax.axvline(x=24, color='#D32F2F', linestyle='--', alpha=0.8, linewidth=1.5, label='24h period')
    ax.plot(period_hours[idx_24h], psd[idx_24h], 'o', color='#D32F2F', markersize=10, zorder=5)
    ax.annotate(f'24h peak\n({psd[idx_24h]:.1f})',
                xy=(period_hours[idx_24h], psd[idx_24h]),
                xytext=(period_hours[idx_24h] * 2.5, psd[idx_24h] * 3),
                fontsize=11, fontweight='bold', color='#D32F2F',
                arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=1.5))

    # Mark 12h harmonic if visible
    idx_12h = np.argmin(np.abs(period_hours - 12))
    ax.axvline(x=12, color='#FF9800', linestyle=':', alpha=0.6, linewidth=1.2, label='12h harmonic')

    ax.set_title(r'Power Spectral Density — CO$_2$ (Sensor 10, 50 cm height)')
    ax.set_xlabel('Period (hours)')
    ax.set_ylabel(r'PSD ((%$^2$)/Hz)')
    ax.legend(loc='upper right', framealpha=0.9, edgecolor='#cccccc')
    ax.set_xlim(1, period_hours.max())

    # Invert x-axis so shorter periods are on the right (high frequency)
    ax.invert_xaxis()

    save_figure(fig, 'dsp_01_PSD_welch')
    return fig


# ============================================================
# 2. FFT FREQUENCY SPECTRUM
# ============================================================
def plot_fft(data):
    """
    Direct FFT magnitude spectrum.
    Shows dominant frequencies with key peaks annotated.
    """
    print("  [2/7] FFT Frequency Spectrum...")

    t_uniform, co2, dt_min = prepare_uniform_signal(
        data["Timestamp"], data["CO2_main"][PRIMARY_SENSOR]
    )

    # Remove mean (detrend) before FFT
    co2_detrended = co2 - np.mean(co2)

    # Compute FFT
    N = len(co2_detrended)
    fft_vals = np.fft.rfft(co2_detrended)
    fft_magnitude = 2.0 / N * np.abs(fft_vals)
    freqs = np.fft.rfftfreq(N, d=dt_min)  # in cycles/minute

    # Convert to cycles/hour for readability
    freqs_per_hour = freqs * 60  # cycles/hour

    fig, ax = plt.subplots(figsize=FIGSIZE)

    ax.plot(freqs_per_hour[1:], fft_magnitude[1:], color='#1565C0', linewidth=0.5, alpha=0.8)

    # Annotate key frequencies
    # 24h cycle: f = 1/24 cycles/hour
    f_24h = 1.0 / 24.0
    idx_24h = np.argmin(np.abs(freqs_per_hour - f_24h))
    ax.axvline(x=f_24h, color='#D32F2F', linestyle='--', alpha=0.8, linewidth=1.5)
    ax.annotate(f'24h cycle\nf = 1/24 h⁻¹',
                xy=(f_24h, fft_magnitude[idx_24h]),
                xytext=(f_24h + 0.01, fft_magnitude[idx_24h] * 0.8),
                fontsize=11, fontweight='bold', color='#D32F2F',
                arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=1.5))

    # 12h harmonic
    f_12h = 1.0 / 12.0
    ax.axvline(x=f_12h, color='#FF9800', linestyle=':', alpha=0.6, linewidth=1.2)
    ax.annotate('12h harmonic', xy=(f_12h, fft_magnitude[np.argmin(np.abs(freqs_per_hour - f_12h))]),
                xytext=(f_12h + 0.01, fft_magnitude[np.argmin(np.abs(freqs_per_hour - f_12h))] * 1.5),
                fontsize=10, color='#FF9800',
                arrowprops=dict(arrowstyle='->', color='#FF9800', lw=1))

    ax.set_title(r'FFT Magnitude Spectrum — CO$_2$ (Sensor 10, 50 cm height)')
    ax.set_xlabel('Frequency (cycles/hour)')
    ax.set_ylabel('Magnitude (%)')
    ax.set_xlim(0, 0.2)  # Focus on low frequencies (up to ~5h period)

    save_figure(fig, 'dsp_02_FFT_spectrum')
    return fig


# ============================================================
# 3. LOWPASS FILTER — SEASONAL TREND
# ============================================================
def plot_lowpass_trend(data):
    """
    Lowpass filter to extract long-term (seasonal) trends.
    Removes daily oscillations, keeping only multi-day changes.
    """
    print("  [3/7] Lowpass Filter — Seasonal Trend...")

    t_uniform, co2, dt_min = prepare_uniform_signal(
        data["Timestamp"], data["CO2_main"][PRIMARY_SENSOR]
    )
    dates = timestamps_to_dates(t_uniform)

    # Design lowpass Butterworth filter
    # Cutoff: 1/(3 days) — removes everything faster than 3 days
    fs = 1.0 / dt_min  # samples/minute
    cutoff_period_minutes = 3 * 24 * 60  # 3 days in minutes
    cutoff_freq = 1.0 / cutoff_period_minutes  # cycles/minute
    nyquist = fs / 2.0
    Wn = cutoff_freq / nyquist  # normalized frequency

    # Use second-order sections for numerical stability
    sos = butter(N=3, Wn=Wn, btype='low', output='sos')
    co2_trend = sosfiltfilt(sos, co2)

    fig, ax = plt.subplots(figsize=FIGSIZE)

    ax.plot(dates, co2, color='#90CAF9', linewidth=0.3, alpha=0.5, label='Raw data (1-min sampling)')
    ax.plot(dates, co2_trend, color='#D32F2F', linewidth=2.0, alpha=0.9,
            label=f'Lowpass trend (cutoff = 3 days)')

    ax.set_title(r'Lowpass Filter — CO$_2$ Seasonal Trend (Sensor 10, 50 cm)')
    ax.set_xlabel('Date')
    ax.set_ylabel(r'CO$_2$ Concentration (%)')
    ax.legend(loc='upper right', framealpha=0.9, edgecolor='#cccccc')
    setup_date_axis(ax)

    save_figure(fig, 'dsp_03_lowpass_trend')
    return fig


# ============================================================
# 4. BANDPASS FILTER — DAILY CYCLE ISOLATION
# ============================================================
def plot_bandpass_daily(data):
    """
    Bandpass filter isolating the ~24h oscillation component.
    Shows the pure diurnal CO2 'breathing' of the mofette.
    """
    print("  [4/7] Bandpass Filter — Daily Cycle...")

    t_uniform, co2, dt_min = prepare_uniform_signal(
        data["Timestamp"], data["CO2_main"][PRIMARY_SENSOR]
    )
    dates = timestamps_to_dates(t_uniform)

    # Design bandpass Butterworth filter around 24h period
    # Passband: 18h to 30h periods
    fs = 1.0 / dt_min
    nyquist = fs / 2.0
    low_period = 30 * 60  # 30 hours in minutes
    high_period = 18 * 60  # 18 hours in minutes
    low_freq = 1.0 / low_period  # cycles/min
    high_freq = 1.0 / high_period  # cycles/min
    Wn = [low_freq / nyquist, high_freq / nyquist]

    sos = butter(N=3, Wn=Wn, btype='band', output='sos')
    co2_daily = sosfiltfilt(sos, co2)

    # Show full range + a 2-week zoomed view
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=FIGSIZE_TALL,
                                    gridspec_kw={'height_ratios': [1, 1.2], 'hspace': 0.3})

    # Full range
    ax1.plot(dates, co2_daily, color='#2E7D32', linewidth=0.5, alpha=0.8)
    ax1.set_title(r'Bandpass Filter — Isolated 24h CO$_2$ Oscillation (Sensor 10, 50 cm)')
    ax1.set_ylabel(r'CO$_2$ Deviation (%)')
    setup_date_axis(ax1)

    # Zoomed: 2-week window in the middle of the dataset
    mid = len(dates) // 2
    two_weeks = 14 * 24 * 60  # 14 days in minutes
    start_idx = max(0, mid - two_weeks // 2)
    end_idx = min(len(dates), mid + two_weeks // 2)

    ax2.plot(dates[start_idx:end_idx], co2_daily[start_idx:end_idx],
             color='#2E7D32', linewidth=1.2, alpha=0.9)
    ax2.plot(dates[start_idx:end_idx], co2[start_idx:end_idx] - np.mean(co2),
             color='#90CAF9', linewidth=0.3, alpha=0.4, label='Raw (detrended)')
    ax2.plot(dates[start_idx:end_idx], co2_daily[start_idx:end_idx],
             color='#2E7D32', linewidth=1.2, alpha=0.9, label='24h bandpass')
    ax2.set_title('Zoomed: 2-week window')
    ax2.set_xlabel('Date')
    ax2.set_ylabel(r'CO$_2$ Deviation (%)')
    ax2.legend(loc='upper right', framealpha=0.9, edgecolor='#cccccc')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax2.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    ax2.xaxis.set_minor_locator(mdates.DayLocator())
    ax2.grid(which='minor', axis='x', alpha=0.15, linestyle=':', color='#666666')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=30, ha='right')

    save_figure(fig, 'dsp_04_bandpass_daily')
    return fig


# ============================================================
# 5. SPECTROGRAM — TIME-FREQUENCY EVOLUTION
# ============================================================
def plot_spectrogram(data):
    """
    Spectrogram showing how frequency content changes over months.
    Reveals if daily cycles are stronger in certain seasons.
    """
    print("  [5/7] Spectrogram...")

    t_uniform, co2, dt_min = prepare_uniform_signal(
        data["Timestamp"], data["CO2_main"][PRIMARY_SENSOR]
    )

    fs = 1.0 / dt_min  # samples/minute

    # Segment length: 7 days for good frequency resolution
    nperseg = 7 * 24 * 60  # 7 days in minutes
    noverlap = nperseg - 24 * 60  # slide by 1 day

    f, t_spec, Sxx = spectrogram(co2, fs=fs, nperseg=nperseg,
                                  noverlap=noverlap, scaling='density')

    # Convert frequency to period in hours
    # f is in cycles/minute
    period_hours = np.zeros_like(f)
    period_hours[1:] = 1.0 / (f[1:] * 60)  # convert to hours
    period_hours[0] = np.inf

    # Convert spectrogram time to dates
    spec_dates = [datetime.fromtimestamp(t_uniform[0] + t_s * 60, tz=timezone.utc) for t_s in t_spec]
    spec_dates_num = mdates.date2num(spec_dates)

    # Focus on periods from 6h to 72h (3 days)
    mask = (period_hours >= 6) & (period_hours <= 72)

    fig, ax = plt.subplots(figsize=(18, 7))

    im = ax.pcolormesh(spec_dates_num, period_hours[mask], 10 * np.log10(Sxx[mask, :]),
                        cmap='magma', shading='auto')
    ax.set_yscale('log')
    ax.set_yticks([6, 8, 12, 24, 48, 72])
    ax.set_yticklabels(['6h', '8h', '12h', '24h', '48h', '72h'])

    # Mark 24h line
    ax.axhline(y=24, color='white', linestyle='--', alpha=0.7, linewidth=1.5, label='24h period')

    ax.set_title(r'Spectrogram — CO$_2$ Frequency Content Over Time (Sensor 10, 50 cm)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Period (hours)')
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')
    ax.legend(loc='upper right', framealpha=0.9)

    cbar = fig.colorbar(im, ax=ax, pad=0.02, aspect=30)
    cbar.set_label('Power (dB)', fontsize=12)

    save_figure(fig, 'dsp_05_spectrogram')
    return fig


# ============================================================
# 6. CROSS-CORRELATION: CO2 vs PRESSURE
# ============================================================
def plot_xcorr_pressure(data):
    """
    Cross-correlation between CO2 and barometric pressure.
    Shows if pressure changes drive CO2 emissions and at what time lag.
    """
    print("  [6/7] Cross-correlation: CO2 vs Pressure...")

    t_uniform, co2, dt_min = prepare_uniform_signal(
        data["Timestamp"], data["CO2_main"][PRIMARY_SENSOR]
    )
    _, pressure, _ = prepare_uniform_signal(
        data["Timestamp"], data["Pressure_Top"]
    )

    # Make sure both signals have the same length
    min_len = min(len(co2), len(pressure))
    co2 = co2[:min_len]
    pressure = pressure[:min_len]

    # Normalize (zero mean, unit variance)
    co2_norm = (co2 - np.mean(co2)) / np.std(co2)
    pressure_norm = (pressure - np.mean(pressure)) / np.std(pressure)

    # Cross-correlation using correlate
    # Only compute for lags up to ±3 days (±4320 minutes)
    max_lag = 3 * 24 * 60  # 3 days in minutes
    correlation = signal.correlate(co2_norm, pressure_norm, mode='full')
    correlation /= len(co2_norm)  # normalize

    # Lag axis in hours
    lags = np.arange(-len(pressure_norm) + 1, len(co2_norm))
    lag_hours = lags * dt_min / 60.0

    # Trim to ±3 days
    mask = np.abs(lag_hours) <= 72
    lag_hours = lag_hours[mask]
    correlation = correlation[mask]

    fig, ax = plt.subplots(figsize=FIGSIZE)

    ax.plot(lag_hours, correlation, color='#1565C0', linewidth=1.0, alpha=0.9)
    ax.axhline(y=0, color='#999999', linestyle='-', linewidth=0.5)
    ax.axvline(x=0, color='#999999', linestyle=':', linewidth=0.8, alpha=0.5)

    # Mark the peak
    peak_idx = np.argmax(np.abs(correlation))
    peak_lag = lag_hours[peak_idx]
    peak_val = correlation[peak_idx]
    ax.plot(peak_lag, peak_val, 'o', color='#D32F2F', markersize=10, zorder=5)
    ax.annotate(f'Peak at lag = {peak_lag:.1f}h\nr = {peak_val:.3f}',
                xy=(peak_lag, peak_val),
                xytext=(peak_lag + 8, peak_val * 0.85),
                fontsize=11, fontweight='bold', color='#D32F2F',
                arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=1.5))

    ax.set_title(r'Cross-Correlation: CO$_2$ vs Barometric Pressure')
    ax.set_xlabel('Lag (hours) — positive = pressure leads')
    ax.set_ylabel('Normalized Cross-Correlation')

    save_figure(fig, 'dsp_06_xcorr_pressure')
    return fig


# ============================================================
# 7. CROSS-CORRELATION: CO2 vs TEMPERATURE
# ============================================================
def plot_xcorr_temperature(data):
    """
    Cross-correlation between CO2 and ambient temperature.
    Shows if temperature changes correlate with CO2 emissions.
    """
    print("  [7/7] Cross-correlation: CO2 vs Temperature...")

    t_uniform, co2, dt_min = prepare_uniform_signal(
        data["Timestamp"], data["CO2_main"][PRIMARY_SENSOR]
    )
    _, temp, _ = prepare_uniform_signal(
        data["Timestamp"], data["Temperature_Top"]
    )

    min_len = min(len(co2), len(temp))
    co2 = co2[:min_len]
    temp = temp[:min_len]

    # Normalize
    co2_norm = (co2 - np.mean(co2)) / np.std(co2)
    temp_norm = (temp - np.mean(temp)) / np.std(temp)

    # Cross-correlation
    max_lag = 3 * 24 * 60
    correlation = signal.correlate(co2_norm, temp_norm, mode='full')
    correlation /= len(co2_norm)

    lags = np.arange(-len(temp_norm) + 1, len(co2_norm))
    lag_hours = lags * dt_min / 60.0

    mask = np.abs(lag_hours) <= 72
    lag_hours = lag_hours[mask]
    correlation = correlation[mask]

    fig, ax = plt.subplots(figsize=FIGSIZE)

    ax.plot(lag_hours, correlation, color='#2E7D32', linewidth=1.0, alpha=0.9)
    ax.axhline(y=0, color='#999999', linestyle='-', linewidth=0.5)
    ax.axvline(x=0, color='#999999', linestyle=':', linewidth=0.8, alpha=0.5)

    # Mark the peak
    peak_idx = np.argmax(np.abs(correlation))
    peak_lag = lag_hours[peak_idx]
    peak_val = correlation[peak_idx]
    ax.plot(peak_lag, peak_val, 'o', color='#D32F2F', markersize=10, zorder=5)
    ax.annotate(f'Peak at lag = {peak_lag:.1f}h\nr = {peak_val:.3f}',
                xy=(peak_lag, peak_val),
                xytext=(peak_lag + 8, peak_val * 0.85),
                fontsize=11, fontweight='bold', color='#D32F2F',
                arrowprops=dict(arrowstyle='->', color='#D32F2F', lw=1.5))

    ax.set_title(r'Cross-Correlation: CO$_2$ vs Ambient Temperature')
    ax.set_xlabel('Lag (hours) — positive = temperature leads')
    ax.set_ylabel('Normalized Cross-Correlation')

    save_figure(fig, 'dsp_07_xcorr_temperature')
    return fig


# ============================================================
# MAIN ENTRY POINT
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("  CO2 Mofette — DSP Analysis")
    print("=" * 60)

    print("\nLoading data...")
    data = get_data_by_minute('data/1_CO2_raw_data/data.csv')
    dates = timestamps_to_dates(data["Timestamp"])
    print(f"  Loaded {len(dates):,} data points")
    print(f"  Time range: {dates[0].strftime('%Y-%m-%d')} to {dates[-1].strftime('%Y-%m-%d')}")

    print(f"\nRunning 7 DSP analyses...\n")
    figures = []
    figures.append(plot_psd(data))
    figures.append(plot_fft(data))
    figures.append(plot_lowpass_trend(data))
    figures.append(plot_bandpass_daily(data))
    figures.append(plot_spectrogram(data))
    figures.append(plot_xcorr_pressure(data))
    figures.append(plot_xcorr_temperature(data))

    print(f"\n{'=' * 60}")
    print(f"  All {len(figures)} figures saved to '{PLOT_DIR}/'")
    print(f"  Displaying interactive plots — close windows when done.")
    print(f"{'=' * 60}")

    plt.show()
