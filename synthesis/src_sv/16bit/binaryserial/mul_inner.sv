`ifndef _mul_inner_
`define _mul_inner_

module mul_inner #(
    parameter WIDTH=16,
    parameter DEPTH=4
) (
    input logic clk,
    input logic rst_n,
    input logic en,
    input logic clr,
    input logic [DEPTH-1 : 0] i_idx,
    input logic signed [WIDTH-1 : 0] i_data0,
    input logic signed [WIDTH-1 : 0] i_data1,
    output logic [DEPTH-1 : 0] o_idx,
    output logic signed [WIDTH*2-1 : 0] o_data
);

    always_ff @(posedge clk or negedge rst_n) begin : o_idx_0
        if (~rst_n) begin
            o_idx <= 0;
        end else begin
            if (clr) begin
                o_idx <= 0;
            end else begin
                o_idx <= en ? i_idx : o_idx;
            end
        end
    end

    assign o_data = (i_data0[o_idx] ? i_data1 : 0);
    
endmodule

`endif