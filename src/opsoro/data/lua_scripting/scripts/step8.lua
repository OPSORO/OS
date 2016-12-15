light = false

function setup()
  -- Called once, when the script is started
  UI:init()
  UI:add_button("lighton", "Light On", "fa-lightbulb-o")
  UI:add_button("lightoff", "Light Off", "fa-power-off")
end

function loop()
  -- Called repeatedly, put your main program here
  if UI:is_button_pressed("lighton") then
    light = true
  elseif UI:is_button_pressed("lightoff") then
    light = false
  end

  if light == true then
    Hardware:led_on()
  else
    Hardware:led_off()
  end
end

function quit()
  -- Called when the script is stopped
  Hardware:led_off()
end
