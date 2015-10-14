Blockly.Blocks['interface_init'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-gamepad.png", 16, 18, ""))
        .appendField("Initialize interface");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(300);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['interface_init'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
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
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['interface_addbutton'] = function(block) {
  var text_name = block.getFieldValue('NAME');
  var text_icon = block.getFieldValue('ICON');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
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
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['interface_addtogglebutton'] = function(block) {
  var text_name = block.getFieldValue('NAME');
  var text_icon = block.getFieldValue('ICON');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['interface_addkey'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-gamepad.png", 16, 18, ""))
        .appendField("Add keyboard key")
        .appendField(new Blockly.FieldDropdown([["up", "UP"], ["down", "DOWN"], ["left", "LEFT"], ["right", "RIGHT"], ["space", "SPACE"]]), "KEY");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(300);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['interface_addkey'] = function(block) {
  var dropdown_key = block.getFieldValue('KEY');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
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
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['interface_addkey2'] = function(block) {
  var text_key = block.getFieldValue('KEY');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['interface_keypress'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-gamepad.png", 16, 18, ""))
        .appendField("When key")
        .appendField(new Blockly.FieldDropdown([["option", "OPTIONNAME"], ["option", "OPTIONNAME"], ["option", "OPTIONNAME"]]), "KEY")
        .appendField("is")
        .appendField(new Blockly.FieldDropdown([["pressed", "PRESSED"], ["released", "RELEASED"]]), "PR_REL");
    this.appendStatementInput("NAME");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(300);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['interface_keypress'] = function(block) {
  var dropdown_key = block.getFieldValue('KEY');
  var dropdown_pr_rel = block.getFieldValue('PR_REL');
  var statements_name = Blockly.JavaScript.statementToCode(block, 'NAME');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['interface_buttonpress'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-gamepad.png", 16, 18, ""))
        .appendField("When button")
        .appendField(new Blockly.FieldDropdown([["option", "OPTIONNAME"], ["option", "OPTIONNAME"], ["option", "OPTIONNAME"]]), "BUTTON")
        .appendField("is")
        .appendField(new Blockly.FieldDropdown([["pressed", "PRESSED"], ["released", "RELEASED"]]), "PR_REL");
    this.appendStatementInput("NAME");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(300);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['interface_buttonpress'] = function(block) {
  var dropdown_button = block.getFieldValue('BUTTON');
  var dropdown_pr_rel = block.getFieldValue('PR_REL');
  var statements_name = Blockly.JavaScript.statementToCode(block, 'NAME');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};
