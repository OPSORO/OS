Blockly.Lua.addReservedWords("Detection");

Blockly.Blocks['detection_get_coordinates'] = {
  init: function() {
    var colour = new Blockly.FieldColour('#ff0000');
    colour.setColours(['#f00','#0f0','#00f','#ff0']).setColumns(2);
    this.appendDummyInput()
        .appendField('If')
        .appendField(colour,'COLOUR')
        .appendField('is detected.');
    this.appendField
    this.setColour(330);
    this.setTooltip('This block can do something with colors');
    this.appendDummyInput()
        .appendField('Follow it');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_get_coordinates'] = function(block) {
  var color = block.getFieldValue('COLOUR')
  var code = '';
  //code += 'print(Detection:is_color("'+color+'"))\n';
  code += 'if Detection:is_color("'+color+'") then\n';
  code += 'x = Detection:get_coord_x("'+color+'")\n';
  code += 'y = Detection:get_coord_y("'+color+'")\n';
  /*code += 'print(x)\n'
  code += 'print(y)\n'*/
  code += 'Detection:folow_object(x,y)\n';
  code += 'end\n';
  return code;
  var code = '';
};

Blockly.Blocks['detection_get_coordinates_face'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Face tracker");
    this.setColour(330);
    this.setTooltip('dit volgt een gezicht');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_get_coordinates_face'] = function(block) {
  var code = '';
  code += 'x = Detection:get_face_coord_x()\n';
  code += 'y = Detection:get_face_coord_y()\n';
  /*code += 'print(x+"")\n'
  code += 'print(y+"")\n'*/
  code += 'Detection:folow_object(x,y)\n';
  return code;
};

var colorVast;
Blockly.Blocks['detection_colorCheck'] = {
  init: function() {
    var colour = new Blockly.FieldColour('#ff0000');
    colour.setColours(['#f00','#0f0','#00f','#ff0']).setColumns(2);
    this.appendDummyInput()
        .appendField('If')
        .appendField(colour,'COLOUR')
        .appendField('is detected.');
    this.appendField
    this.setColour(330);
    this.setTooltip('This block can do something with colors');
    this.appendStatementInput('BODY')
    .appendField('do');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_colorCheck'] = function(block) {
  var statements_body = Blockly.Lua.statementToCode(block, 'BODY');
  var color = block.getFieldValue('COLOUR')
  colorVast = color
  var code = '';
  //code += 'print(Detection:is_color("'+color+'"))\n';
  code += 'if Detection:is_color("'+color+'") then\n';
  code += statements_body;
  code += 'end\n';
  return code;
};


/*simpel blockje start stream*/
Blockly.Blocks['detection_start_stream'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("start vidio");
    this.setColour(330);
    this.setTooltip('start de vidio stream');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_start_stream'] = function(block) {
  var code = 'Detection:start_stream()\n'
  return code;
};

/*simpel blockje stop stream*/
Blockly.Blocks['detection_stop_stream'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("stop vidio");
    this.setColour(330);
    this.setTooltip('stop de vidio stream');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_stop_stream'] = function(block) {
  var code = 'Detection:stop_stream()\n'
  return code;
};
