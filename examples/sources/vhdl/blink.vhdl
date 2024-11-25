library IEEE;
use IEEE.std_logic_1164.all;

entity Blink is
  generic (
    FREQ  : positive := 25e6;
    SECS  : positive := 1
  );
  port (
    clk_i : in  std_logic;
    led_o : out std_logic
  );
end entity Blink;

architecture RTL of Blink is
  constant DIV : positive := FREQ*SECS;
  signal   led : std_logic := '0';
  signal   cnt : natural range 0 to DIV-1 := 0;
begin

  blink_p: process (clk_i)
  begin
    if rising_edge(clk_i) then
      if cnt = DIV-1 then
        cnt <= 0;
        led <= not led;
      else
        cnt <= cnt + 1;
      end if;
    end if;
  end process blink_p;

  led_o <= led;

end architecture RTL;
