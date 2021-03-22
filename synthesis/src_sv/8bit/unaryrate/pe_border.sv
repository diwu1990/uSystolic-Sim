`ifndef _pe_border_
`define _pe_border_

`include "ireg_border.sv"
`include "wreg.sv"
`include "mul_border.sv"
`include "acc.sv"

module pe_border #(
    parameter IWIDTH=8,
    parameter OWIDTH=16
) (
    input logic clk,
    input logic rst_n,
    input logic mac_done,
    input logic en_i,
    input logic clr_i,
    input logic en_w,
    input logic clr_w,
    input logic en_o,
    input logic clr_o,
    input logic signed [IWIDTH-1 : 0] ifm,
    input logic wght_sign,
    input logic [IWIDTH-2 : 0] wght_abs,
    input logic signed [OWIDTH-1 : 0] ofm,
    output logic mac_done_d,
    output logic en_i_d,
    output logic clr_i_d,
    output logic en_w_d,
    output logic clr_w_d,
    output logic en_o_d,
    output logic clr_o_d,
    output logic ifm_sign_d,
    output logic [IWIDTH-2 : 0] ifm_dff_d,
    output logic wght_sign_d,
    output logic [IWIDTH-2 : 0] randW_d,
    output logic [IWIDTH-2 : 0] wght_abs_d,
    output logic signed [OWIDTH-1 : 0] ofm_d
);

    logic [IWIDTH-2 : 0] ifm_abs_d;

    ireg_border #(
        .WIDTH(IWIDTH)
    ) U_ireg_border (
        .clk(clk),
        .rst_n(rst_n),
        .en(en_i),
        .clr(clr_i),
        .i_data(ifm),
        .o_data_sign(ifm_sign_d),
        .o_data_abs(ifm_abs_d)
    );

    wreg #(
        .WIDTH(IWIDTH)
    ) U_wreg (
        .clk(clk),
        .rst_n(rst_n),
        .en(en_w),
        .clr(clr_w),
        .i_data_sign(wght_sign),
        .i_data_abs(wght_abs),
        .o_data_sign(wght_sign_d),
        .o_data_abs(wght_abs_d)
    );

    mul_border #(
        .WIDTH(IWIDTH)
    ) U_mul_border(
        .clk(clk),
        .rst_n(rst_n),
        .i_data_i(ifm_abs_d),
        .i_data_w(wght_abs_d),
        .randW(randW_d),
        .o_bit(ifm_dff_d)
    );

    acc #(
        .WIDTH(OWIDTH)
    ) U_acc(
        .clk(clk),
        .rst_n(rst_n),
        .en(en_o),
        .clr(clr_o),
        .mac_done(mac_done_d),
        .sign_i(ifm_sign_d),
        .sign_w(wght_sign_d),
        .prod_bit(ifm_dff_d),
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