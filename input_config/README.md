Configuration of systolic array hardware.

| Parameter     | Description |
| ------------- | ----------- |
| run_name      | Name of this run, specifying the name of the ouput dir in root/output folder |
| ArrayHeight   | Row count of stystolic array |
| ArrayWidth    | Column count of stystolic array |
| IfmapSramSz   | IFMAP SRAM size in KB |
| FilterSramSz  | FILTER SRAM size in KB |
| OfmapSramSz   | OFMAP SRAM size in KB |
| IfmapOffset   | IFMAP start address in word granularity |
| FilterOffset  | FILTER start address in word granularity |
| OfmapOffset   | OFMAP start address in word granularity |
| Dataflow      | Dataflow, currently use "ws" for weight stationary |
| WordByte      | Byte count for a data word |
| MACCycle      | Cycle count for a MAC operation |
| WeightBwOpt   | Weight bandwidth optimization flag (Bool type) |
