module rm_threshold_classifier(
    input wire clk,
    input wire [7:0] in_data,
    output reg out_data
);
always @(posedge clk) begin
    out_data <= in_data > 8'd127;
end
endmodule

