eye_pos = 0

function eye_overlay(dofpos, dof)
  return eye_pos
end

function setup()
  -- Called once, when the script is started
  -- Initialize hardware and expressions
  UI:init()
  UI:add_key("left")
  UI:add_key("right")

  Hardware.Servo:init()
  Hardware.Servo:neutral()

  Expression.dofs.r_e_hor.add_overlay(eye_overlay)
  Expression.dofs.l_e_hor.add_overlay(eye_overlay)
  Expression:set_emotion_r_phi(1.0, 15, true, 1.5)

  Expression.update()
  Hardware.Servo:enable()
end

function loop()
  -- Called repeatedly, put your main program here
  if rising_edge("left", UI:is_key_pressed("left")) then
  	print("up")
    eye_pos = -0.8
    Expression.update()
  end

  if rising_edge("right", UI:is_key_pressed("right")) then
  	eye_pos = 0.8
  	Expression.update()
  end
end

function quit()
  -- Called when the script is stopped
  Hardware.Servo:disable()
end
