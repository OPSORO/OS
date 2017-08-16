Blockly.Lua.addReservedWords("Expression");

Blockly.Blocks['expression_update'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("/static/images/fontawesome/white/svg/smile-o.svg", 16, 18, ""))
        .appendField("Update expression");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(105);
    this.setTooltip('Calculate and update servo motor positions based on the current expression.');
  }
};
Blockly.Lua['expression_update'] = function(block) {
  var code = "Expression:update()\n";
  return code;
};

Blockly.Blocks['expression_setekman'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("/static/images/fontawesome/white/svg/smile-o.svg", 16, 18, ""))
        .appendField("set emotion to")
        .appendField(new Blockly.FieldDropdown(expressionlist), "EMOTION");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(105);
    this.setTooltip('Set the current facial expression using Ekman\'s basic emotions');
  }
};
Blockly.Lua['expression_setekman'] = function(block) {
  var dropdown_emotion = block.getFieldValue('EMOTION');
  var code = 'Expression:set_emotion_name("' + dropdown_emotion + '")\n';
  return code;
};

Blockly.Blocks['expression_setva'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("/static/images/fontawesome/white/svg/smile-o.svg", 16, 18, ""))
        .appendField("Set emotion to");
    this.appendValueInput("VALENCE")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Valence");
    this.appendValueInput("AROUSAL")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Arousal");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(62);
    this.setTooltip('Set the current facial expression using Valence and Arousal. Parameters range from -1.0 to +1.0.');
  }
};
Blockly.Lua['expression_setva'] = function(block) {
  var value_valence = Blockly.Lua.valueToCode(block, 'VALENCE', Blockly.Lua.ORDER_ATOMIC);
  var value_arousal = Blockly.Lua.valueToCode(block, 'AROUSAL', Blockly.Lua.ORDER_ATOMIC);

  var code = 'Expression:set_emotion_val_ar(' + value_valence + ', ' + value_arousal +')\n';
  return code;
};

Blockly.Blocks['expression_setrphi'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("/static/images/fontawesome/white/svg/smile-o.svg", 16, 18, ""))
        .appendField("Set emotion to");
    this.appendValueInput("R")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("R");
    this.appendValueInput("PHI")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Phi");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(105);
    this.setTooltip('Set the current facial expression using Phi and R. Phi is a value in degrees, R ranges from 0.0 to 1.0.');
  }
};
Blockly.Lua['expression_setrphi'] = function(block) {
  var value_phi = Blockly.Lua.valueToCode(block, 'PHI', Blockly.Lua.ORDER_ATOMIC);
  var value_r = Blockly.Lua.valueToCode(block, 'R', Blockly.Lua.ORDER_ATOMIC);
  var code = 'Expression:set_emotion_r_phi(' + value_phi + ', ' + value_r +', true)\n';
  return code;
};
