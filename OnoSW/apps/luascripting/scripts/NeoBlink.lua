function setup()
	-- Called once, when the script is started
	print("Starting NeoBlink...")
	Hardware.neo_init(8)
end

function loop()
	-- Called repeatedly, put your main program here
	Hardware.neo_set_all(75, 75, 0)
	Hardware.neo_show()
	sleep(1)
	Hardware.neo_set_all(0, 75, 75)
	Hardware.neo_show()
	sleep(1)
end

function quit()
	-- Called when the script is stopped
	Hardware.neo_set_all(0, 0, 0)
	Hardware.neo_show()
end
