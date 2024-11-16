HEADERS = ["BIG", "BAD", "WOLF"]

ERROR_FLAGS = {
    "1": "Battery device error",
    "2": "Temperature device error",
    "3": "Threshold central error"
}


def determine_device_error(s_p_1: str, s_p_2: str) -> str:
    combined_str = s_p_1[:-1] + s_p_2
    pairs = [combined_str[i:i+2] for i in range(0, len(combined_str), 2)]
    bin_pairs = [f"{int(num):08b}" for num in pairs]
    flags = [char[4] for char in bin_pairs]

    for i, flag in enumerate(flags, start=1):
        if flag == "1":
            return ERROR_FLAGS.get(str(i), "Unknown device error")
    return "Unknown device error"


def count_passed_sensors(log_file_path: str) -> None:
    good_sensors = {}
    bad_sensors = {}
    with open(log_file_path, "r") as log_file:
        for line in log_file:

            if HEADERS[0] in line:
                a = line.split(";")
                device_id = a[2]
                state = a[-2]
                s_p_1 = a[6]
                s_p_2 = a[-6]

                if state != "02" and device_id not in bad_sensors:

                    bad_sensors[device_id] = determine_device_error(s_p_1, s_p_2)

                if state == "02" and (
                    device_id not in good_sensors) and (
                    device_id not in bad_sensors):
                    good_sensors[device_id] = 1

                if state == "02" and (
                    device_id in good_sensors) and (
                    device_id not in bad_sensors):
                    good_sensors[device_id] += 1

                if device_id in bad_sensors and device_id in good_sensors:
                    good_sensors.pop(device_id)

    good_sensors_amount = len(good_sensors)
    bad_sensors_amount = len(bad_sensors)
    all_sensors_amount = good_sensors_amount + bad_sensors_amount

    print("All sensors amount:", all_sensors_amount)
    print("Good sensors amount:", good_sensors_amount)
    print("Bad sensors amount:", bad_sensors_amount, "\n")

    for device_id, error_message in bad_sensors.items():
        print(device_id, ": ", error_message)
    print("\n")

    print("Success messages count:")
    for device_id, amount in good_sensors.items():
        print(device_id, ": ", amount)


count_passed_sensors("app_2 (1) (1) (1) (2).log")
