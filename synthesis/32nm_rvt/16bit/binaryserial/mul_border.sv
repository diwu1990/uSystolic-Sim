module mul_border #(
    parameter WIDTH=16
    parameter DEPTH=4
) (
    input logic clk,
    input logic rst_n,
    input logic clr,
    input logic signed [WIDTH-1 : 0] i_data0,
    input logic signed [WIDTH-1 : 0] i_data1,
    output logic signed [WIDTH*2-1 : 0] o_data
);

    logic [DEPTH-1 : 0] cnt;

    always_ff @(posedge clk or negedge rst_n) begin : cnt_0
        if (~rst_n) begin
            cnt <= 0;
        end else begin
            if (clr) begin
                cnt <= 0;
            end else begin
                cnt <= cnt + 1;
            end
        end
    end
    
    assign o_data = (i_data0[cnt] ? i_data1 : 0);
    
endmodule