import math

def mem_block_profiling(
    trace_file=None,
    word_sz_bytes=4,
    mem_block_sz_bytes=16, # in byte
    bank=8,
    min_addr_word=0,
    max_addr_word=100000
):
    """
    this code takes non-stalling traces and bank settings to ensure that the bandwidth can be maximally met
    it reports the actual stall time due to sram data loading conflict.
    """
    tot_access = 0
    max_access = 0
    act_cycles = 0
    stall_cycles = 0
    ideal_start_cycle = 0
    ideal_end_cycle = 0

    mem_block_sz_word = mem_block_sz_bytes / word_sz_bytes

    mem_requests = open(trace_file, 'r')

    # index list of bank and line for each access
    bank_line_list_new = []

    first = True

    for entry in mem_requests:
        
        elems = entry.strip().split(',')
        elems = prune(elems)
        elems = [float(x) for x in elems]

        if first == True:
            first = False
            if elems[0] > 0:
                ideal_start_cycle = 0
            else:
                ideal_start_cycle = elems[0]
        # this value does not matter here, just used to get the ideal max cycle
        ideal_end_cycle = elems[0]

        bank_line_list_old = bank_line_list_new

        bank_line_list_new = []

        # memory block index and bank index generation
        for e in range(1, len(elems)): # each element here is a word
            # only count legal address
            if (elems[e] >= min_addr_word) and (elems[e] < max_addr_word):
                line_idx = int(math.floor((elems[e] - min_addr_word) / (mem_block_sz_word * bank)))
                # cache banking, LSB of index
                bank_idx = int(math.floor((elems[e] - min_addr_word) / mem_block_sz_word) % bank)
                # sram banking, LSB
                # bank_idx = int(math.floor((elems[e] - min_addr_word))) % bank
                bank_line_list_new.append((line_idx, bank_idx))
        
        # conflict check
        # only new accesses from the last load are counted, as old are already buffered
        new_access = 0
        for a in range(len(bank_line_list_new)):
            if bank_line_list_new[a] not in bank_line_list_old:
                new_access += 1
        
        # max repeated access to the same bank, but different line
        max_repeated_access = 0
        for a in range(len(bank_line_list_new)):
            diff_bank_line_list = [(x - bank_line_list_new[a][0], y - bank_line_list_new[a][1]) for (x, y) in bank_line_list_new]

            repeated_access = 0

            for b in range(a+1, len(bank_line_list_new)):
                # two accesses are to the same bank, but different blocks. this increase the stall by 1.
                if diff_bank_line_list[b][0] == 0 and diff_bank_line_list[b][1] != 0:
                    repeated_access += 1
            
            if max_repeated_access < repeated_access:
                max_repeated_access = repeated_access
        
        tot_access += new_access
        # max parallel sram block access
        if max_access < new_access - max_repeated_access:
            max_access = new_access - max_repeated_access
        # in max_repeated_access cycles, data loading can be finished
        stall_cycles += max_repeated_access
        
        # number of active cycles for data loading
        act_cycles += (len(bank_line_list_new) != 0) + max_repeated_access
    
    return tot_access, max_access, act_cycles, stall_cycles, ideal_start_cycle, ideal_end_cycle

def prune(input_list):
    l = []

    for e in input_list:
        e = e.strip() # remove the leading and trailing characters, here space
        if e != '' and e != ' ':
            l.append(e)

    return l


if __name__ == "__main__":
    output = mem_block_profiling(
        trace_file="outputs/eyeriss_ws_UnaryRate/layer_wise/example_run_Conv1_sram_read.csv", 
        word_sz_bytes=1,
        mem_block_sz_bytes=16,
        bank=8,
        min_addr_word=00000000, 
        max_addr_word=10000000)
    print("ifmap", output)

    output = mem_block_profiling(
        trace_file="outputs/eyeriss_ws_UnaryRate/layer_wise/example_run_Conv1_sram_read.csv", 
        word_sz_bytes=1,
        mem_block_sz_bytes=16,
        bank=8,
        min_addr_word=10000000, 
        max_addr_word=20000000)
    print("weight", output)

    output = mem_block_profiling(
        trace_file="outputs/eyeriss_ws_UnaryRate/layer_wise/example_run_Conv1_sram_read.csv", 
        word_sz_bytes=1,
        mem_block_sz_bytes=16,
        bank=8,
        min_addr_word=20000000, 
        max_addr_word=30000000)
    print("ofmap", output)