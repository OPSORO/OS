function setup()
	-- Called once, when the script is started
	print("Starting NeoBlink...")
	Hardware.Neopixel:init(8)
end

function loop()
	-- Called repeatedly, put your main program here
	Hardware.Neopixel:set_all(75, 75, 0)
	Hardware.Neopixel:show()
	sleep(1)
	Hardware.Neopixel:set_all(0, 75, 75)
	Hardware.Neopixel:show()
	sleep(1)
end

function quit()
	-- Called when the script is stopped
	Hardware.Neopixel:set_all(0, 0, 0)
	Hardware.Neopixel:show()
end
