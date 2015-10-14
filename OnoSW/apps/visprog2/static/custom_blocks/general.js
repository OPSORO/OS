// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#eib9jj
Blockly.Blocks['general_onsetup'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("When script is started");
    this.appendStatementInput("BODY");
    this.setColour(330);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['general_onsetup'] = function(block) {
  var statements_name = Blockly.JavaScript.statementToCode(block, 'BODY');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['general_onloop'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("On loop");
    this.appendStatementInput("BODY");
    this.setColour(330);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['general_onloop'] = function(block) {
  var statements_name = Blockly.JavaScript.statementToCode(block, 'BODY');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['general_onquit'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("When script is stopped");
    this.appendStatementInput("BODY");
    this.setColour(330);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['general_onquit'] = function(block) {
  var statements_name = Blockly.JavaScript.statementToCode(block, 'BODY');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['general_sleep'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(290);
		this.appendDummyInput()
		.appendField("Wait");
		this.appendValueInput("TIME")
		.setCheck("Number");
		this.appendDummyInput()
		.appendField("seconds");
		this.setInputsInline(true);
		this.setPreviousStatement(true);
		this.setNextStatement(true);
		this.setTooltip('');
	}
};
Blockly.JavaScript['general_sleep'] = function(block) {
	var value_time = Blockly.JavaScript.valueToCode(block, 'TIME', Blockly.JavaScript.ORDER_ATOMIC)  || "0";
	var code = "sleep(" + value_time + ");\n";
	return code;
};
Blockly.JavaScript.addReservedWords("sleep");
Blockly.JavaScript.addReservedWords("delay");

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#vkifu3
Blockly.Blocks['general_seconds'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(290);
		this.appendDummyInput()
		.appendField("Elapsed time");
		this.setOutput(true, "Number");
		this.setTooltip('Returns the elapsed time in seconds.');
	}
};
Blockly.JavaScript['general_seconds'] = function(block) {
	var code = "seconds()";
	return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];
};
Blockly.JavaScript.addReservedWords("seconds");
