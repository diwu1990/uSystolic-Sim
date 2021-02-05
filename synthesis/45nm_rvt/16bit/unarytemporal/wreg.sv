module wreg #(
    parameter WIDTH=16
) (
    input logic clk,
    input logic rst_n,
    input logic en,
    input logic clr,
    input logic signed [WIDTH-1 : 0] i_data,
    output logic o_data_sign,
    output logic [WIDTH-2 : 0] o_data_abs
);
    
    logic signed [WIDTH-1 : 0] o_data;
    logic signed [WIDTH-1 : 0] o_data_neg;

    // this module is the horizontal buffer for control and data signals
    always_ff @(posedge clk or negedge rst_n) begin : ireg_border
        if (~rst_n) begin
            o_data <= 0;
        end else begin
            if (clr) begin
                o_data <= 0;
            end else begin
                if (en) begin
                    o_data <= i_data;
                end else begin
                    o_data <= o_data;
                end
            end
        end
    end

    assign o_data_neg = -o_data;
    assign o_data_sign = o_data[WIDTH-1];
    assign o_data_abs = o_data_sign ? o_data_neg[WIDTH-2 : 0] : o_data[WIDTH-2 : 0];

endmodule