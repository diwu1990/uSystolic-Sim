Configuration of systolic array hardware.

Example config:

[general]
run_name = "MLPERF_AlphaGoZero_32x32_ws"  <p style='text-align: right;'> name for the ouptut folder </p>

[architecture_presets]
ArrayHeight:    32
ArrayWidth:     32
IfmapSramSz:    512
FilterSramSz:   512
OfmapSramSz:    256
IfmapOffset:    0
FilterOffset:   10000000
OfmapOffset:    20000000
Dataflow:       ws
WordByte:       1
MACCycle:       1
WeightBwOpt:    False