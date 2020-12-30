from simArch import sram_traffic_ws
from simArch import sram_traffic_ws_usystolic
import os
import time

dimension_rows=32 # row size of systolic array
dimension_cols=32 # column size of systolic array
ifmap_h=224 # input feature map height
ifmap_w=224 # input feature map width
filt_h=11 # weight height
filt_w=11 # weight width
num_channels=3 # input channel count
strides=11 # stride, assuming identical in row and column dimension
num_filt=8 # filter count, also output channel count
ifmap_base=0 # input feature map base addr
filt_base=1000000 # weight base addr
ofmap_base=2000000 # output feature map base addr
mac_cycles=1 # cycle count per mul
wgt_bw_opt=False # optimize the bandwidth of input and output to match that of weight


print()
if os.path.exists("sram_read_ws_usystolic_opt.csv"):
  os.remove("sram_read_ws_usystolic_opt.csv")
else:
  print("sram_read_ws_usystolic_opt.csv does not exist")

if os.path.exists("sram_write_ws_usystolic_opt.csv"):
  os.remove("sram_write_ws_usystolic_opt.csv")
else:
  print("sram_write_ws_usystolic_opt.csv does not exist")

start = time.time()
cycle, util = sram_traffic_ws_usystolic.sram_traffic(
        dimension_rows=dimension_rows, # row size of systolic array
        dimension_cols=dimension_cols, # column size of systolic array
        ifmap_h=ifmap_h, # input feature map height
        ifmap_w=ifmap_w, # input feature map width
        filt_h=filt_h, # weight height
        filt_w=filt_w, # weight width
        num_channels=num_channels, # input channel count
        stride_h=strides, # stride, assuming identical in row and column dimension
        stride_w=strides, # stride, assuming identical in row and column dimension
        num_filt=num_filt, # filter count, also output channel count
        ofmap_base=ofmap_base, # output feature map base addr
        filt_base=filt_base, # weight base addr
        ifmap_base=ifmap_base, # input feature map base addr
        mac_cycles=mac_cycles, # cycle count per mul
        wgt_bw_opt=True, # optimize the bandwidth of input and output to match that of weight
        sram_read_trace_file="sram_read_ws_usystolic_opt.csv",
        sram_write_trace_file="sram_write_ws_usystolic_opt.csv")
end = time.time()
print("run time: ", end - start, " sec")
print(cycle, " cycles", util, "% MAC utilization")


print()
if os.path.exists("sram_read_ws_usystolic_no_opt.csv"):
  os.remove("sram_read_ws_usystolic_no_opt.csv")
else:
  print("sram_read_ws_usystolic_no_opt.csv does not exist")

if os.path.exists("sram_write_ws_usystolic_no_opt.csv"):
  os.remove("sram_write_ws_usystolic_no_opt.csv")
else:
  print("sram_write_ws_usystolic_no_opt.csv does not exist")

start = time.time()
cycle, util = sram_traffic_ws_usystolic.sram_traffic(
        dimension_rows=dimension_rows, # row size of systolic array
        dimension_cols=dimension_cols, # column size of systolic array
        ifmap_h=ifmap_h, # input feature map height
        ifmap_w=ifmap_w, # input feature map width
        filt_h=filt_h, # weight height
        filt_w=filt_w, # weight width
        num_channels=num_channels, # input channel count
        stride_h=strides, # stride, assuming identical in row and column dimension
        stride_w=strides, # stride, assuming identical in row and column dimension
        num_filt=num_filt, # filter count, also output channel count
        ofmap_base=ofmap_base, # output feature map base addr
        filt_base=filt_base, # weight base addr
        ifmap_base=ifmap_base, # input feature map base addr
        mac_cycles=mac_cycles, # cycle count per mul
        wgt_bw_opt=False, # optimize the bandwidth of input and output to match that of weight
        sram_read_trace_file="sram_read_ws_usystolic_no_opt.csv",
        sram_write_trace_file="sram_write_ws_usystolic_no_opt.csv")
end = time.time()
print("run time: ", end - start, " sec")
print(cycle, " cycles", util, "% MAC utilization")

print()
if os.path.exists("sram_read_ws.csv"):
  os.remove("sram_read_ws.csv")
else:
  print("sram_read_ws.csv does not exist")

if os.path.exists("sram_write_ws.csv"):
  os.remove("sram_write_ws.csv")
else:
  print("sram_write_ws.csv does not exist")

start = time.time()
cycle, util = sram_traffic_ws.sram_traffic(
        dimension_rows=dimension_rows, # row size of systolic array
        dimension_cols=dimension_cols, # column size of systolic array
        ifmap_h=ifmap_h, # input feature map height
        ifmap_w=ifmap_w, # input feature map width
        filt_h=filt_h, # weight height
        filt_w=filt_w, # weight width
        num_channels=num_channels, # input channel count
        strides=strides, # stride, assuming identical in row and column dimension
        num_filt=num_filt, # filter count, also output channel count
        ofmap_base=ofmap_base, # output feature map base addr
        filt_base=filt_base, # weight base addr
        ifmap_base=ifmap_base, # input feature map base addr
        sram_read_trace_file="sram_read_ws.csv",
        sram_write_trace_file="sram_write_ws.csv")
end = time.time()
print("run time: ", end - start, " sec")
print(cycle, " cycles", util, "% MAC utilization")
