Blockly.Lua.addReservedWords("Detection");

Blockly.Blocks['detection_follow'] = {
  init: function() {
    var colour = new Blockly.FieldColour('#ff0000');
    colour.setColours(['#f00','#0f0','#00f','#ff0']).setColumns(2);
    this.appendDummyInput()
        .appendField('If')
        .appendField(colour,'COLOUR')
        .appendField('is detected.');
    this.appendField
    this.setColour(330);
    this.setTooltip('This will make the robot follow a color, using his eyes.');
    this.appendDummyInput()
        .appendField('Follow it');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_follow'] = function(block) {
  var color = block.getFieldValue('COLOUR')
  var code = '';
  code += 'if Detection:is_color("'+color+'") then\n';
  code += 'x = Detection:get_coord_x("'+color+'")\n';
  code += 'y = Detection:get_coord_y("'+color+'")\n';
  code += 'Detection:folow_object(x,y)\n';
  code += 'end\n';
  return code;
};

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
    this.setTooltip('This statement will check for coordinates of a certain color.');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get y value", "Y"], ["Get x value", "X"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
    //this.setPreviousStatement(true);
    //this.setNextStatement(true);
  }
};
Blockly.Lua['detection_get_coordinates'] = function(block) {
  var color = block.getFieldValue('COLOUR')
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  code += 'if Detection:is_color("'+color+'") then\n';
  if(dropdown == "Y"){
    code += 'return Detection:get_coord_y("'+color+'")\n';
  }else if(dropdown == "X"){
    code += 'Detection:get_coord_x("'+color+'")\n';
  }
  code += 'end\n';
  return code
};

Blockly.Blocks['detection_get_coordinates_face'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Eyes follow face");
    this.setColour(330);
    this.setTooltip('This will make the robot follow a face, using his eyes.');
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
    this.setTooltip('This block will check if the robot detects a certain color.');
    this.appendStatementInput('BODY')
    .appendField('do');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_colorCheck'] = function(block) {
  var statements_body = Blockly.Lua.statementToCode(block, 'BODY');
  var color = block.getFieldValue('COLOUR')
  this.setFieldValue(color,'COLOUR')
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
        .appendField("Start camera");
    this.setColour(330);
    this.setTooltip('This will start the camera for further actions.');
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
        .appendField("Stop camera");
    this.setColour(330);
    this.setTooltip('This will stop the camera. THIS IS IMPORTANT!');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_stop_stream'] = function(block) {
  var code = 'Detection:stop_stream()\n'
  return code;
};
