function setup()
  -- Called once, when the script is started
  UI:init()
  UI:add_button("light", "Light!", "fa-lightbulb-o")
end

function loop()
  -- Called repeatedly, put your main program here
  
end

function quit()
  -- Called when the script is stopped
  Hardware:led_off()
end
