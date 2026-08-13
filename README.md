# GPU-PinPower

GPU-PinPower is a Python-based GPU detection and power estimation tool.

It detects the GPU reported by the operating system, looks up its known power specification, and simulates how that power could be distributed across individual GPU power lines.

> GPU-PinPower is currently a software-based simulator. Power, voltage, current, and pin distribution values are estimates, not real electrical measurements.

## Versions

### V1.1.0

Current release.

V1.1.0 adds:

* CSV logging
* Improved GPU information display
* Estimated pin power distribution
* Estimated voltage and current
* Live terminal dashboard
* Pin imbalance status
* Improved platform support
* Updated documentation

### V1.0.0

Initial public release.

V1.0.0 introduced:

* GPU detection
* GPU power specification database
* Estimated power distribution
* Estimated voltage and current
* Pin imbalance status
* Live terminal output
* Software-only simulation

## Features

* Automatic GPU detection
* NVIDIA GPU detection
* AMD GPU detection
* Intel GPU detection
* Apple GPU detection
* GPU power specification lookup
* Estimated power distribution
* Estimated voltage
* Estimated current
* Live terminal dashboard
* Pin imbalance detection
* CSV logging
* Software-only operation
* No physical GPU power connector required

## Platform Support

GPU-PinPower is designed to work on:

* Windows 10 / 11
* Linux
* macOS
* Apple Silicon Macs
* ChromeOS with Linux/Python support
* Raspberry Pi OS
* Google Colab

> GPU detection depends on information provided by the operating system and the tools available on that platform.

### 🧪 Current Development Platform

GPU-PinPower is currently developed and tested on Windows.

Support for other platforms may depend on the installed Python version and available system tools.

## ⚡ Power Estimation

GPU-PinPower uses a database of known GPU power specifications.

It then estimates how the GPU's specified power could be distributed across simulated power lines.

The voltage and current values are calculated from these estimated power values.

For example, a GPU with a 130 W power specification may be displayed as approximately:

```text
Pin 1     43.21 W      12.00 V        3.60 A
Pin 2     43.84 W      12.00 V        3.65 A
Pin 3     42.95 W      12.00 V        3.58 A
----------------------------------------------
TOTAL     130.00 W      12.00 V       10.83 A
```

These values are simulated and should not be treated as electrical measurements.

## 📊 CSV Logging

V1.1.0 introduces automatic CSV logging.

While GPU-PinPower is running, readings are saved every second to:

```text
gpu_pinpower_log.csv
```

The CSV contains:

* Timestamp
* GPU name
* Vendor
* Operating mode
* Pin 1 power
* Pin 2 power
* Pin 3 power
* Total power
* Voltage
* Pin 1 current
* Pin 2 current
* Pin 3 current
* Total current
* Status

New sessions are appended to the existing CSV file instead of overwriting previous logs.

The CSV file is automatically ignored by Git so runtime logs are not uploaded to the repository.

## Requirements

* Python 3
* A supported operating system
* No external Python packages are required for the simulator

## How to Use

Download the project ZIP file and extract it.

Open a terminal in the extracted GPU-PinPower folder.

Run:

```text
python main.py
```

On some systems, use:

```text
python3 main.py
```

GPU-PinPower will detect the first GPU reported by the operating system and display its estimated power information.

Press:

```text
Ctrl+C
```

to stop the program.

## Windows Example

Open the project folder in File Explorer.

Right-click inside the folder and open a terminal.

Then run:

```text
python main.py
```

The program will start the live dashboard.

## Example Output

```text
==============================================
              GPU-PinPower v1.1.0
==============================================

GPU:              NVIDIA GeForce RTX 5050
Vendor:           NVIDIA
Power Spec:       130 W

MODE:              ESTIMATED

----------------------------------------------
PIN       POWER        VOLTAGE       CURRENT
----------------------------------------------
Pin 1      43.21 W      12.00 V        3.60 A
Pin 2      43.84 W      12.00 V        3.65 A
Pin 3      42.95 W      12.00 V        3.58 A
----------------------------------------------
TOTAL     130.00 W      12.00 V       10.83 A
----------------------------------------------

STATUS: NORMAL

CSV: Logging to gpu_pinpower_log.csv

⚠ Estimated values, not electrical measurements.
Press Ctrl+C to stop.
```

## Project Files

```text
GPU-PinPower/
├── main.py
├── README.md
└── .gitignore
```

`gpu_pinpower_log.csv` is generated automatically when GPU-PinPower runs and is not included in the repository.

## Supported GPU Database

The current built-in database contains:

| GPU      | Vendor | Power Specification |
| -------- | ------ | ------------------: |
| RTX 5050 | NVIDIA |               130 W |
| RTX 4060 | NVIDIA |               115 W |
| RTX 3060 | NVIDIA |               170 W |
| GTX 1650 | NVIDIA |                75 W |

GPU models that are detected but not included in the database will be reported as unsupported for power estimation.

## ⚠️ Important Notice

GPU-PinPower does **not** directly measure:

* GPU connector voltage
* GPU connector current
* Actual pin power
* Actual GPU power consumption

The displayed values are estimates generated by the software.

Do not use GPU-PinPower as an electrical testing or hardware safety instrument.

## Future Development

Possible future features include:

* More GPUs in the database
* Real hardware telemetry where supported
* Graphs and data visualization
* Advanced logging options
* Additional operating-system support
* More detailed power analysis

## License

MIT License

Copyright © 2026 gahan-malik
