function setup()
	-- Called once, when the script is started
	UI:init()
	UI:add_button("light", "Aziz, Light!", "fa-lightbulb-o", true)
end

function loop()
	-- Called repeatedly, put your main program here
	if UI:is_button_pressed("light") then
		Hardware:led_on()
	else
		Hardware:led_off()
	end
end

function quit()
	-- Called when the script is stopped
	Hardware:led_off()
end
