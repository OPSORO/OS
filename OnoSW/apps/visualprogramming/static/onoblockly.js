////////////////////////////////////////////////////////////////
////////////////////////// ONO EVENTS //////////////////////////
////////////////////////////////////////////////////////////////

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#fh6c64
Blockly.Blocks['ono_onsetup'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(20);
		this.appendDummyInput()
		.appendField("Setup");
		this.appendStatementInput("BODY");
		this.setTooltip('This block is run once at the start of the program.');
	}
};
Blockly.JavaScript['ono_onsetup'] = function(block) {
	var statements_body = Blockly.JavaScript.statementToCode(block, 'BODY');
	// Code is put in correct functions/structure in onoapi.js > env_Parse()
	var code = statements_body;
	return code;
};
Blockly.JavaScript.addReservedWords("setup");

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#bjhxr8
Blockly.Blocks['ono_onloop'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(20);
		this.appendDummyInput()
		.appendField("Loop");
		this.appendStatementInput("BODY");
		this.setTooltip('This block is continually executed while the program runs.');
	}
};
Blockly.JavaScript['ono_onloop'] = function(block) {
	var statements_body = Blockly.JavaScript.statementToCode(block, 'BODY');
	// Code is put in correct functions/structure in onoapi.js > env_Parse()
	var code = statements_body;
	return code;
};
Blockly.JavaScript.addReservedWords("loop");

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#d2988e
Blockly.Blocks['ono_onkeypress'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(20);
		this.appendDummyInput()
		.appendField("When")
		.appendField(new Blockly.FieldDropdown([
			["Up", "38"], ["Down", "40"], ["Left", "37"], ["Right", "39"],
			["Space", "32"], ["W", "87"], ["A", "65"], ["S", "83"], ["D", "68"],
			["F", "70"], ["G", "71"]]), "KEY")
		.appendField("is pressed");
		this.appendStatementInput("BODY");
		this.setPreviousStatement(true);
		this.setNextStatement(true);
		this.setTooltip('Executes a block of code when a button is pressed.');
	}
};
Blockly.JavaScript['ono_onkeypress'] = function(block) {
	var statements_body = Blockly.JavaScript.statementToCode(block, 'BODY');
	var dropdown_key = block.getFieldValue('KEY') || "null";
	var code = "if(risingedge(" + dropdown_key + ")){\n";
	code += statements_body;
	code += "}\n"
	return code;
};
Blockly.JavaScript.addReservedWords("risingedge");

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#qjohk4
Blockly.Blocks['ono_onkeyrelease'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(20);
		this.appendDummyInput()
		.appendField("When")
		.appendField(new Blockly.FieldDropdown([
			["Up", "38"], ["Down", "40"], ["Left", "37"], ["Right", "39"],
			["Space", "32"], ["W", "87"], ["A", "65"], ["S", "83"], ["D", "68"],
			["F", "70"], ["G", "71"]]), "KEY")
		.appendField("is released");
		this.appendStatementInput("BODY");
		this.setPreviousStatement(true);
		this.setNextStatement(true);
		this.setTooltip('Executes a block of code when a button is released');
	}
};
Blockly.JavaScript['ono_onkeyrelease'] = function(block) {
	var statements_body = Blockly.JavaScript.statementToCode(block, 'BODY');
	var dropdown_key = block.getFieldValue('KEY')  || "null";
	var code = "if(fallingedge(" + dropdown_key + ")){\n";
	code += statements_body;
	code += "}\n"
	return code;
};
Blockly.JavaScript.addReservedWords("fallingedge");


////////////////////////////////////////////////////////////////
///////////////////////// ONO EMOTIONS /////////////////////////
////////////////////////////////////////////////////////////////

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#tzeik9
Blockly.Blocks['ono_emotion_basic'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(210);
		this.appendDummyInput()
		.appendField("Basic emotion")
		.appendField(new Blockly.FieldDropdown([["Happiness", "18"], ["Sadness", "200"], ["Anger", "153"], ["Surprise", "90"], ["Fear", "125"], ["Disgust", "172"]]), "EMOTION");
		this.setInputsInline(true);
		this.setOutput(true, "emotion");
		this.setTooltip('');
	}
};

Blockly.JavaScript['ono_emotion_basic'] = function(block) {
	var dropdown_emotion = block.getFieldValue('EMOTION') || "18";
	var code = "{alpha: " + dropdown_emotion + ", length: 1.0}";
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#zkfofy
Blockly.Blocks['ono_emotion_val_ar'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(210);
		this.appendDummyInput()
		.appendField("Valence:");
		this.appendValueInput("VALENCE")
		.setCheck("Number");
		this.appendDummyInput()
		.appendField("Arousal")
		this.appendValueInput("AROUSAL")
		.setCheck("Number");
		this.setInputsInline(true);
		this.setOutput(true, "emotion");
		this.setTooltip('');
	}
};

Blockly.JavaScript['ono_emotion_val_ar'] = function(block) {
	var value_valence = Blockly.JavaScript.valueToCode(block, 'VALENCE', Blockly.JavaScript.ORDER_ATOMIC) || "0.0";
	var value_arousal = Blockly.JavaScript.valueToCode(block, 'AROUSAL', Blockly.JavaScript.ORDER_ATOMIC) || "0.0";
	var code = "{valence: " + value_valence + ", arousal: " + value_arousal + "}";
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#8wh3hp
Blockly.Blocks['ono_emotion_alpha_len'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(210);
		this.appendDummyInput()
		.appendField("Alpha:");
		this.appendValueInput("ALPHA")
		.setCheck("Number");
		this.appendDummyInput()
		.appendField("Length:");
		this.appendValueInput("LENGTH")
		.setCheck("Number");
		this.setInputsInline(true);
		this.setOutput(true, "emotion");
		this.setTooltip('');
	}
};

Blockly.JavaScript['ono_emotion_alpha_len'] = function(block) {
	var value_alpha = Blockly.JavaScript.valueToCode(block, 'ALPHA', Blockly.JavaScript.ORDER_ATOMIC)  || "0";
	var value_length = Blockly.JavaScript.valueToCode(block, 'LENGTH', Blockly.JavaScript.ORDER_ATOMIC)  || "0.0";
	var code = "{alpha: " + value_alpha + ", length: " + value_length + "}";
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#tzfeyz
Blockly.Blocks['ono_dof'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(210);
		this.appendDummyInput()
		.appendField("DOF")
		.appendField(new Blockly.FieldDropdown(api_doflist), "DOF");
		this.setOutput(true, 'dof');
		this.setTooltip('');
	}
};

Blockly.JavaScript['ono_dof'] = function(block) {
	var dropdown_dof = block.getFieldValue('DOF');
	var code = "\"" + dropdown_dof + "\"";
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#kdchbf
Blockly.Blocks['ono_alldofs'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(210);
		this.appendDummyInput()
		.appendField("All DOFs");
		this.setOutput(true, 'dof');
		this.setTooltip('');
	}
};
Blockly.JavaScript['ono_alldofs'] = function(block) {
	var code = "null";
	return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#ngxge7
Blockly.Blocks['ono_setposition'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(210);
		this.appendDummyInput()
		.appendField("Set");
		this.appendValueInput("DOFS")
		.setCheck(["String", "Array", "dof"]);
		this.appendDummyInput()
		.appendField("to position");
		this.appendValueInput("POSITION")
		.setCheck("Number");
		this.setInputsInline(true);
		this.setPreviousStatement(true);
		this.setNextStatement(true);
		this.setTooltip('Sets the position of one or more DOFs.');
	}
};
Blockly.JavaScript['ono_setposition'] = function(block) {
	var value_dofs = Blockly.JavaScript.valueToCode(block, 'DOFS', Blockly.JavaScript.ORDER_ATOMIC) || "null";
	var value_position = Blockly.JavaScript.valueToCode(block, 'POSITION', Blockly.JavaScript.ORDER_ATOMIC) || "0";
	var code = "setposition(" + value_dofs + ", " + value_position + ");\n";
	return code;
};
Blockly.JavaScript.addReservedWords("setposition");

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#s82u2i
Blockly.Blocks['ono_setemotion'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(210);
		this.appendDummyInput()
		.appendField("Set");
		this.appendValueInput("DOFS")
		.setCheck(["String", "Array", "dof"]);
		this.appendDummyInput()
		.appendField("to emotion");
		this.appendValueInput("EMOTION")
		.setCheck("emotion");
		this.setInputsInline(true);
		this.setPreviousStatement(true);
		this.setNextStatement(true);
		this.setTooltip('');
	}
};
Blockly.JavaScript['ono_setemotion'] = function(block) {
	var value_dofs = Blockly.JavaScript.valueToCode(block, 'DOFS', Blockly.JavaScript.ORDER_ATOMIC) || "null";
	var value_emotion = Blockly.JavaScript.valueToCode(block, 'EMOTION', Blockly.JavaScript.ORDER_ATOMIC) || "null";
	var code = "setemotion(" + value_dofs + ", " + value_emotion + ");\n";
	return code;
};
Blockly.JavaScript.addReservedWords("setemotion");


////////////////////////////////////////////////////////////////
/////////////////////////// ONO MISC ///////////////////////////
////////////////////////////////////////////////////////////////

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#b6xnj3
Blockly.Blocks['ono_wait'] = {
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

Blockly.JavaScript['ono_wait'] = function(block) {
	var value_time = Blockly.JavaScript.valueToCode(block, 'TIME', Blockly.JavaScript.ORDER_ATOMIC)  || "0";
	var code = "wait(" + value_time + ");\n";
	return code;
};
Blockly.JavaScript.addReservedWords("wait");

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#v7rtav
Blockly.Blocks['ono_playsound'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(290);
		this.appendDummyInput()
		.appendField("Play")
		.appendField(new Blockly.FieldDropdown(api_soundlist), "SOUNDFILE");
		this.setPreviousStatement(true);
		this.setNextStatement(true);
		this.setTooltip('');
	}
};

Blockly.JavaScript['ono_playsound'] = function(block) {
	var dropdown_soundfile = block.getFieldValue('SOUNDFILE') || "\"\n";
	var code = "playsound(\"" + dropdown_soundfile + "\");\n";
	return code;
};
Blockly.JavaScript.addReservedWords("playsound");

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#gd8qn6
Blockly.Blocks['ono_saytts'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(290);
		this.appendDummyInput()
		.appendField("say")
		.appendField(new Blockly.FieldTextInput("Hello!"), "SAY");
		this.setPreviousStatement(true);
		this.setNextStatement(true);
		this.setTooltip('');
	}
};

Blockly.JavaScript['ono_saytts'] = function(block) {
	var text_say = block.getFieldValue('SAY')  || "\"\"";
	var code = "saytts(\"" + text_say + "\");\n";
	return code;
};
Blockly.JavaScript.addReservedWords("saytts");

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#5x9j3w
Blockly.Blocks['ono_servoson'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(290);
		this.appendDummyInput()
		.appendField("Turn servos on.");
		this.setPreviousStatement(true);
		this.setNextStatement(true);
		this.setTooltip('Turn servos on.');
	}
};
Blockly.JavaScript['ono_servoson'] = function(block) {
	var code = "servoson();\n";
	return code;
};
Blockly.JavaScript.addReservedWords("servoson");

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#vja84t
Blockly.Blocks['ono_servosoff'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(290);
		this.appendDummyInput()
		.appendField("Turn servos off");
		this.setPreviousStatement(true);
		this.setNextStatement(true);
		this.setTooltip('Turn servos off.');
	}
};
Blockly.JavaScript['ono_servosoff'] = function(block) {
	var code = "servosoff();\n";
	return code;
};
Blockly.JavaScript.addReservedWords("servosoff");

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#weq2bn
Blockly.Blocks['ono_updateservos'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(290);
		this.appendDummyInput()
		.appendField("Update servos");
		this.setPreviousStatement(true);
		this.setNextStatement(true);
		this.setTooltip('Update all servos.');
	}
};
Blockly.JavaScript['ono_updateservos'] = function(block) {
	var code = "updateservos();\n";
	return code;
};
Blockly.JavaScript.addReservedWords("updateservos");

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#q7qrhn
Blockly.Blocks['ono_showmessage'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(290);
		this.appendValueInput("TEXT")
		.appendField("Show message");
		this.setPreviousStatement(true);
		this.setNextStatement(true);
		this.setTooltip('Show a text message.');
	}
};
Blockly.JavaScript['ono_showmessage'] = function(block) {
	var value_text = Blockly.JavaScript.valueToCode(block, 'TEXT', Blockly.JavaScript.ORDER_ATOMIC);
	var code = "showmessage(" + value_text + ");\n";
	return code;
};
Blockly.JavaScript.addReservedWords("showmessage");

// https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#vkifu3
Blockly.Blocks['ono_elapsedtime'] = {
	init: function() {
		this.setHelpUrl(null);
		this.setColour(290);
		this.appendDummyInput()
		.appendField("Elapsed time");
		this.setOutput(true, "Number");
		this.setTooltip('Returns the time elapsed since the start of the program in milliseconds.');
	}
};
Blockly.JavaScript['ono_elapsedtime'] = function(block) {
	var code = "elapsedtime()";
	return [code, Blockly.JavaScript.ORDER_FUNCTION_CALL];
};
Blockly.JavaScript.addReservedWords("elapsedtime");
