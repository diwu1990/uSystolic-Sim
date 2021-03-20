`ifndef _mul_border_
`define _mul_border_

module mul_border #(
    parameter WIDTH=8
) (
    input logic signed [WIDTH-1 : 0] i_data0,
    input logic signed [WIDTH-1 : 0] i_data1,
    output logic signed [WIDTH*2-1 : 0] o_data
);

    assign o_data = i_data0 * i_data1;
    
endmodule

`endif