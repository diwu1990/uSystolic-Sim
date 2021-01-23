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
    sram_access_buf=True
):
    """
    this code run CACTI according to the configuration of ifmap, filter, ofmap to get power and energy
    1) it calculates the required numbre of banks for SRAM/DRAM (ifmap, filter and ofmap SRAM, as well DRAM)
    2) it profiles the trace file from architecture simulation, and report the required bank count for memory
    3) the cacti result, together with the run time reported from architecture simulation, will generate the total power and total enery for each component
    """
    param_file = open(topology_file, 'r')
    
    ifmap_sram_size *= 1024 # in word
    filter_sram_size *= 1024 # in word
    ofmap_sram_size *= 1024 # in word

    ifmap_sram_exist = (ifmap_sram_size > 0)
    filter_sram_exist = (filter_sram_size > 0)
    ofmap_sram_exist = (ofmap_sram_size > 0)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # dram
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # runtime
    tot_word_ifmap_rd_dram = 0
    max_word_ifmap_rd_dram = 0
    tot_access_ifmap_rd_dram = 0
    tot_row_access_ifmap_rd_dram = 0
    shift_cycles_ifmap_rd_dram = 0
    ideal_start_cycle_ifmap_rd_dram = 0
    ideal_end_cycle_ifmap_rd_dram = 0
    real_start_cycle_ifmap_rd_dram = 0
    real_end_cycle_ifmap_rd_dram = 0

    tot_word_filter_rd_dram = 0
    max_word_filter_rd_dram = 0
    tot_access_filter_rd_dram = 0
    tot_row_access_filter_rd_dram = 0
    shift_cycles_filter_rd_dram = 0
    ideal_start_cycle_filter_rd_dram = 0
    ideal_end_cycle_filter_rd_dram = 0
    real_start_cycle_filter_rd_dram = 0
    real_end_cycle_filter_rd_dram = 0
    
    tot_word_ofmap_rd_dram = 0
    max_word_ofmap_rd_dram = 0
    tot_access_ofmap_rd_dram = 0
    tot_row_access_ofmap_rd_dram = 0
    shift_cycles_ofmap_rd_dram = 0
    ideal_start_cycle_ofmap_rd_dram = 0
    ideal_end_cycle_ofmap_rd_dram = 0
    real_start_cycle_ofmap_rd_dram = 0
    real_end_cycle_ofmap_rd_dram = 0

    tot_word_ofmap_wr_dram = 0
    max_word_ofmap_wr_dram = 0
    tot_access_ofmap_wr_dram = 0
    tot_row_access_ofmap_wr_dram = 0
    shift_cycles_ofmap_wr_dram = 0
    ideal_start_cycle_ofmap_wr_dram = 0
    ideal_end_cycle_ofmap_wr_dram = 0
    real_start_cycle_ofmap_wr_dram = 0
    real_end_cycle_ofmap_wr_dram = 0

    # hw
    max_freq_dram = 0
    activate_energy_dram = 0
    energy_rd_dram = 0
    energy_wr_dram = 0
    precharge_energy_dram = 0
    leakage_power_closed_page_dram = 0
    leakage_power_IO_dram = 0
    area_dram = 0

    dram_page_bits = 0
    dram_bank = 0
    dram_burst = 0
    dram_prefetch = 0
    dram_io_bits = 0

    dram_bw_ideal_ifmap_rd      =   0
    dram_bw_ideal_filter_rd     =   0
    dram_bw_ideal_ofmap_rd      =   0
    dram_bw_ideal_ofmap_wr      =   0
    dram_bw_ideal_total         =   0

    dram_bw_real_ifmap_rd       =   0
    dram_bw_real_filter_rd      =   0
    dram_bw_real_ofmap_rd       =   0
    dram_bw_real_ofmap_wr       =   0
    dram_bw_real_total          =   0

    dram_energy_ifmap_rd        =   0
    dram_energy_filter_rd       =   0
    dram_energy_ofmap_rd        =   0
    dram_energy_ofmap_wr        =   0
    dram_energy_total           =   0

    dram_power_ifmap_rd         =   0
    dram_power_filter_rd        =   0
    dram_power_ofmap_rd         =   0
    dram_power_ofmap_wr         =   0
    dram_power_total            =   0

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # sram
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # runtime, if any
    tot_word_ifmap_rd_sram = 0
    max_word_ifmap_rd_sram = 0
    tot_access_ifmap_rd_sram = 0
    max_access_ifmap_rd_sram = 0
    act_cycles_ifmap_rd_sram = 0
    stall_cycles_ifmap_rd_sram = 0
    ideal_start_cycle_ifmap_rd_sram = 0
    ideal_end_cycle_ifmap_rd_sram = 0
    real_start_cycle_ifmap_rd_sram = 0
    real_end_cycle_ifmap_rd_sram = 0

    tot_word_filter_rd_sram = 0
    max_word_filter_rd_sram = 0
    tot_access_filter_rd_sram = 0
    max_access_filter_rd_sram = 0
    act_cycles_filter_rd_sram = 0
    stall_cycles_filter_rd_sram = 0
    ideal_start_cycle_filter_rd_sram = 0
    ideal_end_cycle_filter_rd_sram = 0
    real_start_cycle_filter_rd_sram = 0
    real_end_cycle_filter_rd_sram = 0

    tot_word_ofmap_rd_sram = 0
    max_word_ofmap_rd_sram = 0
    tot_access_ofmap_rd_sram = 0
    max_access_ofmap_rd_sram = 0
    act_cycles_ofmap_rd_sram = 0
    stall_cycles_ofmap_rd_sram = 0
    ideal_start_cycle_ofmap_rd_sram = 0
    ideal_end_cycle_ofmap_rd_sram = 0
    real_start_cycle_ofmap_rd_sram = 0
    real_end_cycle_ofmap_rd_sram = 0

    tot_word_ofmap_wr_sram = 0
    max_word_ofmap_wr_sram = 0
    tot_access_ofmap_wr_sram = 0
    max_access_ofmap_wr_sram = 0
    act_cycles_ofmap_wr_sram = 0
    stall_cycles_ofmap_wr_sram = 0
    ideal_start_cycle_ofmap_wr_sram = 0
    ideal_end_cycle_ofmap_wr_sram = 0
    real_start_cycle_ofmap_wr_sram = 0
    real_end_cycle_ofmap_wr_sram = 0

    # hw
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

    sram_bank = 0
    sram_block_sz_bytes = 0
    
    sram_area_total = 0

    sram_energy_ifmap_rd = 0
    sram_energy_filter_rd = 0
    sram_energy_ofmap_rd = 0
    sram_energy_ofmap_wr = 0
    sram_energy_total = 0

    sram_power_ifmap_rd = 0
    sram_power_filter_rd = 0
    sram_power_ofmap_rd = 0
    sram_power_ofmap_wr = 0
    sram_power_total = 0

    # working cycles
    ideal_max_clk = 0
    ideal_min_clk = 0
    ideal_total_cycle = 0
    real_max_clk = 0
    real_min_clk = 0
    real_total_cycle = 0
    pe_act_cycle = 0

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # pe
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # extract pe configuration
    config = cp.ConfigParser()
    config.read(pe_cfg_file)

    ireg = config.get(computing, 'IREG').split(',')
    ireg_area_border     = float(ireg[0].strip())
    ireg_leakage_border  = float(ireg[1].strip())
    ireg_dynamic_border  = float(ireg[2].strip())
    ireg_area_inner      = float(ireg[3].strip())
    ireg_leakage_inner   = float(ireg[4].strip())
    ireg_dynamic_inner   = float(ireg[5].strip())

    wreg = config.get(computing, 'WREG').split(',')
    wreg_area       = float(wreg[0].strip())
    wreg_leakage    = float(wreg[1].strip())
    wreg_dynamic    = float(wreg[2].strip())

    mul = config.get(computing, 'MUL').split(',')
    mul_area_border     = float(mul[0].strip())
    mul_leakage_border  = float(mul[1].strip())
    mul_dynamic_border  = float(mul[2].strip())
    mul_area_inner      = float(mul[3].strip())
    mul_leakage_inner   = float(mul[4].strip())
    mul_dynamic_inner   = float(mul[5].strip())

    acc = config.get(computing, 'ACC').split(',')
    acc_area        = float(acc[0].strip())
    acc_leakage     = float(acc[1].strip())
    acc_dynamic     = float(acc[2].strip())

    sa_area_ireg   =  0
    sa_area_wreg   =  0
    sa_area_mul    =  0
    sa_area_acc    =  0
    sa_area_tot    =  0
    
    sa_enery_ireg   =  0
    sa_enery_wreg   =  0
    sa_enery_mul    =  0
    sa_enery_acc    =  0
    sa_enery_tot    =  0

    sa_power_ireg   = 0
    sa_power_wreg   = 0
    sa_power_mul    = 0
    sa_power_acc    = 0
    sa_power_tot    = 0

    onchip_area_tot = 0
    sys_energy_tot = 0
    sys_power_tot = 0

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # output report
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    detail_ideal    = open(run_name + "_detail_ideal.csv", 'w')
    detail_real     = open(run_name + "_detail_real.csv", 'w')
    bw_ideal        = open(run_name + "_avg_bw_ideal.csv", 'w')
    bw_real         = open(run_name + "_avg_bw_real.csv", 'w')
    area            = open(run_name + "_area.csv", 'w')
    energy          = open(run_name + "_energy.csv", 'w')
    power           = open(run_name + "_power.csv", 'w')

    detail_ideal_log =  "Layer,\tType,\t" + \
                    "DRAM I RD start,\tDRAM I RD stop,\tDRAM I RD bytes,\t" + \
                    "DRAM F RD start,\tDRAM F RD stop,\tDRAM F RD bytes,\t" + \
                    "DRAM O RD start,\tDRAM O RD stop,\tDRAM O RD bytes,\t" + \
                    "DRAM O WR start,\tDRAM O WR stop,\tDRAM O WR bytes,\t" + \
                    "SRAM I RD start,\tSRAM I RD stop,\tSRAM I RD bytes,\t" + \
                    "SRAM F RD start,\tSRAM F RD stop,\tSRAM F RD bytes,\t" + \
                    "SRAM O RD start,\tSRAM O RD stop,\tSRAM O RD bytes,\t" + \
                    "SRAM O WR start,\tSRAM O WR stop,\tSRAM O WR bytes,\t\n"

    detail_real_log =   "Layer,\tType,\t" + \
                    "DRAM I RD start,\tDRAM I RD stop,\tDRAM I RD bytes,\t" + \
                    "DRAM F RD start,\tDRAM F RD stop,\tDRAM F RD bytes,\t" + \
                    "DRAM O RD start,\tDRAM O RD stop,\tDRAM O RD bytes,\t" + \
                    "DRAM O WR start,\tDRAM O WR stop,\tDRAM O WR bytes,\t" + \
                    "SRAM I RD start,\tSRAM I RD stop,\tSRAM I RD bytes,\t" + \
                    "SRAM F RD start,\tSRAM F RD stop,\tSRAM F RD bytes,\t" + \
                    "SRAM O RD start,\tSRAM O RD stop,\tSRAM O RD bytes,\t" + \
                    "SRAM O WR start,\tSRAM O WR stop,\tSRAM O WR bytes,\t\n"

    bw_ideal_log =  "Layer,\tType,\t" + \
                    "DRAM I RD BW (Bytes/cycle),\tDRAM F RD BW (Bytes/cycle),\tDRAM O RD BW (Bytes/cycle),\tDRAM O WR BW (Bytes/cycle),\tDRAM BW Total (Bytes/cycle),\t" + \
                    "SRAM I RD BW (Bytes/cycle),\tSRAM F RD BW (Bytes/cycle),\tSRAM O RD BW (Bytes/cycle),\tSRAM O WR BW (Bytes/cycle),\tSRAM BW Total (Bytes/cycle),\t\n"
    
    bw_real_log =   "Layer,\tType,\t" + \
                    "DRAM I RD BW (Bytes/cycle),\tDRAM F RD BW (Bytes/cycle),\tDRAM O RD BW (Bytes/cycle),\tDRAM O WR BW (Bytes/cycle),\tDRAM BW Total (Bytes/cycle),\t" + \
                    "SRAM I RD BW (Bytes/cycle),\tSRAM F RD BW (Bytes/cycle),\tSRAM O RD BW (Bytes/cycle),\tSRAM O WR BW (Bytes/cycle),\tSRAM BW Total (Bytes/cycle),\t\n"
    
    area_log =      "DRAM Area (mm^2),\t" + \
                    "SRAM I Size (Bytes),\tSRAM F Size (Bytes),\tSRAM O Size (Bytes),\tSRAM Total Size (Bytes),\t" + \
                    "SRAM I Area (mm^2),\tSRAM F Area (mm^2),\tSRAM O Area (mm^2),\tSRAM Total (mm^2),\t" + \
                    "IREG (mm^2),\tWREG (mm^2),\tMUL (mm^2),\tACC (mm^2),\tSystolic Array Total (mm^2),\t" + \
                    "On-chip Area Total (mm^2),\t\n"

    energy_log =    "Layer,\tType,\t" + \
                    "DRAM I RD (D) (uJ),\tDRAM F RD (D) (uJ),\tDRAM O RD (D) (uJ),\tDRAM O WR (D) (uJ),\tDRAM Total (D) (uJ),\t" + \
                    "SRAM I RD (D) (uJ),\tSRAM F RD (D) (uJ),\tSRAM O RD (D) (uJ),\tSRAM O WR (D) (uJ),\tSRAM Total (D+L) (uJ),\t" + \
                    "IREG (uJ),\tWREG (uJ),\tMUL (uJ),\tACC (uJ),\tSystolic Array Total (uJ),\t" + \
                    "System Total (uJ)\n"
    
    power_log =     "Layer,\tType,\t" + \
                    "DRAM I RD (D) (mW),\tDRAM F RD (D) (mW),\tDRAM O RD (D) (mW),\tDRAM O WR (D) (mW),\tDRAM Total (D) (mW),\t" + \
                    "SRAM I RD (D) (mW),\tSRAM F RD (D) (mW),\tSRAM O RD (D) (mW),\tSRAM O WR (D) (mW),\tSRAM Total (D+L) (mW),\t" + \
                    "IREG (mW),\tWREG (mW),\tMUL (mW),\tACC (mW),\tSystolic Array Total (mW),\t" + \
                    "System Total (mW)\n"

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # DRAM: area
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # DRAM cacti
    # those results are for entire ddr3 with multiple chips
    print("Run CACTI7.0 for DRAM")
    cacti.dram_cacti(
                origin_config_file=dram_cfg_file, 
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

    # extract the bank count from dram_cfg
    dram_cfg = open(dram_cfg_file, 'r')
    for entry in dram_cfg:
        elems = entry.strip().split(' ')
        elems = prune(elems)
        if len(elems) >= 4:
            if elems[0] == "-page" and elems[1] == "size" and elems[2] == "(bits)":
                dram_page_bits = float(elems[3])
            
            if elems[0] == "-UCA" and elems[1] == "bank" and elems[2] == "count":
                dram_bank = float(elems[3])
            
            if elems[0] == "-internal" and elems[1] == "prefetch" and elems[2] == "width":
                dram_prefetch = float(elems[3])
        
        if len(elems) >= 3:
            if elems[0] == "-burst" and elems[1] == "length":
                dram_burst = float(elems[2])

    dram_io_bits = 64 # always 64 for ddr3

    assert dram_page_bits > 0, "DRAM page bit is invalid, please check the 'dram.cfg' file."
    assert dram_bank > 0, "DRAM bank count is invalid, please check the 'dram.cfg' file."
    assert dram_burst > 0, "DRAM burst length is invalid, please check the 'dram.cfg' file."
    assert dram_prefetch > 0, "DRAM prefetch width is invalid, please check the 'dram.cfg' file."
    assert dram_io_bits > 0, "DRAM IO bit is invalid."
    dram_cfg.close()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # SRAM: area
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # SRAM cacti
    if ifmap_sram_exist == True:
        print("Run CACTI7.0 for SRAM IFMAP")
        # sram config for each parameter is fixed all the time
        cacti.sram_cacti(
                    mem_sz_bytes=ifmap_sram_size * word_sz_bytes, # in byte
                    origin_config_file=sram_cfg_file, 
                    target_config_file=run_name + "_SRAM_ifmap.cfg",
                    result_file=run_name + "_SRAM_ifmap.rpt")

        sram_block_sz_bytes, \
        max_freq_ifmap, \
        energy_per_block_rd_ifmap, \
        energy_per_block_wr_ifmap, \
        leakage_power_ifmap, \
        total_area_ifmap = cacti.sram_report_extract(report=run_name + "_SRAM_ifmap.rpt")

    if filter_sram_exist == True:
        print("Run CACTI7.0 for SRAM Filter")
        # sram config for each parameter is fixed all the time
        cacti.sram_cacti(
                    mem_sz_bytes=filter_sram_size * word_sz_bytes, # in byte
                    origin_config_file=sram_cfg_file, 
                    target_config_file=run_name + "_SRAM_filter.cfg",
                    result_file=run_name + "_SRAM_filter.rpt")

        sram_block_sz_bytes, \
        max_freq_filter, \
        energy_per_block_rd_filter, \
        energy_per_block_wr_filter, \
        leakage_power_filter, \
        total_area_filter = cacti.sram_report_extract(report=run_name + "_SRAM_filter.rpt")
    
    if ofmap_sram_exist == True:
        print("Run CACTI7.0 for SRAM OFMAP")
        # sram config for each parameter is fixed all the time
        cacti.sram_cacti(
                    mem_sz_bytes=ofmap_sram_size * word_sz_bytes, # in byte
                    origin_config_file=sram_cfg_file, 
                    target_config_file=run_name + "_SRAM_ofmap.cfg",
                    result_file=run_name + "_SRAM_ofmap.rpt")

        sram_block_sz_bytes, \
        max_freq_ofmap, \
        energy_per_block_rd_ofmap, \
        energy_per_block_wr_ofmap, \
        leakage_power_ofmap, \
        total_area_ofmap = cacti.sram_report_extract(report=run_name + "_SRAM_ofmap.rpt")
    
    sram_area_total = total_area_ifmap + total_area_filter + total_area_ofmap

    # extract the bank count from sram_cfg
    sram_cfg = open(sram_cfg_file, 'r')
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

    sram_block_sz_word = sram_block_sz_bytes / word_sz_bytes

    sram_cfg.close()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # systolic array: area
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # all calculations here are based on modelling using synthesized data for each components specified in pe.cfg
    sa_area_ireg    = array_h * ireg_area_border + array_h * (array_w - 1) * ireg_area_inner
    sa_area_wreg    = array_h * array_w * wreg_area
    sa_area_mul     = array_h * mul_area_border + array_h * (array_w - 1) * mul_area_inner
    sa_area_acc     = array_h * array_w * acc_area
    sa_area_tot     = sa_area_ireg + sa_area_wreg + sa_area_mul + sa_area_acc
    
    onchip_area_tot = sram_area_total + sa_area_tot
    area_log += str(area_dram) + ",\t" + \
                str(ifmap_sram_size * word_sz_bytes) + ",\t" + \
                str(filter_sram_size * word_sz_bytes) + ",\t" + \
                str(ofmap_sram_size * word_sz_bytes) + ",\t" + \
                str(total_area_ifmap) + ",\t" + \
                str(total_area_filter) + ",\t" + \
                str(total_area_ofmap) + ",\t" + \
                str(sram_area_total) + ",\t" + \
                str(sa_area_ireg) + ",\t" + \
                str(sa_area_wreg) + ",\t" + \
                str(sa_area_mul) + ",\t" + \
                str(sa_area_acc) + ",\t" + \
                str(sa_area_tot) + ",\t" + \
                str(onchip_area_tot) + ",\t\n"

    first = True
    for row in param_file:
        # per layer trace profiling to get bw, energy and power
        if first == True:
            first = False
            # skip the header row
            continue

        elems = row.strip().split(',')
        elems = prune(elems)

        # skip row if unrecognized
        if len(elems) != 11:
            continue
        
        name = elems[0]
        layer_type = elems[1]

        print("")
        print("Commencing trace profiling for " + name)

        # at this point, all traces are supposed to be ready in outputs/run_name/simArchOut
        # find all layers
        path = "./outputs/" + run_name + "/simArchOut/layer_wise/"

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # DRAM profiling
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        print("Profiling IFMAP  DRAM read  trace...")
        # ifmap read
        if ifmap_sram_exist == True:
            trace_file=path + run_name + "_" + name + "_dram_ifmap_read.csv"
        else:
            trace_file=path + run_name + "_" + name + "_sram_read.csv"

        tot_word_ifmap_rd_dram, \
        max_word_ifmap_rd_dram, \
        tot_access_ifmap_rd_dram, \
        tot_row_access_ifmap_rd_dram, \
        shift_cycles_ifmap_rd_dram, \
        ideal_start_cycle_ifmap_rd_dram, \
        ideal_end_cycle_ifmap_rd_dram = block_trace.ddr3_8x8_profiling(
                    trace_file=trace_file,
                    word_sz_bytes=word_sz_bytes,
                    page_bits=dram_page_bits,
                    min_addr_word=ifmap_base,
                    max_addr_word=filter_base)
        real_start_cycle_ifmap_rd_dram = ideal_start_cycle_ifmap_rd_dram - shift_cycles_ifmap_rd_dram
        real_end_cycle_ifmap_rd_dram = ideal_end_cycle_ifmap_rd_dram

        print("Profiling Filter DRAM read  trace...")
        # filter read
        if filter_sram_exist == True:
            trace_file=path + run_name + "_" + name + "_dram_filter_read.csv"
        else:
            trace_file=path + run_name + "_" + name + "_sram_read.csv"

        tot_word_filter_rd_dram, \
        max_word_filter_rd_dram, \
        tot_access_filter_rd_dram, \
        tot_row_access_filter_rd_dram, \
        shift_cycles_filter_rd_dram, \
        ideal_start_cycle_filter_rd_dram, \
        ideal_end_cycle_filter_rd_dram = block_trace.ddr3_8x8_profiling(
                    trace_file=trace_file,
                    word_sz_bytes=word_sz_bytes,
                    page_bits=dram_page_bits,
                    min_addr_word=filter_base,
                    max_addr_word=ofmap_base)
        real_start_cycle_filter_rd_dram = ideal_start_cycle_filter_rd_dram - shift_cycles_filter_rd_dram
        real_end_cycle_filter_rd_dram = ideal_end_cycle_filter_rd_dram

        print("Profiling OFMAP  DRAM read  trace...")
        # ofmap read
        if ofmap_sram_exist == True:
            # when sram exist, assume no ofmap will be read from dram, as sram is large enough
            tot_word_ofmap_rd_dram = 0
            max_word_ofmap_rd_dram = 0
            tot_access_ofmap_rd_dram = 0
            tot_row_access_ofmap_rd_dram = 0
            shift_cycles_ofmap_rd_dram = 0
            ideal_start_cycle_ofmap_rd_dram = 0
            ideal_end_cycle_ofmap_rd_dram = 0
            real_start_cycle_ofmap_rd_dram = 0
            real_end_cycle_ofmap_rd_dram = 0
        else:
            trace_file=path + run_name + "_" + name + "_sram_read.csv"
            tot_word_ofmap_rd_dram, \
            max_word_ofmap_rd_dram, \
            tot_access_ofmap_rd_dram, \
            tot_row_access_ofmap_rd_dram, \
            shift_cycles_ofmap_rd_dram, \
            ideal_start_cycle_ofmap_rd_dram, \
            ideal_end_cycle_ofmap_rd_dram = block_trace.ddr3_8x8_profiling(
                        trace_file=trace_file,
                        word_sz_bytes=word_sz_bytes,
                        page_bits=dram_page_bits,
                        min_addr_word=ofmap_base,
                        max_addr_word=ofmap_base + 10000000)
            real_start_cycle_ofmap_rd_dram = ideal_start_cycle_ofmap_rd_dram
            real_end_cycle_ofmap_rd_dram = ideal_end_cycle_ofmap_rd_dram + shift_cycles_ofmap_rd_dram

        print("Profiling OFMAP  DRAM write trace...")
        # ofmap write
        if ofmap_sram_exist == True:
            trace_file=path + run_name + "_" + name + "_dram_ofmap_write.csv"
        else:
            trace_file=path + run_name + "_" + name + "_sram_write.csv"

        tot_word_ofmap_wr_dram, \
        max_word_ofmap_wr_dram, \
        tot_access_ofmap_wr_dram, \
        tot_row_access_ofmap_wr_dram, \
        shift_cycles_ofmap_wr_dram, \
        ideal_start_cycle_ofmap_wr_dram, \
        ideal_end_cycle_ofmap_wr_dram = block_trace.ddr3_8x8_profiling(
                    trace_file=trace_file,
                    word_sz_bytes=word_sz_bytes,
                    page_bits=dram_page_bits,
                    min_addr_word=ofmap_base,
                    max_addr_word=ofmap_base + 10000000)
        real_start_cycle_ofmap_wr_dram = ideal_start_cycle_ofmap_wr_dram
        real_end_cycle_ofmap_wr_dram = ideal_end_cycle_ofmap_wr_dram + shift_cycles_ofmap_wr_dram

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # SRAM profiling
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        if ifmap_sram_exist == True:
            print("Profiling IFMAP  SRAM read  trace...")
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
                        access_buf=sram_access_buf)
            real_start_cycle_ifmap_rd_sram = ideal_start_cycle_ifmap_rd_sram
            real_end_cycle_ifmap_rd_sram = ideal_end_cycle_ifmap_rd_sram + stall_cycles_ifmap_rd_sram
        else:
            tot_word_ifmap_rd_sram = 0
            max_word_ifmap_rd_sram = 0
            tot_access_ifmap_rd_sram = 0
            max_access_ifmap_rd_sram = 0
            act_cycles_ifmap_rd_sram = 0
            stall_cycles_ifmap_rd_sram = 0
            ideal_start_cycle_ifmap_rd_sram = 0
            ideal_end_cycle_ifmap_rd_sram = 0
            real_start_cycle_ifmap_rd_sram = 0
            real_end_cycle_ifmap_rd_sram = 0

        if filter_sram_exist == True:
            print("Profiling Filter SRAM read  trace...")
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
                        access_buf=sram_access_buf)
            real_start_cycle_filter_rd_sram = ideal_start_cycle_filter_rd_sram
            real_end_cycle_filter_rd_sram = ideal_end_cycle_filter_rd_sram + stall_cycles_filter_rd_sram
        else:
            tot_word_filter_rd_sram = 0
            max_word_filter_rd_sram = 0
            tot_access_filter_rd_sram = 0
            max_access_filter_rd_sram = 0
            act_cycles_filter_rd_sram = 0
            stall_cycles_filter_rd_sram = 0
            ideal_start_cycle_filter_rd_sram = 0
            ideal_end_cycle_filter_rd_sram = 0
            real_start_cycle_filter_rd_sram = 0
            real_end_cycle_filter_rd_sram = 0

        if ofmap_sram_exist == True:
            print("Profiling OFMAP  SRAM read  trace...")
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
                        access_buf=sram_access_buf)
            real_start_cycle_ofmap_rd_sram = ideal_start_cycle_ofmap_rd_sram
            real_end_cycle_ofmap_rd_sram = ideal_end_cycle_ofmap_rd_sram + stall_cycles_ofmap_rd_sram

            print("Profiling OFMAP  SRAM write trace...")
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
                        access_buf=sram_access_buf)
            real_start_cycle_ofmap_wr_sram = ideal_start_cycle_ofmap_wr_sram
            real_end_cycle_ofmap_wr_sram = ideal_end_cycle_ofmap_wr_sram + stall_cycles_ofmap_wr_sram
        else:
            tot_word_ofmap_rd_sram = 0
            max_word_ofmap_rd_sram = 0
            tot_access_ofmap_rd_sram = 0
            max_access_ofmap_rd_sram = 0
            act_cycles_ofmap_rd_sram = 0
            stall_cycles_ofmap_rd_sram = 0
            ideal_start_cycle_ofmap_rd_sram = 0
            ideal_end_cycle_ofmap_rd_sram = 0
            real_start_cycle_ofmap_rd_sram = 0
            real_end_cycle_ofmap_rd_sram = 0

            tot_word_ofmap_wr_sram = 0
            max_word_ofmap_wr_sram = 0
            tot_access_ofmap_wr_sram = 0
            max_access_ofmap_wr_sram = 0
            act_cycles_ofmap_wr_sram = 0
            stall_cycles_ofmap_wr_sram = 0
            ideal_start_cycle_ofmap_wr_sram = 0
            ideal_end_cycle_ofmap_wr_sram = 0
            real_start_cycle_ofmap_wr_sram = 0
            real_end_cycle_ofmap_wr_sram = 0

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # run time calculation
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        ideal_max_clk = max(ideal_end_cycle_ifmap_rd_dram, 
                            ideal_end_cycle_filter_rd_dram, 
                            ideal_end_cycle_ofmap_rd_dram, 
                            ideal_end_cycle_ofmap_wr_dram, 
                            ideal_end_cycle_ifmap_rd_sram, 
                            ideal_end_cycle_filter_rd_sram, 
                            ideal_end_cycle_ofmap_rd_sram, 
                            ideal_end_cycle_ofmap_wr_sram) + 1
        ideal_min_clk = min(ideal_start_cycle_ifmap_rd_dram, 
                            ideal_start_cycle_filter_rd_dram, 
                            ideal_start_cycle_ofmap_rd_dram, 
                            ideal_start_cycle_ofmap_wr_dram, 
                            ideal_start_cycle_ifmap_rd_sram, 
                            ideal_start_cycle_filter_rd_sram, 
                            ideal_start_cycle_ofmap_rd_sram, 
                            ideal_start_cycle_ofmap_wr_sram)
        ideal_total_cycle = ideal_max_clk - ideal_min_clk
        
        real_max_clk =  ideal_max_clk + \
                        stall_cycles_filter_rd_sram + max(stall_cycles_ifmap_rd_sram, stall_cycles_ofmap_rd_sram) + stall_cycles_ofmap_wr_sram + \
                        shift_cycles_ofmap_rd_dram + shift_cycles_ofmap_wr_dram
        real_min_clk =  ideal_min_clk - \
                        shift_cycles_ifmap_rd_dram - shift_cycles_filter_rd_dram
        real_total_cycle = real_max_clk - real_min_clk

        pe_act_cycle =      max(ideal_end_cycle_ifmap_rd_sram, 
                                ideal_end_cycle_filter_rd_sram, 
                                ideal_end_cycle_ofmap_rd_sram, 
                                ideal_end_cycle_ofmap_wr_sram) + \
                            stall_cycles_filter_rd_sram + \
                            max(stall_cycles_ifmap_rd_sram, 
                                stall_cycles_ofmap_rd_sram) + \
                            stall_cycles_ofmap_wr_sram - \
                            min(ideal_start_cycle_ifmap_rd_sram, 
                                ideal_start_cycle_filter_rd_sram, 
                                ideal_start_cycle_ofmap_rd_sram, 
                                ideal_start_cycle_ofmap_wr_sram)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # DRAM: bw, energy, power
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        dram_bw_ideal_ifmap_rd      =   tot_word_ifmap_rd_dram  /   ideal_total_cycle * word_sz_bytes
        dram_bw_ideal_filter_rd     =   tot_word_filter_rd_dram /   ideal_total_cycle * word_sz_bytes
        dram_bw_ideal_ofmap_rd      =   tot_word_ofmap_rd_dram  /   ideal_total_cycle * word_sz_bytes
        dram_bw_ideal_ofmap_wr      =   tot_word_ofmap_wr_dram  /   ideal_total_cycle * word_sz_bytes
        dram_bw_ideal_total         =   dram_bw_ideal_ifmap_rd + dram_bw_ideal_filter_rd + dram_bw_ideal_ofmap_rd + dram_bw_ideal_ofmap_wr

        dram_bw_real_ifmap_rd       =   tot_word_ifmap_rd_dram  /   real_total_cycle * word_sz_bytes
        dram_bw_real_filter_rd      =   tot_word_filter_rd_dram /   real_total_cycle * word_sz_bytes
        dram_bw_real_ofmap_rd       =   tot_word_ofmap_rd_dram  /   real_total_cycle * word_sz_bytes
        dram_bw_real_ofmap_wr       =   tot_word_ofmap_wr_dram  /   real_total_cycle * word_sz_bytes
        dram_bw_real_total          =   dram_bw_real_ifmap_rd + dram_bw_real_filter_rd + dram_bw_real_ofmap_rd + dram_bw_real_ofmap_wr

        dram_energy_ifmap_rd        =   (activate_energy_dram + precharge_energy_dram) * tot_row_access_ifmap_rd_dram + \
                                        energy_rd_dram * tot_access_ifmap_rd_dram
        dram_energy_filter_rd       =   (activate_energy_dram + precharge_energy_dram) * tot_row_access_filter_rd_dram + \
                                        energy_rd_dram * tot_access_filter_rd_dram
        dram_energy_ofmap_rd        =   (activate_energy_dram + precharge_energy_dram) * tot_row_access_ofmap_rd_dram + \
                                        energy_rd_dram * tot_access_ofmap_rd_dram
        dram_energy_ofmap_wr        =   (activate_energy_dram + precharge_energy_dram) * tot_row_access_ofmap_wr_dram + \
                                        energy_wr_dram * tot_access_ofmap_wr_dram
        dram_energy_total           =   dram_energy_ifmap_rd + dram_energy_filter_rd + dram_energy_ofmap_rd + dram_energy_ofmap_wr

        dram_power_ifmap_rd         =   dram_energy_ifmap_rd    /   real_total_cycle
        dram_power_filter_rd        =   dram_energy_filter_rd   /   real_total_cycle
        dram_power_ofmap_rd         =   dram_energy_ofmap_rd    /   real_total_cycle
        dram_power_ofmap_wr         =   dram_energy_ofmap_wr    /   real_total_cycle
        dram_power_total            =   dram_power_ifmap_rd + dram_power_filter_rd + dram_power_ofmap_rd + dram_power_ofmap_wr

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # SRAM: bw, energy, power
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # this dynamic energy actually includes the energy for both writing from dram to sram and reading from sram to systolic array
        if ifmap_sram_exist == True:
            sram_bw_ideal_ifmap_rd      =   tot_word_ifmap_rd_sram  / ideal_total_cycle * word_sz_bytes
            sram_bw_real_ifmap_rd       =   tot_word_ifmap_rd_sram  /  real_total_cycle * word_sz_bytes
            sram_energy_ifmap_rd        =   tot_access_ifmap_rd_sram * energy_per_block_rd_ifmap + \
                                            math.ceil(tot_word_ifmap_rd_dram / sram_block_sz_word) * energy_per_block_wr_ifmap
            sram_power_ifmap_rd         =   sram_energy_ifmap_rd    /  real_total_cycle
        else:
            sram_bw_ideal_ifmap_rd      =   0
            sram_bw_real_ifmap_rd       =   0
            sram_energy_ifmap_rd        =   0
            sram_power_ifmap_rd         =   0
        
        # this dynamic energy actually includes the energy for both writing from dram to sram and reading from sram to systolic array
        if filter_sram_exist == True:
            sram_bw_ideal_filter_rd     =   tot_word_filter_rd_sram / ideal_total_cycle * word_sz_bytes
            sram_bw_real_filter_rd      =   tot_word_filter_rd_sram /  real_total_cycle * word_sz_bytes
            sram_energy_filter_rd       =   tot_access_filter_rd_sram * energy_per_block_rd_filter + \
                                            math.ceil(tot_word_filter_rd_dram / sram_block_sz_word) * energy_per_block_wr_filter
            sram_power_filter_rd        =   sram_energy_filter_rd   /  real_total_cycle
        else:
            sram_bw_ideal_filter_rd     =   0
            sram_bw_real_filter_rd      =   0
            sram_energy_filter_rd       =   0
            sram_power_filter_rd        =   0
        # this dynamic energy actually includes the energy for either writing from dram to sram or reading from sram to systolic array
        # those two situations will not happen simultaneously, if the sram for ofmap is large enough
        if ofmap_sram_exist == True:
            sram_bw_ideal_ofmap_rd      =   tot_word_ofmap_rd_sram  / ideal_total_cycle * word_sz_bytes
            sram_bw_real_ofmap_rd       =   tot_word_ofmap_rd_sram  /  real_total_cycle * word_sz_bytes
            sram_energy_ofmap_rd        =   tot_access_ofmap_rd_sram * energy_per_block_rd_ofmap
            sram_power_ofmap_rd         =   sram_energy_ofmap_rd    /  real_total_cycle

            sram_bw_ideal_ofmap_wr      =   tot_word_ofmap_wr_sram  / ideal_total_cycle * word_sz_bytes
            sram_bw_real_ofmap_wr       =   tot_word_ofmap_wr_sram  /  real_total_cycle * word_sz_bytes
            sram_energy_ofmap_wr        =   tot_access_ofmap_wr_sram * energy_per_block_wr_ofmap + \
                                            math.ceil(tot_word_ofmap_wr_dram / sram_block_sz_word) * energy_per_block_rd_ofmap
            sram_power_ofmap_wr         =   sram_energy_ofmap_rd    /  real_total_cycle
        else:
            sram_bw_ideal_ofmap_rd      =   0
            sram_bw_real_ofmap_rd       =   0
            sram_energy_ofmap_rd        =   0
            sram_power_ofmap_rd         =   0

            sram_bw_ideal_ofmap_wr      =   0
            sram_bw_real_ofmap_wr       =   0
            sram_energy_ofmap_wr        =   0
            sram_power_ofmap_wr         =   0
        
        sram_bw_ideal_total = sram_bw_ideal_ifmap_rd + sram_bw_ideal_filter_rd + sram_bw_ideal_ofmap_rd + sram_bw_ideal_ofmap_wr
        sram_bw_real_total = sram_bw_real_ifmap_rd + sram_bw_real_filter_rd + sram_bw_real_ofmap_rd + sram_bw_real_ofmap_wr
        sram_energy_total           =   leakage_power_ifmap * real_total_cycle + \
                                        leakage_power_filter * real_total_cycle + \
                                        leakage_power_ofmap * real_total_cycle + \
                                        sram_energy_ifmap_rd + sram_energy_filter_rd + sram_energy_ofmap_rd + sram_energy_ofmap_wr
        sram_power_total            =   sram_power_ifmap_rd + sram_power_filter_rd + sram_power_ofmap_rd + sram_power_ofmap_wr

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # systolic array: energy and power
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # all calculations here are based on modelling using synthesized data for each components specified in pe.cfg
        computing_stall_cycles = stall_cycles_ifmap_rd_sram + stall_cycles_ofmap_rd_sram + stall_cycles_ofmap_wr_sram
        # ireg will work all the time
        sa_enery_ireg   =   (array_h * ireg_leakage_border + array_h * (array_w - 1) * ireg_leakage_inner) * real_total_cycle + \
                            (array_h * ireg_dynamic_border + array_h * (array_w - 1) * ireg_dynamic_inner) * pe_act_cycle
        # buf will work only when computing
        sa_enery_wreg   =   array_h * array_w * wreg_leakage * real_total_cycle + \
                            array_h * array_w * wreg_dynamic * (pe_act_cycle - act_cycles_filter_rd_sram - computing_stall_cycles)
        # mul and add will work only when computing with no stalls
        sa_enery_mul    =   (array_h * mul_leakage_border + array_h * (array_w - 1) * mul_leakage_inner) * real_total_cycle + \
                            (array_h * mul_dynamic_border + array_h * (array_w - 1) * mul_dynamic_inner) * (pe_act_cycle - act_cycles_filter_rd_sram - computing_stall_cycles)
        sa_enery_acc    =   array_h * array_w * acc_leakage * real_total_cycle + \
                            array_h * array_w * acc_dynamic * (pe_act_cycle - act_cycles_filter_rd_sram - computing_stall_cycles)
        
        sa_enery_tot    =  sa_enery_ireg + sa_enery_wreg + sa_enery_mul + sa_enery_acc

        sa_power_ireg   = sa_enery_ireg / real_total_cycle
        sa_power_wreg   = sa_enery_wreg / real_total_cycle
        sa_power_mul    = sa_enery_mul / real_total_cycle
        sa_power_acc    = sa_enery_acc / real_total_cycle
        sa_power_tot    = sa_power_ireg + sa_power_wreg + sa_power_mul + sa_power_acc
        
        sys_energy_tot = dram_energy_total + sram_energy_total + sa_enery_tot
        sys_power_tot = dram_power_total + sram_power_total + sa_power_tot
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # log generation
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        detail_ideal_log += str(name) + ",\t" + str(layer_type) + ",\t" + \
                            str(ideal_start_cycle_ifmap_rd_dram) + ",\t" + \
                            str(ideal_end_cycle_ifmap_rd_dram) + ",\t" + \
                            str(tot_word_ifmap_rd_dram * word_sz_bytes) + ",\t" + \
                            str(ideal_start_cycle_filter_rd_dram) + ",\t" + \
                            str(ideal_end_cycle_filter_rd_dram) + ",\t" + \
                            str(tot_word_filter_rd_dram * word_sz_bytes) + ",\t" + \
                            str(ideal_start_cycle_ofmap_rd_dram) + ",\t" + \
                            str(ideal_end_cycle_ofmap_rd_dram) + ",\t" + \
                            str(tot_word_ofmap_rd_dram * word_sz_bytes) + ",\t" +\
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

        detail_real_log +=  str(name) + ",\t" + str(layer_type) + ",\t" + \
                            str(real_start_cycle_ifmap_rd_dram) + ",\t" + \
                            str(real_end_cycle_ifmap_rd_dram) + ",\t" + \
                            str(tot_word_ifmap_rd_dram * word_sz_bytes) + ",\t" + \
                            str(real_start_cycle_filter_rd_dram) + ",\t" + \
                            str(real_end_cycle_filter_rd_dram) + ",\t" + \
                            str(tot_word_filter_rd_dram * word_sz_bytes) + ",\t" + \
                            str(real_start_cycle_ofmap_rd_dram) + ",\t" + \
                            str(real_end_cycle_ofmap_rd_dram) + ",\t" + \
                            str(tot_word_ofmap_rd_dram * word_sz_bytes) + ",\t" + \
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

        bw_ideal_log +=     str(name) + ",\t" + str(layer_type) + ",\t" + \
                            str(dram_bw_ideal_ifmap_rd) + ",\t" + \
                            str(dram_bw_ideal_filter_rd) + ",\t" + \
                            str(dram_bw_ideal_ofmap_rd) + ",\t" + \
                            str(dram_bw_ideal_ofmap_wr) + ",\t" + \
                            str(dram_bw_ideal_total) + ",\t" + \
                            str(sram_bw_ideal_ifmap_rd) + ",\t" + \
                            str(sram_bw_ideal_filter_rd) + ",\t" + \
                            str(sram_bw_ideal_ofmap_rd) + ",\t" + \
                            str(sram_bw_ideal_ofmap_wr) + ",\t" + \
                            str(sram_bw_ideal_total) + ",\t\n"

        bw_real_log +=      str(name) + ",\t" + str(layer_type) + ",\t" + \
                            str(dram_bw_real_ifmap_rd) + ",\t" + \
                            str(dram_bw_real_filter_rd) + ",\t" + \
                            str(dram_bw_real_ofmap_rd) + ",\t" + \
                            str(dram_bw_real_ofmap_wr) + ",\t" + \
                            str(dram_bw_real_total) + ",\t" + \
                            str(sram_bw_real_ifmap_rd) + ",\t" + \
                            str(sram_bw_real_filter_rd) + ",\t" + \
                            str(sram_bw_real_ofmap_rd) + ",\t" + \
                            str(sram_bw_real_ofmap_wr) + ",\t" + \
                            str(sram_bw_real_total) + ",\t\n"
        
        energy_log +=       str(name) + ",\t" + str(layer_type) + ",\t" + \
                            str(dram_energy_ifmap_rd / 1000) + ",\t" + \
                            str(dram_energy_filter_rd / 1000) + ",\t" + \
                            str(dram_energy_ofmap_rd / 1000) + ",\t" + \
                            str(dram_energy_ofmap_wr / 1000) + ",\t" + \
                            str(dram_energy_total / 1000) + ",\t" + \
                            str(sram_energy_ifmap_rd / 1000) + ",\t" + \
                            str(sram_energy_filter_rd / 1000) + ",\t" + \
                            str(sram_energy_ofmap_rd / 1000) + ",\t" + \
                            str(sram_energy_ofmap_wr / 1000) + ",\t" + \
                            str(sram_energy_total / 1000) + ",\t" + \
                            str(sa_enery_ireg / 1000) + ",\t" + \
                            str(sa_enery_mul / 1000) + ",\t" + \
                            str(sa_enery_acc / 1000) + ",\t" + \
                            str(sa_enery_wreg / 1000) + ",\t" + \
                            str(sa_enery_tot / 1000) + ",\t" + \
                            str(sys_energy_tot / 1000) + ",\t\n"

        power_log +=        str(name) + ",\t" + str(layer_type) + ",\t" + \
                            str(dram_power_ifmap_rd) + ",\t" + \
                            str(dram_power_filter_rd) + ",\t" + \
                            str(dram_power_ofmap_rd) + ",\t" + \
                            str(dram_power_ofmap_wr) + ",\t" + \
                            str(dram_power_total) + ",\t" + \
                            str(sram_power_ifmap_rd) + ",\t" + \
                            str(sram_power_filter_rd) + ",\t" + \
                            str(sram_power_ofmap_rd) + ",\t" + \
                            str(sram_power_ofmap_wr) + ",\t" + \
                            str(sram_power_total) + ",\t" + \
                            str(sa_power_ireg) + ",\t" + \
                            str(sa_power_mul) + ",\t" + \
                            str(sa_power_acc) + ",\t" + \
                            str(sa_power_wreg) + ",\t" + \
                            str(sa_power_tot) + ",\t" + \
                            str(sys_power_tot) + ",\t\n"
        
        print("All done for " + name)

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