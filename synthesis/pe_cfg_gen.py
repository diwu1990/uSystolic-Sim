def pe_config_gen(
    path=None,
    frequency=400
):
    file = open(path+"/pe.cfg", "w")
    print("path: ", path)

    config_log = "[Frequency]\nMHz:\t" + str(frequency) + "\n\n"

    # Unaryrate
    config_log += "[UnaryRate]\n"
    config_log = config_log_gen(path=path, computing="unaryrate", config_log=config_log)
    config_log += "[UnaryTemporal]\n"
    config_log = config_log_gen(path=path, computing="unarytemporal", config_log=config_log)
    config_log += "[BinarySerial]\n"
    config_log = config_log_gen(path=path, computing="binaryserial", config_log=config_log)
    config_log += "[BinaryParallel]\n"
    config_log = config_log_gen(path=path, computing="binaryparallel", config_log=config_log)
    file.write(config_log)
    file.close()


def config_log_gen(
    path=None,
    computing=None,
    config_log=None
):
    print("computing: ", computing)
    config_log += "IREG:\t"
    area, leakage, dynamic = profile(path=path, computing=computing, prefix="ireg_border")
    config_log += str(area) + ",\t" + str(leakage) + ",\t" + str(dynamic) + ",\t"
    area, leakage, dynamic = profile(path=path, computing=computing, prefix="ireg_inner")
    config_log += str(area) + ",\t" + str(leakage) + ",\t" + str(dynamic) + ",\t\n"

    config_log += "WREG:\t"
    area, leakage, dynamic = profile(path=path, computing=computing, prefix="wreg")
    config_log += str(area) + ",\t" + str(leakage) + ",\t" + str(dynamic) + ",\t\n"

    config_log += "MUL:\t"
    area, leakage, dynamic = profile(path=path, computing=computing, prefix="mul_border")
    config_log += str(area) + ",\t" + str(leakage) + ",\t" + str(dynamic) + ",\t"
    area, leakage, dynamic = profile(path=path, computing=computing, prefix="mul_inner")
    config_log += str(area) + ",\t" + str(leakage) + ",\t" + str(dynamic) + ",\t\n"

    config_log += "ACC:\t"
    area, leakage, dynamic = profile(path=path, computing=computing, prefix="acc")
    config_log += str(area) + ",\t" + str(leakage) + ",\t" + str(dynamic) + ",\t\n\n"

    return config_log


def profile(
    path=None,
    computing=None,
    prefix=None
):
    """
    unit: area (mm^2), leakage (mW), dynamic (mW)
    """
    area_file = open(path + "/" + computing + "/" + prefix + "_area.txt", "r")
    area = area_report(area_file)
    power_file = open(path + "/" + computing + "/" + prefix + "_power.txt", "r")
    leakage, dynamic = power_report(power_file)
    area_file.close()
    power_file.close()
    return area, leakage, dynamic


def power_report(
    file=None
):
    """
    all outputs have the unit of mW
    """
    for entry in file:
        elems = entry.strip().split(' ')
        elems = prune(elems)
        if len(elems) >= 6:
            if elems[0] == "Total" and elems[1] == "Dynamic" and elems[2] == "Power" and elems[3] == "=":
                dynamic = float(elems[4])
                unit = str(elems[5])
                if unit == "nW":
                    dynamic /= 1000000.0
                elif unit == "uW":
                    dynamic /= 1000.0
                elif unit == "mW":
                    dynamic *= 1.0
                else:
                    print("Unknown unit for dynamic power:" + unit)

            if elems[0] == "Cell" and elems[1] == "Leakage" and elems[2] == "Power" and elems[3] == "=":
                leakage = float(elems[4])
                unit = str(elems[5])
                if unit == "nW":
                    leakage /= 1000000.0
                elif unit == "uW":
                    leakage /= 1000.0
                elif unit == "mW":
                    leakage *= 1.0
                else:
                    print("Unknown unit for leakage power:" + unit)

    return leakage, dynamic


def area_report(
    file=None
):
    """
    output has the unit of mm^2
    """
    for entry in file:
        elems = entry.strip().split(' ')
        elems = prune(elems)
        if len(elems) >= 3:
            if str(elems[0]) == "Total" and str(elems[1]) == "cell" and str(elems[2]) == "area:":
                area = float(elems[3])

            if str(elems[0]) == "Total" and str(elems[1]) == "area:":
                if str(elems[2]) != "undefined":
                    if area < float(elems[2]):
                        area = float(elems[2])
                    
    area /= 1000000.0
    return area


def prune(input_list):
    l = []

    for e in input_list:
        e = e.strip() # remove the leading and trailing characters, here space
        if e != '' and e != ' ':
            l.append(e)

    return l


if __name__ == "__main__":
    pe_config_gen(path="./32nm_rvt/8bit", frequency=400)
    pe_config_gen(path="./32nm_rvt/16bit", frequency=400)
    pe_config_gen(path="./45nm_rvt/8bit", frequency=400)
    pe_config_gen(path="./45nm_rvt/16bit", frequency=400)