import os
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib
from numpy import mean, median

def plot_fig(technode=""):
    font = {'family':'Times New Roman', 'size': 6}
    matplotlib.rc('font', **font)

    print_power_onchip = False
    print_power_total = False
    print_energy_onchip = False
    print_energy_total = False
    print_area = False
    print_bandwidth = False
    print_runtime = False
    print_energy_eff = False
    print_power_eff = False

    if not os.path.exists("./outputs_fig_mlperf/"):
        os.system("mkdir ./outputs_fig_mlperf")

    arch_list = ["tpu", "eyeriss"]
    network_list = ["mlperf"]
    bit_list = ["8"]
    cycle_list = ["32", "64", "128"]
    ram_list = ["ddr3_w__spm", "ddr3_wo_spm"]

    for a in arch_list:
        bw_list = []
        time_ideal_list = []
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
                for r in ram_list[:1]:
                    # binary parallel
                    computing = "bp"
                    name = a + "_" + b.zfill(2) + "b_" + computing + "_" + "001c_" + n + "_" + r
                    if not os.path.exists("./outputs/" + technode + "/" + name):
                        raise ValueError("Folder ./outputs/" + technode + "/" + name + " does not exist.")
                    
                    path = "./outputs/" + technode + "/" + name + "/simHwOut/"
                    bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=6)) # dram bw
                    bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=11)) # sram bw
                    time_ideal_list.append(return_indexed_elems(  input_csv=path + name + "_throughput_ideal.csv", index=3)) # ideal runtime
                    time_list.append(return_indexed_elems(  input_csv=path + name + "_throughput_real.csv", index=3)) # runtime
                    tp_list.append(return_indexed_elems(    input_csv=path + name + "_throughput_real.csv", index=4)) # throughput
                    
                    path = "./outputs/" + technode + "/" + name + "/simEffOut/"
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=8)) # sram area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=9)) # sa ireg area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=10)) # sa wreg area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=11)) # sa mul area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=12)) # sa acc area
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=6)) # dram
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=11)) # sram D
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=15)) # sram L
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=29)) # sa D
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=30)) # sa L
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=6)) # dram
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=11)) # sram D
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=15)) # sram L
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=29)) # sa D
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=30)) # sa L
                    
                    # binary serial
                    computing = "bs"
                    name = a + "_" + b.zfill(2) + "b_" + computing + "_" + b.zfill(3) + "c_" + n + "_" + r
                    if not os.path.exists("./outputs/" + technode + "/" + name):
                        raise ValueError("Folder ./outputs/" + technode + "/" + name + " does not exist.")
                    
                    path = "./outputs/" + technode + "/" + name + "/simHwOut/"
                    bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=6)) # dram bw
                    bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=11)) # sram bw
                    time_ideal_list.append(return_indexed_elems(  input_csv=path + name + "_throughput_ideal.csv", index=3)) # ideal runtime
                    time_list.append(return_indexed_elems(  input_csv=path + name + "_throughput_real.csv", index=3)) # runtime
                    tp_list.append(return_indexed_elems(    input_csv=path + name + "_throughput_real.csv", index=4)) # throughput
                    
                    path = "./outputs/" + technode + "/" + name + "/simEffOut/"
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=8)) # sram area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=9)) # sa ireg area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=10)) # sa wreg area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=11)) # sa mul area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=12)) # sa acc area
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=6)) # dram
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=11)) # sram D
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=15)) # sram L
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=29)) # sa D
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=30)) # sa L
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=6)) # dram
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=11)) # sram D
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=15)) # sram L
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=29)) # sa D
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=30)) # sa L

                for r in ram_list[1:]:
                    # unary rate
                    computing = "ur"
                    for c in cycle_list:
                        name = a + "_" + b.zfill(2) + "b_" + computing + "_" + c.zfill(3) + "c_" + n + "_" + r
                        if not os.path.exists("./outputs/" + technode + "/" + name):
                            raise ValueError("Folder ./outputs/" + technode + "/" + name + " does not exist.")
                        
                        path = "./outputs/" + technode + "/" + name + "/simHwOut/"
                        bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=6)) # dram bw
                        bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=11)) # sram bw
                        time_ideal_list.append(return_indexed_elems(  input_csv=path + name + "_throughput_ideal.csv", index=3)) # ideal runtime
                        time_list.append(return_indexed_elems(  input_csv=path + name + "_throughput_real.csv", index=3)) # runtime
                        tp_list.append(return_indexed_elems(    input_csv=path + name + "_throughput_real.csv", index=4)) # throughput
                        
                        path = "./outputs/" + technode + "/" + name + "/simEffOut/"
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=8)) # sram area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=9)) # sa ireg area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=10)) # sa wreg area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=11)) # sa mul area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=12)) # sa acc area
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=6)) # dram
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=11)) # sram D
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=15)) # sram L
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=29)) # sa D
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=30)) # sa L
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=6)) # dram
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=11)) # sram D
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=15)) # sram L
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=29)) # sa D
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=30)) # sa L

                    # ugemm rate
                    computing = "ug"
                    for c in ["256"]:
                        name = a + "_" + b.zfill(2) + "b_" + computing + "_" + c.zfill(3) + "c_" + n + "_" + r
                        if not os.path.exists("./outputs/" + technode + "/" + name):
                            raise ValueError("Folder ./outputs/" + technode + "/" + name + " does not exist.")

                        path = "./outputs/" + technode + "/" + name + "/simHwOut/"
                        bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=6)) # dram bw
                        bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=11)) # sram bw
                        time_ideal_list.append(return_indexed_elems(  input_csv=path + name + "_throughput_ideal.csv", index=3)) # ideal runtime
                        time_list.append(return_indexed_elems(  input_csv=path + name + "_throughput_real.csv", index=3)) # runtime
                        tp_list.append(return_indexed_elems(    input_csv=path + name + "_throughput_real.csv", index=4)) # throughput

                        path = "./outputs/" + technode + "/" + name + "/simEffOut/"
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=8)) # sram area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=9)) # sa ireg area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=10)) # sa wreg area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=11)) # sa mul area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=12)) # sa acc area
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=6)) # dram
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=11)) # sram D
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=15)) # sram L
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=29)) # sa D
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=30)) # sa L
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=6)) # dram
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=11)) # sram D
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=15)) # sram L
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=29)) # sa D
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=30)) # sa L

        # bandwidth
        my_dpi = 300
        if a == "eyeriss":
            fig_h = 1.6
        else:
            fig_h = 1.3
        fig_w = 3.3115

        bp_color = "#7A81FF"
        bs_color = "#FF7F7F"
        u6_color = "#666666"
        u7_color = "#888888"
        u8_color = "#AAAAAA"
        ug_color = "#CCCCCC"
        bg_color = "#D783FF"

        x_axis = ["Average"]

        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        
        idx_tot = 6

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width
        
        # 8b - spm - bp
        index = 0
        dram_bw_list = bw_list[index * 2][-1:]
        sram_bw_list = [-x for x in bw_list[index * 2 + 1][-1:]]
        idx = 1.5
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=bp_color, label="Binary Parallel")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_bw_list, width, hatch = None, alpha=0.99, color=bp_color)
        dram_bw_list_bp_spm = [i for i in dram_bw_list]
        sram_bw_list_bp_spm = [i for i in sram_bw_list]

        # 8b - spm - bs
        index = 1
        dram_bw_list = bw_list[index * 2][-1:]
        sram_bw_list = [-x for x in bw_list[index * 2 + 1][-1:]]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=bs_color, label="Binary Serial")
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_bw_list, width, hatch = None, alpha=0.99, color=bs_color)
        dram_bw_list_bs_spm = [i for i in dram_bw_list]
        sram_bw_list_bs_spm = [i for i in sram_bw_list]

        # 8b - wospm - ur - 32c
        index = 2
        dram_bw_list = bw_list[index * 2][-1:]
        sram_bw_list = [-x for x in bw_list[index * 2 + 1][-1:]]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=u6_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_bw_list, width, hatch = None, alpha=0.99, color=u6_color)
        dram_bw_list_u6_wspm = [i for i in dram_bw_list]
        sram_bw_list_u6_wspm = [i for i in sram_bw_list]

        # 8b - wospm - ur - 64c
        index = 3
        dram_bw_list = bw_list[index * 2][-1:]
        sram_bw_list = [-x for x in bw_list[index * 2 + 1][-1:]]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=u7_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_bw_list, width, hatch = None, alpha=0.99, color=u7_color)
        dram_bw_list_u7_wspm = [i for i in dram_bw_list]
        sram_bw_list_u7_wspm = [i for i in sram_bw_list]

        # 8b - wospm - ur - 128c
        index = 4
        dram_bw_list = bw_list[index * 2][-1:]
        sram_bw_list = [-x for x in bw_list[index * 2 + 1][-1:]]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=u8_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_bw_list, width, hatch = None, alpha=0.99, color=u8_color)
        dram_bw_list_u8_wspm = [i for i in dram_bw_list]
        sram_bw_list_u8_wspm = [i for i in sram_bw_list]

        # 8b - wospm - ug - 256c
        index = 5
        dram_bw_list = bw_list[index * 2][-1:]
        sram_bw_list = [-x for x in bw_list[index * 2 + 1][-1:]]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=ug_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_bw_list, width, hatch = None, alpha=0.99, color=ug_color)
        dram_bw_list_ug_wspm = [i for i in dram_bw_list]
        sram_bw_list_ug_wspm = [i for i in sram_bw_list]

        ax.set_ylabel('SRAM-DRAM bandwidth\n(GB/s)')
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        plt.xlim(x_idx[0]-0.5, x_idx[-1]+0.5)
        plt.yscale("symlog", linthresh=0.001)

        # locs, labels = plt.yticks()
        if a == "eyeriss":
            locs = [-10, -1, -0.1, -0.01, -0.001, 0, 0.001, 0.01, 0.1, 1, 10]
        else:
            locs = [-10, -1, -0.1, -0.01, -0.001, 0, 0.001, 0.01, 0.1, 1, 10]
        ax.set_yticks(locs)
        y_label_list = []
        for y in locs:
            if y != 0:
                y_label_list.append("{:1.0E}".format(abs(y)))
            else:
                y_label_list.append("0")
        ax.set_yticklabels(y_label_list)

        bottom, top = plt.ylim()

        if a == "eyeriss":
            ax.set_ylim((bottom, top*2500))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top/2500], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            ax.legend(loc="upper center", ncol=3, frameon=True)
        else:
            ax.set_ylim((bottom, top))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
        ax.axhline(y=0, color="k", linewidth = 0.1)
        
        fig.tight_layout()
        plt.savefig('./outputs_fig/' + technode + '/Bandwidth_' + a_cap + ".pdf", bbox_inches='tight', dpi=my_dpi, pad_inches=0.02)

        if print_bandwidth:
            print("DRAM bp spm :", dram_bw_list_bp_spm)
            print("min:", min(dram_bw_list_bp_spm), "max:", max(dram_bw_list_bp_spm))
            print("DRAM bs spm :", dram_bw_list_bs_spm)
            print("min:", min(dram_bw_list_bs_spm), "max:", max(dram_bw_list_bs_spm))

            print("SRAM bp spm :", sram_bw_list_bp_spm)
            print("SRAM bs spm :", sram_bw_list_bs_spm)

            print("DRAM u6 wspm:", dram_bw_list_u6_wspm)
            print("min:", min(dram_bw_list_u6_wspm), "max:", max(dram_bw_list_u6_wspm))
            print("DRAM u7 wspm:", dram_bw_list_u7_wspm)
            print("min:", min(dram_bw_list_u7_wspm), "max:", max(dram_bw_list_u7_wspm))
            print("DRAM u8 wspm:", dram_bw_list_u8_wspm)
            print("min:", min(dram_bw_list_u8_wspm), "max:", max(dram_bw_list_u8_wspm))
            print("DRAM ug wspm:", dram_bw_list_ug_wspm)
            print("min:", min(dram_bw_list_ug_wspm), "max:", max(dram_bw_list_ug_wspm))

            sram_bw_r_list_bp_spm = []
            sram_bw_r_list_bs_spm = []
            for i in range(len(dram_bw_list_bp_spm)):
                sram_bw_r_list_bp_spm.append(-sram_bw_list_bp_spm[i] / dram_bw_list_bp_spm[i])
                sram_bw_r_list_bs_spm.append(-sram_bw_list_bs_spm[i] / dram_bw_list_bs_spm[i])
            print("SRAM bp wspm r:", sram_bw_r_list_bp_spm)
            print("SRAM bs wspm r:", sram_bw_r_list_bs_spm)

        print("Bandwidth fig saved!\n")


        # runtime
        my_dpi = 300
        if a == "eyeriss":
            fig_h = 1.1
        else:
            fig_h = 1
        fig_w = 3.3115

        bp_color = "#7A81FF"
        bs_color = "#FF7F7F"
        u6_color = "#666666"
        u7_color = "#888888"
        u8_color = "#AAAAAA"
        ug_color = "#CCCCCC"
        bg_color = "#D783FF"

        x_axis = ["Average"]

        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        
        idx_tot = 6

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width

        # 8b - spm - bp
        index = 0
        runtime_list = time_list[index][-1:]
        idx = 1.5
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), runtime_list, width, hatch = None, alpha=0.99, color=bp_color, label="Binary Parallel")
        runtime_ideal_r_list_bp_spm = []
        for i in range(len(runtime_list)):
            runtime_ideal_r_list_bp_spm.append(runtime_list[i] / time_ideal_list[index][-1:][i] - 1)

        # 8b - spm - bs
        index = 1
        runtime_list = time_list[index][-1:]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), runtime_list, width, hatch = None, alpha=0.99, color=bs_color, label="Binary Serial")
        runtime_ideal_r_list_bs_spm = []
        for i in range(len(runtime_list)):
            runtime_ideal_r_list_bs_spm.append(runtime_list[i] / time_ideal_list[index][-1:][i] - 1)

        # 8b - wospm - ur - 32c
        index = 2
        runtime_list = time_list[index][-1:]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), runtime_list, width, hatch = None, alpha=0.99, color=u6_color, label="Unary-32c")
        runtime_ideal_r_list_u6_wspm = []
        for i in range(len(runtime_list)):
            runtime_ideal_r_list_u6_wspm.append(runtime_list[i] / time_ideal_list[index][-1:][i] - 1)

        # 8b - wospm - ur - 64c
        index = 3
        runtime_list = time_list[index][-1:]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), runtime_list, width, hatch = None, alpha=0.99, color=u7_color, label="Unary-64c")
        runtime_ideal_r_list_u7_wspm = []
        for i in range(len(runtime_list)):
            runtime_ideal_r_list_u7_wspm.append(runtime_list[i] / time_ideal_list[index][-1:][i] - 1)

        # 8b - wospm - ur - 128c
        index = 4
        runtime_list = time_list[index][-1:]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), runtime_list, width, hatch = None, alpha=0.99, color=u8_color, label="Unary-128c")
        runtime_ideal_r_list_u8_wspm = []
        for i in range(len(runtime_list)):
            runtime_ideal_r_list_u8_wspm.append(runtime_list[i] / time_ideal_list[index][-1:][i] - 1)

        # 8b - wospm - ug - 256c
        index = 5
        runtime_list = time_list[index][-1:]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), runtime_list, width, hatch = None, alpha=0.99, color=ug_color, label="uGEMM-H")
        runtime_ideal_r_list_ug_wspm = []
        for i in range(len(runtime_list)):
            runtime_ideal_r_list_ug_wspm.append(runtime_list[i] / time_ideal_list[index][-1:][i] - 1)

        ax.set_ylabel('Runtime\n(Seconds)')
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        plt.xlim(x_idx[0]-0.5, x_idx[-1]+0.5)
        plt.yscale("log")

        _, top = plt.ylim()

        locs, labels = plt.yticks()
        if a == "eyeriss":
            locs = locs[1:-1]
        else:
            locs = locs[1:]
        ax.set_yticks(locs)
        
        bottom, _ = plt.ylim()
        if a == "eyeriss":
            ax.set_ylim((bottom, top*80))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top/80], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            ax.legend(loc="upper center", ncol=3, frameon=True)
        else:
            ax.set_ylim((bottom, top))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
        
        y_label_list = []
        for y in locs:
            if y != 0:
                y_label_list.append("{:1.0E}".format(abs(y)))
            else:
                y_label_list.append("0")
        ax.set_yticklabels(y_label_list)

        ax.minorticks_off()
        fig.tight_layout()
        plt.savefig('./outputs_fig/' + technode + '/Runtime_' + a_cap + ".pdf", bbox_inches='tight', dpi=my_dpi, pad_inches=0.02)

        if print_runtime:
            print("BP SPM overhead:  ", runtime_ideal_r_list_bp_spm)
            print("CONV mean: ", mean(runtime_ideal_r_list_bp_spm[0:5])*100, "%")
            print("BR SPM overhead:  ", runtime_ideal_r_list_bs_spm)
            print("CONV mean: ", mean(runtime_ideal_r_list_bs_spm[0:5])*100, "%")
            print("U6 WSPM overhead: ", runtime_ideal_r_list_u6_wspm)
            print("CONV mean: ", mean(runtime_ideal_r_list_u6_wspm[0:5])*100, "%")
            print("U7 WSPM overhead: ", runtime_ideal_r_list_u7_wspm)
            print("CONV mean: ", mean(runtime_ideal_r_list_u7_wspm[0:5])*100, "%")
            print("U8 WSPM overhead: ", runtime_ideal_r_list_u8_wspm)
            print("CONV mean: ", mean(runtime_ideal_r_list_u8_wspm[0:5])*100, "%")
            print("UG WSPM overhead: ", runtime_ideal_r_list_ug_wspm)
            print("CONV mean: ", mean(runtime_ideal_r_list_ug_wspm[0:5])*100, "%")

        print("Runtime fig saved!\n")


        # throughput
        my_dpi = 300
        if a == "eyeriss":
            fig_h = 1.1
        else:
            fig_h = 1
        fig_w = 3.3115

        bp_color = "#7A81FF"
        bs_color = "#FF7F7F"
        u6_color = "#666666"
        u7_color = "#888888"
        u8_color = "#AAAAAA"
        ug_color = "#CCCCCC"
        bg_color = "#D783FF"

        x_axis = ["Average"]

        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        
        idx_tot = 6

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width

        # 8b - spm - bp
        index = 0
        throughput_list_bp_spm = tp_list[index][-1:]
        idx = 1.5
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), throughput_list_bp_spm, width, hatch = None, alpha=0.99, color=bp_color, label="Binary Parallel")

        # 8b - spm - bs
        index = 1
        throughput_list_bs_spm = tp_list[index][-1:]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), throughput_list_bs_spm, width, hatch = None, alpha=0.99, color=bs_color, label="Binary Serial")

        # 8b - wospm - ur - 32c
        index = 2
        throughput_list_u6_wspm = tp_list[index][-1:]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), throughput_list_u6_wspm, width, hatch = None, alpha=0.99, color=u6_color, label="Unary-32c")

        # 8b - wospm - ur - 64c
        index = 3
        throughput_list_u7_wspm = tp_list[index][-1:]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), throughput_list_u7_wspm, width, hatch = None, alpha=0.99, color=u7_color, label="Unary-64c")

        # 8b - wospm - ur - 128c
        index = 4
        throughput_list_u8_wspm = tp_list[index][-1:]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), throughput_list_u8_wspm, width, hatch = None, alpha=0.99, color=u8_color, label="Unary-128c")

        # 8b - wospm - ug - 256c
        index = 5
        throughput_list_ug_wspm = tp_list[index][-1:]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), throughput_list_ug_wspm, width, hatch = None, alpha=0.99, color=ug_color, label="uGEMM-H")

        ax.set_ylabel('Throughput\n(Frames/s)')
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        plt.xlim(x_idx[0]-0.5, x_idx[-1]+0.5)
        plt.yscale("log")

        _, top = plt.ylim()

        locs, labels = plt.yticks()
        if a == "eyeriss":
            locs = locs[1:-1]
        else:
            locs = locs[1:]
        ax.set_yticks(locs)
        
        bottom, _ = plt.ylim()
        if a == "eyeriss":
            ax.set_ylim((bottom, top*60))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top/60], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            ax.legend(loc="upper center", ncol=3, frameon=True)
        else:
            ax.set_ylim((bottom, top))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
        
        y_label_list = []
        for y in locs:
            if y != 0:
                y_label_list.append("{:1.0E}".format(abs(y)))
            else:
                y_label_list.append("0")
        ax.set_yticklabels(y_label_list)

        ax.minorticks_off()
        fig.tight_layout()
        plt.savefig('./outputs_fig/' + technode + '/Throughput_' + a_cap + ".pdf", bbox_inches='tight', dpi=my_dpi, pad_inches=0.02)
        print("Throughput fig saved!\n")


        # energy
        my_dpi = 300
        if a == "eyeriss":
            fig_h = 1.3
        else:
            fig_h = 1
        fig_w = 3.3115

        bp_color = "#7A81FF"
        bs_color = "#FF7F7F"
        u6_color = "#666666"
        u7_color = "#888888"
        u8_color = "#AAAAAA"
        ug_color = "#CCCCCC"
        bg_color = "#D783FF"

        x_axis = ["Average"]

        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        
        idx_tot = 6

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width
        
        l_alpha = 0.8

        # 8b - spm - bp
        index = 0
        dram_d_list = energy_list[index * 5 + 0][-1:]
        sram_d_list = energy_list[index * 5 + 1][-1:]
        sram_l_list = energy_list[index * 5 + 2][-1:]
        sarr_d_list = energy_list[index * 5 + 3][-1:]
        sarr_l_list = energy_list[index * 5 + 4][-1:]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx = 1.5
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=bp_color, label='Binary Parallel')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=bp_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=bp_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=bp_color)

        # 8b - spm - bs
        index = 1
        dram_d_list = energy_list[index * 5 + 0][-1:]
        sram_d_list = energy_list[index * 5 + 1][-1:]
        sram_l_list = energy_list[index * 5 + 2][-1:]
        sarr_d_list = energy_list[index * 5 + 3][-1:]
        sarr_l_list = energy_list[index * 5 + 4][-1:]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=bs_color, label='Binary Serial')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=bs_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=bs_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=bs_color)

        # 8b - wospm - ur - 32c
        index = 2
        dram_d_list = energy_list[index * 5 + 0][-1:]
        sram_d_list = energy_list[index * 5 + 1][-1:]
        sram_l_list = energy_list[index * 5 + 2][-1:]
        sarr_d_list = energy_list[index * 5 + 3][-1:]
        sarr_l_list = energy_list[index * 5 + 4][-1:]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=u6_color, label='Unary-32c')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=u6_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=u6_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=u6_color)

        # 8b - wospm - ur - 64c
        index = 3
        dram_d_list = energy_list[index * 5 + 0][-1:]
        sram_d_list = energy_list[index * 5 + 1][-1:]
        sram_l_list = energy_list[index * 5 + 2][-1:]
        sarr_d_list = energy_list[index * 5 + 3][-1:]
        sarr_l_list = energy_list[index * 5 + 4][-1:]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=u7_color, label='Unary-64c')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=u7_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=u7_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=u7_color)

        # 8b - wospm - ur - 128c
        index = 4
        dram_d_list = energy_list[index * 5 + 0][-1:]
        sram_d_list = energy_list[index * 5 + 1][-1:]
        sram_l_list = energy_list[index * 5 + 2][-1:]
        sarr_d_list = energy_list[index * 5 + 3][-1:]
        sarr_l_list = energy_list[index * 5 + 4][-1:]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=u8_color, label='Unary-128c')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=u8_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=u8_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=u8_color)

        # 8b - wospm - ug - 256c
        index = 5
        dram_d_list = energy_list[index * 5 + 0][-1:]
        sram_d_list = energy_list[index * 5 + 1][-1:]
        sram_l_list = energy_list[index * 5 + 2][-1:]
        sarr_d_list = energy_list[index * 5 + 3][-1:]
        sarr_l_list = energy_list[index * 5 + 4][-1:]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=ug_color, label='uGEMM-H')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=ug_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=ug_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=ug_color)

        ax.set_ylabel('SRAM-SA energy\n(uJ)')
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        plt.xlim(x_idx[0]-0.5, x_idx[-1]+0.5)
        plt.yscale("symlog", linthresh=10000)
        bottom, top = plt.ylim()

        if a == "eyeriss":
            ax.set_ylim((bottom, top*8000))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top/8000], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            ax.legend(loc="upper center", ncol=3, frameon=True)
        else:
            ax.set_ylim((bottom, top))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
        ax.axhline(y=0, color="k", linewidth = 0.1)
        
        locs, labels = plt.yticks()
        if a == "eyeriss":
            locs = [-10000000, -100000, 0, 100000, 10000000]
        else:
            locs = [-1000000000, -10000000, -100000, 0, 100000, 10000000] 
        ax.set_yticks(locs)
        y_label_list = []
        for y in locs:
            if y != 0:
                y_label_list.append("{:1.0E}".format(abs(y)))
            else:
                y_label_list.append("0")
        ax.set_yticklabels(y_label_list)
        fig.tight_layout()
        plt.savefig('./outputs_fig/' + technode + '/Energy_' + a_cap + ".pdf", bbox_inches='tight', dpi=my_dpi, pad_inches=0.02)
        print("Energy fig saved!\n")



        # power
        my_dpi = 300
        if a == "eyeriss":
            fig_h = 2
        else:
            fig_h = 1
        fig_w = 3.3115

        bp_color = "#7A81FF"
        bs_color = "#FF7F7F"
        u6_color = "#666666"
        u7_color = "#888888"
        u8_color = "#AAAAAA"
        ug_color = "#CCCCCC"
        bg_color = "#D783FF"

        x_axis = ["Average"]

        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        
        idx_tot = 6

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width
        
        l_alpha = 0.8

        # 8b - spm - bp
        index = 0
        dram_d_list = power_list[index * 5 + 0][-1:]
        sram_d_list = power_list[index * 5 + 1][-1:]
        sram_l_list = power_list[index * 5 + 2][-1:]
        sarr_d_list = power_list[index * 5 + 3][-1:]
        sarr_l_list = power_list[index * 5 + 4][-1:]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx = 1.5
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=bp_color, label='Binary Parallel')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=bp_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=bp_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=bp_color)
        sram_d_list_bp_spm = []
        sram_dl_list_bp_spm = []
        for i in range(len(sram_d_list)):
            sram_d_list_bp_spm.append(sram_d_list[i])
            sram_dl_list_bp_spm.append(sram_d_list[i] + sram_l_list[i])

        # 8b - spm - bs
        index = 1
        dram_d_list = power_list[index * 5 + 0][-1:]
        sram_d_list = power_list[index * 5 + 1][-1:]
        sram_l_list = power_list[index * 5 + 2][-1:]
        sarr_d_list = power_list[index * 5 + 3][-1:]
        sarr_l_list = power_list[index * 5 + 4][-1:]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=bs_color, label='Binary Serial')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=bs_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=bs_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=bs_color)

        # 8b - wospm - ur - 32c
        index = 2
        dram_d_list = power_list[index * 5 + 0][-1:]
        sram_d_list = power_list[index * 5 + 1][-1:]
        sram_l_list = power_list[index * 5 + 2][-1:]
        sarr_d_list = power_list[index * 5 + 3][-1:]
        sarr_l_list = power_list[index * 5 + 4][-1:]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=u6_color, label='Unary-32c')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=u6_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=u6_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=u6_color)

        # 8b - wospm - ur - 64c
        index = 3
        dram_d_list = power_list[index * 5 + 0][-1:]
        sram_d_list = power_list[index * 5 + 1][-1:]
        sram_l_list = power_list[index * 5 + 2][-1:]
        sarr_d_list = power_list[index * 5 + 3][-1:]
        sarr_l_list = power_list[index * 5 + 4][-1:]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=u7_color, label='Unary-64c')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=u7_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=u7_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=u7_color)

        # 8b - wospm - ur - 128c
        index = 4
        dram_d_list = power_list[index * 5 + 0][-1:]
        sram_d_list = power_list[index * 5 + 1][-1:]
        sram_l_list = power_list[index * 5 + 2][-1:]
        sarr_d_list = power_list[index * 5 + 3][-1:]
        sarr_l_list = power_list[index * 5 + 4][-1:]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=u8_color, label='Unary-128c')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=u8_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=u8_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=u8_color)

        # 8b - wospm - ug - 256c
        index = 5
        dram_d_list = power_list[index * 5 + 0][-1:]
        sram_d_list = power_list[index * 5 + 1][-1:]
        sram_l_list = power_list[index * 5 + 2][-1:]
        sarr_d_list = power_list[index * 5 + 3][-1:]
        sarr_l_list = power_list[index * 5 + 4][-1:]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=ug_color, label='uGEMM-H')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=ug_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=ug_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=ug_color)

        ax.set_ylabel('SRAM-SA power\n(mW)')
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        plt.xlim(x_idx[0]-0.5, x_idx[-1]+0.5)
        plt.yscale("linear")
        bottom, top = plt.ylim()
        if a == "eyeriss":
            ax.set_ylim((-300, 100))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, 50], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            ax.legend(loc="upper center", ncol=3, frameon=True)
    
            y_tick_list = [-200, -100, 0, 100]
            ax.set_yticks(y_tick_list)
            y_label_list = []

            for y in y_tick_list:
                if y != 0:
                    y_label_list.append("{:1.0E}".format(abs(y)))
                else:
                    y_label_list.append("0")
            ax.set_yticklabels(y_label_list)
        else:
            ax.set_ylim((bottom, top))
            for x in x_idx:
                ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            
            y_tick_list = [-5000, 0, 5000]
            ax.set_yticks(y_tick_list)
            y_label_list = []

            for y in y_tick_list:
                if y != 0:
                    y_label_list.append("{:1.0E}".format(abs(y)))
                else:
                    y_label_list.append("0")
            ax.set_yticklabels(y_label_list)
        ax.axhline(y=0, color="k", linewidth = 0.1)
        
        fig.tight_layout()
        plt.savefig('./outputs_fig/' + technode + '/Power_' + a_cap + ".pdf", bbox_inches='tight', dpi=my_dpi, pad_inches=0.02)
        print("Power fig saved!\n")



        # total energy with dram
        my_dpi = 300
        if a == "eyeriss":
            fig_h = 1
        else:
            fig_h = 1
        fig_w = 3.3115

        bp_color = "#7A81FF"
        bs_color = "#FF7F7F"
        u6_color = "#666666"
        u7_color = "#888888"
        u8_color = "#AAAAAA"
        ug_color = "#CCCCCC"
        bg_color = "#D783FF"

        x_axis = ["Average"]

        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        
        idx_tot = 6

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width
        
        l_alpha = 0.8

        # 8b - spm - bp
        index = 0
        dram_d_list = energy_list[index * 5 + 0][-1:]
        sram_d_list = energy_list[index * 5 + 1][-1:]
        sram_l_list = energy_list[index * 5 + 2][-1:]
        sarr_d_list = energy_list[index * 5 + 3][-1:]
        sarr_l_list = energy_list[index * 5 + 4][-1:]
        total_energy_list_bp_spm = []
        onchip_energy_list_bp_spm = []
        for i in range(len(x_axis)):
            total_energy_list_bp_spm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_energy_list_bp_spm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx = 1.5
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_energy_list_bp_spm, width, hatch = None, alpha=0.99, color=bp_color, label='Binary Parallel')

        # 8b - spm - bs
        index = 1
        dram_d_list = energy_list[index * 5 + 0][-1:]
        sram_d_list = energy_list[index * 5 + 1][-1:]
        sram_l_list = energy_list[index * 5 + 2][-1:]
        sarr_d_list = energy_list[index * 5 + 3][-1:]
        sarr_l_list = energy_list[index * 5 + 4][-1:]
        total_energy_list_bs_spm = []
        onchip_energy_list_bs_spm = []
        for i in range(len(x_axis)):
            total_energy_list_bs_spm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_energy_list_bs_spm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_energy_list_bs_spm, width, hatch = None, alpha=0.99, color=bs_color, label='Binary Serial')

        onchip_energy_r_list_bs_spm = []
        for i in range(len(x_axis)):
            onchip_energy_r_list_bs_spm.append(1-onchip_energy_list_bs_spm[i]/onchip_energy_list_bp_spm[i])
        
        total_energy_r_list_bs_spm = []
        for i in range(len(x_axis)):
            total_energy_r_list_bs_spm.append(1 - total_energy_list_bs_spm[i]/total_energy_list_bp_spm[i])

        # 8b - wospm - ur - 32c
        index = 2
        dram_d_list = energy_list[index * 5 + 0][-1:]
        sram_d_list = energy_list[index * 5 + 1][-1:]
        sram_l_list = energy_list[index * 5 + 2][-1:]
        sarr_d_list = energy_list[index * 5 + 3][-1:]
        sarr_l_list = energy_list[index * 5 + 4][-1:]
        total_energy_list_u6_wspm = []
        onchip_energy_list_u6_wspm = []
        for i in range(len(x_axis)):
            total_energy_list_u6_wspm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_energy_list_u6_wspm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_energy_list_u6_wspm, width, hatch = None, alpha=0.99, color=u6_color, label='Unary-32c')

        onchip_energy_r_list_u6_wspm = []
        for i in range(len(x_axis)):
            onchip_energy_r_list_u6_wspm.append(1-onchip_energy_list_u6_wspm[i]/onchip_energy_list_bp_spm[i])
        
        total_energy_r_list_u6_wspm = []
        for i in range(len(x_axis)):
            total_energy_r_list_u6_wspm.append(1 - total_energy_list_u6_wspm[i]/total_energy_list_bp_spm[i])

        # 8b - wospm - ur - 64c
        index = 3
        dram_d_list = energy_list[index * 5 + 0][-1:]
        sram_d_list = energy_list[index * 5 + 1][-1:]
        sram_l_list = energy_list[index * 5 + 2][-1:]
        sarr_d_list = energy_list[index * 5 + 3][-1:]
        sarr_l_list = energy_list[index * 5 + 4][-1:]
        total_energy_list_u7_wspm = []
        onchip_energy_list_u7_wspm = []
        for i in range(len(x_axis)):
            total_energy_list_u7_wspm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_energy_list_u7_wspm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_energy_list_u7_wspm, width, hatch = None, alpha=0.99, color=u7_color, label='Unary-64c')

        onchip_energy_r_list_u7_wspm = []
        for i in range(len(x_axis)):
            onchip_energy_r_list_u7_wspm.append(1-onchip_energy_list_u7_wspm[i]/onchip_energy_list_bp_spm[i])
        
        total_energy_r_list_u7_wspm = []
        for i in range(len(x_axis)):
            total_energy_r_list_u7_wspm.append(1 - total_energy_list_u7_wspm[i]/total_energy_list_bp_spm[i])

        # 8b - wospm - ur - 128c
        index = 4
        dram_d_list = energy_list[index * 5 + 0][-1:]
        sram_d_list = energy_list[index * 5 + 1][-1:]
        sram_l_list = energy_list[index * 5 + 2][-1:]
        sarr_d_list = energy_list[index * 5 + 3][-1:]
        sarr_l_list = energy_list[index * 5 + 4][-1:]
        total_energy_list_u8_wspm = []
        onchip_energy_list_u8_wspm = []
        for i in range(len(x_axis)):
            total_energy_list_u8_wspm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_energy_list_u8_wspm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_energy_list_u8_wspm, width, hatch = None, alpha=0.99, color=u8_color, label='Unary-128c')

        onchip_energy_r_list_u8_wspm = []
        for i in range(len(x_axis)):
            onchip_energy_r_list_u8_wspm.append(1-onchip_energy_list_u8_wspm[i]/onchip_energy_list_bp_spm[i])
        
        total_energy_r_list_u8_wspm = []
        for i in range(len(x_axis)):
            total_energy_r_list_u8_wspm.append(1 - total_energy_list_u8_wspm[i]/total_energy_list_bp_spm[i])

         # 8b - wospm - ug - 256c
        index = 5
        dram_d_list = energy_list[index * 5 + 0][-1:]
        sram_d_list = energy_list[index * 5 + 1][-1:]
        sram_l_list = energy_list[index * 5 + 2][-1:]
        sarr_d_list = energy_list[index * 5 + 3][-1:]
        sarr_l_list = energy_list[index * 5 + 4][-1:]
        total_energy_list_ug_wspm = []
        onchip_energy_list_ug_wspm = []
        for i in range(len(x_axis)):
            total_energy_list_ug_wspm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_energy_list_ug_wspm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_energy_list_ug_wspm, width, hatch = None, alpha=0.99, color=ug_color, label='uGEMM-H')

        onchip_energy_r_list_ug_wspm = []
        for i in range(len(x_axis)):
            onchip_energy_r_list_ug_wspm.append(1-onchip_energy_list_ug_wspm[i]/onchip_energy_list_bp_spm[i])

        total_energy_r_list_ug_wspm = []
        for i in range(len(x_axis)):
            total_energy_r_list_ug_wspm.append(1 - total_energy_list_ug_wspm[i]/total_energy_list_bp_spm[i])

        ax.set_ylabel('Total energy\n(uJ)')
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        plt.xlim(x_idx[0]-0.5, x_idx[-1]+0.5)
        plt.yscale("log")

        _, top = plt.ylim()

        locs, labels = plt.yticks()
        if a == "eyeriss":
            locs = locs[1:]
        else:
            locs = locs[1:]
        ax.set_yticks(locs)
        
        bottom, _ = plt.ylim()
        if a == "eyeriss":
            ax.set_ylim((bottom, top))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
        else:
            ax.set_ylim((bottom, top))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
        
        y_label_list = []
        for y in locs:
            if y != 0:
                y_label_list.append("{:1.0E}".format(abs(y)))
            else:
                y_label_list.append("0")
        ax.set_yticklabels(y_label_list)

        ax.minorticks_off()
        fig.tight_layout()
        plt.savefig('./outputs_fig/' + technode + '/Energy_total_' + a_cap + ".pdf", bbox_inches='tight', dpi=my_dpi, pad_inches=0.02)

        if print_energy_onchip:
            print("On-chip energy reduction: ")
            print("binary parallel (baseline):", onchip_energy_list_bp_spm)
            print("binary serial             :", onchip_energy_r_list_bs_spm)
            print("unary 32c                 :", onchip_energy_r_list_u6_wspm)
            print("unary 64c                 :", onchip_energy_r_list_u7_wspm)
            print("unary 128c                :", onchip_energy_r_list_u8_wspm)
            print("ugemm 256c                :", onchip_energy_r_list_ug_wspm)
            print("min    reduction:", min(onchip_energy_r_list_u6_wspm + onchip_energy_r_list_u7_wspm + onchip_energy_r_list_u8_wspm)*100, "%")
            print("mean   reduction:", mean(onchip_energy_r_list_u6_wspm + onchip_energy_r_list_u7_wspm + onchip_energy_r_list_u8_wspm)*100, "%")
            print("median reduction:", median(onchip_energy_r_list_u6_wspm + onchip_energy_r_list_u7_wspm + onchip_energy_r_list_u8_wspm)*100, "%")
            print("max    reduction:", max(onchip_energy_r_list_u6_wspm + onchip_energy_r_list_u7_wspm + onchip_energy_r_list_u8_wspm)*100, "%")
            
            onchip_energy_bs_r_list_u6_wspm = []
            onchip_energy_bs_r_list_u7_wspm = []
            onchip_energy_bs_r_list_u8_wspm = []
            onchip_energy_bs_r_list_ug_wspm = []
            for i in range(len(onchip_energy_list_bs_spm)):
                onchip_energy_bs_r_list_u6_wspm.append(1 - onchip_energy_list_u6_wspm[i] / onchip_energy_list_bs_spm[i])
                onchip_energy_bs_r_list_u7_wspm.append(1 - onchip_energy_list_u7_wspm[i] / onchip_energy_list_bs_spm[i])
                onchip_energy_bs_r_list_u8_wspm.append(1 - onchip_energy_list_u8_wspm[i] / onchip_energy_list_bs_spm[i])
                onchip_energy_bs_r_list_ug_wspm.append(1 - onchip_energy_list_ug_wspm[i] / onchip_energy_list_bs_spm[i])
            print("binary serial (baseline)  :", onchip_energy_list_bs_spm)
            print("unary 32c                 :", onchip_energy_bs_r_list_u6_wspm)
            print("unary 64c                 :", onchip_energy_bs_r_list_u7_wspm)
            print("unary 128c                :", onchip_energy_bs_r_list_u8_wspm)
            print("ugemm 256c                :", onchip_energy_bs_r_list_ug_wspm)
            print("min    reduction:", min(onchip_energy_bs_r_list_u6_wspm + onchip_energy_bs_r_list_u7_wspm + onchip_energy_bs_r_list_u8_wspm)*100, "%")
            print("mean    reduction:", mean(onchip_energy_bs_r_list_u6_wspm + onchip_energy_bs_r_list_u7_wspm + onchip_energy_bs_r_list_u8_wspm)*100, "%")
            print("median reduction:", median(onchip_energy_bs_r_list_u6_wspm + onchip_energy_bs_r_list_u7_wspm + onchip_energy_bs_r_list_u8_wspm)*100, "%")
            print("max    reduction:", max(onchip_energy_bs_r_list_u6_wspm + onchip_energy_bs_r_list_u7_wspm + onchip_energy_bs_r_list_u8_wspm)*100, "%")

        if print_energy_total:
            print("Total energy reduction: ")
            print("binary parallel (baseline):", total_energy_list_bp_spm)
            print("binary serial             :", total_energy_r_list_bs_spm)
            print("unary 32c                 :", total_energy_r_list_u6_wspm)
            print("unary 64c                 :", total_energy_r_list_u7_wspm)
            print("unary 128c                :", total_energy_r_list_u8_wspm)
            print("ugemm 256c                :", total_energy_r_list_ug_wspm)
            print("min    reduction:", min(total_energy_r_list_u6_wspm + total_energy_r_list_u7_wspm + total_energy_r_list_u8_wspm)*100, "%")
            print("mean   reduction:", mean(total_energy_r_list_u6_wspm + total_energy_r_list_u7_wspm + total_energy_r_list_u8_wspm)*100, "%")
            print("median reduction:", median(total_energy_r_list_u6_wspm + total_energy_r_list_u7_wspm + total_energy_r_list_u8_wspm)*100, "%")
            print("max    reduction:", max(total_energy_r_list_u6_wspm + total_energy_r_list_u7_wspm + total_energy_r_list_u8_wspm)*100, "%")
            
            total_energy_bs_r_list_u6_wspm = []
            total_energy_bs_r_list_u7_wspm = []
            total_energy_bs_r_list_u8_wspm = []
            total_energy_bs_r_list_ug_wspm = []
            for i in range(len(total_energy_list_bs_spm)):
                total_energy_bs_r_list_u6_wspm.append(1 - total_energy_list_u6_wspm[i] / total_energy_list_bs_spm[i])
                total_energy_bs_r_list_u7_wspm.append(1 - total_energy_list_u7_wspm[i] / total_energy_list_bs_spm[i])
                total_energy_bs_r_list_u8_wspm.append(1 - total_energy_list_u8_wspm[i] / total_energy_list_bs_spm[i])
                total_energy_bs_r_list_ug_wspm.append(1 - total_energy_list_ug_wspm[i] / total_energy_list_bs_spm[i])
            print("binary serial (baseline)  :", total_energy_list_bs_spm)
            print("unary 32c                 :", total_energy_bs_r_list_u6_wspm)
            print("unary 64c                 :", total_energy_bs_r_list_u7_wspm)
            print("unary 128c                :", total_energy_bs_r_list_u8_wspm)
            print("ugemm 256c                :", total_energy_bs_r_list_ug_wspm)
            print("min    reduction:", min(total_energy_bs_r_list_u6_wspm + total_energy_bs_r_list_u7_wspm + total_energy_bs_r_list_u8_wspm)*100, "%")
            print("mean    reduction:", mean(total_energy_bs_r_list_u6_wspm + total_energy_bs_r_list_u7_wspm + total_energy_bs_r_list_u8_wspm)*100, "%")
            print("median reduction:", median(total_energy_bs_r_list_u6_wspm + total_energy_bs_r_list_u7_wspm + total_energy_bs_r_list_u8_wspm)*100, "%")
            print("max    reduction:", max(total_energy_bs_r_list_u6_wspm + total_energy_bs_r_list_u7_wspm + total_energy_bs_r_list_u8_wspm)*100, "%")

        # energy eff
        onchip_energy_eff_list_bp_spm = []
        onchip_energy_eff_list_bs_spm = []
        onchip_energy_eff_list_u6_wspm = []
        onchip_energy_eff_list_u7_wspm = []
        onchip_energy_eff_list_u8_wspm = []
        onchip_energy_eff_list_ug_wspm = []
        total_energy_eff_list_bp_spm = []
        total_energy_eff_list_bs_spm = []
        total_energy_eff_list_u6_wspm = []
        total_energy_eff_list_u7_wspm = []
        total_energy_eff_list_u8_wspm = []
        total_energy_eff_list_ug_wspm = []
        for i in range(len(throughput_list_bp_spm)):
            onchip_energy_eff_list_bp_spm.append(throughput_list_bp_spm[i] / onchip_energy_list_bp_spm[i])
            onchip_energy_eff_list_bs_spm.append(throughput_list_bs_spm[i] / onchip_energy_list_bs_spm[i])
            onchip_energy_eff_list_u6_wspm.append(throughput_list_u6_wspm[i] / onchip_energy_list_u6_wspm[i])
            onchip_energy_eff_list_u7_wspm.append(throughput_list_u7_wspm[i] / onchip_energy_list_u7_wspm[i])
            onchip_energy_eff_list_u8_wspm.append(throughput_list_u8_wspm[i] / onchip_energy_list_u8_wspm[i])
            onchip_energy_eff_list_ug_wspm.append(throughput_list_ug_wspm[i] / onchip_energy_list_ug_wspm[i])
            total_energy_eff_list_bp_spm.append(throughput_list_bp_spm[i] / total_energy_list_bp_spm[i])
            total_energy_eff_list_bs_spm.append(throughput_list_bs_spm[i] / total_energy_list_bs_spm[i])
            total_energy_eff_list_u6_wspm.append(throughput_list_u6_wspm[i] / total_energy_list_u6_wspm[i])
            total_energy_eff_list_u7_wspm.append(throughput_list_u7_wspm[i] / total_energy_list_u7_wspm[i])
            total_energy_eff_list_u8_wspm.append(throughput_list_u8_wspm[i] / total_energy_list_u8_wspm[i])
            total_energy_eff_list_ug_wspm.append(throughput_list_ug_wspm[i] / total_energy_list_ug_wspm[i])

        onchip_energy_eff_bp_r_list_bs_spm = []
        onchip_energy_eff_bp_r_list_u6_wspm = []
        onchip_energy_eff_bp_r_list_u7_wspm = []
        onchip_energy_eff_bp_r_list_u8_wspm = []
        onchip_energy_eff_bp_r_list_ug_wspm = []
        total_energy_eff_bp_r_list_bs_spm = []
        total_energy_eff_bp_r_list_u6_wspm = []
        total_energy_eff_bp_r_list_u7_wspm = []
        total_energy_eff_bp_r_list_u8_wspm = []
        total_energy_eff_bp_r_list_ug_wspm = []
        onchip_energy_eff_bs_r_list_u6_wspm = []
        onchip_energy_eff_bs_r_list_u7_wspm = []
        onchip_energy_eff_bs_r_list_u8_wspm = []
        onchip_energy_eff_bs_r_list_ug_wspm = []
        total_energy_eff_bs_r_list_u6_wspm = []
        total_energy_eff_bs_r_list_u7_wspm = []
        total_energy_eff_bs_r_list_u8_wspm = []
        total_energy_eff_bs_r_list_ug_wspm = []
        onchip_energy_eff_ug_r_list_u6_wspm = []
        onchip_energy_eff_ug_r_list_u7_wspm = []
        onchip_energy_eff_ug_r_list_u8_wspm = []
        total_energy_eff_ug_r_list_u6_wspm = []
        total_energy_eff_ug_r_list_u7_wspm = []
        total_energy_eff_ug_r_list_u8_wspm = []
        for i in range(len(throughput_list_bp_spm)):
            onchip_energy_eff_bp_r_list_bs_spm.append(onchip_energy_eff_list_bs_spm[i] / onchip_energy_eff_list_bp_spm[i] - 1)
            onchip_energy_eff_bp_r_list_u6_wspm.append(onchip_energy_eff_list_u6_wspm[i] / onchip_energy_eff_list_bp_spm[i] - 1)
            onchip_energy_eff_bp_r_list_u7_wspm.append(onchip_energy_eff_list_u7_wspm[i] / onchip_energy_eff_list_bp_spm[i] - 1)
            onchip_energy_eff_bp_r_list_u8_wspm.append(onchip_energy_eff_list_u8_wspm[i] / onchip_energy_eff_list_bp_spm[i] - 1)
            onchip_energy_eff_bp_r_list_ug_wspm.append(onchip_energy_eff_list_ug_wspm[i] / onchip_energy_eff_list_bp_spm[i] - 1)
            total_energy_eff_bp_r_list_bs_spm.append(total_energy_eff_list_bs_spm[i] / total_energy_eff_list_bp_spm[i] - 1)
            total_energy_eff_bp_r_list_u6_wspm.append(total_energy_eff_list_u6_wspm[i] / total_energy_eff_list_bp_spm[i] - 1)
            total_energy_eff_bp_r_list_u7_wspm.append(total_energy_eff_list_u7_wspm[i] / total_energy_eff_list_bp_spm[i] - 1)
            total_energy_eff_bp_r_list_u8_wspm.append(total_energy_eff_list_u8_wspm[i] / total_energy_eff_list_bp_spm[i] - 1)
            total_energy_eff_bp_r_list_ug_wspm.append(total_energy_eff_list_ug_wspm[i] / total_energy_eff_list_bp_spm[i] - 1)
            onchip_energy_eff_bs_r_list_u6_wspm.append(onchip_energy_eff_list_u6_wspm[i] / onchip_energy_eff_list_bs_spm[i] - 1)
            onchip_energy_eff_bs_r_list_u7_wspm.append(onchip_energy_eff_list_u7_wspm[i] / onchip_energy_eff_list_bs_spm[i] - 1)
            onchip_energy_eff_bs_r_list_u8_wspm.append(onchip_energy_eff_list_u8_wspm[i] / onchip_energy_eff_list_bs_spm[i] - 1)
            onchip_energy_eff_bs_r_list_ug_wspm.append(onchip_energy_eff_list_ug_wspm[i] / onchip_energy_eff_list_bs_spm[i] - 1)
            total_energy_eff_bs_r_list_u6_wspm.append(total_energy_eff_list_u6_wspm[i] / total_energy_eff_list_bs_spm[i] - 1)
            total_energy_eff_bs_r_list_u7_wspm.append(total_energy_eff_list_u7_wspm[i] / total_energy_eff_list_bs_spm[i] - 1)
            total_energy_eff_bs_r_list_u8_wspm.append(total_energy_eff_list_u8_wspm[i] / total_energy_eff_list_bs_spm[i] - 1)
            total_energy_eff_bs_r_list_ug_wspm.append(total_energy_eff_list_ug_wspm[i] / total_energy_eff_list_bs_spm[i] - 1)
            onchip_energy_eff_ug_r_list_u6_wspm.append(onchip_energy_eff_list_u6_wspm[i] / onchip_energy_eff_list_ug_wspm[i] - 1)
            onchip_energy_eff_ug_r_list_u7_wspm.append(onchip_energy_eff_list_u7_wspm[i] / onchip_energy_eff_list_ug_wspm[i] - 1)
            onchip_energy_eff_ug_r_list_u8_wspm.append(onchip_energy_eff_list_u8_wspm[i] / onchip_energy_eff_list_ug_wspm[i] - 1)
            total_energy_eff_ug_r_list_u6_wspm.append(total_energy_eff_list_u6_wspm[i] / total_energy_eff_list_ug_wspm[i] - 1)
            total_energy_eff_ug_r_list_u7_wspm.append(total_energy_eff_list_u7_wspm[i] / total_energy_eff_list_ug_wspm[i] - 1)
            total_energy_eff_ug_r_list_u8_wspm.append(total_energy_eff_list_u8_wspm[i] / total_energy_eff_list_ug_wspm[i] - 1)

        if print_energy_eff:
            print("On-chip energy efficiency improve: ")
            onchip_energy_eff_bp_r_list_ux_wspm_min = min(onchip_energy_eff_bp_r_list_u6_wspm + onchip_energy_eff_bp_r_list_u7_wspm + onchip_energy_eff_bp_r_list_u8_wspm)
            onchip_energy_eff_bp_r_list_ux_wspm_mean = mean(onchip_energy_eff_bp_r_list_u6_wspm + onchip_energy_eff_bp_r_list_u7_wspm + onchip_energy_eff_bp_r_list_u8_wspm)
            onchip_energy_eff_bp_r_list_ux_wspm_median = median(onchip_energy_eff_bp_r_list_u6_wspm + onchip_energy_eff_bp_r_list_u7_wspm + onchip_energy_eff_bp_r_list_u8_wspm)
            onchip_energy_eff_bp_r_list_ux_wspm_max = max(onchip_energy_eff_bp_r_list_u6_wspm + onchip_energy_eff_bp_r_list_u7_wspm + onchip_energy_eff_bp_r_list_u8_wspm)
            print("binary parallel (baseline):", onchip_energy_eff_list_bp_spm)
            print("binary serial             :", onchip_energy_eff_bp_r_list_bs_spm)
            print("unary 32c                 :", onchip_energy_eff_bp_r_list_u6_wspm)
            print("unary 64c                 :", onchip_energy_eff_bp_r_list_u7_wspm)
            print("unary 128c                :", onchip_energy_eff_bp_r_list_u8_wspm)
            print("ugemm 256c                :", onchip_energy_eff_bp_r_list_ug_wspm)
            print("min    improve:", onchip_energy_eff_bp_r_list_ux_wspm_min*100, "%")
            print("mean   improve:", onchip_energy_eff_bp_r_list_ux_wspm_mean*100, "%")
            print("median improve:", onchip_energy_eff_bp_r_list_ux_wspm_median*100, "%")
            print("max    improve:", onchip_energy_eff_bp_r_list_ux_wspm_max*100, "%")

            onchip_energy_eff_bs_r_list_ux_wspm_min = min(onchip_energy_eff_bs_r_list_u6_wspm + onchip_energy_eff_bs_r_list_u7_wspm + onchip_energy_eff_bs_r_list_u8_wspm)
            onchip_energy_eff_bs_r_list_ux_wspm_mean = mean(onchip_energy_eff_bs_r_list_u6_wspm + onchip_energy_eff_bs_r_list_u7_wspm + onchip_energy_eff_bs_r_list_u8_wspm)
            onchip_energy_eff_bs_r_list_ux_wspm_median = median(onchip_energy_eff_bs_r_list_u6_wspm + onchip_energy_eff_bs_r_list_u7_wspm + onchip_energy_eff_bs_r_list_u8_wspm)
            onchip_energy_eff_bs_r_list_ux_wspm_max = max(onchip_energy_eff_bs_r_list_u6_wspm + onchip_energy_eff_bs_r_list_u7_wspm + onchip_energy_eff_bs_r_list_u8_wspm)
            print("binary serial (baseline)  :", onchip_energy_eff_list_bs_spm)
            print("unary 32c                 :", onchip_energy_eff_bs_r_list_u6_wspm)
            print("unary 64c                 :", onchip_energy_eff_bs_r_list_u7_wspm)
            print("unary 128c                :", onchip_energy_eff_bs_r_list_u8_wspm)
            print("ugemm 256c                :", onchip_energy_eff_bs_r_list_ug_wspm)
            print("min    improve:", onchip_energy_eff_bs_r_list_ux_wspm_min*100, "%")
            print("mean   improve:", onchip_energy_eff_bs_r_list_ux_wspm_mean*100, "%")
            print("median improve:", onchip_energy_eff_bs_r_list_ux_wspm_median*100, "%")
            print("max    improve:", onchip_energy_eff_bs_r_list_ux_wspm_max*100, "%")

            onchip_energy_eff_ug_r_list_ux_wspm_min = min(onchip_energy_eff_ug_r_list_u6_wspm + onchip_energy_eff_ug_r_list_u7_wspm + onchip_energy_eff_ug_r_list_u8_wspm)
            onchip_energy_eff_ug_r_list_ux_wspm_mean = mean(onchip_energy_eff_ug_r_list_u6_wspm + onchip_energy_eff_ug_r_list_u7_wspm + onchip_energy_eff_ug_r_list_u8_wspm)
            onchip_energy_eff_ug_r_list_ux_wspm_median = median(onchip_energy_eff_ug_r_list_u6_wspm + onchip_energy_eff_ug_r_list_u7_wspm + onchip_energy_eff_ug_r_list_u8_wspm)
            onchip_energy_eff_ug_r_list_ux_wspm_max = max(onchip_energy_eff_ug_r_list_u6_wspm + onchip_energy_eff_ug_r_list_u7_wspm + onchip_energy_eff_ug_r_list_u8_wspm)
            print("unary 256c (baseline)     :", onchip_energy_eff_list_ug_wspm)
            print("unary 32c                 :", onchip_energy_eff_ug_r_list_u6_wspm)
            print("unary 64c                 :", onchip_energy_eff_ug_r_list_u7_wspm)
            print("unary 128c                :", onchip_energy_eff_ug_r_list_u8_wspm)
            print("min    improve:", onchip_energy_eff_ug_r_list_ux_wspm_min*100, "%")
            print("mean   improve:", onchip_energy_eff_ug_r_list_ux_wspm_mean*100, "%")
            print("median improve:", onchip_energy_eff_ug_r_list_ux_wspm_median*100, "%")
            print("max    improve:", onchip_energy_eff_ug_r_list_ux_wspm_max*100, "%")

            print("Total energy efficiency improve: ")
            total_energy_eff_bp_r_list_ux_wspm_min = min(total_energy_eff_bp_r_list_u6_wspm + total_energy_eff_bp_r_list_u7_wspm + total_energy_eff_bp_r_list_u8_wspm)
            total_energy_eff_bp_r_list_ux_wspm_mean = mean(total_energy_eff_bp_r_list_u6_wspm + total_energy_eff_bp_r_list_u7_wspm + total_energy_eff_bp_r_list_u8_wspm)
            total_energy_eff_bp_r_list_ux_wspm_median = median(total_energy_eff_bp_r_list_u6_wspm + total_energy_eff_bp_r_list_u7_wspm + total_energy_eff_bp_r_list_u8_wspm)
            total_energy_eff_bp_r_list_ux_wspm_max = max(total_energy_eff_bp_r_list_u6_wspm + total_energy_eff_bp_r_list_u7_wspm + total_energy_eff_bp_r_list_u8_wspm)
            print("binary parallel (baseline):", total_energy_eff_list_bp_spm)
            print("binary serial             :", total_energy_eff_bp_r_list_bs_spm)
            print("unary 32c                 :", total_energy_eff_bp_r_list_u6_wspm)
            print("unary 64c                 :", total_energy_eff_bp_r_list_u7_wspm)
            print("unary 128c                :", total_energy_eff_bp_r_list_u8_wspm)
            print("ugemm 256c                :", total_energy_eff_bp_r_list_ug_wspm)
            print("min    improve:", total_energy_eff_bp_r_list_ux_wspm_min*100, "%")
            print("mean   improve:", total_energy_eff_bp_r_list_ux_wspm_mean*100, "%")
            print("median improve:", total_energy_eff_bp_r_list_ux_wspm_median*100, "%")
            print("max    improve:", total_energy_eff_bp_r_list_ux_wspm_max*100, "%")

            total_energy_eff_bs_r_list_ux_wspm_min = min(total_energy_eff_bs_r_list_u6_wspm + total_energy_eff_bs_r_list_u7_wspm + total_energy_eff_bs_r_list_u8_wspm)
            total_energy_eff_bs_r_list_ux_wspm_mean = mean(total_energy_eff_bs_r_list_u6_wspm + total_energy_eff_bs_r_list_u7_wspm + total_energy_eff_bs_r_list_u8_wspm)
            total_energy_eff_bs_r_list_ux_wspm_median = median(total_energy_eff_bs_r_list_u6_wspm + total_energy_eff_bs_r_list_u7_wspm + total_energy_eff_bs_r_list_u8_wspm)
            total_energy_eff_bs_r_list_ux_wspm_max = max(total_energy_eff_bs_r_list_u6_wspm + total_energy_eff_bs_r_list_u7_wspm + total_energy_eff_bs_r_list_u8_wspm)
            print("binary serial (baseline)  :", total_energy_eff_list_bs_spm)
            print("unary 32c                 :", total_energy_eff_bs_r_list_u6_wspm)
            print("unary 64c                 :", total_energy_eff_bs_r_list_u7_wspm)
            print("unary 128c                :", total_energy_eff_bs_r_list_u8_wspm)
            print("ugemm 256c                :", total_energy_eff_bs_r_list_ug_wspm)
            print("min    improve:", total_energy_eff_bs_r_list_ux_wspm_min*100, "%")
            print("mean   improve:", total_energy_eff_bs_r_list_ux_wspm_mean*100, "%")
            print("median improve:", total_energy_eff_bs_r_list_ux_wspm_median*100, "%")
            print("max    improve:", total_energy_eff_bs_r_list_ux_wspm_max*100, "%")

            total_energy_eff_ug_r_list_ux_wspm_min = min(total_energy_eff_ug_r_list_u6_wspm + total_energy_eff_ug_r_list_u7_wspm + total_energy_eff_ug_r_list_u8_wspm)
            total_energy_eff_ug_r_list_ux_wspm_mean = mean(total_energy_eff_ug_r_list_u6_wspm + total_energy_eff_ug_r_list_u7_wspm + total_energy_eff_ug_r_list_u8_wspm)
            total_energy_eff_ug_r_list_ux_wspm_median = median(total_energy_eff_ug_r_list_u6_wspm + total_energy_eff_ug_r_list_u7_wspm + total_energy_eff_ug_r_list_u8_wspm)
            total_energy_eff_ug_r_list_ux_wspm_max = max(total_energy_eff_ug_r_list_u6_wspm + total_energy_eff_ug_r_list_u7_wspm + total_energy_eff_ug_r_list_u8_wspm)
            print("ugemm 256c (baseline)     :", total_energy_eff_list_ug_wspm)
            print("unary 32c                 :", total_energy_eff_ug_r_list_u6_wspm)
            print("unary 64c                 :", total_energy_eff_ug_r_list_u7_wspm)
            print("unary 128c                :", total_energy_eff_ug_r_list_u8_wspm)
            print("min    improve:", total_energy_eff_ug_r_list_ux_wspm_min*100, "%")
            print("mean   improve:", total_energy_eff_ug_r_list_ux_wspm_mean*100, "%")
            print("median improve:", total_energy_eff_ug_r_list_ux_wspm_median*100, "%")
            print("max    improve:", total_energy_eff_ug_r_list_ux_wspm_max*100, "%")

            print("__________________________________________________________________________________________________")
            print("binary parallel | on-chip | ", onchip_energy_eff_bp_r_list_ux_wspm_min, onchip_energy_eff_bp_r_list_ux_wspm_mean, onchip_energy_eff_bp_r_list_ux_wspm_max)
            print("                __________________________________________________________________________________")
            print("                | total   | ", total_energy_eff_bp_r_list_ux_wspm_min, total_energy_eff_bp_r_list_ux_wspm_mean, total_energy_eff_bp_r_list_ux_wspm_max)
            print("__________________________________________________________________________________________________")
            print("binary serial   | on-chip | ", onchip_energy_eff_bs_r_list_ux_wspm_min, onchip_energy_eff_bs_r_list_ux_wspm_mean, onchip_energy_eff_bs_r_list_ux_wspm_max)
            print("                __________________________________________________________________________________")
            print("                | total   | ", total_energy_eff_bs_r_list_ux_wspm_min, total_energy_eff_bs_r_list_ux_wspm_mean, total_energy_eff_bs_r_list_ux_wspm_max)
            print("__________________________________________________________________________________________________")
            print("ugemm 256c      | on-chip | ", onchip_energy_eff_ug_r_list_ux_wspm_min, onchip_energy_eff_ug_r_list_ux_wspm_mean, onchip_energy_eff_ug_r_list_ux_wspm_max)
            print("                __________________________________________________________________________________")
            print("                | total   | ", total_energy_eff_ug_r_list_ux_wspm_min, total_energy_eff_ug_r_list_ux_wspm_mean, total_energy_eff_ug_r_list_ux_wspm_max)
            print("__________________________________________________________________________________________________")


        print("Energy total fig saved!\n")


        # total power with dram
        my_dpi = 300
        if a == "eyeriss":
            fig_h = 1
        else:
            fig_h = 1
        fig_w = 3.3115

        bp_color = "#7A81FF"
        bs_color = "#FF7F7F"
        u6_color = "#666666"
        u7_color = "#888888"
        u8_color = "#AAAAAA"
        ug_color = "#CCCCCC"
        bg_color = "#D783FF"

        x_axis = ["Average"]

        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        
        idx_tot = 6

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width
        
        l_alpha = 0.8

        # 8b - spm - bp
        index = 0
        dram_d_list = power_list[index * 5 + 0][-1:]
        sram_d_list = power_list[index * 5 + 1][-1:]
        sram_l_list = power_list[index * 5 + 2][-1:]
        sarr_d_list = power_list[index * 5 + 3][-1:]
        sarr_l_list = power_list[index * 5 + 4][-1:]
        total_power_list_bp_spm = []
        onchip_power_list_bp_spm = []
        for i in range(len(x_axis)):
            total_power_list_bp_spm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_power_list_bp_spm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx = 1.5
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_power_list_bp_spm, width, hatch = None, alpha=0.99, color=bp_color, label='Binary Parallel')


        # 8b - spm - bs
        index = 1
        dram_d_list = power_list[index * 5 + 0][-1:]
        sram_d_list = power_list[index * 5 + 1][-1:]
        sram_l_list = power_list[index * 5 + 2][-1:]
        sarr_d_list = power_list[index * 5 + 3][-1:]
        sarr_l_list = power_list[index * 5 + 4][-1:]
        total_power_list_bs_spm = []
        onchip_power_list_bs_spm = []
        for i in range(len(x_axis)):
            total_power_list_bs_spm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_power_list_bs_spm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_power_list_bs_spm, width, hatch = None, alpha=0.99, color=bs_color, label='Binary Serial')

        onchip_power_r_list_bs_spm = []
        for i in range(len(x_axis)):
            onchip_power_r_list_bs_spm.append(1-onchip_power_list_bs_spm[i]/onchip_power_list_bp_spm[i])
        
        total_power_r_list_bs_spm = []
        for i in range(len(x_axis)):
            total_power_r_list_bs_spm.append(1 - total_power_list_bs_spm[i]/total_power_list_bp_spm[i])

        # 8b - wospm - ur - 32c
        index = 2
        dram_d_list = power_list[index * 5 + 0][-1:]
        sram_d_list = power_list[index * 5 + 1][-1:]
        sram_l_list = power_list[index * 5 + 2][-1:]
        sarr_d_list = power_list[index * 5 + 3][-1:]
        sarr_l_list = power_list[index * 5 + 4][-1:]
        total_power_list_u6_wspm = []
        onchip_power_list_u6_wspm = []
        for i in range(len(x_axis)):
            total_power_list_u6_wspm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_power_list_u6_wspm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_power_list_u6_wspm, width, hatch = None, alpha=0.99, color=u6_color, label='Unary-32c')

        onchip_power_r_list_u6_wspm = []
        for i in range(len(x_axis)):
            onchip_power_r_list_u6_wspm.append(1-onchip_power_list_u6_wspm[i]/onchip_power_list_bp_spm[i])
        
        total_power_r_list_u6_wspm = []
        for i in range(len(x_axis)):
            total_power_r_list_u6_wspm.append(1 - total_power_list_u6_wspm[i]/total_power_list_bp_spm[i])

        # 8b - wospm - ur - 64c
        index = 3
        dram_d_list = power_list[index * 5 + 0][-1:]
        sram_d_list = power_list[index * 5 + 1][-1:]
        sram_l_list = power_list[index * 5 + 2][-1:]
        sarr_d_list = power_list[index * 5 + 3][-1:]
        sarr_l_list = power_list[index * 5 + 4][-1:]
        total_power_list_u7_wspm = []
        onchip_power_list_u7_wspm = []
        for i in range(len(x_axis)):
            total_power_list_u7_wspm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_power_list_u7_wspm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_power_list_u7_wspm, width, hatch = None, alpha=0.99, color=u7_color, label='Unary-64c')

        onchip_power_r_list_u7_wspm = []
        for i in range(len(x_axis)):
            onchip_power_r_list_u7_wspm.append(1-onchip_power_list_u7_wspm[i]/onchip_power_list_bp_spm[i])
        
        total_power_r_list_u7_wspm = []
        for i in range(len(x_axis)):
            total_power_r_list_u7_wspm.append(1 - total_power_list_u7_wspm[i]/total_power_list_bp_spm[i])

        # 8b - wospm - ur - 128c
        index = 4
        dram_d_list = power_list[index * 5 + 0][-1:]
        sram_d_list = power_list[index * 5 + 1][-1:]
        sram_l_list = power_list[index * 5 + 2][-1:]
        sarr_d_list = power_list[index * 5 + 3][-1:]
        sarr_l_list = power_list[index * 5 + 4][-1:]
        total_power_list_u8_wspm = []
        onchip_power_list_u8_wspm = []
        for i in range(len(x_axis)):
            total_power_list_u8_wspm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_power_list_u8_wspm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_power_list_u8_wspm, width, hatch = None, alpha=0.99, color=u8_color, label='Unary-128c')

        onchip_power_r_list_u8_wspm = []
        for i in range(len(x_axis)):
            onchip_power_r_list_u8_wspm.append(1-onchip_power_list_u8_wspm[i]/onchip_power_list_bp_spm[i])
        
        total_power_r_list_u8_wspm = []
        for i in range(len(x_axis)):
            total_power_r_list_u8_wspm.append(1 - total_power_list_u8_wspm[i]/total_power_list_bp_spm[i])

        # 8b - wospm - ug - 256c
        index = 5
        dram_d_list = power_list[index * 5 + 0][-1:]
        sram_d_list = power_list[index * 5 + 1][-1:]
        sram_l_list = power_list[index * 5 + 2][-1:]
        sarr_d_list = power_list[index * 5 + 3][-1:]
        sarr_l_list = power_list[index * 5 + 4][-1:]
        total_power_list_ug_wspm = []
        onchip_power_list_ug_wspm = []
        for i in range(len(x_axis)):
            total_power_list_ug_wspm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_power_list_ug_wspm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_power_list_ug_wspm, width, hatch = None, alpha=0.99, color=ug_color, label='uGEMM-H')

        onchip_power_r_list_ug_wspm = []
        for i in range(len(x_axis)):
            onchip_power_r_list_ug_wspm.append(1-onchip_power_list_ug_wspm[i]/onchip_power_list_bp_spm[i])

        total_power_r_list_ug_wspm = []
        for i in range(len(x_axis)):
            total_power_r_list_ug_wspm.append(1 - total_power_list_ug_wspm[i]/total_power_list_bp_spm[i])

        ax.set_ylabel('Total power\n(mW)')
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        plt.xlim(x_idx[0]-0.5, x_idx[-1]+0.5)
        plt.yscale("linear")

        bottom, top = plt.ylim()
        if a == "eyeriss":
            ax.set_ylim(bottom, 2500)
            for x in x_idx:
                ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            ax.text(0-1.5*width, 2600, "{:.2f}".format(total_power_list_bp_spm[0]), horizontalalignment="right")
            ax.text(0-0.5*width, 2600, "{:.2f}".format(total_power_list_bs_spm[0]), horizontalalignment="left")

            y_tick_list = [0, 1000, 2000]
            ax.set_yticks(y_tick_list)
            y_label_list = []

            for y in y_tick_list:
                if y != 0:
                    y_label_list.append("{:1.0E}".format(abs(y)))
                else:
                    y_label_list.append("0")
            ax.set_yticklabels(y_label_list)
        else:
            ax.set_ylim(bottom, top)
            for x in x_idx:
                ax.fill_betweenx([bottom, top+2000], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            y_tick_list = [0, 5000, 10000]
            ax.set_yticks(y_tick_list)
            y_label_list = []

            for y in y_tick_list:
                if y != 0:
                    y_label_list.append("{:1.0E}".format(abs(y)))
                else:
                    y_label_list.append("0")
            ax.set_yticklabels(y_label_list)

        ax.minorticks_off()
        fig.tight_layout()
        plt.savefig('./outputs_fig/' + technode + '/Power_total_' + a_cap + ".pdf", bbox_inches='tight', dpi=my_dpi, pad_inches=0.02)

        if print_power_onchip:
            print("On-chip power reduction: ")
            print("binary parallel (baseline):", onchip_power_list_bp_spm)
            print("binary serial             :", onchip_power_r_list_bs_spm)
            print("unary 32c                 :", onchip_power_r_list_u6_wspm)
            print("unary 64c                 :", onchip_power_r_list_u7_wspm)
            print("unary 128c                :", onchip_power_r_list_u8_wspm)
            print("ugemm 256c                :", onchip_power_r_list_ug_wspm)
            print("min    reduction:", min(onchip_power_r_list_u6_wspm + onchip_power_r_list_u7_wspm + onchip_power_r_list_u8_wspm)*100, "%")
            print("mean    reduction:", mean(onchip_power_r_list_u6_wspm + onchip_power_r_list_u7_wspm + onchip_power_r_list_u8_wspm)*100, "%")
            print("median reduction:", median(onchip_power_r_list_u6_wspm + onchip_power_r_list_u7_wspm + onchip_power_r_list_u8_wspm)*100, "%")
            print("max    reduction:", max(onchip_power_r_list_u6_wspm + onchip_power_r_list_u7_wspm + onchip_power_r_list_u8_wspm)*100, "%")

            onchip_power_bs_r_list_u6_wspm = []
            onchip_power_bs_r_list_u7_wspm = []
            onchip_power_bs_r_list_u8_wspm = []
            onchip_power_bs_r_list_ug_wspm = []
            for i in range(len(onchip_power_list_bs_spm)):
                onchip_power_bs_r_list_u6_wspm.append(1 - onchip_power_list_u6_wspm[i] / onchip_power_list_bs_spm[i])
                onchip_power_bs_r_list_u7_wspm.append(1 - onchip_power_list_u7_wspm[i] / onchip_power_list_bs_spm[i])
                onchip_power_bs_r_list_u8_wspm.append(1 - onchip_power_list_u8_wspm[i] / onchip_power_list_bs_spm[i])
                onchip_power_bs_r_list_ug_wspm.append(1 - onchip_power_list_ug_wspm[i] / onchip_power_list_bs_spm[i])
            print("binary serial (baseline)  :", onchip_power_list_bs_spm)
            print("unary 32c                 :", onchip_power_bs_r_list_u6_wspm)
            print("unary 64c                 :", onchip_power_bs_r_list_u7_wspm)
            print("unary 128c                :", onchip_power_bs_r_list_u8_wspm)
            print("ugemm 256c                :", onchip_power_bs_r_list_ug_wspm)
            print("min    reduction:", min(onchip_power_bs_r_list_u6_wspm + onchip_power_bs_r_list_u7_wspm + onchip_power_bs_r_list_u8_wspm)*100, "%")
            print("mean    reduction:", mean(onchip_power_bs_r_list_u6_wspm + onchip_power_bs_r_list_u7_wspm + onchip_power_bs_r_list_u8_wspm)*100, "%")
            print("median reduction:", median(onchip_power_bs_r_list_u6_wspm + onchip_power_bs_r_list_u7_wspm + onchip_power_bs_r_list_u8_wspm)*100, "%")
            print("max    reduction:", max(onchip_power_bs_r_list_u6_wspm + onchip_power_bs_r_list_u7_wspm + onchip_power_bs_r_list_u8_wspm)*100, "%")

            onchip_power_ug_r_list_u6_wspm = []
            onchip_power_ug_r_list_u7_wspm = []
            onchip_power_ug_r_list_u8_wspm = []
            for i in range(len(onchip_power_list_ug_wspm)):
                onchip_power_ug_r_list_u6_wspm.append(1 - onchip_power_list_u6_wspm[i] / onchip_power_list_ug_wspm[i])
                onchip_power_ug_r_list_u7_wspm.append(1 - onchip_power_list_u7_wspm[i] / onchip_power_list_ug_wspm[i])
                onchip_power_ug_r_list_u8_wspm.append(1 - onchip_power_list_u8_wspm[i] / onchip_power_list_ug_wspm[i])
            print("ugemm 256c    (baseline)  :", onchip_power_list_ug_wspm)
            print("unary 32c                 :", onchip_power_ug_r_list_u6_wspm)
            print("unary 64c                 :", onchip_power_ug_r_list_u7_wspm)
            print("unary 128c                :", onchip_power_ug_r_list_u8_wspm)
            print("min    reduction:", min(onchip_power_ug_r_list_u6_wspm + onchip_power_ug_r_list_u7_wspm + onchip_power_ug_r_list_u8_wspm)*100, "%")
            print("mean    reduction:", mean(onchip_power_ug_r_list_u6_wspm + onchip_power_ug_r_list_u7_wspm + onchip_power_ug_r_list_u8_wspm)*100, "%")
            print("median reduction:", median(onchip_power_ug_r_list_u6_wspm + onchip_power_ug_r_list_u7_wspm + onchip_power_ug_r_list_u8_wspm)*100, "%")
            print("max    reduction:", max(onchip_power_ug_r_list_u6_wspm + onchip_power_ug_r_list_u7_wspm + onchip_power_ug_r_list_u8_wspm)*100, "%")

        if print_power_total:
            print("Total power reduction: ")
            print("binary parallel (baseline):", total_power_list_bp_spm)
            print("binary serial             :", total_power_r_list_bs_spm)
            print("unary 32c                 :", total_power_r_list_u6_wspm)
            print("unary 64c                 :", total_power_r_list_u7_wspm)
            print("unary 128c                :", total_power_r_list_u8_wspm)
            print("ugemm 256c                :", total_power_r_list_ug_wspm)
            print("min    reduction:", min(total_power_r_list_u6_wspm + total_power_r_list_u7_wspm + total_power_r_list_u8_wspm)*100, "%")
            print("mean   reduction:", mean(total_power_r_list_u6_wspm + total_power_r_list_u7_wspm + total_power_r_list_u8_wspm)*100, "%")
            print("median reduction:", median(total_power_r_list_u6_wspm + total_power_r_list_u7_wspm + total_power_r_list_u8_wspm)*100, "%")
            print("max    reduction:", max(total_power_r_list_u6_wspm + total_power_r_list_u7_wspm + total_power_r_list_u8_wspm)*100, "%")

            total_power_bs_r_list_u6_wspm = []
            total_power_bs_r_list_u7_wspm = []
            total_power_bs_r_list_u8_wspm = []
            total_power_bs_r_list_ug_wspm = []
            for i in range(len(total_power_list_bs_spm)):
                total_power_bs_r_list_u6_wspm.append(1 - total_power_list_u6_wspm[i] / total_power_list_bs_spm[i])
                total_power_bs_r_list_u7_wspm.append(1 - total_power_list_u7_wspm[i] / total_power_list_bs_spm[i])
                total_power_bs_r_list_u8_wspm.append(1 - total_power_list_u8_wspm[i] / total_power_list_bs_spm[i])
                total_power_bs_r_list_ug_wspm.append(1 - total_power_list_ug_wspm[i] / total_power_list_bs_spm[i])
            print("binary serial (baseline)  :", total_power_list_bs_spm)
            print("unary 32c                 :", total_power_bs_r_list_u6_wspm)
            print("unary 64c                 :", total_power_bs_r_list_u7_wspm)
            print("unary 128c                :", total_power_bs_r_list_u8_wspm)
            print("ugemm 256c                :", total_power_bs_r_list_ug_wspm)
            print("min    reduction:", min(total_power_bs_r_list_u6_wspm + total_power_bs_r_list_u7_wspm + total_power_bs_r_list_u8_wspm)*100, "%")
            print("mean    reduction:", mean(total_power_bs_r_list_u6_wspm + total_power_bs_r_list_u7_wspm + total_power_bs_r_list_u8_wspm)*100, "%")
            print("median reduction:", median(total_power_bs_r_list_u6_wspm + total_power_bs_r_list_u7_wspm + total_power_bs_r_list_u8_wspm)*100, "%")
            print("max    reduction:", max(total_power_bs_r_list_u6_wspm + total_power_bs_r_list_u7_wspm + total_power_bs_r_list_u8_wspm)*100, "%")

            total_power_ug_r_list_u6_wspm = []
            total_power_ug_r_list_u7_wspm = []
            total_power_ug_r_list_u8_wspm = []
            for i in range(len(total_power_list_ug_wspm)):
                total_power_ug_r_list_u6_wspm.append(1 - total_power_list_u6_wspm[i] / total_power_list_ug_wspm[i])
                total_power_ug_r_list_u7_wspm.append(1 - total_power_list_u7_wspm[i] / total_power_list_ug_wspm[i])
                total_power_ug_r_list_u8_wspm.append(1 - total_power_list_u8_wspm[i] / total_power_list_ug_wspm[i])
            print("ugemm 256c (baseline)    :", total_power_list_ug_wspm)
            print("unary 32c                 :", total_power_ug_r_list_u6_wspm)
            print("unary 64c                 :", total_power_ug_r_list_u7_wspm)
            print("unary 128c                :", total_power_ug_r_list_u8_wspm)
            print("min    reduction:", min(total_power_ug_r_list_u6_wspm + total_power_ug_r_list_u7_wspm + total_power_ug_r_list_u8_wspm)*100, "%")
            print("mean    reduction:", mean(total_power_ug_r_list_u6_wspm + total_power_ug_r_list_u7_wspm + total_power_ug_r_list_u8_wspm)*100, "%")
            print("median reduction:", median(total_power_ug_r_list_u6_wspm + total_power_ug_r_list_u7_wspm + total_power_ug_r_list_u8_wspm)*100, "%")
            print("max    reduction:", max(total_power_ug_r_list_u6_wspm + total_power_ug_r_list_u7_wspm + total_power_ug_r_list_u8_wspm)*100, "%")

        # power eff
        onchip_power_eff_list_bp_spm = []
        onchip_power_eff_list_bs_spm = []
        onchip_power_eff_list_u6_wspm = []
        onchip_power_eff_list_u7_wspm = []
        onchip_power_eff_list_u8_wspm = []
        onchip_power_eff_list_ug_wspm = []
        total_power_eff_list_bp_spm = []
        total_power_eff_list_bs_spm = []
        total_power_eff_list_u6_wspm = []
        total_power_eff_list_u7_wspm = []
        total_power_eff_list_u8_wspm = []
        total_power_eff_list_ug_wspm = []
        for i in range(len(throughput_list_bp_spm)):
            onchip_power_eff_list_bp_spm.append(throughput_list_bp_spm[i] / onchip_power_list_bp_spm[i])
            onchip_power_eff_list_bs_spm.append(throughput_list_bs_spm[i] / onchip_power_list_bs_spm[i])
            onchip_power_eff_list_u6_wspm.append(throughput_list_u6_wspm[i] / onchip_power_list_u6_wspm[i])
            onchip_power_eff_list_u7_wspm.append(throughput_list_u7_wspm[i] / onchip_power_list_u7_wspm[i])
            onchip_power_eff_list_u8_wspm.append(throughput_list_u8_wspm[i] / onchip_power_list_u8_wspm[i])
            onchip_power_eff_list_ug_wspm.append(throughput_list_ug_wspm[i] / onchip_power_list_ug_wspm[i])
            total_power_eff_list_bp_spm.append(throughput_list_bp_spm[i] / total_power_list_bp_spm[i])
            total_power_eff_list_bs_spm.append(throughput_list_bs_spm[i] / total_power_list_bs_spm[i])
            total_power_eff_list_u6_wspm.append(throughput_list_u6_wspm[i] / total_power_list_u6_wspm[i])
            total_power_eff_list_u7_wspm.append(throughput_list_u7_wspm[i] / total_power_list_u7_wspm[i])
            total_power_eff_list_u8_wspm.append(throughput_list_u8_wspm[i] / total_power_list_u8_wspm[i])
            total_power_eff_list_ug_wspm.append(throughput_list_ug_wspm[i] / total_power_list_ug_wspm[i])

        onchip_power_eff_bp_r_list_bs_spm = []
        onchip_power_eff_bp_r_list_u6_wspm = []
        onchip_power_eff_bp_r_list_u7_wspm = []
        onchip_power_eff_bp_r_list_u8_wspm = []
        onchip_power_eff_bp_r_list_ug_wspm = []
        total_power_eff_bp_r_list_bs_spm = []
        total_power_eff_bp_r_list_u6_wspm = []
        total_power_eff_bp_r_list_u7_wspm = []
        total_power_eff_bp_r_list_u8_wspm = []
        total_power_eff_bp_r_list_ug_wspm = []
        onchip_power_eff_bs_r_list_u6_wspm = []
        onchip_power_eff_bs_r_list_u7_wspm = []
        onchip_power_eff_bs_r_list_u8_wspm = []
        onchip_power_eff_bs_r_list_ug_wspm = []
        total_power_eff_bs_r_list_u6_wspm = []
        total_power_eff_bs_r_list_u7_wspm = []
        total_power_eff_bs_r_list_u8_wspm = []
        total_power_eff_bs_r_list_ug_wspm = []
        onchip_power_eff_ug_r_list_u6_wspm = []
        onchip_power_eff_ug_r_list_u7_wspm = []
        onchip_power_eff_ug_r_list_u8_wspm = []
        total_power_eff_ug_r_list_u6_wspm = []
        total_power_eff_ug_r_list_u7_wspm = []
        total_power_eff_ug_r_list_u8_wspm = []
        for i in range(len(throughput_list_bp_spm)):
            onchip_power_eff_bp_r_list_bs_spm.append(onchip_power_eff_list_bs_spm[i] / onchip_power_eff_list_bp_spm[i] - 1)
            onchip_power_eff_bp_r_list_u6_wspm.append(onchip_power_eff_list_u6_wspm[i] / onchip_power_eff_list_bp_spm[i] - 1)
            onchip_power_eff_bp_r_list_u7_wspm.append(onchip_power_eff_list_u7_wspm[i] / onchip_power_eff_list_bp_spm[i] - 1)
            onchip_power_eff_bp_r_list_u8_wspm.append(onchip_power_eff_list_u8_wspm[i] / onchip_power_eff_list_bp_spm[i] - 1)
            onchip_power_eff_bp_r_list_ug_wspm.append(onchip_power_eff_list_ug_wspm[i] / onchip_power_eff_list_bp_spm[i] - 1)
            total_power_eff_bp_r_list_bs_spm.append(total_power_eff_list_bs_spm[i] / total_power_eff_list_bp_spm[i] - 1)
            total_power_eff_bp_r_list_u6_wspm.append(total_power_eff_list_u6_wspm[i] / total_power_eff_list_bp_spm[i] - 1)
            total_power_eff_bp_r_list_u7_wspm.append(total_power_eff_list_u7_wspm[i] / total_power_eff_list_bp_spm[i] - 1)
            total_power_eff_bp_r_list_u8_wspm.append(total_power_eff_list_u8_wspm[i] / total_power_eff_list_bp_spm[i] - 1)
            total_power_eff_bp_r_list_ug_wspm.append(total_power_eff_list_ug_wspm[i] / total_power_eff_list_bp_spm[i] - 1)
            onchip_power_eff_bs_r_list_u6_wspm.append(onchip_power_eff_list_u6_wspm[i] / onchip_power_eff_list_bs_spm[i] - 1)
            onchip_power_eff_bs_r_list_u7_wspm.append(onchip_power_eff_list_u7_wspm[i] / onchip_power_eff_list_bs_spm[i] - 1)
            onchip_power_eff_bs_r_list_u8_wspm.append(onchip_power_eff_list_u8_wspm[i] / onchip_power_eff_list_bs_spm[i] - 1)
            onchip_power_eff_bs_r_list_ug_wspm.append(onchip_power_eff_list_ug_wspm[i] / onchip_power_eff_list_bs_spm[i] - 1)
            total_power_eff_bs_r_list_u6_wspm.append(total_power_eff_list_u6_wspm[i] / total_power_eff_list_bs_spm[i] - 1)
            total_power_eff_bs_r_list_u7_wspm.append(total_power_eff_list_u7_wspm[i] / total_power_eff_list_bs_spm[i] - 1)
            total_power_eff_bs_r_list_u8_wspm.append(total_power_eff_list_u8_wspm[i] / total_power_eff_list_bs_spm[i - 1])
            total_power_eff_bs_r_list_ug_wspm.append(total_power_eff_list_ug_wspm[i] / total_power_eff_list_bs_spm[i - 1])
            onchip_power_eff_ug_r_list_u6_wspm.append(onchip_power_eff_list_u6_wspm[i] / onchip_power_eff_list_ug_wspm[i] - 1)
            onchip_power_eff_ug_r_list_u7_wspm.append(onchip_power_eff_list_u7_wspm[i] / onchip_power_eff_list_ug_wspm[i] - 1)
            onchip_power_eff_ug_r_list_u8_wspm.append(onchip_power_eff_list_u8_wspm[i] / onchip_power_eff_list_ug_wspm[i] - 1)
            total_power_eff_ug_r_list_u6_wspm.append(total_power_eff_list_u6_wspm[i] / total_power_eff_list_ug_wspm[i] - 1)
            total_power_eff_ug_r_list_u7_wspm.append(total_power_eff_list_u7_wspm[i] / total_power_eff_list_ug_wspm[i] - 1)
            total_power_eff_ug_r_list_u8_wspm.append(total_power_eff_list_u8_wspm[i] / total_power_eff_list_ug_wspm[i - 1])

        # plot eff
        my_dpi = 300
        if a == "eyeriss":
            fig_h = 0.8
        else:
            fig_h = 0.8
        fig_w = 3.3115

        bp_color = "#7A81FF"
        bs_color = "#FF7F7F"
        u6_color = "#666666"
        u7_color = "#888888"
        u8_color = "#AAAAAA"
        ug_color = "#CCCCCC"
        bg_color = "#D783FF"

        x_axis = ["Over Binary Parallel", "Over Binary Serial"]
        x_idx = np.arange(len(x_axis))

        width = 0.1

        eff_fig, eff_ax = plt.subplots(figsize=(fig_w, fig_h))
        eff_ax.bar(x_idx - 3.5 * width, [mean(onchip_energy_eff_bp_r_list_u6_wspm), mean(onchip_energy_eff_bs_r_list_u6_wspm)], width, hatch = None, alpha=0.99, color=u6_color, label='Unary-32c')
        eff_ax.bar(x_idx - 2.5 * width, [mean(onchip_energy_eff_bp_r_list_u7_wspm), mean(onchip_energy_eff_bs_r_list_u7_wspm)], width, hatch = None, alpha=0.99, color=u7_color, label='Unary-64c')
        eff_ax.bar(x_idx - 1.5 * width, [mean(onchip_energy_eff_bp_r_list_u8_wspm), mean(onchip_energy_eff_bs_r_list_u8_wspm)], width, hatch = None, alpha=0.99, color=u8_color, label='Unary-128c')
        eff_ax.bar(x_idx - 0.5 * width, [mean(onchip_energy_eff_bp_r_list_ug_wspm), mean(onchip_energy_eff_bs_r_list_ug_wspm)], width, hatch = None, alpha=0.99, color=ug_color, label='uGEMM-H')
        eff_ax.set_ylabel('E.E.I.'+r'($\times$)')
        eff_ax.minorticks_off()
        if print_power_eff:
            print("max onchip energy eff improve for all layers: ", mean(onchip_energy_eff_bp_r_list_u6_wspm))

        eff_ax2 = eff_ax.twinx()
        eff_ax2.bar(x_idx + 0.5 * width, [mean(onchip_power_eff_bp_r_list_u6_wspm), mean(onchip_power_eff_bs_r_list_u6_wspm)], width, hatch = None, alpha=0.99, color=u6_color)
        eff_ax2.bar(x_idx + 1.5 * width, [mean(onchip_power_eff_bp_r_list_u7_wspm), mean(onchip_power_eff_bs_r_list_u7_wspm)], width, hatch = None, alpha=0.99, color=u7_color)
        eff_ax2.bar(x_idx + 2.5 * width, [mean(onchip_power_eff_bp_r_list_u8_wspm), mean(onchip_power_eff_bs_r_list_u8_wspm)], width, hatch = None, alpha=0.99, color=u8_color)
        eff_ax2.bar(x_idx + 3.5 * width, [mean(onchip_power_eff_bp_r_list_ug_wspm), mean(onchip_power_eff_bs_r_list_ug_wspm)], width, hatch = None, alpha=0.99, color=ug_color)
        eff_ax2.set_ylabel('P.E.I.'+r'($\times$)')
        eff_ax2.minorticks_off()
        if print_power_eff:
            print("max onchip power eff improve for all layers: ", mean(onchip_power_eff_bp_r_list_u6_wspm))

        eff_ax.set_xticks(x_idx)
        eff_ax.set_xticklabels(x_axis)
        plt.xlim(x_idx[0]-0.5, x_idx[-1]+0.5)
        plt.yscale("linear")
        
        if a == "eyeriss":
            eff_ax.set_ylim((-1, 4))
            eff_ax.set_yticks([0, 3])
            eff_ax.set_yticklabels(["{:3d}".format(0), "{:3d}".format(3)])
            eff_ax2.set_ylim((-4, 16))
            eff_ax2.set_yticks([0, 12])
            eff_ax2.set_yticklabels(["{:2d}".format(0), "{:2d}".format(12)])
            bottom, top = eff_ax.get_ylim()
            for x in x_idx:
                eff_ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            eff_ax.axhline(y=0, color="k", linewidth = 0.1)
            eff_ax2.axhline(y=0, color="k", linewidth = 0.1)
        else:
            eff_ax.set_ylim((0, 80))
            eff_ax.set_yticks([0, 50])
            eff_ax.set_yticklabels(["{:3d}".format(0), "{:3d}".format(50)])
            eff_ax2.set_ylim((0, 16))
            eff_ax2.set_yticks([0, 10])
            eff_ax2.set_yticklabels(["{:2d}".format(0), "{:2d}".format(10)])
            for x in x_idx:
                eff_ax2.fill_betweenx([0, 40], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
        
        # if a == "eyeriss":
        #     eff_ax.legend(loc="upper center", ncol=3, frameon=True)
        # else:
        #     pass

        eff_fig.tight_layout()
        plt.savefig('./outputs_fig/' + technode + '/Energy_power_eff_onchip_mlperf_' + a_cap + ".pdf", bbox_inches='tight', dpi=my_dpi, pad_inches=0.02)


        if print_power_eff:
            print("On-chip power efficiency improve: ")
            onchip_power_eff_bp_r_list_ux_wspm_min = min(onchip_power_eff_bp_r_list_u6_wspm + onchip_power_eff_bp_r_list_u7_wspm + onchip_power_eff_bp_r_list_u8_wspm)
            onchip_power_eff_bp_r_list_ux_wspm_mean = mean(onchip_power_eff_bp_r_list_u6_wspm + onchip_power_eff_bp_r_list_u7_wspm + onchip_power_eff_bp_r_list_u8_wspm)
            onchip_power_eff_bp_r_list_ux_wspm_median = median(onchip_power_eff_bp_r_list_u6_wspm + onchip_power_eff_bp_r_list_u7_wspm + onchip_power_eff_bp_r_list_u8_wspm)
            onchip_power_eff_bp_r_list_ux_wspm_max = max(onchip_power_eff_bp_r_list_u6_wspm + onchip_power_eff_bp_r_list_u7_wspm + onchip_power_eff_bp_r_list_u8_wspm)
            print("binary parallel (baseline):", onchip_power_eff_list_bp_spm)
            print("binary serial             :", onchip_power_eff_bp_r_list_bs_spm)
            print("unary 32c                 :", onchip_power_eff_bp_r_list_u6_wspm)
            print("unary 64c                 :", onchip_power_eff_bp_r_list_u7_wspm)
            print("unary 128c                :", onchip_power_eff_bp_r_list_u8_wspm)
            print("ugemm 256c                :", onchip_power_eff_bp_r_list_ug_wspm)
            print("min    improve:", onchip_power_eff_bp_r_list_ux_wspm_min*100, "%")
            print("mean   improve:", onchip_power_eff_bp_r_list_ux_wspm_mean*100, "%")
            print("median improve:", onchip_power_eff_bp_r_list_ux_wspm_median*100, "%")
            print("max    improve:", onchip_power_eff_bp_r_list_ux_wspm_max*100, "%")

            onchip_power_eff_bs_r_list_ux_wspm_min = min(onchip_power_eff_bs_r_list_u6_wspm + onchip_power_eff_bs_r_list_u7_wspm + onchip_power_eff_bs_r_list_u8_wspm)
            onchip_power_eff_bs_r_list_ux_wspm_mean = mean(onchip_power_eff_bs_r_list_u6_wspm + onchip_power_eff_bs_r_list_u7_wspm + onchip_power_eff_bs_r_list_u8_wspm)
            onchip_power_eff_bs_r_list_ux_wspm_median = median(onchip_power_eff_bs_r_list_u6_wspm + onchip_power_eff_bs_r_list_u7_wspm + onchip_power_eff_bs_r_list_u8_wspm)
            onchip_power_eff_bs_r_list_ux_wspm_max = max(onchip_power_eff_bs_r_list_u6_wspm + onchip_power_eff_bs_r_list_u7_wspm + onchip_power_eff_bs_r_list_u8_wspm)
            print("binary serial (baseline)  :", onchip_power_eff_list_bs_spm)
            print("unary 32c                 :", onchip_power_eff_bs_r_list_u6_wspm)
            print("unary 64c                 :", onchip_power_eff_bs_r_list_u7_wspm)
            print("unary 128c                :", onchip_power_eff_bs_r_list_u8_wspm)
            print("ugemm 256c                :", onchip_power_eff_bs_r_list_ug_wspm)
            print("min    improve:", onchip_power_eff_bs_r_list_ux_wspm_min*100, "%")
            print("mean   improve:", onchip_power_eff_bs_r_list_ux_wspm_mean*100, "%")
            print("median improve:", onchip_power_eff_bs_r_list_ux_wspm_median*100, "%")
            print("max    improve:", onchip_power_eff_bs_r_list_ux_wspm_max*100, "%")

            onchip_power_eff_ug_r_list_ux_wspm_min = min(onchip_power_eff_ug_r_list_u6_wspm + onchip_power_eff_ug_r_list_u7_wspm + onchip_power_eff_ug_r_list_u8_wspm)
            onchip_power_eff_ug_r_list_ux_wspm_mean = mean(onchip_power_eff_ug_r_list_u6_wspm + onchip_power_eff_ug_r_list_u7_wspm + onchip_power_eff_ug_r_list_u8_wspm)
            onchip_power_eff_ug_r_list_ux_wspm_median = median(onchip_power_eff_ug_r_list_u6_wspm + onchip_power_eff_ug_r_list_u7_wspm + onchip_power_eff_ug_r_list_u8_wspm)
            onchip_power_eff_ug_r_list_ux_wspm_max = max(onchip_power_eff_ug_r_list_u6_wspm + onchip_power_eff_ug_r_list_u7_wspm + onchip_power_eff_ug_r_list_u8_wspm)
            print("ugemm 256c (baseline)     :", onchip_power_eff_list_ug_wspm)
            print("unary 32c                 :", onchip_power_eff_ug_r_list_u6_wspm)
            print("unary 64c                 :", onchip_power_eff_ug_r_list_u7_wspm)
            print("unary 128c                :", onchip_power_eff_ug_r_list_u8_wspm)
            print("min    improve:", onchip_power_eff_ug_r_list_ux_wspm_min*100, "%")
            print("mean   improve:", onchip_power_eff_ug_r_list_ux_wspm_mean*100, "%")
            print("median improve:", onchip_power_eff_ug_r_list_ux_wspm_median*100, "%")
            print("max    improve:", onchip_power_eff_ug_r_list_ux_wspm_max*100, "%")

            print("Total power efficiency improve: ")
            total_power_eff_bp_r_list_ux_wspm_min = min(total_power_eff_bp_r_list_u6_wspm + total_power_eff_bp_r_list_u7_wspm + total_power_eff_bp_r_list_u8_wspm)
            total_power_eff_bp_r_list_ux_wspm_mean = mean(total_power_eff_bp_r_list_u6_wspm + total_power_eff_bp_r_list_u7_wspm + total_power_eff_bp_r_list_u8_wspm)
            total_power_eff_bp_r_list_ux_wspm_median = median(total_power_eff_bp_r_list_u6_wspm + total_power_eff_bp_r_list_u7_wspm + total_power_eff_bp_r_list_u8_wspm)
            total_power_eff_bp_r_list_ux_wspm_max = max(total_power_eff_bp_r_list_u6_wspm + total_power_eff_bp_r_list_u7_wspm + total_power_eff_bp_r_list_u8_wspm)
            print("binary parallel (baseline):", total_power_eff_list_bp_spm)
            print("binary serial             :", total_power_eff_bp_r_list_bs_spm)
            print("unary 32c                 :", total_power_eff_bp_r_list_u6_wspm)
            print("unary 64c                 :", total_power_eff_bp_r_list_u7_wspm)
            print("unary 128c                :", total_power_eff_bp_r_list_u8_wspm)
            print("ugemm 256c                :", total_power_eff_bp_r_list_ug_wspm)
            print("min    improve:", total_power_eff_bp_r_list_ux_wspm_min*100, "%")
            print("mean   improve:", total_power_eff_bp_r_list_ux_wspm_mean*100, "%")
            print("median improve:", total_power_eff_bp_r_list_ux_wspm_median*100, "%")
            print("max    improve:", total_power_eff_bp_r_list_ux_wspm_max*100, "%")

            total_power_eff_bs_r_list_ux_wspm_min = min(total_power_eff_bs_r_list_u6_wspm + total_power_eff_bs_r_list_u7_wspm + total_power_eff_bs_r_list_u8_wspm)
            total_power_eff_bs_r_list_ux_wspm_mean = mean(total_power_eff_bs_r_list_u6_wspm + total_power_eff_bs_r_list_u7_wspm + total_power_eff_bs_r_list_u8_wspm)
            total_power_eff_bs_r_list_ux_wspm_median = median(total_power_eff_bs_r_list_u6_wspm + total_power_eff_bs_r_list_u7_wspm + total_power_eff_bs_r_list_u8_wspm)
            total_power_eff_bs_r_list_ux_wspm_max = max(total_power_eff_bs_r_list_u6_wspm + total_power_eff_bs_r_list_u7_wspm + total_power_eff_bs_r_list_u8_wspm)
            print("binary serial (baseline)  :", total_power_eff_list_bs_spm)
            print("unary 32c                 :", total_power_eff_bs_r_list_u6_wspm)
            print("unary 64c                 :", total_power_eff_bs_r_list_u7_wspm)
            print("unary 128c                :", total_power_eff_bs_r_list_u8_wspm)
            print("ugemm 256c                :", total_power_eff_bs_r_list_ug_wspm)
            print("min    improve:", total_power_eff_bs_r_list_ux_wspm_min*100, "%")
            print("mean   improve:", total_power_eff_bs_r_list_ux_wspm_mean*100, "%")
            print("median improve:", total_power_eff_bs_r_list_ux_wspm_median*100, "%")
            print("max    improve:", total_power_eff_bs_r_list_ux_wspm_max*100, "%")

            total_power_eff_ug_r_list_ux_wspm_min = min(total_power_eff_ug_r_list_u6_wspm + total_power_eff_ug_r_list_u7_wspm + total_power_eff_ug_r_list_u8_wspm)
            total_power_eff_ug_r_list_ux_wspm_mean = mean(total_power_eff_ug_r_list_u6_wspm + total_power_eff_ug_r_list_u7_wspm + total_power_eff_ug_r_list_u8_wspm)
            total_power_eff_ug_r_list_ux_wspm_median = median(total_power_eff_ug_r_list_u6_wspm + total_power_eff_ug_r_list_u7_wspm + total_power_eff_ug_r_list_u8_wspm)
            total_power_eff_ug_r_list_ux_wspm_max = max(total_power_eff_ug_r_list_u6_wspm + total_power_eff_ug_r_list_u7_wspm + total_power_eff_ug_r_list_u8_wspm)
            print("ugemm 256c (baseline)     :", total_power_eff_list_ug_wspm)
            print("unary 32c                 :", total_power_eff_ug_r_list_u6_wspm)
            print("unary 64c                 :", total_power_eff_ug_r_list_u7_wspm)
            print("unary 128c                :", total_power_eff_ug_r_list_u8_wspm)
            print("min    improve:", total_power_eff_ug_r_list_ux_wspm_min*100, "%")
            print("mean   improve:", total_power_eff_ug_r_list_ux_wspm_mean*100, "%")
            print("median improve:", total_power_eff_ug_r_list_ux_wspm_median*100, "%")
            print("max    improve:", total_power_eff_ug_r_list_ux_wspm_max*100, "%")

            print("__________________________________________________________________________________________________")
            print("binary parallel | on-chip | ", onchip_power_eff_bp_r_list_ux_wspm_min, onchip_power_eff_bp_r_list_ux_wspm_mean, onchip_power_eff_bp_r_list_ux_wspm_max)
            print("                __________________________________________________________________________________")
            print("                | total   | ", total_power_eff_bp_r_list_ux_wspm_min, total_power_eff_bp_r_list_ux_wspm_mean, total_power_eff_bp_r_list_ux_wspm_max)
            print("__________________________________________________________________________________________________")
            print("binary serial   | on-chip | ", onchip_power_eff_bs_r_list_ux_wspm_min, onchip_power_eff_bs_r_list_ux_wspm_mean, onchip_power_eff_bs_r_list_ux_wspm_max)
            print("                __________________________________________________________________________________")
            print("                | total   | ", total_power_eff_bs_r_list_ux_wspm_min, total_power_eff_bs_r_list_ux_wspm_mean, total_power_eff_bs_r_list_ux_wspm_max)
            print("__________________________________________________________________________________________________")
            print("ugemm 256c      | on-chip | ", onchip_power_eff_ug_r_list_ux_wspm_min, onchip_power_eff_ug_r_list_ux_wspm_mean, onchip_power_eff_ug_r_list_ux_wspm_max)
            print("                __________________________________________________________________________________")
            print("                | total   | ", total_power_eff_ug_r_list_ux_wspm_min, total_power_eff_ug_r_list_ux_wspm_mean, total_power_eff_ug_r_list_ux_wspm_max)
            print("__________________________________________________________________________________________________")
            
        print("Power total fig saved!\n")
        
        print("Energy power efficiency onchip fig saved!\n")

        print()


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
