import math

def sram_profiling(
    trace_file=None,
    word_sz_bytes=4,
    block_sz_bytes=16, # in byte for bank row
    bank=8,
    min_addr_word=0,
    max_addr_word=100000,
    access_buf=True
):
    """
    this code takes non-stalling traces and bank settings to ensure that the bandwidth can be maximally met
    it reports the stall time due to sram data conflict.
    """
    tot_word = 0
    max_word = 0
    tot_access = 0
    max_access = 0
    act_cycles = 0
    stall_cycles = 0
    ideal_start_cycle = 0
    ideal_end_cycle = 0

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
        # this value does not matter here, just used to get the ideal max cycle
        ideal_end_cycle = elems[0]

        row_bank_list_old = row_bank_list_new
        row_bank_list_new = []

        # memory block index and bank index generation
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

        # conflict check
        # only new accesses from the last load are counted, as old are already buffered
        new_access = 0
        if access_buf == True:
            # only different blocks are accessed, old accesses are buffered already and required no access
            for a in range(len(row_bank_list_new)):
                if row_bank_list_new[a] not in row_bank_list_old:
                    new_access += 1
        else:
            new_access = len(row_bank_list_new)
        
        # max repeated access to the same bank, but different row
        max_bank_conflict = 0
        for a in range(len(row_bank_list_new)):
            diff_row_bank_list = [(x - row_bank_list_new[a][0], y - row_bank_list_new[a][1]) for (x, y) in row_bank_list_new]

            bank_conflict = 0
            for b in range(a+1, len(row_bank_list_new)):
                # two accesses are to the same bank, but different blocks. this increase the stall by 1.
                if diff_row_bank_list[b][0] != 0 and diff_row_bank_list[b][1] == 0:
                    bank_conflict += 1
            
            if max_bank_conflict < bank_conflict:
                max_bank_conflict = bank_conflict

        tot_access += new_access
        # max parallel sram block access
        if max_access < new_access - max_bank_conflict:
            max_access = new_access - max_bank_conflict
        # in max_bank_conflict cycles, data loading can be finished
        stall_cycles += max_bank_conflict
        
        # number of active cycles for data loading
        act_cycles += (len(row_bank_list_new) != 0) + max_bank_conflict

        # if len(row_bank_list_new) > 0:
        #     print(row_bank_list_new, max_bank_conflict, stall_cycles)

    return tot_word, max_word, tot_access, max_access, act_cycles, stall_cycles, ideal_start_cycle, ideal_end_cycle


def dram_profiling(
    trace_file=None,
    word_sz_bytes=4,
    page_sz_bytes=16, # in byte for a dram row/page
    bank=8,
    bw_bytes=16, # in byte, 64 bits x 2 / 8 = 16 bytes for DDR3
    sram_sz_word=4,
    sram_block_sz_word=4,
    min_addr_word=0,
    max_addr_word=100000
):
    """
    this code takes non-stalling traces and bank settings to ensure that the bandwidth can be maximally met
    it reports the stall time due to dram data conflict.
    """
    tot_word = 0
    max_word = 0
    tot_row_access = 0
    tot_access = 0
    ideal_start_cycle = 0
    ideal_end_cycle = 0

    page_sz_word = page_sz_bytes / word_sz_bytes
    bw_word = bw_bytes / word_sz_bytes

    sram_block = [] # length indicated by sram_sz_word
    max_sram_block = sram_sz_word / sram_block_sz_word

    per_sram_block_cycle = sram_block_sz_word / bw_word

    requests = open(trace_file, 'r')

    # index list of bank and row for each access
    row_bank_list_new = []

    first = True
    last_burst_end_cycle = -1000000000 # can be arbitrarily large
    cur_burst_start_cycle = 0
    previous_cycle = 0
    budget_cycles = 0
    shift_cycles = 0

    for entry in requests:
        
        elems = entry.strip().split(',')
        elems = prune(elems)
        elems = [float(x) for x in elems]

        valid_word = 0

        if first == True:
            first = False
            ideal_start_cycle = elems[0]
            previous_cycle = elems[0] - 1
        
        # this value does not matter here, just used to get the ideal max cycle
        ideal_end_cycle = elems[0]
        row_bank_list_old = row_bank_list_new
        row_bank_list_new = []

        # memory block index and bank index generation
        for e in range(1, len(elems)): # each element here is a word
            # only count legal address
            if (elems[e] >= min_addr_word) and (elems[e] < max_addr_word):
                row_idx = int(math.floor((elems[e] - min_addr_word) / page_sz_word))
                # cache banking, LSB of index bits
                bank_idx = int(math.floor((elems[e] - min_addr_word) / (page_sz_word / bank)) % bank)
                row_bank_list_new.append((row_idx, bank_idx))
                valid_word += 1
        # print(row_bank_list_new)

        tot_word += valid_word
        if max_word < valid_word:
            max_word = valid_word

        # merge access if they have identical bank and row index: the actual access to different blocks
        row_bank_list_new = list(set(row_bank_list_new))

        extra_cycles = -1
        # check whether the required row/bank is already in sram
        for e in range(len(row_bank_list_new)):
            if e in sram_block:
                pass
            else:
                if len(sram_block) >= max_sram_block:
                    sram_block.pop(0)
                sram_block.append(e)
                extra_cycles += per_sram_block_cycle
        
        budget_cycles -= extra_cycles
        if budget_cycles < 0:
            shift_cycles += extra_cycles
        
        if extra_cycles > 0:
            tot_access += extra_cycles + 1
        else:
            tot_access += 1

        # conflict check
        # only new accesses from the last load are counted, as old are already buffered
        new_row_access = 0
        # only different blocks are accessed, old accesses are buffered already and required no access
        for a in range(len(row_bank_list_new)):
            if row_bank_list_new[a][0] not in [x for (x, y) in row_bank_list_old]:
                new_row_access += 1
        
        tot_row_access += new_row_access
        
        # print(tot_row_access, row_bank_list_new, row_bank_list_old)

        if previous_cycle + 1 < elems[0]:
            # print("old", last_burst_end_cycle, cur_burst_start_cycle, budget_cycles)
            last_burst_end_cycle = previous_cycle
            cur_burst_start_cycle = elems[0]
            budget_cycles += cur_burst_start_cycle - last_burst_end_cycle
            # print("new", last_burst_end_cycle, cur_burst_start_cycle, budget_cycles)

        previous_cycle = elems[0]

    if shift_cycles > 0:
        shift_cycles = math.ceil(shift_cycles)
    else:
        shift_cycles = math.floor(shift_cycles)
    
    tot_access = math.ceil(tot_access)

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
    #     bank=8,
    #     min_addr_word=00000000, 
    #     max_addr_word=10000000,
    #     access_buf=True)
    # print("ifmap", output)

    # output = sram_profiling(
    #     trace_file="outputs/example_run/simArchOut/layer_wise/example_run_Conv1_sram_read.csv", 
    #     word_sz_bytes=1,
    #     block_sz_bytes=16,
    #     bank=8,
    #     min_addr_word=10000000, 
    #     max_addr_word=20000000,
    #     access_buf=True)
    # print("weight", output)

    # output = sram_profiling(
    #     trace_file="outputs/example_run/simArchOut/layer_wise/example_run_Conv1_sram_read.csv", 
    #     word_sz_bytes=1,
    #     block_sz_bytes=16,
    #     bank=8,
    #     min_addr_word=20000000, 
    #     max_addr_word=30000000,
    #     access_buf=True)
    # print("ofmap", output)

    output = dram_profiling(
        trace_file="outputs/example_run/simArchOut/layer_wise/example_run_Conv1_dram_ifmap_read.csv", 
        word_sz_bytes=1,
        page_sz_bytes=1024,
        bank=8,
        bw_bytes=16,
        sram_sz_word=1024,
        sram_block_sz_word=16,
        min_addr_word=00000000, 
        max_addr_word=10000000)
    print("ifmap", output)

    output = dram_profiling(
        trace_file="outputs/example_run/simArchOut/layer_wise/example_run_Conv1_dram_filter_read.csv", 
        word_sz_bytes=1,
        page_sz_bytes=1024,
        bank=8,
        bw_bytes=16,
        sram_sz_word=1024,
        sram_block_sz_word=16,
        min_addr_word=10000000, 
        max_addr_word=20000000)
    print("weight", output)

    output = dram_profiling(
        trace_file="outputs/example_run/simArchOut/layer_wise/example_run_Conv1_dram_ofmap_write.csv", 
        word_sz_bytes=1,
        page_sz_bytes=1024,
        bank=8,
        bw_bytes=16,
        sram_sz_word=1024,
        sram_block_sz_word=16,
        min_addr_word=20000000, 
        max_addr_word=30000000)
    print("ofmap", output)