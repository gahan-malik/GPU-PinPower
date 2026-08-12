import random
import time
import os
import csv
from datetime import datetime

filename = "power_log.csv"

if not os.path.exists(filename):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Time",
            "Pin 1 Power (W)",
            "Pin 2 Power (W)",
            "Pin 3 Power (W)",
            "Total Power (W)"
        ])

while True:
    pins = {
        "Pin 1": {"voltage": 12.04, "current": random.uniform(3.0, 3.6)},
        "Pin 2": {"voltage": 12.03, "current": random.uniform(3.0, 3.6)},
        "Pin 3": {"voltage": 12.05, "current": random.uniform(3.0, 3.6)}
    }

    powers = []

    for data in pins.values():
        powers.append(data["voltage"] * data["current"])

    total_power = sum(powers)

    now = datetime.now().strftime("%H:%M:%S")

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            now,
            f"{powers[0]:.2f}",
            f"{powers[1]:.2f}",
            f"{powers[2]:.2f}",
            f"{total_power:.2f}"
        ])

    os.system("cls")

    print("GPU-PinPower")
    print("================================")
    print(f"Pin 1   {powers[0]:.2f} W")
    print(f"Pin 2   {powers[1]:.2f} W")
    print(f"Pin 3   {powers[2]:.2f} W")
    print("================================")
    print(f"TOTAL   {total_power:.2f} W")
    print("\nLogging data to power_log.csv...")
    
    time.sleep(1)