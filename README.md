# uSystolic-Sim
*uSystolic-Sim* is a systolic array simulator built on top of [ARM SCALE-Sim](https://github.com/ARM-software/SCALE-Sim), which leverages memory traces to evaluate:
1) the execution latency
2) the memory bandwidth
3) the power and energy consumption, including both the computing kernel and memory hierarchy


## Feature
### 1. Weight-stationary dataflow
*uSystolic-Sim* focuses on the weight-stationary dataflow, which enables low-cost and high-accuracy unary computing for a fair comparison with bianry computing.
However, it is open to any customized dataflow.

### 2. Cycle-accurate trace generation
Assuming no stalls in the computing kernel, *uSystolic-Sim* generates perfect cycle-accurate SRAM traces and approximate DRAM traces. Note that [ARM SCALE-Sim](https://github.com/ARM-software/SCALE-Sim) does not generate cycle-accurate traces, as it assumes [zero data feeding delay](https://github.com/diwu1990/uSystolic-Sim/blob/main/outputs/README.md). This difference does not change the latency and bandwidth numbers, but provides better estimation of the power and energy.

### 3. Computing-scheme-aware, multi-cycle MAC operation
*uSystolic-Sim* is aware of the computing scheme at the kernel, including [unary computing](https://conferences.computer.org/isca/pdfs/ISCA2020-4QlDegUf3fKiwUXfV0KdCm/466100a377/466100a377.pdf), bit-serial and bit-parallel binary computing. *uSystolic-Sim* offers per GEMM level configuration for MAC operations. The maximum cycle count for a MAC operation is related to the computing scheme in the kernel. For exmaple, with N-bit binary source data, unary computing, bit-seral and bit-parallel binary computing will spend at most 2^N, N and 1 cycles for one MAC operations, respectively.

### 4. Varying-bitwidth data
*uSystolic-Sim* provides flexible configuration for the data bitwidth. The data bitwidth can be arbitrary as required by the target application, and will ultimately influence the power and energy consumption. Note that *uSystolic-Sim* focuses on the performance and efficiency evaluation, while ignoring the influence of data bitwidth on accuracy.

## Workflow
### 1. Architecture simulation - [simArch](https://github.com/diwu1990/uSystolic-Sim/blob/main/simArch)
All mandatory traces are generated for all GEMM operations, e.g., in deep neural networks. Also, the MAC utilization is reported.

### 2. Hardware simulation - [simHw](https://github.com/diwu1990/uSystolic-Sim/blob/main/simHw)
The traces are profiled to generate the ideal and real latency, bandwidth, throughout and runtime for all GEMM operations. Intermediate data for power and energy estimation are also generated at this step. This step accounts for most of the total runtime.

### 3. Efficiency simulation - [simEff](https://github.com/diwu1990/uSystolic-Sim/blob/main/simEff)
The Intermediate data, together with SRAM, DRAM and systolic array configurations, are utilized to estimate the power and energy consumption for all hardware.

### Input
All inputs are configuration files for the target systolic array, including
1. ./config/run_name/systolic.cfg: file to get systolic array architechture from
2. ./config/run_name/network.csv: consecutive GEMM topologies to read
3. ./config/run_name/sram.cfg: SRAM configs for hardware simulation. Note that the sizes are specified in systolic.cfg
4. ./config/run_name/dram.cfg: DRAM configs for hardware simulation
5. ./config/run_name/pe.cfg: PE area and power data for hardware simulation

To generate example configuration files, run:```python3 sweep_config.py```, and you will see the generated configuration files in ./config.

### Output

The simulator generates read write traces and summary logs at ```./outputs/<run_name>```.

* Layer wise runtime and average utilization
* Layer wise MAX DRAM bandwidth log
* Layer wise AVG DRAM bandwidth log
* Layer wise breakdown of data movement and compute cycles

In addition cycle accurate SRAM/DRAM access logs are also dumped and could be accesses at ```./outputs/<run_name>/layer_wise```


## Example run
* Run a single configuration:```python3 evaluate.py -name=/name/of/the/run/in/.config/folder```
* Run all configurations:```source run_all.sh```


## Citing

To be released.

<!-- If you find this tool useful for your research, please use the following bibtex to cite us,

```
bib
``` -->

## Authors

[Di Wu](http://diwu1990.github.io/), Department of ECE, University of Wisconsin-Madison

