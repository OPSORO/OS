Blockly.Lua.addReservedWords("Hardware");

Blockly.Blocks['hardware_ledonoff'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("/static/images/fontawesome/white/svg/wrench.svg", 16, 18, ""))
        .appendField("Turn status LED")
        .appendField(new Blockly.FieldDropdown([["on", "ON"], ["off", "OFF"]]), "ONOFF");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(270);
    this.setTooltip('Turn the red status LED on or off.');
  }
};
Blockly.Lua['hardware_ledonoff'] = function(block) {
  var dropdown_onoff = block.getFieldValue('ONOFF');
  var code = '';
  if(dropdown_onoff == "ON"){
    code = "Hardware:led_on()\n"
  }else{
    code = "Hardware:led_off()\n"
  }
  return code;
};

Blockly.Blocks['hardware_readanalog'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("/static/images/fontawesome/white/svg/wrench.svg", 16, 18, ""))
        .appendField("Read analog sensor")
        .appendField(new Blockly.FieldDropdown([["A0", "0"], ["A1", "1"], ["A2", "2"], ["A3", "3"]]), "CHANNEL");
    this.setOutput(true);
    this.setColour(270);
    this.setTooltip('Read the value of an analog sensor.\nValue ranges from 0 at 0V to 1023 at 3.3V.');
  }
};
Blockly.Lua['hardware_readanalog'] = function(block) {
  var dropdown_channel = block.getFieldValue('CHANNEL');
  var code = 'Hardware.Analog:read_channel(' + dropdown_channel + ')';
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};
