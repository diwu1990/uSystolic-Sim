import os
import matplotlib.pyplot as plt
import numpy as np
import math

def plot_fig(technode=""):
    
    yscale = "linear"

    if not os.path.exists("./outputs_fig/"):
        os.system("mkdir ./outputs_fig")

    arch_list = ["tpu", "eyeriss"]
    network_list = ["alexnet"]
    bit_list = ["8", "16"]
    cycle_list = ["32", "64", "128", "256"]
    ram_list = ["ddr3_w__spm", "ddr3_wo_spm"]

    

    for a in arch_list:
        bw_list = []
        time_list = []
        tp_list = []
        area_list = []
        power_list = []
        energy_list = []
        if a == "tpu":
            a_cap = "TPU"
        else:
            a_cap = "Eyeriss"

        print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ")
        print("Processing " + a + ":")
        print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ")
        
        for b in bit_list:
            for n in network_list:
                for r in ram_list:
                    # binary parallel
                    computing = "bp"
                    name = a + "_" + b.zfill(2) + "b_" + computing + "_" + "001c_" + n + "_" + r
                    if not os.path.exists("./outputs/" + technode + "/" + name):
                        raise ValueError("Folder ./outputs/" + technode + "/" + name + " does not exist.")
                    
                    path = "./outputs/" + technode + "/" + name + "/simHwOut/"
                    bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=6)) # dram bw
                    bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=11)) # sram bw
                    time_list.append(return_indexed_elems(  input_csv=path + name + "_throughput_real.csv", index=3)) # runtime
                    tp_list.append(return_indexed_elems(    input_csv=path + name + "_throughput_real.csv", index=4)) # throughput
                    
                    path = "./outputs/" + technode + "/" + name + "/simEffOut/"
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=9)) # sa ireg area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=10)) # sa wreg area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=11)) # sa mul area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=12)) # sa acc area
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=6)) # dram
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=11)) # sram D
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=15)) # sram L
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=31)) # sa
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=6)) # dram
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=11)) # sram D
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=15)) # sram L
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=31)) # sa
                    
                    # binary serial
                    computing = "bs"
                    name = a + "_" + b.zfill(2) + "b_" + computing + "_" + b.zfill(3) + "c_" + n + "_" + r
                    if not os.path.exists("./outputs/" + technode + "/" + name):
                        raise ValueError("Folder ./outputs/" + technode + "/" + name + " does not exist.")
                    
                    path = "./outputs/" + technode + "/" + name + "/simHwOut/"
                    bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=6)) # dram bw
                    bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=11)) # sram bw
                    time_list.append(return_indexed_elems(  input_csv=path + name + "_throughput_real.csv", index=3)) # runtime
                    tp_list.append(return_indexed_elems(    input_csv=path + name + "_throughput_real.csv", index=4)) # throughput
                    
                    path = "./outputs/" + technode + "/" + name + "/simEffOut/"
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=9)) # sa ireg area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=10)) # sa wreg area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=11)) # sa mul area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=12)) # sa acc area
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=6)) # dram
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=11)) # sram D
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=15)) # sram L
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=31)) # sa
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=6)) # dram
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=11)) # sram D
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=15)) # sram L
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=31)) # sa

                    # unary rate
                    computing = "ur"
                    for c in cycle_list:
                        name = a + "_" + b.zfill(2) + "b_" + computing + "_" + c.zfill(3) + "c_" + n + "_" + r
                        if not os.path.exists("./outputs/" + technode + "/" + name):
                            raise ValueError("Folder ./outputs/" + technode + "/" + name + " does not exist.")
                        
                        path = "./outputs/" + technode + "/" + name + "/simHwOut/"
                        bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=6)) # dram bw
                        bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=11)) # sram bw
                        time_list.append(return_indexed_elems(  input_csv=path + name + "_throughput_real.csv", index=3)) # runtime
                        tp_list.append(return_indexed_elems(    input_csv=path + name + "_throughput_real.csv", index=4)) # throughput
                        
                        path = "./outputs/" + technode + "/" + name + "/simEffOut/"
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=9)) # sa ireg area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=10)) # sa wreg area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=11)) # sa mul area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=12)) # sa acc area
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=6)) # dram
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=11)) # sram D
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=15)) # sram L
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=31)) # sa
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=6)) # dram
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=11)) # sram D
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=15)) # sram L
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=31)) # sa

                    # unary temporal
                    computing = "ut"
                    for c in cycle_list:
                        name = a + "_" + b.zfill(2) + "b_" + computing + "_" + c.zfill(3) + "c_" + n + "_" + r
                        if not os.path.exists("./outputs/" + technode + "/" + name):
                            raise ValueError("Folder ./outputs/" + technode + "/" + name + " does not exist.")
                        
                        path = "./outputs/" + technode + "/" + name + "/simHwOut/"
                        bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=6)) # dram bw
                        bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=11)) # sram bw
                        time_list.append(return_indexed_elems(  input_csv=path + name + "_throughput_real.csv", index=3)) # runtime
                        tp_list.append(return_indexed_elems(    input_csv=path + name + "_throughput_real.csv", index=4)) # throughput
                        
                        path = "./outputs/" + technode + "/" + name + "/simEffOut/"
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=9)) # sa ireg area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=10)) # sa wreg area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=11)) # sa mul area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=12)) # sa acc area
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=6)) # dram
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=11)) # sram D
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=15)) # sram L
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=31)) # sa
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=6)) # dram
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=11)) # sram D
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=15)) # sram L
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=31)) # sa

    
        # bw
        x_axis = ["Conv1", "Conv2", "Conv3", "Conv4", "Conv5", "FC6", "FC7", "FC8", "AVG"]

        fig, ax = plt.subplots()
        
        idx_tot = 12

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width + 0.01

        # 8b - spm - bp
        index = 0
        bot_list = bw_list[index * 2]
        top_list = bw_list[index * 2 + 1]
        idx = 0
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b", label='DRAM')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r", label='SRAM')

        # 8b - spm - bs
        index = 1
        bot_list = bw_list[index * 2]
        top_list = bw_list[index * 2 + 1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # 8b - spm - ur - 32c
        index = 2
        bot_list = bw_list[index * 2]
        top_list = bw_list[index * 2 + 1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # 8b - spm - ur - 64c
        index = 3
        bot_list = bw_list[index * 2]
        top_list = bw_list[index * 2 + 1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # 8b - spm - ur - 128c
        index = 4
        bot_list = bw_list[index * 2]
        top_list = bw_list[index * 2 + 1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # 8b - spm - ur - 256c
        index = 5
        bot_list = bw_list[index * 2]
        top_list = bw_list[index * 2 + 1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # 8b - spm - ut - 32c
        # index = 6
        # bot_list = bw_list[index * 2]
        # top_list = bw_list[index * 2 + 1]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # 8b - spm - ut - 64c
        # index = 7
        # bot_list = bw_list[index * 2]
        # top_list = bw_list[index * 2 + 1]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # 8b - spm - ut - 128c
        # index = 8
        # bot_list = bw_list[index * 2]
        # top_list = bw_list[index * 2 + 1]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # 8b - spm - ut - 256c
        # index = 9
        # bot_list = bw_list[index * 2]
        # top_list = bw_list[index * 2 + 1]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # 8b - wospm - bp
        index = 10
        bot_list = bw_list[index * 2]
        top_list = bw_list[index * 2 + 1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # 8b - wospm - bs
        index = 11
        bot_list = bw_list[index * 2]
        top_list = bw_list[index * 2 + 1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # 8b - wospm - ur - 32c
        index = 12
        bot_list = bw_list[index * 2]
        top_list = bw_list[index * 2 + 1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # 8b - wospm - ur - 64c
        index = 13
        bot_list = bw_list[index * 2]
        top_list = bw_list[index * 2 + 1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # 8b - wospm - ur - 128c
        index = 14
        bot_list = bw_list[index * 2]
        top_list = bw_list[index * 2 + 1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # 8b - wospm - ur - 256c
        index = 15
        bot_list = bw_list[index * 2]
        top_list = bw_list[index * 2 + 1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # # 8b - wospm - ut - 32c
        # index = 16
        # bot_list = bw_list[index * 2]
        # top_list = bw_list[index * 2 + 1]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # # 8b - wospm - ut - 64c
        # index = 17
        # bot_list = bw_list[index * 2]
        # top_list = bw_list[index * 2 + 1]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # # 8b - wospm - ut - 128c
        # index = 18
        # bot_list = bw_list[index * 2]
        # top_list = bw_list[index * 2 + 1]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        # # 8b - wospm - ut - 256c
        # index = 19
        # bot_list = bw_list[index * 2]
        # top_list = bw_list[index * 2 + 1]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), top_list, width, bottom=bot_list, hatch = '/', alpha=0.99, color="r")

        ax.set_ylabel('Bandwidth (GBytes/sec)')
        ax.set_title('Memory bandwidth for AlexNet on ' + a_cap)
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        ax.legend()
        upper = [12.8 for i in range(len(x_idx))]
        plt.plot(x_idx, upper, "r--")
        plt.yscale(yscale)
        plt.savefig('./outputs_fig/' + technode + '/Memory bandwidth for AlexNet on ' + a_cap+ ".pdf", bbox_inches='tight')
        print("Bandwidth fig saved!")


        # time
        x_axis = ["Conv1", "Conv2", "Conv3", "Conv4", "Conv5", "FC6", "FC7", "FC8"]

        fig, ax = plt.subplots()
        
        idx_tot = 12

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width + 0.01

        # 8b - spm - bp
        index = 0
        bot_list = time_list[index][:-1]
        idx = 0
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - spm - bs
        index = 1
        bot_list = time_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - spm - ur - 32c
        index = 2
        bot_list = time_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - spm - ur - 64c
        index = 3
        bot_list = time_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - spm - ur - 128c
        index = 4
        bot_list = time_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - spm - ur - 256c
        index = 5
        bot_list = time_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # # 8b - spm - ut - 32c
        # index = 6
        # bot_list = time_list[index][:-1]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # # 8b - spm - ut - 64c
        # index = 7
        # bot_list = time_list[index][:-1]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # # 8b - spm - ut - 128c
        # index = 8
        # bot_list = time_list[index][:-1]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # # 8b - spm - ut - 256c
        # index = 9
        # bot_list = time_list[index][:-1]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - wospm - bp
        index = 10
        bot_list = time_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - wospm - bs
        index = 11
        bot_list = time_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - wospm - ur - 32c
        index = 12
        bot_list = time_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - wospm - ur - 64c
        index = 13
        bot_list = time_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - wospm - ur - 128c
        index = 14
        bot_list = time_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - wospm - ur - 256c
        index = 15
        bot_list = time_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # # 8b - wospm - ut - 32c
        # index = 16
        # bot_list = time_list[index][:-1]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # # 8b - wospm - ut - 64c
        # index = 17
        # bot_list = time_list[index][:-1]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # # 8b - wospm - ut - 128c
        # index = 18
        # bot_list = time_list[index][:-1]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # # 8b - wospm - ut - 256c
        # index = 19
        # bot_list = time_list[index][:-1]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        ax.set_ylabel('Runtime (Seconds)')
        ax.set_title('Runtime for AlexNet on ' + a_cap)
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        # plt.ylim(0, 0.1)
        plt.yscale(yscale)
        plt.savefig('./outputs_fig/' + technode + '/Runtime for AlexNet on ' + a_cap+ ".pdf", bbox_inches='tight')
        print("Runtime fig saved!")


        # throughput
        x_axis = ["Conv1", "Conv2", "Conv3", "Conv4", "Conv5", "FC6", "FC7", "FC8", "Total"]

        fig, ax = plt.subplots()
        
        idx_tot = 12

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width + 0.01

        # 8b - spm - bp
        index = 0
        bot_list = tp_list[index]
        idx = 0
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - spm - bs
        index = 1
        bot_list = tp_list[index]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - spm - ur - 32c
        index = 2
        bot_list = tp_list[index]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - spm - ur - 64c
        index = 3
        bot_list = tp_list[index]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - spm - ur - 128c
        index = 4
        bot_list = tp_list[index]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - spm - ur - 256c
        index = 5
        bot_list = tp_list[index]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # # 8b - spm - ut - 32c
        # index = 6
        # bot_list = tp_list[index]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # # 8b - spm - ut - 64c
        # index = 7
        # bot_list = tp_list[index]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # # 8b - spm - ut - 128c
        # index = 8
        # bot_list = tp_list[index]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # # 8b - spm - ut - 256c
        # index = 9
        # bot_list = tp_list[index]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - wospm - bp
        index = 10
        bot_list = tp_list[index]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - wospm - bs
        index = 11
        bot_list = tp_list[index]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - wospm - ur - 32c
        index = 12
        bot_list = tp_list[index]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - wospm - ur - 64c
        index = 13
        bot_list = tp_list[index]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - wospm - ur - 128c
        index = 14
        bot_list = tp_list[index]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # 8b - wospm - ur - 256c
        index = 15
        bot_list = tp_list[index]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # # 8b - wospm - ut - 32c
        # index = 16
        # bot_list = tp_list[index]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # # 8b - wospm - ut - 64c
        # index = 17
        # bot_list = tp_list[index]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # # 8b - wospm - ut - 128c
        # index = 18
        # bot_list = tp_list[index]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        # # 8b - wospm - ut - 256c
        # index = 19
        # bot_list = tp_list[index]
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), bot_list, width, hatch = 'x', alpha=0.99, color="b")

        ax.set_ylabel('Throughput (Frames/sec)')
        ax.set_title('Throughput for AlexNet on ' + a_cap)
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        plt.yscale(yscale)
        plt.savefig('./outputs_fig/' + technode + '/Throughput for AlexNet on ' + a_cap+ ".pdf", bbox_inches='tight')
        print("Throughput fig saved!")


        # area
        x_axis = ["BP-8b", "BS-8b", "UR-8b", "UT-8b", "BP-16b", "BS-16b", "UR-16b", "UT-16b"]

        fig, ax = plt.subplots()
        
        x_idx = np.arange(len(x_axis))

        width = 0.35

        index = 0
        ireg_list = [
                        area_list[ 0 * 4 + index][0], area_list[ 1 * 4 + index][0], area_list[ 2 * 4 + index][0], area_list[ 6 * 4 + index][0], 
                        area_list[20 * 4 + index][0], area_list[21 * 4 + index][0], area_list[22 * 4 + index][0], area_list[26 * 4 + index][0]
                    ]
        index = 1
        wreg_list = [
                        area_list[ 0 * 4 + index][0], area_list[ 1 * 4 + index][0], area_list[ 2 * 4 + index][0], area_list[ 6 * 4 + index][0], 
                        area_list[20 * 4 + index][0], area_list[21 * 4 + index][0], area_list[22 * 4 + index][0], area_list[26 * 4 + index][0]
                    ]
        index = 2
        mul_list = [
                        area_list[ 0 * 4 + index][0], area_list[ 1 * 4 + index][0], area_list[ 2 * 4 + index][0], area_list[ 6 * 4 + index][0], 
                        area_list[20 * 4 + index][0], area_list[21 * 4 + index][0], area_list[22 * 4 + index][0], area_list[26 * 4 + index][0]
                    ]
        index = 3
        acc_list = [
                        area_list[ 0 * 4 + index][0], area_list[ 1 * 4 + index][0], area_list[ 2 * 4 + index][0], area_list[ 6 * 4 + index][0], 
                        area_list[20 * 4 + index][0], area_list[21 * 4 + index][0], area_list[22 * 4 + index][0], area_list[26 * 4 + index][0]
                    ]

        bot_list    = []
        bot1_list   = []
        bot2_list   = []
        top_list    = []

        for i in range(len(x_axis)):
            bot_list.append(ireg_list[i])
            bot1_list.append(bot_list[i] + wreg_list[i])
            bot2_list.append(bot1_list[i] + mul_list[i])
            top_list.append(bot2_list[i] + acc_list[i])

        ax.bar(x_idx, ireg_list, width, hatch = 'x', alpha=0.99, color="b", label='IREG')
        ax.bar(x_idx, wreg_list, width, bottom=bot_list, hatch = '+', alpha=0.99, color="r", label='WREG')
        ax.bar(x_idx, mul_list, width, bottom=bot1_list, hatch = '/', alpha=0.99, color="g", label='MUL')
        ax.bar(x_idx, acc_list, width, bottom=bot2_list, hatch = '*', alpha=0.99, color="y", label='ACC')

        ax.set_ylabel('Area (mm^2)')
        ax.set_title('Systolic array area breakdown on ' + a_cap)
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        ax.legend()
        plt.savefig('./outputs_fig/' + technode + '/Systolic array area breakdown on ' + a_cap+ ".pdf", bbox_inches='tight')
        print("Area fig saved!")

        # energy
        x_axis = ["Conv1", "Conv2", "Conv3", "Conv4", "Conv5", "FC6", "FC7", "FC8"]

        fig, ax = plt.subplots()
        
        idx_tot = 12

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width + 0.01

        # 8b - spm - bp
        index = 0
        dram_list = energy_list[index * 4][:-1]
        sram_d_list = energy_list[index * 4 + 1][:-1]
        sram_l_list = energy_list[index * 4 + 2][:-1]
        sarr_list = energy_list[index * 4 + 3][:-1]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx = 0
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b", label='DRAM D')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r", label='SRAM D')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g", label='SRAM L')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y", label='SArr')

        # 8b - spm - bs
        index = 1
        dram_list = energy_list[index * 4][:-1]
        sram_d_list = energy_list[index * 4 + 1][:-1]
        sram_l_list = energy_list[index * 4 + 2][:-1]
        sarr_list = energy_list[index * 4 + 3][:-1]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - spm - ur - 32c
        index = 2
        dram_list = energy_list[index * 4][:-1]
        sram_d_list = energy_list[index * 4 + 1][:-1]
        sram_l_list = energy_list[index * 4 + 2][:-1]
        sarr_list = energy_list[index * 4 + 3][:-1]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - spm - ur - 64c
        index = 3
        dram_list = energy_list[index * 4][:-1]
        sram_d_list = energy_list[index * 4 + 1][:-1]
        sram_l_list = energy_list[index * 4 + 2][:-1]
        sarr_list = energy_list[index * 4 + 3][:-1]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - spm - ur - 128c
        index = 4
        dram_list = energy_list[index * 4][:-1]
        sram_d_list = energy_list[index * 4 + 1][:-1]
        sram_l_list = energy_list[index * 4 + 2][:-1]
        sarr_list = energy_list[index * 4 + 3][:-1]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - spm - ur - 256c
        index = 5
        dram_list = energy_list[index * 4][:-1]
        sram_d_list = energy_list[index * 4 + 1][:-1]
        sram_l_list = energy_list[index * 4 + 2][:-1]
        sarr_list = energy_list[index * 4 + 3][:-1]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # # 8b - spm - ut - 32c
        # index = 6
        # dram_list = energy_list[index * 4][:-1]
        # sram_d_list = energy_list[index * 4 + 1][:-1]
        # sram_l_list = energy_list[index * 4 + 2][:-1]
        # sarr_list = energy_list[index * 4 + 3][:-1]
        # bot_list = []
        # bot1_list = []
        # bot2_list = []
        # for i in range(len(x_axis)):
        #     bot_list.append(dram_list[i])
        #     bot1_list.append(bot_list[i] + sram_d_list[i])
        #     bot2_list.append(bot1_list[i] + sram_l_list[i])
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # # 8b - spm - ut - 64c
        # index = 7
        # dram_list = energy_list[index * 4][:-1]
        # sram_d_list = energy_list[index * 4 + 1][:-1]
        # sram_l_list = energy_list[index * 4 + 2][:-1]
        # sarr_list = energy_list[index * 4 + 3][:-1]
        # bot_list = []
        # bot1_list = []
        # bot2_list = []
        # for i in range(len(x_axis)):
        #     bot_list.append(dram_list[i])
        #     bot1_list.append(bot_list[i] + sram_d_list[i])
        #     bot2_list.append(bot1_list[i] + sram_l_list[i])
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # # 8b - spm - ut - 128c
        # index = 8
        # dram_list = energy_list[index * 4][:-1]
        # sram_d_list = energy_list[index * 4 + 1][:-1]
        # sram_l_list = energy_list[index * 4 + 2][:-1]
        # sarr_list = energy_list[index * 4 + 3][:-1]
        # bot_list = []
        # bot1_list = []
        # bot2_list = []
        # for i in range(len(x_axis)):
        #     bot_list.append(dram_list[i])
        #     bot1_list.append(bot_list[i] + sram_d_list[i])
        #     bot2_list.append(bot1_list[i] + sram_l_list[i])
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # # 8b - spm - ut - 256c
        # index = 9
        # dram_list = energy_list[index * 4][:-1]
        # sram_d_list = energy_list[index * 4 + 1][:-1]
        # sram_l_list = energy_list[index * 4 + 2][:-1]
        # sarr_list = energy_list[index * 4 + 3][:-1]
        # bot_list = []
        # bot1_list = []
        # bot2_list = []
        # for i in range(len(x_axis)):
        #     bot_list.append(dram_list[i])
        #     bot1_list.append(bot_list[i] + sram_d_list[i])
        #     bot2_list.append(bot1_list[i] + sram_l_list[i])
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - wospm - bp
        index = 10
        dram_list = energy_list[index * 4][:-1]
        sram_d_list = energy_list[index * 4 + 1][:-1]
        sram_l_list = energy_list[index * 4 + 2][:-1]
        sarr_list = energy_list[index * 4 + 3][:-1]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - wospm - bs
        index = 11
        dram_list = energy_list[index * 4][:-1]
        sram_d_list = energy_list[index * 4 + 1][:-1]
        sram_l_list = energy_list[index * 4 + 2][:-1]
        sarr_list = energy_list[index * 4 + 3][:-1]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - wospm - ur - 32c
        index = 12
        dram_list = energy_list[index * 4][:-1]
        sram_d_list = energy_list[index * 4 + 1][:-1]
        sram_l_list = energy_list[index * 4 + 2][:-1]
        sarr_list = energy_list[index * 4 + 3][:-1]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - wospm - ur - 64c
        index = 13
        dram_list = energy_list[index * 4][:-1]
        sram_d_list = energy_list[index * 4 + 1][:-1]
        sram_l_list = energy_list[index * 4 + 2][:-1]
        sarr_list = energy_list[index * 4 + 3][:-1]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - wospm - ur - 128c
        index = 14
        dram_list = energy_list[index * 4][:-1]
        sram_d_list = energy_list[index * 4 + 1][:-1]
        sram_l_list = energy_list[index * 4 + 2][:-1]
        sarr_list = energy_list[index * 4 + 3][:-1]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - wospm - ur - 256c
        index = 15
        dram_list = energy_list[index * 4][:-1]
        sram_d_list = energy_list[index * 4 + 1][:-1]
        sram_l_list = energy_list[index * 4 + 2][:-1]
        sarr_list = energy_list[index * 4 + 3][:-1]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # # 8b - wospm - ut - 32c
        # index = 16
        # dram_list = energy_list[index * 4][:-1]
        # sram_d_list = energy_list[index * 4 + 1][:-1]
        # sram_l_list = energy_list[index * 4 + 2][:-1]
        # sarr_list = energy_list[index * 4 + 3][:-1]
        # bot_list = []
        # bot1_list = []
        # bot2_list = []
        # for i in range(len(x_axis)):
        #     bot_list.append(dram_list[i])
        #     bot1_list.append(bot_list[i] + sram_d_list[i])
        #     bot2_list.append(bot1_list[i] + sram_l_list[i])
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # # 8b - wospm - ut - 64c
        # index = 17
        # dram_list = energy_list[index * 4][:-1]
        # sram_d_list = energy_list[index * 4 + 1][:-1]
        # sram_l_list = energy_list[index * 4 + 2][:-1]
        # sarr_list = energy_list[index * 4 + 3][:-1]
        # bot_list = []
        # bot1_list = []
        # bot2_list = []
        # for i in range(len(x_axis)):
        #     bot_list.append(dram_list[i])
        #     bot1_list.append(bot_list[i] + sram_d_list[i])
        #     bot2_list.append(bot1_list[i] + sram_l_list[i])
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # # 8b - wospm - ut - 128c
        # index = 18
        # dram_list = energy_list[index * 4][:-1]
        # sram_d_list = energy_list[index * 4 + 1][:-1]
        # sram_l_list = energy_list[index * 4 + 2][:-1]
        # sarr_list = energy_list[index * 4 + 3][:-1]
        # bot_list = []
        # bot1_list = []
        # bot2_list = []
        # for i in range(len(x_axis)):
        #     bot_list.append(dram_list[i])
        #     bot1_list.append(bot_list[i] + sram_d_list[i])
        #     bot2_list.append(bot1_list[i] + sram_l_list[i])
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # # 8b - wospm - ut - 256c
        # index = 19
        # dram_list = energy_list[index * 4][:-1]
        # sram_d_list = energy_list[index * 4 + 1][:-1]
        # sram_l_list = energy_list[index * 4 + 2][:-1]
        # sarr_list = energy_list[index * 4 + 3][:-1]
        # bot_list = []
        # bot1_list = []
        # bot2_list = []
        # for i in range(len(x_axis)):
        #     bot_list.append(dram_list[i])
        #     bot1_list.append(bot_list[i] + sram_d_list[i])
        #     bot2_list.append(bot1_list[i] + sram_l_list[i])
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        ax.set_ylabel('Enery (uJ)')
        ax.set_title('Enery consumption for AlexNet on ' + a_cap)
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        ax.legend()
        plt.yscale(yscale)
        plt.savefig('./outputs_fig/' + technode + '/Enery consumption for AlexNet on ' + a_cap+ ".pdf", bbox_inches='tight')
        print("Energy fig saved!")


        # power
        x_axis = ["Conv1", "Conv2", "Conv3", "Conv4", "Conv5", "FC6", "FC7", "FC8", "AVG"]

        fig, ax = plt.subplots()
        
        idx_tot = 12

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width + 0.01

        # 8b - spm - bp
        index = 0
        dram_list = power_list[index * 4]
        sram_d_list = power_list[index * 4 + 1]
        sram_l_list = power_list[index * 4 + 2]
        sarr_list = power_list[index * 4 + 3]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx = 0
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b", label='DRAM D')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r", label='SRAM D')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g", label='SRAM L')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y", label='SArr')

        # 8b - spm - bs
        index = 1
        dram_list = power_list[index * 4]
        sram_d_list = power_list[index * 4 + 1]
        sram_l_list = power_list[index * 4 + 2]
        sarr_list = power_list[index * 4 + 3]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - spm - ur - 32c
        index = 2
        dram_list = power_list[index * 4]
        sram_d_list = power_list[index * 4 + 1]
        sram_l_list = power_list[index * 4 + 2]
        sarr_list = power_list[index * 4 + 3]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - spm - ur - 64c
        index = 3
        dram_list = power_list[index * 4]
        sram_d_list = power_list[index * 4 + 1]
        sram_l_list = power_list[index * 4 + 2]
        sarr_list = power_list[index * 4 + 3]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - spm - ur - 128c
        index = 4
        dram_list = power_list[index * 4]
        sram_d_list = power_list[index * 4 + 1]
        sram_l_list = power_list[index * 4 + 2]
        sarr_list = power_list[index * 4 + 3]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - spm - ur - 256c
        index = 5
        dram_list = power_list[index * 4]
        sram_d_list = power_list[index * 4 + 1]
        sram_l_list = power_list[index * 4 + 2]
        sarr_list = power_list[index * 4 + 3]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # # 8b - spm - ut - 32c
        # index = 6
        # dram_list = power_list[index * 4]
        # sram_d_list = power_list[index * 4 + 1]
        # sram_l_list = power_list[index * 4 + 2]
        # sarr_list = power_list[index * 4 + 3]
        # bot_list = []
        # bot1_list = []
        # bot2_list = []
        # for i in range(len(x_axis)):
        #     bot_list.append(dram_list[i])
        #     bot1_list.append(bot_list[i] + sram_d_list[i])
        #     bot2_list.append(bot1_list[i] + sram_l_list[i])
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # # 8b - spm - ut - 64c
        # index = 7
        # dram_list = power_list[index * 4]
        # sram_d_list = power_list[index * 4 + 1]
        # sram_l_list = power_list[index * 4 + 2]
        # sarr_list = power_list[index * 4 + 3]
        # bot_list = []
        # bot1_list = []
        # bot2_list = []
        # for i in range(len(x_axis)):
        #     bot_list.append(dram_list[i])
        #     bot1_list.append(bot_list[i] + sram_d_list[i])
        #     bot2_list.append(bot1_list[i] + sram_l_list[i])
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # # 8b - spm - ut - 128c
        # index = 8
        # dram_list = power_list[index * 4]
        # sram_d_list = power_list[index * 4 + 1]
        # sram_l_list = power_list[index * 4 + 2]
        # sarr_list = power_list[index * 4 + 3]
        # bot_list = []
        # bot1_list = []
        # bot2_list = []
        # for i in range(len(x_axis)):
        #     bot_list.append(dram_list[i])
        #     bot1_list.append(bot_list[i] + sram_d_list[i])
        #     bot2_list.append(bot1_list[i] + sram_l_list[i])
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # # 8b - spm - ut - 256c
        # index = 9
        # dram_list = power_list[index * 4]
        # sram_d_list = power_list[index * 4 + 1]
        # sram_l_list = power_list[index * 4 + 2]
        # sarr_list = power_list[index * 4 + 3]
        # bot_list = []
        # bot1_list = []
        # bot2_list = []
        # for i in range(len(x_axis)):
        #     bot_list.append(dram_list[i])
        #     bot1_list.append(bot_list[i] + sram_d_list[i])
        #     bot2_list.append(bot1_list[i] + sram_l_list[i])
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - wospm - bp
        index = 10
        dram_list = power_list[index * 4]
        sram_d_list = power_list[index * 4 + 1]
        sram_l_list = power_list[index * 4 + 2]
        sarr_list = power_list[index * 4 + 3]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - wospm - bs
        index = 11
        dram_list = power_list[index * 4]
        sram_d_list = power_list[index * 4 + 1]
        sram_l_list = power_list[index * 4 + 2]
        sarr_list = power_list[index * 4 + 3]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - wospm - ur - 32c
        index = 12
        dram_list = power_list[index * 4]
        sram_d_list = power_list[index * 4 + 1]
        sram_l_list = power_list[index * 4 + 2]
        sarr_list = power_list[index * 4 + 3]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - wospm - ur - 64c
        index = 13
        dram_list = power_list[index * 4]
        sram_d_list = power_list[index * 4 + 1]
        sram_l_list = power_list[index * 4 + 2]
        sarr_list = power_list[index * 4 + 3]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - wospm - ur - 128c
        index = 14
        dram_list = power_list[index * 4]
        sram_d_list = power_list[index * 4 + 1]
        sram_l_list = power_list[index * 4 + 2]
        sarr_list = power_list[index * 4 + 3]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # 8b - wospm - ur - 256c
        index = 15
        dram_list = power_list[index * 4]
        sram_d_list = power_list[index * 4 + 1]
        sram_l_list = power_list[index * 4 + 2]
        sarr_list = power_list[index * 4 + 3]
        bot_list = []
        bot1_list = []
        bot2_list = []
        for i in range(len(x_axis)):
            bot_list.append(dram_list[i])
            bot1_list.append(bot_list[i] + sram_d_list[i])
            bot2_list.append(bot1_list[i] + sram_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # # 8b - wospm - ut - 32c
        # index = 16
        # dram_list = power_list[index * 4]
        # sram_d_list = power_list[index * 4 + 1]
        # sram_l_list = power_list[index * 4 + 2]
        # sarr_list = power_list[index * 4 + 3]
        # bot_list = []
        # bot1_list = []
        # bot2_list = []
        # for i in range(len(x_axis)):
        #     bot_list.append(dram_list[i])
        #     bot1_list.append(bot_list[i] + sram_d_list[i])
        #     bot2_list.append(bot1_list[i] + sram_l_list[i])
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # # 8b - wospm - ut - 64c
        # index = 17
        # dram_list = power_list[index * 4]
        # sram_d_list = power_list[index * 4 + 1]
        # sram_l_list = power_list[index * 4 + 2]
        # sarr_list = power_list[index * 4 + 3]
        # bot_list = []
        # bot1_list = []
        # bot2_list = []
        # for i in range(len(x_axis)):
        #     bot_list.append(dram_list[i])
        #     bot1_list.append(bot_list[i] + sram_d_list[i])
        #     bot2_list.append(bot1_list[i] + sram_l_list[i])
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # # 8b - wospm - ut - 128c
        # index = 18
        # dram_list = power_list[index * 4]
        # sram_d_list = power_list[index * 4 + 1]
        # sram_l_list = power_list[index * 4 + 2]
        # sarr_list = power_list[index * 4 + 3]
        # bot_list = []
        # bot1_list = []
        # bot2_list = []
        # for i in range(len(x_axis)):
        #     bot_list.append(dram_list[i])
        #     bot1_list.append(bot_list[i] + sram_d_list[i])
        #     bot2_list.append(bot1_list[i] + sram_l_list[i])
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        # # 8b - wospm - ut - 256c
        # index = 19
        # dram_list = power_list[index * 4]
        # sram_d_list = power_list[index * 4 + 1]
        # sram_l_list = power_list[index * 4 + 2]
        # sarr_list = power_list[index * 4 + 3]
        # bot_list = []
        # bot1_list = []
        # bot2_list = []
        # for i in range(len(x_axis)):
        #     bot_list.append(dram_list[i])
        #     bot1_list.append(bot_list[i] + sram_d_list[i])
        #     bot2_list.append(bot1_list[i] + sram_l_list[i])
        # idx += 1
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_list, width, hatch = 'x', alpha=0.99, color="b")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_list, width, bottom=bot_list, hatch = 'o', alpha=0.99, color="r")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_list, width, bottom=bot1_list, hatch = '+', alpha=0.99, color="g")
        # ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_list, width, bottom=bot2_list, hatch = '/', alpha=0.99, color="y")

        ax.set_ylabel('Power (mW)')
        ax.set_title('Power consumption for AlexNet on ' + a_cap)
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        ax.legend()
        plt.yscale(yscale)
        plt.savefig('./outputs_fig/' + technode + '/Power consumption for AlexNet on ' + a_cap+ ".pdf", bbox_inches='tight')
        print("Power fig saved!")
        print("")


def prune(input_list):
    l = []

    for e in input_list:
        e = e.strip() # remove the leading and trailing characters, here space
        if e != '' and e != ' ':
            l.append(e)

    return l


def return_indexed_elems(input_csv=None, index=None):
    l = []

    csv_file = open(input_csv, "r")
    
    first = True
    for entry in csv_file:
        if first == True:
            first = False
            continue

        elems = entry.strip().split(',')
        elems = prune(elems)
        if len(elems) > 0:
            l.append(float(elems[index]))
    
    csv_file.close()

    return l


if __name__ == '__main__':
    plot_fig()
    # plot_fig(technode="45nm_rvt")
