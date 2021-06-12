import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

def pe_config_gen(
    path=None,
    frequency=400
):
    print("path: ", path)
    config_log = "[Frequency]\nMHz:\t" + str(frequency) + "\n\n"
    reg_log = ""

    config_log += "[UnaryRate]\n"
    reg_log += "[UnaryRate]\n"
    config_log, total_area, total_leakage, total_dynamic = config_log_gen(path=path, computing="unaryrate", config_log=config_log)
    reg_log = pe_regression(path=path, computing="unaryrate", reg_log=reg_log, total_area=total_area, total_leakage=total_leakage, total_dynamic=total_dynamic)

    config_log += "[UnaryTemporal]\n"
    reg_log += "[UnaryTemporal]\n"
    config_log, total_area, total_leakage, total_dynamic = config_log_gen(path=path, computing="unarytemporal", config_log=config_log)
    reg_log = pe_regression(path=path, computing="unarytemporal", reg_log=reg_log, total_area=total_area, total_leakage=total_leakage, total_dynamic=total_dynamic)
    
    config_log += "[UgemmRate]\n"
    reg_log += "[UgemmRate]\n"
    config_log, total_area, total_leakage, total_dynamic = config_log_gen(path=path, computing="ugemmrate", config_log=config_log)
    reg_log = pe_regression(path=path, computing="ugemmrate", reg_log=reg_log, total_area=total_area, total_leakage=total_leakage, total_dynamic=total_dynamic)
    
    config_log += "[BinarySerial]\n"
    reg_log += "[BinarySerial]\n"
    config_log, total_area, total_leakage, total_dynamic = config_log_gen(path=path, computing="binaryserial", config_log=config_log)
    reg_log = pe_regression(path=path, computing="binaryserial", reg_log=reg_log, total_area=total_area, total_leakage=total_leakage, total_dynamic=total_dynamic)
    
    config_log += "[BinaryParallel]\n"
    reg_log += "[BinaryParallel]\n"
    config_log, total_area, total_leakage, total_dynamic = config_log_gen(path=path, computing="binaryparallel", config_log=config_log)
    reg_log = pe_regression(path=path, computing="binaryparallel", reg_log=reg_log, total_area=total_area, total_leakage=total_leakage, total_dynamic=total_dynamic)
    
    file = open(path+"/pe.cfg", "w")
    file.write(config_log)
    file.close()

    file = open(path+"/regression.cfg", "w")
    file.write(reg_log)
    file.close()


def config_log_gen(
    path=None,
    computing=None,
    config_log=None
):
    print("\t\tcomputing: ", computing)

    total_area = [0, 0]
    total_leakage = [0, 0]
    total_dynamic = [0, 0]

    config_log += "IREG:\t"
    area, leakage, dynamic = profile(path=path, computing=computing, prefix="ireg_border")
    total_area[0] += area
    total_leakage[0] += leakage
    total_dynamic[0] += dynamic
    config_log += str(area) + ",\t" + str(leakage) + ",\t" + str(dynamic) + ",\t"
    area, leakage, dynamic = profile(path=path, computing=computing, prefix="ireg_inner")
    total_area[1] += area
    total_leakage[1] += leakage
    total_dynamic[1] += dynamic
    config_log += str(area) + ",\t" + str(leakage) + ",\t" + str(dynamic) + ",\t\n"

    config_log += "WREG:\t"
    area, leakage, dynamic = profile(path=path, computing=computing, prefix="wreg")
    total_area[0] += area
    total_leakage[0] += leakage
    total_dynamic[0] += dynamic
    total_area[1] += area
    total_leakage[1] += leakage
    total_dynamic[1] += dynamic
    config_log += str(area) + ",\t" + str(leakage) + ",\t" + str(dynamic) + ",\t"
    config_log += str(area) + ",\t" + str(leakage) + ",\t" + str(dynamic) + ",\t\n"

    config_log += "MUL:\t"
    area, leakage, dynamic = profile(path=path, computing=computing, prefix="mul_border")
    total_area[0] += area
    total_leakage[0] += leakage
    total_dynamic[0] += dynamic
    config_log += str(area) + ",\t" + str(leakage) + ",\t" + str(dynamic) + ",\t"
    area, leakage, dynamic = profile(path=path, computing=computing, prefix="mul_inner")
    total_area[1] += area
    total_leakage[1] += leakage
    total_dynamic[1] += dynamic
    config_log += str(area) + ",\t" + str(leakage) + ",\t" + str(dynamic) + ",\t\n"

    config_log += "ACC:\t"
    area, leakage, dynamic = profile(path=path, computing=computing, prefix="acc")
    total_area[0] += area
    total_leakage[0] += leakage
    total_dynamic[0] += dynamic
    total_area[1] += area
    total_leakage[1] += leakage
    total_dynamic[1] += dynamic
    config_log += str(area) + ",\t" + str(leakage) + ",\t" + str(dynamic) + ",\t"
    config_log += str(area) + ",\t" + str(leakage) + ",\t" + str(dynamic) + ",\t\n\n"

    return config_log, total_area, total_leakage, total_dynamic


def pe_regression(
    path=None,
    computing=None,
    reg_log=None,
    total_area=None,
    total_leakage=None,
    total_dynamic=None
):
    
    input = np.array([[4, 4], [8, 8], [12, 14], [16, 16], [32, 32]])
    input = np.log2(input)

    area_out = np.array([])
    leakage_out = np.array([])
    dynamic_out = np.array([])

    # pe_border
    area_b, leakage_b, dynamic_b = profile(path=path, computing=computing, prefix="pe_border")
    
    # pe_inner
    area_i, leakage_i, dynamic_i = profile(path=path, computing=computing, prefix="pe_inner")

    # array_4
    H = 4
    W = 4
    cnt_b = H
    cnt_i = H * (W - 1)
    area_ref = cnt_b * area_b + cnt_i * area_i
    leakage_ref = cnt_b * leakage_b + cnt_i * leakage_i
    dynamic_ref = cnt_b * dynamic_b + cnt_i * dynamic_i
    area, leakage, dynamic = profile(path=path, computing=computing, prefix="array_"+str(H))
    area_r = area / area_ref
    leakage_r = leakage / leakage_ref
    dynamic_r = dynamic / dynamic_ref
    area_out = np.append(area_out, area_r)
    leakage_out = np.append(leakage_out, leakage_r)
    dynamic_out = np.append(dynamic_out, dynamic_r)

    # array_8
    H = 8
    W = 8
    cnt_b = H
    cnt_i = H * (W - 1)
    area_ref = cnt_b * area_b + cnt_i * area_i
    leakage_ref = cnt_b * leakage_b + cnt_i * leakage_i
    dynamic_ref = cnt_b * dynamic_b + cnt_i * dynamic_i
    area, leakage, dynamic = profile(path=path, computing=computing, prefix="array_"+str(H))
    area_r = area / area_ref
    leakage_r = leakage / leakage_ref
    dynamic_r = dynamic / dynamic_ref
    area_out = np.append(area_out, area_r)
    leakage_out = np.append(leakage_out, leakage_r)
    dynamic_out = np.append(dynamic_out, dynamic_r)

    # array_eyeriss
    H = 12
    W = 14
    cnt_b = H
    cnt_i = H * (W - 1)
    area_ref = cnt_b * area_b + cnt_i * area_i
    leakage_ref = cnt_b * leakage_b + cnt_i * leakage_i
    dynamic_ref = cnt_b * dynamic_b + cnt_i * dynamic_i
    area, leakage, dynamic = profile(path=path, computing=computing, prefix="array_eyeriss")
    area_r = area / area_ref
    leakage_r = leakage / leakage_ref
    dynamic_r = dynamic / dynamic_ref
    area_out = np.append(area_out, area_r)
    leakage_out = np.append(leakage_out, leakage_r)
    dynamic_out = np.append(dynamic_out, dynamic_r)

    # array_16
    H = 16
    W = 16
    cnt_b = H
    cnt_i = H * (W - 1)
    area_ref = cnt_b * area_b + cnt_i * area_i
    leakage_ref = cnt_b * leakage_b + cnt_i * leakage_i
    dynamic_ref = cnt_b * dynamic_b + cnt_i * dynamic_i
    area, leakage, dynamic = profile(path=path, computing=computing, prefix="array_"+str(H))
    area_r = area / area_ref
    leakage_r = leakage / leakage_ref
    dynamic_r = dynamic / dynamic_ref
    area_out = np.append(area_out, area_r)
    leakage_out = np.append(leakage_out, leakage_r)
    dynamic_out = np.append(dynamic_out, dynamic_r)

    # array_32
    H = 32
    W = 32
    cnt_b = H
    cnt_i = H * (W - 1)
    area_ref = cnt_b * area_b + cnt_i * area_i
    leakage_ref = cnt_b * leakage_b + cnt_i * leakage_i
    dynamic_ref = cnt_b * dynamic_b + cnt_i * dynamic_i
    area, leakage, dynamic = profile(path=path, computing=computing, prefix="array_"+str(H))
    area_r = area / area_ref
    leakage_r = leakage / leakage_ref
    dynamic_r = dynamic / dynamic_ref
    area_out = np.append(area_out, area_r)
    leakage_out = np.append(leakage_out, leakage_r)
    dynamic_out = np.append(dynamic_out, dynamic_r)

    area_reg = LinearRegression()
    area_reg.fit(input, area_out)
    # not sure why this regression can keep identy for the mid value
    assert area_reg.predict(input)[2] - area_out[2] < 0.00001
    reg_log += "Area:\t"
    reg_log += str(area_reg.coef_[0]) + ",\t" + str(area_reg.coef_[1]) + ",\t" + str(area_reg.intercept_) + ",\t" + str(area_b/total_area[0]) + ",\t" + str(area_i/total_area[1]) + ",\t\n"

    leakage_reg = LinearRegression()
    leakage_reg.fit(input, leakage_out)
    assert leakage_reg.predict(input)[2] - leakage_out[2] < 0.00001
    reg_log += "Leakage:\t"
    reg_log += str(leakage_reg.coef_[0]) + ",\t" + str(leakage_reg.coef_[1]) + ",\t" + str(leakage_reg.intercept_) + ",\t" + str(leakage_b/total_leakage[0]) + ",\t" + str(leakage_i/total_leakage[1]) + ",\t\n"

    dynamic_reg = LinearRegression()
    dynamic_reg.fit(input, dynamic_out)
    assert dynamic_reg.predict(input)[2] - dynamic_out[2] < 0.00001
    reg_log += "Dynamic:\t"
    reg_log += str(dynamic_reg.coef_[0]) + ",\t" + str(dynamic_reg.coef_[1]) + ",\t" + str(dynamic_reg.intercept_) + ",\t" + str(dynamic_b/total_dynamic[0]) + ",\t" + str(dynamic_i/total_dynamic[1]) + ",\t\n\n"

    return reg_log


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
    # pe_config_gen(path="./45nm_rvt/8bit", frequency=400)
    # pe_config_gen(path="./45nm_rvt/16bit", frequency=400)