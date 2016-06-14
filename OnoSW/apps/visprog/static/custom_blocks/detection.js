Blockly.Lua.addReservedWords("Detection");

Blockly.Blocks['detection_follow_color'] = {
  init: function() {
    var colour = new Blockly.FieldColour('#ff0000');
    colour.setColours(['#f00','#0f0','#00f','#ff0']).setColumns(2);
    this.appendDummyInput()
        .appendField('If')
        .appendField(colour,'COLOUR')
        .appendField('is detected.');
    this.appendField
    this.setColour(330);
    this.setTooltip('This will make the robot look at a certain color and follow it with his eyes.');
    this.appendDummyInput()
        .appendField('Follow color with eyes');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};

Blockly.Lua['detection_follow_color'] = function(block) {
  var color = block.getFieldValue('COLOUR')
  var code = '';
  code += 'if (Detection:is_color_detected("'+color+'") == null) then\n';
  code += 'print("Something went wrong. Did you perhaps forget to start the camera? (or did you get an error earlier in the script?)")';
  code += 'end\n';
  code += 'if Detection:is_color_detected("'+color+'") then\n';
  code += 'x = Detection:get_color_coord_x("'+color+'")\n';
  code += 'y = Detection:get_color_coord_y("'+color+'")\n';
  code += 'Detection:follow_object(x,y)\n';
  code += 'end\n';
  return code;
};

Blockly.Blocks['detection_get_coordinates_color'] = {
  init: function() {
    var colour = new Blockly.FieldColour('#ff0000');
    colour.setColours(['#f00','#0f0','#00f','#ff0']).setColumns(2);
    this.appendDummyInput()
        .appendField('If')
        .appendField(colour,'COLOUR')
        .appendField('is detected.');
    this.appendField
    this.setColour(330);
    this.setTooltip('This block will return the coordinates of a detected color.');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get y value", "Y"], ["Get x value", "X"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_color'] = function(block) {
  var color = block.getFieldValue('COLOUR')
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  if(dropdown == "Y"){
    code += 'if (Detection:is_color_detected("'+color+'") == null) then\n';
    code += 'print("Something went wrong. Did you perhaps forget to start the camera?")';
    code += 'end\n';
    code += 'if (Detection:is_color_detected("'+color+'") == false) then\n';
    code += 'print("No color with hexcode '+color+' detected. Make sure to use an if block to see if a color is detected.")';
    code += 'end\n';
    code = 'Detection:get_coord_y("'+color+'")\n';
  }else if(dropdown == "X"){
    code += 'if (Detection:is_color_detected("'+color+'") == null) then\n';
    code += 'print("Something went wrong. Did you perhaps forget to start the camera? (or did you get an error earlier in the script?)")';
    code += 'end\n';
    code = 'Detection:get_coord_x("'+color+'")\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['detection_get_coordinates_face'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Follow face with eyes");
    this.setColour(330);
    this.setTooltip('This will make the robot look at a face and follow it with his eyes.');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_get_coordinates_face'] = function(block) {
  var code = '';
  code += 'if (Detection:is_face_detected() == null) then\n';
  code += 'print("Something went wrong. Did you perhaps forget to start the camera? (or did you get an error earlier in the script?)")';
  code += 'end\n';
  code += 'if (Detection:is_face_detected("'+color+'") == false) then\n';
  code += 'print("No faces detected. Make sure to use an if block to see if a face is detected.")';
  code += 'end\n';
  code += 'x = Detection:get_face_coord_x()\n';
  code += 'y = Detection:get_face_coord_y()\n';
  code += 'Detection:follow_object(x,y)\n';
  return code;
};

Blockly.Blocks['detection_color_check'] = {
  init: function() {
    var colour = new Blockly.FieldColour('#ff0000');
    colour.setColours(['#f00','#0f0','#00f','#ff0']).setColumns(2);
    this.appendDummyInput()
        .appendField('If')
        .appendField(colour,'COLOUR')
        .appendField('is detected.');
    this.appendField
    this.setColour(330);
    this.setTooltip('This block will check if the chosen color is detected.');
    this.appendStatementInput('BODY')
    .appendField('do');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_color_check'] = function(block) {
  var statements_body = Blockly.Lua.statementToCode(block, 'BODY');
  var color = block.getFieldValue('COLOUR')
  this.setFieldValue(color,'COLOUR')
  var code = '';
  code += 'if (Detection:is_color_detected("'+color+'") == null) then\n';
  code += 'print("Something went wrong. Did you perhaps forget to start the camera? (or did you get an error earlier in the script?)")';
  code += 'end\n';
  code += 'if Detection:is_color_detected("'+color+'") then\n';
  code += statements_body;
  code += 'end\n';
  return code;
};

Blockly.Blocks['detection_start_stream'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Start camera");
    this.setColour(330);
    this.setTooltip('This will start the camera.');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_start_stream'] = function(block) {
  var code = '';
  code += 'if (Detection:start_stream() == null) then\n';
  code += 'print("Something went wrong. Is the camera broken, disabled or disconnected? (or did you get an error earlier in the script?)")\n';
  code += 'else Detection:start_stream()\n'
  code += 'end\n';
  return code;
};

Blockly.Blocks['detection_stop_stream'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Stop camera");
    this.setColour(330);
    this.setTooltip('This will stop the camera. IMPORTANT: This is required for optimal experience.');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_stop_stream'] = function(block) {
  var code = 'Detection:stop_stream()\n'
  code += 'if (Detection:stop_stream() == null) then\n';
  code += 'print("Something went wrong. Is the camera broken, disabled or disconnected? (or did you get an error earlier in the script?)")';
  code += 'end\n';
  return code;
};

/*---------- nog testen me een bakes ----------*/
Blockly.Blocks['detection_get_coordinates_face'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('If face is detected');
    this.appendField
    this.setColour(330);
    this.setTooltip('This block can do something with colors');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get y waarde", "Y"], ["Get x waarde", "X"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  if(dropdown == "Y"){
    code = 'Detection:get_face_coord_x()\n';
  }else if(dropdown == "X"){
    code = 'Detection:get_face_coord_y()\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['detection_initialize_predictor'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Start predicting faces");
    this.setColour(330);
    this.setTooltip('This will start loading a script that will predict possible faces and gather their coordinates. THIS IS NEEDED FOR OTHER FACE RELATED CODING!');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_initialize_predictor'] = function(block) {
  var code = ''
  code += 'if (Detection:initialize_predictor() == null) then\n';
  code += 'print("Something went wrong. There is a corrupt file path inside the filesystem. Contact a developer for more info.")\n';
  code += 'else Detection:initialize_predictor()\n'
  code += 'end\n';
  return code;
};


Blockly.Blocks['detection_get_coordinates_face_nose'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('If nose is detected');
    this.appendField
    this.setColour(330);
    this.setTooltip('This block can do something with colors');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get y waarde", "Y"], ["Get x waarde", "X"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face_nose'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  code += 'coords = Detection:receive_face_points(30)\n';
  if(dropdown == "Y"){
    code = 'return coords[0]\n';
  }else if(dropdown == "X"){
    code = 'return coords[1]\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['detection_get_coordinates_face_outer_left_eb'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('If outer eyebrouw point+20 is detected');
    this.appendField
    this.setColour(330);
    this.setTooltip('This block can do something with colors');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get y waarde", "Y"], ["Get x waarde", "X"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face_outer_left_eb'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  code += 'coords = Detection:receive_face_points(17)\n';
  if(dropdown == "Y"){
    code = 'return coords[0]\n';
  }else if(dropdown == "X"){
    code = 'return coords[1]\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['detection_get_coordinates_face_inner_left_eb'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('If inner eyebrouw point is detected');
    this.appendField
    this.setColour(330);
    this.setTooltip('This block can do something with colors');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get y waarde", "Y"], ["Get x waarde", "X"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face_inner_left_eb'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  code += 'coords = Detection:receive_face_points(21)\n';
  if(dropdown == "Y"){
    code = 'return coords[0]\n';
  }else if(dropdown == "X"){
    code = 'return coords[1]\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['detection_get_coordinates_face_outer_right_eb'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('If outer eyebrouwpoint is detected');
    this.appendField
    this.setColour(330);
    this.setTooltip('This block can do something with colors');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get y waarde", "Y"], ["Get x waarde", "X"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face_outer_right_eb'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  code += 'coords = Detection:receive_face_points(26)\n';
  if(dropdown == "Y"){
    code = 'return coords[0]\n';
  }else if(dropdown == "X"){
    code = 'return coords[1]\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['detection_get_coordinates_face_inner_right_eb'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('If inner eyebrouw point is detected');
    this.appendField
    this.setColour(330);
    this.setTooltip('This block can do something with colors');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get y waarde", "Y"], ["Get x waarde", "X"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face_outer_right_eb'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  code += 'coords = Detection:receive_face_points(22)\n';
  if(dropdown == "Y"){
    code = 'return coords[0]\n';
  }else if(dropdown == "X"){
    code = 'return coords[1]\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};














Blockly.Blocks['detection_get_coordinates_face_right_mouth'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('If right mout point is detected');
    this.appendField
    this.setColour(330);
    this.setTooltip('This block can do something with colors');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get y waarde", "Y"], ["Get x waarde", "X"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face_right_mouth'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  code += 'coords = Detection:receive_face_points(22)\n';
  if(dropdown == "Y"){
    code = 'return coords[0]\n';
  }else if(dropdown == "X"){
    code = 'return coords[1]\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['detection_get_coordinates_face_left_mouth'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('If left mouth point is detected');
    this.appendField
    this.setColour(330);
    this.setTooltip('This block can do something with colors');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get y waarde", "Y"], ["Get x waarde", "X"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face_left_mouth'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  code += 'coords = Detection:receive_face_points(22)\n';
  if(dropdown == "Y"){
    code = 'return coords[0]\n';
  }else if(dropdown == "X"){
    code = 'return coords[1]\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['detection_get_coordinates_face_upper_mouth'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('If upper lip is detected');
    this.appendField
    this.setColour(330);
    this.setTooltip('This block can do something with colors');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get y waarde", "Y"], ["Get x waarde", "X"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face_upper_mouth'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  code += 'coords = Detection:receive_face_points(22)\n';
  if(dropdown == "Y"){
    code = 'return coords[0]\n';
  }else if(dropdown == "X"){
    code = 'return coords[1]\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['detection_get_coordinates_face_lower_mouth'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('If lower lip is detected');
    this.appendField
    this.setColour(330);
    this.setTooltip('This block can do something with colors');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get y waarde", "Y"], ["Get x waarde", "X"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face_lower_mouth'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  code += 'coords = Detection:receive_face_points(22)\n';
  if(dropdown == "Y"){
    code = 'return coords[0]\n';
  }else if(dropdown == "X"){
    code = 'return coords[1]\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};





Blockly.Blocks['detection_mirror_face'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('Mirror face');
    this.appendField
    this.setColour(330);
    this.setTooltip('This block can do something with colors');
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_mirror_face'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  code += 'coords = Detection:receive_face_points(22)\n';
  if(dropdown == "Y"){
    code = 'return coords[0]\n';
  }else if(dropdown == "X"){
    code = 'return coords[1]\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};
>>>>>>> Blockly blocks toegevoegd
