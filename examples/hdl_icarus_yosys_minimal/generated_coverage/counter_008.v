module counter_008(input clk, output reg [3:0] q); always @(posedge clk) q <= q + 1; endmodule
