import math


def prune(input_list):
    l = []

    for e in input_list:
        e = e.strip() # remove the leading and trailing characters, here space
        if e != '' and e != ' ':
            l.append(e)

    return l


def dram_trace_read_v2(
        sram_sz_word   = 512 * 1024, 
        min_addr_word = 0, max_addr_word=1000000, # in word
        default_read_bw_words = 8,               # in words, this is arbitrary
        sram_trace_file = "sram_log.csv",
        dram_trace_file = "dram_log.csv"
    ):

    """
    dram read happens for all ifmap, weight and ofmap
    double buffering should be used, but is not simulated here, thus need one read and one write port for ifmap and weight sram
    the dram access here is in burst mode
    """

    t_fill_start    = -1
    t_drain_start   = 0
    init_bw         = default_read_bw_words         # Taking an arbitrary initial bw of 4 bytes per cycle

    sram = set()

    sram_requests = open(sram_trace_file, 'r')
    dram          = open(dram_trace_file, 'w')

    for entry in sram_requests:
        elems = entry.strip().split(',')
        elems = prune(elems)
        elems = [float(x) for x in elems]
        
        clk = elems[0]

        for e in range(1, len(elems)): # each element here is a word
            # only count legal addresses
            if (elems[e] not in sram) and (elems[e] >= min_addr_word) and (elems[e] < max_addr_word):
                
                # Used up all the unique data in the SRAM?
                # len(sram) is the word count in the SRAM
                if len(sram) + 1 > sram_sz_word:
                    # once sram is full, generate all needed traces; then empty sram, and start collect the rest in a recursive manner.
                    if t_fill_start == -1:
                        t_fill_start = t_drain_start - math.ceil(len(sram) / init_bw)

                    # Generate the filling trace from time t_fill_start to t_drain_start
                    cycles_needed   = t_drain_start - t_fill_start
                    words_per_cycle = math.ceil(len(sram) / cycles_needed)

                    c = t_fill_start

                    while len(sram) > 0:
                        trace = str(c) + ", "

                        for _ in range(words_per_cycle):
                            if len(sram) > 0:
                                p = sram.pop()
                                trace += str(p) + ", "
                                
                        trace += "\n"
                        dram.write(trace)
                        c += 1

                    t_fill_start    = t_drain_start
                    t_drain_start   = clk

                # Add the new element to sram, and the content will be sorted in ascending order
                sram.add(elems[e])

    if len(sram) > 0:
        if t_fill_start == -1:
            t_fill_start = t_drain_start - math.ceil(len(sram) / init_bw)

        # Generate the filling trace from time t_fill_start to t_drain_start
        cycles_needed = t_drain_start - t_fill_start
        words_per_cycle = math.ceil(len(sram) / cycles_needed)

        c = t_fill_start
        
        while len(sram) > 0:
            trace = str(c) + ", "

            for _ in range(words_per_cycle):
                if len(sram) > 0:
                    p = sram.pop()
                    trace += str(p) + ", "

            trace += "\n"
            dram.write(trace)
            c += 1

    sram_requests.close()
    dram.close()


def dram_trace_write(ofmap_sram_size_word = 64, # total size of two buffers, filling_buf and draining_buf. Each has a read/write port.
                     default_write_bw_words = 8,                     # in words, this is arbitrary
                     sram_write_trace_file = "sram_write.csv",
                     dram_write_trace_file = "dram_write.csv"):
    """
    only for ofmap write, ifmap and weight wont be written back to DRAM
    double buffering will be used for ofmap sram, and each has a read/write port.
    the dram access here is in burst mode
    """
    traffic = open(sram_write_trace_file, 'r')
    trace_file  = open(dram_write_trace_file, 'w')

    last_clk = 0
    clk = 0

    sram_buffer = [set(), set()] # double buffering
    filling_buf     = 0
    draining_buf    = 1

    for row in traffic:
        elems = row.strip().split(',')
        elems = prune(elems)
        elems = [float(x) for x in elems]

        clk = elems[0]

        # If enough space is in the filling buffer
        # Keep filling the buffer
        if (len(sram_buffer[filling_buf]) + len(elems) - 1) < (ofmap_sram_size_word / 2):
            for i in range(1,len(elems)):
                sram_buffer[filling_buf].add(elems[i])

        # Filling buffer is full, spill the data to the other buffer
        else:
            # If there is data in the draining buffer
            # drain it
            if len(sram_buffer[draining_buf]) > 0: # after first swap, the draining buf is the previous filling buf
                delta_clks = clk - last_clk # the cycle count between two swaps
                data_per_clk = math.ceil(len(sram_buffer[draining_buf]) / delta_clks) # bandwidth between two swaps

                # Drain the data
                c = last_clk + 1
                while len(sram_buffer[draining_buf]) > 0:
                    trace = str(c) + ", "
                    c += 1
                    for _ in range(int(data_per_clk)):
                        if len(sram_buffer[draining_buf]) > 0:
                            addr = sram_buffer[draining_buf].pop()
                            trace += str(addr) + ", "

                    trace_file.write(trace + "\n")

            # Swap the ids for drain buffer and fill buffer
            tmp             = draining_buf
            draining_buf    = filling_buf
            filling_buf     = tmp

            # Set the last clk value, which is the moment to swap
            last_clk = clk

            # Fill the new data now
            for i in range(1,len(elems)):
                sram_buffer[filling_buf].add(elems[i])

    # Drain the last/final fill buffer
    reasonable_clk = clk
    if len(sram_buffer[draining_buf]) > 0:
        data_per_clk = default_write_bw_words

        # Drain the data
        c = last_clk + 1
        while len(sram_buffer[draining_buf]) > 0:
            trace = str(c) + ", "
            c += 1
            for _ in range(int(data_per_clk)):
                if len(sram_buffer[draining_buf]) > 0:
                    addr = sram_buffer[draining_buf].pop()
                    trace += str(addr) + ", "

            trace_file.write(trace + "\n")
            reasonable_clk = max(c, clk)

    if len(sram_buffer[filling_buf]) > 0:
        data_per_clk = default_write_bw_words

        # Drain the data
        c = reasonable_clk + 1
        while len(sram_buffer[filling_buf]) > 0:
            trace = str(c)+ ", "
            c += 1
            for _ in range(int(data_per_clk)):
                if len(sram_buffer[filling_buf]) > 0:
                    addr = sram_buffer[filling_buf].pop()
                    trace += str(addr) + ", "

            trace_file.write(trace + "\n")


    # All traces done
    traffic.close()
    trace_file.close()

if __name__ == "__main__":
    dram_trace_read_v2(min_addr_word=0, max_addr_word=1000000, dram_trace_file="ifmaps_dram_read.csv")
    dram_trace_read_v2(min_addr_word=1000000, max_addr_word=100000000, dram_trace_file="filter_dram_read.csv")
