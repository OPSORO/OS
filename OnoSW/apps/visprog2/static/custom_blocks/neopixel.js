Blockly.Blocks['neo_init'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-lightbulb-o.png", 16, 18, ""))
        .appendField("Initialize")
        .appendField(new Blockly.FieldTextInput("8"), "NUMPIXELS")
        .appendField("NeoPixels");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(20);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['neo_init'] = function(block) {
  var text_numpixels = block.getFieldValue('NUMPIXELS');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['neo_brightness'] = {
  init: function() {
    this.appendValueInput("BRIGHTNESS")
        .setCheck("Number")
        .appendField(new Blockly.FieldImage("static/icons/fa-lightbulb-o.png", 16, 18, ""))
        .appendField("Set brightness to");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(20);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['neo_brightness'] = function(block) {
  var value_name = Blockly.JavaScript.valueToCode(block, 'BRIGHTNESS', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['neo_update'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-lightbulb-o.png", 16, 18, ""))
        .appendField("Update pixels");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(20);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['neo_update'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['neo_setpixel'] = {
  init: function() {
    this.appendValueInput("PIXEL")
        .setCheck("Number")
        .appendField(new Blockly.FieldImage("static/icons/fa-lightbulb-o.png", 16, 18, ""))
        .appendField("Set pixel");
    this.appendDummyInput()
        .appendField("to color")
        .appendField(new Blockly.FieldColour("#ff0000"), "COLOR");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(20);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['neo_setpixel'] = function(block) {
  var value_pixel = Blockly.JavaScript.valueToCode(block, 'PIXEL', Blockly.JavaScript.ORDER_ATOMIC);
  var colour_color = block.getFieldValue('COLOR');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['neo_setrange'] = {
  init: function() {
    this.appendValueInput("START")
        .setCheck("Number")
        .appendField(new Blockly.FieldImage("static/icons/fa-lightbulb-o.png", 16, 18, ""))
        .appendField("Set pixels from");
    this.appendValueInput("END")
        .setCheck("Number")
        .appendField("to");
    this.appendDummyInput()
        .appendField("to color")
        .appendField(new Blockly.FieldColour("#ff0000"), "COLOR");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(20);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['neo_setrange'] = function(block) {
  var value_start = Blockly.JavaScript.valueToCode(block, 'START', Blockly.JavaScript.ORDER_ATOMIC);
  var value_end = Blockly.JavaScript.valueToCode(block, 'END', Blockly.JavaScript.ORDER_ATOMIC);
  var colour_color = block.getFieldValue('COLOR');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['neo_setall'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-lightbulb-o.png", 16, 18, ""))
        .appendField("Set all pixels to color")
        .appendField(new Blockly.FieldColour("#ff0000"), "COLOR");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(20);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['neo_setall'] = function(block) {
  var colour_color = block.getFieldValue('COLOR');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};
