import subprocess
import os
import time

def sram_cacti(
    mem_sz_bytes=16, # in byte
    origin_config_file=None,
    target_config_file=None,
    result_file=None
):
    """
    run the cacti with input configuration, work for SRAM, whose size is either calculated to match the bw or pre-specified
    """
    original = open(origin_config_file, 'r')
    target   = open(target_config_file, 'w')

    target.write("-size (bytes) " + str(mem_sz_bytes) + "\n")
    
    for entry in original:
        target.write(entry)
    
    original.close()
    target.close()

    if not os.path.exists("./simEff/cacti7/cacti"):
        subprocess.call(["make", "all"], shell=True, cwd="./simEff/cacti7/")
        time.sleep(20)
    rep_cmd = "cp ./cacti ./cacti_" + target_config_file
    subprocess.call([rep_cmd], shell=True, cwd="./simEff/cacti7/")
    final_cmd = "./cacti_" + target_config_file + " -infile ../../" + target_config_file + " > ../../" + result_file
    subprocess.call([final_cmd], shell=True, cwd="./simEff/cacti7/")
    rm_cmd = "rm -rf ./cacti_" + target_config_file
    subprocess.call([rm_cmd], shell=True, cwd="./simEff/cacti7/")


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

        if line_idx == 2:
            # unit: mW
            block_sz_bytes = float(entry.strip().split(':')[-1].strip())
    
    if line_idx <= 64:
        raise ValueError("Check " + report + " for sram cacti failure.")

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
    cacti_out.close()
    return block_sz_bytes, max_freq, energy_per_block_rd, energy_per_block_wr, leakage_power, total_area


def dram_cacti(
    origin_config_file=None,
    target_config_file=None,
    result_file=None
):
    """
    run the cacti with input configuration, work for DRAM (DRAM size is pre-specified)
    """
    original = open(origin_config_file, 'r')
    target   = open(target_config_file, 'w')

    for entry in original:
        target.write(entry)
    
    original.close()
    target.close()

    if not os.path.exists("./simEff/cacti7/cacti"):
        subprocess.call(["make", "all"], shell=True, cwd="./simEff/cacti7/")
        time.sleep(20)
    rep_cmd = "cp ./cacti ./cacti_" + target_config_file
    subprocess.call([rep_cmd], shell=True, cwd="./simEff/cacti7/")
    final_cmd = "./cacti_" + target_config_file + " -infile ../../" + target_config_file + " > ../../" + result_file
    subprocess.call([final_cmd], shell=True, cwd="./simEff/cacti7/")
    rm_cmd = "rm -rf ./cacti_" + target_config_file
    subprocess.call([rm_cmd], shell=True, cwd="./simEff/cacti7/")


def dram_report_extract(
    report=None
):
    # get the area and power numbers in the report for final memory power and energy estimation.
    cacti_out = open(report, 'r')

    line_idx = 0
    for entry in cacti_out:
        line_idx += 1
        if line_idx == 12:
            ram_type = entry.strip().split(':')[-1].strip()
            assert ram_type == "Scratch RAM", "Invalid DRAM type."
        if line_idx == 50:
            # unit: ns
            bank = float(entry.strip().split(':')[-1].strip())
        if line_idx == 58:
            # unit: ns
            access_time = float(entry.strip().split(':')[-1].strip())
        if line_idx == 59:
            # unit: ns
            cycle_time = float(entry.strip().split(':')[-1].strip())
        if line_idx == 61:
            # unit: nJ
            activate_energy = float(entry.strip().split(':')[-1].strip())
        if line_idx == 62:
            # unit: nJ
            energy_rd = float(entry.strip().split(':')[-1].strip())
        if line_idx == 63:
            # unit: nJ
            energy_wr = float(entry.strip().split(':')[-1].strip())
        if line_idx == 64:
            # unit: nJ
            precharge_energy = float(entry.strip().split(':')[-1].strip())
        if line_idx == 65:
            # unit: mW
            leakage_power_closed_page = float(entry.strip().split(':')[-1].strip())
        if line_idx == 66:
            # unit: mW
            leakage_power_open_page = float(entry.strip().split(':')[-1].strip())
        if line_idx == 67:
            # unit: mW
            leakage_power_IO = float(entry.strip().split(':')[-1].strip())
        if line_idx == 68:
            # unit: mW
            refresh_power = float(entry.strip().split(':')[-1].strip())
        if line_idx == 69:
            # unit: mm^2
            height = float(entry.strip().split(':')[-1].split('x')[0].strip())
            width = float(entry.strip().split(':')[-1].split('x')[1].strip())
            area = height * width

    if line_idx <= 69:
        raise ValueError("Check " + report + " for dram cacti failure.")

    # MHz
    max_freq = 1 / cycle_time * 1000
    cacti_out.close()
    return max_freq, activate_energy, energy_rd, energy_wr, precharge_energy, leakage_power_closed_page, leakage_power_open_page, leakage_power_IO, refresh_power, area


if __name__ == "__main__":

    sram_cacti(
        mem_sz_bytes=1024*1024, # in byte
        origin_config_file="./config/example_run/sram.cfg", 
        target_config_file="./config/example_run/real_sram.cfg",
        result_file="./config/example_run/sram.rpt"
        )

    out = sram_report_extract(
        report="./config/example_run/sram.rpt"
        )

    print(out)