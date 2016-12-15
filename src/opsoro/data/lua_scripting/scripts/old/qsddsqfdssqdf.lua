function setup()
	-- Called once, when the script is started
	UI:init()
	UI:add_button("hello", "Hello!", "fa-hand-spock-o", false)
	UI:add_button("light", "Light!", "fa-lightbulb-o", false)
	UI:add_key("down")
	UI:add_key("x")
	UI:add_key("space")
	Hardware:cap_init(8)
end

function loop()
	-- Called repeatedly, put your main program here
	if rising_edge("space", UI:is_key_pressed("space")) then
		print("E0: " .. Hardware:cap_get_baseline_data(5))
	end
end

function quit()
	-- Called when the script is stopped

end
