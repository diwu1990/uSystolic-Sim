Configuration of systolic array hardware.

| Parameter     | Type   | Description |
| ------------- | ------ | ----------- |
| run_name      | str    | Specifying the folder name in root/output |
| ArrayHeight   | int    | Count of rows for the stystolic array |
| ArrayWidth    | int    | Count of columns for the stystolic array |
| IfmapSramSz   | float  | SRAM size in KB for input feature maps |
| FilterSramSz  | float  | SRAM size in KB for weight filters |
| OfmapSramSz   | float  | SRAM size in KB for output feature maps |
| IfmapOffset   | int    | Start address in word granularity for input feature maps |
| FilterOffset  | int    | Start address in word granularity for weight filters |
| OfmapOffset   | int    | Start address in word granularity for output feature maps |
| Dataflow      | str    | Dataflow, currently use "ws" for weight stationary |
| WordByte      | float  | Count of bytes for a data word |
| WeightBwOpt   | bool   | Weight bandwidth optimization flag |
| Computing     | str    | Applied computing scheme |
| ZeroIfmapSram | bool   | IFMAP SRAM existence flag |
| ZeroFilterSram| bool   | Weight SRAM existence flag |
| ZeroOfmapSram | bool   | OFMAP SRAM existence flag |
| SramAccBuf    | bool   | SRAM access buffer existence flag |
