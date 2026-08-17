import platform
import subprocess
import random
import time
import csv
import os
from datetime import datetime


# ============================================================
# GPU-PinPower v1.2.0
# Multi-vendor GPU database + estimated power monitoring
# ============================================================

from gpu_database import GPU_DATABASE

try:
    from AMDdatabase import AMD_GPU_DATABASE
except ImportError:
    AMD_GPU_DATABASE = {}

try:
    from Inteldatabase import INTEL_GPU_DATABASE
except ImportError:
    INTEL_GPU_DATABASE = {}

try:
    from AppleSiliconDatabase import APPLE_SILICON_DATABASE
except ImportError:
    APPLE_SILICON_DATABASE = {}


# ============================================================
# Combine all databases
# ============================================================

ALL_GPU_DATABASES = {}

ALL_GPU_DATABASES.update(GPU_DATABASE)
ALL_GPU_DATABASES.update(AMD_GPU_DATABASE)
ALL_GPU_DATABASES.update(INTEL_GPU_DATABASE)
ALL_GPU_DATABASES.update(APPLE_SILICON_DATABASE)


# ============================================================
# GPU Detection
# ============================================================

def detect_gpu():
    system = platform.system()

    try:

        # ----------------------------------------------------
        # Windows
        # ----------------------------------------------------

        if system == "Windows":

            command = [
                "powershell",
                "-Command",
                "Get-CimInstance Win32_VideoController | "
                "Select-Object -ExpandProperty Name"
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            return [
                line.strip()
                for line in result.stdout.splitlines()
                if line.strip()
            ]


        # ----------------------------------------------------
        # Linux
        # ----------------------------------------------------

        elif system == "Linux":

            command = [
                "sh",
                "-c",
                "lspci | grep -Ei 'VGA|3D|Display'"
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            return [
                line.strip()
                for line in result.stdout.splitlines()
                if line.strip()
            ]


        # ----------------------------------------------------
        # macOS
        # ----------------------------------------------------

        elif system == "Darwin":

            command = [
                "system_profiler",
                "SPDisplaysDataType"
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

            gpus = []

            for line in result.stdout.splitlines():

                line = line.strip()

                if line.startswith("Chipset Model:"):

                    gpu_name = line.split(":", 1)[1].strip()

                    gpus.append(gpu_name)

            return gpus


        return []

    except Exception:
        return []


# ============================================================
# GPU Database Lookup
# ============================================================

def get_gpu_info(gpu_name):

    gpu_lower = gpu_name.lower()

    # --------------------------------------------------------
    # Exact / substring lookup
    # --------------------------------------------------------

    for model, info in ALL_GPU_DATABASES.items():

        model_lower = model.lower()

        if model_lower in gpu_lower:

            return {
                "model": model,
                "vendor": info.get("vendor", "Unknown"),
                "architecture": info.get(
                    "architecture",
                    "Unknown"
                ),
                "type": info.get(
                    "type",
                    "Unknown"
                ),
                "power_watts": info.get(
                    "power_watts"
                ),
                "power_type": info.get(
                    "power_type",
                    "Unknown"
                ),
                "notes": info.get(
                    "notes",
                    ""
                )
            }


    # --------------------------------------------------------
    # Reverse lookup
    #
    # Helps when the detected name contains a slightly
    # different vendor prefix.
    # --------------------------------------------------------

    for model, info in ALL_GPU_DATABASES.items():

        model_words = model.lower().split()

        useful_words = [
            word
            for word in model_words
            if len(word) > 2
        ]

        if useful_words:

            matches = sum(
                word in gpu_lower
                for word in useful_words
            )

            if matches >= max(
                2,
                len(useful_words) // 2
            ):

                return {
                    "model": model,
                    "vendor": info.get(
                        "vendor",
                        "Unknown"
                    ),
                    "architecture": info.get(
                        "architecture",
                        "Unknown"
                    ),
                    "type": info.get(
                        "type",
                        "Unknown"
                    ),
                    "power_watts": info.get(
                        "power_watts"
                    ),
                    "power_type": info.get(
                        "power_type",
                        "Unknown"
                    ),
                    "notes": info.get(
                        "notes",
                        ""
                    )
                }


    # --------------------------------------------------------
    # Unknown GPU
    # --------------------------------------------------------

    return {
        "model": gpu_name,
        "vendor": "Unknown",
        "architecture": "Unknown",
        "type": "Unknown",
        "power_watts": None,
        "power_type": "Unknown",
        "notes": "No database entry"
    }


# ============================================================
# Estimated Pin Power
# ============================================================

def simulate_pin_power(total_power):

    if total_power is None:
        return [None, None, None]

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


# ============================================================
# Current Calculation
# ============================================================

def calculate_currents(pin_power, voltage):

    if voltage <= 0:
        return [0.0, 0.0, 0.0]

    return [
        power / voltage
        for power in pin_power
    ]


# ============================================================
# Pin Status
# ============================================================

def get_status(pin_power):

    if not pin_power:
        return "N/A"

    average = sum(pin_power) / len(pin_power)

    if average <= 0:
        return "N/A"

    difference = max(
        abs(power - average)
        for power in pin_power
    )

    percentage = (
        difference / average
    ) * 100

    if percentage < 5:
        return "NORMAL"

    elif percentage < 10:
        return "SLIGHT IMBALANCE"

    else:
        return "HIGH IMBALANCE"


# ============================================================
# CSV Logging
# ============================================================

CSV_FILE = "gpu_pinpower_log.csv"


def setup_csv():

    file = open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8"
    )

    writer = csv.writer(file)

    if os.path.getsize(CSV_FILE) == 0:

        writer.writerow([
            "Timestamp",
            "GPU",
            "Vendor",
            "Architecture",
            "Type",
            "Mode",
            "Power Spec (W)",
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
    info,
    pin_power,
    voltage,
    currents,
    total_current,
    status
):

    writer.writerow([
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        gpu,

        info["vendor"],

        info["architecture"],

        info["type"],

        "ESTIMATED",

        (
            ""
            if info["power_watts"] is None
            else f"{info['power_watts']:.2f}"
        ),

        f"{pin_power[0]:.2f}",
        f"{pin_power[1]:.2f}",
        f"{pin_power[2]:.2f}",

        f"{sum(pin_power):.2f}",

        f"{voltage:.2f}",

        f"{currents[0]:.2f}",
        f"{currents[1]:.2f}",
        f"{currents[2]:.2f}",

        f"{total_current:.2f}",

        status
    ])

    file.flush()


# ============================================================
# Dashboard
# ============================================================

def main():

    print()
    print("==============================================")
    print("              GPU-PinPower v1.2.0")
    print("==============================================")
    print()
    print("Detecting GPU...")
    print()

    gpus = detect_gpu()

    if not gpus:

        print("GPU: Not detected")
        print()

        print("==============================================")

        return


    # --------------------------------------------------------
    # Use the first detected GPU
    # --------------------------------------------------------

    gpu = gpus[0]

    info = get_gpu_info(gpu)


    # --------------------------------------------------------
    # No database entry
    # --------------------------------------------------------

    if info["power_watts"] is None:

        print(
            f"GPU:          {gpu}"
        )

        print(
            f"Vendor:       {info['vendor']}"
        )

        print(
            f"Architecture: {info['architecture']}"
        )

        print(
            f"Type:         {info['type']}"
        )

        print(
            "Power Spec:   N/A"
        )

        print(
            f"Power Type:   {info['power_type']}"
        )

        print(
            f"Notes:        {info['notes']}"
        )

        print()

        print(
            "No reference power value is available."
        )

        print(
            "Estimated power monitoring is disabled."
        )

        return


    # --------------------------------------------------------
    # Reference power
    # --------------------------------------------------------

    power_spec = info["power_watts"]

    # V1.1.0-style estimated voltage
    voltage = 12.0


    # --------------------------------------------------------
    # CSV
    # --------------------------------------------------------

    csv_file, csv_writer = setup_csv()


    try:

        while True:

            # -----------------------------------------------
            # Estimate pin power
            # -----------------------------------------------

            pin_power = simulate_pin_power(
                power_spec
            )

            total_power = sum(pin_power)


            # -----------------------------------------------
            # Calculate current
            # -----------------------------------------------

            currents = calculate_currents(
                pin_power,
                voltage
            )

            total_current = (
                total_power / voltage
            )


            # -----------------------------------------------
            # Status
            # -----------------------------------------------

            status = get_status(
                pin_power
            )


            # -----------------------------------------------
            # CSV
            # -----------------------------------------------

            log_data(
                csv_writer,
                csv_file,
                gpu,
                info,
                pin_power,
                voltage,
                currents,
                total_current,
                status
            )


            # -----------------------------------------------
            # Clear terminal
            # -----------------------------------------------

            print(
                "\033[2J\033[H",
                end=""
            )


            # -----------------------------------------------
            # Header
            # -----------------------------------------------

            print(
                "=============================================="
            )

            print(
                "              GPU-PinPower v1.2.0"
            )

            print(
                "=============================================="
            )

            print()

            print(
                f"GPU:              {gpu}"
            )

            print(
                f"Vendor:           {info['vendor']}"
            )

            print(
                f"Architecture:     {info['architecture']}"
            )

            print(
                f"Type:              {info['type']}"
            )

            print(
                f"Power Spec:       {power_spec} W"
            )

            print(
                f"Power Type:       {info['power_type']}"
            )

            print()

            print(
                "MODE:              ESTIMATED"
            )

            print()

            print(
                "----------------------------------------------"
            )

            print(
                "PIN       POWER        VOLTAGE       CURRENT"
            )

            print(
                "----------------------------------------------"
            )


            # -----------------------------------------------
            # Pin 1
            # -----------------------------------------------

            print(
                f"Pin 1     "
                f"{pin_power[0]:6.2f} W      "
                f"{voltage:5.2f} V       "
                f"{currents[0]:5.2f} A"
            )


            # -----------------------------------------------
            # Pin 2
            # -----------------------------------------------

            print(
                f"Pin 2     "
                f"{pin_power[1]:6.2f} W      "
                f"{voltage:5.2f} V       "
                f"{currents[1]:5.2f} A"
            )


            # -----------------------------------------------
            # Pin 3
            # -----------------------------------------------

            print(
                f"Pin 3     "
                f"{pin_power[2]:6.2f} W      "
                f"{voltage:5.2f} V       "
                f"{currents[2]:5.2f} A"
            )


            # -----------------------------------------------
            # Total
            # -----------------------------------------------

            print(
                "----------------------------------------------"
            )

            print(
                f"TOTAL     "
                f"{total_power:6.2f} W      "
                f"{voltage:5.2f} V       "
                f"{total_current:5.2f} A"
            )

            print(
                "----------------------------------------------"
            )

            print()

            print(
                f"STATUS: {status}"
            )

            print()

            print(
                f"CSV: Logging to {CSV_FILE}"
            )

            print()

            print(
                "Reference power comes from the GPU database."
            )

            print(
                "Live-looking values are simulated estimates."
            )

            print()

            print(
                "Press Ctrl+C to stop."
            )

            print()


            time.sleep(1)


    except KeyboardInterrupt:

        print()

        print(
            "GPU-PinPower stopped."
        )


    finally:

        csv_file.close()

        print(
            f"CSV log saved to: {CSV_FILE}"
        )


# ============================================================
# Start
# ============================================================

if __name__ == "__main__":
    main()