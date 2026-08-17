# GPU-PinPower

GPU-PinPower is a Python-based GPU power estimation and monitoring simulator.

It estimates how a GPU's reference power could be distributed across individual power pins and calculates estimated voltage and current values.

> ⚠️ **Important:** GPU-PinPower uses estimated/simulated values. It does **not** directly measure electrical power flowing through individual GPU connector pins.

## Version

**GPU-PinPower V1.2.0**

## Features

* GPU detection
* Multi-vendor GPU database
* NVIDIA GPU specifications
* AMD Radeon desktop GPU specifications
* Intel Arc and Intel integrated graphics database
* Apple Silicon database
* GPU architecture information
* Desktop/integrated GPU type information
* Reference power specification lookup
* Estimated per-pin power distribution
* Estimated voltage
* Estimated per-pin current
* Estimated total current
* Pin imbalance detection
* Live-updating terminal dashboard
* CSV logging
* Cross-platform detection logic for Windows, Linux and macOS

## Supported GPU Databases

### NVIDIA

The NVIDIA database covers major desktop GPU generations from modern RTX cards back to older GeForce generations.

Examples include:

* GeForce RTX 50 Series
* GeForce RTX 40 Series
* GeForce RTX 30 Series
* GeForce RTX 20 Series
* GeForce GTX 16 Series
* GeForce GTX 10 Series
* GeForce GTX 900 Series
* GeForce GTX 700 Series
* GeForce GTX 600 Series
* GeForce GTX 500 Series
* GeForce GTX 400 Series
* GeForce GTX 200 Series
* GeForce 9000 Series
* GeForce 8000 Series
* GeForce 7000 Series
* GeForce 6000 Series
* GeForce FX 5000 Series
* GeForce 4 Series
* GeForce 3 Series
* GeForce 2 Series
* GeForce 256

## AMD

The AMD desktop database covers major Radeon generations from the RX 9000 generation back to the HD 5000 era.

Examples include:

* Radeon RX 9000 Series
* Radeon RX 7000 Series
* Radeon RX 6000 Series
* Radeon RX 5000 Series
* Radeon RX 500 Series
* Radeon RX 400 Series
* Radeon R9 Series
* Radeon R7 Series
* Radeon R5 Series
* Radeon HD 7000 Series
* Radeon HD 6000 Series
* Radeon HD 5000 Series

The AMD database in this release focuses on **desktop GPUs**.

## Intel

The Intel database includes:

* Intel Arc B-Series
* Intel Arc A-Series
* Intel Iris Xe
* Intel UHD Graphics
* Intel HD Graphics

Integrated Intel graphics use `N/A` for standalone GPU power specifications when a separate GPU power rating is not appropriate.

## Apple Silicon

Apple Silicon coverage includes the major:

* Apple M1
* Apple M1 Pro
* Apple M1 Max
* Apple M1 Ultra
* Apple M2
* Apple M2 Pro
* Apple M2 Max
* Apple M2 Ultra
* Apple M3
* Apple M3 Pro
* Apple M3 Max
* Apple M3 Ultra
* Apple M4
* Apple M4 Pro
* Apple M4 Max
* Apple M5
* Apple M5 Pro
* Apple M5 Max

Apple Silicon GPUs are integrated into the SoC, so a standalone GPU power specification may be shown as `N/A`.

## Power Estimation

GPU-PinPower uses the GPU's database power specification as the reference value.

For example:

```text
Power Spec: 130 W
```

The simulator then distributes that power across three simulated pins.

Example:

```text
Pin 1     42.31 W
Pin 2     43.27 W
Pin 3     44.42 W

TOTAL     130.00 W
```

The distribution changes slightly over time to simulate normal variation.

## Voltage and Current

V1.2.0 retains the V1.1.0 estimation model.

The simulator uses:

```text
Voltage = 12.00 V
```

Estimated current is calculated using:

```text
Current = Power / Voltage
```

Example:

```text
Power:   43.20 W
Voltage: 12.00 V
Current: 3.60 A
```

## Pin Balance

GPU-PinPower compares the estimated power on each pin.

Possible statuses are:

```text
NORMAL
SLIGHT IMBALANCE
HIGH IMBALANCE
```

These are simulated software results and should not be treated as electrical safety measurements.

## CSV Logging

GPU-PinPower automatically logs readings to:

```text
gpu_pinpower_log.csv
```

Logged information includes:

* Timestamp
* GPU
* Vendor
* Architecture
* GPU type
* Mode
* Reference power
* Pin power
* Total power
* Voltage
* Pin current
* Total current
* Status

## Running GPU-PinPower

Open a terminal in the V1.2.0 directory:

```powershell
cd GPU-PinPower-v1.2.0
```

Run:

```powershell
python main.py
```

Press:

```text
Ctrl+C
```

to stop the program.

## Example Output

```text
==============================================
              GPU-PinPower v1.2.0
==============================================

GPU:              NVIDIA GeForce RTX 5050
Vendor:           NVIDIA
Architecture:     Blackwell
Type:             Desktop
Power Spec:       130 W
Power Type:       TGP

MODE:              ESTIMATED

----------------------------------------------
PIN       POWER        VOLTAGE       CURRENT
----------------------------------------------
Pin 1      42.31 W      12.00 V        3.53 A
Pin 2      43.27 W      12.00 V        3.61 A
Pin 3      44.42 W      12.00 V        3.70 A
----------------------------------------------
TOTAL     130.00 W      12.00 V       10.83 A
----------------------------------------------

STATUS: NORMAL
```

## Important Limitations

GPU-PinPower is a **simulation and estimation tool**.

It does not directly measure:

* PCIe connector pin current
* PCIe connector pin voltage
* Individual physical power-pin temperature
* Actual electrical current flowing through each connector pin

Reference power specifications and estimated readings are different things.

For GPUs without a suitable database power specification, GPU-PinPower may display:

```text
Power Spec: N/A
```

## Project Structure

```text
GPU-PinPower-v1.2.0/
│
├── main.py
├── gpu_detection.py
├── gpu_database.py
├── AMDdatabase.py
├── Inteldatabase.py
├── AppleSiliconDatabase.py
├── GPU-PinPower.py
└── gpu_pinpower_log.csv
```

## Platforms

GPU detection logic is provided for:

* Windows
* Linux
* macOS

The exact information available depends on the operating system, GPU driver and hardware.

## Version History

### V1.2.0

* Expanded GPU database
* Added AMD database
* Added Intel database
* Added Apple Silicon database
* Expanded NVIDIA database
* Added architecture information
* Added GPU type information
* Improved GPU database lookup
* Restored estimated power distribution
* Restored estimated voltage and current calculations
* Improved CSV logging
* Added multi-vendor database support
* Updated terminal dashboard

### V1.1.0

* Added GPU detection
* Added GPU power specifications
* Added estimated pin power
* Added estimated voltage
* Added estimated current
* Added pin imbalance detection
* Added CSV logging

### V1.0.0

* Initial GPU-PinPower release
* Power distribution simulation
* Pin imbalance simulation

## License

This project is provided for educational and experimental purposes.

GPU-PinPower is not intended to be used as a certified electrical measurement or hardware safety tool.
