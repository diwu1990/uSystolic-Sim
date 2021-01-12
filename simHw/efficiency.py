import math
import subprocess
import simHw.profiling.mem_block_profiling as profiling

def efficiency(
    ifmap_sram_size=1, # in K-Word
    filter_sram_size=1, # in K-Word
    ofmap_sram_size=1, # in K-Word
    sram_file=None,
    dram_file=None,
    pe_file=None,
    profiling_file=None
):
    """
    this code run CACTI according to the configuration of ifmap, filter, ofmap to get power and energy
    1) it calculates the required numbre of banks for SRAM/DRAM (ifmap, filter and ofmap SRAM, as well DRAM)
    2) it profiles the trace file from architecture simulation, and report the required bank count for memory
    3) the cacti result, together with the run time reported from architecture simulation, will generate the total power and total enery for each component
    """
    ifmap_sram_size *= 1024 # in Byte
    filter_sram_size *= 1024 # in Byte
    ofmap_sram_size *= 1024 # in Byte

    power = 0
    energy = 0
    return power, energy


