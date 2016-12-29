Blockly.Lua.addReservedWords("Camera");

Blockly.Blocks['camera_start'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Turn On Camera");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.Lua['camera_start'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = 'Camera:startSystemProcessing()\n';
  return code;
};


Blockly.Blocks['camera_stop'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Turn Off Camera");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Lua['camera_stop'] = function(block) {
  var code = 'Camera:stopSystemProcessing()\n';
  return code;
};

Blockly.Blocks['camera_refresh_rate'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Refresh Rate");
    this.setOutput(true, "Number");
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Lua['camera_refresh_rate'] = function(block) {
  var code = 'Camera:getRefreshRate()';
  return [code, Blockly.Lua.ORDER_EQUALITY];
};

Blockly.Blocks['camera_reg_facedetection'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Face detection: ")
        .appendField(new Blockly.FieldDropdown([["Enabled", "true"], ["Disabled", "false"]]), "STATUS");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
  };


Blockly.Lua['camera_reg_facedetection'] = function(block) {
  var dropdown_status = block.getFieldValue('STATUS');
  // TODO: Assemble JavaScript into code variable.
  var code = 'if(' + dropdown_status + ' == true) then\n' +
    'Camera:registerSystem("FaceTracking")\n' +
    'else\n' +
    'Camera:unregisterSystem("FaceTracking")\n'+
    'end\n';
  return code;
};

Blockly.Blocks['camera_search_face'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Search Face Position");
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("[out] found")
        .appendField(new Blockly.FieldVariable("item"), "FACE_DETECT");
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("[out] X")
        .appendField(new Blockly.FieldVariable("item"), "X");
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("[out] Y")
        .appendField(new Blockly.FieldVariable("item"), "Y");
    this.setInputsInline(false);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  },
  getVars: function() {
    return [this.getFieldValue('FACE_DETECT'),this.getFieldValue('X'),this.getFieldValue('Y')];
  }
};

Blockly.Lua['camera_search_face'] = function(block) {
  var variable_face_detect = Blockly.Lua.variableDB_.getName(block.getFieldValue('FACE_DETECT'), Blockly.Variables.NAME_TYPE);
  var variable_x = Blockly.Lua.variableDB_.getName(block.getFieldValue('X'), Blockly.Variables.NAME_TYPE);
  var variable_y = Blockly.Lua.variableDB_.getName(block.getFieldValue('Y'), Blockly.Variables.NAME_TYPE);
  // TODO: Assemble Lua into code variable.
  var code = 'face = Camera:getFaceCenter()\n' +
    'if(face == nil) then\n' +
    variable_face_detect + ' = false\n' +
    variable_x + ' = 0\n' +
    variable_y + ' = 0\n' +
    'else\n' +
    variable_face_detect + ' = true\n' +
    variable_x + ' = face[0]\n' +
    variable_y + ' = face[1]\n' +
    'end\n';
  return code;
};
