import math

def bank_calc(
    trace_file=None,
    word_sz_bytes=4,
    mem_block_sz_bytes=16, # in byte
    min_addr_word=0,
    max_addr_word=100000
):
    """
    this code calculates the number of required banks according to the trace file
    the resultant bank count can be very large in some case
    as a result, this code is not involved in the pipeline, but acts as a refence instead
    """

    mem_block_sz_word = mem_block_sz_bytes / word_sz_bytes

    mem_requests = open(trace_file, 'r')

    bank = 1
    line = 0
    for entry in mem_requests:
        line += 1
        elems = entry.strip().split(',')
        elems = prune(elems)
        elems = [float(x) for x in elems]

        bank_enough = False
        while bank_enough == False:
            line_list = []
            bank_list = []

            # memory block index and bank index generation
            for e in range(1, len(elems)): # each element here is a word
                # only count legal address
                if (elems[e] >= min_addr_word) and (elems[e] < max_addr_word):
                    line_list.append(int(math.floor((elems[e] - min_addr_word) / (mem_block_sz_word * bank))))
                    # sram banking, LSB
                    bank_list.append(int(math.floor((elems[e] - min_addr_word))) % bank)
                    # cache banking, LSB of index
                    # bank_list.append(int(math.floor((elems[e] - min_addr_word) / mem_block_sz_word) % bank))
            
            bank_enough = True
            # conflict check
            for a in range(len(line_list)):
                diff_line_list = [x - line_list[a] for x in line_list]
                diff_bank_list = [x - bank_list[a] for x in bank_list]

                for b in range(a+1, len(line_list)):
                    if diff_bank_list[b] == 0 and diff_line_list[b] != 0:
                        bank_enough = False
                        continue
                
                if bank_enough == False:
                    continue
            
            if bank_enough == False:
                # print("line: ", line, " current bank: ", bank, "new bank: ", bank *2)
                # print(elems, line_list, bank_list)
                bank = bank * 2

    return bank


def prune(input_list):
    l = []

    for e in input_list:
        e = e.strip() # remove the leading and trailing characters, here space
        if e != '' and e != ' ':
            l.append(e)

    return l


if __name__ == "__main__":
    bank = bank_calc(
        trace_file="outputs/eyeriss_ws_UnaryRate/layer_wise/example_run_Conv1_sram_read.csv", 
        word_sz_bytes=1,
        mem_block_sz_bytes=16,
        min_addr_word=0,
        max_addr_word=10000000)
    print("ifmap bank: ", bank)

    bank = bank_calc(
        trace_file="outputs/eyeriss_ws_UnaryRate/layer_wise/example_run_Conv1_sram_read.csv", 
        word_sz_bytes=1,
        mem_block_sz_bytes=16,
        min_addr_word=10000000, 
        max_addr_word=20000000)
    print("weight bank: ", bank)

    bank = bank_calc(
        trace_file="outputs/eyeriss_ws_UnaryRate/layer_wise/example_run_Conv1_sram_read.csv", 
        word_sz_bytes=1,
        mem_block_sz_bytes=16,
        min_addr_word=20000000, 
        max_addr_word=30000000)
    print("ofmap bank: ", bank)