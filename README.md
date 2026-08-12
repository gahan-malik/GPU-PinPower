## Platform Support

GPU-PinPower is written in Python and is designed to work on:

- Windows 10 / 11
- Linux
- MacOS
- ChromeOS with Linux/Python support
- Raspberry Pi OS
- Google Colab

> GPU-PinPower is currently a software-based simulator. It does not require a physical GPU or PCIe power connector to run.

### 🧪 Current Development Platform

GPU-PinPower is currently being developed and tested on Windows.

Support for other platforms may depend on the Python version and installed dependencies.
## 🚧 Current Status

GPU-PinPower currently runs as a **digital simulator**.

It estimates how power could be distributed across the individual power lines of a PCIe GPU connector.

> ⚠️ These values are estimates, not real electrical measurements.

## Features

- Estimated per-pin power
- Estimated voltage and current
- Live monitoring
- Power calculations
- CSV logging
- Simulated pin imbalance detection
- Python-based

## Simulation

GPU-PinPower can simulate different GPU power conditions without requiring any hardware.
after you complete downloading the zip file, Extract it. Right-click the main.py file and run in terminal and write this code:python main.py 
< Example:
license: MIT
```text 
================================
MODE: ESTIMATED

Pin 1   ~40.2 W
Pin 2   ~39.7 W
Pin 3   ~40.1 W
================================
TOTAL   ~120.0 W

STATUS: NORMAL
