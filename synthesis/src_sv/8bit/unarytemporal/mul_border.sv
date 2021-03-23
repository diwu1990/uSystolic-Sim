`ifndef _mul_border_
`define _mul_border_

`include "sobol8.sv"

module mul_border #(
    parameter WIDTH=8
) (
    input logic clk,
    input logic rst_n,
    input logic init,
    input logic clr,
    input logic [WIDTH-2 : 0] i_data_i,
    input logic [WIDTH-2 : 0] i_data_w,
    output logic [WIDTH-2 : 0] randW,
    output logic o_bit,
    output logic i_bit_d
);

    logic [WIDTH-2 : 0] cnt;
    logic [WIDTH-1 : 0] randW_all;
    logic bitI;
    logic bitW;
    
    always_ff @(posedge clk or negedge rst_n) begin : temporal
        if (~rst_n) begin
            cnt <= 0;
        end else begin
            if (init) begin
                cnt <= i_data_i;
            end else begin
                if (clr | ~bitI) begin
                    cnt <= 0;
                end else begin
                    cnt <= cnt - 1;
                end
            end
        end
    end

    assign bitI = ~(|cnt == 0);
    assign i_bit_d = bitI;

    sobol8 U_sobol_W(
        .clk(clk),
        .rst_n(rst_n),
        .enable(bitI),
        .sobolSeq(randW_all)
    );

    assign randW = randW_all[WIDTH-1 : 1];
    
    assign bitW = i_data_w > randW;

    assign o_bit = bitI & bitW;

endmodule

`endif