import subprocess

def run_cacti(
    mem_sz_bytes=16, # in byte
    mem_config_file=None,
    target_config_file=None,
    result_file=None
):
    """
    run the cacti with input configuration, work for both DRAM and SRAM
    """
    original = open(mem_config_file, 'r')
    target   = open(target_config_file, 'w')

    target.write("-size (bytes) " + str(mem_sz_bytes) + "\n")
    
    for entry in original:
        target.write(entry)
    
    original.close()
    target.close()

    subprocess.call(["make", "all"], shell=True, cwd="./simHw/cacti7/")
    final_cmd = "./cacti -infile ../../" + target_config_file + " > ../../" + result_file
    subprocess.call([final_cmd], shell=True, cwd="./simHw/cacti7/")


def sram_report_extract(
    report=None
):
    # get the area and power numbers in the report for final memory power and energy estimation.
    cacti_out = open(report, 'r')

    line_idx = 0
    for entry in cacti_out:
        line_idx += 1
        if line_idx == 12:
            ram_type = entry.strip().split(':')[-1].strip()
            assert ram_type == "Scratch RAM", "Invalid SRAM type."
        if line_idx == 50:
            # unit: ns
            bank = float(entry.strip().split(':')[-1].strip())
        if line_idx == 58:
            # unit: ns
            access_time = float(entry.strip().split(':')[-1].strip())
        if line_idx == 59:
            # unit: ns
            cycle_time = float(entry.strip().split(':')[-1].strip())
        if line_idx == 60:
            # unit: nJ
            dynamic_energy_rd = float(entry.strip().split(':')[-1].strip())
        if line_idx == 61:
            # unit: nJ
            dynamic_energy_wr = float(entry.strip().split(':')[-1].strip())
        if line_idx == 62:
            # unit: mW
            leakage_power_bank = float(entry.strip().split(':')[-1].strip())
        if line_idx == 63:
            # unit: mW
            gate_leakage_power_bank = float(entry.strip().split(':')[-1].strip())
        if line_idx == 64:
            # unit: mm^2
            height = float(entry.strip().split(':')[-1].split('x')[0].strip())
            width = float(entry.strip().split(':')[-1].split('x')[1].strip())
            area = height * width
    
    # MHz
    max_freq = 1 / cycle_time * 1000
    # nJ
    energy_per_block_rd = dynamic_energy_rd
    # nJ
    energy_per_block_wr = dynamic_energy_wr
    # mW
    leakage_power = (leakage_power_bank + gate_leakage_power_bank) * bank
    # mm^2
    total_area = area
    return max_freq, energy_per_block_rd, energy_per_block_wr, leakage_power, total_area


def dram_report_extract(
    report=None
):
    # get the area and power numbers in the report for final memory power and energy estimation.

    return None


if __name__ == "__main__":

    run_cacti(
        mem_sz_bytes=1024*1024, # in byte
        mem_config_file="./config/example_run/sram.cfg", 
        target_config_file="./config/example_run/real_sram.cfg",
        result_file="./config/example_run/sram.rpt"
        )

    out = sram_report_extract(
        report="./config/example_run/sram.rpt"
        )

    print(out)