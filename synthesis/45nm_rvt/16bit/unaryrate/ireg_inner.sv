module ireg_inner #(
    parameter WIDTH=1
) (
    input logic clk,
    input logic rst_n,
    input logic en,
    input logic clr,
    input logic i_data_sign,
    input logic i_data_dff,
    output logic o_data_sign,
    output logic o_data_dff
);

    // this module is the horizontal buffer for control and data signals
    always_ff @(posedge clk or negedge rst_n) begin : ireg_inner
        if (~rst_n) begin
            o_data_sign <= 0;
            o_data_dff <= 0;
        end else begin
            if (clr) begin
                o_data_sign <= 0;
                o_data_dff <= 0;
            end else begin
                if (en) begin
                    o_data_sign <= o_data_sign;
                    o_data_dff <= i_data_dff;
                end else begin
                    o_data_sign <= o_data_sign;
                    o_data_dff <= o_data_dff;
                end
            end
        end
    end

endmodule