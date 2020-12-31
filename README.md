# uSystolic-Sim
*uSystolic-Sim* is a [systolic array](https://github.com/diwu1990/uSystolic-Sim/blob/main/systolic_array.md) simulator, which generates cycle-accurate traces to evaluate 
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
All mandatory traces are generated to evaluate the latency, utilization and bandwidth for all GEMM operations, e.g., in deep neural networks.
The config files inside [input_config](https://github.com/diwu1990/uSystolic-Sim/blob/main/input_config/README.md) contain achitecture presets.
The csv files inside [input_topology](https://github.com/diwu1990/uSystolic-Sim/blob/main/input_topology/README.md) contain different networks.

### 2. Hardware simulation - [simHw](https://github.com/diwu1990/uSystolic-Sim/blob/main/simHw/README.md)
The traces, latency and bandwidth numbers are further used to model the power and energy consumption of the systolic array with the a target computing scheme.

## Example run
* Run the default configuration: ```python eval.py```
* Wait for the run to finish

* Run your own configuration:```python scale.py -arch_config=input_config/your_own.cfg -network=input_topology/your_own.csv```
* Wait for the run to finish

### Output

The simulator generates read write traces and summary logs at ```./outputs/<run_name>```.

* Layer wise runtime and average utilization
* Layer wise MAX DRAM bandwidth log
* Layer wise AVG DRAM bandwidth log
* Layer wise breakdown of data movement and compute cycles

In addition cycle accurate SRAM/DRAM access logs are also dumped and could be accesses at ```./outputs/<run_name>/layer_wise```

## Citing

To be released.

<!-- If you find this tool useful for your research, please use the following bibtex to cite us,

```
bib
``` -->

## Authors

[Di Wu](http://diwu1990.github.io/), Department of ECE, University of Wisconsin-Madison

