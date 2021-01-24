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
    input logic signed [WIDTH-1 : 0] sum_i,
    output logic signed [WIDTH-1 : 0] sum_o
);

    logic neg;
    assign neg = sign_i & sign_w;

    logic signed [WIDTH-1 : 0] prod;
    assign prod = prod_bit ? (neg ? -1 : 1) : 0;

    // this module is the horizontal buffer for control and data signals
    always_ff @(posedge clk or negedge rst_n) begin : acc_proc
        if (~rst_n) begin
            sum_o <= 0;
        end else begin
            if (clr) begin
                sum_o <= 0;
            end else begin
                if (en) begin
                    sum_o <= (acc ? sum_i : sum_o)  + prod;
                end else begin
                    sum_o <= sum_o;
                end
            end
        end
    end

endmodule