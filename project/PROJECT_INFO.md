# CO₂ Mofette Measurement — Project Info

## Location
- **Site**: Mofette (natural CO₂ emission vent)
- **Location**: Covasna, Romania
- **Coordinates**: Covasna county, Eastern Carpathians

## Measurement Period
- **Start**: 2022-04-08, 22:03:16 UTC
- **End**: 2022-11-07, 10:53:54 UTC
- **Duration**: ~7 months (213 days)
- **Season coverage**: Spring → Autumn

## Research
- **Article**: "CO2 Dynamics in a Mofette: Measurement and Modeling"
- **Authors**: Attila Gergely, Alexandru Szakács, Ágnes Gál, Zoltán Neda

## Sensor Setup
| Sensor Group         | Count | Type   | Spacing      | Orientation     |
|----------------------|-------|--------|--------------|-----------------|
| CO₂ + Temp (main)    | 20    | STC31  | 5 cm apart   | Bottom → Top    |
| CO₂ + Temp (side)    | 4     | STC31  | 10 cm apart  | Top → Bottom    |
| Pressure (top/bottom)| 2     | BMP280 | —            | Top & Bottom    |
| Humidity (top/bottom)| 2     | DHT11  | —            | Top & Bottom    |
| Temp ambient (top/bottom)| 2 | BMP280 | —            | Top & Bottom    |

## Data Summary
- **Total measurements**: ~17.3 million
- **Invalid entries**: ~75,966 (0.4%)
- **Sampling rate**: ~1 sample/second
- **Raw file**: `new_device_column1.txt` (~6 GB)
- **Converted CSV**: `data.csv` (with header row)
