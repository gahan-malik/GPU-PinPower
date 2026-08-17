# GPU-PinPower

GPU-PinPower is a Python-based GPU detection and power estimation tool.

It detects the GPU reported by the operating system, looks up its known power specification, and estimates how that power could be distributed across simulated GPU power lines.

>  GPU-PinPower is a software-based simulator. Power, voltage, current, and pin-distribution values are estimates, not real electrical measurements.

##  V1.2.0

V1.2.0 is a major GPU database and compatibility update.

### What's New

- Expanded GPU database
- NVIDIA, AMD, Intel, and Apple Silicon database support
- Improved GPU detection
- GPU power specification lookup
- Improved database handling
- Expanded project structure
- Updated platform support information
- Updated documentation

V1.2.0 expands GPU-PinPower beyond the RTX 5050-focused support introduced in V1.1.0 and provides the foundation for broader GPU support.

## ⚠️ Important: Running the V1.2.0 ZIP

The V1.2.0 download ZIP contains the main project inside the `GPU-PinPower-v1.2.0` folder.

After extracting the ZIP, open a terminal inside that folder and run:

```text
python main.py
```

On some systems, use:

```text
python3 main.py
```

> **Important:** The outer extracted folder also contains a `main.py`. For V1.2.0, run the `main.py` inside `GPU-PinPower-v1.2.0`.

Example:

```text
GPU-PinPower-1.2.0/
└── GPU-PinPower-1.2.0/
    └── GPU-PinPower-v1.2.0/
        ├── main.py
        ├── gpu_database.py
        ├── gpu_detection.py
        └── ...
```

## Features

- Automatic GPU detection
- NVIDIA GPU detection
- AMD GPU detection
- Intel GPU detection
- Apple GPU detection
- GPU power specification lookup
- Estimated power distribution
- Estimated voltage
- Estimated current
- Live terminal output
- Pin imbalance detection
- CSV logging
- Software-only operation
- No physical GPU power connector required

## Platform Support

GPU-PinPower is designed to work on:

- Windows 10 / 11
- Linux
- macOS
- Apple Silicon Macs
- ChromeOS with Linux/Python support
- Raspberry Pi OS
- Google Colab

> GPU detection depends on information provided by the operating system and the tools available on that platform.

###  Current Development Platform

GPU-PinPower is currently developed and tested on Windows.

Support for other platforms may depend on the installed Python version and available system tools.

##  Power Estimation

GPU-PinPower uses a database of known GPU power specifications.

It estimates how the GPU's specified power could be distributed across simulated power lines.

Voltage and current values are calculated from these estimated power values.

For example, a GPU with a 130 W power specification may be displayed as approximately:

```text
Pin 1     43.21 W      12.00 V        3.60 A
Pin 2     43.84 W      12.00 V        3.65 A
Pin 3     42.95 W      12.00 V        3.58 A
----------------------------------------------
TOTAL     130.00 W      12.00 V       10.83 A
```

These values are simulated and should not be treated as electrical measurements.

##  CSV Logging

GPU-PinPower supports CSV logging for runtime data.

When logging is enabled, readings can be saved to:

```text
gpu_pinpower_log.csv
```

Runtime logs are ignored by Git and are not uploaded to the repository.

## Requirements

- Python 3
- A supported operating system
- No external Python packages are required for the core simulator

## How to Use

1. Download the project ZIP from the GitHub Releases page.
2. Extract the ZIP.
3. Open a terminal inside the `GPU-PinPower-v1.2.0` folder.
4. Run:

```text
python main.py
```

On some systems:

```text
python3 main.py
```

GPU-PinPower will detect the GPU reported by the operating system and display its available power information.

Press:

```text
Ctrl+C
```

to stop the program.

## Windows Example

Open the `GPU-PinPower-v1.2.0` folder in File Explorer.

Right-click inside the folder and open a terminal.

Then run:

```text
python main.py
```

## Example Output

```text
==============================
       GPU-PinPower V1.2.0
==============================

GPU: NVIDIA GeForce RTX 5050
Vendor: NVIDIA
Power: 130 W
```

The exact output depends on the detected GPU and the available database information.

## Project Files

The V1.2.0 project contains the main program, GPU detection code, and GPU database modules.

```text
GPU-PinPower-v1.2.0/
├── main.py
├── GPU-PinPower.py
├── gpu_detection.py
├── gpu_database.py
├── gpu_database.json
├── AMDdatabase.py
├── Inteldatabase.py
├── AppleSiliconDatabase.py
└── README.md
```

##  GPU Database

V1.2.0 expands the GPU database structure to support multiple GPU vendors and architectures.

The database contains power specifications used for software estimation. GPU models that are detected but do not have matching database information may report unavailable power information.

## ⚠️ Important Notice

GPU-PinPower does **not** directly measure:

- GPU connector voltage
- GPU connector current
- Actual pin power
- Actual GPU power consumption

The displayed values are estimates generated by software.

Do not use GPU-PinPower as an electrical testing or hardware safety instrument.

## Future Development

Possible future features include:

- More GPUs in the database
- Real hardware telemetry where supported
- Graphs and data visualization
- Advanced logging options
- Additional operating-system support
- More detailed power analysis

## License

MIT License

Copyright © 2026 gahan-malik
