`ifndef _mul_border_
`define _mul_border_

module mul_border #(
    parameter WIDTH=8
    parameter DEPTH=3
) (
    input logic clk,
    input logic rst_n,
    input logic en,
    input logic clr,
    input logic signed [WIDTH-1 : 0] i_data0,
    input logic signed [WIDTH-1 : 0] i_data1,
    output logic [DEPTH-1 : 0] idx,
    output logic signed [WIDTH*2-1 : 0] o_data
);

    always_ff @(posedge clk or negedge rst_n) begin : idx_0
        if (~rst_n) begin
            idx <= 0;
        end else begin
            if (clr) begin
                idx <= 0;
            end else begin
                idx <= idx + en;
            end
        end
    end
    
    assign o_data = (i_data0[idx] ? i_data1 : 0);
    
endmodule

`endif