require "bit32"

num_pixels = 8
num_electrodes = 12

function setup()
	-- Called once, when the script is started
	print("Starting NeoPixel Keypad...")
	Hardware.Neopixel:init(num_pixels)
	Hardware.Capacitive:init(num_electrodes)
end

function loop()
	-- Called repeatedly, put your main program here
	local touchData = Hardware.Capacitive:get_touched()

	Hardware.Neopixel:set_all(0, 0, 0)

	for i=0,7 do
		if bit32.extract(touchData, i) > 0 then
			Hardware.Neopixel:set_pixel(i, 75, 75, 0)
		end
	end
	Hardware.Neopixel:show()
end

function quit()
	-- Called when the script is stopped
	Hardware.Neopixel:set_all(0, 0, 0)
	Hardware.Neopixel:show()
end
