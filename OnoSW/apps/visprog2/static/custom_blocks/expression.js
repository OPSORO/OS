Blockly.Blocks['expression_update'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-smile-o.png", 16, 18, ""))
        .appendField("Update expression");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(105);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['expression_update'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['expression_setekman'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-smile-o.png", 16, 18, ""))
        .appendField("set emotion to")
        .appendField(new Blockly.FieldDropdown([["happy", "HAPPY"], ["sad", "SAD"], ["angry", "ANGRY"], ["surprise", "SURPRISE"], ["fear", "FEAR"], ["disgust", "DISGUST"]]), "EMOTION");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(105);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['expression_setekman'] = function(block) {
  var dropdown_emotion = block.getFieldValue('EMOTION');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['expression_setva'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-smile-o.png", 16, 18, ""))
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
    this.setColour(105);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['expression_setva'] = function(block) {
  var value_valence = Blockly.JavaScript.valueToCode(block, 'VALENCE', Blockly.JavaScript.ORDER_ATOMIC);
  var value_arousal = Blockly.JavaScript.valueToCode(block, 'AROUSAL', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['expression_setphir'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-smile-o.png", 16, 18, ""))
        .appendField("Set emotion to");
    this.appendValueInput("PHI")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Phi");
    this.appendValueInput("R")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("R");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(105);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['expression_setphir'] = function(block) {
  var value_phi = Blockly.JavaScript.valueToCode(block, 'PHI', Blockly.JavaScript.ORDER_ATOMIC);
  var value_r = Blockly.JavaScript.valueToCode(block, 'R', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};
