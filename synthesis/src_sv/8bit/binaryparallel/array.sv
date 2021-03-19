`include "pe_border.sv"
`include "pe_inner.sv"

module array #(
    parameter HEIGHT=12,
    parameter WIDTH=14,
    parameter IWIDTH=8,
    parameter OWIDTH=24
) (
    input logic clk,
    input logic rst_n,
    input logic [HEIGHT-1 : 0] en_i,
    input logic [HEIGHT-1 : 0] clr_i,
    input logic [WIDTH-1 : 0] en_w,
    input logic [WIDTH-1 : 0] clr_w,
    input logic [WIDTH-1 : 0] en_o,
    input logic [WIDTH-1 : 0] clr_o,
    input logic signed [HEIGHT-1 : 0] ifm [IWIDTH-1 : 0],
    input logic signed [WIDTH-1 : 0] wght [IWIDTH-1 : 0],
    output logic signed [WIDTH-1 : 0] ofm [OWIDTH-1 : 0]
);

    logic [HEIGHT-1 : 0] en_i_x [WIDTH-1 : 0];
    logic [HEIGHT-1 : 0] clr_i_x [WIDTH-1 : 0];
    logic [WIDTH-1 : 0] en_w_x [HEIGHT-1 : 0];
    logic [WIDTH-1 : 0] clr_w_x [HEIGHT-1 : 0];
    logic [WIDTH-1 : 0] en_o_x [HEIGHT-1 : 0];
    logic [WIDTH-1 : 0] clr_o_x [HEIGHT-1 : 0];

    logic signed [HEIGHT-1 : 0][WIDTH-1 : 0] ifm_x [IWIDTH-1 : 0];
    logic signed [WIDTH-1 : 0][HEIGHT-1 : 0] wght_x [IWIDTH-1 : 0];
    logic signed [WIDTH-1 : 0][HEIGHT-1 : 0] ofm_x [OWIDTH-1 : 0];

    genvar h, w;
    generate
        for (h = 0; h < HEIGHT; h++) begin
            pe_border #(
                IWIDTH=IWIDTH,
                OWIDTH=OWIDTH
            ) U_pe_border (
                .clk(clk),
                .rst_n(rst_n),
                .en_i(),
                .clr_i(),
                .en_w(),
                .clr_w(),
                .en_o(),
                .clr_o(),
                .ifm(),
                .wght(),
                .ofm(),
                .ifm_d(),
                .wght_d(),
                .ofm_d()
            );
            for (w = 1; w < WIDTH; w++) begin
                
            end
        end
    endgenerate

endmodule