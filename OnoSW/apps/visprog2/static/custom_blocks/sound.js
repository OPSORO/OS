Blockly.Blocks['sound_saytts'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-volume-down.png", 16, 18, ""))
        .appendField("Say")
        .appendField(new Blockly.FieldTextInput("I am a robot!"), "TEXT");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(300);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['sound_saytts'] = function(block) {
  var text_text = block.getFieldValue('TEXT');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['sound_play'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-volume-down.png", 16, 18, ""))
        .appendField("Play")
        .appendField(new Blockly.FieldDropdown([["option", "OPTIONNAME"], ["option", "OPTIONNAME"], ["option", "OPTIONNAME"]]), "NAME");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(300);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['sound_play'] = function(block) {
  var dropdown_name = block.getFieldValue('NAME');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};
