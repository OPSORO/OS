function setup()
  -- Called once, when the script is started
  Hardware:led_on()
end

function loop()
  -- Called repeatedly, put your main program here

end

function quit()
  -- Called when the script is stopped
  Hardware:led_off()
end
