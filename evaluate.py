import os
import time
import math
import configparser as cp
import simArch.run_nets as r
import simHw.efficiency as eff
from absl import flags
from absl import app
import platform
import subprocess
import warnings

FLAGS = flags.FLAGS
# name of flag | default | explanation
flags.DEFINE_string("name", "template_run", "indicateing path to get config files")
# template is tpu_08b_ur_032c_ddr3_w_sram_alexnet
# architecture sim input config
# path/systolic.cfg: file to get systolic array architechture from
# path/network.csv: consecutive GEMM topologies to read
# hardware sim input config
# path/sram.cfg: SRAM configs for hardware simulation. Note that the sizes are specified in systolic.cfg
# path/dram.cfg: DRAM configs for hardware simulation
# path/pe.cfg: PE area and power data for hardware simulation

class evaluate:
    def __init__(self, save = False, simArch = True, simHw = True):
        self.save_space = save
        self.simArch = simArch
        self.simHw = simHw

    def parse_config(self):
        general = 'general'
        arch_sec = 'architecture_presets'
        hw_sec = 'hardware_presets'
        path = os.getcwd() + "/config/" + FLAGS.name

        if not os.path.exists(path):
            raise ValueError("Input name is invalid.")

        config_filename = path + "/systolic.cfg"
        print("Using Architechture from ",config_filename)

        config = cp.ConfigParser()
        config.read(config_filename)

        ## Read the run name from the configuration path
        self.run_name = config_filename.split('/')[-2]

        ## Read the architecture_presets
        ## Array height
        ar_h = config.get(arch_sec, 'ArrayHeight').split(',')
        self.ar_h = ar_h[0].strip()

        ## Array width
        ar_w = config.get(arch_sec, 'ArrayWidth').split(',')
        self.ar_w = ar_w[0].strip()

        ## IFMAP SRAM buffer
        # in K-Word
        ifmap_sram = config.get(arch_sec, 'IfmapSramSz').split(',')
        self.isram = ifmap_sram[0].strip()

        ## FILTER SRAM buffer
        # in K-Word
        filter_sram = config.get(arch_sec, 'FilterSramSz').split(',')
        self.fsram = filter_sram[0].strip()

        ## OFMAP SRAM buffer
        # in K-Word
        ofmap_sram = config.get(arch_sec, 'OfmapSramSz').split(',')
        self.osram = ofmap_sram[0].strip()

        self.dataflow= config.get(arch_sec, 'Dataflow')
        self.df_string = "Weight Stationary"
        assert self.dataflow == 'ws', "Input dataflow for uSystolic should be weight stationary."

        # in Word
        ifmap_offset = config.get(arch_sec, 'IfmapOffset')
        self.ifmap_offset = int(ifmap_offset.strip())

        # in Word
        filter_offset = config.get(arch_sec, 'FilterOffset')
        self.filter_offset = int(filter_offset.strip())

        # in Word
        ofmap_offset = config.get(arch_sec, 'OfmapOffset')
        self.ofmap_offset = int(ofmap_offset.strip())
        
        word_sz_bytes = config.get(arch_sec, 'WordByte')
        self.word_sz_bytes = float(word_sz_bytes.strip())
        
        self.wgt_bw_opt = to_bool(config.get(arch_sec, 'WeightBwOpt').strip())

        # this parameter is used to evaluate power and energy
        self.computing= config.get(arch_sec, 'Computing').strip()

        self.zero_sram_ifmap = to_bool(config.get(hw_sec, 'ZeroIfmapSram').strip())
        self.zero_sram_filter = to_bool(config.get(hw_sec, 'ZeroFilterSram').strip())
        self.zero_sram_ofmap = to_bool(config.get(hw_sec, 'ZeroOfmapSram').strip())
        self.sram_access_buf = to_bool(config.get(hw_sec, 'SramAccBuf').strip())

        self.topology_file = path + "/network.csv"

        self.sram_file = path + "/sram.cfg"

        self.dram_file = path + "/dram.cfg"

        self.pe_file = path + "/pe.cfg"
        
        self.time_stamp = time.time()

    def run_eval(self):
        self.parse_config()

        # clean up first to avoid program stuck
        os.system("chmod 777 ./clean.sh")
        os.system("./clean.sh")

        if self.simArch == True:
            self.run_arch()

        if self.simHw == True:
            self.run_hw()

    def run_arch(self):

        print("====================================================")
        print("************ uSystolic Architecture Sim ************")
        print("====================================================")
        print("Array Size:    \t" + str(self.ar_h) + "x" + str(self.ar_w))
        print("SRAM IFMAP:    \t" + str(self.isram))
        print("SRAM Filter:   \t" + str(self.fsram))
        print("SRAM OFMAP:    \t" + str(self.osram))
        print("Word Bytes:    \t" + str(self.word_sz_bytes))
        print("Dataflow:      \t" + self.df_string)
        print("Weight BW Opt: \t" + str(self.wgt_bw_opt))
        print("CSV file:      \t" + self.topology_file)
        print("====================================================")

        offset_list = [self.ifmap_offset, self.filter_offset, self.ofmap_offset] # in Word

        # for arch sim, dram trace generation requires non-zero sram size
        # now arch sim only reports the mac utilization, as well as generating ideal sram and dram traces
        r.run_net(
            ifmap_sram_size  = int(self.isram), # in K-Word
            filter_sram_size = int(self.fsram), # in K-Word
            ofmap_sram_size  = int(self.osram), # in K-Word
            array_h = int(self.ar_h),
            array_w = int(self.ar_w),
            net_name = self.run_name,
            data_flow = self.dataflow,
            word_size_bytes = self.word_sz_bytes,
            wgt_bw_opt = self.wgt_bw_opt,
            topology_file = self.topology_file,
            offset_list = offset_list
            )
        self.arch_cleanup()
        print("******* uSystolic Architecture Sim Complete ********")
        sec = time.time() - self.time_stamp
        hours = int(math.floor(sec / 3600))
        mins = int(math.floor((sec % 3600) / 60))
        secs = int(math.floor(sec % 60))
        print("Runtime: " + str(hours) + "-hours,    " + str(mins) + "-mins,    " + str(secs) + "-secs")
        self.time_stamp = time.time()
        print("Results: ./outputs/"+self.run_name+"/simArchOut/")

    def run_hw(self):
        print()
        print()
        print()
        print("====================================================")
        print("************** uSystolic Hardware Sim **************")
        print("====================================================")
        print("Computing:     \t" + self.computing)
        print("SRAM file:     \t" + self.sram_file)
        print("DRAM file:     \t" + self.dram_file)
        print("PE file:       \t" + self.pe_file)
        print("====================================================")

        if self.zero_sram_ifmap == True:
            # estimate the ifmap sram size to hide latency
            print("IFMAP  SRAM is disabled in actual hardware.")
            if self.computing == "BinarySerial" or self.computing == "BinaryParallel":
                print("\tFor binary computing, this is not suggested!\n")
            self.isram = 0
        if self.zero_sram_filter == True:
            # estimate the filter sram size to hide latency
            print("FILTER SRAM is disabled in actual hardware.")
            if self.computing == "BinarySerial" or self.computing == "BinaryParallel":
                print("\tFor binary computing, this is not suggested!\n")
            self.fsram = 0
        if self.zero_sram_ofmap == True:
            # estimate the ofmap sram size to hide latency
            print("OFMAP  SRAM is disabled in actual hardware.")
            if self.computing == "BinarySerial" or self.computing == "BinaryParallel":
                print("\tFor binary computing, this is not suggested!\n")
            self.osram = 0
        
        eff.estimate(
            array_h = int(self.ar_h),
            array_w = int(self.ar_w),
            ifmap_sram_size  = int(self.isram), # in K-Word
            filter_sram_size = int(self.fsram), # in K-Word
            ofmap_sram_size  = int(self.osram), # in K-Word
            word_sz_bytes=self.word_sz_bytes, # bytes per word
            ifmap_base=self.ifmap_offset, # in word
            filter_base=self.filter_offset, # in word
            ofmap_base=self.ofmap_offset, # in word
            sram_cfg_file=self.sram_file,
            dram_cfg_file=self.dram_file,
            pe_cfg_file=self.pe_file,
            computing=self.computing,
            run_name=self.run_name,
            topology_file=self.topology_file,
            sram_access_buf=self.sram_access_buf
        )
        self.hw_cleanup()
        print("********* uSystolic Hardware Sim Complete **********")
        sec = time.time() - self.time_stamp
        hours = int(math.floor(sec / 3600))
        mins = int(math.floor((sec % 3600) / 60))
        secs = int(math.floor(sec % 60))
        print("Runtime: " + str(hours) + "-hours,    " + str(mins) + "-mins,    " + str(secs) + "-secs")
        print("Results: ./outputs/"+self.run_name+"/simHwOut/")
        print()

    def arch_cleanup(self):
        if not os.path.exists("./outputs/"):
            os.system("mkdir ./outputs")

        path = "./outputs/" + self.run_name + "/simArchOut"

        if not os.path.exists(path):
            os.system("mkdir -p " + path + "/")
        else:
            t = time.time()
            new_path= path + "_" + str(t)
            os.system("mv " + path + " " + new_path)
            os.system("mkdir -p " + path + "/")

        cmd = "mv " + self.run_name + "*.csv " + path
        os.system(cmd)

        cmd = "mkdir " + path +"/layer_wise"
        os.system(cmd)

        cmd = "mv " + path + "/" + self.run_name + "*sram* " + path +"/layer_wise"
        os.system(cmd)

        cmd = "mv " + path + "/" + self.run_name + "*dram* " + path +"/layer_wise"
        os.system(cmd)

        if self.save_space == True:
            cmd = "rm -rf " + path +"/layer_wise"
            os.system(cmd)

    def hw_cleanup(self):
        # for linux os
        if not os.path.exists("./outputs/"):
            os.system("mkdir ./outputs")

        path = "./outputs/" + self.run_name + "/simHwOut"

        if not os.path.exists(path):
            os.system("mkdir -p " + path + "/")
        else:
            t = time.time()
            new_path= path + "_" + str(t)
            os.system("mv " + path + " " + new_path)
            os.system("mkdir -p " + path + "/")

        cmd = "mv " + self.run_name + "*.rpt " + path
        os.system(cmd)

        cmd = "mv " + self.run_name + "*.cfg* " + path
        os.system(cmd)

        cmd = "mv " + self.run_name + "*.csv " + path
        os.system(cmd)


def to_bool(value):
    """
       Converts 'something' to boolean. Raises exception for invalid formats
           Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
           Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...
    """
    if str(value).lower() in ("yes", "y", "true",  "t", "1"): return True
    if str(value).lower() in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))


def main(argv):
    s = evaluate(save = False, simArch = True, simHw = True)
    s.run_eval()

if __name__ == '__main__':
    app.run(main)
