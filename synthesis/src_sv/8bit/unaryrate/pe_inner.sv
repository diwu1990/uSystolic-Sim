`ifndef _pe_inner_
`define _pe_inner_

`include "ireg_inner.sv"
`include "wreg.sv"
`include "mul_inner.sv"
`include "acc.sv"

module pe_inner #(
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
    input logic ifm_sign,
    input logic ifm_dff,
    input logic wght_sign,
    input logic [IWIDTH-2 : 0] randW,
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
    output logic ifm_dff_d,
    output logic wght_sign_d,
    output logic [IWIDTH-2 : 0] randW_d,
    output logic [IWIDTH-2 : 0] wght_abs_d,
    output logic signed [OWIDTH-1 : 0] ofm_d
);

    logic prod;

    ireg_inner U_ireg_inner (
        .clk(clk),
        .rst_n(rst_n),
        .en(en_i),
        .clr(clr_i),
        .i_data_sign(ifm_sign),
        .i_data_dff(ifm_dff),
        .o_data_sign(ifm_sign_d),
        .o_data_dff(ifm_dff_d),
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

    mul_inner #(
        .WIDTH(IWIDTH)
    ) U_mul_inner(
        .clk(clk),
        .rst_n(rst_n),
        .i_bit_i(ifm_dff_d),
        .i_randW(randW),
        .i_data_w(wght_abs_d),
        .o_randW(randW_d)
        .o_bit(prod)
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
        .prod_bit(prod),
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