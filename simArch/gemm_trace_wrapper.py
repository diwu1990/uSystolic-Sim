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
        filter_sram_size = 64, ifmap_sram_size= 64, ofmap_sram_size = 64, # in word
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
    print("Generate SRAM   read/write trace in word...")
    # SRAM trace is in word granulatiry
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
    # dram data placement: ifmap -> filt -> ofmap
    # ifmap read dram
    print("Generate IFMAP  DRAM read  trace in word...")
    dram.dram_trace_read_v2(
        sram_sz_word=ifmap_sram_size,
        min_addr_word=ifmap_base, max_addr_word=filt_base,
        sram_trace_file=sram_read_trace_file,
        dram_trace_file=dram_ifmap_trace_file,
    )
    
    # filter read dram
    print("Generate FILTER DRAM read  trace in word...")
    dram.dram_trace_read_v2(
        sram_sz_word= filter_sram_size,
        min_addr_word=filt_base, max_addr_word=ofmap_base,
        sram_trace_file= sram_read_trace_file,
        dram_trace_file= dram_filter_trace_file,
    )

    # assume ofmap sram is large enough to hold all ofmap, so no dram read is needed here
    # ofmap write dram
    print("Generate OFMAP  DRAM write trace in word...")
    dram.dram_trace_write(
        ofmap_sram_size_word= ofmap_sram_size,
        sram_write_trace_file= sram_write_trace_file,
        dram_write_trace_file= dram_ofmap_trace_file
    )
    
    return util, sram_cycles
