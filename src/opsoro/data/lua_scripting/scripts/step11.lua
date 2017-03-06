function setup()
  -- Called once, when the script is started
  UI:init()
  UI:add_key("up")
  UI:add_key("down")

  Hardware:Servo:init()
  Hardware:Servo:neutral()

  Expression:set_emotion_val_ar(0.0, 0.0)
  Expression.update()

  Hardware:Servo:enable()
end

function loop()
  -- Called repeatedly, put your main program here
  if rising_edge("up", UI:is_key_pressed("up")) then
  	print("up")
    Expression:set_emotion_r_phi(1.0, 30, true, 1.5)
  end

  if rising_edge("down", UI:is_key_pressed("down")) then
  	print("down")
    Expression:set_emotion_r_phi(1.0, 200, true, 1.5)
  end

  Expression.update()
end

function quit()
  -- Called when the script is stopped
  Hardware:Servo:disable()
end
