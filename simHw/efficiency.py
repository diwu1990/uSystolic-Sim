def efficiency(
    ifmap_sram_size=1, # in KB
    filter_sram_size=1, # in KB
    ofmap_sram_size=1, # in KB
    sram_file=None,
    dram_file=None,
    pe_file=None
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
