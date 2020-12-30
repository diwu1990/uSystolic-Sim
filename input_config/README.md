Configuration of systolic array hardware.

| Parameter     | Description |
| ------------- | ----------- |
| run_name      | Name of this run, specifying the name of the ouput dir in root/output folder (str type) |
| ArrayHeight   | Count of rows for the stystolic array (int type) |
| ArrayWidth    | Count of columns for the stystolic array (int type) |
| IfmapSramSz   | SRAM size in KB for input feature maps (float type) |
| FilterSramSz  | SRAM size in KB for weight filters (float type) |
| OfmapSramSz   | SRAM size in KB for output feature maps (int type) |
| IfmapOffset   | Start address in word granularity for input feature maps (int type) |
| FilterOffset  | Start address in word granularity for weight filters (int type) |
| OfmapOffset   | Start address in word granularity for output feature maps (int type) |
| Dataflow      | Dataflow, currently use "ws" for weight stationary (str type) |
| WordByte      | Count of bytes for a data word (float type) |
| MACCycle      | Count of cycles for a MAC operation (int type) |
| WeightBwOpt   | Weight bandwidth optimization flag (bool type) |
