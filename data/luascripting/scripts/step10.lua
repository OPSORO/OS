function setup()
  -- Called once, when the script is started
  UI:init()
  UI:add_key("up")
  UI:add_key("down")

  Hardware:servo_init()
  Hardware:servo_neutral()

  Expression:set_emotion_val_ar(0.0, 0.0)
  Expression.update()

  Hardware:servo_enable()
end

function loop()
  -- Called repeatedly, put your main program here
  if rising_edge("up", UI:is_key_pressed("up")) then
  	print("up")
    Expression:set_emotion_r_phi(1.0, 30, true)
    Expression.update()
  end

  if rising_edge("down", UI:is_key_pressed("down")) then
  	print("down")
    Expression:set_emotion_r_phi(1.0, 200, true)
    Expression.update()
  end
end

function quit()
  -- Called when the script is stopped
  Hardware:servo_disable()
end
