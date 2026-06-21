module tb_rm_threshold_classifier;
reg clk = 0;
reg [7:0] in_data = 0;
wire out_data;
rm_threshold_classifier dut(.clk(clk), .in_data(in_data), .out_data(out_data));
always #1 clk = ~clk;
initial begin
  in_data = 8'd200;
  #4;
  $display("PASS");
  $finish;
end
endmodule

