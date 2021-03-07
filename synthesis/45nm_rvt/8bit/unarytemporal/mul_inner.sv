`include "sobol8.sv"

module mul_inner #(
    parameter WIDTH=8
) (
    input logic clk,
    input logic rst_n,
    input logic i_bit_i,
    input logic [WIDTH-2 : 0] i_data_w,
    input logic [WIDTH-2 : 0] i_randW,
    input logic [WIDTH-2 : 0] o_randW,
    output logic o_bit
);

    logic bitI;
    logic bitW;
    
    assign bitI = i_bit_i;

    assign bitW = i_data_w > o_randW;

    assign o_bit = bitI & bitW;

    always_ff @(posedge clk) begin : buf_randW
        o_randW <= i_randW;
    end

endmodule