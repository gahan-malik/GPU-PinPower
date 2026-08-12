# GPU-PinPower

A Python tool for estimating and monitoring power distribution across individual PCIe GPU power pins. ⚡

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

Example:

```text after downloading the zip file. Extract all the files and right click the main.py file and run in terminal and write python main.py
GPU-PinPower
================================
MODE: ESTIMATED

Pin 1   ~40.2 W
Pin 2   ~39.7 W
Pin 3   ~40.1 W
================================
TOTAL   ~120.0 W

STATUS: NORMAL
License : TBD
