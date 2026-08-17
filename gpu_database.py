def find_gpu(gpu_name):
    database = load_database()

    if database is None:
        return None

    detected_name = gpu_name.lower().strip()

    # Exact match
    for gpu in database["gpus"]:
        if gpu["name"].lower().strip() == detected_name:
            return gpu

    # Partial match
    for gpu in database["gpus"]:
        database_name = gpu["name"].lower().strip()

        if database_name in detected_name:
            return gpu

    return None