Blockly.Lua.addReservedWords("Drive");

Blockly.Blocks['stop'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-lightbulb-o.png", 16, 18, ""))
        .appendField("Stop");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(20);
    this.setTooltip('Stop the robot');
  }
};
Blockly.Lua['stop'] = function(block) {
var code = 'Robot:set_dof_value("wheel_left_front","wheel",'+ 0 + ')\n'
      + 'Robot:set_dof_value("wheel_right_front","wheel",'+ 0 + ')\n'
      + 'Robot:set_dof_value("wheel_left_back","wheel",'+ 0 + ')\n'
      + 'Robot:set_dof_value("wheel_right_back","wheel",'+ 0 + ')\n';
      return code;
}

Blockly.Blocks['drive'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-lightbulb-o.png", 16, 18, ""))
        .appendField("Drive")
        .appendField(new Blockly.FieldDropdown([["forward", "FORWARD"], ["backward", "BACKWARD"]]),'DIRECTION');
    this.appendValueInput("Speed")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("SPEED");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(20);
    this.setTooltip('drive forward of backward with a speed from 0 to 100');
  }
};
Blockly.Lua['drive'] = function(block) {
  var code = "";
  var direction = block.getFieldValue('DIRECTION');
  var speed = Blockly.Lua.valueToCode(block, 'SPEED', Blockly.Lua.ORDER_ATOMIC)/100.0;

  if(direction == "FORWARD"){
    code = 'Robot:set_dof_value("wheel_left_front","wheel",'+ speed + ')\n'
    + 'Robot:set_dof_value("wheel_right_front","wheel",'+ speed + ')\n'
    + 'Robot:set_dof_value("wheel_left_back","wheel",'+ speed + ')\n'
    + 'Robot:set_dof_value("wheel_right_back","wheel",'+ speed + ')\n';
  }
  else {
    speed = - speed;
    code = 'Robot:set_dof_value("wheel_left_front","wheel",'+ speed + ')\n'
    + 'Robot:set_dof_value("wheel_right_front","wheel",'+ speed + ')\n'
    + 'Robot:set_dof_value("wheel_left_back","wheel",'+ speed + ')\n'
    + 'Robot:set_dof_value("wheel_right_back","wheel",'+ speed + ')\n';
  }
  return code;
};

Blockly.Blocks['shortTurn'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-lightbulb-o.png", 16, 18, ""))
        .appendField("Short Turn ")
        .appendField(new Blockly.FieldDropdown([["left", "LEFT"], ["right", "RIGHT"]]),'DIRECTION');
    this.appendValueInput("Speed")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("SPEED");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(20);
    this.setTooltip('drive forward of backward with a speed from 0 to 100');
  }
};
Blockly.Lua['shortTurn'] = function(block) {
  var code = "";
  var direction = block.getFieldValue('DIRECTION');
  var speed = Blockly.Lua.valueToCode(block, 'SPEED', Blockly.Lua.ORDER_ATOMIC)/100.0;

  if(direction == "LEFT"){
    code = 'Robot:set_dof_value("wheel_left_front","wheel",'+ (string)(-speed) + ')\n'
    + 'Robot:set_dof_value("wheel_right_front","wheel",'+ speed + ')\n'
    + 'Robot:set_dof_value("wheel_left_back","wheel",'+ (string)(-speed) + ')\n'
    + 'Robot:set_dof_value("wheel_right_back","wheel",'+ speed + ')\n';
  }
  else {
    speed = - speed;
    code = 'Robot:set_dof_value("wheel_left_front","wheel",'+ speed + ')\n'
    + 'Robot:set_dof_value("wheel_right_front","wheel",'+ (string)(-speed) + ')\n'
    + 'Robot:set_dof_value("wheel_left_back","wheel",'+ speed + ')\n'
    + 'Robot:set_dof_value("wheel_right_back","wheel",'+ (string)(-speed) + ')\n';
  }
  return code;
};

Blockly.Blocks['longTurn'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-lightbulb-o.png", 16, 18, ""))
        .appendField("Long Turn ")
        .appendField(new Blockly.FieldDropdown([["left", "LEFT"], ["right", "RIGHT"]]),'DIRECTION');
    this.appendValueInput("Speed")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("SPEED");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(20);
    this.setTooltip('drive forward of backward with a speed from 0 to 100');
  }
};
Blockly.Lua['shortTurn'] = function(block) {
  var code = "";
  var direction = block.getFieldValue('DIRECTION');
  var speed = Blockly.Lua.valueToCode(block, 'SPEED', Blockly.Lua.ORDER_ATOMIC)/100.0;

  if(direction == "LEFT"){
    code = 'Robot:set_dof_value("wheel_left_front","wheel",'+ 0 + ')\n'
    + 'Robot:set_dof_value("wheel_right_front","wheel",'+ speed + ')\n'
    + 'Robot:set_dof_value("wheel_left_back","wheel",'+ 0 + ')\n'
    + 'Robot:set_dof_value("wheel_right_back","wheel",'+ speed + ')\n';
  }
  else {
    speed = - speed;
    code = 'Robot:set_dof_value("wheel_left_front","wheel",'+ speed + ')\n'
    + 'Robot:set_dof_value("wheel_right_front","wheel",'+ 0 + ')\n'
    + 'Robot:set_dof_value("wheel_left_back","wheel",'+ speed + ')\n'
    + 'Robot:set_dof_value("wheel_right_back","wheel",'+ 0 + ')\n';
  }
  return code;
};
