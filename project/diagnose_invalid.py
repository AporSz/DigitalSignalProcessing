import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

path_txt = os.path.join('data', '1_CO2_raw_data', 'new_device_column1.txt')

# Categories of invalid entries
categories = {
    "empty_or_short_line": 0,        # First line (timestamp) is empty or unparseable
    "timestamp_not_float": 0,        # Can't parse timestamp as float
    "data_line_too_short": 0,        # Second line has <= 2 values after stripping
    "not_enough_sensor_values": 0,   # IndexError - fewer than 54 values expected
    "value_not_float": 0,            # A sensor value can't be parsed as float
    "other": 0,
}

# Store samples of each category (up to 5 examples each)
samples = {k: [] for k in categories}
MAX_SAMPLES = 5

total = 0
invalid = 0

with open(path_txt) as f:
    while True:
        try:
            line1 = f.readline()
            if line1 == "":
                break  # EOF

            total += 1

            # Try parsing timestamp
            l1 = line1.strip().split()
            if len(l1) == 0:
                categories["empty_or_short_line"] += 1
                invalid += 1
                if len(samples["empty_or_short_line"]) < MAX_SAMPLES:
                    samples["empty_or_short_line"].append(f"Line pair #{total}: timestamp line = {repr(line1[:200])}")
                # Still need to read the second line to stay in sync
                f.readline()
                continue

            try:
                t = float(l1[0])
            except ValueError:
                categories["timestamp_not_float"] += 1
                invalid += 1
                if len(samples["timestamp_not_float"]) < MAX_SAMPLES:
                    samples["timestamp_not_float"].append(f"Line pair #{total}: {repr(line1[:200])}")
                f.readline()
                continue

            # Read data line
            line2 = f.readline()
            if line2 == "":
                categories["empty_or_short_line"] += 1
                invalid += 1
                break

            l2 = line2.strip()[2:].split()

            if len(l2) <= 2:
                categories["data_line_too_short"] += 1
                invalid += 1
                if len(samples["data_line_too_short"]) < MAX_SAMPLES:
                    samples["data_line_too_short"].append(
                        f"Line pair #{total}: timestamp={t}, data line ({len(l2)} values) = {repr(line2[:300])}"
                    )
                continue

            # Check if we have enough values (need 6 + 40 + 8 = 54)
            expected_values = 54
            if len(l2) < expected_values:
                categories["not_enough_sensor_values"] += 1
                invalid += 1
                if len(samples["not_enough_sensor_values"]) < MAX_SAMPLES:
                    samples["not_enough_sensor_values"].append(
                        f"Line pair #{total}: timestamp={t}, got {len(l2)} values (expected {expected_values}), data = {repr(line2[:300])}"
                    )
                continue

            # Try parsing all values as float
            try:
                for i in range(len(l2)):
                    float(l2[i])
            except ValueError as e:
                categories["value_not_float"] += 1
                invalid += 1
                if len(samples["value_not_float"]) < MAX_SAMPLES:
                    bad_val = l2[i] if i < len(l2) else "?"
                    samples["value_not_float"].append(
                        f"Line pair #{total}: timestamp={t}, bad value at index {i} = {repr(bad_val)}, context = ...{' '.join(l2[max(0,i-2):i+3])}..."
                    )
                continue

        except Exception as e:
            categories["other"] += 1
            invalid += 1
            if len(samples["other"]) < MAX_SAMPLES:
                samples["other"].append(f"Line pair #{total}: {type(e).__name__}: {e}")

        if total % 1000000 == 0:
            print(f"Scanned {total / 1000000:.0f}M entries...")

print(f"\n{'='*60}")
print(f"RESULTS: {invalid} invalid out of {total} total ({100*invalid/total:.2f}%)")
print(f"{'='*60}\n")

for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
    if count > 0:
        pct = 100 * count / total
        print(f"  {cat}: {count:,} ({pct:.2f}%)")
        for s in samples[cat]:
            print(f"    -> {s}")
        print()
