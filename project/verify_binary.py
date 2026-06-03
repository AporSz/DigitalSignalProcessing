"""
Verify CO2 binary datasets (custom .bin from convert_csv_to_bin, or cleaned .npy).

Usage (from repo root):
  python -m project.verify_binary --bin project/data/1_CO2_raw_data/data.bin
  python -m project.verify_binary --bin project/data/1_CO2_raw_data/data.bin --csv project/data/1_CO2_raw_data/data.csv
  python -m project.verify_binary --npy project/data/2_CO2_cleand_data/new_device_all_data_filterd.npy
  python -m project.verify_binary --self-test
"""

import argparse
import csv
import sys
import tempfile
from pathlib import Path

from project.utils.data_utils import (
    RECORD_SIZE_BYTES,
    convert_csv_to_bin,
    verify_bin_file,
    verify_npy_file,
)


def _print_report(label, report):
    print(f"\n=== {label} ===")
    for key, value in report.items():
        if key in ("issues", "warnings"):
            continue
        print(f"  {key}: {value}")
    if report.get("warnings"):
        print("  warnings:")
        for warning in report["warnings"]:
            print(f"    - {warning}")
    if report.get("issues"):
        print("  issues:")
        for issue in report["issues"]:
            print(f"    - {issue}")
    status = "VALID" if report.get("valid") else "INVALID"
    print(f"  result: {status}")


def run_self_test():
    """Round-trip: small CSV -> .bin -> verify (and optional CSV cross-check)."""
    rows = [
        {
            "Timestamp": "1649455396.5622404",
            "Pressure_Top": "93512.25",
            "Humidity_Top": "65.00",
            "Temperature_Top": "9.34",
            "Pressure_Bottom": "93925.87",
            "Humidity_Bottom": "89.00",
            "Temperature_Bottom": "8.37",
            **{f"CO2_main{i}": str(70.0 - i) for i in range(1, 21)},
            **{f"Temperature_main{i}": str(8.0 + i * 0.01) for i in range(1, 21)},
            **{f"CO2_side{i}": str(50.0 + i) for i in range(1, 5)},
            **{f"Temperature_side{i}": str(8.5 + i * 0.1) for i in range(1, 5)},
        },
        {
            "Timestamp": "1649455397.5622404",
            "Pressure_Top": "93510.00",
            "Humidity_Top": "64.00",
            "Temperature_Top": "9.30",
            "Pressure_Bottom": "93920.00",
            "Humidity_Bottom": "88.00",
            "Temperature_Bottom": "8.35",
            **{f"CO2_main{i}": str(71.0 - i) for i in range(1, 21)},
            **{f"Temperature_main{i}": str(8.1 + i * 0.01) for i in range(1, 21)},
            **{f"CO2_side{i}": str(51.0 + i) for i in range(1, 5)},
            **{f"Temperature_side{i}": str(8.6 + i * 0.1) for i in range(1, 5)},
        },
    ]
    fieldnames = list(rows[0].keys())

    with tempfile.TemporaryDirectory() as tmp:
        csv_path = Path(tmp) / "sample.csv"
        bin_path = Path(tmp) / "sample.bin"

        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        convert_csv_to_bin(csv_path, bin_path)
        size = bin_path.stat().st_size
        expected = len(rows) * RECORD_SIZE_BYTES
        if size != expected:
            print(f"Self-test failed: bin size {size} != expected {expected}")
            return False

        report = verify_bin_file(bin_path, path_csv=csv_path)
        _print_report("self-test .bin", report)
        return report["valid"]


def main():
    parser = argparse.ArgumentParser(description="Verify CO2 binary data files")
    parser.add_argument("--bin", type=Path, help="Path to .bin file (from convert_csv_to_bin)")
    parser.add_argument("--csv", type=Path, help="Optional CSV to cross-check against --bin")
    parser.add_argument("--npy", type=Path, help="Path to cleaned .npy file")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if CO2/humidity are outside 0–100 %% (use for cleaned data)",
    )
    parser.add_argument("--self-test", action="store_true", help="Run built-in round-trip test")
    args = parser.parse_args()

    if args.self_test:
        ok = run_self_test()
        sys.exit(0 if ok else 1)

    if not args.bin and not args.npy:
        parser.print_help()
        print("\nProvide --bin and/or --npy, or use --self-test.")
        sys.exit(1)

    exit_code = 0

    if args.bin:
        if not args.bin.is_file():
            print(f"Error: bin file not found: {args.bin}")
            sys.exit(1)
        report = verify_bin_file(args.bin, path_csv=args.csv, strict_ranges=args.strict)
        _print_report(str(args.bin), report)
        if not report["valid"]:
            exit_code = 1

    if args.npy:
        if not args.npy.is_file():
            print(f"Error: npy file not found: {args.npy}")
            sys.exit(1)
        report = verify_npy_file(args.npy)
        _print_report(str(args.npy), report)
        if not report["valid"]:
            exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
