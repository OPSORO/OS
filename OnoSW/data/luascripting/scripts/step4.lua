function setup()
  -- Called once, when the script is started

end

function loop()
  -- Called repeatedly, put your main program here
  Hardware:led_on()
  sleep(1)
  Hardware:led_off()
  sleep(1)
end

function quit()
  -- Called when the script is stopped
  Hardware:led_off()
end
