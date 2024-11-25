library IEEE;
use IEEE.std_logic_1164.all;

package blink_pkg is

  component Blink is
    generic (
      FREQ  : positive := 25e6;
      SECS  : positive := 1
    );
    port (
      clk_i :  in std_logic;
      led_o : out std_logic
    );
  end component Blink;

end package blink_pkg;
