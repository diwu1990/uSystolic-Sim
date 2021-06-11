`ifndef _mul_border_
`define _mul_border_

`include "sobol8.sv"

module mul_border #(
    parameter WIDTH=8
) (
    input logic clk,
    input logic rst_n,
    input logic [WIDTH-1 : 0] i_data_i,
    input logic [WIDTH-1 : 0] i_data_w,
    output logic [WIDTH-1 : 0] randW,
    output logic [WIDTH-1 : 0] randW_inv,
    output logic o_bit,
    output logic i_bit_d
);

    logic [WIDTH-1 : 0] randI;
    logic bitI;
    logic bitI_inv;
    logic bitW;
    logic bitW_inv;

    
    sobol8 U_sobol_I(
        .clk(clk),
        .rst_n(rst_n),
        .enable(1'b1),
        .sobolSeq(randI)
    );

    assign bitI = i_data_i > randI;
    assign i_bit_d = bitI;
    assign bitI_inv = ~bitI;
    
    sobol8 U_sobol_W(
        .clk(clk),
        .rst_n(rst_n),
        .enable(bitI),
        .sobolSeq(randW)
    );

    sobol8 U_sobol_W_inv(
        .clk(clk),
        .rst_n(rst_n),
        .enable(bitI_inv),
        .sobolSeq(randW_inv)
    );

    assign bitW = i_data_w > randW;
    assign bitW_inv = i_data_w <= randW_inv;

    assign o_bit = (bitI & bitW) | (bitI_inv & bitW_inv);

endmodule

`endif