import math
import warnings

"""
This module execute usystolic in a cycle accurate manner.
All traces are in word granularity.
Note that the scale-sim scheduling allows multiple filters mapped to the same column simultaneously, and reuqires multiple output ports and nonlocal connections.
The scheduling here does not allow this.
"""
def sram_traffic(
    dimension_rows=16, # row size of systolic array
    dimension_cols=16, # column size of systolic array
    ifmap_h=7, # input feature map height
    ifmap_w=7, # input feature map width
    filt_h=3, # weight height
    filt_w=3, # weight width
    num_channels=1, # input channel count
    stride_h=1, # stride in row dimension
    stride_w=1, # stride in column dimension
    num_filt=33, # filter count, also output channel count
    ofmap_base=2000000, # output feature map base addr, in word
    filt_base=1000000, # weight base addr, in word
    ifmap_base=0, # input feature map base addr, in word
    mac_cycles=1, # cycle count per mac
    wgt_bw_opt=True, # optimize the bandwidth of weight and output to match that of input
    sram_read_trace_file="sram_read.csv",
    sram_write_trace_file="sram_write.csv"
):
    
    # check if mac_cycles is power of 2; if not, raise a warning
    # this mac_cycles is 
    #     1) to scale/shift the output for unary computing. For example, 8-bit data generates length-256 bitstreams, and a mac_cycles of 32 will early terminate the computing, and the output will be shifted by 3 bits.
    #     2) not used for binary computing. For example, a mac_cycles of 1 is usually used for bit-parallel binary computing, regardless of the bitwidth; a mac_cycles of N is used for N-bit bit-serial binary computing.
    # for simulation here, this value affects the throughput/bandwidth
    log2_mac_cycles = math.log2(mac_cycles)
    if log2_mac_cycles == math.ceil(log2_mac_cycles) and log2_mac_cycles == math.floor(log2_mac_cycles):
        pass
    else:
        warnings.warn("The cycle count for MAC in systolic array is not power of 2.")
    
    # input is streamed in from top; output is streamed out from top; weight is streamed in from left
    max_i_bw = math.floor(dimension_rows / mac_cycles)
    max_o_bw = math.floor(dimension_cols / mac_cycles)
    if wgt_bw_opt is True:
        # consider bound the input/output bandwidth to the weight bandwidth
        max_w_bw = int(min(math.ceil((dimension_rows + dimension_cols)/mac_cycles), dimension_cols))
    else:
        # consider no stalls in all data transfer, i.e., no optimization to the SRAM bandwidth.
        max_w_bw = dimension_cols
        
    # Dimensions of output feature map channel
    ofmap_h = math.floor((ifmap_h - filt_h + stride_h) / stride_h)
    ofmap_w = math.floor((ifmap_w - filt_w + stride_w) / stride_w)

    # Number of pixels in one convolution window
    filt_sz = filt_h * filt_w * num_channels

    # total number of ofmap px per channel
    ofmap_px_filt  = ofmap_h * ofmap_w
    
    # Variables to calculate folds in runtime
    # mapping multiple filters to one column at the same time is forbidden to avoid multiple output ports.
    # mapping count of a single filter onto a column
    col_fold = 1
    if dimension_rows < filt_sz:
        col_fold = math.ceil(filt_sz / dimension_rows)
    
    # mapping count of all filters onto the entire array, at the granularity of filter
    # filters and columns follow 1-to-1 mapping
    arr_fold = 1
    arr_fold = math.ceil(num_filt / dimension_cols)
    
    # Variables for utilization calculation
    util = 0
    compute_cycles = 0
    
    remaining_filt = num_filt
    cycles = 0
    prev_cycl = 0

    # These are the starting addresses of filter weights in the memory
    # weight memory format: FHWC
    all_filt_addr_list = []
    for f in range(num_filt):
        addr = f * filt_sz + filt_base
        all_filt_addr_list.append(addr)

    for v in range(int(arr_fold)):
        # Take a slice of the starting addresses that are relevant for this arr_fold 
        filt_this_fold = min(remaining_filt, dimension_cols)
        idx_start = v * dimension_cols
        idx_end = idx_start + filt_this_fold
        # list of filter addrs for current arr_fold
        filt_addr_list = all_filt_addr_list[idx_start:idx_end]

        rem_wgt_filt = filt_sz # Tracks the elements processed within a conv filter
        
        for h in range(col_fold): # col_fold >= 1
            rows_this_fold = min(rem_wgt_filt, dimension_rows)

            # Values returned
            # cycles -> Cycle count for the next operation
            # filt_addr_list -> The starting filter address for the next iteration
            cycles, filt_addr_list  = gen_trace_filter_fold(
                                        col_addrs = filt_addr_list,
                                        cycle = cycles,
                                        num_rows = dimension_rows, 
                                        num_cols = dimension_cols,
                                        act_rows = rows_this_fold,
                                        act_cols = filt_this_fold,
                                        bandwidth = max_w_bw,
                                        sram_read_trace_file = sram_read_trace_file
                                        )
            # generate ifmap and ofmap traces simultaneously
            cycles = gen_trace_ifmap_ofmap_fold(
                                        cycle = cycles,
                                        num_rows = dimension_rows,
                                        num_cols = dimension_cols,
                                        act_rows= rows_this_fold,
                                        act_cols = filt_this_fold,
                                        remaining = rem_wgt_filt,
                                        filt_sz = filt_sz,
                                        ifmap_h = ifmap_h,
                                        ifmap_w = ifmap_w,
                                        filt_h = filt_h, 
                                        filt_w = filt_w,
                                        num_channels = num_channels,
                                        num_filters = num_filt,
                                        stride_h = stride_h,
                                        stride_w = stride_w,
                                        ofmap_h = ofmap_h,
                                        ofmap_w = ofmap_w,
                                        ofmap_px_filt = int(ofmap_px_filt),
                                        ifmap_base = ifmap_base,
                                        ofmap_base = ofmap_base,
                                        filters_done = (v * dimension_cols),
                                        mac_cycles = mac_cycles,
                                        sram_read_trace_file = sram_read_trace_file,
                                        sram_write_trace_file = sram_write_trace_file
                                        )
            
            # ratio of used macs to total
            util_this_fold = (rows_this_fold * filt_this_fold) /(dimension_rows * dimension_cols)

            rem_wgt_filt -= rows_this_fold

            fold_cycl = cycles - prev_cycl
            util += util_this_fold *  fold_cycl
            compute_cycles += fold_cycl
            prev_cycl = cycles
            
        remaining_filt -= filt_this_fold

    final = str(cycles)
    final_util = (util / compute_cycles) * 100
    return (final, final_util)


def gen_trace_filter_fold(
    col_addrs=[], # the element count indicates columns to use
    cycle=0, # the start cycle
    num_rows=4, # total number of rows
    num_cols = 4, # total number of cols
    act_rows=4, # used rows, always counted from top
    act_cols=4, # used col, always counted from left
    bandwidth=4, # max io bandwidth at top
    sram_read_trace_file="sram_read.csv"
):
    """
    apply FHWC format, low indexed weights are streamed first
    """
    outfile = open(sram_read_trace_file, 'a')
    assert act_cols == len(col_addrs), "Mismatch between active columns and their addresses."

    # output formatting: Add empty commas for row addresses as no element is fed from the left
    prefix = ""
    for r in range(num_rows):
        prefix += ", "
    
    for r in range(act_rows):
        cur_col = 0
        while cur_col < act_cols:
            entry = str(cycle) + ", " + prefix
            for c in range(0, cur_col): # fill empty cols
                entry += ", "

            for c in range(bandwidth):
                if cur_col < act_cols:
                    entry += str(col_addrs[cur_col]) + ", "
                    col_addrs[cur_col] += 1
                    cur_col += 1

            for c in range(cur_col, num_cols): # fill empty cols
                entry += ", "

            cycle += 1
            entry += "\n"
            outfile.write(entry)

    outfile.close()

    return cycle, col_addrs


def gen_trace_ifmap_ofmap_fold(
    cycle = 0,
    num_rows = 4,
    num_cols = 4,
    act_rows= 4,
    act_cols = 4,
    remaining = 4,
    filt_sz = 4,
    ifmap_h = 4,
    ifmap_w = 4,
    filt_h = 3,
    filt_w = 3,
    stride_h = 1,
    stride_w = 1,
    ofmap_h = 4,
    ofmap_w = 4,
    ofmap_px_filt = 16,
    num_channels = 3,
    num_filters = 8,
    ifmap_base = 0,
    ofmap_base = 2000000,
    filters_done = 0,
    mac_cycles = 1,
    sram_read_trace_file = "sram_read.csv",
    sram_write_trace_file = "sram_write.csv"
):
    """
    apply HWC format to both ifmap and ofmap
    """
    print(mac_cycles)
    rd_file = open(sram_read_trace_file, 'a')
    wr_file = open(sram_write_trace_file,'a')
    
    assert filters_done < num_filters, "Incorrect count of remaining filters."
    
    wc_filt = filt_w * num_channels
    wc_ifmap = ifmap_w * num_channels
    
    postfix = ""
    for c in range(num_cols):
        postfix += ", "
    
    cur_cycle = 0
    tot_cycle = ofmap_px_filt * mac_cycles + act_cols + act_rows # cycles for all ofmap of this col fold is done, assume no stall in the mac array.
    px_cycle  = mac_cycles + act_cols + act_rows # cycles for computing an ofmap element
    
    # ofmap memory stack
    ofmap_addr_offset  = filters_done
    ofmap_bot_addr = ofmap_addr_offset + ofmap_base
    ofmap_top_addr = (ofmap_px_filt - 1) * num_filters + act_cols + ofmap_bot_addr
    
    # ifmap memory stack
    # initial ifmap index
    wc_ifmap = ifmap_w * num_channels
    wc_filt = filt_w * num_channels
    
    ifmap_px_idx_init = (filt_sz - remaining)
    ifmap_h_idx_init = math.floor(ifmap_px_idx_init / wc_filt)
    ifmap_w_idx_init = math.floor((ifmap_px_idx_init % wc_filt) / num_channels)
    ifmap_c_idx_init = ifmap_px_idx_init % num_channels
    ifmap_bot_addr = ifmap_base + ifmap_h_idx_init * ifmap_w * num_channels + ifmap_w_idx_init * num_channels + ifmap_c_idx_init
    
    if remaining == act_rows:
        ifmap_top_addr = ifmap_base + ifmap_h * ifmap_w * num_channels
    else:
        ifmap_h_used_init = (ofmap_h - 1) * stride_h
        ifmap_w_used_init = (ofmap_w - 1) * stride_w
        ifmap_px_idx_init_next_fold = filt_sz - (remaining - act_rows)
        ifmap_h_idx_init_next_fold = math.floor(ifmap_px_idx_init_next_fold / wc_filt)
        ifmap_w_idx_init_next_fold = math.floor((ifmap_px_idx_init_next_fold % wc_filt) / num_channels)
        ifmap_c_idx_init_next_fold = ifmap_px_idx_init_next_fold % num_channels
        ifmap_top_addr = ifmap_base + (ifmap_h_used_init + ifmap_h_idx_init_next_fold) * ifmap_w * num_channels + (ifmap_w_used_init + ifmap_w_idx_init_next_fold) * num_channels + ifmap_c_idx_init_next_fold
    
    while cur_cycle < tot_cycle:
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # ifmap read
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        """
        top rows are printed first, but bottom rows are first streamed in
        """
        rd_entry = ""
        rd_en = False
        
        ofmap_px_row = math.floor(cur_cycle / mac_cycles) # index of ofmap px in process
        ofmap_px_cycle_row = cur_cycle % mac_cycles # index of current process
    
        for r in range(num_rows - 1, -1, -1): # smaller indexes represent top rows
            reverse_row = (act_rows - r - 1) # rows with smaller weight indexes, i.e., larger row indexes, are filled first.
            if (r < act_rows) and (reverse_row % mac_cycles == ofmap_px_cycle_row % mac_cycles): # ifmap read
                # get the h and w indexes of the ofmap px for this row/conv window
                ofmap_h_idx = math.floor(ofmap_px_row / ofmap_w)
                ofmap_w_idx = ofmap_px_row % ofmap_w
                ofmap_legal = ofmap_h_idx >= 0 and ofmap_h_idx < ofmap_h and ofmap_w_idx >= 0 and ofmap_w_idx < ofmap_w
                # get the h and w indexes of first ifmap px for this row/conv window
                ifmap_h_idx_init = ofmap_h_idx * stride_h
                ifmap_w_idx_init = ofmap_w_idx * stride_w
                # the relative index of the px in the conv window
                ifmap_px_idx_relative = ifmap_px_idx_init + reverse_row
                # get the absolute h, w and c indexes of current ifmap px for this row/conv window
                ifmap_h_idx = math.floor(ifmap_px_idx_relative / wc_filt) + ifmap_h_idx_init
                ifmap_w_idx = math.floor((ifmap_px_idx_relative % wc_filt) / num_channels) + ifmap_w_idx_init
                ifmap_c_idx = ifmap_px_idx_relative % num_channels

                ifmap_addr = ifmap_h_idx * wc_ifmap + ifmap_w_idx * num_channels + ifmap_c_idx
                
                if ifmap_addr >= ifmap_bot_addr and ifmap_addr < ifmap_top_addr and ofmap_legal:
                    rd_en = True
                    rd_entry = str(ifmap_addr) + ", " + rd_entry
                else:
                    rd_entry = ", " + rd_entry

                ofmap_px_row -= 1
            else:
                rd_entry = ", " + rd_entry
        
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        # ofmap read, predict whether next cycle there exists output to be written to SRAM
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        rd_en_ofmap = False
        rd_ofmap_latency = 1
        rd_entry_ext, rd_en_ofmap = check_ofmap(
                                update = rd_en_ofmap,
                                entry = "",
                                cur_cycle = cur_cycle + rd_ofmap_latency,
                                num_cols = num_cols,
                                act_cols = act_cols,
                                act_rows = act_rows,
                                mac_cycles = mac_cycles,
                                num_filters = num_filters,
                                ofmap_bot_addr = ofmap_bot_addr,
                                ofmap_top_addr = ofmap_top_addr
                            )
        
        # ofmap write
        wr_en = rd_en_ofmap
        wr_entry = str(cycle + rd_ofmap_latency) + ", " + rd_entry_ext
        
        if remaining == filt_sz:
            # no need to read from memory if first time getting the partial sum
            rd_en_ofmap = False
            rd_entry += postfix
        else:
            rd_entry += rd_entry_ext
        
        rd_entry += "\n"
        if rd_en is True or rd_en_ofmap is True:
            rd_entry = str(cycle) + ", " + rd_entry
            rd_file.write(rd_entry)

        wr_entry += "\n"
        if wr_en is True:
            wr_file.write(wr_entry)
        
        cur_cycle += 1
        cycle += 1
        
    rd_file.close()
    wr_file.close()
    return cycle


def check_ofmap(
    update = False,
    entry = None,
    cur_cycle = 0,
    num_cols = 0,
    act_cols = 0,
    act_rows = 0,
    mac_cycles = 0,
    num_filters = 0,
    ofmap_bot_addr = 0,
    ofmap_top_addr = 0
):
    """
    update means there is at least one valid output at this cycle
    left ofmap at each row is generated first
    """
    ofmap_cycle_col = (cur_cycle - act_rows - mac_cycles)
    ofmap_px_col = math.floor(ofmap_cycle_col / mac_cycles)
    ofmap_px_cycle_col = ofmap_cycle_col % mac_cycles
    ofmap_base_addr = ofmap_px_col * num_filters + ofmap_bot_addr

    for c in range(num_cols):
        if (c < act_cols) and (c % mac_cycles == ofmap_px_cycle_col % mac_cycles):
            ofmap_addr = ofmap_base_addr + c
            if ofmap_addr >= ofmap_bot_addr and ofmap_addr < ofmap_top_addr:
                update = True
                entry += str(ofmap_addr) + ", "
            else:
                entry += ", "
            ofmap_base_addr -= num_filters
        else:
            entry += ", "
            
    return entry, update

