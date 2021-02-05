import evaluate
import os

def gen_run_config(tech_node=None):

    arch_list = ["tpu", "eyeriss"]
    network_list = ["alexnet"]
    # network_list = ["test"]
    bit_list = ["8", "16"]
    cycle_list = ["32", "64", "128", "256"]
    ram_list = ["ddr3_w__spm", "ddr3_wo_spm"]

    for a in arch_list:
        for b in bit_list:
            # unary rate
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
                                elems[1] = "UnaryRate"
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
                                cfg_log += entry + "\n"
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
                                cfg_log += entry + "\n"
                        cfg_file.close()
                        cfg_file = open("./config/" + path + "/sram.cfg", "w")
                        cfg_file.write(cfg_log)
                        cfg_file.close()

                        # no need to change pe.cfg and dram.cfg
                        # get pe.cfg
                        if b == "8":
                            cmd = "cp ./synthesis/" + tech_node + "/8bit/pe.cfg " + "./config/" + path
                            os.system(cmd)
                        elif b == "16":
                            cmd = "cp ./synthesis/" + tech_node + "/16bit/pe.cfg " + "./config/" + path
                            os.system(cmd)
                        else:
                            raise ValueError("Unknown word bit setting.")
                        
                        # get dram.cfg
                        cmd = "cp ./config_src/memory_config/dram.cfg " + "./config/" + path
                        os.system(cmd)
            
            # unary temporal
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
                                elems[1] = "UnaryTemporal"
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
                                cfg_log += entry + "\n"
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
                                cfg_log += entry + "\n"
                        cfg_file.close()
                        cfg_file = open("./config/" + path + "/sram.cfg", "w")
                        cfg_file.write(cfg_log)
                        cfg_file.close()

                        # no need to change pe.cfg and dram.cfg
                        # get pe.cfg
                        if b == "8":
                            cmd = "cp ./synthesis/" + tech_node + "/8bit/pe.cfg " + "./config/" + path
                            os.system(cmd)
                        elif b == "16":
                            cmd = "cp ./synthesis/" + tech_node + "/16bit/pe.cfg " + "./config/" + path
                            os.system(cmd)
                        else:
                            raise ValueError("Unknown word bit setting.")
                        
                        # get dram.cfg
                        cmd = "cp ./config_src/memory_config/dram.cfg " + "./config/" + path
                        os.system(cmd)
            
            # binary serial
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
                            elems[1] = "BinarySerial"
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
                            cfg_log += entry + "\n"
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
                            cfg_log += entry + "\n"
                    cfg_file.close()
                    cfg_file = open("./config/" + path + "/sram.cfg", "w")
                    cfg_file.write(cfg_log)
                    cfg_file.close()

                    # no need to change pe.cfg and dram.cfg
                    # get pe.cfg
                    if b == "8":
                        cmd = "cp ./synthesis/" + tech_node + "/8bit/pe.cfg " + "./config/" + path
                        os.system(cmd)
                    elif b == "16":
                        cmd = "cp ./synthesis/" + tech_node + "/16bit/pe.cfg " + "./config/" + path
                        os.system(cmd)
                    else:
                        raise ValueError("Unknown word bit setting.")
                    
                    # get dram.cfg
                    cmd = "cp ./config_src/memory_config/dram.cfg " + "./config/" + path
                    os.system(cmd)
        
            # binary parallel
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
                            elems[1] = "BinaryParallel"
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
                            cfg_log += entry + "\n"
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
                            cfg_log += entry + "\n"
                    cfg_file.close()
                    cfg_file = open("./config/" + path + "/sram.cfg", "w")
                    cfg_file.write(cfg_log)
                    cfg_file.close()

                    # no need to change pe.cfg and dram.cfg
                    # get pe.cfg
                    if b == "8":
                        cmd = "cp ./synthesis/" + tech_node + "/8bit/pe.cfg " + "./config/" + path
                        os.system(cmd)
                    elif b == "16":
                        cmd = "cp ./synthesis/" + tech_node + "/16bit/pe.cfg " + "./config/" + path
                        os.system(cmd)
                    else:
                        raise ValueError("Unknown word bit setting.")
                    
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
    # gen_run_config(tech_node="32nm_rvt")
    gen_run_config(tech_node="45nm_rvt")
