// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#eib9jj
Blockly.Blocks['general_onsetup'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("When script is started");
    this.appendStatementInput("BODY");
    this.setColour(330);
    this.setTooltip('This block is run once at the start of the script.');
  }
};
Blockly.Lua['general_onsetup'] = function(block) {
  var statements_body = Blockly.Lua.statementToCode(block, 'BODY');
  var code = "function setup()\n" + statements_body + "end\n";
  return code;
};
Blockly.Lua.addReservedWords("setup");

Blockly.Blocks['general_onloop'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("On loop");
    this.appendStatementInput("BODY");
    this.setColour(330);
    this.setTooltip('This block runs continuously while the script is active.');
  }
};
Blockly.Lua['general_onloop'] = function(block) {
  var statements_body = Blockly.Lua.statementToCode(block, 'BODY');
  var code = "function loop()\n" + statements_body + "end\n";
  return code;
};
Blockly.Lua.addReservedWords("loop");

Blockly.Blocks['general_onquit'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("When script is stopped");
    this.appendStatementInput("BODY");
    this.setColour(330);
    this.setTooltip('This block is run once when the script is stopped.');
  }
};
Blockly.Lua['general_onquit'] = function(block) {
  var statements_body = Blockly.Lua.statementToCode(block, 'BODY');
  var code = "function quit()\n" + statements_body + "end\n";
  return code;
};
Blockly.Lua.addReservedWords("quit");

Blockly.Blocks['general_sleep'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(330);
		this.appendDummyInput()
		.appendField("Wait");
		this.appendValueInput("TIME")
		.setCheck("Number");
		this.appendDummyInput()
		.appendField("seconds");
		this.setInputsInline(true);
		this.setPreviousStatement(true);
		this.setNextStatement(true);
		this.setTooltip('Pause the script for a number of seconds.');
	}
};
Blockly.Lua['general_sleep'] = function(block) {
	var value_time = Blockly.Lua.valueToCode(block, 'TIME', Blockly.Lua.ORDER_ATOMIC)  || "0";
	var code = "sleep(" + value_time + ")\n";
	return code;
};
Blockly.Lua.addReservedWords("sleep");
Blockly.Lua.addReservedWords("delay");

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#vkifu3
Blockly.Blocks['general_seconds'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(330);
		this.appendDummyInput()
		.appendField("Elapsed time");
		this.setOutput(true, "Number");
		this.setTooltip('Return the elapsed time in seconds.');
	}
};
Blockly.Lua['general_seconds'] = function(block) {
	var code = "seconds()";
	return [code, Blockly.Lua.ORDER_FUNCTION_CALL];
};
Blockly.Lua.addReservedWords("seconds");
Blockly.Lua.addReservedWords("millis");
