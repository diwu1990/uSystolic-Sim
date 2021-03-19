module acc #(
    parameter WIDTH=16
) (
    input logic clk,
    input logic rst_n,
    input logic en,
    input logic clr,
    input logic mac_done,
    input logic sign_i,
    input logic sign_w,
    input logic prod_bit,
    input logic signed [WIDTH-1 : 0] sum_i,
    output logic signed [WIDTH-1 : 0] sum_o
);

    logic neg;
    assign neg = sign_i ^ sign_w;

    logic signed [WIDTH-1 : 0] prod;
    assign prod = prod_bit ? (neg ? -1 : 1) : 0;

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