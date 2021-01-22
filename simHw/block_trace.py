import math

def sram_profiling(
    trace_file=None,
    word_sz_bytes=4,    # word size in bytes
    block_sz_bytes=16,  # in byte for bank row
    bank=8,
    min_addr_word=0,
    max_addr_word=100000,
    access_buf=True
):
    """
    this code takes non-stalling sram trace and reorganizes the trace to meet the bandwidth requirement.
    currently, it does not generate new trace, which can be improved later.
    """
    # list of output
    tot_word = 0            # total number of output word
    max_word = 0            # max number of output word
    tot_access = 0          # total number of sram block access
    max_access = 0          # max number of sram block access
    act_cycles = 0          # active sram access time
    stall_cycles = 0        # extra cycles to access data, during which the computing can be stalled
    ideal_start_cycle = 0   # start cycle of the original trace
    ideal_end_cycle = 0     # end cycle of the original trace

    block_sz_word = block_sz_bytes / word_sz_bytes

    requests = open(trace_file, 'r')

    # index list of bank and row for each access
    row_bank_list_new = []

    first = True

    for entry in requests:
        elems = entry.strip().split(',')
        elems = prune(elems)
        elems = [float(x) for x in elems]
        valid_word = 0

        if first == True:
            first = False
            ideal_start_cycle = elems[0]
        
        ideal_end_cycle = elems[0]
        row_bank_list_old = row_bank_list_new
        row_bank_list_new = []

        # memory row index and bank index generation
        for e in range(1, len(elems)): # each element here is a word
            # only count legal address
            if (elems[e] >= min_addr_word) and (elems[e] < max_addr_word):
                row_idx = int(math.floor((elems[e] - min_addr_word) / (block_sz_word * bank)))
                # cache banking, LSB of index bits
                bank_idx = int(math.floor((elems[e] - min_addr_word) / block_sz_word) % bank)
                # sram banking, LSB
                # bank_idx = int(math.floor((elems[e] - min_addr_word))) % bank
                row_bank_list_new.append((row_idx, bank_idx))
                valid_word += 1

        tot_word += valid_word
        if max_word < valid_word:
            max_word = valid_word

        # merge access if they have identical bank and row index: the actual access to different blocks
        row_bank_list_new = list(set(row_bank_list_new))

        # distinct sram access
        new_access = 0
        if access_buf == True:
            # only different blocks are accessed, old accesses are buffered already and required no access
            # this will cause extra hardware overhead, which is not modelled in this simulator
            for a in range(len(row_bank_list_new)):
                if row_bank_list_new[a] not in row_bank_list_old:
                    new_access += 1
        else:
            new_access = len(row_bank_list_new)
        
        # max number of accesses to the same bank, but different row, which results in bank conflict
        max_bank_conflict = 0
        for a in range(len(row_bank_list_new)):
            diff_row_bank_list = [(x - row_bank_list_new[a][0], y - row_bank_list_new[a][1]) for (x, y) in row_bank_list_new]

            bank_conflict = 0
            for b in range(a+1, len(row_bank_list_new)):
                if diff_row_bank_list[b][0] != 0 and diff_row_bank_list[b][1] == 0:
                    # two accesses are to the same bank, but different rows.
                    # each conflict increases the sram stall by 1.
                    bank_conflict += 1
            
            if max_bank_conflict < bank_conflict:
                max_bank_conflict = bank_conflict

        tot_access += new_access
        # max parallel sram block access
        if max_access < new_access - max_bank_conflict:
            max_access = new_access - max_bank_conflict
        # in max_bank_conflict cycles, data loading can be finished
        # and the stalled access is not merged with access for the next cycle.
        stall_cycles += max_bank_conflict
        
        # number of active cycles for data loading
        act_cycles += (len(row_bank_list_new) != 0) + max_bank_conflict

    return tot_word, max_word, tot_access, max_access, act_cycles, stall_cycles, ideal_start_cycle, ideal_end_cycle


def ddr3_8x8_profiling(
    trace_file=None,
    word_sz_bytes=1,
    page_bits=8192, # number of bits for a dram page/row
    min_addr_word=0,
    max_addr_word=100000
):
    """
    this code takes non-stalling dram trace and reorganizes the trace to meet the bandwidth requirement.
    currently, it does not generate new trace, which can be improved later.
    all default values are for ddr3, the output values are used by cacti "main memory" type
    in this model, the burst behavior in the dram is not modeled, as such the reported cycle count will be larger, i.e., a pessimistic estimation
    """
    
    # output list
    tot_word = 0
    max_word = 0
    tot_access = 0
    tot_row_access = 0
    shift_cycles = 0
    ideal_start_cycle = 0
    ideal_end_cycle = 0

    bank=8 # number of banks in a chip. banks can be interleaved to reduce access latency. not modelled for simplicity.
    burst=8 # number of bytes for a single bank row and col address, and burst is sequential. not modelled for simplicity.
    prefetch=8 # number of prefetches/chips, with each chip referring to 1 prefetch. prefetch is parallel
    io_bits=8 # number of bits provided by all chips, with each chip providing io_bits/prefectch bits, each 8 bit provided by a single bank in the chip

    # number of words per page
    page_byte = page_bits / 8

    # per cycle ddr bandwidth in word
    io_byte = io_bits / 8

    requests = open(trace_file, 'r')

    # applied address mapping: row + bank + col + chip
    # this mapping is just for modeling, and actual implementation can be different
    # for default ddr3 setting, 14-b row + 3-b bank + 10-b col + 3-b chip
    # more info about ddr3 can be found here: http://mermaja.act.uji.es/docencia/is37/data/DDR3.pdf page 15

    # parallel prefetch via chip has higher priority than sequential burst in a bank
    # prefetch_buf format (row idx, col idx, chip idx)
    # consecutive addresses are transmitted using prefetech instead of burst, as they are from the same bank but different chips
    # bank interleaving is not simulated here, as they will not incur high access overhead
    prefetch_buf_new = []
    prefetch_buf_old = []
    current_prefetch = []

    first = True
    act_cycles = 0

    for entry in requests:
        elems = entry.strip().split(',')
        elems = prune(elems)
        elems = [float(x) for x in elems]
        valid_word = 0
        
        if first == True:
            first = False
            ideal_start_cycle = elems[0]

        ideal_end_cycle = elems[0]
        prefetch_buf_new = []

        # memory row index and col index generation inside a chip
        for e in range(1, len(elems)): # each element here is a word
            # only count legal address
            if (elems[e] >= min_addr_word) and (elems[e] < max_addr_word):
                # get the byte addr of the element, as dram is byte addressable
                elem_addr_byte = math.floor((elems[e] - min_addr_word) * word_sz_bytes)
                # this row index contain both row and bank in the address
                row_idx = math.floor(elem_addr_byte / page_byte)
                # col idx inside a chip
                col_idx = math.floor((elem_addr_byte % page_byte) / prefetch)
                # chip index
                chip_idx = math.floor(elem_addr_byte % prefetch)
                prefetch_buf_new.append((row_idx, col_idx, chip_idx))
                valid_word += 1

        # print(len(prefetch_buf_new))
        act_cycles += (len(prefetch_buf_new) > 0)

        # add addresses for multi-byte word
        tmp_prefetch_buf = list(prefetch_buf_new)
        for w in range(math.ceil(word_sz_bytes) - 1):
            for (x, y, z) in tmp_prefetch_buf:
                # get the byte addr of the element, as dram is byte addressable
                elem_addr_byte = x * page_byte + y * prefetch + z + (w + 1)
                # this row index contain both row and bank in the address
                row_idx = math.floor(elem_addr_byte / page_byte)
                # col idx inside a chip
                col_idx = math.floor((elem_addr_byte % page_byte) / prefetch)
                # chip index
                chip_idx = math.floor(elem_addr_byte % prefetch)
                prefetch_buf_new.append((row_idx, col_idx, chip_idx))

        tot_word += valid_word
        if max_word < valid_word:
            max_word = valid_word
        
        # merge the repeated accesses in byte granularity
        prefetch_buf_new = list(set(prefetch_buf_new))

        # print(elems[1:])
        # print(prefetch_buf_new)

        new_access = 0
        # update the prefetch start addr
        prefetch_row_col_new = list(set([(x, y) for (x, y, z) in prefetch_buf_new]))
        prefetch_row_col_old = list(set([(x, y) for (x, y, z) in prefetch_buf_old]))
        for (x, y) in prefetch_row_col_new:
            # a new start address for prefetch
            if (x, y) not in prefetch_row_col_old:
                start_chip = 1000000
                for (i, j, k) in prefetch_buf_new:
                    if x == i and j == y and k < start_chip:
                        # add a new prefetch
                        start_chip = k
                current_prefetch.append((x, y))
                # each prefetch means an access
                new_access += 1
        tot_access += new_access
        # print(new_access)
        # print(current_prefetch)

        for (x, y) in prefetch_row_col_old:
            if (x, y) not in prefetch_row_col_new:
                # remove a prefetch if it's not used anymore
                current_prefetch.remove((x, y))
        # print(current_prefetch)
        
        # only new row accesses from the last load are counted, as old are already buffered
        new_row_access = 0
        # only different blocks are accessed, old accesses are buffered already and required no access
        prefetch_row_new = list(set([x for (x, y, z) in prefetch_buf_new]))
        prefetch_row_old = list(set([x for (x, y, z) in prefetch_buf_old]))
        for a in range(len(prefetch_row_new)):
            if prefetch_row_new[a] not in prefetch_row_old:
                new_row_access += 1
            
        tot_row_access += new_row_access

        prefetch_buf_old = prefetch_buf_new
    
    # divided by two because of ddr
    shift_cycles = max((math.ceil(tot_access / 2) - act_cycles), 0 )

    # print(tot_access / 2)
    # print(act_cycles)
    return tot_word, max_word, tot_access, tot_row_access, shift_cycles, ideal_start_cycle, ideal_end_cycle


def prune(input_list):
    l = []

    for e in input_list:
        e = e.strip() # remove the leading and trailing characters, here space
        if e != '' and e != ' ':
            l.append(e)

    return l



if __name__ == "__main__":
    # output = sram_profiling(
    #     trace_file="outputs/example_run/simArchOut/layer_wise/example_run_Conv1_sram_read.csv", 
    #     word_sz_bytes=1,
    #     block_sz_bytes=16,
    #     bank=4,
    #     min_addr_word=00000000, 
    #     max_addr_word=10000000,
    #     access_buf=True)
    # print("ifmap", output)

    # output = sram_profiling(
    #     trace_file="outputs/example_run/simArchOut/layer_wise/example_run_Conv1_sram_read.csv", 
    #     word_sz_bytes=1,
    #     block_sz_bytes=16,
    #     bank=4,
    #     min_addr_word=10000000, 
    #     max_addr_word=20000000,
    #     access_buf=True)
    # print("weight", output)

    # output = sram_profiling(
    #     trace_file="outputs/example_run/simArchOut/layer_wise/example_run_Conv1_sram_read.csv", 
    #     word_sz_bytes=1,
    #     block_sz_bytes=16,
    #     bank=4,
    #     min_addr_word=20000000, 
    #     max_addr_word=30000000,
    #     access_buf=True)
    # print("ofmap", output)

    # output = dram_profiling(
    #     trace_file="outputs/example_run/simArchOut/layer_wise/example_run_Conv1_dram_ifmap_read.csv", 
    #     word_sz_bytes=1,
    #     page_sz_bytes=1024,
    #     chip=8,
    #     bw_bytes=16,
    #     sram_sz_word=1024,
    #     sram_block_sz_word=16,
    #     min_addr_word=00000000, 
    #     max_addr_word=10000000)
    # print("ifmap", output)

    # output = dram_profiling(
    #     trace_file="outputs/example_run/simArchOut/layer_wise/example_run_Conv1_dram_filter_read.csv", 
    #     word_sz_bytes=1,
    #     page_sz_bytes=1024,
    #     chip=8,
    #     bw_bytes=16,
    #     sram_sz_word=1024,
    #     sram_block_sz_word=16,
    #     min_addr_word=10000000, 
    #     max_addr_word=20000000)
    # print("weight", output)

    # output = dram_profiling(
    #     trace_file="outputs/example_run/simArchOut/layer_wise/example_run_Conv1_dram_ofmap_write.csv", 
    #     word_sz_bytes=1,
    #     page_sz_bytes=1024,
    #     chip=8,
    #     bw_bytes=16,
    #     sram_sz_word=1024,
    #     sram_block_sz_word=16,
    #     min_addr_word=20000000, 
    #     max_addr_word=30000000)
    # print("ofmap", output)

    output = ddr3_8x8_profiling(trace_file="config/example_run/test_trace.csv",
                            word_sz_bytes=2,
                            page_bits=8192,
                            min_addr_word=10000000,
                            max_addr_word=20000000
                            )
    print(
            "\ntot_word", output[0], 
            "\nmax_word", output[1], 
            "\ntot_access", output[2], 
            "\ntot_row_access", output[3], 
            "\nshift_cycles", output[4], 
            "\nideal_start_cycle", output[5], 
            "\nideal_end_cycle", output[6]
        )