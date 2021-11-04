import math
import simHw.block_trace as block_trace
import configparser as cp

def profiling(
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
    this code take the ideal trace from the simArch, and generate detailed runtime statistics with real hardware
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

    dram_bw_ideal_ifmap_rd_all      =   0
    dram_bw_ideal_filter_rd_all     =   0
    dram_bw_ideal_ofmap_rd_all      =   0
    dram_bw_ideal_ofmap_wr_all      =   0
    dram_bw_ideal_total_all         =   0

    dram_bw_real_ifmap_rd       =   0
    dram_bw_real_filter_rd      =   0
    dram_bw_real_ofmap_rd       =   0
    dram_bw_real_ofmap_wr       =   0
    dram_bw_real_total          =   0

    dram_bw_real_ifmap_rd_all       =   0
    dram_bw_real_filter_rd_all      =   0
    dram_bw_real_ofmap_rd_all       =   0
    dram_bw_real_ofmap_wr_all       =   0
    dram_bw_real_total_all          =   0

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
    sram_bank = 0
    sram_block_sz_bytes = 0
    
    sram_bw_ideal_ifmap_rd      =   0
    sram_bw_ideal_filter_rd     =   0
    sram_bw_ideal_ofmap_rd      =   0
    sram_bw_ideal_ofmap_wr      =   0
    sram_bw_ideal_total         =   0

    sram_bw_ideal_ifmap_rd_all      =   0
    sram_bw_ideal_filter_rd_all     =   0
    sram_bw_ideal_ofmap_rd_all      =   0
    sram_bw_ideal_ofmap_wr_all      =   0
    sram_bw_ideal_total_all         =   0

    sram_bw_real_ifmap_rd       =   0
    sram_bw_real_filter_rd      =   0
    sram_bw_real_ofmap_rd       =   0
    sram_bw_real_ofmap_wr       =   0
    sram_bw_real_total          =   0

    sram_bw_real_ifmap_rd_all       =   0
    sram_bw_real_filter_rd_all      =   0
    sram_bw_real_ofmap_rd_all       =   0
    sram_bw_real_ofmap_wr_all       =   0
    sram_bw_real_total_all          =   0

    # working cycles
    ideal_max_clk = 0
    ideal_min_clk = 0
    ideal_layer_cycle = 0
    ideal_layer_sec = 0
    ideal_layer_throughput = 0

    ideal_cycle_all = 0
    ideal_sec_all = 0
    ideal_throughput_all = 0

    real_max_clk = 0
    real_min_clk = 0
    real_layer_cycle = 0
    real_layer_sec = 0
    real_layer_throughput = 0

    real_cycle_all = 0
    real_sec_all = 0
    real_throughput_all = 0

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

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # output report
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    detail_ideal    = open(run_name + "_detail_ideal.csv", 'w')
    detail_real     = open(run_name + "_detail_real.csv", 'w')
    bw_ideal        = open(run_name + "_avg_bw_ideal.csv", 'w')
    bw_real         = open(run_name + "_avg_bw_real.csv", 'w')
    tp_ideal        = open(run_name + "_throughput_ideal.csv", 'w')
    tp_real         = open(run_name + "_throughput_real.csv", 'w')
    hw_runtime      = open(run_name + "_hw_runtime.csv", 'w')

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
                    "DRAM I RD BW (GBytes/sec),\tDRAM F RD BW (GBytes/sec),\tDRAM O RD BW (GBytes/sec),\tDRAM O WR BW (GBytes/sec),\tDRAM BW Total (GBytes/sec),\t" + \
                    "SRAM I RD BW (GBytes/sec),\tSRAM F RD BW (GBytes/sec),\tSRAM O RD BW (GBytes/sec),\tSRAM O WR BW (GBytes/sec),\tSRAM BW Total (GBytes/sec),\t\n"
    
    bw_real_log =   "Layer,\tType,\t" + \
                    "DRAM I RD BW (GBytes/sec),\tDRAM F RD BW (GBytes/sec),\tDRAM O RD BW (GBytes/sec),\tDRAM O WR BW (GBytes/sec),\tDRAM BW Total (GBytes/sec),\t" + \
                    "SRAM I RD BW (GBytes/sec),\tSRAM F RD BW (GBytes/sec),\tSRAM O RD BW (GBytes/sec),\tSRAM O WR BW (GBytes/sec),\tSRAM BW Total (GBytes/sec),\t\n"
    
    tp_ideal_log =  "Layer,\tType,\t" + \
                    "Cycle Total (Cycles),\tTime Total (Secs),\tThroughput (Frames/sec)\t\n"
    
    tp_real_log =  "Layer,\tType,\t" + \
                    "Cycle Total (Cycles),\tTime Total (Secs),\tThroughput (Frames/sec)\t\n"
    
    hw_runtime_log =  "Layer,\tType,\t" + \
                    "tot_word_ifmap_rd_dram,\t" + \
                    "max_word_ifmap_rd_dram,\t" + \
                    "tot_access_ifmap_rd_dram,\t" + \
                    "tot_row_access_ifmap_rd_dram,\t" + \
                    "act_cycles_ifmap_rd_dram,\t" + \
                    "shift_cycles_ifmap_rd_dram,\t" + \
                    "ideal_start_cycle_ifmap_rd_dram,\t" + \
                    "ideal_end_cycle_ifmap_rd_dram,\t" + \
                    "real_start_cycle_ifmap_rd_dram,\t" + \
                    "real_end_cycle_ifmap_rd_dram,\t" + \
                    "tot_word_filter_rd_dram,\t" + \
                    "max_word_filter_rd_dram,\t" + \
                    "tot_access_filter_rd_dram,\t" + \
                    "tot_row_access_filter_rd_dram,\t" + \
                    "act_cycles_filter_rd_dram,\t" + \
                    "shift_cycles_filter_rd_dram,\t" + \
                    "ideal_start_cycle_filter_rd_dram,\t" + \
                    "ideal_end_cycle_filter_rd_dram,\t" + \
                    "real_start_cycle_filter_rd_dram,\t" + \
                    "real_end_cycle_filter_rd_dram,\t" + \
                    "tot_word_ofmap_rd_dram,\t" + \
                    "max_word_ofmap_rd_dram,\t" + \
                    "tot_access_ofmap_rd_dram,\t" + \
                    "tot_row_access_ofmap_rd_dram,\t" + \
                    "act_cycles_ofmap_rd_dram,\t" + \
                    "shift_cycles_ofmap_rd_dram,\t" + \
                    "ideal_start_cycle_ofmap_rd_dram,\t" + \
                    "ideal_end_cycle_ofmap_rd_dram,\t" + \
                    "real_start_cycle_ofmap_rd_dram,\t" + \
                    "real_end_cycle_ofmap_rd_dram,\t" + \
                    "tot_word_ofmap_wr_dram,\t" + \
                    "max_word_ofmap_wr_dram,\t" + \
                    "tot_access_ofmap_wr_dram,\t" + \
                    "tot_row_access_ofmap_wr_dram,\t" + \
                    "act_cycles_ofmap_wr_dram,\t" + \
                    "shift_cycles_ofmap_wr_dram,\t" + \
                    "ideal_start_cycle_ofmap_wr_dram,\t" + \
                    "ideal_end_cycle_ofmap_wr_dram,\t" + \
                    "real_start_cycle_ofmap_wr_dram,\t" + \
                    "real_end_cycle_ofmap_wr_dram,\t" + \
                    "tot_word_ifmap_rd_sram,\t" + \
                    "max_word_ifmap_rd_sram,\t" + \
                    "tot_access_ifmap_rd_sram,\t" + \
                    "max_access_ifmap_rd_sram,\t" + \
                    "act_cycles_ifmap_rd_sram,\t" + \
                    "stall_cycles_ifmap_rd_sram,\t" + \
                    "ideal_start_cycle_ifmap_rd_sram,\t" + \
                    "ideal_end_cycle_ifmap_rd_sram,\t" + \
                    "real_start_cycle_ifmap_rd_sram,\t" + \
                    "real_end_cycle_ifmap_rd_sram,\t" + \
                    "tot_word_filter_rd_sram,\t" + \
                    "max_word_filter_rd_sram,\t" + \
                    "tot_access_filter_rd_sram,\t" + \
                    "max_access_filter_rd_sram,\t" + \
                    "act_cycles_filter_rd_sram,\t" + \
                    "stall_cycles_filter_rd_sram,\t" + \
                    "ideal_start_cycle_filter_rd_sram,\t" + \
                    "ideal_end_cycle_filter_rd_sram,\t" + \
                    "real_start_cycle_filter_rd_sram,\t" + \
                    "real_end_cycle_filter_rd_sram,\t" + \
                    "tot_word_ofmap_rd_sram,\t" + \
                    "max_word_ofmap_rd_sram,\t" + \
                    "tot_access_ofmap_rd_sram,\t" + \
                    "max_access_ofmap_rd_sram,\t" + \
                    "act_cycles_ofmap_rd_sram,\t" + \
                    "stall_cycles_ofmap_rd_sram,\t" + \
                    "ideal_start_cycle_ofmap_rd_sram,\t" + \
                    "ideal_end_cycle_ofmap_rd_sram,\t" + \
                    "real_start_cycle_ofmap_rd_sram,\t" + \
                    "real_end_cycle_ofmap_rd_sram,\t" + \
                    "tot_word_ofmap_wr_sram,\t" + \
                    "max_word_ofmap_wr_sram,\t" + \
                    "tot_access_ofmap_wr_sram,\t" + \
                    "max_access_ofmap_wr_sram,\t" + \
                    "act_cycles_ofmap_wr_sram,\t" + \
                    "stall_cycles_ofmap_wr_sram,\t" + \
                    "ideal_start_cycle_ofmap_wr_sram,\t" + \
                    "ideal_end_cycle_ofmap_wr_sram,\t" + \
                    "real_start_cycle_ofmap_wr_sram,\t" + \
                    "real_end_cycle_ofmap_wr_sram,\t" + \
                    "ideal_layer_cycle,\t" + \
                    "ideal_layer_sec,\t" + \
                    "real_layer_cycle,\t" + \
                    "real_layer_sec,\t" + \
                    "act_cycle_ifmap_rd,\t" + \
                    "act_cycle_filter_rd,\t" + \
                    "act_cycle_ofmap_rd,\t" + \
                    "act_cycle_ofmap_wr,\t" + \
                    "dynamic_cycle_ireg,\t" + \
                    "dynamic_cycle_wreg,\t" + \
                    "dynamic_cycle_mac,\t" + \
                    "\n"

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # DRAM parameter
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
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
    # SRAM parameter
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
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

    first = True
    for row in param_file:
        # per layer trace profiling to get real runtime statistics
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
        act_cycles_ifmap_rd_dram, \
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
        act_cycles_filter_rd_dram, \
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
            act_cycles_ofmap_rd_dram = 0
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
            act_cycles_ofmap_rd_dram, \
            shift_cycles_ofmap_rd_dram, \
            ideal_start_cycle_ofmap_rd_dram, \
            ideal_end_cycle_ofmap_rd_dram = block_trace.ddr3_8x8_profiling(
                        trace_file=trace_file,
                        word_sz_bytes=word_sz_bytes,
                        page_bits=dram_page_bits,
                        min_addr_word=ofmap_base,
                        max_addr_word=ofmap_base + filter_base - ifmap_base)
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
        act_cycles_ofmap_wr_dram, \
        shift_cycles_ofmap_wr_dram, \
        ideal_start_cycle_ofmap_wr_dram, \
        ideal_end_cycle_ofmap_wr_dram = block_trace.ddr3_8x8_profiling(
                    trace_file=trace_file,
                    word_sz_bytes=word_sz_bytes,
                    page_bits=dram_page_bits,
                    min_addr_word=ofmap_base,
                    max_addr_word=ofmap_base + filter_base - ifmap_base)
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
                        max_addr_word=ofmap_base + filter_base - ifmap_base,
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
                        max_addr_word=ofmap_base + filter_base - ifmap_base,
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
                            ideal_end_cycle_ofmap_wr_sram)
        ideal_min_clk = min(ideal_start_cycle_ifmap_rd_dram, 
                            ideal_start_cycle_filter_rd_dram, 
                            ideal_start_cycle_ofmap_rd_dram, 
                            ideal_start_cycle_ofmap_wr_dram, 
                            ideal_start_cycle_ifmap_rd_sram, 
                            ideal_start_cycle_filter_rd_sram, 
                            ideal_start_cycle_ofmap_rd_sram, 
                            ideal_start_cycle_ofmap_wr_sram)
        ideal_layer_cycle = ideal_max_clk - ideal_min_clk + 1
        ideal_layer_sec = ideal_layer_cycle * running_period / float(10**6)
        ideal_layer_throughput = 1 / ideal_layer_sec
        ideal_cycle_all += ideal_layer_cycle
        ideal_sec_all += ideal_layer_sec
        # sram stall and dram shift have similar meanings: the extra cycle for data access compared to the ideal
        # sram stall can be overlapped for stall_cycles_ifmap_rd_sram and stall_cycles_ofmap_rd_sram due to multiple copies of sram
        # dram shift can't be overlapped due to sharing the same dram IO
        real_max_clk =  ideal_max_clk + \
                        stall_cycles_filter_rd_sram + max(stall_cycles_ifmap_rd_sram, stall_cycles_ofmap_rd_sram) + stall_cycles_ofmap_wr_sram + \
                        shift_cycles_ofmap_rd_dram + shift_cycles_ofmap_wr_dram
        real_min_clk =  ideal_min_clk - \
                        shift_cycles_ifmap_rd_dram - shift_cycles_filter_rd_dram
        real_layer_cycle = real_max_clk - real_min_clk + 1
        real_layer_sec = real_layer_cycle * running_period / float(10**6)
        real_layer_throughput = 1 / real_layer_sec
        real_cycle_all += real_layer_cycle
        real_sec_all += real_layer_sec

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # DRAM: bw
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        dram_bw_ideal_ifmap_rd      =   tot_word_ifmap_rd_dram  * word_sz_bytes / float(2**30) / ideal_layer_sec
        dram_bw_ideal_filter_rd     =   tot_word_filter_rd_dram * word_sz_bytes / float(2**30) / ideal_layer_sec
        dram_bw_ideal_ofmap_rd      =   tot_word_ofmap_rd_dram  * word_sz_bytes / float(2**30) / ideal_layer_sec
        dram_bw_ideal_ofmap_wr      =   tot_word_ofmap_wr_dram  * word_sz_bytes / float(2**30) / ideal_layer_sec
        dram_bw_ideal_total         =   dram_bw_ideal_ifmap_rd + dram_bw_ideal_filter_rd + dram_bw_ideal_ofmap_rd + dram_bw_ideal_ofmap_wr

        dram_bw_real_ifmap_rd       =   tot_word_ifmap_rd_dram  * word_sz_bytes / float(2**30) / real_layer_sec
        dram_bw_real_filter_rd      =   tot_word_filter_rd_dram * word_sz_bytes / float(2**30) / real_layer_sec
        dram_bw_real_ofmap_rd       =   tot_word_ofmap_rd_dram  * word_sz_bytes / float(2**30) / real_layer_sec
        dram_bw_real_ofmap_wr       =   tot_word_ofmap_wr_dram  * word_sz_bytes / float(2**30) / real_layer_sec
        dram_bw_real_total          =   dram_bw_real_ifmap_rd + dram_bw_real_filter_rd + dram_bw_real_ofmap_rd + dram_bw_real_ofmap_wr

        tot_word_ifmap_rd_dram_all  += tot_word_ifmap_rd_dram
        tot_word_filter_rd_dram_all += tot_word_filter_rd_dram
        tot_word_ofmap_rd_dram_all  += tot_word_ofmap_rd_dram
        tot_word_ofmap_wr_dram_all  += tot_word_ofmap_wr_dram

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # SRAM: bw,
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        if ifmap_sram_exist == True:
            sram_bw_ideal_ifmap_rd  =   tot_word_ifmap_rd_sram  * word_sz_bytes / float(2**30) / ideal_layer_sec
            sram_bw_real_ifmap_rd   =   tot_word_ifmap_rd_sram  * word_sz_bytes / float(2**30) / real_layer_sec
        else:
            sram_bw_ideal_ifmap_rd  =   0
            sram_bw_real_ifmap_rd   =   0
        
        if filter_sram_exist == True:
            sram_bw_ideal_filter_rd =   tot_word_filter_rd_sram  * word_sz_bytes / float(2**30) / ideal_layer_sec
            sram_bw_real_filter_rd  =   tot_word_filter_rd_sram  * word_sz_bytes / float(2**30) / real_layer_sec
        else:
            sram_bw_ideal_filter_rd =   0
            sram_bw_real_filter_rd  =   0

        # those two situations will not happen simultaneously, if the sram for ofmap is large enough
        if ofmap_sram_exist == True:
            sram_bw_ideal_ofmap_rd  =   tot_word_ofmap_rd_sram   * word_sz_bytes / float(2**30) / ideal_layer_sec
            sram_bw_real_ofmap_rd   =   tot_word_ofmap_rd_sram   * word_sz_bytes / float(2**30) / real_layer_sec

            sram_bw_ideal_ofmap_wr  =   tot_word_ofmap_wr_sram   * word_sz_bytes / float(2**30) / ideal_layer_sec
            sram_bw_real_ofmap_wr   =   tot_word_ofmap_wr_sram   * word_sz_bytes / float(2**30) / real_layer_sec
        else:
            sram_bw_ideal_ofmap_rd  =   0
            sram_bw_real_ofmap_rd   =   0

            sram_bw_ideal_ofmap_wr  =   0
            sram_bw_real_ofmap_wr   =   0
        
        sram_bw_ideal_total = sram_bw_ideal_ifmap_rd + sram_bw_ideal_filter_rd + sram_bw_ideal_ofmap_rd + sram_bw_ideal_ofmap_wr
        sram_bw_real_total = sram_bw_real_ifmap_rd + sram_bw_real_filter_rd + sram_bw_real_ofmap_rd + sram_bw_real_ofmap_wr
        
        tot_word_ifmap_rd_sram_all  += tot_word_ifmap_rd_sram
        tot_word_filter_rd_sram_all += tot_word_filter_rd_sram
        tot_word_ofmap_rd_sram_all  += tot_word_ofmap_rd_sram
        tot_word_ofmap_wr_sram_all  += tot_word_ofmap_wr_sram

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # systolic array: run time cycle
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # cycles for pe to be active: during ifmap streaming and ofmap streaming
        if ifmap_sram_exist == True:
            act_cycle_ifmap_rd = act_cycles_ifmap_rd_sram
        else:
            act_cycle_ifmap_rd = act_cycles_ifmap_rd_dram
        
        if filter_sram_exist == True:
            act_cycle_filter_rd = act_cycles_filter_rd_sram
        else:
            act_cycle_filter_rd = act_cycles_filter_rd_dram

        if ofmap_sram_exist == True:
            act_cycle_ofmap_rd = act_cycles_ofmap_rd_sram
        else:
            act_cycle_ofmap_rd = act_cycles_ofmap_rd_dram

        if ofmap_sram_exist == True:
            act_cycle_ofmap_wr = act_cycles_ofmap_wr_sram
        else:
            act_cycle_ofmap_wr = act_cycles_ofmap_wr_dram

        dynamic_cycle_ireg = act_cycle_ifmap_rd
        dynamic_cycle_wreg = act_cycle_filter_rd
        dynamic_cycle_mac = max(act_cycle_ifmap_rd, act_cycle_ofmap_rd, act_cycle_ofmap_wr)

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
        
        tp_ideal_log +=     str(name) + ",\t" + str(layer_type) + ",\t" + \
                            str(ideal_layer_cycle) + ",\t" + \
                            str(ideal_layer_sec) + ",\t" + \
                            str(ideal_layer_throughput) + ",\t\n"
        
        tp_real_log +=      str(name) + ",\t" + str(layer_type) + ",\t" + \
                            str(real_layer_cycle) + ",\t" + \
                            str(real_layer_sec) + ",\t" + \
                            str(real_layer_throughput) + ",\t\n"
        
        hw_runtime_log +=   str(name) + ",\t" + str(layer_type) + ",\t" + \
                            str(tot_word_ifmap_rd_dram) + ",\t" + \
                            str(max_word_ifmap_rd_dram) + ",\t" + \
                            str(tot_access_ifmap_rd_dram) + ",\t" + \
                            str(tot_row_access_ifmap_rd_dram) + ",\t" + \
                            str(act_cycles_ifmap_rd_dram) + ",\t" + \
                            str(shift_cycles_ifmap_rd_dram) + ",\t" + \
                            str(ideal_start_cycle_ifmap_rd_dram) + ",\t" + \
                            str(ideal_end_cycle_ifmap_rd_dram) + ",\t" + \
                            str(real_start_cycle_ifmap_rd_dram) + ",\t" + \
                            str(real_end_cycle_ifmap_rd_dram) + ",\t" + \
                            str(tot_word_filter_rd_dram) + ",\t" + \
                            str(max_word_filter_rd_dram) + ",\t" + \
                            str(tot_access_filter_rd_dram) + ",\t" + \
                            str(tot_row_access_filter_rd_dram) + ",\t" + \
                            str(act_cycles_filter_rd_dram) + ",\t" + \
                            str(shift_cycles_filter_rd_dram) + ",\t" + \
                            str(ideal_start_cycle_filter_rd_dram) + ",\t" + \
                            str(ideal_end_cycle_filter_rd_dram) + ",\t" + \
                            str(real_start_cycle_filter_rd_dram) + ",\t" + \
                            str(real_end_cycle_filter_rd_dram) + ",\t" + \
                            str(tot_word_ofmap_rd_dram) + ",\t" + \
                            str(max_word_ofmap_rd_dram) + ",\t" + \
                            str(tot_access_ofmap_rd_dram) + ",\t" + \
                            str(tot_row_access_ofmap_rd_dram) + ",\t" + \
                            str(act_cycles_ofmap_rd_dram) + ",\t" + \
                            str(shift_cycles_ofmap_rd_dram) + ",\t" + \
                            str(ideal_start_cycle_ofmap_rd_dram) + ",\t" + \
                            str(ideal_end_cycle_ofmap_rd_dram) + ",\t" + \
                            str(real_start_cycle_ofmap_rd_dram) + ",\t" + \
                            str(real_end_cycle_ofmap_rd_dram) + ",\t" + \
                            str(tot_word_ofmap_wr_dram) + ",\t" + \
                            str(max_word_ofmap_wr_dram) + ",\t" + \
                            str(tot_access_ofmap_wr_dram) + ",\t" + \
                            str(tot_row_access_ofmap_wr_dram) + ",\t" + \
                            str(act_cycles_ofmap_wr_dram) + ",\t" + \
                            str(shift_cycles_ofmap_wr_dram) + ",\t" + \
                            str(ideal_start_cycle_ofmap_wr_dram) + ",\t" + \
                            str(ideal_end_cycle_ofmap_wr_dram) + ",\t" + \
                            str(real_start_cycle_ofmap_wr_dram) + ",\t" + \
                            str(real_end_cycle_ofmap_wr_dram) + ",\t" + \
                            str(tot_word_ifmap_rd_sram) + ",\t" + \
                            str(max_word_ifmap_rd_sram) + ",\t" + \
                            str(tot_access_ifmap_rd_sram) + ",\t" + \
                            str(max_access_ifmap_rd_sram) + ",\t" + \
                            str(act_cycles_ifmap_rd_sram) + ",\t" + \
                            str(stall_cycles_ifmap_rd_sram) + ",\t" + \
                            str(ideal_start_cycle_ifmap_rd_sram) + ",\t" + \
                            str(ideal_end_cycle_ifmap_rd_sram) + ",\t" + \
                            str(real_start_cycle_ifmap_rd_sram) + ",\t" + \
                            str(real_end_cycle_ifmap_rd_sram) + ",\t" + \
                            str(tot_word_filter_rd_sram) + ",\t" + \
                            str(max_word_filter_rd_sram) + ",\t" + \
                            str(tot_access_filter_rd_sram) + ",\t" + \
                            str(max_access_filter_rd_sram) + ",\t" + \
                            str(act_cycles_filter_rd_sram) + ",\t" + \
                            str(stall_cycles_filter_rd_sram) + ",\t" + \
                            str(ideal_start_cycle_filter_rd_sram) + ",\t" + \
                            str(ideal_end_cycle_filter_rd_sram) + ",\t" + \
                            str(real_start_cycle_filter_rd_sram) + ",\t" + \
                            str(real_end_cycle_filter_rd_sram) + ",\t" + \
                            str(tot_word_ofmap_rd_sram) + ",\t" + \
                            str(max_word_ofmap_rd_sram) + ",\t" + \
                            str(tot_access_ofmap_rd_sram) + ",\t" + \
                            str(max_access_ofmap_rd_sram) + ",\t" + \
                            str(act_cycles_ofmap_rd_sram) + ",\t" + \
                            str(stall_cycles_ofmap_rd_sram) + ",\t" + \
                            str(ideal_start_cycle_ofmap_rd_sram) + ",\t" + \
                            str(ideal_end_cycle_ofmap_rd_sram) + ",\t" + \
                            str(real_start_cycle_ofmap_rd_sram) + ",\t" + \
                            str(real_end_cycle_ofmap_rd_sram) + ",\t" + \
                            str(tot_word_ofmap_wr_sram) + ",\t" + \
                            str(max_word_ofmap_wr_sram) + ",\t" + \
                            str(tot_access_ofmap_wr_sram) + ",\t" + \
                            str(max_access_ofmap_wr_sram) + ",\t" + \
                            str(act_cycles_ofmap_wr_sram) + ",\t" + \
                            str(stall_cycles_ofmap_wr_sram) + ",\t" + \
                            str(ideal_start_cycle_ofmap_wr_sram) + ",\t" + \
                            str(ideal_end_cycle_ofmap_wr_sram) + ",\t" + \
                            str(real_start_cycle_ofmap_wr_sram) + ",\t" + \
                            str(real_end_cycle_ofmap_wr_sram) + ",\t" + \
                            str(ideal_layer_cycle) + ",\t" + \
                            str(ideal_layer_sec) + ",\t" + \
                            str(real_layer_cycle) + ",\t" + \
                            str(real_layer_sec) + ",\t" + \
                            str(act_cycle_ifmap_rd) + ",\t" + \
                            str(act_cycle_filter_rd) + ",\t" + \
                            str(act_cycle_ofmap_rd) + ",\t" + \
                            str(act_cycle_ofmap_wr) + ",\t" + \
                            str(dynamic_cycle_ireg) + ",\t" + \
                            str(dynamic_cycle_wreg) + ",\t" + \
                            str(dynamic_cycle_mac) + ",\t" + \
                            "\n"

        print("All done for " + name)

    dram_bw_ideal_ifmap_rd_all      =   tot_word_ifmap_rd_dram_all  * word_sz_bytes / float(2**30) / ideal_sec_all
    dram_bw_ideal_filter_rd_all     =   tot_word_filter_rd_dram_all * word_sz_bytes / float(2**30) / ideal_sec_all
    dram_bw_ideal_ofmap_rd_all      =   tot_word_ofmap_rd_dram_all  * word_sz_bytes / float(2**30) / ideal_sec_all
    dram_bw_ideal_ofmap_wr_all      =   tot_word_ofmap_wr_dram_all  * word_sz_bytes / float(2**30) / ideal_sec_all
    dram_bw_ideal_total_all         =   dram_bw_ideal_ifmap_rd_all + dram_bw_ideal_filter_rd_all + dram_bw_ideal_ofmap_rd_all + dram_bw_ideal_ofmap_wr_all

    dram_bw_real_ifmap_rd_all       =   tot_word_ifmap_rd_dram_all  * word_sz_bytes / float(2**30) / real_sec_all
    dram_bw_real_filter_rd_all      =   tot_word_filter_rd_dram_all * word_sz_bytes / float(2**30) / real_sec_all
    dram_bw_real_ofmap_rd_all       =   tot_word_ofmap_rd_dram_all  * word_sz_bytes / float(2**30) / real_sec_all
    dram_bw_real_ofmap_wr_all       =   tot_word_ofmap_wr_dram_all  * word_sz_bytes / float(2**30) / real_sec_all
    dram_bw_real_total_all          =   dram_bw_real_ifmap_rd_all + dram_bw_real_filter_rd_all + dram_bw_real_ofmap_rd_all + dram_bw_real_ofmap_wr_all

    sram_bw_ideal_ifmap_rd_all      =   tot_word_ifmap_rd_sram_all  * word_sz_bytes / float(2**30) / ideal_sec_all
    sram_bw_ideal_filter_rd_all     =   tot_word_filter_rd_sram_all  * word_sz_bytes / float(2**30) / ideal_sec_all
    sram_bw_ideal_ofmap_rd_all      =   tot_word_ofmap_rd_sram_all  * word_sz_bytes / float(2**30) / ideal_sec_all
    sram_bw_ideal_ofmap_wr_all      =   tot_word_ofmap_wr_sram_all  * word_sz_bytes / float(2**30) / ideal_sec_all
    sram_bw_ideal_total_all         =   sram_bw_ideal_ifmap_rd_all + sram_bw_ideal_filter_rd_all + sram_bw_ideal_ofmap_rd_all + sram_bw_ideal_ofmap_wr_all

    sram_bw_real_ifmap_rd_all       =   tot_word_ifmap_rd_sram_all  * word_sz_bytes / float(2**30) / real_sec_all
    sram_bw_real_filter_rd_all      =   tot_word_filter_rd_sram_all  * word_sz_bytes / float(2**30) / real_sec_all
    sram_bw_real_ofmap_rd_all       =   tot_word_ofmap_rd_sram_all  * word_sz_bytes / float(2**30) / real_sec_all
    sram_bw_real_ofmap_wr_all       =   tot_word_ofmap_wr_sram_all  * word_sz_bytes / float(2**30) / real_sec_all
    sram_bw_real_total_all          =   sram_bw_real_ifmap_rd_all + sram_bw_real_filter_rd_all + sram_bw_real_ofmap_rd_all + sram_bw_real_ofmap_wr_all

    bw_ideal_log +=     str(run_name) + ",\t" + "All" + ",\t" + \
                        str(dram_bw_ideal_ifmap_rd_all) + ",\t" + \
                        str(dram_bw_ideal_filter_rd_all) + ",\t" + \
                        str(dram_bw_ideal_ofmap_rd_all) + ",\t" + \
                        str(dram_bw_ideal_ofmap_wr_all) + ",\t" + \
                        str(dram_bw_ideal_total_all) + ",\t" + \
                        str(sram_bw_ideal_ifmap_rd_all) + ",\t" + \
                        str(sram_bw_ideal_filter_rd_all) + ",\t" + \
                        str(sram_bw_ideal_ofmap_rd_all) + ",\t" + \
                        str(sram_bw_ideal_ofmap_wr_all) + ",\t" + \
                        str(sram_bw_ideal_total_all) + ",\t\n"

    bw_real_log +=      str(run_name) + ",\t" + "All" + ",\t" + \
                        str(dram_bw_real_ifmap_rd_all) + ",\t" + \
                        str(dram_bw_real_filter_rd_all) + ",\t" + \
                        str(dram_bw_real_ofmap_rd_all) + ",\t" + \
                        str(dram_bw_real_ofmap_wr_all) + ",\t" + \
                        str(dram_bw_real_total_all) + ",\t" + \
                        str(sram_bw_real_ifmap_rd_all) + ",\t" + \
                        str(sram_bw_real_filter_rd_all) + ",\t" + \
                        str(sram_bw_real_ofmap_rd_all) + ",\t" + \
                        str(sram_bw_real_ofmap_wr_all) + ",\t" + \
                        str(sram_bw_real_total_all) + ",\t\n"

    ideal_throughput_all = 1 / ideal_sec_all
    tp_ideal_log +=     str(run_name) + ",\t" + "All" + ",\t" + \
                        str(ideal_cycle_all) + ",\t" + \
                        str(ideal_sec_all) + ",\t" + \
                        str(ideal_throughput_all) + ",\t\n"
    
    real_throughput_all = 1 / real_sec_all
    tp_real_log +=      str(run_name) + ",\t" + "All" + ",\t" + \
                        str(real_cycle_all) + ",\t" + \
                        str(real_sec_all) + ",\t" + \
                        str(real_throughput_all) + ",\t\n"

    detail_ideal.write(detail_ideal_log)
    detail_real.write(detail_real_log)
    bw_ideal.write(bw_ideal_log)
    bw_real.write(bw_real_log)
    tp_ideal.write(tp_ideal_log)
    tp_real.write(tp_real_log)
    hw_runtime.write(hw_runtime_log)

    detail_ideal.close()
    detail_real.close()
    bw_ideal.close()
    bw_real.close()
    tp_ideal.close()
    tp_real.close()
    hw_runtime.close()
    param_file.close()

def prune(input_list):
    l = []

    for e in input_list:
        e = e.strip() # remove the leading and trailing characters, here space
        if e != '' and e != ' ':
            l.append(e)

    return l


if __name__ == "__main__":
    profiling(run_name="example_run")