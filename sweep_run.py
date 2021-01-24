import evaluate
import os

def gen_run_config():

    arch_list = ["tpu", "eyeriss"]
    network_list = ["alexnet"]
    bit_list = [8, 16]
    cycle_list = [32, 64, 128, 256]

    for b in bit_list:
        for c in cycle_list:
            for a in arch_list:
                computing = "ur"
                path = a + "_" + str(b) + "b_" + computing + str(c) + "c_" + "dram_sram"
                print(path)
            # if not os.path.exists("./outputs/"):
            # os.system("mkdir ./outputs")


if __name__ == '__main__':
    gen_run_config()
