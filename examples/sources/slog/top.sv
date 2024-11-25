`include "header1.svh"
`include "header2.svh"

module Top #(
  parameter int FREQ = 0,
  parameter int SECS = 0
)(
  input  clk_i,
  output led_o
);

  Blink #(.FREQ (FREQ), .SECS (SECS)) dut (.clk_i (clk_i), .led_o (led_o));

`ifndef INCLUDE1
  reg led;
  always @(posedge clk_i) led <= 1'b0;
  always @(posedge clk_i) led <= 1'b1;
  assign led_o = led;
  initial begin $stop; $error("intentional"); end
`endif

`ifndef INCLUDE2
  reg led;
  always @(posedge clk_i) led <= 1'b0;
  always @(posedge clk_i) led <= 1'b1;
  assign led_o = led;
  initial begin $stop; $error("intentional"); end
`endif

`ifndef DEFINE1
  reg led;
  always @(posedge clk_i) led <= 1'b0;
  always @(posedge clk_i) led <= 1'b1;
  assign led_o = led;
  initial begin $stop; $error("intentional"); end
`endif

`ifndef DEFINE2
  reg led;
  always @(posedge clk_i) led <= 1'b0;
  always @(posedge clk_i) led <= 1'b1;
  assign led_o = led;
  initial begin $stop; $error("intentional"); end
`endif

  generate
    if (!FREQ || !SECS) begin
      reg led;
      always @(posedge clk_i) led <= 1'b0;
      always @(posedge clk_i) led <= 1'b1;
      assign led_o = led;
      initial begin $stop; $error("intentional"); end
    end
  endgenerate

endmodule
