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
    
    fname = net_name + "_mac_util.csv"
    cycl = open(fname, 'w')
    cycl.write("Layer,\tType,\tCycles,\t% Utilization,\n")

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
            print("Commencing trace generation for " + name + " with a MAC cycle count of " + str(mac_cycles))
            
            # all trace should be generated in granularity of word, the word size only influence the bandwidth
            util, clk = gemm_trace.gen_all_traces(array_h = array_h,
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

            util_str = str(util)
            line = name + ",\t" + layer_type + ",\t" + clk +",\t" + util_str + ",\n"
            cycl.write(line)

    cycl.close()
    param_file.close()


def prune(input_list):
    l = []

    for e in input_list:
        e = e.strip() # remove the leading and trailing characters, here space
        if e != '' and e != ' ':
            l.append(e)

    return l