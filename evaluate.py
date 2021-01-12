import os
import time
import configparser as cp
import simArch.run_nets as r
import simHw.efficiency as eff
from absl import flags
from absl import app
import platform

FLAGS = flags.FLAGS
# name of flag | default | explanation
# architecture sim input config
flags.DEFINE_string("systolic", "./config/example_run/systolic.cfg", "file to get systolic array architechture from")
flags.DEFINE_string("network", "./config/example_run/gemm.csv", "consecutive GEMM topologies to read")
# hardware sim input config
flags.DEFINE_string("sram", "./config/example_run/sram.cfg", "SRAM configs for hardware simulation. Note that the sizes are specified in systolic.cfg")
flags.DEFINE_string("dram", "./config/example_run/dram.cfg", "DRAM configs for hardware simulation")
flags.DEFINE_string("pe", "./config/example_run/pe.cfg", "PE area and power data for hardware simulation")

class evaluate:
    def __init__(self, save = False, arch = True, hw = True):
        self.save_space = save
        self.simArch = arch
        self.simHw = hw

    def parse_config(self):
        general = 'general'
        arch_sec = 'architecture_presets'
        config_filename = FLAGS.systolic
        print("Using Architechture from ",config_filename)

        config = cp.ConfigParser()
        config.read(config_filename)

        ## Read the run name
        self.run_name = config.get(general, 'run_name')

        ## Read the architecture_presets
        ## Array height min, max
        ar_h = config.get(arch_sec, 'ArrayHeight').split(',')
        self.ar_h_min = ar_h[0].strip()

        ## Array width min, max
        ar_w = config.get(arch_sec, 'ArrayWidth').split(',')
        self.ar_w_min = ar_w[0].strip()

        ## IFMAP SRAM buffer min, max
        # in K-Word
        ifmap_sram = config.get(arch_sec, 'IfmapSramSz').split(',')
        self.isram_min = ifmap_sram[0].strip()

        ## FILTER SRAM buffer min, max
        # in K-Word
        filter_sram = config.get(arch_sec, 'FilterSramSz').split(',')
        self.fsram_min = filter_sram[0].strip()

        ## OFMAP SRAM buffer min, max
        # in K-Word
        ofmap_sram = config.get(arch_sec, 'OfmapSramSz').split(',')
        self.osram_min = ofmap_sram[0].strip()

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
        
        self.wgt_bw_opt= config.get(arch_sec, 'WeightBwOpt')

        # this parameter is used to evaluate power and energy
        self.computing= config.get(arch_sec, 'Computing')

        self.topology_file = FLAGS.network

        self.sram_file = FLAGS.sram

        self.dram_file = FLAGS.dram

        self.pe_file = FLAGS.pe

    def run_eval(self):
        self.parse_config()

        if self.simArch == True:
            self.run_arch()

        if self.simHw == True:
            self.run_hw()

    def run_arch(self):
        # either linux or windows OS works

        print("====================================================")
        print("************ uSystolic Architecture Sim ************")
        print("====================================================")
        print("Array Size: \t" + str(self.ar_h_min) + "x" + str(self.ar_w_min))
        print("SRAM IFMAP: \t" + str(self.isram_min))
        print("SRAM Filter: \t" + str(self.fsram_min))
        print("SRAM OFMAP: \t" + str(self.osram_min))
        print("Word Bytes: \t" + str(self.word_sz_bytes))
        print("Dataflow: \t" + self.df_string)
        print("Weight BW Opt: \t" + str(self.wgt_bw_opt))
        print("CSV file path: \t" + self.topology_file)
        print("====================================================")

        net_name = self.topology_file.split('/')[-2]
        offset_list = [self.ifmap_offset, self.filter_offset, self.ofmap_offset] # in Word

        self.profiling_file = r.run_net(
                    ifmap_sram_size  = int(self.isram_min), # in K-Word
                    filter_sram_size = int(self.fsram_min), # in K-Word
                    ofmap_sram_size  = int(self.osram_min), # in K-Word
                    array_h = int(self.ar_h_min),
                    array_w = int(self.ar_w_min),
                    net_name = net_name,
                    data_flow = self.dataflow,
                    word_size_bytes = self.word_sz_bytes,
                    wgt_bw_opt = self.wgt_bw_opt,
                    topology_file = self.topology_file,
                    offset_list = offset_list
                )
        self.arch_cleanup()
        print("******* uSystolic Architecture Sim Complete ********")

    def run_hw(self):
        # linux OS is required due to executing CACTI

        print("====================================================")
        print("************** uSystolic Hardware Sim **************")
        print("====================================================")
        print("Computing: \t" + self.computing)
        print("Weight BW Opt: \t" + str(self.wgt_bw_opt))
        print("SRAM file path: \t" + self.sram_file)
        print("DRAM file path: \t" + self.dram_file)
        print("PE file path: \t" + self.pe_file)
        print("====================================================")

        eff.efficiency(
            ifmap_sram_size=1, # in K-Word
            filter_sram_size=1, # in K-Word
            ofmap_sram_size=1, # in K-Word
            sram_file=self.sram_file,
            dram_file=self.dram_file,
            pe_file=self.pe_file,
            profiling_file=self.profiling_file
        )
        # self.hw_cleanup()

        print("********* uSystolic Hardware Sim Complete **********")

    def arch_cleanup(self):
        system = platform.system()
        if system == "Windows":
            # for windows os
            if not os.path.isdir(".\\outputs"):
                os.system("mkdir .\\outputs")

            path = ".\\outputs\\" + self.run_name

            if not os.path.isdir(path):
                os.system("mkdir " + path)
            else:
                t = time.time()
                new_path= path + "_" + str(t)
                os.system("move " + path + " " + new_path)
                os.system("mkdir " + path)

            cmd = "move *.csv " + path
            os.system(cmd)

            cmd = "mkdir " + path +"\\layer_wise"
            os.system(cmd)

            cmd = "move " + path +"\\*sram* " + path +"\\layer_wise"
            os.system(cmd)

            cmd = "move " + path +"\\*dram* " + path +"\\layer_wise"
            os.system(cmd)

            if self.save_space == True:
                cmd = "rm -rf " + path +"\\layer_wise"
                os.system(cmd)
        else:
            # for linux os
            if not os.path.exists("./outputs/"):
                os.system("mkdir ./outputs")

            path = "./outputs/" + self.run_name

            if not os.path.exists(path):
                os.system("mkdir " + path)
            else:
                t = time.time()
                new_path= path + "_" + str(t)
                os.system("mv " + path + " " + new_path)
                os.system("mkdir " + path)

            cmd = "mv *.csv " + path
            os.system(cmd)

            cmd = "mkdir " + path +"/layer_wise"
            os.system(cmd)

            cmd = "mv " + path +"/*sram* " + path +"/layer_wise"
            os.system(cmd)

            cmd = "mv " + path +"/*dram* " + path +"/layer_wise"
            os.system(cmd)

            if self.save_space == True:
                cmd = "rm -rf " + path +"/layer_wise"
                os.system(cmd)

    def hw_cleanup(self):
        system = platform.system()
        if system == "Windows":
            # for windows os
            if not os.path.isdir(".\\outputs"):
                os.system("mkdir .\\outputs")

            path = ".\\outputs\\" + self.run_name

            if not os.path.isdir(path):
                os.system("mkdir " + path)
            else:
                t = time.time()
                new_path= path + "_" + str(t)
                os.system("move " + path + " " + new_path)
                os.system("mkdir " + path)

            cmd = "move *.csv " + path
            os.system(cmd)

            cmd = "mkdir " + path +"\\layer_wise"
            os.system(cmd)

            cmd = "move " + path +"\\*sram* " + path +"\\layer_wise"
            os.system(cmd)

            cmd = "move " + path +"\\*dram* " + path +"\\layer_wise"
            os.system(cmd)

            if self.save_space == True:
                cmd = "rm -rf " + path +"\\layer_wise"
                os.system(cmd)
        else:
            # for linux os
            if not os.path.exists("./outputs/"):
                os.system("mkdir ./outputs")

            path = "./outputs/" + self.run_name

            if not os.path.exists(path):
                os.system("mkdir " + path)
            else:
                t = time.time()
                new_path= path + "_" + str(t)
                os.system("mv " + path + " " + new_path)
                os.system("mkdir " + path)

            cmd = "mv *.csv " + path
            os.system(cmd)

            cmd = "mkdir " + path +"/layer_wise"
            os.system(cmd)

            cmd = "mv " + path +"/*sram* " + path +"/layer_wise"
            os.system(cmd)

            cmd = "mv " + path +"/*dram* " + path +"/layer_wise"
            os.system(cmd)

            if self.save_space == True:
                cmd = "rm -rf " + path +"/layer_wise"
                os.system(cmd)


def main(argv):
    s = evaluate(save = False, arch = True, hw = True)
    s.run_eval()

if __name__ == '__main__':
  app.run(main)
