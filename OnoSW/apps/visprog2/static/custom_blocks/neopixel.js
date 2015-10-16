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
    this.setTooltip('Initialize the NeoPixel port with a specified number of pixels.');
  }
};
Blockly.Lua['neo_init'] = function(block) {
  var text_numpixels = block.getFieldValue('NUMPIXELS');
  var code = 'Hardware:neo_init(' + text_numpixels + ')\n';
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
    this.setTooltip('Set the global brightness of the pixels. Value between 0 to 255.');
  }
};
Blockly.Lua['neo_brightness'] = function(block) {
  var value_brightness = Blockly.Lua.valueToCode(block, 'BRIGHTNESS', Blockly.Lua.ORDER_ATOMIC);
  var code = 'Hardware:neo_set_brightness(' + value_brightness + ')\n';
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
    this.setTooltip('Send pixel data to the NeoPixels.');
  }
};
Blockly.Lua['neo_update'] = function(block) {
  var code = 'Hardware:neo_show()\n';
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
    this.setTooltip('Set the color of a single pixel.');
  }
};
Blockly.Lua['neo_setpixel'] = function(block) {
  var value_pixel = Blockly.Lua.valueToCode(block, 'PIXEL', Blockly.Lua.ORDER_ATOMIC);
  var colour_color = block.getFieldValue('COLOR');

  var hex = parseInt(colour_color.substring(1), 16);
  var r = (hex & 0xff0000) >> 16;
  var g = (hex & 0x00ff00) >> 8;
  var b = hex & 0x0000ff;

  var code = 'Hardware:neo_set_pixel(' + value_pixel + ', ' + r + ', ' + g  + ', ' + b + ')\n';
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
    this.setTooltip('Set the color of a range of pixels.');
  }
};
Blockly.Lua['neo_setrange'] = function(block) {
  var value_start = Blockly.Lua.valueToCode(block, 'START', Blockly.Lua.ORDER_ATOMIC);
  var value_end = Blockly.Lua.valueToCode(block, 'END', Blockly.Lua.ORDER_ATOMIC);
  var colour_color = block.getFieldValue('COLOR');

  var hex = parseInt(colour_color.substring(1), 16);
  var r = (hex & 0xff0000) >> 16;
  var g = (hex & 0x00ff00) >> 8;
  var b = hex & 0x0000ff;

  var code = 'Hardware:neo_set_range(' + value_start + ', ' + value_end + ', ' + r + ', ' + g  + ', ' + b + ')\n';
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
    this.setTooltip('Set the color of all pixels.');
  }
};
Blockly.Lua['neo_setall'] = function(block) {
  var colour_color = block.getFieldValue('COLOR');

  var hex = parseInt(colour_color.substring(1), 16);
  var r = (hex & 0xff0000) >> 16;
  var g = (hex & 0x00ff00) >> 8;
  var b = hex & 0x0000ff;

  var code = 'Hardware:neo_set_all(' + r + ', ' + g  + ', ' + b + ')\n';
  return code;
};
