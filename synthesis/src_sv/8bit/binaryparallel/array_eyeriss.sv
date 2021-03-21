`ifndef _array_eyeriss_
`define _array_eyeriss_

`include "pe_border.sv"
`include "pe_inner.sv"

module array_eyeriss #(
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
    input logic signed [IWIDTH-1 : 0] ifm [HEIGHT-1 : 0],
    input logic signed [IWIDTH-1 : 0] wght [WIDTH-1 : 0],
    output logic signed [OWIDTH-1 : 0] ofm [WIDTH-1 : 0]
);

    logic [WIDTH : 0] en_i_x [HEIGHT-1 : 0];
    logic [WIDTH : 0] clr_i_x [HEIGHT-1 : 0];
    logic [HEIGHT : 0] en_w_x [WIDTH-1 : 0];
    logic [HEIGHT : 0] clr_w_x [WIDTH-1 : 0];
    logic [HEIGHT : 0] en_o_x [WIDTH-1 : 0];
    logic [HEIGHT : 0] clr_o_x [WIDTH-1 : 0];

    logic signed [IWIDTH-1 : 0] ifm_x [HEIGHT-1 : 0][WIDTH : 0];
    logic signed [IWIDTH-1 : 0] wght_x [WIDTH-1 : 0][HEIGHT : 0];
    logic signed [OWIDTH-1 : 0] ofm_x [WIDTH-1 : 0][HEIGHT : 0];

    genvar h;
    generate
        for (h = 0; h < HEIGHT; h++) begin
            assign en_i_x[h][0] = en_i[h];
            assign clr_i_x[h][0] = clr_i[h];
            assign ifm_x[h][0] = ifm[h];
        end
    endgenerate

    genvar w;
    generate
        for (w = 0; w < WIDTH; w++) begin
            assign en_w_x[w][0] = en_w[w];
            assign clr_w_x[w][0] = clr_w[w];
            assign wght_x[w][0] = wght[w];

            assign en_o_x[w][HEIGHT] = en_o[w];
            assign clr_o_x[w][HEIGHT] = clr_o[w];
            assign ofm[w] = ofm_x[w][0];
            assign ofm_x[w][HEIGHT] = 0;
        end
    endgenerate

    genvar h, w;
    generate
        for (h = 0; h < HEIGHT; h++) begin
            pe_border #(
                .IWIDTH(IWIDTH),
                .OWIDTH(OWIDTH)
            ) U_pe_border (
                .clk(clk),
                .rst_n(rst_n),
                
                .en_i(en_i_x[h][0]),
                .clr_i(clr_i_x[h][0]),
                .ifm(ifm_x[h][0]),
                .en_i_d(en_i_x[h][1]),
                .clr_i_d(clr_i_x[h][1]),
                .ifm_d(ifm_x[h][1]),
                
                .en_w(en_w_x[0][h]),
                .clr_w(clr_w_x[0][h]),
                .wght(wght_x[0][h]),
                .en_w_d(en_w_x[0][h+1]),
                .clr_w_d(clr_w_x[0][h+1]),
                .wght_d(wght_x[0][h+1]),

                .en_o(en_o_x[0][h+1]),
                .clr_o(clr_o_x[0][h+1]),
                .ofm(ofm_x[0][h+1]),
                .en_o_d(en_o_x[0][h]),
                .clr_o_d(clr_o_x[0][h]),
                .ofm_d(ofm_x[0][h])
            );
            for (w = 1; w < WIDTH; w++) begin
                pe_inner #(
                    .IWIDTH(IWIDTH),
                    .OWIDTH(OWIDTH)
                ) U_pe_inner (
                    .clk(clk),
                    .rst_n(rst_n),

                    .en_i(en_i_x[h][w]),
                    .clr_i(clr_i_x[h][w]),
                    .ifm(ifm_x[h][w]),
                    .en_i_d(en_i_x[h][w+1]),
                    .clr_i_d(clr_i_x[h][w+1]),
                    .ifm_d(ifm_x[h][w+1]),

                    .en_w(en_w_x[w][h]),
                    .clr_w(clr_w_x[w][h]),
                    .wght(wght_x[w][h]),
                    .en_w_d(en_w_x[w][h+1]),
                    .clr_w_d(clr_w_x[w][h+1]),
                    .wght_d(wght_x[w][h+1]),
                    
                    .en_o(en_o_x[w][h+1]),
                    .clr_o(clr_o_x[w][h+1]),
                    .ofm(ofm_x[w][h+1]),
                    .en_o_d(en_o_x[w][h]),
                    .clr_o_d(clr_o_x[w][h]),
                    .ofm_d(ofm_x[w][h])
                );
            end
        end
    endgenerate

endmodule

`endif