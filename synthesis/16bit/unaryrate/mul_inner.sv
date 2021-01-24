`include "sobol8.sv"

module mul_inner #(
    parameter WIDTH=16
) (
    input logic clk,
    input logic rst_n,
    input logic i_bit_i,
    input logic [WIDTH-2 : 0] i_data_w,
    output logic o_bit
);

    logic [WIDTH-1 : 0] randW;
    logic bitI;
    logic bitW;
    
    assign bitI = i_bit_i;

    sobol8 U_sobol_W(
        .clk(clk),
        .rst_n(rst_n),
        .enable(bitI),
        .sobolSeq(randW)
    );

    assign bitW = i_data_w > randW[WIDTH-1 : 1];

    assign o_bit = bitI & bitW;

endmodule