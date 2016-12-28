Blockly.Lua.addReservedWords("Robot");

Blockly.Blocks['drive_stop'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-lightbulb-o.png", 16, 18, ""))
        .appendField("Stop");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(220);
    this.setTooltip('Stop the robot');
  }
};
Blockly.Lua['drive_stop'] = function(block) {
  var code = 'Robot:execute{action="stop", tags={"wheels"}}\n'
  return code;
}

Blockly.Blocks['drive_drive'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-lightbulb-o.png", 16, 18, ""))
        .appendField("Drive")
        .appendField(new Blockly.FieldDropdown([["forward", "FORWARD"], ["backward", "BACKWARD"]]),'DIRECTION');
    this.appendValueInput("SPEED")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Speed");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(220);
    this.setTooltip('drive forward of backward with a speed from 0 to 100');
  }
};
Blockly.Lua['drive_drive'] = function(block) {
  var code = "";
  var direction = block.getFieldValue('DIRECTION');
  var speed = Blockly.Lua.valueToCode(block, 'SPEED', Blockly.Lua.ORDER_ATOMIC);

  if(direction == "FORWARD"){
    var code = 'Robot:execute{action="forward", tags={"wheels"},speed= '+ speed+'}\n'
  }
  else {
    var code = 'Robot:execute{action="backward", tags={"wheels"},speed= '+ speed+'}\n'
  }
  return code;
};

Blockly.Blocks['drive_shortTurn'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-lightbulb-o.png", 16, 18, ""))
        .appendField("Short Turn ")
        .appendField(new Blockly.FieldDropdown([["left", "LEFT"], ["right", "RIGHT"]]),'DIRECTION');
    this.appendValueInput("SPEED")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Speed");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(220);
    this.setTooltip('drive forward of backward with a speed from 0 to 100');
  }
};
Blockly.Lua['drive_shortTurn'] = function(block) {
  var code = "";
  var direction = block.getFieldValue('DIRECTION');
  var speed = Blockly.Lua.valueToCode(block, 'SPEED', Blockly.Lua.ORDER_ATOMIC);

  if(direction == "LEFT"){
    var code = 'Robot:execute{action="shortLeft", tags={"wheels"},speed= '+ speed+'}\n'
  }
  else {
    var code = 'Robot:execute{action="shortRight", tags={"wheels"},speed= '+ (-speed)+'}\n'
  }
  return code;
};

Blockly.Blocks['drive_longTurn'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-lightbulb-o.png", 16, 18, ""))
        .appendField("Long Turn ")
        .appendField(new Blockly.FieldDropdown([["left", "LEFT"], ["right", "RIGHT"]]),'DIRECTION');
    this.appendValueInput("SPEED")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Speed");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(220);
    this.setTooltip('drive forward of backward with a speed from 0 to 100');
  }
};
Blockly.Lua['drive_longTurn'] = function(block) {
  var code = "";
  var direction = block.getFieldValue('DIRECTION');
  var speed = Blockly.Lua.valueToCode(block, 'SPEED', Blockly.Lua.ORDER_ATOMIC);

  if(direction == "LEFT"){
    var code = 'Robot:execute{action="longLeft", tags={"wheels"},speed= '+ speed+'}\n'
  }
  else {
    var code = 'Robot:execute{action="longRight", tags={"wheels"},speed= '+ speed+'}\n'
  }
  return code;
};

Blockly.Blocks['drive_drive_side'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-lightbulb-o.png", 16, 18, ""))
        .appendField("Drive")
        .appendField(new Blockly.FieldDropdown([["left", "LEFT"], ["right", "RIGHT"]]),'DIRECTION');
    this.appendValueInput("SPEED")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Speed");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(220);
    this.setTooltip('discription');
  }
};
Blockly.Lua['drive_drive_side'] = function(block) {
  var code = "";
  var direction = block.getFieldValue('DIRECTION');
  var speed = Blockly.Lua.valueToCode(block, 'SPEED', Blockly.Lua.ORDER_ATOMIC);

  if(direction == "LEFT"){
    var code = 'Robot:execute{action="forward", tags={"wheel,left"},speed= '+ speed+'}\n'
  }
  else {
    var code = 'Robot:execute{action="backward", tags={"wheel,right"},speed= '+ speed+'}\n'
  }
  return code;
};
