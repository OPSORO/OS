function setup()
	Robot:reset_dofs()

end

function loop()
	Robot:execute{action="close",tags={"eye"}}
	delay(1000)
	Robot:execute{action="open",tags={"eye"}}
	delay(1000)

end

function quit()
	-- Called when the script is stopped

end
