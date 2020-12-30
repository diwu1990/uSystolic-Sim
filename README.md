# uSystolic-Sim
*uSystolic-Sim* is a systolic array simulator, which generates cycle-accurate traces to evaluate 
1) the latency for GEMM execution
2) the bandwidth for memory accesses
3) the power and energy consumption, including both computing kernels and memory hierarchies

*uSystolic-Sim* is not developed to support general systolic array simulations as [SCALE-Sim](https://github.com/ARM-software/SCALE-Sim) by ARM.


*uSystolic-Sim* is aware of the computing scheme, including [unary computing](https://conferences.computer.org/isca/pdfs/ISCA2020-4QlDegUf3fKiwUXfV0KdCm/466100a377/466100a377.pdf), bit-serial binary computing and bit-parallel binary computing.

## uSystolic-Sim Features
### weight-stationary dataflow
### cycle-accurate trace generation
### multi-cycle MAC execution
### varying-byte data word

## uSystolic-Sim Components
### archSim - architecture simulation

### hwSim - hardware simulation