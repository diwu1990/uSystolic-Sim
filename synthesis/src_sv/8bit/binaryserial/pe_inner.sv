`ifndef _pe_inner_
`define _pe_inner_

`include "ireg_inner.sv"
`include "wreg.sv"
`include "mul_inner.sv"
`include "acc.sv"

module pe_inner #(
    parameter IWIDTH=8,
    parameter IDEPTH=3,
    parameter OWIDTH=24
) (
    input logic clk,
    input logic rst_n,
    input logic [IDEPTH-1 : 0] idx,
    input logic mac_done,
    input logic en_i,
    input logic clr_i,
    input logic en_w,
    input logic clr_w,
    input logic en_o,
    input logic clr_o,
    input logic signed [IWIDTH-1 : 0] ifm,
    input logic signed [IWIDTH-1 : 0] wght,
    input logic signed [OWIDTH-1 : 0] ofm,
    output logic [IDEPTH-1 : 0] idx_d,
    output logic mac_done_d,
    output logic en_i_d,
    output logic clr_i_d,
    output logic en_w_d,
    output logic clr_w_d,
    output logic en_o_d,
    output logic clr_o_d,
    output logic signed [IWIDTH-1 : 0] ifm_d,
    output logic signed [IWIDTH-1 : 0] wght_d,
    output logic signed [OWIDTH-1 : 0] ofm_d
);

    logic signed [IWIDTH-1 : 0] prod;

    ireg_inner #(
        .WIDTH(IWIDTH)
    ) U_ireg_inner (
        .clk(clk),
        .rst_n(rst_n),
        .en(en_i),
        .clr(clr_i),
        .i_data(ifm),
        .o_data(ifm_d)
    );

    wreg #(
        .WIDTH(IWIDTH)
    ) U_wreg (
        .clk(clk),
        .rst_n(rst_n),
        .en(en_w),
        .clr(clr_w),
        .i_data(wght),
        .o_data(wght_d)
    );

    mul_inner #(
        .WIDTH(IWIDTH),
        .DEPTH(IDEPTH)
    ) U_mul_inner(
        .clk(clk),
        .rst_n(rst_n),
        .en(1'b1),
        .clr(1'b0),
        .i_idx(idx),
        .i_data0(ifm_d),
        .i_data1(wght_d),
        .o_idx(idx_d),
        .o_data(prod)
    );

    acc #(
        .WIDTH(OWIDTH)
    ) U_acc(
        .clk(clk),
        .rst_n(rst_n),
        .en(en_o),
        .clr(clr_o),
        .mac_done(mac_done_d),
        .prod({{(OWIDTH-IWIDTH){prod[IWIDTH-1]}}, prod}),
        .sum_i(ofm),
        .sum_o(ofm_d)
    );

    always_ff @( posedge clk ) begin : en_clr
        en_i_d <= en_i;
        en_w_d <= en_w;
        en_o_d <= en_o;
        clr_i_d <= clr_i;
        clr_w_d <= clr_w;
        clr_o_d <= clr_o;
        mac_done_d <= mac_done;
    end

endmodule

`endif