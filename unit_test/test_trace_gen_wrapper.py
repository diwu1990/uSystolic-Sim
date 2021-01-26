from simArch.trace_gen_wrapper import gen_all_traces
import glob, os

def run(
    word_size_bytes = 1,
    sram_size = 64,
    mac_cycles = 1,
    wgt_bw_opt = False
):
    prefix = str(word_size_bytes) + "_" + str(sram_size) + "_" + str(mac_cycles) + "_"
    reg = prefix + "*.csv"
    for f in glob.glob(reg):
        os.remove(f)
    gen_all_traces(
            array_h = 8,
            array_w = 8,
            ifmap_h = 7, ifmap_w = 7,
            filt_h  = 3, filt_w = 3,
            num_channels = 3,
            stride_h = 1, stride_w = 1, num_filt = 8,
            word_size_bytes = word_size_bytes,
            filter_sram_size = sram_size, ifmap_sram_size= sram_size, ofmap_sram_size = sram_size,
            mac_cycles=mac_cycles, wgt_bw_opt=wgt_bw_opt,
            sram_read_trace_file = prefix + "sram_read.csv", sram_write_trace_file = prefix + "sram_write.csv",
            dram_filter_trace_file = prefix + "dram_filter_read.csv", dram_ifmap_trace_file = prefix + "dram_ifmap_read.csv", dram_ofmap_trace_file = prefix + "dram_ofmap_write.csv"
            )


run(word_size_bytes = 1, sram_size = 16, mac_cycles = 1, wgt_bw_opt = False)
run(word_size_bytes = 1, sram_size = 16, mac_cycles = 256, wgt_bw_opt = False)
run(word_size_bytes = 1, sram_size = 32, mac_cycles = 1, wgt_bw_opt = False)
run(word_size_bytes = 0.5, sram_size = 16, mac_cycles = 1, wgt_bw_opt = False)
run(word_size_bytes = 1, sram_size = 32, mac_cycles = 256, wgt_bw_opt = False)
run(word_size_bytes = 0.5, sram_size = 16, mac_cycles = 256, wgt_bw_opt = False)