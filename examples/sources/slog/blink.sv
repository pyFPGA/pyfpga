module Blink #(
  parameter int FREQ = 25000000,
  parameter int SECS = 1
)(
  input  clk_i,
  output led_o
);

  localparam int          DIV = FREQ*SECS;
  logic                   led = 0;
  logic [$clog2(DIV)-1:0] cnt = 0;

  always_ff @(posedge clk_i) begin
    if (cnt == DIV-1) begin
      cnt <= 0;
      led <= ~led;
    end else begin
      cnt <= cnt + 1;
    end
  end

  assign led_o = led;

endmodule
