# uSystolic-Sim
*uSystolic-Sim* is a [systolic array](https://github.com/ARM-software/SCALE-Sim/blob/master/ideas.md) simulator built on top of [ARM SCALE-Sim](https://github.com/ARM-software/SCALE-Sim), which leverages memory traces to evaluate:
1) area
2) bandwidth
3) runtime
4) throughput
5) energy
6) power
of the systolic array with varying computing schemes.

## Feature
The major features in *uSystolic-Sim* different from [ARM SCALE-Sim](https://github.com/ARM-software/SCALE-Sim) are list below.
### 1. Weight-stationary dataflow
*uSystolic-Sim* focuses on the weight-stationary dataflow, which enables low-cost and high-accuracy unary computing for a fair comparison with binary computing.

### 2. Varying-bitwidth data
*uSystolic-Sim* provides flexible configuration for the data bitwidth. The data bitwidth can be arbitrary as required by the target application, and will ultimately influence the power and energy consumption.

### 3. Computing-scheme-aware, multi-cycle MAC operation
*uSystolic-Sim* is aware of the computing scheme at the kernel, including [unary computing](https://unarycomputing.github.io/), bit-parallel and bit-serial binary computing. *uSystolic-Sim* offers per GEMM level configuration for MAC operations. The maximum cycle count for a MAC operation is related to the computing scheme in the kernel. For exmaple, with N-bit binary source data, unary computing, bit-parallel and bit-seral binary computing will spend at most 2^N, 1 and N cycles for a single MAC operation, respectively.

### 4. Memory-contention-aware run-time statistics
Assuming stall-less computation in the systolic array, *uSystolic-Sim* first generates perfect cycle-accurate SRAM traces and DRAM traces, unlike [ARM SCALE-Sim](https://github.com/ARM-software/SCALE-Sim) assuming [zero data feeding delay](https://github.com/diwu1990/uSystolic-Sim/blob/main/outputs/README.md) (not cycle-accurate). Then *uSystolic-Sim* further takes into consideration the memory contention for more realistic run-time statistics to evaluate the systolic array hardware.



## Workflow
### 1. Architecture simulation - [simArch](https://github.com/diwu1990/uSystolic-Sim/blob/main/simArch)
All mandatory traces are generated for all GEMM operations, e.g., in deep neural networks. Also, the MAC utilization is reported.

### 2. Hardware simulation - [simHw](https://github.com/diwu1990/uSystolic-Sim/blob/main/simHw)
The traces are profiled to generate both the ideal and real bandwidth, runtime and throughput for all GEMM operations. Intermediate data for energy and power estimation are also generated at this step. This step accounts for most of the total runtime.

### 3. Efficiency simulation - [simEff](https://github.com/diwu1990/uSystolic-Sim/blob/main/simEff)
The Intermediate data, together with SRAM, DRAM and systolic array configurations, are utilized to estimate the power and energy consumption for all hardware.

## System requirement
1. Linux OS
2. python3.x
3. absl-py
4. configparser
5. subprocess
6. tqdm
7. gcc/g++

Tested on Ubuntu 20.04.2.0 LTS (Focal Fossa)

## Input
All inputs for <run_name> shall be contained in ```./config/<run_name>```. Inputs are configuration files for the target systolic array, including:
1) ```./config/<run_name>/systolic.cfg```: systolic array configuration.
2) ```./config/<run_name>/network.csv``` : GEMM configuration.
3) ```./config/<run_name>/sram.cfg```    : SRAM configuration for hardware simulation. Note that the sizes are specified in systolic.cfg.
4) ```./config/<run_name>/dram.cfg```    : DRAM configuration for hardware simulation.
5) ```./config/<run_name>/pe.cfg```      : PE area and power data for hardware simulation. Those numbers should be pre-synthesized.

Example configuration files can be obtained by running ```python3 sweep_config.py``` and then will be generated in ```./config/```.

## Output

All outputs for <run_name> will be located in ```./outputs/<run_name>```.

1) ```./outputs/<run_name>/simArchOut``` : the traces files and the report for MAC utilization.
2) ```./outputs/<run_name>/simHwOut```   : the ideal and real reports for bandwidth, throughput and runtime.
3) ```./outputs/<run_name>/simEffOut```  : the real reports for area, power and energy.
4) ```./outputs/<run_name>/config```     : the input configuration, a copy of ```./config/<run_name>.

By default, the logs will be displayed in terminal with indications of above result folders.

## Command to run
For first-time users, you will need a disk space more than 700GB to ensure, all default configurations can be successfully run.
1. ```python3 sweep_config.py```: generate all default configurations with each located in ```./config/<run_name>```.
2. ```source run_all.sh```: run all configurations in ```./config/<run_name>```. This shell script will run those configurations in background and move all logs to ```./log/<run_name>```.
3. ```source run_check```: check whether all ```./config/<run_name>``` produce correspondent results in ```./outputs/<run_name>```.

Run a single configuration:

```python3 evaluate.py -name=./config/<run_name>```, and logs will be displayed in terminal by default.

*If the current run is stopped before it finishes, run ```source clean.sh``` before starting the next run.*

## Citing

To be released.

<!-- If you find this tool useful for your research, please use the following bibtex to cite us,

```
bib
``` -->

## Author

[Di Wu](http://diwu1990.github.io/), Department of ECE, University of Wisconsin-Madison

