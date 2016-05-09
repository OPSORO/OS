blink_anim = AnimatePeriodic({0, 4.8, 4.9, 5, 7.8, 7.9, 8}, {0, 0, 1, 0, 0, 1, 0})

eye_gaze = 0

mouth_anim = nil

random_gaze = 0

function create_random_gaze()
	random_gaze = (math.random()*2-1)
end

function gaze_overlay(dofpos, dof)
  return eye_gaze
end

function blink_overlay(dofpos, dof)
  if blink_anim() > 0 then
    return -0.8
  else
    return dofpos
  end
end

function mouth_overlay(dofpos, dof)
  if mouth_anim == nil then
    return dofpos
  else
  	--return dofpos + mouth_anim()
  	return mouth_anim()
  end
end

function wait_and_update(duration)
  local end_t = seconds() + duration
  while end_t > seconds() do
    Expression.update()
  end
end

function setup()
  -- Called once, when the script is started
  
  -- Generate TTS files:
  Sound:say_tts("Hello, my name is Ono", true)
  Sound:say_tts("Hi there Wustainvies", true)
  Sound:say_tts("And I am a social robot!", true)
  Sound:say_tts("Sometimes I can be sad", true)
  Sound:say_tts("But usually I'm very happy!", true)
  Sound:say_tts("I can look to the right", true)
  Sound:say_tts("I can look to the left", true)
  Sound:say_tts("right", true)
  Sound:say_tts("left", true)
  Sound:say_tts("right", true)
  Sound:say_tts("left", true)
  Sound:say_tts("I can do acting too", true)
  Sound:say_tts("Do you want me to tell you a joke ?", true)
  Sound:say_tts("Who was that ?", true)
  Sound:say_tts("Oopsy, sorry, it was me", true)
  Sound:say_tts("ha ha ha ha", true)
  
  -- Initialize hardware and expressions
  Hardware:servo_init()
  Hardware:servo_neutral()
  

  Expression.dofs.r_e_hor.add_overlay(gaze_overlay)
  Expression.dofs.l_e_hor.add_overlay(gaze_overlay)

  Expression.dofs.r_e_lid.add_overlay(blink_overlay)
  Expression.dofs.l_e_lid.add_overlay(blink_overlay)
  Expression.dofs.m_mid.add_overlay(mouth_overlay)
  Expression:set_emotion_r_phi(1.0, 15, true, 1.5)
  
  Expression.update()
  Hardware:servo_enable()

  -- Run demo scenario
  lipsync("Hello, my name is Ono", 1.6, {0.1, 0.45, 0.8})
  sleep(1)

  lipsync("Hi there Wustainvies", 2, {0.1, 0.45, 0.8, 1.5, 1.8})
  sleep(1.5)
  
  lipsync("I am a social robot!", 1.8, {0.1, 0.45, 0.8})
  sleep(0.5)

  lipsync("Sometimes I can be sad", 1.6, {0.1, 0.45, 0.8})
  sleep(0.5)

  Expression:set_emotion_r_phi(1.0, 200, true, 1.0)
  wait_and_update(2.5)
  
  Expression:set_emotion_r_phi(0.0, 15, true, 1.0)
  wait_and_update(1.5)

  lipsync("But usually I'm very happy!", 2.0, {0.1, 0.45, 0.8})
  sleep(0.5)

  Expression:set_emotion_r_phi(1.0, 35, true, 1.0)
  wait_and_update(3)
  Expression:set_emotion_r_phi(1.0, 15, true, 1.0)
  wait_and_update(1.5)

  
  lipsync("I can look to the right", 1.5, {0.1, 0.45, 0.8})
  sleep(0.5)
  eye_gaze=1
  wait_and_update(1.5)
  
  lipsync("I can look to the left", 1.5, {0.1, 0.45, 0.8})
  sleep(0.5)
  eye_gaze=-1
  wait_and_update(1.5)
  
  lipsync("right", 0.5, {0.1, 0.4})
  sleep(0.3)
  eye_gaze=1
  wait_and_update(0.5)
  
  lipsync("left", 0.5, {0.1, 0.4})
  sleep(0.3)
  eye_gaze=-1
  wait_and_update(0.5)

  eye_gaze=0
  lipsync("Do you want me to tell you a joke ?", 2, {0.1, 0.3, 0.45, 0.6, 0.8, 1, 1.2, 1.4, 1.7, 2})
  sleep(2)
  wait_and_update(2.5)
  
  Sound:play_file("fart-01.wav")
  Expression:set_emotion_r_phi(1.0, 90, true)
  sleep(1)
 wait_and_update(1)
  lipsync("Who was that ?", 1, {0.1, 0.45, 0.8})
  sleep(1.5)
  Expression:set_emotion_r_phi(1.0, 163, true)
  sleep(1)
 wait_and_update(1)
  eye_gaze=1
  wait_and_update(1.5)
  eye_gaze=-1
  wait_and_update(1.5)
  eye_gaze=1
  wait_and_update(1.5)
  eye_gaze=-1
  wait_and_update(1.5)
  
  Expression:set_emotion_r_phi(1.0, 70, true, 1.0)
  eye_gaze=0
  wait_and_update(0.5)
  lipsync("Oopsy, sorry, it was me", 1.0, {0.1, 0.45, 0.8})
  sleep(2)
  
  Expression:set_emotion_r_phi(1.0, 35, true, 1.0)
  wait_and_update(0.5)
  lipsync("ha ha ha ha", 1, {0.1, 0.45, 0.8})
  sleep(0.5)
  wait_and_update(1)
  
end

function lipsync(text, dur, o_pos)
  t = {}
  pos = {}
  
  table.insert(t,   0)
  table.insert(pos, 0.5)
  
  for k,v in pairs(o_pos) do
  	--print(k,v)
  	table.insert(t,    dur*v - 0.2 )
  	table.insert(t,    dur*v)
  	table.insert(t,    dur*v + 0.2 )
  	table.insert(pos,  1)
  	table.insert(pos, -1)
  	table.insert(pos,  1)
  end
  
  table.insert(t,   dur)
  table.insert(pos, 0.5)
  
  Sound:say_tts(text)
  mouth_anim = Animate(t, pos)
  wait_and_update(dur)
  mouth_anim = nil
end

function loop()

  Expression.update()
end

function quit()
  -- Called when the script is stopped
  Hardware:servo_disable()
end
