`ifndef _mul_inner_
`define _mul_inner_

module mul_inner #(
    parameter WIDTH=16
) (
    input logic clk,
    input logic rst_n,
    input logic i_bit_i,
    input logic [WIDTH-1 : 0] i_data_w,
    input logic [WIDTH-1 : 0] i_randW,
    input logic [WIDTH-1 : 0] i_randW_inv,
    output logic [WIDTH-1 : 0] o_randW,
    output logic [WIDTH-1 : 0] o_randW_inv,
    output logic o_bit
);

    logic bitI;
    logic bitW;
    logic bitW_inv;
    
    assign bitI = i_bit_i;
    assign bitI_inv = ~bitI;

    assign bitW = i_data_w > o_randW;
    assign bitW_inv = i_data_w <= o_randW_inv;

    assign o_bit = bitI & bitW;

    always_ff @(posedge clk) begin : buf_randW
        o_randW <= i_randW;
        o_randW_inv <= i_randW_inv;
    end

    assign o_bit = (bitI & bitW) | (bitI_inv & bitW_inv);

endmodule

`endif