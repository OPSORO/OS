Blockly.Lua.addReservedWords("Face");

Blockly.Blocks['face_eye_openclose'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Set ");
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["left","LEFT"], ["right","RIGHT"], ["both","BOTH"]]), "EYE_SELECT");
    this.appendDummyInput()
        .appendField("eye");
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["open","open"], ["close","close"]]), "EYE_POS");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(180);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Lua['face_eye_openclose'] = function(block) {
  var dropdown_eye_select = block.getFieldValue('EYE_SELECT');
  var dropdown_eye_pos = block.getFieldValue('EYE_POS');
  var code = '';
  if( dropdown_eye_select == 'LEFT'){
    var code = 'Robot:execute{action="'+ dropdown_eye_pos+ '",tags={"eye","left"}' + '}\n';
  }
  else if (dropdown_eye_select == 'RIGHT') {
    var code = 'Robot:execute{action="'+ dropdown_eye_pos+ '",tags={"eye","right"}' + '}\n';
  }
  else{
    var code = 'Robot:execute{action="'+ dropdown_eye_pos+ '",tags={"eye"}' + '}\n';
  }
  return code;
};

Blockly.Blocks['face_eye_set'] = {
  init: function() {
    this.appendValueInput("DOF_VALUE")
        .setCheck("Number")
        .appendField("Set ")
        .appendField(new Blockly.FieldDropdown([["left","LEFT"], ["right","RIGHT"], ["both","BOTH"]]), "EYE_SELECT")
        .appendField("eye");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(180);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Lua['face_eye_set'] = function(block) {
  var dropdown_eye_select = block.getFieldValue('EYE_SELECT');
  var value_dof_value = Blockly.Lua.valueToCode(block, 'DOF_VALUE', Blockly.Lua.ORDER_ATOMIC);
  var code = '';
  if( dropdown_eye_select == 'LEFT'){
    var code = 'Robot:execute{action="set",tags={"eye","left"},value='+ value_dof_value + '}\n';
  }
  else if (dropdown_eye_select == 'RIGHT') {
    var code = 'Robot:execute{action="set",tags={"eye","right"},value='+ value_dof_value + '}\n';
  }
  else{
    var code = 'Robot:execute{action="set",tags={"eye"},value='+ value_dof_value + '}\n';
  }
  return code;
};

Blockly.Blocks['face_look_at'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Look at: ");
    this.appendValueInput("HOR")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Horizontal: ");
    this.appendValueInput("VERT")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Vertical: ");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(180);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Lua['face_look_at'] = function(block) {
  var value_hor = Blockly.Lua.valueToCode(block, 'HOR', Blockly.Lua.ORDER_ATOMIC);
  var value_ver = Blockly.Lua.valueToCode(block, 'VERT', Blockly.Lua.ORDER_ATOMIC);
  var code = 'Robot:execute{action="look_at",tags={"eye"},hor='+ value_hor + ',vert='+ value_ver+ '}\n';
  return code;
};


Blockly.Blocks['face_mouth_set'] = {
  init: function() {
    this.appendValueInput("DOF_VALUE")
        .setCheck("Number")
        .appendField("Set mouth ");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(180);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Lua['face_mouth_set'] = function(block) {
  var value_dof_value = Blockly.Lua.valueToCode(block, 'DOF_VALUE', Blockly.Lua.ORDER_ATOMIC);
  // TODO: Assemble Lua into code variable.
  var code = 'Robot:execute{action="set",tags={"mouth"},value='+ value_dof_value + '}\n';
  return code;
};

Blockly.Blocks['face_eyebrow_set'] = {
  init: function() {
    this.appendValueInput("DOF_VALUE")
        .setCheck("Number")
        .appendField("Set eyebrow");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(180);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Lua['face_eyebrow_set'] = function(block) {
  var value_dof_value = Blockly.Lua.valueToCode(block, 'DOF_VALUE', Blockly.Lua.ORDER_ATOMIC);
  var code = 'Robot:execute{action="set",tags={"eyebrow"},value='+ value_dof_value + '}\n';
  return code;
};

Blockly.Blocks['face_reset'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Reset all modules");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(180);
    this.setTooltip('Reset all modules (wheels to)');
    this.setHelpUrl('');
  }
};

Blockly.Lua['face_reset'] = function(block) {
  var code = 'Robot:reset_dofs()\n';
  return code;
};
