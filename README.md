# uSystolic-Sim
*uSystolic-Sim* is a systolic array simulator, which generates cycle-accurate traces to evaluate 
1) the latency for GEMM execution
2) the bandwidth for memory accesses
3) the power and energy consumption, including both computing kernels and memory hierarchies

*uSystolic-Sim* is aware of the computing scheme, including [unary computing](https://conferences.computer.org/isca/pdfs/ISCA2020-4QlDegUf3fKiwUXfV0KdCm/466100a377/466100a377.pdf), bit-serial binary computing and bit-parallel binary computing.

## Feature
### 1. Weight-stationary dataflow
Ideally, *uSystolic-Sim* is open to any dataflow. But currently, it focuses on the weight-stationary dataflow, which enables low-cost and high-accuracy unary computing for a fair comparison with bianry computing.

### 2. Cycle-accurate trace generation
Assuming no stalls in the computing kernels, *uSystolic-Sim* generates __cycle-accurate__ SRAM traces and approximate DRAM traces.

### 3. Multi-cycle MAC execution
*uSystolic-Sim* offers per GEMM level configuration for MAC operations. The cycle count for a MAC operation is determined by the computing scheme in the kernels. For exmaple, with N-bit binary source data, unary computing, bit-seral and bit-parallel binary computing will spend 2^N, N and 1 cycles for one MAC operations, respectively.

### 4. Varying-bitwidth data
*uSystolic-Sim* provides per GEMM level configuration for the data bitwidth, and the bitwidth is N can be arbitrary, as required by the target application.

## Workflow
### 1. Architecture simulation - [archSim](https://github.com/diwu1990/uSystolic-Sim/blob/main/archSim/README.md)
All mandatory traces are generated to evaluate the latency and bandwidth for all GEMM operations, e.g., in deep neural networks.

### 2. Hardware simulation - [hwSim](https://github.com/diwu1990/uSystolic-Sim/blob/main/hwSim/README.md)
The traces file, latency and bandwidth numbers are further used to model the power and energy consumption of the systolic array with the a target computing scheme.