 Blockly.Lua.addReservedWords("Detection");

Blockly.Blocks['detection_follow_color'] = {
  init: function() {
    var colour = new Blockly.FieldColour('#ff0000');
    colour.setColours(['#f00','#0f0','#00f','#ff0']).setColumns(2);
    this.appendDummyInput()
        .appendField('Follow')
        .appendField(colour,'COLOUR')
        .appendField('with eyes.');
    this.appendField
    this.setColour(180);
    this.setTooltip('This will make the robot follow a certain color using his eyes. \n[Requirements: Start camera]');
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

Blockly.Blocks['detection_follow_face'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('Follow face with eyes.');
    this.appendField
    this.setColour(180);
    this.setTooltip('This will make the robot follow a face using his eyes. \n[Requirements: Start camera]');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_follow_face'] = function(block) {
  var code = '';
  code += 'coords = Detection:get_face_coords()\n';
  code += 'Detection:follow_object(coords[0],coords[1])\n';
  return code;
};

Blockly.Blocks['detection_get_coordinates_color'] = {
  init: function() {
    var colour = new Blockly.FieldColour('#ff0000');
    colour.setColours(['#f00','#0f0','#00f','#ff0']).setColumns(2);
    this.appendDummyInput()
        .appendField('Get position of')
        .appendField(colour,'COLOUR')
    this.appendField
    this.setColour(180);
    this.setTooltip('This will return a coordinate of a detected color from 0 to 350. \n[Requirements: Start camera]');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get x coordinate", "X"], ["Get y coordinate", "Y"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_color'] = function(block) {
  var color = block.getFieldValue('COLOUR')
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  if(dropdown == "Y"){
    /*code += 'if (Detection:is_color_detected("'+color+'") == null) then\n';
    code += 'print("Something went wrong. Did you perhaps forget to start the camera?")';
    code += 'end\n';
    code += 'if (Detection:is_color_detected("'+color+'") == false) then\n';
    code += 'print("No color with hexcode '+color+' detected. Make sure to use an if block to see if a color is detected.")';
    code += 'end\n';*/
    code += 'Detection:get_color_coord_y("'+color+'")\n';
  }else if(dropdown == "X"){
    /*code += 'if (Detection:is_color_detected("'+color+'") == null) then\n';
    code += 'print("Something went wrong. Did you perhaps forget to start the camera? (or did you get an error earlier in the script?)")';
    code += 'end\n';*/
    code += 'Detection:get_color_coord_x("'+color+'")\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
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
    this.setColour(180);
    this.setTooltip('This will detect if a certain color is detected.');
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
  //code += 'if (Detection:is_color_detected("'+color+'") == null) then\n';
  //code += 'print("Something went wrong. Did you perhaps forget to start the camera? (or did you get an error earlier in the script?)")';
  //code += 'end\n';
  //code += 'if Detection:is_color_detected("'+color+'") then\n';
  //code += statements_body;
  //code += 'end\n';
  code += 'print(Detection:is_color_detected("'+color+'"))\n'
  return code;
};

Blockly.Blocks['detection_face_check'] = {
  init: function() {
    var colour = new Blockly.FieldColour('#ff0000');
    colour.setColours(['#f00','#0f0','#00f','#ff0']).setColumns(2);
    this.appendDummyInput()
        .appendField('If face is detected.');
    this.appendField
    this.setColour(180);
    this.setTooltip('This will detect if a face is detected.');
    this.appendStatementInput('BODY')
    .appendField('do');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_face_check'] = function(block) {
  var statements_body = Blockly.Lua.statementToCode(block, 'BODY');
  var color = block.getFieldValue('COLOUR')
  this.setFieldValue(color,'COLOUR')
  var code = '';
  //code += 'if (Detection:is_face_detected() == null) then\n';
  //code += 'print("Something went wrong. Did you perhaps forget to start the camera? (or did you get an error earlier in the script?)")';
  //code += 'end\n';
  //code += 'if Detection:is_face_detected() then\n';
  //code += statements_body;
  //code += 'end\n';
  code += 'print(Detection:is_face_detected())\n'
  return code;
};

Blockly.Blocks['detection_start_stream'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/start-flag.png", 16, 18, ""))
        .appendField("Start camera");
    this.setColour(180);
    this.setTooltip('This will start the camera. The camera takes 1 second to warm up the videostream. When the camera warmup is done, it ll automatically continue to the next code. \nIMPORTANT: This code is needed to use any other block in Detection.');
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
        .appendField(new Blockly.FieldImage("static/icons/stop-flag.png", 16, 18, ""))
        .appendField("Stop camera");
    this.setColour(180);
    this.setTooltip('This will stop the camera from streaming. This will save CPU power, but wont give a possibility to run any other detection code. \n[Requirements: Start camera]');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_stop_stream'] = function(block) {
  var code = ''
  code += 'Detection:stop_stream()\n'
  return code;
};

Blockly.Blocks['detection_get_coordinates_face'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('Get position of face');
    this.appendField
    this.setColour(180);
    this.setTooltip('This will return a coordinate of a detected face from 0 to 350. \n[Requirements: Start camera]');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get x coordinate", "X"], ["Get y coordinate", "Y"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  if(dropdown == "Y"){
    code = 'Detection:get_face_coord_y()\n';
  }else if(dropdown == "X"){
    code = 'Detection:get_face_coord_x()\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['detection_start_predictor'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/exc-mark.png", 16, 18, ""))
        .appendField("Initialize face predictor.");
    this.setColour(180);
    this.setTooltip('This will start initializing a big file which is a face predictor. This needs to be initialized to mirror a facial expression (Mirror face). This only has to be called once.');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_start_predictor'] = function(block) {
  var code = ''
  //code += 'if (Detection:initialize_predictor() == null) then\n';
  //code += 'print("Something went wrong. There is a corrupt file path inside the filesystem. Contact a developer for more info.")\n';
  //code += 'else Detection:initialize_predictor()\n'
  code += 'Detection:initialize_predictor()\n'
  //code += 'end\n';
  return code;
};


Blockly.Blocks['detection_get_coordinates_face_nose'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('Get position of nose');
    this.appendField
    this.setColour(180);
    this.setTooltip('This will return a coordinate of a detected nose from 0 to 350. \n[Requirements: Start camera]');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get x coordinate", "X"], ["Get y coordinate", "Y"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face_nose'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  if(dropdown == "Y"){
    code = 'Detection:receive_face_points(30,"y")\n';
  }else if(dropdown == "X"){
    code = 'Detection:receive_face_points(30,"x")\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['detection_get_coordinates_face_outer_right_eb'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('Get position of outer right eyebrow');
    this.appendField
    this.setColour(180);
    this.setTooltip('This will return a coordinate of a detected outer point of the right eyebrow from 0 to 350. \n[Requirements: Start camera]');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get x coordinate", "X"], ["Get y coordinate", "Y"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face_outer_right_eb'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  if(dropdown == "Y"){
    code = 'Detection:receive_face_points(17,"y")\n';
  }else if(dropdown == "X"){
    code = 'Detection:receive_face_points(17,"x")\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['detection_get_coordinates_face_inner_right_eb'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('Get position of inner right eyebrow');
    this.appendField
    this.setColour(180);
    this.setTooltip('This will return a coordinate of a detected inner point of the right eyebrow from 0 to 350. \n[Requirements: Start camera]');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get x coordinate", "X"], ["Get y coordinate", "Y"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face_inner_right_eb'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  if(dropdown == "Y"){
    code = 'Detection:receive_face_points(21,"y")\n';
  }else if(dropdown == "X"){
    code = 'Detection:receive_face_points(21,"x")\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['detection_get_coordinates_face_outer_left_eb'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('Get position of outer left eyebrow');
    this.appendField
    this.setColour(180);
    this.setTooltip('This will return a coordinate of a detected outer point of the left eyebrow from 0 to 350. \n[Requirements: Start camera]');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get x coordinate", "X"], ["Get y coordinate", "Y"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face_outer_left_eb'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  if(dropdown == "Y"){
    code = 'Detection:receive_face_points(26,"y")\n';
  }else if(dropdown == "X"){
    code = 'Detection:receive_face_points(26,"x")\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['detection_get_coordinates_face_inner_left_eb'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('Get position of inner left eyebrow');
    this.appendField
    this.setColour(180);
    this.setTooltip('This will return a coordinate of a detected inner point of the left eyebrow from 0 to 350. \n[Requirements: Start camera]');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get x coordinate", "X"], ["Get y coordinate", "Y"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face_inner_left_eb'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  if(dropdown == "Y"){
    code = 'Detection:receive_face_points(22,"y")\n';
  }else if(dropdown == "X"){
    code = 'Detection:receive_face_points(22,"x")\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['detection_get_coordinates_face_left_mouth'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('Get position of left mouth');
    this.appendField
    this.setColour(180);
    this.setTooltip('This will return a coordinate of a detected left point of the mouth from 0 to 350. \n[Requirements: Start camera]');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get x coordinate", "X"], ["Get y coordinate", "Y"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face_left_mouth'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  if(dropdown == "Y"){
    code = 'Detection:receive_face_points(54,"y")\n';
  }else if(dropdown == "X"){
    code = 'Detection:receive_face_points(54,"x")\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['detection_get_coordinates_face_right_mouth'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('Get position of right mouth');
    this.appendField
    this.setColour(180);
    this.setTooltip('This will return a coordinate of a detected right point of the mouth from 0 to 350. \n[Requirements: Start camera]');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get x coordinate", "X"], ["Get y coordinate", "Y"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face_right_mouth'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  if(dropdown == "Y"){
    code = 'Detection:receive_face_points(60,"y")\n';
  }else if(dropdown == "X"){
    code = 'Detection:receive_face_points(60,"x")\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};


Blockly.Blocks['detection_get_coordinates_face_lower_mouth'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('Get position of lower mouth');
    this.appendField
    this.setColour(180);
    this.setTooltip('This will return a coordinate of a detected lowest point of the mouth from 0 to 350. \n[Requirements: Start camera]');
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([["Get x coordinate", "X"], ["Get y coordinate", "Y"]]), "DROPDOWN");
    this.setOutput(true, 'Number');
  }
};
Blockly.Lua['detection_get_coordinates_face_lower_mouth'] = function(block) {
  var dropdown = block.getFieldValue('DROPDOWN');
  var code = '';
  if(dropdown == "Y"){
    code = 'Detection:receive_face_points(66,"y")\n';
  }else if(dropdown == "X"){
    code = 'Detection:receive_face_points(66,"x")\n';
  }
  return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};

Blockly.Blocks['detection_mirror_face'] = {
  init: function() {
    this.appendDummyInput()
        .appendField('Mirror detected face.');
    this.appendField
    this.setColour(180);
    this.setTooltip('This will make the robot copy your facial expressions. \n[Requirements: Start camera, Initialize face predictor, Initialize all servos, Put all servos on]');
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Lua['detection_mirror_face'] = function(block) {
  var code = '';
  code += 'print(Detection:aanpassen_face())\n';
  return code;
};
