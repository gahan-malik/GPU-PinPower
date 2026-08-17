import subprocess


def detect_gpu():
    """
    Detect installed GPUs on Windows.

    Returns:
        list: Detected GPUs with their names and vendors.
    """

    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-CimInstance Win32_VideoController | "
                "Select-Object Name, AdapterCompatibility | "
                "ConvertTo-Json"
            ],
            capture_output=True,
            text=True,
            check=True
        )

        import json

        data = json.loads(result.stdout)

        if isinstance(data, dict):
            data = [data]

        gpus = []

        for gpu in data:
            name = gpu.get("Name")
            vendor = gpu.get("AdapterCompatibility")

            if name:
                gpus.append({
                    "name": name.strip(),
                    "vendor": vendor.strip() if vendor else "Unknown"
                })

        return gpus

    except (subprocess.SubprocessError, OSError, json.JSONDecodeError):
        return []