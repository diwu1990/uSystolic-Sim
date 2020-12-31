# uSystolic-Sim
*uSystolic-Sim* is a systolic array simulator, which generates cycle-accurate traces to evaluate 
1) the latency for GEMM execution the computing kernel
2) the bandwidth for memory hierarchy
3) the power and energy consumption, including both the computing kernel and memory hierarchy

*uSystolic-Sim* is aware of the computing scheme at the kernel, including [unary computing](https://conferences.computer.org/isca/pdfs/ISCA2020-4QlDegUf3fKiwUXfV0KdCm/466100a377/466100a377.pdf), bit-serial and bit-parallel binary computing.

## Feature
### 1. Weight-stationary dataflow
Ideally, *uSystolic-Sim* is open to any dataflow. But currently, it focuses on the weight-stationary dataflow, which enables low-cost and high-accuracy unary computing for a fair comparison with bianry computing.

### 2. Cycle-accurate trace generation
Assuming no stalls in the computing kernel, *uSystolic-Sim* generates cycle-accurate SRAM traces and approximate DRAM traces.

### 3. Computing scheme-aware, multi-cycle MAC operation
*uSystolic-Sim* offers per GEMM level configuration for MAC operations. The maximum cycle count for a MAC operation is related to the computing scheme in the kernel. For exmaple, with N-bit binary source data, unary computing, bit-seral and bit-parallel binary computing will spend at most 2^N, N and 1 cycles for one MAC operations, respectively.

### 4. Varying-bitwidth data
*uSystolic-Sim* provides per GEMM level configuration for the data bitwidth. The data bitwidth can be arbitrary, as required by the target application, and will ultimately influence the power and energy consumption. Note that *uSystolic-Sim* focuses on the performance and efficiency evaluation, while ignoring the influence of data bitwidth on accuracy.

## Workflow
### 1. Architecture simulation - [simArch](https://github.com/diwu1990/uSystolic-Sim/blob/main/simArch/README.md)
All mandatory traces are generated to evaluate the latency and bandwidth for all GEMM operations, e.g., in deep neural networks.

### 2. Hardware simulation - [simHw](https://github.com/diwu1990/uSystolic-Sim/blob/main/simHw/README.md)
The traces, latency and bandwidth numbers are further used to model the power and energy consumption of the systolic array with the a target computing scheme.

## Example run
This experiment will run the default MLPERF_AlphaGoZero_32x32_os architechture contained inside scale.cfg. 
It will also run alexnet as its network topology.
* Run the command: ```python scale.py```
* Wait for the run to finish


Here is sample of the config file.  
![sample config](https://raw.githubusercontent.com/AnandS09/SCALE-Sim/master/images/config_example.png "sample config")    
Architecture presets are the variable parameters for SCALE-Sim, like array size, memory etc.  

The Network Topoplogy csv file contains the network that we want to test in our architechture.  
SCALE-Sim accepts topology csv in the format shown below.  
![yolo_tiny topology](https://raw.githubusercontent.com/AnandS09/SCALE-Sim/master/images/yolo_tiny_csv.png "yolo_tiny.csv")

Since SCALE-Sim is a CNN simulator please do not provide any layers other than convolutional or fully connected in the csv.
You can take a look at 
[yolo_tiny.csv](https://raw.githubusercontent.com/AnandS09/SCALE-Sim/master/topologies/yolo_tiny.csv)
for your reference.

### Output

Here is an example output dumped to stdout when running Yolo tiny (whose configuration is in yolo_tiny.csv):
![screen_out](https://github.com/AnandS09/SCALE-Sim/blob/master/images/output.png "std_out")

Also, the simulator generates read write traces and summary logs at ```./outputs/<topology_name>```.
There are three summary logs:

* Layer wise runtime and average utilization
* Layer wise MAX DRAM bandwidth log
* Layer wise AVG DRAM bandwidth log
* Layer wise breakdown of data movement and compute cycles

In addition cycle accurate SRAM/DRAM access logs are also dumped and could be accesses at ```./outputs/<topology_name>/layer_wise```

The config file inside configs contain achitecture presets.  
the csv files inside toologies contain different networks

In order to change a different arichtechture/network, create a new .cfg file inside ```cofigs``` and call a new network by running
```python scale.py -arch_config=configs/eyeriss.cfg -network=topologies/yolo.csv```





## Citing

To be released.

<!-- If you find this tool useful for your research, please use the following bibtex to cite us,

```
bib
``` -->

## Authors

[Di Wu](http://diwu1990.github.io/), Department of ECE, University of Wisconsin-Madison

