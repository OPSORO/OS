Blockly.Lua.addReservedWords("UI");

Blockly.Blocks['interface_init'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-gamepad.png", 16, 18, ""))
        .appendField("Initialize interface");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(300);
    this.setTooltip('Initialize the user interface. This creates a new button in the toolbar to open the script UI.');
  }
};
Blockly.Lua['interface_init'] = function(block) {
  var code = 'UI:init()\n';
  return code;
};

Blockly.Blocks['interface_addbutton'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-gamepad.png", 16, 18, ""))
        .appendField("Add button")
        .appendField(new Blockly.FieldTextInput("Press Me!"), "NAME")
        .appendField("with icon")
        .appendField(new Blockly.FieldTextInput("fa-heart"), "ICON");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(300);
    this.setTooltip('Add a button to the interface.');
  }
};
Blockly.Lua['interface_addbutton'] = function(block) {
  var text_name = block.getFieldValue('NAME');
  var text_icon = block.getFieldValue('ICON');

  var identifier = text_name;
  identifier = identifier.toUpperCase();
  identifier = identifier.replace(/[^\w\s]/g, "");
  identifier = identifier.replace(/\s{1,}/g, "_");

  var code = 'UI:add_button("' + identifier + '", "' + text_name + '", "' + text_icon + '")\n';
  return code;
};

Blockly.Blocks['interface_addtogglebutton'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-gamepad.png", 16, 18, ""))
        .appendField("Add toggle button")
        .appendField(new Blockly.FieldTextInput("Toggle Me!"), "NAME")
        .appendField("with icon")
        .appendField(new Blockly.FieldTextInput("fa-rocket"), "ICON");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(300);
    this.setTooltip('Add a toggle button to the interface.');
  }
};
Blockly.Lua['interface_addtogglebutton'] = function(block) {
  var text_name = block.getFieldValue('NAME');
  var text_icon = block.getFieldValue('ICON');

  var identifier = text_name;
  identifier = identifier.toUpperCase();
  identifier = identifier.replace(/[^\w\s]/g, "");
  identifier = identifier.replace(/\s{1,}/g, "_");

  var code = 'UI:add_button("' + identifier + '", "' + text_name + '", "' + text_icon + '", true)\n';
  return code;
};

Blockly.Blocks['interface_addkey'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-gamepad.png", 16, 18, ""))
        .appendField("Add keyboard key")
        .appendField(new Blockly.FieldDropdown([["up", "up"], ["down", "down"], ["left", "left"], ["right", "right"], ["space", "space"]]), "KEY");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(300);
    this.setTooltip('Add a listener for a special key to the interface.');
  }
};
Blockly.Lua['interface_addkey'] = function(block) {
  var dropdown_key = block.getFieldValue('KEY');
  var code = 'UI:add_key("' + dropdown_key + '")\n';
  return code;
};

Blockly.Blocks['interface_addkey2'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-gamepad.png", 16, 18, ""))
        .appendField("Add keyboard key")
        .appendField(new Blockly.FieldTextInput("a"), "KEY");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(300);
    this.setTooltip('Add a listener for a letter key to the interface.');
  }
};
Blockly.Lua['interface_addkey2'] = function(block) {
  var text_key = block.getFieldValue('KEY');
  var code = 'UI:add_key("' + dropdown_key + '")\n';
  return code;
};

Blockly.Blocks['interface_keypress'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-gamepad.png", 16, 18, ""))
        .appendField("When key")
        .appendField(new Blockly.FieldDropdown(interface_keypress_dd), "KEY")
        .appendField("is")
        .appendField(new Blockly.FieldDropdown([["pressed", "PRESSED"], ["released", "RELEASED"]]), "PR_REL");
    this.appendStatementInput("BODY");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(300);
    this.setTooltip('');
  }
};
function interface_keypress_dd(){
  var keys1 = window.parent.find_block_values("interface_addkey", "KEY");
  var keys2 = window.parent.find_block_values("interface_addkey2", "KEY");

  var keys = keys1.concat(keys2);

  if(keys.length == 0){
    return [["No keys defined!", "ERROR"]];
  }

  var ret = []
  $(keys).each(function(idx, elem){
    ret.push([elem, elem]);
  });

  return ret;
}
Blockly.Lua['interface_keypress'] = function(block) {
  var dropdown_key = block.getFieldValue('KEY');
  var dropdown_pr_rel = block.getFieldValue('PR_REL');
  var statements_body = Blockly.Lua.statementToCode(block, 'BODY');

  var identifier = dropdown_key.toUpperCase();

  var code = '';

  if(dropdown_pr_rel == "PRESSED"){
    code += 'if rising_edge("' + identifier + '", UI:is_key_pressed("' + dropdown_key + '")) then\n';
    code += statements_body;
    code += 'end\n';
  }else{
    code += 'if falling_edge("' + identifier + '", UI:is_key_pressed("' + dropdown_key + '")) then\n';
    code += statements_body;
    code += 'end\n';
  }

  return code;
};

Blockly.Blocks['interface_buttonpress'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-gamepad.png", 16, 18, ""))
        .appendField("When button")
        .appendField(new Blockly.FieldDropdown(interface_buttonpress_dd), "BUTTON")
        .appendField("is")
        .appendField(new Blockly.FieldDropdown([["pressed", "PRESSED"], ["released", "RELEASED"]]), "PR_REL");
    this.appendStatementInput("BODY");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(300);
    this.setTooltip('');
  }
};
function interface_buttonpress_dd(){
  var buttons1 = window.parent.find_block_values("interface_addbutton", "NAME");
  var buttons2 = window.parent.find_block_values("interface_addtogglebutton", "NAME");
  var buttons = buttons1.concat(buttons2);
  if(buttons.length == 0){
    return [["No buttons defined!", "ERROR"]];
  }

  var ret = []
  $(buttons).each(function(idx, elem){
    ret.push([elem, elem]);
  });

  return ret;
}
Blockly.Lua['interface_buttonpress'] = function(block) {
  var dropdown_button = block.getFieldValue('BUTTON');
  var dropdown_pr_rel = block.getFieldValue('PR_REL');
  var statements_body = Blockly.Lua.statementToCode(block, 'BODY');

  var identifier = dropdown_button;
  identifier = identifier.toUpperCase();
  identifier = identifier.replace(/[^\w\s]/g, "");
  identifier = identifier.replace(/\s{1,}/g, "_");

  var code = '';
  if(dropdown_pr_rel == "PRESSED"){
    code += 'if rising_edge("' + identifier + '", UI:is_button_pressed("' + identifier + '")) then\n';
    code += statements_body;
    code += 'end\n';
  }else{
    code += 'if falling_edge("' + identifier + '", UI:is_button_pressed("' + identifier + '")) then\n';
    code += statements_body;
    code += 'end\n';
  }

  return code;
};

Blockly.Blocks['interface_is_key_pressed'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Is key ")
        .appendField(new Blockly.FieldDropdown(interface_keypress_dd), "KEY")
        .appendField("pressed?");
    this.setOutput(true, "Boolean");
    this.setColour(300);
    this.setTooltip('Returns true if a key is pressed.');
  }
};
Blockly.Lua['interface_is_key_pressed'] = function(block) {
  var dropdown_key = block.getFieldValue('KEY');
  var identifier = dropdown_key.toUpperCase();
  var code = 'UI:is_key_pressed("' + identifier + '")';
  return [code, Blockly.Lua.ORDER_ATOMIC];
};

Blockly.Blocks['interface_is_button_pressed'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Is button ")
        .appendField(new Blockly.FieldDropdown(interface_buttonpress_dd), "BUTTON")
        .appendField("pressed?");
    this.setOutput(true, "Boolean");
    this.setColour(300);
    this.setTooltip('Returns true if a button is pressed.');
  }
};
Blockly.Lua['interface_is_button_pressed'] = function(block) {
  var dropdown_button = block.getFieldValue('BUTTON');

  var identifier = dropdown_button;
  identifier = identifier.toUpperCase();
  identifier = identifier.replace(/[^\w\s]/g, "");
  identifier = identifier.replace(/\s{1,}/g, "_");

  var code = 'UI:is_button_pressed("' + identifier + '")';
  return [code, Blockly.Lua.ORDER_ATOMIC];
};
