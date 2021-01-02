Configuration of GEMMs to run on systolic array hardware.

| Parameter     | Type   | Description |
| ------------- | ------ | ----------- |
| Layer name    | str    | Name of this GEMM layer |
| IFMAP Height  | int    | Height of input feature maps |
| IFMAP Width   | int    | Width of input feature maps |
| Filter Height | int    | Height of weight filters |
| Filter Width  | int    | Width of weight filters |
| Channels      | int    | Count of input channels |
| Num Filter    | int    | Count of output channels/filters |
| Stride H      | int    | Strides in the height dimension |
| Stride W      | int    | Strides in the width dimension |
| MAC Cycles    | int    | Count of cycles for a MAC operation |
