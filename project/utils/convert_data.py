import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.data_utils import convert_txt_to_csv

input_file = os.path.join('../data', '1_CO2_raw_data', 'new_device_column1.txt')
output_file = os.path.join('../data', '1_CO2_raw_data', 'data.csv')

if not os.path.exists(input_file):
    print(f"ERROR: Input file not found: {input_file}")
    sys.exit(1)

# Remove partial output from previous interrupted runs
if os.path.exists(output_file):
    print(f"Removing existing partial CSV: {output_file}")
    os.remove(output_file)

print(f"Converting: {input_file}")
print(f"Output:     {output_file}")
print("This may take several minutes for a 6GB file...")
print()

convert_txt_to_csv(input_file, output_file)

print()
print(f"Done! CSV saved to: {output_file}")
