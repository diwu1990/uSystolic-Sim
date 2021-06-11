`ifndef _acc_
`define _acc_

module acc #(
    parameter WIDTH=24
) (
    input logic clk,
    input logic rst_n,
    input logic en,
    input logic clr,
    input logic mac_done,
    input logic prod_bit,
    input logic [WIDTH-1 : 0] sum_i,
    output logic [WIDTH-1 : 0] sum_o
);

    logic signed [WIDTH-1 : 0] prod;
    assign prod = prod_bit ? 1 : 0;

    // this module is the horizontal buffer for control and data signals
    always_ff @(posedge clk or negedge rst_n) begin : mac_done_proc
        if (~rst_n) begin
            sum_o <= 0;
        end else begin
            if (clr) begin
                sum_o <= 0;
            end else begin
                if (en) begin
                    sum_o <= (mac_done ? sum_i : prod)  + sum_o;
                end else begin
                    sum_o <= sum_o;
                end
            end
        end
    end

endmodule

`endif