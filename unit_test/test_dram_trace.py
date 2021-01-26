from simArch.dram_trace import dram_trace_read_v2, dram_trace_write

word_size_bytes = 1
ifmap_sram_size= 64
filter_sram_size = 64
ofmap_sram_size = 64
ifmap_base=0
filt_base = 1000000
ofmap_base = 2000000

sram_read_trace_file = "sram_read_ws_usystolic_opt.csv"
dram_ifmap_trace_file = "dram_ifmap_read.csv"

dram_trace_read_v2(
        sram_sz_bytes=ifmap_sram_size,
        word_sz_bytes=word_size_bytes,
        min_addr=ifmap_base, max_addr=filt_base,
        sram_trace_file=sram_read_trace_file,
        dram_trace_file=dram_ifmap_trace_file,
    )


sram_write_trace_file = "sram_write_ws_usystolic_opt.csv"
dram_ofmap_trace_file = "dram_ofmap_write.csv"

dram_trace_write(
        ofmap_sram_size_bytes= ofmap_sram_size,
        word_sz_bytes= word_size_bytes,
        sram_write_trace_file= sram_write_trace_file,
        dram_write_trace_file= dram_ofmap_trace_file
    )