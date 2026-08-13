import platform
import subprocess
import random
import time
import csv
from datetime import datetime


# ==========================================
# GPU-PinPower v1.1.0
# GPU power estimation database
# ==========================================

GPU_DATABASE = {
    "RTX 5050": {
        "vendor": "NVIDIA",
        "power": 130
    },
    "RTX 4060": {
        "vendor": "NVIDIA",
        "power": 115
    },
    "RTX 3060": {
        "vendor": "NVIDIA",
        "power": 170
    },
    "GTX 1650": {
        "vendor": "NVIDIA",
        "power": 75
    }
}


# ==========================================
# GPU Detection
# ==========================================

def detect_gpu():
    system = platform.system()

    try:

        # Windows
        if system == "Windows":

            command = [
                "powershell",
                "-Command",
                "Get-CimInstance Win32_VideoController | "
                "Select-Object -ExpandProperty Name"
            ]

            result = subprocess.check_output(
                command,
                text=True,
                stderr=subprocess.DEVNULL
            )

            return [
                gpu.strip()
                for gpu in result.splitlines()
                if gpu.strip()
            ]

        # Linux
        elif system == "Linux":

            command = [
                "sh",
                "-c",
                "lspci | grep -Ei 'VGA|3D|Display'"
            ]

            result = subprocess.check_output(
                command,
                text=True,
                stderr=subprocess.DEVNULL
            )

            return [
                gpu.strip()
                for gpu in result.splitlines()
                if gpu.strip()
            ]

        # macOS
        elif system == "Darwin":

            command = [
                "system_profiler",
                "SPDisplaysDataType"
            ]

            result = subprocess.check_output(
                command,
                text=True,
                stderr=subprocess.DEVNULL
            )

            gpus = []

            for line in result.splitlines():

                if "Chipset Model:" in line:

                    gpus.append(
                        line.split(":", 1)[1].strip()
                    )

            return gpus

        return []

    except Exception:
        return []


# ==========================================
# GPU Information
# ==========================================

def get_gpu_info(gpu_name):

    for model, info in GPU_DATABASE.items():

        if model.lower() in gpu_name.lower():

            return {
                "model": model,
                "vendor": info["vendor"],
                "power": info["power"]
            }

    return {
        "model": gpu_name,
        "vendor": "Unknown",
        "power": None
    }


# ==========================================
# Simulated Pin Power
# ==========================================

def simulate_pin_power(total_power):

    variation = [
        random.uniform(0.95, 1.05),
        random.uniform(0.95, 1.05),
        random.uniform(0.95, 1.05)
    ]

    total_variation = sum(variation)

    return [
        total_power * value / total_variation
        for value in variation
    ]


# ==========================================
# Status
# ==========================================

def get_status(pins):

    average = sum(pins) / len(pins)

    difference = max(
        abs(pin - average)
        for pin in pins
    )

    percentage = (difference / average) * 100

    if percentage < 5:
        return "NORMAL"

    elif percentage < 10:
        return "SLIGHT IMBALANCE"

    else:
        return "HIGH IMBALANCE"


# ==========================================
# CSV Logging
# ==========================================

CSV_FILE = "gpu_pinpower_log.csv"


def setup_csv():

    file = open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8"
    )

    writer = csv.writer(file)

    # Add header only when the file is empty
    if file.tell() == 0:

        writer.writerow([
            "Timestamp",
            "GPU",
            "Vendor",
            "Mode",
            "Pin 1 Power (W)",
            "Pin 2 Power (W)",
            "Pin 3 Power (W)",
            "Total Power (W)",
            "Voltage (V)",
            "Pin 1 Current (A)",
            "Pin 2 Current (A)",
            "Pin 3 Current (A)",
            "Total Current (A)",
            "Status"
        ])

        file.flush()

    return file, writer


def log_data(
    writer,
    file,
    gpu,
    vendor,
    pins,
    voltage,
    currents,
    total_current,
    status
):

    writer.writerow([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        gpu,
        vendor,
        "ESTIMATED",
        f"{pins[0]:.2f}",
        f"{pins[1]:.2f}",
        f"{pins[2]:.2f}",
        f"{sum(pins):.2f}",
        f"{voltage:.2f}",
        f"{currents[0]:.2f}",
        f"{currents[1]:.2f}",
        f"{currents[2]:.2f}",
        f"{total_current:.2f}",
        status
    ])

    # Make sure every reading is immediately saved
    file.flush()


# ==========================================
# Dashboard
# ==========================================

gpus = detect_gpu()

if not gpus:

    print()
    print("==============================================")
    print("              GPU-PinPower v1.1.0")
    print("==============================================")
    print()
    print("GPU: Not detected")
    print()
    print("==============================================")

    raise SystemExit


gpu = gpus[0]

info = get_gpu_info(gpu)

if info["power"] is None:

    print()
    print("==============================================")
    print("              GPU-PinPower v1.1.0")
    print("==============================================")
    print()
    print(f"GPU:     {gpu}")
    print(f"Vendor:  {info['vendor']}")
    print("Power:   N/A")
    print()
    print("Power specification is not available")
    print("for this GPU in the database.")
    print()
    print("==============================================")

    raise SystemExit


total_power = info["power"]

# ==========================================
# Start CSV Logger
# ==========================================

csv_file, csv_writer = setup_csv()


print("\033[2J\033[H", end="")

print("==============================================")
print("              GPU-PinPower v1.1.0")
print("==============================================")
print()
print(f"GPU:              {gpu}")
print(f"Vendor:           {info['vendor']}")
print(f"Power Spec:       {total_power} W")
print()
print("MODE:              ESTIMATED")
print()
print(f"CSV LOG:          {CSV_FILE}")
print()
print("----------------------------------------------")
print("PIN DISTRIBUTION")
print("----------------------------------------------")


try:

    while True:

        pins = simulate_pin_power(total_power)

        voltage = 12.0

        currents = [
            power / voltage
            for power in pins
        ]

        status = get_status(pins)

        total_current = sum(pins) / voltage

        # ==========================================
        # CSV Logging
        # ==========================================

        log_data(
            csv_writer,
            csv_file,
            gpu,
            info["vendor"],
            pins,
            voltage,
            currents,
            total_current,
            status
        )

        # ==========================================
        # Dashboard
        # ==========================================

        print("\033[2J\033[H", end="")

        print("==============================================")
        print("              GPU-PinPower v1.1.0")
        print("==============================================")
        print()
        print(f"GPU:              {gpu}")
        print(f"Vendor:           {info['vendor']}")
        print(f"Power Spec:       {total_power:.0f} W")
        print()
        print("MODE:              ESTIMATED")
        print()
        print("----------------------------------------------")
        print("PIN       POWER        VOLTAGE       CURRENT")
        print("----------------------------------------------")

        print(
            f"Pin 1     {pins[0]:6.2f} W      "
            f"{voltage:5.2f} V       "
            f"{currents[0]:5.2f} A"
        )

        print(
            f"Pin 2     {pins[1]:6.2f} W      "
            f"{voltage:5.2f} V       "
            f"{currents[1]:5.2f} A"
        )

        print(
            f"Pin 3     {pins[2]:6.2f} W      "
            f"{voltage:5.2f} V       "
            f"{currents[2]:5.2f} A"
        )

        print("----------------------------------------------")

        print(
            f"TOTAL     {sum(pins):6.2f} W      "
            f"{voltage:5.2f} V       "
            f"{total_current:5.2f} A"
        )

        print("----------------------------------------------")
        print()
        print(f"STATUS: {status}")
        print()
        print(f"CSV: Logging to {CSV_FILE}")
        print()
        print("⚠ Estimated values, not electrical measurements.")
        print("Press Ctrl+C to stop.")
        print()

        time.sleep(1)


except KeyboardInterrupt:

    print()
    print("GPU-PinPower stopped.")

finally:

    csv_file.close()
    print(f"CSV log saved to: {CSV_FILE}")