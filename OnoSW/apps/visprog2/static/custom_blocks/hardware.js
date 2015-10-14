Blockly.Blocks['hardware_ledonoff'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-wrench.png", 16, 18, ""))
        .appendField("Turn status LED")
        .appendField(new Blockly.FieldDropdown([["on", "ON"], ["off", "OFF"]]), "ONOFF");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(270);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['hardware_ledonoff'] = function(block) {
  var dropdown_onoff = block.getFieldValue('ONOFF');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['hardware_readanalog'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-wrench.png", 16, 18, ""))
        .appendField("Read analog sensor")
        .appendField(new Blockly.FieldDropdown([["A0", "0"], ["A1", "1"], ["A2", "2"], ["A3", "3"]]), "CHANNEL");
    this.setOutput(true);
    this.setColour(270);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['hardware_ledonoff'] = function(block) {
  var dropdown_channel = block.getFieldValue('CHANNEL');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};
