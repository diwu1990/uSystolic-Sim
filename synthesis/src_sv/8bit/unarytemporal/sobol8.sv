`ifndef _sobol8_
`define _sobol8_

module sobol8 #(
    parameter WIDTH = 8,
    parameter LOGWIDTH = 3
) (
    input logic clk,        // Clock
    input logic rst_n,      // Asynchronous reset active low
    input logic enable,     // used for uMUL
    output logic [WIDTH-1 : 0] sobolSeq
);
    // check paper "Algorithm 659" for details

    logic [LOGWIDTH-1:0] vecIdx;
    logic [WIDTH-1:0] dirVec [WIDTH-1:0];

    // binary counter
    logic [WIDTH-1:0]cnt;
    always_ff @(posedge clk or negedge rst_n) begin : proc_1
        if(~rst_n) begin
            cnt <= 0;
        end else begin
            cnt <= cnt + enable;
        end
    end

    // least significant zero index
    logic [WIDTH-1:0] inacc;
    logic [WIDTH-1:0] outoh; // one hot coding

    genvar i;

    assign inacc[0] = ~cnt[0];
    generate
        for (i = 1; i < WIDTH; i++) begin
            assign inacc[i] = inacc[i-1] | ~cnt[i];
        end
    endgenerate

    assign outoh[0] = inacc[0];
    generate
        for (i = 1; i < WIDTH; i++) begin
            assign outoh[i] = inacc[i-1] ^ inacc[i];
        end
    endgenerate

    // vector lookup and sequence generation
    always_ff @(posedge clk or negedge rst_n) begin : proc_sobolSeq
        if(~rst_n) begin
            sobolSeq <= 0;
        end else begin
            if(enable) begin
                sobolSeq <= sobolSeq ^ dirVec[vecIdx];
            end else begin
                sobolSeq <= sobolSeq;
            end
        end
    end

    /* initialization of directional vectors for current dimension*/
    always_comb begin : proc_dirVec_8
        dirVec[0]   <= 'b10000000;
        dirVec[1]   <= 'b01000000;
        dirVec[2]   <= 'b00100000;
        dirVec[3]   <= 'b00010000;
        dirVec[4]   <= 'b00001000;
        dirVec[5]   <= 'b00000100;
        dirVec[6]   <= 'b00000010;
        dirVec[7]   <= 'b00000001;
    end

    always_comb begin : proc_outoh_8
        case(outoh)
            'b00000001 : vecIdx = 'd0;
            'b00000010 : vecIdx = 'd1;
            'b00000100 : vecIdx = 'd2;
            'b00001000 : vecIdx = 'd3;
            'b00010000 : vecIdx = 'd4;
            'b00100000 : vecIdx = 'd5;
            'b01000000 : vecIdx = 'd6;
            'b10000000 : vecIdx = 'd7;
            default : vecIdx = 'd0;
        endcase // onehot
    end

endmodule

`endif