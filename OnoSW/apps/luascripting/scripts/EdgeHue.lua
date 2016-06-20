require "math"

hue_pos = 0

function setup()
	-- Called once, when the script is started
	UI:init()
	UI:add_key("up")
	UI:add_key("down")
	Hardware:neo_init(8)
	Hardware:neo_set_brightness(50)
end

function loop()
	-- Called repeatedly, put your main program here
	if falling_edge("up", UI:is_key_pressed("up")) then
		--print "Light released!"
		hue_pos = hue_pos + 1
		if hue_pos > 19 then
			hue_pos = 0
		end
		change_color()
	end
	if falling_edge("down", UI:is_key_pressed("down")) then
		--print "Light released!"
		hue_pos = hue_pos - 1
		if hue_pos < 0 then
			hue_pos = 19
		end
		change_color()
	end
end

function change_color()
	local hue = math.floor(map(hue_pos, 0, 20, 0, 255))
	--local hue = 30
	Hardware:neo_set_all_hsv(hue, 255, 255)
	Hardware:neo_show()
end

function quit()
	-- Called when the script is stopped
	Hardware:neo_set_all(0, 0, 0)
	Hardware:neo_show()
end
