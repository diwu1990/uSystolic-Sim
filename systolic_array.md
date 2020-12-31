# Systolic array

## Processing Element

Each PE can access/store data in following types of memories with a corresponding latency:
* local register (scratchpad): 
* spatial flow (accessing data from a neighboring PE)
* Global memory (limited access to outmost PEs)

Each PE is able to:

* load data from the its own register, neighbor PEs, global memory
* muliply data
* add data
* store data in its register, pass it to neighbor PEs, broadcast to global memory

## Dataflow
Data in systolic array can be either:

* input feature map (typically the largest)
* weight filters (multiply element wise filter by input, add them up, save them as output, then moves in strides)
* output feature map (smaller than input, can get smaller with large stride or large filter)

PEs arranged in a big array, and global memory that is specified for output, input and filters (aka weights)

Athe weight stationary dataflow can reuse weights during loading inputs:

* __weights__ are loaded once and stored in the __register__ different PEs
* __inputs__ are loaded from __global memory__ everytime
* after parallely multiplying, __psums__ are __spacially__ shared to neighbors for addition
