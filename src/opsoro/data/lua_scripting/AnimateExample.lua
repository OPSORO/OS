function setup()
	-- Called once, when the script is started
	UI:init()
	UI:add_key("space")
	a = Animate:new({0, 5, 10}, {100, 50, 100})
end

function loop()
	-- Called repeatedly, put your main program here
	if rising_edge("space", UI:is_key_pressed("space")) then
		print("a = " .. a())
	end
end

function quit()
	-- Called when the script is stopped

end
