Blockly.Blocks['servo_init'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-gears.png", 16, 18, ""))
        .appendField("Initialize servos");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(345);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['servo_init'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['servo_enabledisable'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-gears.png", 16, 18, ""))
        .appendField("Turn all servos")
        .appendField(new Blockly.FieldDropdown([["on", "ON"], ["off", "OFF"]]), "NAME");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(345);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['servo_enabledisable'] = function(block) {
  var dropdown_name = block.getFieldValue('NAME');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['servo_set'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-gears.png", 16, 18, ""))
        .appendField("Set servo ")
        .appendField(new Blockly.FieldDropdown(
					[
						["0", "0"], ["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"], ["5", "5"],
						["6", "6"], ["7", "7"], ["8", "8"], ["9", "9"], ["10", "10"], ["11", "11"],
						["12", "12"], ["13", "13"], ["14", "14"], ["15", "15"]
					]),
					"CHANNEL");
    this.appendValueInput("POS")
        .setCheck("Number")
        .appendField("to position");
    this.setInputsInline(true);
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(345);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['servo_set'] = function(block) {
  var dropdown_channel = block.getFieldValue('CHANNEL');
  var value_pos = Blockly.JavaScript.valueToCode(block, 'POS', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};
