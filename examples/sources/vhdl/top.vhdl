library IEEE;
use IEEE.std_logic_1164.all;
library blink_lib;
use blink_lib.blink_pkg.all;

entity Top is
  generic (
    FREQ : natural := 0;
    SECS : natural := 0
  );
  port (
    clk_i :  in std_logic;
    led_o : out std_logic
  );
end entity Top;

architecture ARCH of Top is
  signal led : std_logic;
begin

  blink_i: Blink
  generic map (FREQ => FREQ, SECS => SECS)
  port map (clk_i => clk_i, led_o => led_o);

  gen_error: if (FREQ=0 or SECS=0) generate
  begin
    process(clk_i)
    begin
      if rising_edge(clk_i) then
        led <= '0';
      end if;
    end process;
    process(clk_i)
    begin
      if rising_edge(clk_i) then
        led <= '1';
      end if;
    end process;
    led_o <= led;
  end generate gen_error;

end architecture ARCH;
