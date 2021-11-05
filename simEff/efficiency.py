import math
import simEff.cacti_result as cacti
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
    3) the cacti result, together with the run time reported from architecture simulation, will generate the total power and total energy for each component
    """
    param_file = open(topology_file, 'r')
    
    ifmap_sram_size *= 1024 # in word
    filter_sram_size *= 1024 # in word
    ofmap_sram_size *= 1024 # in word
    sram_total_size = ifmap_sram_size + filter_sram_size + ofmap_sram_size

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
    act_cycles_ifmap_rd_dram = 0
    shift_cycles_ifmap_rd_dram = 0
    ideal_start_cycle_ifmap_rd_dram = 0
    ideal_end_cycle_ifmap_rd_dram = 0
    real_start_cycle_ifmap_rd_dram = 0
    real_end_cycle_ifmap_rd_dram = 0

    tot_word_filter_rd_dram = 0
    max_word_filter_rd_dram = 0
    tot_access_filter_rd_dram = 0
    tot_row_access_filter_rd_dram = 0
    act_cycles_filter_rd_dram = 0
    shift_cycles_filter_rd_dram = 0
    ideal_start_cycle_filter_rd_dram = 0
    ideal_end_cycle_filter_rd_dram = 0
    real_start_cycle_filter_rd_dram = 0
    real_end_cycle_filter_rd_dram = 0
    
    tot_word_ofmap_rd_dram = 0
    max_word_ofmap_rd_dram = 0
    tot_access_ofmap_rd_dram = 0
    tot_row_access_ofmap_rd_dram = 0
    act_cycles_ofmap_rd_dram = 0
    shift_cycles_ofmap_rd_dram = 0
    ideal_start_cycle_ofmap_rd_dram = 0
    ideal_end_cycle_ofmap_rd_dram = 0
    real_start_cycle_ofmap_rd_dram = 0
    real_end_cycle_ofmap_rd_dram = 0

    tot_word_ofmap_wr_dram = 0
    max_word_ofmap_wr_dram = 0
    tot_access_ofmap_wr_dram = 0
    tot_row_access_ofmap_wr_dram = 0
    act_cycles_ofmap_wr_dram = 0
    shift_cycles_ofmap_wr_dram = 0
    ideal_start_cycle_ofmap_wr_dram = 0
    ideal_end_cycle_ofmap_wr_dram = 0
    real_start_cycle_ofmap_wr_dram = 0
    real_end_cycle_ofmap_wr_dram = 0

    tot_word_ifmap_rd_dram_all = 0
    tot_word_filter_rd_dram_all = 0
    tot_word_ofmap_rd_dram_all = 0
    tot_word_ofmap_wr_dram_all = 0

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

    dram_energy_ifmap_rd        =   0
    dram_energy_filter_rd       =   0
    dram_energy_ofmap_rd        =   0
    dram_energy_ofmap_wr        =   0
    dram_energy_total_dynamic   =   0

    dram_energy_ifmap_rd_all        =   0
    dram_energy_filter_rd_all       =   0
    dram_energy_ofmap_rd_all        =   0
    dram_energy_ofmap_wr_all        =   0
    dram_energy_total_dynamic_all   =   0

    dram_power_ifmap_rd         =   0
    dram_power_filter_rd        =   0
    dram_power_ofmap_rd         =   0
    dram_power_ofmap_wr         =   0
    dram_power_total_dynamic    =   0

    dram_power_ifmap_rd_all         =   0
    dram_power_filter_rd_all        =   0
    dram_power_ofmap_rd_all         =   0
    dram_power_ofmap_wr_all         =   0
    dram_power_total_dynamic_all    =   0

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

    tot_word_ifmap_rd_sram_all = 0
    tot_word_filter_rd_sram_all = 0
    tot_word_ofmap_rd_sram_all = 0
    tot_word_ofmap_wr_sram_all = 0

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
    sram_energy_dynamic = 0

    sram_energy_ifmap_rd_all = 0
    sram_energy_filter_rd_all = 0
    sram_energy_ofmap_rd_all = 0
    sram_energy_ofmap_wr_all = 0
    sram_energy_dynamic_all = 0

    sram_energy_ifmap_l = 0
    sram_energy_filter_l = 0
    sram_energy_ofmap_l = 0
    sram_energy_leakage = 0
    sram_energy_total = 0

    sram_energy_ifmap_l_all = 0
    sram_energy_filter_l_all = 0
    sram_energy_ofmap_l_all = 0
    sram_energy_leakage_all = 0
    sram_energy_total_all = 0

    sram_power_ifmap_rd = 0
    sram_power_filter_rd = 0
    sram_power_ofmap_rd = 0
    sram_power_ofmap_wr = 0
    sram_power_dynamic = 0

    sram_power_ifmap_rd_all = 0
    sram_power_filter_rd_all = 0
    sram_power_ofmap_rd_all = 0
    sram_power_ofmap_wr_all = 0
    sram_power_dynamic_all = 0

    sram_power_ifmap_l = 0
    sram_power_filter_l = 0
    sram_power_ofmap_l = 0
    sram_power_leakage = 0
    sram_power_total = 0

    sram_power_ifmap_l_all = 0
    sram_power_filter_l_all = 0
    sram_power_ofmap_l_all = 0
    sram_power_leakage_all = 0
    sram_power_total_all = 0

    # working cycles
    ideal_layer_cycle = 0
    ideal_layer_sec = 0

    ideal_cycle_all = 0
    ideal_sec_all = 0

    real_layer_cycle = 0
    real_layer_sec = 0

    real_cycle_all = 0
    real_sec_all = 0

    act_cycle_ifmap_rd = 0
    act_cycle_filter_rd = 0
    act_cycle_ofmap_rd = 0
    act_cycle_ofmap_wr = 0

    dynamic_cycle_ireg = 0
    dynamic_cycle_wreg = 0
    dynamic_cycle_mac = 0

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # pe
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # extract pe configuration
    config = cp.ConfigParser()
    config.read(pe_cfg_file)
    frequency = float(config.get("Frequency", 'MHz').split(',')[0].strip())
    period = 1.0 / frequency # in us unit
    try:
        running_frequency = float(config.get("Running Frequency", 'MHz').split(',')[0].strip())
        running_period = 1.0 / running_frequency # in us unit
    except:
        running_frequency = frequency
        running_period = period

    ireg = config.get(computing, 'IREG').split(',')
    ireg_area_border     = float(ireg[0].strip())
    ireg_leakage_border  = float(ireg[1].strip())
    ireg_dynamic_border  = float(ireg[2].strip())
    ireg_area_inner      = float(ireg[3].strip())
    ireg_leakage_inner   = float(ireg[4].strip())
    ireg_dynamic_inner   = float(ireg[5].strip())

    wreg = config.get(computing, 'WREG').split(',')
    wreg_area_border     = float(wreg[0].strip())
    wreg_leakage_border  = float(wreg[1].strip())
    wreg_dynamic_border  = float(wreg[2].strip())
    wreg_area_inner      = float(wreg[3].strip())
    wreg_leakage_inner   = float(wreg[4].strip())
    wreg_dynamic_inner   = float(wreg[5].strip())

    mul = config.get(computing, 'MUL').split(',')
    mul_area_border     = float(mul[0].strip())
    mul_leakage_border  = float(mul[1].strip())
    mul_dynamic_border  = float(mul[2].strip())
    mul_area_inner      = float(mul[3].strip())
    mul_leakage_inner   = float(mul[4].strip())
    mul_dynamic_inner   = float(mul[5].strip())

    acc = config.get(computing, 'ACC').split(',')
    acc_area_border     = float(acc[0].strip())
    acc_leakage_border  = float(acc[1].strip())
    acc_dynamic_border  = float(acc[2].strip())
    acc_area_inner      = float(acc[3].strip())
    acc_leakage_inner   = float(acc[4].strip())
    acc_dynamic_inner   = float(acc[5].strip())

    sa_area_ireg   =  0
    sa_area_wreg   =  0
    sa_area_mul    =  0
    sa_area_acc    =  0
    sa_area_tot    =  0
    
    sa_energy_ireg_d     =  0
    sa_energy_ireg_l     =  0
    sa_energy_ireg       =  0

    sa_energy_ireg_d_all     =  0
    sa_energy_ireg_l_all     =  0
    sa_energy_ireg_all       =  0

    sa_energy_wreg_d     =  0
    sa_energy_wreg_l     =  0
    sa_energy_wreg       =  0

    sa_energy_wreg_d_all     =  0
    sa_energy_wreg_l_all     =  0
    sa_energy_wreg_all       =  0

    sa_energy_mul_d      =  0
    sa_energy_mul_l      =  0
    sa_energy_mul        =  0

    sa_energy_mul_d_all      =  0
    sa_energy_mul_l_all      =  0
    sa_energy_mul_all        =  0

    sa_energy_acc_d      =  0
    sa_energy_acc_l      =  0
    sa_energy_acc        =  0

    sa_energy_acc_d_all      =  0
    sa_energy_acc_l_all      =  0
    sa_energy_acc_all        =  0

    sa_energy_dynamic    =  0
    sa_energy_leakage    =  0
    sa_energy_tot        =  0

    sa_energy_dynamic_all    =  0
    sa_energy_leakage_all    =  0
    sa_energy_tot_all        =  0

    sa_power_ireg_d     = 0
    sa_power_ireg_l     = 0
    sa_power_ireg       = 0

    sa_power_ireg_d_all     = 0
    sa_power_ireg_l_all     = 0
    sa_power_ireg_all       = 0

    sa_power_wreg_d     = 0
    sa_power_wreg_l     = 0
    sa_power_wreg       = 0

    sa_power_wreg_d_all     = 0
    sa_power_wreg_l_all     = 0
    sa_power_wreg_all       = 0

    sa_power_mul_d      = 0
    sa_power_mul_l      = 0
    sa_power_mul        = 0

    sa_power_mul_d_all      = 0
    sa_power_mul_l_all      = 0
    sa_power_mul_all        = 0

    sa_power_acc_d      = 0
    sa_power_acc_l      = 0
    sa_power_acc        = 0

    sa_power_acc_d_all      = 0
    sa_power_acc_l_all      = 0
    sa_power_acc_all        = 0
    
    sa_power_dynamic    = 0
    sa_power_leakage    = 0
    sa_power_tot        = 0

    sa_power_dynamic_all    = 0
    sa_power_leakage_all    = 0
    sa_power_tot_all        = 0

    onchip_area_tot = 0

    sys_energy_dynamic = 0
    sys_energy_leakage = 0
    sys_energy_tot = 0

    sys_energy_dynamic_all = 0
    sys_energy_leakage_all = 0
    sys_energy_tot_all = 0

    sys_power_dynamic = 0
    sys_power_leakage = 0
    sys_power_tot = 0

    sys_power_dynamic_all = 0
    sys_power_leakage_all = 0
    sys_power_tot_all = 0

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # output report
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    area            = open(run_name + "_area.csv", 'w')
    energy          = open(run_name + "_energy.csv", 'w')
    power           = open(run_name + "_power.csv", 'w')

    area_log =      "DRAM Area (mm^2),\t" + \
                    "SRAM I Size (Bytes),\tSRAM F Size (Bytes),\tSRAM O Size (Bytes),\tSRAM Total Size (Bytes),\t" + \
                    "SRAM I Area (mm^2),\tSRAM F Area (mm^2),\tSRAM O Area (mm^2),\tSRAM Total (mm^2),\t" + \
                    "IREG (mm^2),\tWREG (mm^2),\tMUL (mm^2),\tACC (mm^2),\tSystolic Array Total (mm^2),\t" + \
                    "On-chip Area Total (mm^2),\t\n"

    energy_log =    "Layer,\tType,\t" + \
                    "DRAM I RD (D) (nJ),\tDRAM F RD (D) (nJ),\tDRAM O RD (D) (nJ),\tDRAM O WR (D) (nJ),\tDRAM Total (D) (nJ),\t" + \
                    "SRAM I RD (D) (nJ),\tSRAM F RD (D) (nJ),\tSRAM O RD (D) (nJ),\tSRAM O WR (D) (nJ),\tSRAM Total (D) (nJ),\t" + \
                    "SRAM I (L) (nJ),\tSRAM F (L) (nJ),\tSRAM O (L) (nJ),\tSRAM Total (L) (nJ),\t" + \
                    "SRAM Total (D+L) (nJ),\t" + \
                    "IREG (D) (nJ),\tIREG (L) (nJ),\tIREG Total (D+L) (nJ),\t" + \
                    "WREG (D) (nJ),\tWREG (L) (nJ),\tWREG Total (D+L) (nJ),\t" + \
                    "MUL (D) (nJ),\tMUL (L) (nJ),\tMUL Total (D+L) (nJ),\t" + \
                    "ACC (D) (nJ),\tACC (L) (nJ),\tACC Total (D+L) (nJ),\t" + \
                    "Systolic Array Total (D) (nJ),\tSystolic Array Total (L) (nJ),\tSystolic Array Total (D+L) (nJ),\t" + \
                    "System Total (D) (nJ),\tSystem Total (L) (nJ),\tSystem Total (D+L) (nJ),\t\n"
    
    power_log =     "Layer,\tType,\t" + \
                    "DRAM I RD (D) (mW),\tDRAM F RD (D) (mW),\tDRAM O RD (D) (mW),\tDRAM O WR (D) (mW),\tDRAM Total (D) (mW),\t" + \
                    "SRAM I RD (D) (mW),\tSRAM F RD (D) (mW),\tSRAM O RD (D) (mW),\tSRAM O WR (D) (mW),\tSRAM Total (D) (mW),\t" + \
                    "SRAM I (L) (mW),\tSRAM F (L) (mW),\tSRAM O (L) (mW),\tSRAM Total (L) (mW),\t" + \
                    "SRAM Total (D+L) (mW),\t" + \
                    "IREG (D) (mW),\tIREG (L) (mW),\tIREG Total (D+L) (mW),\t" + \
                    "WREG (D) (mW),\tWREG (L) (mW),\tWREG Total (D+L) (mW),\t" + \
                    "MUL (D) (mW),\tMUL (L) (mW),\tMUL Total (D+L) (mW),\t" + \
                    "ACC (D) (mW),\tACC (L) (mW),\tACC Total (D+L) (mW),\t" + \
                    "Systolic Array Total (D) (mW),\tSystolic Array Total (L) (mW),\tSystolic Array Total (D+L) (mW),\t" + \
                    "System Total (D) (mW),\tSystem Total (L) (mW),\tSystem Total (D+L) (mW),\t\n"

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
    leakage_power_open_page_dram, \
    leakage_power_IO_dram, \
    refresh_power_dram, \
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
    sa_area_wreg    = array_h * wreg_area_border + array_h * (array_w - 1) * wreg_area_inner
    sa_area_mul     = array_h * mul_area_border + array_h * (array_w - 1) * mul_area_inner
    sa_area_acc     = array_h * acc_area_border + array_h * (array_w - 1) * acc_area_inner
    sa_area_tot     = sa_area_ireg + sa_area_wreg + sa_area_mul + sa_area_acc
    
    onchip_area_tot = sram_area_total + sa_area_tot
    area_log += str(area_dram) + ",\t" + \
                str(ifmap_sram_size * word_sz_bytes) + ",\t" + \
                str(filter_sram_size * word_sz_bytes) + ",\t" + \
                str(ofmap_sram_size * word_sz_bytes) + ",\t" + \
                str(sram_total_size * word_sz_bytes) + ",\t" + \
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

    row_idx = 0

    first = True
    for row in param_file:
        row_idx += 1

        # per layer trace profiling to get energy and power
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
        if layer_type == "GEMM":
            mac_cycles = int(elems[10].strip())
        else:
            mac_cycles = 1

        print("")
        print("Commencing efficiency estimation for " + name)

        # at this point, all hw_runtime statistics are supposed to be ready in outputs/run_name/simEffOut
        # find the corresponding layers
        hw_runtime = open("./outputs/" + run_name + "/simHwOut/" + run_name + "_hw_runtime.csv", 'r')
        found_flag = False
        row_idx_hw = 0
        for row_hw in hw_runtime:
            row_idx_hw += 1
            elems_hw = row_hw.strip().split(',')
            elems_hw = prune(elems_hw)

            if name == elems_hw[0]:
                found_flag = True
                elems_hw = [float(elem_hw) for elem_hw in elems_hw[2:]]

                [tot_word_ifmap_rd_dram, 
                max_word_ifmap_rd_dram, 
                tot_access_ifmap_rd_dram, 
                tot_row_access_ifmap_rd_dram, 
                act_cycles_ifmap_rd_dram, 
                shift_cycles_ifmap_rd_dram, 
                ideal_start_cycle_ifmap_rd_dram, 
                ideal_end_cycle_ifmap_rd_dram, 
                real_start_cycle_ifmap_rd_dram, 
                real_end_cycle_ifmap_rd_dram, 
                tot_word_filter_rd_dram, 
                max_word_filter_rd_dram, 
                tot_access_filter_rd_dram, 
                tot_row_access_filter_rd_dram, 
                act_cycles_filter_rd_dram, 
                shift_cycles_filter_rd_dram, 
                ideal_start_cycle_filter_rd_dram, 
                ideal_end_cycle_filter_rd_dram, 
                real_start_cycle_filter_rd_dram, 
                real_end_cycle_filter_rd_dram, 
                tot_word_ofmap_rd_dram, 
                max_word_ofmap_rd_dram, 
                tot_access_ofmap_rd_dram, 
                tot_row_access_ofmap_rd_dram, 
                act_cycles_ofmap_rd_dram, 
                shift_cycles_ofmap_rd_dram, 
                ideal_start_cycle_ofmap_rd_dram, 
                ideal_end_cycle_ofmap_rd_dram, 
                real_start_cycle_ofmap_rd_dram, 
                real_end_cycle_ofmap_rd_dram, 
                tot_word_ofmap_wr_dram, 
                max_word_ofmap_wr_dram, 
                tot_access_ofmap_wr_dram, 
                tot_row_access_ofmap_wr_dram, 
                act_cycles_ofmap_wr_dram, 
                shift_cycles_ofmap_wr_dram, 
                ideal_start_cycle_ofmap_wr_dram, 
                ideal_end_cycle_ofmap_wr_dram, 
                real_start_cycle_ofmap_wr_dram, 
                real_end_cycle_ofmap_wr_dram, 
                tot_word_ifmap_rd_sram, 
                max_word_ifmap_rd_sram, 
                tot_access_ifmap_rd_sram, 
                max_access_ifmap_rd_sram, 
                act_cycles_ifmap_rd_sram, 
                stall_cycles_ifmap_rd_sram, 
                ideal_start_cycle_ifmap_rd_sram, 
                ideal_end_cycle_ifmap_rd_sram, 
                real_start_cycle_ifmap_rd_sram, 
                real_end_cycle_ifmap_rd_sram, 
                tot_word_filter_rd_sram, 
                max_word_filter_rd_sram, 
                tot_access_filter_rd_sram, 
                max_access_filter_rd_sram, 
                act_cycles_filter_rd_sram, 
                stall_cycles_filter_rd_sram, 
                ideal_start_cycle_filter_rd_sram, 
                ideal_end_cycle_filter_rd_sram, 
                real_start_cycle_filter_rd_sram, 
                real_end_cycle_filter_rd_sram, 
                tot_word_ofmap_rd_sram, 
                max_word_ofmap_rd_sram, 
                tot_access_ofmap_rd_sram, 
                max_access_ofmap_rd_sram, 
                act_cycles_ofmap_rd_sram, 
                stall_cycles_ofmap_rd_sram, 
                ideal_start_cycle_ofmap_rd_sram, 
                ideal_end_cycle_ofmap_rd_sram, 
                real_start_cycle_ofmap_rd_sram, 
                real_end_cycle_ofmap_rd_sram, 
                tot_word_ofmap_wr_sram, 
                max_word_ofmap_wr_sram, 
                tot_access_ofmap_wr_sram, 
                max_access_ofmap_wr_sram, 
                act_cycles_ofmap_wr_sram, 
                stall_cycles_ofmap_wr_sram, 
                ideal_start_cycle_ofmap_wr_sram, 
                ideal_end_cycle_ofmap_wr_sram, 
                real_start_cycle_ofmap_wr_sram, 
                real_end_cycle_ofmap_wr_sram, 
                ideal_layer_cycle, 
                ideal_layer_sec, 
                real_layer_cycle, 
                real_layer_sec, 
                act_cycle_ifmap_rd, 
                act_cycle_filter_rd, 
                act_cycle_ofmap_rd, 
                act_cycle_ofmap_wr, 
                dynamic_cycle_ireg, 
                dynamic_cycle_wreg, 
                dynamic_cycle_mac] = elems_hw
        hw_runtime.close()
        assert found_flag == True, "Can't find required hardware runtime statistics."

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # run time calculation
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        ideal_cycle_all += ideal_layer_cycle
        ideal_sec_all += ideal_layer_sec
        # sram stall and dram shift have similar meanings: the extra cycle for data access compared to the ideal
        # sram stall can be overlapped for stall_cycles_ifmap_rd_sram and stall_cycles_ofmap_rd_sram due to multiple copies of sram
        # dram shift can't be overlapped due to sharing the same dram IO
        real_cycle_all += real_layer_cycle
        real_sec_all += real_layer_sec

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # DRAM: energy and power
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        dram_energy_ifmap_rd        =   (activate_energy_dram + precharge_energy_dram) * tot_row_access_ifmap_rd_dram + \
                                        energy_rd_dram * tot_access_ifmap_rd_dram
        dram_energy_filter_rd       =   (activate_energy_dram + precharge_energy_dram) * tot_row_access_filter_rd_dram + \
                                        energy_rd_dram * tot_access_filter_rd_dram
        dram_energy_ofmap_rd        =   (activate_energy_dram + precharge_energy_dram) * tot_row_access_ofmap_rd_dram + \
                                        energy_rd_dram * tot_access_ofmap_rd_dram
        dram_energy_ofmap_wr        =   (activate_energy_dram + precharge_energy_dram) * tot_row_access_ofmap_wr_dram + \
                                        energy_wr_dram * tot_access_ofmap_wr_dram
        dram_energy_total_dynamic   =   dram_energy_ifmap_rd + dram_energy_filter_rd + dram_energy_ofmap_rd + dram_energy_ofmap_wr

        dram_power_ifmap_rd         =   dram_energy_ifmap_rd        /   (real_layer_cycle * running_period)
        dram_power_filter_rd        =   dram_energy_filter_rd       /   (real_layer_cycle * running_period)
        dram_power_ofmap_rd         =   dram_energy_ofmap_rd        /   (real_layer_cycle * running_period)
        dram_power_ofmap_wr         =   dram_energy_ofmap_wr        /   (real_layer_cycle * running_period)
        dram_power_total_dynamic    =   dram_energy_total_dynamic   /   (real_layer_cycle * running_period)

        tot_word_ifmap_rd_dram_all  += tot_word_ifmap_rd_dram
        tot_word_filter_rd_dram_all += tot_word_filter_rd_dram
        tot_word_ofmap_rd_dram_all  += tot_word_ofmap_rd_dram
        tot_word_ofmap_wr_dram_all  += tot_word_ofmap_wr_dram

        dram_energy_ifmap_rd_all    += dram_energy_ifmap_rd
        dram_energy_filter_rd_all   += dram_energy_filter_rd
        dram_energy_ofmap_rd_all    += dram_energy_ofmap_rd
        dram_energy_ofmap_wr_all    += dram_energy_ofmap_wr
        dram_energy_total_dynamic_all += dram_energy_total_dynamic

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # SRAM: energy and power
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # this dynamic energy actually includes the energy for both writing from dram to sram and reading from sram to systolic array
        if ifmap_sram_exist == True:
            sram_energy_ifmap_rd    =   tot_access_ifmap_rd_sram * energy_per_block_rd_ifmap + \
                                        math.ceil(tot_word_ifmap_rd_dram / sram_block_sz_word) * energy_per_block_wr_ifmap
            sram_power_ifmap_rd     =   sram_energy_ifmap_rd    /  (real_layer_cycle * running_period)
        else:
            sram_energy_ifmap_rd    =   0
            sram_power_ifmap_rd     =   0
        
        # this dynamic energy actually includes the energy for both writing from dram to sram and reading from sram to systolic array
        if filter_sram_exist == True:
            sram_energy_filter_rd   =   tot_access_filter_rd_sram * energy_per_block_rd_filter + \
                                        math.ceil(tot_word_filter_rd_dram / sram_block_sz_word) * energy_per_block_wr_filter
            sram_power_filter_rd    =   sram_energy_filter_rd   /  (real_layer_cycle * running_period)
        else:
            sram_energy_filter_rd   =   0
            sram_power_filter_rd    =   0
        # this dynamic energy actually includes the energy for either writing from dram to sram or reading from sram to systolic array
        # those two situations will not happen simultaneously, if the sram for ofmap is large enough
        if ofmap_sram_exist == True:
            sram_energy_ofmap_rd    =   tot_access_ofmap_rd_sram * energy_per_block_rd_ofmap
            sram_power_ofmap_rd     =   sram_energy_ofmap_rd    /  (real_layer_cycle * running_period)

            sram_energy_ofmap_wr    =   tot_access_ofmap_wr_sram * energy_per_block_wr_ofmap + \
                                        math.ceil(tot_word_ofmap_wr_dram / sram_block_sz_word) * energy_per_block_rd_ofmap
            sram_power_ofmap_wr     =   sram_energy_ofmap_wr    /  (real_layer_cycle * running_period)
        else:
            sram_energy_ofmap_rd    =   0
            sram_power_ofmap_rd     =   0

            sram_energy_ofmap_wr    =   0
            sram_power_ofmap_wr     =   0
        

        sram_energy_dynamic         =   sram_energy_ifmap_rd + sram_energy_filter_rd + sram_energy_ofmap_rd + sram_energy_ofmap_wr

        sram_energy_ifmap_l         =   leakage_power_ifmap  * (real_layer_cycle * running_period)
        sram_energy_filter_l        =   leakage_power_filter * (real_layer_cycle * running_period)
        sram_energy_ofmap_l         =   leakage_power_ofmap  * (real_layer_cycle * running_period)
        sram_energy_leakage         =   sram_energy_ifmap_l + sram_energy_filter_l + sram_energy_ofmap_l
        sram_energy_total           =   sram_energy_dynamic + sram_energy_leakage

        sram_power_dynamic          =   sram_energy_dynamic     / (real_layer_cycle * running_period)

        sram_power_ifmap_l          =   sram_energy_ifmap_l     / (real_layer_cycle * running_period)
        sram_power_filter_l         =   sram_energy_filter_l    / (real_layer_cycle * running_period)
        sram_power_ofmap_l          =   sram_energy_ofmap_l     / (real_layer_cycle * running_period)
        sram_power_leakage          =   sram_energy_leakage     / (real_layer_cycle * running_period)
        sram_power_total            =   sram_energy_total       / (real_layer_cycle * running_period)
        
        tot_word_ifmap_rd_sram_all  += tot_word_ifmap_rd_sram
        tot_word_filter_rd_sram_all += tot_word_filter_rd_sram
        tot_word_ofmap_rd_sram_all  += tot_word_ofmap_rd_sram
        tot_word_ofmap_wr_sram_all  += tot_word_ofmap_wr_sram

        sram_energy_ifmap_rd_all    += sram_energy_ifmap_rd
        sram_energy_filter_rd_all   += sram_energy_filter_rd
        sram_energy_ofmap_rd_all    += sram_energy_ofmap_rd
        sram_energy_ofmap_wr_all    += sram_energy_ofmap_wr
        sram_energy_dynamic_all     += sram_energy_dynamic

        sram_energy_ifmap_l_all     += sram_energy_ifmap_l
        sram_energy_filter_l_all    += sram_energy_filter_l
        sram_energy_ofmap_l_all     += sram_energy_ofmap_l
        sram_energy_leakage_all     += sram_energy_leakage
        sram_energy_total_all       += sram_energy_total

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # systolic array: energy and power
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # ireg will toggle only when loading ifmaps
        sa_energy_ireg_d =   (array_h * ireg_dynamic_border + array_h * (array_w - 1) * ireg_dynamic_inner) * dynamic_cycle_ireg / mac_cycles * period
        sa_energy_ireg_l =   (array_h * ireg_leakage_border + array_h * (array_w - 1) * ireg_leakage_inner) * (real_layer_cycle * running_period)
        sa_energy_ireg   =   sa_energy_ireg_d + sa_energy_ireg_l
        
        sa_energy_ireg_d_all    +=  sa_energy_ireg_d
        sa_energy_ireg_l_all    +=  sa_energy_ireg_l
        sa_energy_ireg_all      +=  sa_energy_ireg

        # wreg will toggle only when loading filters
        sa_energy_wreg_d =   (array_h * wreg_dynamic_border + array_h * (array_w - 1) * wreg_dynamic_inner) * dynamic_cycle_wreg * period
        sa_energy_wreg_l =   (array_h * wreg_leakage_border + array_h * (array_w - 1) * wreg_leakage_inner) * (real_layer_cycle * running_period)
        sa_energy_wreg   =   sa_energy_wreg_d + sa_energy_wreg_l

        sa_energy_wreg_d_all    +=  sa_energy_wreg_d
        sa_energy_wreg_l_all    +=  sa_energy_wreg_l
        sa_energy_wreg_all      +=  sa_energy_wreg
        
        # mul and add (mac) will work only when computing with no stalls
        sa_energy_mul_d  =   (array_h * mul_dynamic_border + array_h * (array_w - 1) * mul_dynamic_inner) * dynamic_cycle_mac * period
        sa_energy_mul_l  =   (array_h * mul_leakage_border + array_h * (array_w - 1) * mul_leakage_inner) * (real_layer_cycle * running_period)
        sa_energy_mul    =   sa_energy_mul_d + sa_energy_mul_l

        sa_energy_mul_d_all    +=  sa_energy_mul_d
        sa_energy_mul_l_all    +=  sa_energy_mul_l
        sa_energy_mul_all      +=  sa_energy_mul

        sa_energy_acc_d  =   (array_h * acc_dynamic_border + array_h * (array_w - 1) * acc_dynamic_inner) * dynamic_cycle_mac * period
        sa_energy_acc_l  =   (array_h * acc_leakage_border + array_h * (array_w - 1) * acc_leakage_inner) * (real_layer_cycle * running_period)
        sa_energy_acc    =   sa_energy_acc_d + sa_energy_acc_l
        
        sa_energy_acc_d_all    +=  sa_energy_acc_d
        sa_energy_acc_l_all    +=  sa_energy_acc_l
        sa_energy_acc_all      +=  sa_energy_acc

        sa_energy_dynamic=  sa_energy_ireg_d + sa_energy_wreg_d + sa_energy_mul_d + sa_energy_acc_d
        sa_energy_leakage=  sa_energy_ireg_l + sa_energy_wreg_l + sa_energy_mul_l + sa_energy_acc_l
        sa_energy_tot    =  sa_energy_dynamic + sa_energy_leakage

        sa_energy_dynamic_all    +=  sa_energy_dynamic
        sa_energy_leakage_all    +=  sa_energy_leakage
        sa_energy_tot_all      +=  sa_energy_tot

        sa_power_ireg_d = sa_energy_ireg_d   / (real_layer_cycle * running_period)
        sa_power_ireg_l = sa_energy_ireg_l   / (real_layer_cycle * running_period)
        sa_power_ireg   = sa_energy_ireg     / (real_layer_cycle * running_period)
        sa_power_wreg_d = sa_energy_wreg_d   / (real_layer_cycle * running_period)
        sa_power_wreg_l = sa_energy_wreg_l   / (real_layer_cycle * running_period)
        sa_power_wreg   = sa_energy_wreg     / (real_layer_cycle * running_period)
        sa_power_mul_d  = sa_energy_mul_d    / (real_layer_cycle * running_period)
        sa_power_mul_l  = sa_energy_mul_l    / (real_layer_cycle * running_period)
        sa_power_mul    = sa_energy_mul      / (real_layer_cycle * running_period)
        sa_power_acc_d  = sa_energy_acc_d    / (real_layer_cycle * running_period)
        sa_power_acc_l  = sa_energy_acc_l    / (real_layer_cycle * running_period)
        sa_power_acc    = sa_energy_acc      / (real_layer_cycle * running_period)
        sa_power_dynamic= sa_power_ireg_d + sa_power_wreg_d + sa_power_mul_d + sa_power_acc_d
        sa_power_leakage= sa_power_ireg_l + sa_power_wreg_l + sa_power_mul_l + sa_power_acc_l
        sa_power_tot    = sa_power_dynamic + sa_power_leakage

        sys_energy_dynamic  = dram_energy_total_dynamic + sram_energy_dynamic + sa_energy_dynamic
        sys_energy_leakage  = sram_energy_leakage + sa_energy_leakage
        sys_energy_tot      = sys_energy_dynamic + sys_energy_leakage

        sys_energy_dynamic_all  += sys_energy_dynamic
        sys_energy_leakage_all  += sys_energy_leakage
        sys_energy_tot_all      += sys_energy_tot
        
        sys_power_dynamic   = sys_energy_dynamic / (real_layer_cycle * running_period)
        sys_power_leakage   = sys_energy_leakage / (real_layer_cycle * running_period)
        sys_power_tot       = sys_power_dynamic + sys_power_leakage
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # log generation
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

        energy_log +=       str(name) + ",\t" + str(layer_type) + ",\t" + \
                            str(dram_energy_ifmap_rd) + ",\t" + \
                            str(dram_energy_filter_rd) + ",\t" + \
                            str(dram_energy_ofmap_rd) + ",\t" + \
                            str(dram_energy_ofmap_wr) + ",\t" + \
                            str(dram_energy_total_dynamic) + ",\t" + \
                            str(sram_energy_ifmap_rd) + ",\t" + \
                            str(sram_energy_filter_rd) + ",\t" + \
                            str(sram_energy_ofmap_rd) + ",\t" + \
                            str(sram_energy_ofmap_wr) + ",\t" + \
                            str(sram_energy_dynamic) + ",\t" + \
                            str(sram_energy_ifmap_l) + ",\t" + \
                            str(sram_energy_filter_l) + ",\t" + \
                            str(sram_energy_ofmap_l) + ",\t" + \
                            str(sram_energy_leakage) + ",\t" + \
                            str(sram_energy_total) + ",\t" + \
                            str(sa_energy_ireg_d) + ",\t" + \
                            str(sa_energy_ireg_l) + ",\t" + \
                            str(sa_energy_ireg) + ",\t" + \
                            str(sa_energy_wreg_d) + ",\t" + \
                            str(sa_energy_wreg_l) + ",\t" + \
                            str(sa_energy_wreg) + ",\t" + \
                            str(sa_energy_mul_d) + ",\t" + \
                            str(sa_energy_mul_l) + ",\t" + \
                            str(sa_energy_mul) + ",\t" + \
                            str(sa_energy_acc_d) + ",\t" + \
                            str(sa_energy_acc_l) + ",\t" + \
                            str(sa_energy_acc) + ",\t" + \
                            str(sa_energy_dynamic) + ",\t" + \
                            str(sa_energy_leakage) + ",\t" + \
                            str(sa_energy_tot) + ",\t" + \
                            str(sys_energy_dynamic) + ",\t" + \
                            str(sys_energy_leakage) + ",\t" + \
                            str(sys_energy_tot) + ",\t\n"

        power_log +=        str(name) + ",\t" + str(layer_type) + ",\t" + \
                            str(dram_power_ifmap_rd) + ",\t" + \
                            str(dram_power_filter_rd) + ",\t" + \
                            str(dram_power_ofmap_rd) + ",\t" + \
                            str(dram_power_ofmap_wr) + ",\t" + \
                            str(dram_power_total_dynamic) + ",\t" + \
                            str(sram_power_ifmap_rd) + ",\t" + \
                            str(sram_power_filter_rd) + ",\t" + \
                            str(sram_power_ofmap_rd) + ",\t" + \
                            str(sram_power_ofmap_wr) + ",\t" + \
                            str(sram_power_dynamic) + ",\t" + \
                            str(sram_power_ifmap_l) + ",\t" + \
                            str(sram_power_filter_l) + ",\t" + \
                            str(sram_power_ofmap_l) + ",\t" + \
                            str(sram_power_leakage) + ",\t" + \
                            str(sram_power_total) + ",\t" + \
                            str(sa_power_ireg_d) + ",\t" + \
                            str(sa_power_ireg_l) + ",\t" + \
                            str(sa_power_ireg) + ",\t" + \
                            str(sa_power_wreg_d) + ",\t" + \
                            str(sa_power_wreg_l) + ",\t" + \
                            str(sa_power_wreg) + ",\t" + \
                            str(sa_power_mul_d) + ",\t" + \
                            str(sa_power_mul_l) + ",\t" + \
                            str(sa_power_mul) + ",\t" + \
                            str(sa_power_acc_d) + ",\t" + \
                            str(sa_power_acc_l) + ",\t" + \
                            str(sa_power_acc) + ",\t" + \
                            str(sa_power_dynamic) + ",\t" + \
                            str(sa_power_leakage) + ",\t" + \
                            str(sa_power_tot) + ",\t" + \
                            str(sys_power_dynamic) + ",\t" + \
                            str(sys_power_leakage) + ",\t" + \
                            str(sys_power_tot) + ",\t\n"
        
        print("All done for " + name)
    
    dram_power_ifmap_rd_all         = dram_energy_ifmap_rd_all      / (real_cycle_all * running_period)
    dram_power_filter_rd_all        = dram_energy_filter_rd_all     / (real_cycle_all * running_period)
    dram_power_ofmap_rd_all         = dram_energy_ofmap_rd_all      / (real_cycle_all * running_period)
    dram_power_ofmap_wr_all         = dram_energy_ofmap_wr_all      / (real_cycle_all * running_period)
    dram_power_total_dynamic_all    = dram_energy_total_dynamic_all / (real_cycle_all * running_period)
    sram_power_ifmap_rd_all         = sram_energy_ifmap_rd_all      / (real_cycle_all * running_period)
    sram_power_filter_rd_all        = sram_energy_filter_rd_all     / (real_cycle_all * running_period)
    sram_power_ofmap_rd_all         = sram_energy_ofmap_rd_all      / (real_cycle_all * running_period)
    sram_power_ofmap_wr_all         = sram_energy_ofmap_wr_all      / (real_cycle_all * running_period)
    sram_power_dynamic_all          = sram_energy_dynamic_all       / (real_cycle_all * running_period)
    sram_power_ifmap_l_all          = sram_energy_ifmap_l_all       / (real_cycle_all * running_period)
    sram_power_filter_l_all         = sram_energy_filter_l_all      / (real_cycle_all * running_period)
    sram_power_ofmap_l_all          = sram_energy_ofmap_l_all       / (real_cycle_all * running_period)
    sram_power_leakage_all          = sram_energy_leakage_all       / (real_cycle_all * running_period)
    sram_power_total_all            = sram_energy_total_all         / (real_cycle_all * running_period)
    sa_power_ireg_d_all             = sa_energy_ireg_d_all          / (real_cycle_all * running_period)
    sa_power_ireg_l_all             = sa_energy_ireg_l_all          / (real_cycle_all * running_period)
    sa_power_ireg_all               = sa_energy_ireg_all            / (real_cycle_all * running_period)
    sa_power_wreg_d_all             = sa_energy_wreg_d_all          / (real_cycle_all * running_period)
    sa_power_wreg_l_all             = sa_energy_wreg_l_all          / (real_cycle_all * running_period)
    sa_power_wreg_all               = sa_energy_wreg_all            / (real_cycle_all * running_period)
    sa_power_mul_d_all              = sa_energy_mul_d_all           / (real_cycle_all * running_period)
    sa_power_mul_l_all              = sa_energy_mul_l_all           / (real_cycle_all * running_period)
    sa_power_mul_all                = sa_energy_mul_all             / (real_cycle_all * running_period)
    sa_power_acc_d_all              = sa_energy_acc_d_all           / (real_cycle_all * running_period)
    sa_power_acc_l_all              = sa_energy_acc_l_all           / (real_cycle_all * running_period)
    sa_power_acc_all                = sa_energy_acc_all             / (real_cycle_all * running_period)
    sa_power_dynamic_all            = sa_energy_dynamic_all         / (real_cycle_all * running_period)
    sa_power_leakage_all            = sa_energy_leakage_all         / (real_cycle_all * running_period)
    sa_power_tot_all                = sa_energy_tot_all             / (real_cycle_all * running_period)
    sys_power_dynamic_all           = sys_energy_dynamic_all        / (real_cycle_all * running_period)
    sys_power_leakage_all           = sys_energy_leakage_all        / (real_cycle_all * running_period)
    sys_power_tot_all               = sys_energy_tot_all            / (real_cycle_all * running_period)

    energy_log +=       str(run_name) + ",\t" + "All" + ",\t" + \
                        str(dram_energy_ifmap_rd_all) + ",\t" + \
                        str(dram_energy_filter_rd_all) + ",\t" + \
                        str(dram_energy_ofmap_rd_all) + ",\t" + \
                        str(dram_energy_ofmap_wr_all) + ",\t" + \
                        str(dram_energy_total_dynamic_all) + ",\t" + \
                        str(sram_energy_ifmap_rd_all) + ",\t" + \
                        str(sram_energy_filter_rd_all) + ",\t" + \
                        str(sram_energy_ofmap_rd_all) + ",\t" + \
                        str(sram_energy_ofmap_wr_all) + ",\t" + \
                        str(sram_energy_dynamic_all) + ",\t" + \
                        str(sram_energy_ifmap_l_all) + ",\t" + \
                        str(sram_energy_filter_l_all) + ",\t" + \
                        str(sram_energy_ofmap_l_all) + ",\t" + \
                        str(sram_energy_leakage_all) + ",\t" + \
                        str(sram_energy_total_all) + ",\t" + \
                        str(sa_energy_ireg_d_all) + ",\t" + \
                        str(sa_energy_ireg_l_all) + ",\t" + \
                        str(sa_energy_ireg_all) + ",\t" + \
                        str(sa_energy_wreg_d_all) + ",\t" + \
                        str(sa_energy_wreg_l_all) + ",\t" + \
                        str(sa_energy_wreg_all) + ",\t" + \
                        str(sa_energy_mul_d_all) + ",\t" + \
                        str(sa_energy_mul_l_all) + ",\t" + \
                        str(sa_energy_mul_all) + ",\t" + \
                        str(sa_energy_acc_d_all) + ",\t" + \
                        str(sa_energy_acc_l_all) + ",\t" + \
                        str(sa_energy_acc_all) + ",\t" + \
                        str(sa_energy_dynamic_all) + ",\t" + \
                        str(sa_energy_leakage_all) + ",\t" + \
                        str(sa_energy_tot_all) + ",\t" + \
                        str(sys_energy_dynamic_all) + ",\t" + \
                        str(sys_energy_leakage_all) + ",\t" + \
                        str(sys_energy_tot_all) + ",\t\n"

    power_log +=        str(run_name) + ",\t" + "All" + ",\t" + \
                        str(dram_power_ifmap_rd_all) + ",\t" + \
                        str(dram_power_filter_rd_all) + ",\t" + \
                        str(dram_power_ofmap_rd_all) + ",\t" + \
                        str(dram_power_ofmap_wr_all) + ",\t" + \
                        str(dram_power_total_dynamic_all) + ",\t" + \
                        str(sram_power_ifmap_rd_all) + ",\t" + \
                        str(sram_power_filter_rd_all) + ",\t" + \
                        str(sram_power_ofmap_rd_all) + ",\t" + \
                        str(sram_power_ofmap_wr_all) + ",\t" + \
                        str(sram_power_dynamic_all) + ",\t" + \
                        str(sram_power_ifmap_l_all) + ",\t" + \
                        str(sram_power_filter_l_all) + ",\t" + \
                        str(sram_power_ofmap_l_all) + ",\t" + \
                        str(sram_power_leakage_all) + ",\t" + \
                        str(sram_power_total_all) + ",\t" + \
                        str(sa_power_ireg_d_all) + ",\t" + \
                        str(sa_power_ireg_l_all) + ",\t" + \
                        str(sa_power_ireg_all) + ",\t" + \
                        str(sa_power_wreg_d_all) + ",\t" + \
                        str(sa_power_wreg_l_all) + ",\t" + \
                        str(sa_power_wreg_all) + ",\t" + \
                        str(sa_power_mul_d_all) + ",\t" + \
                        str(sa_power_mul_l_all) + ",\t" + \
                        str(sa_power_mul_all) + ",\t" + \
                        str(sa_power_acc_d_all) + ",\t" + \
                        str(sa_power_acc_l_all) + ",\t" + \
                        str(sa_power_acc_all) + ",\t" + \
                        str(sa_power_dynamic_all) + ",\t" + \
                        str(sa_power_leakage_all) + ",\t" + \
                        str(sa_power_tot_all) + ",\t" + \
                        str(sys_power_dynamic_all) + ",\t" + \
                        str(sys_power_leakage_all) + ",\t" + \
                        str(sys_power_tot_all) + ",\t\n"

    area.write(area_log)
    energy.write(energy_log)
    power.write(power_log)

    area.close()
    energy.close()
    power.close()
    param_file.close()

def prune(input_list):
    l = []

    for e in input_list:
        e = e.strip() # remove the leading and trailing characters, here space
        if e != '' and e != ' ':
            l.append(e)

    return l


if __name__ == "__main__":
    estimate(run_name="example_run")