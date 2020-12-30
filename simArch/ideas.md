Mind you that this simulator is based on google's tpu while Eyeriss is from MIT/NVIDIA
# The processing element

## memory

Each PE can access/store data in:

* local register (scratchpad): 
* spatial flow (accessing data from a neighboring PE)
* Global memory

each has a corresponding latency

## operations
each PE is able to:

* load data from the its own register, neighbor PEs, global memory
* muliply data
* add data
* store data in its register, pass it to neighbor PEs, broadcast to global memory

## data
data can be either:

* input feature map (typically the largest)
* weights/filters (multiply element wise filter by input, add them up, save them as output, then moves in strides)
* output feature map (smaller than input, can get smaller with large stride or large filter)


# dataflow
Accelerator is composed of

* PEs arranged in a big array
* Global memory that is specified for output, input and filters(aka weights)

dataflow can be:
## Weight stationary: (reuse weights, load input)

* __weights__ are loaded once and stored in the __register__ different PEs
* __inputs__ are loaded from __global memory__ everytime
* after parallely multiplying, __psums__ are __spacially__ shared to neighbors for addition
