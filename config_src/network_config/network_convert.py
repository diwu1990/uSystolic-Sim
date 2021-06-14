def convert_network_config(src_file="network.csv", dst_file="network_new.csv"):
    i_file = open(src_file, 'r')
    o_file = open(dst_file, 'w')

    row_idx = 0
    first = True
    for row in i_file:
        row_idx += 1
        # per layer trace gen
        if first:
            # skip the header row
            first = False
            o_file.write("Layer name, Layer Type, IFMAP Height, IFMAP Width, Filter Height, Filter Width, Channels, Num Filter, Stride H, Stride W, MAC Cycles,\n")
            continue
            
        elems = row.strip().split(',')
        elems = prune(elems)

        # skip row if unrecognized
        if len(elems) != 8:
            o_file.write(row)
            continue
        else:
            dst_str = elems[0] + "_" + str(row_idx-1) + ",\t" + \
                        "GEMM" + ",\t" + \
                        elems[1] + ",\t" + \
                        elems[2] + ",\t" + \
                        elems[3] + ",\t" + \
                        elems[4] + ",\t" + \
                        elems[5] + ",\t" + \
                        elems[6] + ",\t" + \
                        elems[7] + ",\t" + \
                        elems[7] + ",\t" + \
                        "32,\t\n"
            o_file.write(dst_str)
    
    i_file.close()
    o_file.close()


def prune(input_list):
    l = []

    for e in input_list:
        e = e.strip() # remove the leading and trailing characters, here space
        if e != '' and e != ' ':
            l.append(e)

    return l


if __name__ == '__main__':
    src_file = "/mnt/ssd1/Project/uSystolic-Sim/config_src/network_config/gemm_config_from_scalesim/mlperf/MLPERF.csv"
    dst_file = "./mlperf/network.csv"
    convert_network_config(src_file, dst_file)
