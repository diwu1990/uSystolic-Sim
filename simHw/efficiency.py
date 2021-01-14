import math
import simHw.block_trace as block_trace
import simHw.cacti_result as cacti
from os import listdir
from os.path import isfile, join
import configparser as cp

def estimate(
    array_h=4,
    array_w=4,
    ifmap_sram_size=1, # in K-Word
    filter_sram_size=1, # in K-Word
    ofmap_sram_size=1, # in K-Word
    word_sz_bytes=1, # bytes per word
    ifmap_base=0, # in word
    filter_base=10000000, # in word
    ofmap_base=20000000, # in word
    sram_cfg_file=None,
    dram_cfg_file=None,
    pe_cfg_file=None,
    computing=None,
    run_name=None,
    topology_file=None,
    access_buf=True
):
    """
    this code run CACTI according to the configuration of ifmap, filter, ofmap to get power and energy
    1) it calculates the required numbre of banks for SRAM/DRAM (ifmap, filter and ofmap SRAM, as well DRAM)
    2) it profiles the trace file from architecture simulation, and report the required bank count for memory
    3) the cacti result, together with the run time reported from architecture simulation, will generate the total power and total enery for each component
    """
    param_file = open(topology_file, 'r')
    first = True
    
    ifmap_sram_size *= 1024 # in word
    filter_sram_size *= 1024 # in word
    ofmap_sram_size *= 1024 # in word

    ifmap_sram_exist = (ifmap_sram_size > 0)
    filter_sram_exist = (filter_sram_size > 0)
    ofmap_sram_exist = (ofmap_sram_size > 0)

    # sram data
    tot_word_ifmap_rd_sram = 0
    max_word_ifmap_rd_sram = 0
    tot_access_ifmap_rd_sram = 0
    max_access_ifmap_rd_sram = 0
    act_cycles_ifmap_rd_sram = 0
    stall_cycles_ifmap_rd_sram = 0
    ideal_start_cycle_ifmap_rd_sram = 0
    ideal_end_cycle_ifmap_rd_sram = 0

    tot_word_filter_rd_sram = 0
    max_word_filter_rd_sram = 0
    tot_access_filter_rd_sram = 0
    max_access_filter_rd_sram = 0
    act_cycles_filter_rd_sram = 0
    stall_cycles_filter_rd_sram = 0
    ideal_start_cycle_filter_rd_sram = 0
    ideal_end_cycle_filter_rd_sram = 0

    tot_word_ofmap_rd_sram = 0
    max_word_ofmap_rd_sram = 0
    tot_access_ofmap_rd_sram = 0
    max_access_ofmap_rd_sram = 0
    act_cycles_ofmap_rd_sram = 0
    stall_cycles_ofmap_rd_sram = 0
    ideal_start_cycle_ofmap_rd_sram = 0
    ideal_end_cycle_ofmap_rd_sram = 0

    tot_word_ofmap_wr_sram = 0
    max_word_ofmap_wr_sram = 0
    tot_access_ofmap_wr_sram = 0
    max_access_ofmap_wr_sram = 0
    act_cycles_ofmap_wr_sram = 0
    stall_cycles_ofmap_wr_sram = 0
    ideal_start_cycle_ofmap_wr_sram = 0
    ideal_end_cycle_ofmap_wr_sram = 0

    # sram hw
    max_freq_ifmap = 0
    energy_per_block_rd_ifmap = 0
    energy_per_block_wr_ifmap = 0
    leakage_power_ifmap = 0
    total_area_ifmap = 0

    max_freq_filter = 0
    energy_per_block_rd_filter = 0
    energy_per_block_wr_filter = 0
    leakage_power_filter = 0
    total_area_filter = 0
    
    max_freq_ofmap = 0
    energy_per_block_rd_ofmap = 0
    energy_per_block_wr_ofmap = 0
    leakage_power_ofmap = 0
    total_area_ofmap = 0

    # dram data
    tot_access_ifmap_rd_dram = 0
    max_access_ifmap_rd_dram = 0
    act_cycles_ifmap_rd_dram = 0
    stall_cycles_ifmap_rd_dram = 0
    ideal_start_cycle_ifmap_rd_dram = 0
    ideal_end_cycle_ifmap_rd_dram = 0

    tot_access_filter_rd_dram = 0
    max_access_filter_rd_dram = 0
    act_cycles_filter_rd_dram = 0
    stall_cycles_filter_rd_dram = 0
    ideal_start_cycle_filter_rd_dram = 0
    ideal_end_cycle_filter_rd_dram = 0

    tot_access_ofmap_wr_dram = 0
    max_access_ofmap_wr_dram = 0
    act_cycles_ofmap_wr_dram = 0
    stall_cycles_ofmap_wr_dram = 0
    ideal_start_cycle_ofmap_wr_dram = 0
    ideal_end_cycle_ofmap_wr_dram = 0

    # sram hw
    max_freq_dram = 0
    energy_per_block_rd_dram = 0
    energy_per_block_wr_dram = 0
    leakage_power_dram = 0
    total_area_dram = 0

    # working cycles
    ideal_max_clk = -1
    ideal_min_clk = 100000
    real_max_clk = -1
    real_min_clk = 100000

    # pe data
    config = cp.ConfigParser()
    config.read(pe_cfg_file)

    src = config.get(computing, 'SRC').split(',')
    src_area_border     = src[0].strip()
    src_leakage_border  = src[1].strip()
    src_dynamic_border  = src[2].strip()
    src_area_inner      = src[3].strip()
    src_leakage_inner   = src[4].strip()
    src_dynamic_inner   = src[5].strip()

    mul = config.get(computing, 'MUL').split(',')
    mul_area     = mul[0].strip()
    mul_leakage  = mul[1].strip()
    mul_dynamic  = mul[2].strip()

    add = config.get(computing, 'ADD').split(',')
    add_area     = add[0].strip()
    add_leakage  = add[1].strip()
    add_dynamic  = add[2].strip()

    buf = config.get(computing, 'BUF').split(',')
    buf_area     = buf[0].strip()
    buf_leakage  = buf[1].strip()
    buf_dynamic  = buf[2].strip()

    # summary report
    bw_ideal        = open(run_name + "_avg_bw_ideal.csv", 'w')
    bw_real         = open(run_name + "_avg_bw_real.csv", 'w')
    maxbw_ideal     = open(run_name + "_max_bw_ideal.csv", 'w')
    maxbw_real      = open(run_name + "_max_bw_real.csv", 'w')
    detail  = open(run_name + "_detail.csv", 'w')
    power   = open(run_name + "_power.csv", 'w')
    energy  = open(run_name + "_energy.csv", 'w')
    area  = open(run_name + "_area.csv", 'w')

    bw_log =    "IFMAP SRAM Size (Bytes),\tFilter SRAM Size (Bytes),\tOFMAP SRAM Size (Bytes),\t" + \
                "Conv Layer Num,\t" + \
                "DRAM IFMAP Read BW (Bytes/cycle),\tDRAM Filter Read BW (Bytes/cycle),\tDRAM OFMAP Write BW (Bytes/cycle),\t" + \
                "SRAM IFMAP Read BW (Bytes/cycle),\tSRAM Filter Read BW (Bytes/cycle),\tSRAM OFMAP Read BW (Bytes/cycle),\t" + \
                "SRAM OFMAP Write BW (Bytes/cycle), \n"
    bw_ideal.write(bw_log)
    bw_real.write(bw_log)
    maxbw_ideal.write(bw_log)
    maxbw_real.write(bw_log)

    detailed_log = "Layer," +\
                "\tDRAM_IFMAP_start,\tDRAM_IFMAP_stop,\tDRAM_IFMAP_bytes," + \
                "\tDRAM_Filter_start,\tDRAM_Filter_stop,\tDRAM_Filter_bytes," + \
                "\tDRAM_OFMAP_start,\tDRAM_OFMAP_stop,\tDRAM_OFMAP_bytes," + \
                "\tSRAM_read_start,\tSRAM_read_stop,\tSRAM_read_bytes," +\
                "\tSRAM_write_start,\tSRAM_write_stop,\tSRAM_write_bytes,\n"
    detail.write(detailed_log)

    area_log =      "IFMAP SRAM (mm^2),\tFilter SRAM (mm^2),\tOFMAP SRAM (mm^2),\tTotal SRAM (mm^2),\t" + \
                    "Total SRC (mm^2),\tTotal MUL (mm^2),\tTotal ADD (mm^2),\tTotal BUF (mm^2),\tTotal Systolic Array (mm^2),\t"
    area.write(area_log)

    energy_log =    "DRAM (uJ),\t" + \
                    "IFMAP SRAM (uJ),\tFilter SRAM (uJ),\tOFMAP SRAM (uJ),\tTotal SRAM (uJ),\t" + \
                    "Total SRC (uJ),\tTotal MUL (uJ),\tTotal ADD (uJ),\tTotal BUF (uJ),\tTotal Systolic Array (uJ),\t"
    energy.write(energy_log)

    power_log =     "DRAM (mW),\t" + \
                    "IFMAP SRAM (mW),\tFilter SRAM (mW),\tOFMAP SRAM (mW),\tTotal SRAM (mW),\t" + \
                    "Total SRC (mW),\tTotal MUL (mW),\tTotal ADD (mW),\tTotal BUF (mW),\tTotal Systolic Array (mW),\t"
    power.write(power_log)

    layer_idx = 0
    for row in param_file:
        # per layer trace profiling
        if first is True:
            first = False
            # skip the first row
            continue

        elems = row.strip().split(',')
        # Do not continue if incomplete line
        if len(elems) < 11:
            continue
        
        layer_idx += 1
        print("Processing layer ", layer_idx)

        name = elems[0]
        bw_log_ideal = ""
        bw_log_real = ""
        area_log = ""
        energy_log = ""
        power_log = ""

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # DRAM: area, energy and power
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # extract the bank count from dram_cfg
        dram_cfg = open(dram_cfg_file, 'r')
        dram_bank = 0
        dram_block_sz_bytes = 0
        for entry in dram_cfg:
            elems = entry.strip().split(' ')
            elems = prune(elems)
            if elems[0] == "-UCA" and elems[1] == "bank" and elems[2] == "count":
                dram_bank = float(elems[3])
            
            if elems[0] == "-block" and elems[1] == "size" and elems[2] == "(bytes)":
                dram_block_sz_bytes = float(elems[3])

        assert dram_bank > 0, "DRAM bank count is invalid, please check the 'dram.cfg' file."
        assert dram_block_sz_bytes > 0, "DRAM block size is invalid, please check the 'dram.cfg' file."
        
        dram_cfg.close()

        # ifmap read
        tot_access_ifmap_rd_dram, \
        max_access_ifmap_rd_dram, \
        act_cycles_ifmap_rd_dram, \
        stall_cycles_ifmap_rd_dram, \
        ideal_start_cycle_ifmap_rd_dram, \
        ideal_end_cycle_ifmap_rd_dram = block_trace.dram_profiling(
                    trace_file=path + run_name + "_" + name + "_dram_ifmap_read.csv",
                    word_sz_bytes=word_sz_bytes,
                    mem_block_sz_bytes=dram_block_sz_bytes,
                    bank=dram_bank,
                    min_addr_word=ifmap_base,
                    max_addr_word=filter_base)
        
        # filter read
        tot_access_filter_rd_dram, \
        max_access_filter_rd_dram, \
        act_cycles_filter_rd_dram, \
        stall_cycles_filter_rd_dram, \
        ideal_start_cycle_filter_rd_dram, \
        ideal_end_cycle_filter_rd_dram = block_trace.dram_profiling(
                    trace_file=path + run_name + "_" + name + "_dram_filter_read.csv",
                    word_sz_bytes=word_sz_bytes,
                    mem_block_sz_bytes=dram_block_sz_bytes,
                    bank=dram_bank,
                    min_addr_word=filter_base,
                    max_addr_word=ofmap_base)
        
        # ofmap write
        tot_access_ofmap_wr_dram, \
        max_access_ofmap_wr_dram, \
        act_cycles_ofmap_wr_dram, \
        stall_cycles_ofmap_wr_dram, \
        ideal_start_cycle_ofmap_wr_dram, \
        ideal_end_cycle_ofmap_wr_dram = block_trace.dram_profiling(
                    trace_file=path + run_name + "_" + name + "_dram_ofmap_write.csv",
                    word_sz_bytes=word_sz_bytes,
                    mem_block_sz_bytes=dram_block_sz_bytes,
                    bank=dram_bank,
                    min_addr_word=ofmap_base,
                    max_addr_word=ofmap_base + 10000000)

        if layer_idx == 1:
            cacti.dram_cacti(
                        src_config_file=dram_cfg_file, 
                        target_config_file=run_name + "_DRAM.cfg",
                        result_file=run_name + "_DRAM.rpt")

            max_freq_dram, \
            energy_per_block_rd_dram, \
            energy_per_block_wr_dram, \
            leakage_power_dram, \
            total_area_dram = cacti.dram_report_extract(report=run_name + "_DRAM.rpt")

        bw_log_ideal += ""
        bw_log_real += ""
        area_log += str(total_area_dram) + ",\t"
        energy_log += ""
        power_log += ""

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # SRAM: area, energy and power
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # extract the bank count from sram_cfg
        sram_cfg = open(sram_cfg_file, 'r')
        sram_bank = 0
        sram_block_sz_bytes = 0
        for entry in sram_cfg:
            elems = entry.strip().split(' ')
            elems = prune(elems)
            if len(elems) >= 4:
                if elems[0] == "-UCA" and elems[1] == "bank" and elems[2] == "count":
                    sram_bank = float(elems[3])
                
                if elems[0] == "-block" and elems[1] == "size" and elems[2] == "(bytes)":
                    sram_block_sz_bytes = float(elems[3])

        assert sram_bank > 0, "SRAM bank count is invalid, please check the 'sram.cfg' file."
        assert sram_block_sz_bytes > 0, "SRAM block size is invalid, please check the 'sram.cfg' file."

        sram_cfg.close()

        # at this point, all traces are supposed to be ready in outputs/run_name/simArchOut
        # find all layers
        path = "./outputs/" + run_name + "/simArchOut/layer_wise/"
        
        # ifmap read
        tot_word_ifmap_rd_sram, \
        max_word_ifmap_rd_sram, \
        tot_access_ifmap_rd_sram, \
        max_access_ifmap_rd_sram, \
        act_cycles_ifmap_rd_sram, \
        stall_cycles_ifmap_rd_sram, \
        ideal_start_cycle_ifmap_rd_sram, \
        ideal_end_cycle_ifmap_rd_sram = block_trace.sram_profiling(
                    trace_file=path + run_name + "_" + name + "_sram_read.csv",
                    word_sz_bytes=word_sz_bytes,
                    block_sz_bytes=sram_block_sz_bytes,
                    bank=sram_bank,
                    min_addr_word=ifmap_base,
                    max_addr_word=filter_base,
                    access_buf=access_buf)
        
        # filter read
        tot_word_filter_rd_sram, \
        max_word_filter_rd_sram, \
        tot_access_filter_rd_sram, \
        max_access_filter_rd_sram, \
        act_cycles_filter_rd_sram, \
        stall_cycles_filter_rd_sram, \
        ideal_start_cycle_filter_rd_sram, \
        ideal_end_cycle_filter_rd_sram = block_trace.sram_profiling(
                    trace_file=path + run_name + "_" + name + "_sram_read.csv",
                    word_sz_bytes=word_sz_bytes,
                    block_sz_bytes=sram_block_sz_bytes,
                    bank=sram_bank,
                    min_addr_word=filter_base,
                    max_addr_word=ofmap_base,
                    access_buf=access_buf)

        # ofmap read
        tot_word_ofmap_rd_sram, \
        max_word_ofmap_rd_sram, \
        tot_access_ofmap_rd_sram, \
        max_access_ofmap_rd_sram, \
        act_cycles_ofmap_rd_sram, \
        stall_cycles_ofmap_rd_sram, \
        ideal_start_cycle_ofmap_rd_sram, \
        ideal_end_cycle_ofmap_rd_sram = block_trace.sram_profiling(
                    trace_file=path + run_name + "_" + name + "_sram_read.csv",
                    word_sz_bytes=word_sz_bytes,
                    block_sz_bytes=sram_block_sz_bytes,
                    bank=sram_bank,
                    min_addr_word=ofmap_base,
                    max_addr_word=ofmap_base + 10000000,
                    access_buf=access_buf)

        # ofmap write
        tot_word_ofmap_wr_sram, \
        max_word_ofmap_wr_sram, \
        tot_access_ofmap_wr_sram, \
        max_access_ofmap_wr_sram, \
        act_cycles_ofmap_wr_sram, \
        stall_cycles_ofmap_wr_sram, \
        ideal_start_cycle_ofmap_wr_sram, \
        ideal_end_cycle_ofmap_wr_sram = block_trace.sram_profiling(
                    trace_file=path + run_name + "_" + name + "_sram_write.csv",
                    word_sz_bytes=word_sz_bytes,
                    block_sz_bytes=sram_block_sz_bytes,
                    bank=sram_bank,
                    min_addr_word=ofmap_base,
                    max_addr_word=ofmap_base + 10000000,
                    access_buf=access_buf)

        if layer_idx == 1:
            if ifmap_sram_exist == True:
                # sram config for each parameter is fixed all the time
                cacti.sram_cacti(
                            mem_sz_bytes=ifmap_sram_size * word_sz_bytes, # in byte
                            src_config_file=sram_cfg_file, 
                            target_config_file=run_name + "_SRAM_ifmap.cfg",
                            result_file=run_name + "_SRAM_ifmap.rpt")

                max_freq_ifmap, \
                energy_per_block_rd_ifmap, \
                energy_per_block_wr_ifmap, \
                leakage_power_ifmap, \
                total_area_ifmap = cacti.sram_report_extract(report=run_name + "_SRAM_ifmap.rpt")

            if filter_sram_exist == True:
                # sram config for each parameter is fixed all the time
                cacti.sram_cacti(
                            mem_sz_bytes=ifmap_sram_size * word_sz_bytes, # in byte
                            src_config_file=sram_cfg_file, 
                            target_config_file=run_name + "_SRAM_filter.cfg",
                            result_file=run_name + "_SRAM_filter.rpt")

                max_freq_filter, \
                energy_per_block_rd_filter, \
                energy_per_block_wr_filter, \
                leakage_power_filter, \
                total_area_filter = cacti.sram_report_extract(report=run_name + "_SRAM_filter.rpt")
            
            if ofmap_sram_exist == True:
                # sram config for each parameter is fixed all the time
                cacti.sram_cacti(
                            mem_sz_bytes=ifmap_sram_size * word_sz_bytes, # in byte
                            src_config_file=sram_cfg_file, 
                            target_config_file=run_name + "_SRAM_ofmap.cfg",
                            result_file=run_name + "_SRAM_ofmap.rpt")

                max_freq_ofmap, \
                energy_per_block_rd_ofmap, \
                energy_per_block_wr_ofmap, \
                leakage_power_ofmap, \
                total_area_ofmap = cacti.sram_report_extract(report=run_name + "_SRAM_ofmap.rpt")
            
            # SRAM area
            sram_area_ifmap     = total_area_ifmap
            sram_area_filter    = total_area_filter
            sram_area_ofmap     = total_area_ofmap
            sram_area_total     = sram_area_ifmap + sram_area_filter + sram_area_ofmap
            area_log += str(sram_area_ifmap) + ",\t" + str(sram_area_filter) + ",\t" + str(sram_area_ofmap) + ",\t" + str(sram_area_total) + ",\t"

        ideal_total_cycle = ideal_max_clk - ideal_min_clk + 1
        real_total_cycle = real_max_clk - real_min_clk + 1

        sram_cycle =    max(ideal_end_cycle_ifmap_rd_sram + stall_cycles_ifmap_rd_sram, 
                            ideal_end_cycle_ofmap_rd_sram + stall_cycles_ofmap_rd_sram, 
                            ideal_end_cycle_ofmap_wr_sram + stall_cycles_ofmap_wr_sram) - \
                        min(ideal_start_cycle_ifmap_rd_sram, 
                            ideal_start_cycle_filter_rd_sram, 
                            ideal_start_cycle_ofmap_rd_sram, 
                            ideal_start_cycle_ofmap_wr_sram) + \
                        stall_cycles_filter_rd_sram

        # SRAM bw
        sram_bw_ideal_ifmap_rd     = tot_word_ifmap_rd_sram    / ideal_total_cycle * word_sz_bytes
        sram_bw_ideal_filter_rd    = tot_word_filter_rd_sram   / ideal_total_cycle * word_sz_bytes
        sram_bw_ideal_ofmap_rd     = tot_word_ofmap_rd_sram    / ideal_total_cycle * word_sz_bytes
        sram_bw_ideal_ofmap_wr     = tot_word_ofmap_wr_sram    / ideal_total_cycle * word_sz_bytes
        bw_log_ideal += str(sram_bw_ideal_ifmap_rd) + ",\t" + str(sram_bw_ideal_filter_rd) + ",\t" + str(sram_bw_ideal_ofmap_rd) + ",\t" + str(sram_bw_ideal_ofmap_wr) + ",\t"

        sram_bw_real_ifmap_rd      = tot_word_ifmap_rd_sram    /  real_total_cycle * word_sz_bytes
        sram_bw_real_filter_rd     = tot_word_filter_rd_sram   /  real_total_cycle * word_sz_bytes
        sram_bw_real_ofmap_rd      = tot_word_ofmap_rd_sram    /  real_total_cycle * word_sz_bytes
        sram_bw_real_ofmap_wr      = tot_word_ofmap_wr_sram    /  real_total_cycle * word_sz_bytes
        bw_log_real += str(sram_bw_real_ifmap_rd) + ",\t" + str(sram_bw_real_filter_rd) + ",\t" + str(sram_bw_real_ofmap_rd) + ",\t" + str(sram_bw_real_ofmap_wr) + ",\t"

        # SRAM energy
        sram_energy_ifmap   =   leakage_power_ifmap     * real_total_cycle + \
                                tot_access_ifmap_rd_sram    * (energy_per_block_rd_ifmap    + energy_per_block_wr_ifmap)
        sram_energy_filter  =   leakage_power_filter    * real_total_cycle + \
                                tot_access_filter_rd_sram   * (energy_per_block_rd_filter   + energy_per_block_wr_filter)
        sram_energy_ofmap   =   leakage_power_ofmap     * real_total_cycle + \
                                tot_access_filter_rd_sram   * (energy_per_block_rd_ofmap    + energy_per_block_wr_ofmap)
        sram_energy_total   =   sram_energy_ifmap + sram_energy_filter + sram_energy_ofmap
        energy_log += str(sram_energy_ifmap) + ",\t" + str(sram_energy_filter) + ",\t" + str(sram_energy_ofmap) + ",\t" + str(sram_energy_total) + ",\t"
        
        # SRAM power
        sram_power_ifmap    =   sram_energy_ifmap   / real_total_cycle
        sram_power_filter   =   sram_energy_filter  / real_total_cycle
        sram_power_ofmap    =   sram_energy_ofmap   / real_total_cycle
        sram_power_total    =   sram_power_ifmap + sram_power_filter + sram_power_ofmap
        power_log += str(sram_power_ifmap) + ",\t" + str(sram_power_filter) + ",\t" + str(sram_power_ofmap) + ",\t" + str(sram_power_total) + ",\t"

        print((tot_word_filter_rd_sram + tot_word_ifmap_rd_sram + tot_word_ofmap_rd_sram))
        print((tot_word_filter_rd_sram + tot_word_ifmap_rd_sram + tot_word_ofmap_rd_sram) / ideal_total_cycle)
        print((tot_word_filter_rd_sram + tot_word_ifmap_rd_sram + tot_word_ofmap_rd_sram) / real_total_cycle)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # systolic array: area, energy and power
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # all calculations here are based on modelling using synthesized data for each components specified in pe.cfg
        sa_area_src = array_h * src_area_border + array_h * array_w * src_area_inner
        sa_area_mul = array_h * array_w * mul_area
        sa_area_add = array_h * array_w * add_area
        sa_area_buf = array_h * (array_w - 1) * buf_area
        sa_area_tot = sa_area_src + sa_area_mul + sa_area_add + sa_area_buf + sa_area_tot
        area_log += str(sa_area_src) + ",\t" + str(sa_area_mul) + ",\t" + str(sa_area_add) + ",\t" + str(sa_area_buf) + ",\t" + str(sa_area_tot) + ",\t"
        
        sa_enery_src =  (array_h * src_leakage_border + array_h * array_w * src_leakage_inner) * real_total_cycle + \
                        (array_h * src_dynamic_border + array_h * array_w * src_dynamic_inner) * sram_cycle
        sa_enery_mul =  array_h * array_w * mul_leakage * real_total_cycle + \
                        array_h * array_w * mul_dynamic * (sram_cycle - act_cycles_filter_rd_sram)
        sa_enery_add =  array_h * array_w * add_leakage * real_total_cycle + \
                        array_h * array_w * add_dynamic * (sram_cycle - act_cycles_filter_rd_sram)
        sa_enery_buf =  array_h * (array_w - 1) * buf_leakage * real_total_cycle + \
                        array_h * (array_w - 1) * buf_dynamic * (sram_cycle - act_cycles_filter_rd_sram)
        sa_enery_tot =  sa_enery_src + sa_enery_mul + sa_enery_add + sa_enery_buf
        energy_log += str(sa_enery_src) + ",\t" + str(sa_enery_mul) + ",\t" + str(sa_enery_add) + ",\t" + str(sa_enery_buf) + ",\t" + str(sa_enery_tot) + ",\t"

        sa_power_src = sa_enery_src / real_total_cycle
        sa_power_mul = sa_enery_mul / real_total_cycle
        sa_power_add = sa_enery_add / real_total_cycle
        sa_power_buf = sa_enery_buf / real_total_cycle
        sa_power_tot = sa_power_src + sa_power_mul + sa_power_add + sa_power_buf
        power_log += str(sa_power_src) + ",\t" + str(sa_power_mul) + ",\t" + str(sa_power_add) + ",\t" + str(sa_power_buf) + ",\t" + str(sa_power_tot) + ",\t"

    bw_ideal.close()
    bw_real.close()
    maxbw_ideal.close()
    maxbw_real.close()
    detail.close()
    power.close()
    energy.close()


def prune(input_list):
    l = []

    for e in input_list:
        e = e.strip() # remove the leading and trailing characters, here space
        if e != '' and e != ' ':
            l.append(e)

    return l


if __name__ == "__main__":
    estimate(run_name="example_run")