`ifndef _sobol8_
`define _sobol8_

module sobol16 #(
    parameter WIDTH = 16,
    parameter LOGWIDTH = 4
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
    always_comb begin : proc_dirVec_16
        dirVec[0]   <= 'b1000000000000000;
        dirVec[1]   <= 'b0100000000000000;
        dirVec[2]   <= 'b0010000000000000;
        dirVec[3]   <= 'b0001000000000000;
        dirVec[4]   <= 'b0000100000000000;
        dirVec[5]   <= 'b0000010000000000;
        dirVec[6]   <= 'b0000001000000000;
        dirVec[7]   <= 'b0000000100000000;
        dirVec[8]   <= 'b0000000010000000;
        dirVec[9]   <= 'b0000000001000000;
        dirVec[10]  <= 'b0000000000100000;
        dirVec[11]  <= 'b0000000000010000;
        dirVec[12]  <= 'b0000000000001000;
        dirVec[13]  <= 'b0000000000000100;
        dirVec[14]  <= 'b0000000000000010;
        dirVec[15]  <= 'b0000000000000001;
    end

    always_comb begin : proc_outoh_16
        case(outoh)
            'b0000000000000001 : vecIdx = 'd0;
            'b0000000000000010 : vecIdx = 'd1;
            'b0000000000000100 : vecIdx = 'd2;
            'b0000000000001000 : vecIdx = 'd3;
            'b0000000000010000 : vecIdx = 'd4;
            'b0000000000100000 : vecIdx = 'd5;
            'b0000000001000000 : vecIdx = 'd6;
            'b0000000010000000 : vecIdx = 'd7;
            'b0000000100000000 : vecIdx = 'd8;
            'b0000001000000000 : vecIdx = 'd9;
            'b0000010000000000 : vecIdx = 'd10;
            'b0000100000000000 : vecIdx = 'd11;
            'b0001000000000000 : vecIdx = 'd12;
            'b0010000000000000 : vecIdx = 'd13;
            'b0100000000000000 : vecIdx = 'd14;
            'b1000000000000000 : vecIdx = 'd15;
            default : vecIdx = 'd0;
        endcase // onehot
    end

endmodule

`endif