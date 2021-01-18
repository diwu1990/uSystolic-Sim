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
    dram_bw_bytes = 16
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
    tot_word_ifmap_rd_dram = 0
    max_word_ifmap_rd_dram = 0
    tot_row_access_ifmap_rd_dram = 0
    shift_cycles_ifmap_rd_dram = 0
    ideal_start_cycle_ifmap_rd_dram = 0
    ideal_end_cycle_ifmap_rd_dram = 0

    tot_word_filter_rd_dram = 0
    max_word_filter_rd_dram = 0
    tot_row_access_filter_rd_dram = 0
    shift_cycles_filter_rd_dram = 0
    ideal_start_cycle_filter_rd_dram = 0
    ideal_end_cycle_filter_rd_dram = 0

    tot_word_ofmap_wr_dram = 0
    max_word_ofmap_wr_dram = 0
    tot_row_access_ofmap_wr_dram = 0
    shift_cycles_ofmap_wr_dram = 0
    ideal_start_cycle_ofmap_wr_dram = 0
    ideal_end_cycle_ofmap_wr_dram = 0

    # dram hw
    max_freq_dram = 0
    activate_energy_dram = 0
    energy_rd_dram = 0
    energy_wr_dram = 0
    precharge_energy_dram = 0
    leakage_power_closed_page_dram = 0
    leakage_power_IO_dram = 0
    area_dram = 0

    # working cycles
    ideal_max_clk = -1
    ideal_min_clk = 100000
    real_max_clk = -1
    real_min_clk = 100000

    # pe data
    config = cp.ConfigParser()
    config.read(pe_cfg_file)

    src = config.get(computing, 'SRC').split(',')
    src_area_border     = float(src[0].strip())
    src_leakage_border  = float(src[1].strip())
    src_dynamic_border  = float(src[2].strip())
    src_area_inner      = float(src[3].strip())
    src_leakage_inner   = float(src[4].strip())
    src_dynamic_inner   = float(src[5].strip())

    mul = config.get(computing, 'MUL').split(',')
    mul_area     = float(mul[0].strip())
    mul_leakage  = float(mul[1].strip())
    mul_dynamic  = float(mul[2].strip())

    add = config.get(computing, 'ADD').split(',')
    add_area     = float(add[0].strip())
    add_leakage  = float(add[1].strip())
    add_dynamic  = float(add[2].strip())

    buf = config.get(computing, 'BUF').split(',')
    buf_area     = float(buf[0].strip())
    buf_leakage  = float(buf[1].strip())
    buf_dynamic  = float(buf[2].strip())

    # summary report
    detail_ideal    = open(run_name + "_detail.csv", 'w')
    detail_real     = open(run_name + "_detail.csv", 'w')
    bw_ideal        = open(run_name + "_avg_bw_ideal.csv", 'w')
    bw_real         = open(run_name + "_avg_bw_real.csv", 'w')
    area            = open(run_name + "_area.csv", 'w')
    energy          = open(run_name + "_energy.csv", 'w')
    power           = open(run_name + "_power.csv", 'w')

    detail_ideal_log =    "Layer,\t" +\
                    "DRAM_IFMAP_Read_start,\tDRAM_IFMAP_Read_stop,\tDRAM_IFMAP_Read_bytes,\t" + \
                    "DRAM_Filter_Read_start,\tDRAM_Filter_Read_stop,\tDRAM_Filter_Read_bytes,\t" + \
                    "DRAM_OFMAP_Write_start,\tDRAM_OFMAP_Write_stop,\tDRAM_OFMAP_Write_bytes,\t" + \
                    "SRAM_IFMAP_Read_start,\tSRAM_IFMAP_Read_stop,\tSRAM_IFMAP_Read_bytes,\t" +\
                    "SRAM_Filter_Read_start,\tSRAM_Filter_Read_stop,\tSRAM_Filter_Read_bytes,\t" +\
                    "SRAM_OFMAP_Read_start,\tSRAM_OFMAP_Read_stop,\tSRAM_OFMAP_Read_bytes,\t" +\
                    "SRAM_OFMAP_Write_start,\tSRAM_OFMAP_Write_stop,\tSRAM_OFMAP_Write_bytes,\t\n"

    detail_real_log =    "Layer,\t" +\
                    "DRAM_IFMAP_Read_start,\tDRAM_IFMAP_Read_stop,\tDRAM_IFMAP_Read_bytes,\t" + \
                    "DRAM_Filter_Read_start,\tDRAM_Filter_Read_stop,\tDRAM_Filter_Read_bytes,\t" + \
                    "DRAM_OFMAP_Write_start,\tDRAM_OFMAP_Write_stop,\tDRAM_OFMAP_Write_bytes,\t" + \
                    "SRAM_IFMAP_Read_start,\tSRAM_IFMAP_Read_stop,\tSRAM_IFMAP_Read_bytes,\t" +\
                    "SRAM_Filter_Read_start,\tSRAM_Filter_Read_stop,\tSRAM_Filter_Read_bytes,\t" +\
                    "SRAM_OFMAP_Read_start,\tSRAM_OFMAP_Read_stop,\tSRAM_OFMAP_Read_bytes,\t" +\
                    "SRAM_OFMAP_Write_start,\tSRAM_OFMAP_Write_stop,\tSRAM_OFMAP_Write_bytes,\t\n"

    bw_ideal_log =  "Layer,\t" + \
                    "DRAM IFMAP Read BW (Bytes/cycle),\tDRAM Filter Read BW (Bytes/cycle),\tDRAM OFMAP Write BW (Bytes/cycle),\t" + \
                    "SRAM IFMAP Read BW (Bytes/cycle),\tSRAM Filter Read BW (Bytes/cycle),\tSRAM OFMAP Read BW (Bytes/cycle),\t" + \
                    "SRAM OFMAP Write BW (Bytes/cycle),\t\n"
    
    bw_real_log =   "Layer,\t" + \
                    "DRAM IFMAP Read BW (Bytes/cycle),\tDRAM Filter Read BW (Bytes/cycle),\tDRAM OFMAP Write BW (Bytes/cycle),\t" + \
                    "SRAM IFMAP Read BW (Bytes/cycle),\tSRAM Filter Read BW (Bytes/cycle),\tSRAM OFMAP Read BW (Bytes/cycle),\t" + \
                    "SRAM OFMAP Write BW (Bytes/cycle),\t\n"

    area_log =      "DRAM Area (mm^2),\t" + \
                    "SRAM IFMAP Size (Bytes),\tFilter SRAM Size (Bytes),\tOFMAP SRAM Size (Bytes),\tTotal SRAM Size (mm^2),\t" + \
                    "SRAM IFMAP Area (mm^2),\tFilter SRAM Area (mm^2),\tOFMAP SRAM Area (mm^2),\tTotal SRAM (mm^2),\t" + \
                    "SRC (mm^2),\tMUL (mm^2),\tADD (mm^2),\tBUF (mm^2),\tSystolic Array Total (mm^2),\t" + \
                    "On-chip Area Total (mm^2),\t\n"

    energy_log =    "Layer,\t" + \
                    "DRAM IFMAP (uJ),\tDRAM Filter (uJ),\tDRAM OFMAP (uJ),\tDRAM Total (uJ),\t" + \
                    "SRAM IFMAP (uJ),\tSRAM Filter (uJ),\tSRAM OFMAP (uJ),\tSRAM Total (uJ),\t" + \
                    "SRC (uJ),\tMUL (uJ),\tADD (uJ),\tBUF (uJ),\tSystolic Array Total (uJ),\t" + \
                    "System Total (uJ)\n"
    
    power_log =     "Layer,\t" + \
                    "DRAM IFMAP (mW),\tDRAM Filter (mW),\tDRAM OFMAP (mW),\tDRAM Total (mW),\t" + \
                    "SRAM IFMAP (mW),\tSRAM Filter (mW),\tSRAM OFMAP (mW),\tSRAM Total (mW),\t" + \
                    "SRC (mW),\tMUL (mW),\tADD (mW),\tBUF (mW),\tSystolic Array Total (mW),\t" + \
                    "System Total (mW)\n"

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # DRAM: area
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # DRAM cacti
    cacti.dram_cacti(
                src_config_file=dram_cfg_file, 
                target_config_file=run_name + "_DRAM.cfg",
                result_file=run_name + "_DRAM.rpt")

    max_freq_dram, \
    activate_energy_dram, \
    energy_rd_dram, \
    energy_wr_dram, \
    precharge_energy_dram, \
    leakage_power_closed_page_dram, \
    leakage_power_IO_dram, \
    area_dram = cacti.dram_report_extract(report=run_name + "_DRAM.rpt")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # SRAM: area
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # SRAM cacti
    if ifmap_sram_exist == True:
        # sram config for each parameter is fixed all the time
        cacti.sram_cacti(
                    mem_sz_bytes=ifmap_sram_size * word_sz_bytes, # in byte
                    src_config_file=sram_cfg_file, 
                    target_config_file=run_name + "_SRAM_ifmap.cfg",
                    result_file=run_name + "_SRAM_ifmap.rpt")

        sram_block_sz_bytes, \
        max_freq_ifmap, \
        energy_per_block_rd_ifmap, \
        energy_per_block_wr_ifmap, \
        leakage_power_ifmap, \
        total_area_ifmap = cacti.sram_report_extract(report=run_name + "_SRAM_ifmap.rpt")

    if filter_sram_exist == True:
        # sram config for each parameter is fixed all the time
        cacti.sram_cacti(
                    mem_sz_bytes=filter_sram_size * word_sz_bytes, # in byte
                    src_config_file=sram_cfg_file, 
                    target_config_file=run_name + "_SRAM_filter.cfg",
                    result_file=run_name + "_SRAM_filter.rpt")

        sram_block_sz_bytes, \
        max_freq_filter, \
        energy_per_block_rd_filter, \
        energy_per_block_wr_filter, \
        leakage_power_filter, \
        total_area_filter = cacti.sram_report_extract(report=run_name + "_SRAM_filter.rpt")
    
    if ofmap_sram_exist == True:
        # sram config for each parameter is fixed all the time
        cacti.sram_cacti(
                    mem_sz_bytes=ofmap_sram_size * word_sz_bytes, # in byte
                    src_config_file=sram_cfg_file, 
                    target_config_file=run_name + "_SRAM_ofmap.cfg",
                    result_file=run_name + "_SRAM_ofmap.rpt")

        sram_block_sz_bytes, \
        max_freq_ofmap, \
        energy_per_block_rd_ofmap, \
        energy_per_block_wr_ofmap, \
        leakage_power_ofmap, \
        total_area_ofmap = cacti.sram_report_extract(report=run_name + "_SRAM_ofmap.rpt")
    
    sram_area_total = total_area_ifmap + total_area_filter + total_area_ofmap

    sram_block_sz_word = sram_block_sz_bytes / word_sz_bytes
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # systolic array: area
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # all calculations here are based on modelling using synthesized data for each components specified in pe.cfg
    sa_area_src = array_h * src_area_border + array_h * array_w * src_area_inner
    sa_area_mul = array_h * array_w * mul_area
    sa_area_add = array_h * array_w * add_area
    sa_area_buf = array_h * (array_w - 1) * buf_area
    sa_area_tot = sa_area_src + sa_area_mul + sa_area_add + sa_area_buf
    
    onchip_area_tot = sram_area_total + sa_area_tot
    area_log += str(area_dram) + ",\t" + \
                str(ifmap_sram_size * word_sz_bytes) + ",\t" + \
                str(filter_sram_size * word_sz_bytes) + ",\t" + \
                str(ofmap_sram_size * word_sz_bytes) + ",\t" + \
                str(total_area_ifmap) + ",\t" + \
                str(total_area_filter) + ",\t" + \
                str(total_area_ofmap) + ",\t" + \
                str(sram_area_total) + ",\t" + \
                str(sa_area_src) + ",\t" + \
                str(sa_area_mul) + ",\t" + \
                str(sa_area_add) + ",\t" + \
                str(sa_area_buf) + ",\t" + \
                str(sa_area_tot) + ",\t" + \
                str(onchip_area_tot) + ",\t\n"

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
        # print("Processing layer ", layer_idx)

        name = elems[0]

        # at this point, all traces are supposed to be ready in outputs/run_name/simArchOut
        # find all layers
        path = "./outputs/" + run_name + "/simArchOut/layer_wise/"

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # DRAM profiling
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # extract the bank count from dram_cfg
        dram_cfg = open(dram_cfg_file, 'r')
        dram_bank = 0
        dram_page_sz_bits = 0
        for entry in dram_cfg:
            elems = entry.strip().split(' ')
            elems = prune(elems)
            if len(elems) >= 4:
                if elems[0] == "-UCA" and elems[1] == "bank" and elems[2] == "count":
                    dram_bank = float(elems[3])
                
                if elems[0] == "-page" and elems[1] == "size" and elems[2] == "(bits)":
                    dram_page_sz_bits = float(elems[3])

        dram_page_sz_bytes = dram_page_sz_bits / 8
        assert dram_bank > 0, "DRAM bank count is invalid, please check the 'dram.cfg' file."
        assert dram_page_sz_bytes > 0, "DRAM block size is invalid, please check the 'dram.cfg' file."
        dram_cfg.close()

        # ifmap read
        tot_word_ifmap_rd_dram, \
        max_word_ifmap_rd_dram, \
        tot_access_ifmap_rd_dram, \
        tot_row_access_ifmap_rd_dram, \
        shift_cycles_ifmap_rd_dram, \
        ideal_start_cycle_ifmap_rd_dram, \
        ideal_end_cycle_ifmap_rd_dram = block_trace.dram_profiling(
                    trace_file=path + run_name + "_" + name + "_dram_ifmap_read.csv",
                    word_sz_bytes=word_sz_bytes,
                    page_sz_bytes=dram_page_sz_bytes,
                    bank=dram_bank,
                    bw_bytes=dram_bw_bytes, # in byte, 64 bits x 2 / 8 = 16 bytes for DDR3
                    sram_sz_word=ifmap_sram_size,
                    sram_block_sz_word=sram_block_sz_word,
                    min_addr_word=ifmap_base,
                    max_addr_word=filter_base)
        real_start_cycle_ifmap_rd_dram = ideal_start_cycle_ifmap_rd_dram - shift_cycles_ifmap_rd_dram
        real_end_cycle_ifmap_rd_dram = ideal_end_cycle_ifmap_rd_dram

        # filter read
        tot_word_filter_rd_dram, \
        max_word_filter_rd_dram, \
        tot_access_filter_rd_dram, \
        tot_row_access_filter_rd_dram, \
        shift_cycles_filter_rd_dram, \
        ideal_start_cycle_filter_rd_dram, \
        ideal_end_cycle_filter_rd_dram = block_trace.dram_profiling(
                    trace_file=path + run_name + "_" + name + "_dram_filter_read.csv",
                    word_sz_bytes=word_sz_bytes,
                    page_sz_bytes=dram_page_sz_bytes,
                    bank=dram_bank,
                    bw_bytes=dram_bw_bytes, # in byte, 64 bits x 2 / 8 = 16 bytes for DDR3
                    sram_sz_word=filter_sram_size,
                    sram_block_sz_word=sram_block_sz_word,
                    min_addr_word=filter_base,
                    max_addr_word=ofmap_base)
        real_start_cycle_filter_rd_dram = ideal_start_cycle_filter_rd_dram - shift_cycles_filter_rd_dram
        real_end_cycle_filter_rd_dram = ideal_end_cycle_filter_rd_dram

        # ofmap write
        tot_word_ofmap_wr_dram, \
        max_word_ofmap_wr_dram, \
        tot_access_ofmap_wr_dram, \
        tot_row_access_ofmap_wr_dram, \
        shift_cycles_ofmap_wr_dram, \
        ideal_start_cycle_ofmap_wr_dram, \
        ideal_end_cycle_ofmap_wr_dram = block_trace.dram_profiling(
                    trace_file=path + run_name + "_" + name + "_dram_ofmap_write.csv",
                    word_sz_bytes=word_sz_bytes,
                    page_sz_bytes=dram_page_sz_bytes,
                    bank=dram_bank,
                    bw_bytes=dram_bw_bytes, # in byte, 64 bits x 2 / 8 = 16 bytes for DDR3
                    sram_sz_word=ofmap_sram_size,
                    sram_block_sz_word=sram_block_sz_word,
                    min_addr_word=ofmap_base,
                    max_addr_word=ofmap_base + 10000000)
        real_start_cycle_ofmap_wr_dram = ideal_start_cycle_ofmap_wr_dram
        real_end_cycle_ofmap_wr_dram = ideal_end_cycle_ofmap_wr_dram + shift_cycles_ofmap_wr_dram

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # SRAM profiling
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
        real_start_cycle_ifmap_rd_sram = ideal_start_cycle_ifmap_rd_sram
        real_end_cycle_ifmap_rd_sram = ideal_end_cycle_ifmap_rd_sram + stall_cycles_ifmap_rd_sram

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
        real_start_cycle_filter_rd_sram = ideal_start_cycle_filter_rd_sram
        real_end_cycle_filter_rd_sram = ideal_end_cycle_filter_rd_sram + stall_cycles_filter_rd_sram

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
        real_start_cycle_ofmap_rd_sram = ideal_start_cycle_ofmap_rd_sram
        real_end_cycle_ofmap_rd_sram = ideal_end_cycle_ofmap_rd_sram + stall_cycles_ofmap_rd_sram

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
        real_start_cycle_ofmap_wr_sram = ideal_start_cycle_ofmap_wr_sram
        real_end_cycle_ofmap_wr_sram = ideal_end_cycle_ofmap_wr_sram + stall_cycles_ofmap_wr_sram

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # run time calculation
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        ideal_min_clk = min(ideal_start_cycle_ifmap_rd_dram, 
                            ideal_start_cycle_filter_rd_dram, 
                            ideal_start_cycle_ofmap_wr_dram,
                            ideal_start_cycle_ifmap_rd_sram, 
                            ideal_start_cycle_filter_rd_sram, 
                            ideal_start_cycle_ofmap_rd_sram,
                            ideal_start_cycle_ofmap_wr_sram)
        ideal_max_clk = max(ideal_end_cycle_ifmap_rd_dram, 
                            ideal_end_cycle_filter_rd_dram, 
                            ideal_end_cycle_ofmap_wr_dram,
                            ideal_end_cycle_ifmap_rd_sram, 
                            ideal_end_cycle_filter_rd_sram, 
                            ideal_end_cycle_ofmap_rd_sram,
                            ideal_end_cycle_ofmap_wr_sram)
        ideal_total_cycle = ideal_max_clk - ideal_min_clk + 1

        real_min_clk =  min(real_start_cycle_ifmap_rd_dram, 
                            real_start_cycle_filter_rd_dram, 
                            real_start_cycle_ofmap_wr_dram,
                            real_start_cycle_ifmap_rd_sram, 
                            real_start_cycle_filter_rd_sram, 
                            real_start_cycle_ofmap_rd_sram,
                            real_start_cycle_ofmap_wr_sram)
        real_max_clk =  max(real_end_cycle_ifmap_rd_sram, 
                            real_end_cycle_filter_rd_sram, 
                            real_end_cycle_ofmap_rd_sram,
                            real_end_cycle_ofmap_wr_sram) - \
                        min(ideal_end_cycle_ifmap_rd_sram, 
                            ideal_end_cycle_filter_rd_sram, 
                            ideal_end_cycle_ofmap_rd_sram,
                            ideal_end_cycle_ofmap_wr_sram) + real_end_cycle_ofmap_wr_dram
        real_total_cycle = real_max_clk - real_min_clk + 1

        sram_cycle =    stall_cycles_filter_rd_sram + \
                        max(ideal_end_cycle_ifmap_rd_sram + stall_cycles_ifmap_rd_sram, 
                            ideal_end_cycle_ofmap_rd_sram + stall_cycles_ofmap_rd_sram, 
                            ideal_end_cycle_ofmap_wr_sram + stall_cycles_ofmap_wr_sram) - \
                        min(ideal_start_cycle_ifmap_rd_sram, 
                            ideal_start_cycle_filter_rd_sram, 
                            ideal_start_cycle_ofmap_rd_sram, 
                            ideal_start_cycle_ofmap_wr_sram)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # DRAM: bw, energy, power
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        dram_bw_ideal_ifmap_rd      =   tot_word_ifmap_rd_dram    / ideal_total_cycle * word_sz_bytes
        dram_bw_ideal_filter_rd     =   tot_word_filter_rd_dram   / ideal_total_cycle * word_sz_bytes
        dram_bw_ideal_ofmap_wr      =   tot_word_ofmap_wr_dram    / ideal_total_cycle * word_sz_bytes

        dram_bw_real_ifmap_rd       =   tot_word_ifmap_rd_dram    /  real_total_cycle * word_sz_bytes
        dram_bw_real_filter_rd      =   tot_word_filter_rd_dram   /  real_total_cycle * word_sz_bytes
        dram_bw_real_ofmap_wr       =   tot_word_ofmap_wr_dram    /  real_total_cycle * word_sz_bytes

        dram_energy_ifmap           =   tot_row_access_ifmap_rd_dram * (activate_energy_dram + precharge_energy_dram) + \
                                        tot_access_ifmap_rd_dram * energy_rd_dram
        dram_energy_filter          =   tot_row_access_filter_rd_dram * (activate_energy_dram + precharge_energy_dram) + \
                                        tot_access_filter_rd_dram * energy_rd_dram
        dram_energy_ofmap           =   tot_row_access_ofmap_wr_dram * (activate_energy_dram + precharge_energy_dram) + \
                                        tot_access_ofmap_wr_dram * energy_wr_dram
        dram_energy_total           =   dram_energy_ifmap + dram_energy_filter + dram_energy_ofmap

        dram_power_ifmap            =   dram_energy_ifmap   / real_total_cycle
        dram_power_filter           =   dram_energy_filter  / real_total_cycle
        dram_power_ofmap            =   dram_energy_ofmap   / real_total_cycle
        dram_power_total            =   dram_energy_total   / real_total_cycle

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # SRAM: bw, energy, power
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        sram_bw_ideal_ifmap_rd      =   tot_word_ifmap_rd_sram    / ideal_total_cycle * word_sz_bytes
        sram_bw_ideal_filter_rd     =   tot_word_filter_rd_sram   / ideal_total_cycle * word_sz_bytes
        sram_bw_ideal_ofmap_rd      =   tot_word_ofmap_rd_sram    / ideal_total_cycle * word_sz_bytes
        sram_bw_ideal_ofmap_wr      =   tot_word_ofmap_wr_sram    / ideal_total_cycle * word_sz_bytes

        sram_bw_real_ifmap_rd       =   tot_word_ifmap_rd_sram    /  real_total_cycle * word_sz_bytes
        sram_bw_real_filter_rd      =   tot_word_filter_rd_sram   /  real_total_cycle * word_sz_bytes
        sram_bw_real_ofmap_rd       =   tot_word_ofmap_rd_sram    /  real_total_cycle * word_sz_bytes
        sram_bw_real_ofmap_wr       =   tot_word_ofmap_wr_sram    /  real_total_cycle * word_sz_bytes
        
        sram_energy_ifmap           =   leakage_power_ifmap     * real_total_cycle + \
                                        tot_access_ifmap_rd_sram    * (energy_per_block_rd_ifmap    + energy_per_block_wr_ifmap)
        sram_energy_filter          =   leakage_power_filter    * real_total_cycle + \
                                        tot_access_filter_rd_sram   * (energy_per_block_rd_filter   + energy_per_block_wr_filter)
        sram_energy_ofmap           =   leakage_power_ofmap     * real_total_cycle + \
                                        tot_access_filter_rd_sram   * (energy_per_block_rd_ofmap    + energy_per_block_wr_ofmap)
        sram_energy_total           =   sram_energy_ifmap + sram_energy_filter + sram_energy_ofmap
        
        sram_power_ifmap            =   sram_energy_ifmap   / real_total_cycle
        sram_power_filter           =   sram_energy_filter  / real_total_cycle
        sram_power_ofmap            =   sram_energy_ofmap   / real_total_cycle
        sram_power_total            =   sram_energy_total   / real_total_cycle
        
        # print((tot_word_filter_rd_sram + tot_word_ifmap_rd_sram + tot_word_ofmap_rd_sram))
        # print((tot_word_filter_rd_sram + tot_word_ifmap_rd_sram + tot_word_ofmap_rd_sram) / ideal_total_cycle)
        # print((tot_word_filter_rd_sram + tot_word_ifmap_rd_sram + tot_word_ofmap_rd_sram) / real_total_cycle)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # systolic array: energy and power
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # all calculations here are based on modelling using synthesized data for each components specified in pe.cfg
        computing_stall_cycles = stall_cycles_ifmap_rd_sram + stall_cycles_ofmap_rd_sram + stall_cycles_ofmap_wr_sram
        # src will work all the time
        sa_enery_src =  (array_h * src_leakage_border + array_h * array_w * src_leakage_inner) * real_total_cycle + \
                        (array_h * src_dynamic_border + array_h * array_w * src_dynamic_inner) * sram_cycle
        # mul and add will work only when computing with no stalls
        sa_enery_mul =  array_h * array_w * mul_leakage * real_total_cycle + \
                        array_h * array_w * mul_dynamic * (sram_cycle - act_cycles_filter_rd_sram - computing_stall_cycles)
        sa_enery_add =  array_h * array_w * add_leakage * real_total_cycle + \
                        array_h * array_w * add_dynamic * (sram_cycle - act_cycles_filter_rd_sram - computing_stall_cycles)
        # buf will work only when computing
        sa_enery_buf =  array_h * (array_w - 1) * buf_leakage * real_total_cycle + \
                        array_h * (array_w - 1) * buf_dynamic * (sram_cycle - act_cycles_filter_rd_sram)
        sa_enery_tot =  sa_enery_src + sa_enery_mul + sa_enery_add + sa_enery_buf

        sa_power_src = sa_enery_src / real_total_cycle
        sa_power_mul = sa_enery_mul / real_total_cycle
        sa_power_add = sa_enery_add / real_total_cycle
        sa_power_buf = sa_enery_buf / real_total_cycle
        sa_power_tot = sa_power_src + sa_power_mul + sa_power_add + sa_power_buf
        
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # log generation
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        detail_ideal_log += str(name) + ",\t" + \
                            str(ideal_start_cycle_ifmap_rd_dram) + ",\t" + \
                            str(ideal_end_cycle_ifmap_rd_dram) + ",\t" + \
                            str(tot_word_ifmap_rd_dram * word_sz_bytes) + ",\t" + \
                            str(ideal_start_cycle_filter_rd_dram) + ",\t" + \
                            str(ideal_end_cycle_filter_rd_dram) + ",\t" + \
                            str(tot_word_filter_rd_dram * word_sz_bytes) + ",\t" + \
                            str(ideal_start_cycle_ofmap_wr_dram) + ",\t" + \
                            str(ideal_end_cycle_ofmap_wr_dram) + ",\t" + \
                            str(tot_word_ofmap_wr_dram * word_sz_bytes) + ",\t" +\
                            str(ideal_start_cycle_ifmap_rd_sram) + ",\t" + \
                            str(ideal_end_cycle_ifmap_rd_sram) + ",\t" + \
                            str(tot_word_ifmap_rd_sram * word_sz_bytes) + ",\t" + \
                            str(ideal_start_cycle_filter_rd_sram) + ",\t" + \
                            str(ideal_end_cycle_filter_rd_sram) + ",\t" + \
                            str(tot_word_filter_rd_sram * word_sz_bytes) + ",\t" + \
                            str(ideal_start_cycle_ofmap_rd_sram) + ",\t" + \
                            str(ideal_end_cycle_ofmap_rd_sram) + ",\t" + \
                            str(tot_word_ofmap_rd_sram * word_sz_bytes) + ",\t" + \
                            str(ideal_start_cycle_ofmap_wr_sram) + ",\t" + \
                            str(ideal_end_cycle_ofmap_wr_sram) + ",\t" + \
                            str(tot_word_ofmap_wr_sram * word_sz_bytes) + ",\t\n"

        detail_real_log +=  str(name) + ",\t" + \
                            str(real_start_cycle_ifmap_rd_dram) + ",\t" + \
                            str(real_end_cycle_ifmap_rd_dram) + ",\t" + \
                            str(tot_word_ifmap_rd_dram * word_sz_bytes) + ",\t" + \
                            str(real_start_cycle_filter_rd_dram) + ",\t" + \
                            str(real_end_cycle_filter_rd_dram) + ",\t" + \
                            str(tot_word_filter_rd_dram * word_sz_bytes) + ",\t" + \
                            str(real_start_cycle_ofmap_wr_dram) + ",\t" + \
                            str(real_end_cycle_ofmap_wr_dram) + ",\t" + \
                            str(tot_word_ofmap_wr_dram * word_sz_bytes) + ",\t" + \
                            str(real_start_cycle_ifmap_rd_sram) + ",\t" + \
                            str(real_end_cycle_ifmap_rd_sram) + ",\t" + \
                            str(tot_word_ifmap_rd_sram * word_sz_bytes) + ",\t" + \
                            str(real_start_cycle_filter_rd_sram) + ",\t" + \
                            str(real_end_cycle_filter_rd_sram) + ",\t" + \
                            str(tot_word_filter_rd_sram * word_sz_bytes) + ",\t" + \
                            str(real_start_cycle_ofmap_rd_sram) + ",\t" + \
                            str(real_end_cycle_ofmap_rd_sram) + ",\t" + \
                            str(tot_word_ofmap_rd_sram * word_sz_bytes) + ",\t" + \
                            str(real_start_cycle_ofmap_wr_sram) + ",\t" + \
                            str(real_end_cycle_ofmap_wr_sram) + ",\t" + \
                            str(tot_word_ofmap_wr_sram * word_sz_bytes) + ",\t\n"

        bw_ideal_log +=     str(name) + ",\t" + \
                            str(dram_bw_ideal_ifmap_rd) + ",\t" + \
                            str(dram_bw_ideal_filter_rd) + ",\t" + \
                            str(dram_bw_ideal_ofmap_wr) + ",\t" + \
                            str(sram_bw_ideal_ifmap_rd) + ",\t" + \
                            str(sram_bw_ideal_filter_rd) + ",\t" + \
                            str(sram_bw_ideal_ofmap_rd) + ",\t" + \
                            str(sram_bw_ideal_ofmap_wr) + ",\t\n"

        bw_real_log +=      str(name) + ",\t" + \
                            str(dram_bw_real_ifmap_rd) + ",\t" + \
                            str(dram_bw_real_filter_rd) + ",\t" + \
                            str(dram_bw_real_ofmap_wr) + ",\t" + \
                            str(sram_bw_real_ifmap_rd) + ",\t" + \
                            str(sram_bw_real_filter_rd) + ",\t" + \
                            str(sram_bw_real_ofmap_rd) + ",\t" + \
                            str(sram_bw_real_ofmap_wr) + ",\t\n"
        
        energy_log +=       str(name) + ",\t" + \
                            str(dram_energy_ifmap) + ",\t" + \
                            str(dram_energy_filter) + ",\t" + \
                            str(dram_energy_ofmap) + ",\t" + \
                            str(dram_energy_total) + ",\t" + \
                            str(sram_energy_ifmap) + ",\t" + \
                            str(sram_energy_filter) + ",\t" + \
                            str(sram_energy_ofmap) + ",\t" + \
                            str(sram_energy_total) + ",\t" + \
                            str(sa_enery_src) + ",\t" + \
                            str(sa_enery_mul) + ",\t" + \
                            str(sa_enery_add) + ",\t" + \
                            str(sa_enery_buf) + ",\t" + \
                            str(sa_enery_tot) + ",\t\n"

        power_log +=        str(name) + ",\t" + \
                            str(dram_power_ifmap) + ",\t" + \
                            str(dram_power_filter) + ",\t" + \
                            str(dram_power_ofmap) + ",\t" + \
                            str(dram_power_total) + ",\t" + \
                            str(sram_power_ifmap) + ",\t" + \
                            str(sram_power_filter) + ",\t" + \
                            str(sram_power_ofmap) + ",\t" + \
                            str(sram_power_total) + ",\t" + \
                            str(sa_power_src) + ",\t" + \
                            str(sa_power_mul) + ",\t" + \
                            str(sa_power_add) + ",\t" + \
                            str(sa_power_buf) + ",\t" + \
                            str(sa_power_tot) + ",\t\n"


    detail_ideal.write(detail_ideal_log)
    detail_real.write(detail_real_log)
    bw_ideal.write(bw_ideal_log)
    bw_real.write(bw_real_log)
    area.write(area_log)
    energy.write(energy_log)
    power.write(power_log)

    detail_ideal.close()
    detail_real.close()
    bw_ideal.close()
    bw_real.close()
    area.close()
    energy.close()
    power.close()

def prune(input_list):
    l = []

    for e in input_list:
        e = e.strip() # remove the leading and trailing characters, here space
        if e != '' and e != ' ':
            l.append(e)

    return l


if __name__ == "__main__":
    estimate(run_name="example_run")