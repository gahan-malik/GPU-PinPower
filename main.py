import time
import os
import csv
from datetime import datetime

# Starting estimated GPU power
total_gpu_power = 30.0

# How quickly the simulated GPU load changes
power_change = 5.0

# Estimated share of power for each pin
# These are simulation values, NOT real measurements.
pin_share = {
    "Pin 1": 0.33,
    "Pin 2": 0.34,
    "Pin 3": 0.33
}

filename = "power_log.csv"

# Create CSV header if the file doesn't exist
if not os.path.exists(filename):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Time",
            "Pin 1 Estimated Power (W)",
            "Pin 2 Estimated Power (W)",
            "Pin 3 Estimated Power (W)",
            "Estimated Total Power (W)"
        ])

while True:

    # Simulate GPU load increasing and decreasing
    total_gpu_power += power_change

    if total_gpu_power >= 130:
        power_change = -5.0

    if total_gpu_power <= 30:
        power_change = 5.0

    # Calculate estimated power for each pin
    powers = {}

    for pin, share in pin_share.items():
        powers[pin] = total_gpu_power * share

    estimated_total = sum(powers.values())

    # Clear terminal
    os.system("cls")

    # Display monitor
    print("GPU-PinPower")
    print("================================")
    print("MODE: ESTIMATED")
    print(f"GPU LOAD POWER: ~{total_gpu_power:.2f} W")
    print("================================")

    for pin, power in powers.items():
        print(f"{pin}   ~{power:.2f} W")

    print("================================")
    print(f"TOTAL   ~{estimated_total:.2f} W")
    print()
    print("STATUS: NORMAL")
    print("Updating every second...")

    # Save reading to CSV
    now = datetime.now().strftime("%H:%M:%S")

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            now,
            f"{powers['Pin 1']:.2f}",
            f"{powers['Pin 2']:.2f}",
            f"{powers['Pin 3']:.2f}",
            f"{estimated_total:.2f}"
        ])

    time.sleep(1)