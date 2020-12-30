import os
import time
import configparser as cp
import run_nets as r
from absl import flags
from absl import app
import platform

FLAGS = flags.FLAGS
# name of flag | default | explanation
flags.DEFINE_string("arch_config", "./input_config/eval.cfg", "file where we are getting our architechture from")
flags.DEFINE_string("network", "./input_topology/test_net/test_net.csv", "topology that we are reading")

class eval:
    def __init__(self, sweep = False, save = False):
        self.sweep = sweep
        self.save_space = save

    def parse_config(self):
        general = 'general'
        arch_sec = 'architecture_presets'
        net_sec  = 'network_presets'
        config_filename = FLAGS.arch_config
        print("Using Architechture from ",config_filename)

        config = cp.ConfigParser()
        config.read(config_filename)

        ## Read the run name
        self.run_name = config.get(general, 'run_name')

        ## Read the architecture_presets
        ## Array height min, max
        ar_h = config.get(arch_sec, 'ArrayHeight').split(',')
        self.ar_h_min = ar_h[0].strip()

        if len(ar_h) > 1:
            self.ar_h_max = ar_h[1].strip()

        ## Array width min, max
        ar_w = config.get(arch_sec, 'ArrayWidth').split(',')
        self.ar_w_min = ar_w[0].strip()

        if len(ar_w) > 1:
            self.ar_w_max = ar_w[1].strip()

        ## IFMAP SRAM buffer min, max
        # in KB
        ifmap_sram = config.get(arch_sec, 'IfmapSramSz').split(',')
        self.isram_min = ifmap_sram[0].strip()

        if len(ifmap_sram) > 1:
            self.isram_max = ifmap_sram[1].strip()


        ## FILTER SRAM buffer min, max
        # in KB
        filter_sram = config.get(arch_sec, 'FilterSramSz').split(',')
        self.fsram_min = filter_sram[0].strip()

        if len(filter_sram) > 1:
            self.fsram_max = filter_sram[1].strip()


        ## OFMAP SRAM buffer min, max
        # in KB
        ofmap_sram = config.get(arch_sec, 'OfmapSramSz').split(',')
        self.osram_min = ofmap_sram[0].strip()

        if len(ofmap_sram) > 1:
            self.osram_max = ofmap_sram[1].strip()

        self.dataflow= config.get(arch_sec, 'Dataflow')

        ifmap_offset = config.get(arch_sec, 'IfmapOffset')
        self.ifmap_offset = int(ifmap_offset.strip())

        filter_offset = config.get(arch_sec, 'FilterOffset')
        self.filter_offset = int(filter_offset.strip())

        ofmap_offset = config.get(arch_sec, 'OfmapOffset')
        self.ofmap_offset = int(ofmap_offset.strip())
        
        word_sz_bytes = config.get(arch_sec, 'WordByte')
        self.word_sz_bytes = float(word_sz_bytes.strip())
        
        mac_cycles = config.get(arch_sec, 'MACCycle')
        self.mac_cycles = int(mac_cycles.strip())
        
        self.wgt_bw_opt= config.get(arch_sec, 'WeightBwOpt')

        self.topology_file= FLAGS.network

    def run_eval(self):
        self.parse_config()

        if self.sweep == False:
            self.run_once()
        else:
            self.run_sweep()


    def run_once(self):

        df_string = "Weight Stationary"
        assert self.dataflow == 'ws', "Input dataflow for uSystolic should be weight stationary."

        print("====================================================")
        print("***************** uSystolic SIM ********************")
        print("====================================================")
        print("Array Size: \t" + str(self.ar_h_min) + "x" + str(self.ar_w_min))
        print("SRAM IFMAP: \t" + str(self.isram_min))
        print("SRAM Filter: \t" + str(self.fsram_min))
        print("SRAM OFMAP: \t" + str(self.osram_min))
        print("Word Bytes: \t" + str(self.word_sz_bytes))
        print("Weight BW Opt: \t" + str(self.wgt_bw_opt))
        print("CSV file path: \t" + self.topology_file)
        print("Dataflow: \t" + df_string)
        print("====================================================")

        net_name = self.topology_file.split('/')[-1].split('.')[0]
        offset_list = [self.ifmap_offset, self.filter_offset, self.ofmap_offset]

        r.run_net(  ifmap_sram_size  = int(self.isram_min), # in KB
                    filter_sram_size = int(self.fsram_min), # in KB
                    ofmap_sram_size  = int(self.osram_min), # in KB
                    array_h = int(self.ar_h_min),
                    array_w = int(self.ar_w_min),
                    net_name = net_name,
                    data_flow = self.dataflow,
                    word_size_bytes = self.word_sz_bytes,
                    mac_cycles = self.mac_cycles,
                    wgt_bw_opt = self.wgt_bw_opt,
                    topology_file = self.topology_file,
                    offset_list = offset_list
                )
        self.cleanup()
        print("************ uSystolic SIM Run Complete ************")


    def cleanup(self):
        system = platform.system()
        if system == "Windows":
            # for windows system
            if not os.path.isdir(".\\outputs"):
                os.system("mkdir .\\outputs")

            net_name = self.topology_file.split('/')[-1].split('.')[0]

            path = ".\\output\\eval_out"
            if self.run_name == "":
                path = ".\\outputs\\" + net_name +"_"+ self.dataflow
            else:
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
            # for windows system
            if not os.path.exists("./outputs/"):
                os.system("mkdir ./outputs")

            net_name = self.topology_file.split('/')[-1].split('.')[0]

            path = "./output/eval_out"
            if self.run_name == "":
                path = "./outputs/" + net_name +"_"+ self.dataflow
            else:
                path = "./outputs/" + self.run_name

            if not os.path.exists(path):
                os.system("mkdir " + path)
            else:
                t = time.time()
                new_path= path + "_" + str(t)
                os.system("move " + path + " " + new_path)
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
    s = eval(save = False, sweep = False)
    s.run_eval()

if __name__ == '__main__':
  app.run(main)
