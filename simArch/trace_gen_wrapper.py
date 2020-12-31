import math
import simArch.dram_trace as dram
import simArch.sram_traffic_ws_usystolic as sram_traffic_ws_usystolic

def gen_all_traces(
        array_h = 4,
        array_w = 4,
        ifmap_h = 7, ifmap_w = 7,
        filt_h  = 3, filt_w = 3,
        num_channels = 3,
        stride_h = 1,
        stride_w = 1,
        num_filt = 8,

        data_flow = "ws",

        word_size_bytes = 1,
        filter_sram_size = 64, ifmap_sram_size= 64, ofmap_sram_size = 64, # all with a unit of byte

        filt_base = 1000000, ifmap_base=0, ofmap_base = 2000000, # in word granularity
        mac_cycles=2, # extended input, indicating the cycle count for one mac operation
        wgt_bw_opt=False, # extended input, indicating the weight loading bw is bounded by the read bw during calculation
        
        sram_read_trace_file = "sram_read.csv",
        sram_write_trace_file = "sram_write.csv",

        dram_filter_trace_file = "dram_filter_read.csv",
        dram_ifmap_trace_file = "dram_ifmap_read.csv",
        dram_ofmap_trace_file = "dram_ofmap_write.csv"
    ):

    sram_cycles = 0
    util        = 0
    
    assert data_flow == "ws", "Dataflow other than weight stationary is not supported in uSystolic simulator."
    print("Generate SRAM read/write trace...")
    sram_cycles, util = sram_traffic_ws_usystolic.sram_traffic(
                                                            dimension_rows = array_h,
                                                            dimension_cols = array_w,
                                                            ifmap_h = ifmap_h, ifmap_w = ifmap_w,
                                                            filt_h = filt_h, filt_w = filt_w,
                                                            num_channels = num_channels,
                                                            stride_h = stride_h, stride_w = stride_w, num_filt = num_filt,
                                                            ofmap_base = ofmap_base, filt_base = filt_base, ifmap_base = ifmap_base,
                                                            mac_cycles=mac_cycles,
                                                            wgt_bw_opt=wgt_bw_opt,
                                                            sram_read_trace_file = sram_read_trace_file,
                                                            sram_write_trace_file = sram_write_trace_file
                                                        )
    print("Done...")
    print("Average utilization : \t"  + str(util) + " %")
    print("Cycles for compute  : \t"  + str(sram_cycles) + " cycles")
    # dram data placement: ifmap -> filt -> ofmap
    # ifmap read dram
    print("Generate IFMAP DRAM read trace...")
    dram.dram_trace_read_v2(
        sram_sz_bytes=ifmap_sram_size,
        word_sz_bytes=word_size_bytes,
        min_addr=ifmap_base, max_addr=filt_base,
        sram_trace_file=sram_read_trace_file,
        dram_trace_file=dram_ifmap_trace_file,
    )
    print("Done...")
    
    # filter read dram
    print("Generate FILTER DRAM read trace...")
    dram.dram_trace_read_v2(
        sram_sz_bytes= filter_sram_size,
        word_sz_bytes= word_size_bytes,
        min_addr=filt_base, max_addr=ofmap_base,
        sram_trace_file= sram_read_trace_file,
        dram_trace_file= dram_filter_trace_file,
    )
    print("Done...")

    # ofmap write dram
    print("Generate OFMAP DRAM write trace...")
    dram.dram_trace_write(
        ofmap_sram_size_bytes= ofmap_sram_size,
        word_sz_bytes= word_size_bytes,
        sram_write_trace_file= sram_write_trace_file,
        dram_write_trace_file= dram_ofmap_trace_file
    )
    print("Done...")

    print("Analyze average statistics...")
    bw_numbers, detailed_log  = gen_bw_numbers(
                                            dram_ifmap_trace_file,
                                            dram_filter_trace_file,
                                            dram_ofmap_trace_file,
                                            sram_write_trace_file,
                                            sram_read_trace_file,
                                            word_size_bytes
                                            )
    print("Done...")
    
    return bw_numbers, detailed_log, util, sram_cycles


def gen_max_bw_numbers(
    dram_ifmap_trace_file, 
    dram_filter_trace_file,
    dram_ofmap_trace_file, 
    sram_write_trace_file, 
    sram_read_trace_file,
    word_size_bytes
):

    max_dram_ifmap_bw_in_words = 0 # max words per cycle
    num_words = 0
    max_dram_act_clk = ""
    f = open(dram_ifmap_trace_file, 'r')

    for row in f:
        clk = row.split(',')[0]
        num_words = len(row.split(',')) - 2
        
        if max_dram_ifmap_bw_in_words < num_words:
            max_dram_ifmap_bw_in_words = num_words
            max_dram_act_clk = clk
    f.close()

    max_dram_filter_bw_in_words = 0 # max words per cycle
    num_words = 0
    max_dram_filt_clk = ""
    f = open(dram_filter_trace_file, 'r')

    for row in f:
        clk = row.split(',')[0]
        num_words = len(row.split(',')) - 2

        if max_dram_filter_bw_in_words < num_words:
            max_dram_filter_bw_in_words = num_words
            max_dram_filt_clk = clk
    f.close()

    max_dram_ofmap_bw_in_words = 0 # max words per cycle
    num_words = 0
    max_dram_ofmap_clk = ""
    f = open(dram_ofmap_trace_file, 'r')

    for row in f:
        clk = row.split(',')[0]
        num_words = len(row.split(',')) - 2

        if max_dram_ofmap_bw_in_words < num_words:
            max_dram_ofmap_bw_in_words = num_words
            max_dram_ofmap_clk = clk
    f.close()
    
    max_sram_ofmap_bw_in_words = 0 # max words per cycle
    num_words = 0
    f = open(sram_write_trace_file, 'r')

    for row in f:
        elems = row.strip().split(',')
        num_words = parse_sram_read_data(elems[1:])

        if max_sram_ofmap_bw_in_words < num_words:
            max_sram_ofmap_bw_in_words = num_words
    f.close()

    max_sram_read_bw_in_words = 0 # max words per cycle
    num_words = 0
    f = open(sram_read_trace_file, 'r')

    for row in f:
        elems = row.strip().split(',')
        num_words = parse_sram_read_data(elems[1:])
        
        if max_sram_read_bw_in_words < num_words:
            max_sram_read_bw_in_words = num_words
    f.close()

    log  = str(max_dram_ifmap_bw_in_words * word_size_bytes) + ",\t" + str(max_dram_filter_bw_in_words * word_size_bytes) + ",\t" 
    log += str(max_dram_ofmap_bw_in_words * word_size_bytes) + ",\t" + str(max_sram_read_bw_in_words * word_size_bytes) + ",\t"
    log += str(max_sram_ofmap_bw_in_words * word_size_bytes)  + ","
    return log


def gen_bw_numbers(
    dram_ifmap_trace_file,
    dram_filter_trace_file,
    dram_ofmap_trace_file,
    sram_write_trace_file,
    sram_read_trace_file,
    word_size_bytes
):

    min_clk = 100000
    max_clk = -1
    detailed_log = ""

    num_dram_ifmap_words = 0
    f = open(dram_ifmap_trace_file, 'r')
    start_clk = 0
    first = True

    for row in f:
        num_dram_ifmap_words += len(row.split(',')) - 2
        
        elems = row.strip().split(',')
        clk = float(elems[0])

        if first:
            first = False
            start_clk = clk

        if clk < min_clk:
            min_clk = clk

    stop_clk = clk
    detailed_log += str(start_clk) + ",\t" + str(stop_clk) + ",\t" + str(num_dram_ifmap_words) + ",\t"
    f.close()

    num_dram_filter_words = 0
    f = open(dram_filter_trace_file, 'r')
    first = True

    for row in f:
        num_dram_filter_words += len(row.split(',')) - 2

        elems = row.strip().split(',')
        clk = float(elems[0])

        if first:
            first = False
            start_clk = clk

        if clk < min_clk:
            min_clk = clk

    stop_clk = clk
    detailed_log += str(start_clk) + ",\t" + str(stop_clk) + ",\t" + str(num_dram_filter_words) + ",\t"
    f.close()

    num_dram_ofmap_words = 0
    f = open(dram_ofmap_trace_file, 'r')
    first = True

    for row in f:
        num_dram_ofmap_words += len(row.split(',')) - 2

        elems = row.strip().split(',')
        clk = float(elems[0])

        if first:
            first = False
            start_clk = clk

    stop_clk = clk
    detailed_log += str(start_clk) + ",\t" + str(stop_clk) + ",\t" + str(num_dram_ofmap_words) + ",\t"
    f.close()
    if clk > max_clk:
        max_clk = clk
    
    num_sram_ofmap_words = 0
    f = open(sram_write_trace_file, 'r')
    first = True

    for row in f:
        elems = row.strip().split(',')
        clk = float(elems[0])

        if first:
            first = False
            start_clk = clk
        
        valid_words = parse_sram_read_data(elems[1:])
        num_sram_ofmap_words += valid_words

    stop_clk = clk
    detailed_log += str(start_clk) + ",\t" + str(stop_clk) + ",\t" + str(num_sram_ofmap_words) + ",\t"
    f.close()
    if clk > max_clk:
        max_clk = clk
    
    num_sram_read_words = 0
    f = open(sram_read_trace_file, 'r')
    first = True

    for row in f:
        elems = row.strip().split(',')
        clk = float(elems[0])

        if first:
            first = False
            start_clk = clk

        valid_words = parse_sram_read_data(elems[1:])
        num_sram_read_words += valid_words

    stop_clk = clk
    detailed_log += str(start_clk) + ",\t" + str(stop_clk) + ",\t" + str(num_sram_read_words) + ",\t"
    f.close()
    sram_clk = clk
    if clk > max_clk:
        max_clk = clk

    delta_clk = max_clk - min_clk

    dram_ifmap_bw       = num_dram_ifmap_words / delta_clk * word_size_bytes
    dram_filter_bw      = num_dram_filter_words / delta_clk * word_size_bytes
    dram_ofmap_bw       = num_dram_ofmap_words / delta_clk * word_size_bytes
    sram_ofmap_bw       = num_sram_ofmap_words / delta_clk * word_size_bytes
    sram_read_bw        = num_sram_read_words / delta_clk * word_size_bytes
    
    units = " Bytes/cycle"
    print("DRAM IFMAP Read BW  : \t" + str(dram_ifmap_bw) + units)
    print("DRAM Filter Read BW : \t" + str(dram_filter_bw) + units)
    print("DRAM OFMAP Write BW : \t" + str(dram_ofmap_bw) + units)
    
    log = str(dram_ifmap_bw) + ",\t" + str(dram_filter_bw) + ",\t" + str(dram_ofmap_bw) + ",\t" + str(sram_read_bw) + ",\t" + str(sram_ofmap_bw) + ","
    return log, detailed_log


def parse_sram_read_data(elems):
    """
    to remove empty commas
    """
    data = 0
    for i in range(len(elems)):
        e = elems[i]
        if e != ' ':
            data += 1
    return data

