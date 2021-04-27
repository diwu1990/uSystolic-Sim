The architecute simulation in *uSystolic-Sim* is adapted from [SCALE-Sim](https://github.com/ARM-software/SCALE-Sim) by ARM. In brief, the key difference is that *uSystolic-Sim* emphasizes the influence of computing schemes, while SCALE-Sim targets the influence of dataflow.

The following table provides a comparison between them. For general performance analysis, *uSystolic-Sim* additionally supports asymmetric strides in matrix convolution, besides the report of trace, latency, utilization and bandwidth. For the dataflow, *uSystolic-Sim* currently only supports weight stationary, which natually provides high accuracy for unary computing; on the other hand, SCALE-Sim is developed to provide generalizability. For computing scheme, *uSystolic-Sim* can support varying computing schemes with different MAC cycle count and data bitwidth, which jointly influence the cycle-level trace behavior, as well as the final energy and power consumption.

| Function | Feature               | *uSystolic-Sim*    | SCALE-Sim          |
| -------- | --------------------- | ------------------ | ------------------ |
| Performance Analysis  | <ul><li>Trace generation</li><li>GEMM latency</li><li>MAC utilization</li><li>Memory bandwidth</li><li>Asymmetric strides</li></ul> | <ul><li>:heavy_check_mark:</li><li>:heavy_check_mark:</li><li>:heavy_check_mark:</li><li>:heavy_check_mark:</li><li>:heavy_check_mark:</li></ul> | <ul><li>:heavy_check_mark:</li><li>:heavy_check_mark:</li><li>:heavy_check_mark:</li><li>:heavy_check_mark:</li><li></li></ul> |
| Dataflow | <ul><li>Weight stationary</li><li>Input stationary</li><li>Output stationary</li></ul>      | <ul><li>:heavy_check_mark:</li><li></li><li></li></ul> | <ul><li>:heavy_check_mark:</li><li>:heavy_check_mark:</li><li>:heavy_check_mark:</li></ul> |
| Computing scheme | <ul><li>Multi-cycle MAC</li><li>Varying-bitwidth data</li><li>Cycle-accurate trace</li></ul> | <ul><li>:heavy_check_mark:</li><li>:heavy_check_mark:</li><li>:heavy_check_mark:</li></ul> | <ul><li></li><li></li><li></li></ul> |


## Architecute simulation workflow

### 1. Configure systolic array hardware.
Configure the hardware using [parameters](https://github.com/diwu1990/uSystolic-Sim/blob/main/config_src/systolic_config/README.md), which remain unchanged during the execution of all GEMMs.

### 2. Configure GEMM typology.
Configure the GEMM using [parameters](https://github.com/diwu1990/uSystolic-Sim/tree/main/config_src/network_config/README.md) with each GEMM having its own typology and MAC cycle count.

### 3. Generate the perfect trace.
Above configurations are read by the simulator to generate cycle-accurate traces for both SRAM and DRAM, assuming no stalls.
