`include "sobol16.sv"

module mul_border #(
    parameter WIDTH=16
) (
    input logic clk,
    input logic rst_n,
    input logic init,
    input logic clr,
    input logic [WIDTH-2 : 0] i_data_i,
    input logic [WIDTH-2 : 0] i_data_w,
    output logic o_bit
);

    logic [WIDTH-2 : 0] cnt;
    logic [WIDTH-1 : 0] randW;
    logic bitI;
    logic bitW;
    
    always_ff @(posedge clk or negedge rst_n) begin : temporal
        if (~rst_n) begin
            cnt <= 0;
        end else begin
            if (init) begin
                cnt <= i_data_i;
            end else begin
                if (clr | ~bitI) begin
                    cnt <= 0;
                end else begin
                    cnt <= cnt - 1;
                end
            end
        end
    end

    assign bitI = ~(|cnt == 0);

    sobol16 U_sobol_W(
        .clk(clk),
        .rst_n(rst_n),
        .enable(bitI),
        .sobolSeq(randW)
    );

    assign bitW = i_data_w > randW[WIDTH-1 : 1];

    assign o_bit = bitI & bitW;

endmodule