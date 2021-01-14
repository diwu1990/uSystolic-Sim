import math

def sram_profiling(
    trace_file=None,
    word_sz_bytes=4,
    block_sz_bytes=16, # in byte
    bank=8,
    min_addr_word=0,
    max_addr_word=100000,
    access_buf=True
):
    """
    this code takes non-stalling traces and bank settings to ensure that the bandwidth can be maximally met
    it reports the actual stall time due to sram data loading conflict.
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

    # index list of bank and line for each access
    bank_line_list_new = []

    first = True

    for entry in requests:
        
        elems = entry.strip().split(',')
        elems = prune(elems)
        elems = [float(x) for x in elems]

        valid_word = 0

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
                line_idx = int(math.floor((elems[e] - min_addr_word) / (block_sz_word * bank)))
                # cache banking, LSB of index bits
                bank_idx = int(math.floor((elems[e] - min_addr_word) / block_sz_word) % bank)
                # sram banking, LSB
                # bank_idx = int(math.floor((elems[e] - min_addr_word))) % bank
                bank_line_list_new.append((line_idx, bank_idx))
                valid_word += 1

        tot_word += valid_word
        if max_word < valid_word:
            max_word = valid_word

        # merge access if they have identical bank and line index: the actual access to different blocks
        bank_line_list_new = list(set(bank_line_list_new))

        # conflict check
        # only new accesses from the last load are counted, as old are already buffered
        new_access = 0
        if access_buf == True:
            # only different blocks are accessed, old accesses are buffered already and required no access
            for a in range(len(bank_line_list_new)):
                if bank_line_list_new[a] not in bank_line_list_old:
                    new_access += 1
        else:
            new_access = len(bank_line_list_new)
        
        # max repeated access to the same bank, but different line
        max_bank_conflict = 0
        for a in range(len(bank_line_list_new)):
            diff_bank_line_list = [(x - bank_line_list_new[a][0], y - bank_line_list_new[a][1]) for (x, y) in bank_line_list_new]

            bank_conflict = 0

            for b in range(a+1, len(bank_line_list_new)):
                # two accesses are to the same bank, but different blocks. this increase the stall by 1.
                if diff_bank_line_list[b][0] == 0 and diff_bank_line_list[b][1] != 0:
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
        act_cycles += (len(bank_line_list_new) != 0) + max_bank_conflict
    
    return tot_word, max_word, tot_access, max_access, act_cycles, stall_cycles, ideal_start_cycle, ideal_end_cycle


def sram_profiling(
    trace_file=None,
    word_sz_bytes=4,
    block_sz_bytes=16, # in byte
    bank=8,
    min_addr_word=0,
    max_addr_word=100000,
    access_buf=True
):
    return None


def prune(input_list):
    l = []

    for e in input_list:
        e = e.strip() # remove the leading and trailing characters, here space
        if e != '' and e != ' ':
            l.append(e)

    return l



if __name__ == "__main__":
    output = sram_profiling(
        trace_file="outputs/eyeriss_ws_UnaryRate/layer_wise/example_run_Conv1_sram_read.csv", 
        word_sz_bytes=1,
        block_sz_bytes=16,
        bank=8,
        min_addr_word=00000000, 
        max_addr_word=10000000,
        access_buf=True)
    print("ifmap", output)

    output = sram_profiling(
        trace_file="outputs/eyeriss_ws_UnaryRate/layer_wise/example_run_Conv1_sram_read.csv", 
        word_sz_bytes=1,
        block_sz_bytes=16,
        bank=8,
        min_addr_word=10000000, 
        max_addr_word=20000000,
        access_buf=True)
    print("weight", output)

    output = sram_profiling(
        trace_file="outputs/eyeriss_ws_UnaryRate/layer_wise/example_run_Conv1_sram_read.csv", 
        word_sz_bytes=1,
        block_sz_bytes=16,
        bank=8,
        min_addr_word=20000000, 
        max_addr_word=30000000,
        access_buf=True)
    print("ofmap", output)