`ifndef _wreg_
`define _wreg_

module wreg #(
    parameter WIDTH=16
) (
    input logic clk,
    input logic rst_n,
    input logic en,
    input logic clr,
    input logic i_data_sign,
    input logic [WIDTH-2 : 0] i_data_abs,
    output logic o_data_sign,
    output logic [WIDTH-2 : 0] o_data_abs
);
    
    // this module is the horizontal buffer for control and data signals
    always_ff @(posedge clk or negedge rst_n) begin : wreg
        if (~rst_n) begin
            o_data_sign <= 0;
            o_data_abs <= 0;
        end else begin
            if (clr) begin
                o_data_sign <= 0;
                o_data_abs <= 0;
            end else begin
                if (en) begin
                    o_data_sign <= i_data_sign;
                    o_data_abs <= i_data_abs;
                end else begin
                    o_data_sign <= o_data_sign;
                    o_data_abs <= o_data_abs;
                end
            end
        end
    end

endmodule

`endif