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


Blockly.Blocks['drive_simple'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("Drive")
            .appendField(new Blockly.FieldDropdown([
                ["forward", "FORWARD"],
                ["backward", "BACKWARD"],
                ["left ", "LEFT"],
                ["right", "RIGHT"]
            ]), "DRIVE_SELECTION");
        this.appendValueInput("SPEED")
            .setCheck("Number")
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("Speed");
        this.setInputsInline(false);
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(220);
        this.setTooltip('');
        this.setHelpUrl('');
    }
};

Blockly.Lua['drive_simple'] = function(block) {
    var dropdown_drive_selection = block.getFieldValue('DRIVE_SELECTION');
    var value_speed = Blockly.Lua.valueToCode(block, 'SPEED', Blockly.Lua.ORDER_ATOMIC);
    var code = '';
    switch (dropdown_drive_selection) {
        case "FORWARD":
            code = 'Robot:execute{action="forward", tags={"wheels"},speed= ' + value_speed + '}\n'
            break;
        case "BACKWARD":
            code = 'Robot:execute{action="backward", tags={"wheels"},speed= ' + value_speed + '}\n'
            break;
        case "LEFT":
            code = 'Robot:execute{action="shortLeft", tags={"wheels"},speed= ' + value_speed + '}\n'
            break;
        case "RIGHT":
            code = 'Robot:execute{action="shortRight", tags={"wheels"},speed= ' + value_speed + '}\n'
            break;
        default:
            code = 'Robot:execute{action="stop", tags={"wheels"}' + '}\n'
    }
    return code;
};

Blockly.Blocks['drive_advance'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Wheel speed: ");
    this.appendValueInput("SPEED_LEFT")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Left");
    this.appendValueInput("SPEED_RIGHT")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Right");
    this.setInputsInline(false);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('Set the speed of the wheels on each side. Speed-values are from -1.0 to 1.0 ');
    this.setHelpUrl('');
  }
};

Blockly.Lua['drive_advance'] = function(block) {
  var value_speed_left = Blockly.Lua.valueToCode(block, 'SPEED_LEFT', Blockly.Lua.ORDER_ATOMIC);
  var value_speed_right = Blockly.Lua.valueToCode(block, 'SPEED_RIGHT', Blockly.Lua.ORDER_ATOMIC);
  var code = 'Robot:execute{action="forward", tags={"wheel","left"},speed= ' + (value_speed_left) + '}\n'
  code += 'Robot:execute{action="forward", tags={"wheel","right"},speed= ' + (value_speed_right) + '}\n'
  return code;
};
