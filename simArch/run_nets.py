import simArch.gemm_trace_wrapper as gemm_trace

def run_net(
    ifmap_sram_size=1, # in K-Word
    filter_sram_size=1, # in K-Word
    ofmap_sram_size=1, # in K-Word
    array_h=32,
    array_w=32,
    data_flow='ws',
    word_size_bytes=1,
    wgt_bw_opt=False,
    topology_file=None,
    net_name=None,
    offset_list = [0, 10000000, 20000000] # in word
):

    ifmap_sram_size *= 1024 # in word
    filter_sram_size *= 1024 # in word
    ofmap_sram_size *= 1024 # in word

    param_file = open(topology_file, 'r')
    
    # fname = net_name + "_avg_bw.csv"
    # bw = open(fname, 'w')

    # f2name = net_name + "_max_bw.csv"
    # maxbw = open(f2name, 'w')

    f3name = net_name + "_mac_util.csv"
    cycl = open(f3name, 'w')

    # f4name = net_name + "_detail.csv"
    # detail = open(f4name, 'w')

    # bw.write("IFMAP SRAM Size (Bytes),\tFilter SRAM Size (Bytes),\tOFMAP SRAM Size (Bytes),\tLayer,\tDRAM IFMAP Read BW (Bytes/cycle),\tDRAM Filter Read BW (Bytes/cycle),\tDRAM OFMAP Write BW (Bytes/cycle),\tSRAM Read BW (Bytes/cycle),\tSRAM OFMAP Write BW (Bytes/cycle), \n")
    # maxbw.write("IFMAP SRAM Size (Bytes),\tFilter SRAM Size (Bytes),\tOFMAP SRAM Size (Bytes),\tLayer,\tMax DRAM IFMAP Read BW (Bytes/cycle),\tMax DRAM Filter Read BW (Bytes/cycle),\tMax DRAM OFMAP Write BW (Bytes/cycle),\tMax SRAM Read BW (Bytes/cycle),\tMax SRAM OFMAP Write BW (Bytes/cycle),\n")
    cycl.write("Layer,\tType,\tCycles,\t% Utilization,\n")
    # detailed_log = "Layer,\tType\t," +\
    #              "\tDRAM_IFMAP_start,\tDRAM_IFMAP_stop,\tDRAM_IFMAP_bytes," + \
    #              "\tDRAM_Filter_start,\tDRAM_Filter_stop,\tDRAM_Filter_bytes," + \
    #              "\tDRAM_OFMAP_start,\tDRAM_OFMAP_stop,\tDRAM_OFMAP_bytes," + \
    #              "\tSRAM_read_start,\tSRAM_read_stop,\tSRAM_read_bytes," +\
    #              "\tSRAM_write_start,\tSRAM_write_stop,\tSRAM_write_bytes,\n"

    # detail.write(detailed_log)

    first = True
    for row in param_file:
        # per layer trace gen
        if first:
            # skip the header row
            first = False
            continue
            
        elems = row.strip().split(',')
        elems = prune(elems)

        # skip row if unrecognized
        if len(elems) != 11:
            continue

        name = elems[0].strip()
        layer_type = elems[1].strip()

        if layer_type == "GEMM":
            ifmap_h = int(elems[2].strip())
            ifmap_w = int(elems[3].strip())

            filt_h = int(elems[4].strip())
            filt_w = int(elems[5].strip())

            num_channels = int(elems[6].strip())
            num_filters = int(elems[7].strip())

            stride_h = int(elems[8].strip())
            stride_w = int(elems[9].strip())
            mac_cycles = int(elems[10].strip())
            
            ifmap_base  = offset_list[0] # in word
            filter_base = offset_list[1] # in word
            ofmap_base  = offset_list[2] # in word

            print("")
            print("Commencing run for " + name + " with a MAC cycle count " + str(mac_cycles))
            
            # bw_log = str(ifmap_sram_size * word_size_bytes) +",\t" + str(filter_sram_size * word_size_bytes) + ",\t" + str(ofmap_sram_size * word_size_bytes) + ",\t" + name + ",\t"
            # max_bw_log = bw_log
            # detailed_log = name + ",\t"

            # all trace should be generated in granularity of word, the word size only influence the bandwidth
            # bw_str, detailed_str, util, clk =  \
            util, clk = gemm_trace.gen_all_traces(  array_h = array_h,
                                    array_w = array_w,
                                    ifmap_h = ifmap_h,
                                    ifmap_w = ifmap_w,
                                    filt_h = filt_h,
                                    filt_w = filt_w,
                                    num_channels = num_channels,
                                    num_filt = num_filters,
                                    stride_h = stride_h,
                                    stride_w = stride_w,
                                    data_flow = data_flow,
                                    word_size_bytes = word_size_bytes,
                                    filter_sram_size = filter_sram_size, # in word
                                    ifmap_sram_size = ifmap_sram_size, # in word
                                    ofmap_sram_size = ofmap_sram_size, # in word
                                    filt_base = filter_base, # in word granularity
                                    ifmap_base = ifmap_base, # in word granularity
                                    ofmap_base = ofmap_base, # in word granularity
                                    mac_cycles = mac_cycles,
                                    wgt_bw_opt = wgt_bw_opt,
                                    sram_read_trace_file= net_name + "_" + name + "_sram_read.csv",
                                    sram_write_trace_file= net_name + "_" + name + "_sram_write.csv",
                                    dram_filter_trace_file=net_name + "_" + name + "_dram_filter_read.csv",
                                    dram_ifmap_trace_file= net_name + "_" + name + "_dram_ifmap_read.csv",
                                    dram_ofmap_trace_file= net_name + "_" + name + "_dram_ofmap_write.csv"
                                )
            print("All done for " + name)

    #         bw_log += bw_str
    #         bw.write(bw_log + "\n")

    #         detailed_log += detailed_str
    #         detail.write(detailed_log + "\n")
            
    #         print("Analyze maximum statistics in byte...")
    #         max_bw_log += gemm_trace.gen_max_bw_numbers(
    #                                 sram_read_trace_file = net_name + "_" + name + "_sram_read.csv",
    #                                 sram_write_trace_file= net_name + "_" + name + "_sram_write.csv",
    #                                 dram_filter_trace_file=net_name + "_" + name + "_dram_filter_read.csv",
    #                                 dram_ifmap_trace_file= net_name + "_" + name + "_dram_ifmap_read.csv",
    #                                 dram_ofmap_trace_file= net_name + "_" + name + "_dram_ofmap_write.csv",
    #                                 word_size_bytes= word_size_bytes
    #                                 )
    #         print("All done...")
    #         maxbw.write(max_bw_log + "\n")

            util_str = str(util)
            line = name + ",\t" + layer_type + ",\t" + clk +",\t" + util_str + ",\n"
            cycl.write(line)

    # bw.close()
    # maxbw.close()
    # cycl.close()
    # detail.close()
    # param_file.close()


def prune(input_list):
    l = []

    for e in input_list:
        e = e.strip() # remove the leading and trailing characters, here space
        if e != '' and e != ' ':
            l.append(e)

    return l