`include "sobol16.sv"

module mul_border #(
    parameter WIDTH=16
) (
    input logic clk,
    input logic rst_n,
    input logic [WIDTH-2 : 0] i_data_i,
    input logic [WIDTH-2 : 0] i_data_w,
    output logic o_bit
);

    logic [WIDTH-1 : 0] randI;
    logic [WIDTH-1 : 0] randW;
    logic bitI;
    logic bitW;
    
    sobol16 U_sobol_I(
        .clk(clk),
        .rst_n(rst_n),
        .enable(1'b1),
        .sobolSeq(randI)
    );

    assign bitI = i_data_i > randI[WIDTH-1 : 1];

    sobol16 U_sobol_W(
        .clk(clk),
        .rst_n(rst_n),
        .enable(bitI),
        .sobolSeq(randW)
    );

    assign bitW = i_data_w > randW[WIDTH-1 : 1];

    assign o_bit = bitI & bitW;

endmodule