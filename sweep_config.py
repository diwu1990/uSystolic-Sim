import evaluate
import os
import configparser as cp
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

def gen_run_config(tech_node=None):

    arch_list = ["tpu", "eyeriss"]
    network_list = ["alexnet"]
    bit_list = ["8", "16"]
    cycle_list = ["32", "64", "128"]
    ram_list = ["ddr3_w__spm", "ddr3_wo_spm"]

    for a in arch_list:
        for b in bit_list:
            # unary rate
            str_flag = "UnaryRate"
            computing = "ur"
            for c in cycle_list:
                for n in network_list:
                    for r in ram_list:
                        path = a + "_" + b.zfill(2) + "b_" + computing + "_" + c.zfill(3) + "c_" + n + "_" + r
                        print(path)
                        if not os.path.exists("./config/" + path):
                            os.system("mkdir ./config/" + path)
                        cmd = "cp ./config_src/network_config/" + n + "/network.csv " + "./config/" + path
                        os.system(cmd)
                        
                        cfg_log = ""
                        cfg_file = open("./config/" + path + "/network.csv", "r")
                        first = True
                        for entry in cfg_file:
                            if first == True:
                                cfg_log += entry
                                first = False
                                continue
                            elems = entry.strip().split(',')
                            elems = prune(elems)
                            if len(elems) == 11:
                                elems[10] = c
                            for e in elems:
                                cfg_log += e + ",\t"
                            cfg_log += "\n"
                        cfg_file.close()
                        cfg_file = open("./config/" + path + "/network.csv", "w")
                        cfg_file.write(cfg_log)
                        cfg_file.close()
                        
                        # get systolic.cfg
                        cmd = "cp ./config_src/systolic_config/" + a + "/systolic.cfg " + "./config/" + path
                        os.system(cmd)

                        cfg_log = ""
                        cfg_file = open("./config/" + path + "/systolic.cfg", "r")
                        for entry in cfg_file:
                            elems = entry.strip().split(':')
                            elems = prune(elems)
                            if len(elems) == 2 and elems[0] == "WordByte":
                                elems[1] = str(float(b) / 8)
                            if len(elems) == 2 and elems[0] == "Computing":
                                elems[1] = str_flag
                            if len(elems) == 2 and (elems[0] == "ZeroIfmapSram" or elems[0] == "ZeroFilterSram" or elems[0] == "ZeroOfmapSram"):
                                if r == "ddr3_w__spm":
                                    elems[1] = "False"
                                elif r == "ddr3_wo_spm":
                                    elems[1] = "True"
                                else:
                                    raise ValueError("Unknown sram setting.")
                            
                            if len(elems) == 2:
                                cfg_log += elems[0] + ":\t" + elems[1] + "\n"
                            else:
                                cfg_log += entry
                        cfg_file.close()
                        cfg_file = open("./config/" + path + "/systolic.cfg", "w")
                        cfg_file.write(cfg_log)
                        cfg_file.close()

                        # get sram.cfg
                        cmd = "cp ./config_src/memory_config/sram.cfg " + "./config/" + path
                        os.system(cmd)

                        cfg_log = ""
                        cfg_file = open("./config/" + path + "/sram.cfg", "r")
                        for entry in cfg_file:
                            elems = entry.strip().split(' ')
                            elems = prune(elems)
                            if len(elems) == 3 and elems[0] == "-technology" and elems[1] == "(u)":
                                if tech_node == "32nm_rvt":
                                    elems[2] = str(0.032)
                                elif tech_node == "45nm_rvt":
                                    elems[2] = str(0.045)
                                else:
                                    raise ValueError("Unknown sram tech node.")
                            
                            if len(elems) == 3:
                                cfg_log += elems[0] + " " + elems[1] + " " + elems[2] + "\n"
                            else:
                                cfg_log += entry
                        cfg_file.close()
                        cfg_file = open("./config/" + path + "/sram.cfg", "w")
                        cfg_file.write(cfg_log)
                        cfg_file.close()

                        # get pe.cfg
                        if b == "8":
                            cmd = "cp ./synthesis/" + tech_node + "/8bit/*.cfg " + "./config/" + path
                            os.system(cmd)
                        elif b == "16":
                            cmd = "cp ./synthesis/" + tech_node + "/16bit/*.cfg " + "./config/" + path
                            os.system(cmd)
                        else:
                            raise ValueError("Unknown word bit setting.")
                        
                        # parse regression file
                        if a == "eyeriss":
                            H = np.log2(12)
                            W = np.log2(14)
                        elif a == "tpu":
                            H = np.log2(256)
                            W = np.log2(256)
                        else:
                            raise ValueError("Unknown arch.")
                        config = cp.ConfigParser()
                        config.read("./config/" + path + "/regression.cfg")
                        area_params = config.get(str_flag, 'Area').split(',')
                        area_reg = LinearRegression()
                        area_reg.coef_ = np.array([float(area_params[0].strip()), float(area_params[1].strip())])
                        area_reg.intercept_ = float(area_params[2].strip())
                        area_b_scale = float(area_params[3].strip()) * area_reg.predict([[H, W]])[0]
                        area_i_scale = float(area_params[4].strip()) * area_reg.predict([[H, W]])[0]

                        leakage_params = config.get(str_flag, 'Leakage').split(',')
                        leakage_reg = LinearRegression()
                        leakage_reg.coef_ = np.array([float(leakage_params[0].strip()), float(leakage_params[1].strip())])
                        leakage_reg.intercept_ = float(leakage_params[2].strip())
                        leakage_b_scale = float(leakage_params[3].strip()) * leakage_reg.predict([[H, W]])[0]
                        leakage_i_scale = float(leakage_params[4].strip()) * leakage_reg.predict([[H, W]])[0]

                        dynamic_params = config.get(str_flag, 'Dynamic').split(',')
                        dynamic_reg = LinearRegression()
                        dynamic_reg.coef_ = np.array([float(dynamic_params[0].strip()), float(dynamic_params[1].strip())])
                        dynamic_reg.intercept_ = float(dynamic_params[2].strip())
                        dynamic_b_scale = float(dynamic_params[3].strip()) * dynamic_reg.predict([[H, W]])[0]
                        dynamic_i_scale = float(dynamic_params[4].strip()) * dynamic_reg.predict([[H, W]])[0]
                        
                        cfg_log = ""
                        cfg_file = open("./config/" + path + "/pe.cfg", "r")
                        find_flag = False
                        done_flag = False
                        for entry in cfg_file:
                            if done_flag == False:
                                elems = prune(entry.strip().split(':'))
                                if len(elems) == 2:
                                    elems = elems[:1] + prune(elems[1].strip().split(','))
                                if len(elems) > 0 and find_flag == False:
                                    if elems[0] == "[" + str_flag + "]":
                                        find_flag = True
                                        cfg_log += entry
                                    else:
                                        cfg_log += entry
                                elif find_flag == True and len(elems) > 0:
                                    if elems[0] == "IREG":
                                        cfg_log += elems[0] + ":\t" + \
                                                    str(float(elems[1]) * area_b_scale) + ",\t" + str(float(elems[2]) * leakage_b_scale) + ",\t" + str(float(elems[3]) * dynamic_b_scale) + ",\t" + \
                                                    str(float(elems[4]) * area_i_scale) + ",\t" + str(float(elems[5]) * leakage_i_scale) + ",\t" + str(float(elems[6]) * dynamic_i_scale) + ",\t\n" 
                                    elif elems[0] == "WREG":
                                        cfg_log += elems[0] + ":\t" + \
                                                    str(float(elems[1]) * area_b_scale) + ",\t" + str(float(elems[2]) * leakage_b_scale) + ",\t" + str(float(elems[3]) * dynamic_b_scale) + ",\t" + \
                                                    str(float(elems[4]) * area_i_scale) + ",\t" + str(float(elems[5]) * leakage_i_scale) + ",\t" + str(float(elems[6]) * dynamic_i_scale) + ",\t\n" 
                                    elif elems[0] == "MUL":
                                        cfg_log += elems[0] + ":\t" + \
                                                    str(float(elems[1]) * area_b_scale) + ",\t" + str(float(elems[2]) * leakage_b_scale) + ",\t" + str(float(elems[3]) * dynamic_b_scale) + ",\t" + \
                                                    str(float(elems[4]) * area_i_scale) + ",\t" + str(float(elems[5]) * leakage_i_scale) + ",\t" + str(float(elems[6]) * dynamic_i_scale) + ",\t\n" 
                                    elif elems[0] == "ACC":
                                        cfg_log += elems[0] + ":\t" + \
                                                    str(float(elems[1]) * area_b_scale) + ",\t" + str(float(elems[2]) * leakage_b_scale) + ",\t" + str(float(elems[3]) * dynamic_b_scale) + ",\t" + \
                                                    str(float(elems[4]) * area_i_scale) + ",\t" + str(float(elems[5]) * leakage_i_scale) + ",\t" + str(float(elems[6]) * dynamic_i_scale) + ",\t\n" 
                                    else:
                                        raise ValueError("Unknown parameters in pe.cfg.")
                                elif find_flag == True and len(elems) == 0:
                                    find_flag = False
                                    done_flag = False
                                    cfg_log += entry
                                else:
                                    cfg_log += entry
                            else:
                                cfg_log += entry
                        cfg_file.close()
                        cfg_file = open("./config/" + path + "/pe.cfg", "w")
                        cfg_file.write(cfg_log)
                        cfg_file.close()

                        cmd = "rm ./config/" + path + "/regression.cfg"
                        os.system(cmd)
                        
                        # no need to change dram.cfg
                        # get dram.cfg
                        cmd = "cp ./config_src/memory_config/dram.cfg " + "./config/" + path
                        os.system(cmd)
            
            # unary temporal
            str_flag = "UnaryTemporal"
            computing = "ut"
            for c in cycle_list:
                for n in network_list:
                    for r in ram_list:
                        path = a + "_" + b.zfill(2) + "b_" + computing + "_" + c.zfill(3) + "c_" + n + "_" + r
                        print(path)
                        if not os.path.exists("./config/" + path):
                            os.system("mkdir ./config/" + path)
                        cmd = "cp ./config_src/network_config/" + n + "/network.csv " + "./config/" + path
                        os.system(cmd)
                        
                        cfg_log = ""
                        cfg_file = open("./config/" + path + "/network.csv", "r")
                        first = True
                        for entry in cfg_file:
                            if first == True:
                                cfg_log += entry
                                first = False
                                continue
                            elems = entry.strip().split(',')
                            elems = prune(elems)
                            if len(elems) == 11:
                                elems[10] = c
                            for e in elems:
                                cfg_log += e + ",\t"
                            cfg_log += "\n"
                        cfg_file.close()
                        cfg_file = open("./config/" + path + "/network.csv", "w")
                        cfg_file.write(cfg_log)
                        cfg_file.close()
                        
                        # get systolic.cfg
                        cmd = "cp ./config_src/systolic_config/" + a + "/systolic.cfg " + "./config/" + path
                        os.system(cmd)

                        cfg_log = ""
                        cfg_file = open("./config/" + path + "/systolic.cfg", "r")
                        for entry in cfg_file:
                            elems = entry.strip().split(':')
                            elems = prune(elems)
                            if len(elems) == 2 and elems[0] == "WordByte":
                                elems[1] = str(float(b) / 8)
                            if len(elems) == 2 and elems[0] == "Computing":
                                elems[1] = str_flag
                            if len(elems) == 2 and (elems[0] == "ZeroIfmapSram" or elems[0] == "ZeroFilterSram" or elems[0] == "ZeroOfmapSram"):
                                if r == "ddr3_w__spm":
                                    elems[1] = "False"
                                elif r == "ddr3_wo_spm":
                                    elems[1] = "True"
                                else:
                                    raise ValueError("Unknown sram setting.")
                            
                            if len(elems) == 2:
                                cfg_log += elems[0] + ":\t" + elems[1] + "\n"
                            else:
                                cfg_log += entry
                        cfg_file.close()
                        cfg_file = open("./config/" + path + "/systolic.cfg", "w")
                        cfg_file.write(cfg_log)
                        cfg_file.close()

                        # get sram.cfg
                        cmd = "cp ./config_src/memory_config/sram.cfg " + "./config/" + path
                        os.system(cmd)

                        cfg_log = ""
                        cfg_file = open("./config/" + path + "/sram.cfg", "r")
                        for entry in cfg_file:
                            elems = entry.strip().split(' ')
                            elems = prune(elems)
                            if len(elems) == 3 and elems[0] == "-technology" and elems[1] == "(u)":
                                if tech_node == "32nm_rvt":
                                    elems[2] = str(0.032)
                                elif tech_node == "45nm_rvt":
                                    elems[2] = str(0.045)
                                else:
                                    raise ValueError("Unknown sram tech node.")
                            
                            if len(elems) == 3:
                                cfg_log += elems[0] + " " + elems[1] + " " + elems[2] + "\n"
                            else:
                                cfg_log += entry
                        cfg_file.close()
                        cfg_file = open("./config/" + path + "/sram.cfg", "w")
                        cfg_file.write(cfg_log)
                        cfg_file.close()

                        # get pe.cfg
                        if b == "8":
                            cmd = "cp ./synthesis/" + tech_node + "/8bit/*.cfg " + "./config/" + path
                            os.system(cmd)
                        elif b == "16":
                            cmd = "cp ./synthesis/" + tech_node + "/16bit/*.cfg " + "./config/" + path
                            os.system(cmd)
                        else:
                            raise ValueError("Unknown word bit setting.")
                        
                        # parse regression file
                        if a == "eyeriss":
                            H = np.log2(12)
                            W = np.log2(14)
                        elif a == "tpu":
                            H = np.log2(256)
                            W = np.log2(256)
                        else:
                            raise ValueError("Unknown arch.")
                        config = cp.ConfigParser()
                        config.read("./config/" + path + "/regression.cfg")
                        area_params = config.get(str_flag, 'Area').split(',')
                        area_reg = LinearRegression()
                        area_reg.coef_ = np.array([float(area_params[0].strip()), float(area_params[1].strip())])
                        area_reg.intercept_ = float(area_params[2].strip())
                        area_b_scale = float(area_params[3].strip()) * area_reg.predict([[H, W]])[0]
                        area_i_scale = float(area_params[4].strip()) * area_reg.predict([[H, W]])[0]

                        leakage_params = config.get(str_flag, 'Leakage').split(',')
                        leakage_reg = LinearRegression()
                        leakage_reg.coef_ = np.array([float(leakage_params[0].strip()), float(leakage_params[1].strip())])
                        leakage_reg.intercept_ = float(leakage_params[2].strip())
                        leakage_b_scale = float(leakage_params[3].strip()) * leakage_reg.predict([[H, W]])[0]
                        leakage_i_scale = float(leakage_params[4].strip()) * leakage_reg.predict([[H, W]])[0]

                        dynamic_params = config.get(str_flag, 'Dynamic').split(',')
                        dynamic_reg = LinearRegression()
                        dynamic_reg.coef_ = np.array([float(dynamic_params[0].strip()), float(dynamic_params[1].strip())])
                        dynamic_reg.intercept_ = float(dynamic_params[2].strip())
                        dynamic_b_scale = float(dynamic_params[3].strip()) * dynamic_reg.predict([[H, W]])[0]
                        dynamic_i_scale = float(dynamic_params[4].strip()) * dynamic_reg.predict([[H, W]])[0]
                        
                        cfg_log = ""
                        cfg_file = open("./config/" + path + "/pe.cfg", "r")
                        find_flag = False
                        done_flag = False
                        for entry in cfg_file:
                            if done_flag == False:
                                elems = prune(entry.strip().split(':'))
                                if len(elems) == 2:
                                    elems = elems[:1] + prune(elems[1].strip().split(','))
                                if len(elems) > 0 and find_flag == False:
                                    if elems[0] == "[" + str_flag + "]":
                                        find_flag = True
                                        cfg_log += entry
                                    else:
                                        cfg_log += entry
                                elif find_flag == True and len(elems) > 0:
                                    if elems[0] == "IREG":
                                        cfg_log += elems[0] + ":\t" + \
                                                    str(float(elems[1]) * area_b_scale) + ",\t" + str(float(elems[2]) * leakage_b_scale) + ",\t" + str(float(elems[3]) * dynamic_b_scale) + ",\t" + \
                                                    str(float(elems[4]) * area_i_scale) + ",\t" + str(float(elems[5]) * leakage_i_scale) + ",\t" + str(float(elems[6]) * dynamic_i_scale) + ",\t\n" 
                                    elif elems[0] == "WREG":
                                        cfg_log += elems[0] + ":\t" + \
                                                    str(float(elems[1]) * area_b_scale) + ",\t" + str(float(elems[2]) * leakage_b_scale) + ",\t" + str(float(elems[3]) * dynamic_b_scale) + ",\t" + \
                                                    str(float(elems[4]) * area_i_scale) + ",\t" + str(float(elems[5]) * leakage_i_scale) + ",\t" + str(float(elems[6]) * dynamic_i_scale) + ",\t\n" 
                                    elif elems[0] == "MUL":
                                        cfg_log += elems[0] + ":\t" + \
                                                    str(float(elems[1]) * area_b_scale) + ",\t" + str(float(elems[2]) * leakage_b_scale) + ",\t" + str(float(elems[3]) * dynamic_b_scale) + ",\t" + \
                                                    str(float(elems[4]) * area_i_scale) + ",\t" + str(float(elems[5]) * leakage_i_scale) + ",\t" + str(float(elems[6]) * dynamic_i_scale) + ",\t\n" 
                                    elif elems[0] == "ACC":
                                        cfg_log += elems[0] + ":\t" + \
                                                    str(float(elems[1]) * area_b_scale) + ",\t" + str(float(elems[2]) * leakage_b_scale) + ",\t" + str(float(elems[3]) * dynamic_b_scale) + ",\t" + \
                                                    str(float(elems[4]) * area_i_scale) + ",\t" + str(float(elems[5]) * leakage_i_scale) + ",\t" + str(float(elems[6]) * dynamic_i_scale) + ",\t\n" 
                                    else:
                                        raise ValueError("Unknown parameters in pe.cfg.")
                                elif find_flag == True and len(elems) == 0:
                                    find_flag = False
                                    done_flag = False
                                    cfg_log += entry
                                else:
                                    cfg_log += entry
                            else:
                                cfg_log += entry
                        cfg_file.close()
                        cfg_file = open("./config/" + path + "/pe.cfg", "w")
                        cfg_file.write(cfg_log)
                        cfg_file.close()

                        cmd = "rm ./config/" + path + "/regression.cfg"
                        os.system(cmd)
                        
                        # no need to change dram.cfg
                        # get dram.cfg
                        cmd = "cp ./config_src/memory_config/dram.cfg " + "./config/" + path
                        os.system(cmd)
            
            # binary serial
            str_flag = "BinarySerial"
            computing = "bs"
            for n in network_list:
                for r in ram_list:
                    path = a + "_" + b.zfill(2) + "b_" + computing + "_" + b.zfill(3) + "c_" + n + "_" + r
                    print(path)
                    if not os.path.exists("./config/" + path):
                        os.system("mkdir ./config/" + path)
                    cmd = "cp ./config_src/network_config/" + n + "/network.csv " + "./config/" + path
                    os.system(cmd)
                    
                    cfg_log = ""
                    cfg_file = open("./config/" + path + "/network.csv", "r")
                    first = True
                    for entry in cfg_file:
                        if first == True:
                            cfg_log += entry
                            first = False
                            continue
                        elems = entry.strip().split(',')
                        elems = prune(elems)
                        if len(elems) == 11:
                            elems[10] = b
                        for e in elems:
                            cfg_log += e + ",\t"
                        cfg_log += "\n"
                    cfg_file.close()
                    cfg_file = open("./config/" + path + "/network.csv", "w")
                    cfg_file.write(cfg_log)
                    cfg_file.close()
                    
                    # get systolic.cfg
                    cmd = "cp ./config_src/systolic_config/" + a + "/systolic.cfg " + "./config/" + path
                    os.system(cmd)

                    cfg_log = ""
                    cfg_file = open("./config/" + path + "/systolic.cfg", "r")
                    for entry in cfg_file:
                        elems = entry.strip().split(':')
                        elems = prune(elems)
                        if len(elems) == 2 and elems[0] == "WordByte":
                            elems[1] = str(float(b) / 8)
                        if len(elems) == 2 and elems[0] == "Computing":
                            elems[1] = str_flag
                        if len(elems) == 2 and (elems[0] == "ZeroIfmapSram" or elems[0] == "ZeroFilterSram" or elems[0] == "ZeroOfmapSram"):
                            if r == "ddr3_w__spm":
                                elems[1] = "False"
                            elif r == "ddr3_wo_spm":
                                elems[1] = "True"
                            else:
                                raise ValueError("Unknown sram setting.")
                        
                        if len(elems) == 2:
                            cfg_log += elems[0] + ":\t" + elems[1] + "\n"
                        else:
                            cfg_log += entry
                    cfg_file.close()
                    cfg_file = open("./config/" + path + "/systolic.cfg", "w")
                    cfg_file.write(cfg_log)
                    cfg_file.close()

                    # get sram.cfg
                    cmd = "cp ./config_src/memory_config/sram.cfg " + "./config/" + path
                    os.system(cmd)

                    cfg_log = ""
                    cfg_file = open("./config/" + path + "/sram.cfg", "r")
                    for entry in cfg_file:
                        elems = entry.strip().split(' ')
                        elems = prune(elems)
                        if len(elems) == 3 and elems[0] == "-technology" and elems[1] == "(u)":
                            if tech_node == "32nm_rvt":
                                elems[2] = str(0.032)
                            elif tech_node == "45nm_rvt":
                                elems[2] = str(0.045)
                            else:
                                raise ValueError("Unknown sram tech node.")
                        
                        if len(elems) == 3:
                            cfg_log += elems[0] + " " + elems[1] + " " + elems[2] + "\n"
                        else:
                            cfg_log += entry
                    cfg_file.close()
                    cfg_file = open("./config/" + path + "/sram.cfg", "w")
                    cfg_file.write(cfg_log)
                    cfg_file.close()

                    # get pe.cfg
                    if b == "8":
                        cmd = "cp ./synthesis/" + tech_node + "/8bit/*.cfg " + "./config/" + path
                        os.system(cmd)
                    elif b == "16":
                        cmd = "cp ./synthesis/" + tech_node + "/16bit/*.cfg " + "./config/" + path
                        os.system(cmd)
                    else:
                        raise ValueError("Unknown word bit setting.")
                    
                    # parse regression file
                    if a == "eyeriss":
                        H = np.log2(12)
                        W = np.log2(14)
                    elif a == "tpu":
                        H = np.log2(256)
                        W = np.log2(256)
                    else:
                        raise ValueError("Unknown arch.")
                    config = cp.ConfigParser()
                    config.read("./config/" + path + "/regression.cfg")
                    area_params = config.get(str_flag, 'Area').split(',')
                    area_reg = LinearRegression()
                    area_reg.coef_ = np.array([float(area_params[0].strip()), float(area_params[1].strip())])
                    area_reg.intercept_ = float(area_params[2].strip())
                    area_b_scale = float(area_params[3].strip()) * area_reg.predict([[H, W]])[0]
                    area_i_scale = float(area_params[4].strip()) * area_reg.predict([[H, W]])[0]

                    leakage_params = config.get(str_flag, 'Leakage').split(',')
                    leakage_reg = LinearRegression()
                    leakage_reg.coef_ = np.array([float(leakage_params[0].strip()), float(leakage_params[1].strip())])
                    leakage_reg.intercept_ = float(leakage_params[2].strip())
                    leakage_b_scale = float(leakage_params[3].strip()) * leakage_reg.predict([[H, W]])[0]
                    leakage_i_scale = float(leakage_params[4].strip()) * leakage_reg.predict([[H, W]])[0]

                    dynamic_params = config.get(str_flag, 'Dynamic').split(',')
                    dynamic_reg = LinearRegression()
                    dynamic_reg.coef_ = np.array([float(dynamic_params[0].strip()), float(dynamic_params[1].strip())])
                    dynamic_reg.intercept_ = float(dynamic_params[2].strip())
                    dynamic_b_scale = float(dynamic_params[3].strip()) * dynamic_reg.predict([[H, W]])[0]
                    dynamic_i_scale = float(dynamic_params[4].strip()) * dynamic_reg.predict([[H, W]])[0]
                    
                    cfg_log = ""
                    cfg_file = open("./config/" + path + "/pe.cfg", "r")
                    find_flag = False
                    done_flag = False
                    for entry in cfg_file:
                        if done_flag == False:
                            elems = prune(entry.strip().split(':'))
                            if len(elems) == 2:
                                elems = elems[:1] + prune(elems[1].strip().split(','))
                            if len(elems) > 0 and find_flag == False:
                                if elems[0] == "[" + str_flag + "]":
                                    find_flag = True
                                    cfg_log += entry
                                else:
                                    cfg_log += entry
                            elif find_flag == True and len(elems) > 0:
                                if elems[0] == "IREG":
                                    cfg_log += elems[0] + ":\t" + \
                                                str(float(elems[1]) * area_b_scale) + ",\t" + str(float(elems[2]) * leakage_b_scale) + ",\t" + str(float(elems[3]) * dynamic_b_scale) + ",\t" + \
                                                str(float(elems[4]) * area_i_scale) + ",\t" + str(float(elems[5]) * leakage_i_scale) + ",\t" + str(float(elems[6]) * dynamic_i_scale) + ",\t\n" 
                                elif elems[0] == "WREG":
                                    cfg_log += elems[0] + ":\t" + \
                                                str(float(elems[1]) * area_b_scale) + ",\t" + str(float(elems[2]) * leakage_b_scale) + ",\t" + str(float(elems[3]) * dynamic_b_scale) + ",\t" + \
                                                str(float(elems[4]) * area_i_scale) + ",\t" + str(float(elems[5]) * leakage_i_scale) + ",\t" + str(float(elems[6]) * dynamic_i_scale) + ",\t\n" 
                                elif elems[0] == "MUL":
                                    cfg_log += elems[0] + ":\t" + \
                                                str(float(elems[1]) * area_b_scale) + ",\t" + str(float(elems[2]) * leakage_b_scale) + ",\t" + str(float(elems[3]) * dynamic_b_scale) + ",\t" + \
                                                str(float(elems[4]) * area_i_scale) + ",\t" + str(float(elems[5]) * leakage_i_scale) + ",\t" + str(float(elems[6]) * dynamic_i_scale) + ",\t\n" 
                                elif elems[0] == "ACC":
                                    cfg_log += elems[0] + ":\t" + \
                                                str(float(elems[1]) * area_b_scale) + ",\t" + str(float(elems[2]) * leakage_b_scale) + ",\t" + str(float(elems[3]) * dynamic_b_scale) + ",\t" + \
                                                str(float(elems[4]) * area_i_scale) + ",\t" + str(float(elems[5]) * leakage_i_scale) + ",\t" + str(float(elems[6]) * dynamic_i_scale) + ",\t\n" 
                                else:
                                    raise ValueError("Unknown parameters in pe.cfg.")
                            elif find_flag == True and len(elems) == 0:
                                find_flag = False
                                done_flag = False
                                cfg_log += entry
                            else:
                                cfg_log += entry
                        else:
                            cfg_log += entry
                    cfg_file.close()
                    cfg_file = open("./config/" + path + "/pe.cfg", "w")
                    cfg_file.write(cfg_log)
                    cfg_file.close()

                    cmd = "rm ./config/" + path + "/regression.cfg"
                    os.system(cmd)
                    
                    # no need to change dram.cfg
                    # get dram.cfg
                    cmd = "cp ./config_src/memory_config/dram.cfg " + "./config/" + path
                    os.system(cmd)
        
            # binary parallel
            str_flag = "BinaryParallel"
            computing = "bp"
            for n in network_list:
                for r in ram_list:
                    path = a + "_" + b.zfill(2) + "b_" + computing + "_" + "001c_" + n + "_" + r
                    print(path)
                    if not os.path.exists("./config/" + path):
                        os.system("mkdir ./config/" + path)
                    cmd = "cp ./config_src/network_config/" + n + "/network.csv " + "./config/" + path
                    os.system(cmd)
                    
                    cfg_log = ""
                    cfg_file = open("./config/" + path + "/network.csv", "r")
                    first = True
                    for entry in cfg_file:
                        if first == True:
                            cfg_log += entry
                            first = False
                            continue
                        elems = entry.strip().split(',')
                        elems = prune(elems)
                        if len(elems) == 11:
                            elems[10] = "1"
                        for e in elems:
                            cfg_log += e + ",\t"
                        cfg_log += "\n"
                    cfg_file.close()
                    cfg_file = open("./config/" + path + "/network.csv", "w")
                    cfg_file.write(cfg_log)
                    cfg_file.close()
                    
                    # get systolic.cfg
                    cmd = "cp ./config_src/systolic_config/" + a + "/systolic.cfg " + "./config/" + path
                    os.system(cmd)

                    cfg_log = ""
                    cfg_file = open("./config/" + path + "/systolic.cfg", "r")
                    for entry in cfg_file:
                        elems = entry.strip().split(':')
                        elems = prune(elems)
                        if len(elems) == 2 and elems[0] == "WordByte":
                            elems[1] = str(float(b) / 8)
                        if len(elems) == 2 and elems[0] == "Computing":
                            elems[1] = str_flag
                        if len(elems) == 2 and (elems[0] == "ZeroIfmapSram" or elems[0] == "ZeroFilterSram" or elems[0] == "ZeroOfmapSram"):
                            if r == "ddr3_w__spm":
                                elems[1] = "False"
                            elif r == "ddr3_wo_spm":
                                elems[1] = "True"
                            else:
                                raise ValueError("Unknown sram setting.")
                        
                        if len(elems) == 2:
                            cfg_log += elems[0] + ":\t" + elems[1] + "\n"
                        else:
                            cfg_log += entry
                    cfg_file.close()
                    cfg_file = open("./config/" + path + "/systolic.cfg", "w")
                    cfg_file.write(cfg_log)
                    cfg_file.close()

                    # get sram.cfg
                    cmd = "cp ./config_src/memory_config/sram.cfg " + "./config/" + path
                    os.system(cmd)

                    cfg_log = ""
                    cfg_file = open("./config/" + path + "/sram.cfg", "r")
                    for entry in cfg_file:
                        elems = entry.strip().split(' ')
                        elems = prune(elems)
                        if len(elems) == 3 and elems[0] == "-technology" and elems[1] == "(u)":
                            if tech_node == "32nm_rvt":
                                elems[2] = str(0.032)
                            elif tech_node == "45nm_rvt":
                                elems[2] = str(0.045)
                            else:
                                raise ValueError("Unknown sram tech node.")
                        
                        if len(elems) == 3:
                            cfg_log += elems[0] + " " + elems[1] + " " + elems[2] + "\n"
                        else:
                            cfg_log += entry
                    cfg_file.close()
                    cfg_file = open("./config/" + path + "/sram.cfg", "w")
                    cfg_file.write(cfg_log)
                    cfg_file.close()

                    # get pe.cfg
                    if b == "8":
                        cmd = "cp ./synthesis/" + tech_node + "/8bit/*.cfg " + "./config/" + path
                        os.system(cmd)
                    elif b == "16":
                        cmd = "cp ./synthesis/" + tech_node + "/16bit/*.cfg " + "./config/" + path
                        os.system(cmd)
                    else:
                        raise ValueError("Unknown word bit setting.")
                    
                    # parse regression file
                    if a == "eyeriss":
                        H = np.log2(12)
                        W = np.log2(14)
                    elif a == "tpu":
                        H = np.log2(256)
                        W = np.log2(256)
                    else:
                        raise ValueError("Unknown arch.")
                    config = cp.ConfigParser()
                    config.read("./config/" + path + "/regression.cfg")
                    area_params = config.get(str_flag, 'Area').split(',')
                    area_reg = LinearRegression()
                    area_reg.coef_ = np.array([float(area_params[0].strip()), float(area_params[1].strip())])
                    area_reg.intercept_ = float(area_params[2].strip())
                    area_b_scale = float(area_params[3].strip()) * area_reg.predict([[H, W]])[0]
                    area_i_scale = float(area_params[4].strip()) * area_reg.predict([[H, W]])[0]

                    leakage_params = config.get(str_flag, 'Leakage').split(',')
                    leakage_reg = LinearRegression()
                    leakage_reg.coef_ = np.array([float(leakage_params[0].strip()), float(leakage_params[1].strip())])
                    leakage_reg.intercept_ = float(leakage_params[2].strip())
                    leakage_b_scale = float(leakage_params[3].strip()) * leakage_reg.predict([[H, W]])[0]
                    leakage_i_scale = float(leakage_params[4].strip()) * leakage_reg.predict([[H, W]])[0]

                    dynamic_params = config.get(str_flag, 'Dynamic').split(',')
                    dynamic_reg = LinearRegression()
                    dynamic_reg.coef_ = np.array([float(dynamic_params[0].strip()), float(dynamic_params[1].strip())])
                    dynamic_reg.intercept_ = float(dynamic_params[2].strip())
                    dynamic_b_scale = float(dynamic_params[3].strip()) * dynamic_reg.predict([[H, W]])[0]
                    dynamic_i_scale = float(dynamic_params[4].strip()) * dynamic_reg.predict([[H, W]])[0]
                    
                    cfg_log = ""
                    cfg_file = open("./config/" + path + "/pe.cfg", "r")
                    find_flag = False
                    done_flag = False
                    for entry in cfg_file:
                        if done_flag == False:
                            elems = prune(entry.strip().split(':'))
                            if len(elems) == 2:
                                elems = elems[:1] + prune(elems[1].strip().split(','))
                            if len(elems) > 0 and find_flag == False:
                                if elems[0] == "[" + str_flag + "]":
                                    find_flag = True
                                    cfg_log += entry
                                else:
                                    cfg_log += entry
                            elif find_flag == True and len(elems) > 0:
                                if elems[0] == "IREG":
                                    cfg_log += elems[0] + ":\t" + \
                                                str(float(elems[1]) * area_b_scale) + ",\t" + str(float(elems[2]) * leakage_b_scale) + ",\t" + str(float(elems[3]) * dynamic_b_scale) + ",\t" + \
                                                str(float(elems[4]) * area_i_scale) + ",\t" + str(float(elems[5]) * leakage_i_scale) + ",\t" + str(float(elems[6]) * dynamic_i_scale) + ",\t\n" 
                                elif elems[0] == "WREG":
                                    cfg_log += elems[0] + ":\t" + \
                                                str(float(elems[1]) * area_b_scale) + ",\t" + str(float(elems[2]) * leakage_b_scale) + ",\t" + str(float(elems[3]) * dynamic_b_scale) + ",\t" + \
                                                str(float(elems[4]) * area_i_scale) + ",\t" + str(float(elems[5]) * leakage_i_scale) + ",\t" + str(float(elems[6]) * dynamic_i_scale) + ",\t\n" 
                                elif elems[0] == "MUL":
                                    cfg_log += elems[0] + ":\t" + \
                                                str(float(elems[1]) * area_b_scale) + ",\t" + str(float(elems[2]) * leakage_b_scale) + ",\t" + str(float(elems[3]) * dynamic_b_scale) + ",\t" + \
                                                str(float(elems[4]) * area_i_scale) + ",\t" + str(float(elems[5]) * leakage_i_scale) + ",\t" + str(float(elems[6]) * dynamic_i_scale) + ",\t\n" 
                                elif elems[0] == "ACC":
                                    cfg_log += elems[0] + ":\t" + \
                                                str(float(elems[1]) * area_b_scale) + ",\t" + str(float(elems[2]) * leakage_b_scale) + ",\t" + str(float(elems[3]) * dynamic_b_scale) + ",\t" + \
                                                str(float(elems[4]) * area_i_scale) + ",\t" + str(float(elems[5]) * leakage_i_scale) + ",\t" + str(float(elems[6]) * dynamic_i_scale) + ",\t\n" 
                                else:
                                    raise ValueError("Unknown parameters in pe.cfg.")
                            elif find_flag == True and len(elems) == 0:
                                find_flag = False
                                done_flag = False
                                cfg_log += entry
                            else:
                                cfg_log += entry
                        else:
                            cfg_log += entry
                    cfg_file.close()
                    cfg_file = open("./config/" + path + "/pe.cfg", "w")
                    cfg_file.write(cfg_log)
                    cfg_file.close()

                    cmd = "rm ./config/" + path + "/regression.cfg"
                    os.system(cmd)
                    
                    # no need to change dram.cfg
                    # get dram.cfg
                    cmd = "cp ./config_src/memory_config/dram.cfg " + "./config/" + path
                    os.system(cmd)

    
def prune(input_list):
    l = []

    for e in input_list:
        e = e.strip() # remove the leading and trailing characters, here space
        if e != '' and e != ' ':
            l.append(e)

    return l


if __name__ == '__main__':
    gen_run_config(tech_node="32nm_rvt")
    # gen_run_config(tech_node="45nm_rvt")
