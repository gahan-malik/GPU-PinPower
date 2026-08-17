from gpu_detection import detect_gpu
from gpu_database import find_gpu


def main():
    print("==============================")
    print("       GPU-PinPower V1.2.0")
    print("==============================")
    print()

    gpus = detect_gpu()

    if not gpus:
        print("GPU: Not detected")
        return

    for detected_gpu in gpus:
        gpu_name = detected_gpu["name"]

        print(f"GPU: {gpu_name}")
        print(f"Vendor: {detected_gpu['vendor']}")

        database_gpu = find_gpu(gpu_name)

        if database_gpu:
            print(f"Power: {database_gpu['power']} W")
        else:
            print("Power: N/A")

        print()


if __name__ == "__main__":
    main()