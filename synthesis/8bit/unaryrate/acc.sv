module acc #(
    parameter WIDTH=32
) (
    input logic clk,
    input logic rst_n,
    input logic en,
    input logic clr,
    input logic acc,
    input logic sign_i,
    input logic sign_w,
    input logic prod_bit,
    input logic signed [WIDTH-1 : 0] i_data1,
    output logic signed [WIDTH-1 : 0] o_data
);

    logic neg;
    assign neg = sign_i & sign_w;

    logic signed [WIDTH-1 : 0] prod;
    assign prod = neg ? -1 : 1;

    // this module is the horizontal buffer for control and data signals
    always_ff @(posedge clk or negedge rst_n) begin : acc_proc
        if (~rst_n) begin
            o_data <= 0;
        end else begin
            if (clr) begin
                o_data <= 0;
            end else begin
                if (en) begin
                    if (acc) begin
                        o_data <= prod + i_data1;
                    end else begin
                        o_data <= o_data + prod;
                    end
                end else begin
                    o_data <= o_data;
                end
            end
        end
    end

endmodule