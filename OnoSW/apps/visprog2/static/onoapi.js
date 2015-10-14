var KEY_LEFT = 37;
var KEY_UP = 38;
var KEY_RIGHT = 39;
var KEY_DOWN = 40;
var KEY_SPACE = 32;
var KEY_W = 87;
var KEY_S = 83;
var KEY_A = 65;
var KEY_D = 68;
var KEY_F = 70;
var KEY_G = 71;

var KEYS = [
	KEY_LEFT,
	KEY_UP,
	KEY_RIGHT,
	KEY_DOWN,
	KEY_SPACE,
	KEY_W,
	KEY_S,
	KEY_A,
	KEY_D,
	KEY_F,
	KEY_G
];

var env_interpreter = null;

var env_stepdelay = 0;
var env_running = false;
var env_timeout_obj = null;
var env_t_start = Date.now();

var env_keydown = {
	KEY_LEFT: false,
	KEY_UP: false,
	KEY_RIGHT: false,
	KEY_DOWN: false,
	KEY_SPACE: false,
	KEY_W: false,
	KEY_S: false,
	KEY_A: false,
	KEY_D: false,
	KEY_F: false,
	KEY_G: false
};
var env_rising_laststatus = {
	KEY_LEFT: false,
	KEY_UP: false,
	KEY_RIGHT: false,
	KEY_DOWN: false,
	KEY_SPACE: false,
	KEY_W: false,
	KEY_S: false,
	KEY_A: false,
	KEY_D: false,
	KEY_F: false,
	KEY_G: false
};
var env_falling_laststatus = {
	KEY_LEFT: false,
	KEY_UP: false,
	KEY_RIGHT: false,
	KEY_DOWN: false,
	KEY_SPACE: false,
	KEY_W: false,
	KEY_S: false,
	KEY_A: false,
	KEY_D: false,
	KEY_F: false,
	KEY_G: false
};

function api_wait(secs){
	env_stepdelay = secs*1000;
}

function api_showmessage(text){
	addMessage(text);
}

function api_risingedge(key){
	var ret = false;
	if( env_keydown[key] && !(env_rising_laststatus[key]) ){
		ret = true;
	}
	env_rising_laststatus[key] = env_keydown[key];
	return ret;
}

function api_fallingedge(key){
	var ret = false;
	if( !(env_keydown[key]) && env_falling_laststatus[key] ){
		ret = true;
	}
	env_falling_laststatus[key] = env_keydown[key];
	return ret;
}

function api_elapsedtime(){
	return Date.now() - env_t_start;
}

function api_playsound(snd){
	$.ajax({
		dataType: "json",
		type: "GET",
		url: "api/playsound/" + snd,
		success: function(data){
			if(data.status == "error"){
				addError(data.message);
			}
		}
	});
	env_stepdelay = 10;
}

function api_saytts(text){
	$.ajax({
		dataType: "json",
		type: "GET",
		url: "api/saytts",
		data: {"text": text},
		success: function(data){
			if(data.status == "error"){
				addError(data.message);
			}
		}
	});
	env_stepdelay = 10;
}

function api_servoson(){
	$.ajax({
		dataType: "json",
		type: "GET",
		url: "api/servoson",
		success: function(data){
			if(data.status == "error"){
				addError(data.message);
			}
		}
	});
	env_stepdelay = 10;
}

function api_servosoff(){
	$.ajax({
		dataType: "json",
		type: "GET",
		url: "api/servosoff",
		success: function(data){
			if(data.status == "error"){
				addError(data.message);
			}
		}
	});
	env_stepdelay = 10;
}

function api_updateservos(){
	$.ajax({
		dataType: "json",
		type: "GET",
		url: "api/updateservos",
		success: function(data){
			if(data.status == "error"){
				addError(data.message);
			}
		}
	});
	env_stepdelay = 10;
}

function api_setposition(dofs_, pos_){
	var dofs_param = null;

	if(dofs_.isPrimitive){
		dofs_param = dofs_.valueOf();
	}else{
		dofs_param = [];
		$.each(dofs_.properties, function(index, value){
			dofs_param.push(value.toString());
		});
		dofs_param = dofs_param.join(",");
	}

	$.ajax({
		dataType: "json",
		type: "GET",
		url: "api/setposition",
		data: {
			dofs: dofs_param,
			pos: pos_
		},
		success: function(data){
			if(data.status == "error"){
				addError(data.message);
			}
		}
	});
	env_stepdelay = 10;
}

function api_setemotion(dofs_, emotion_){
	var dofs_param = null;
	var data_ = {};

	if(dofs_.isPrimitive){
		dofs_param = dofs_.valueOf();
	}else{
		dofs_param = [];
		$.each(dofs_.properties, function(index, value){
			dofs_param.push(value.toString());
		});
		dofs_param = dofs_param.join(",");
	}
	data_["dofs"] = dofs_param;

	if(!emotion_.isPrimitive){
		$.each(emotion_.properties, function(index, value){
			//dofs_param.push(value.toString());
			data_[index] = value.toString();
		});
	}

	$.ajax({
		dataType: "json",
		type: "GET",
		url: "api/setemotion",
		data: data_,
		success: function(data){
			if(data.status == "error"){
				addError(data.message);
			}
		}
	});

	env_stepdelay = 10;
}


function env_InitApi(interpreter, scope) {
	// alert() API
	var wrapper = function(text) {
		text = text ? text.toString() : "";
		return interpreter.createPrimitive(alert(text));
	};
	interpreter.setProperty(scope, "alert", interpreter.createNativeFunction(wrapper));

	// prompt() API
	wrapper = function(text) {
		text = text ? text.toString() : "";
		return interpreter.createPrimitive(prompt(text));
	};
	interpreter.setProperty(scope, "prompt", interpreter.createNativeFunction(wrapper));

	// wait() API
	wrapper = function(secs) {
		//text = text ? text.toString() : "";
		secs = $.isNumeric(secs) ? Number(secs) : 0;
		return interpreter.createPrimitive(api_wait(secs));
	};
	interpreter.setProperty(scope, "wait", interpreter.createNativeFunction(wrapper));

	// showmessage() API
	wrapper = function(text) {
		text = text ? text.toString() : "";
		return interpreter.createPrimitive(api_showmessage(text));
	};
	interpreter.setProperty(scope, "showmessage", interpreter.createNativeFunction(wrapper));

	// risingedge() API
	wrapper = function(key) {
		key = $.isNumeric(key) ? Number(key) : 0;
		return interpreter.createPrimitive(api_risingedge(key));
	};
	interpreter.setProperty(scope, "risingedge", interpreter.createNativeFunction(wrapper));

	// fallingedge() API
	wrapper = function(key) {
		key = $.isNumeric(key) ? Number(key) : 0;
		return interpreter.createPrimitive(api_fallingedge(key));
	};
	interpreter.setProperty(scope, "fallingedge", interpreter.createNativeFunction(wrapper));

	// elapsedtime() API
	wrapper = function() {
		return interpreter.createPrimitive(api_elapsedtime());
	};
	interpreter.setProperty(scope, "elapsedtime", interpreter.createNativeFunction(wrapper));

	// playsound() API
	wrapper = function(snd) {
		snd = snd ? snd.toString() : "";
		return interpreter.createPrimitive(api_playsound(snd));
	};
	interpreter.setProperty(scope, "playsound", interpreter.createNativeFunction(wrapper));

	// saytts() API
	wrapper = function(text) {
		text = text ? text.toString() : "";
		return interpreter.createPrimitive(api_saytts(text));
	};
	interpreter.setProperty(scope, "saytts", interpreter.createNativeFunction(wrapper));

	// servoson() API
	wrapper = function() {
		return interpreter.createPrimitive(api_servoson());
	};
	interpreter.setProperty(scope, "servoson", interpreter.createNativeFunction(wrapper));

	// servosoff() API
	wrapper = function() {
		return interpreter.createPrimitive(api_servosoff());
	};
	interpreter.setProperty(scope, "servosoff", interpreter.createNativeFunction(wrapper));

	// updateservos() API
	wrapper = function() {
		return interpreter.createPrimitive(api_updateservos());
	};
	interpreter.setProperty(scope, "updateservos", interpreter.createNativeFunction(wrapper));

	// setposition() API
	wrapper = function(dofs, pos) {
		pos = pos ? pos.toNumber() : 0;
		return interpreter.createPrimitive(api_setposition(dofs, pos));
	};
	interpreter.setProperty(scope, "setposition", interpreter.createNativeFunction(wrapper));

	// setemotion() API
	wrapper = function(dofs, emotion) {
		return interpreter.createPrimitive(api_setemotion(dofs, emotion));
	};
	interpreter.setProperty(scope, "setemotion", interpreter.createNativeFunction(wrapper));
}

function env_Parse(){
	// Send XML to server for backup
	var xml = Blockly.Xml.workspaceToDom(Blockly.mainWorkspace);
	var xml_text = Blockly.Xml.domToPrettyText(xml);

	$.ajax({
		dataType: "json",
		data: {"file": xml_text},
		type: "POST",
		url: "savecode",
		success: function(data){}
	});

	// Cconvert only ono_setup and ono_loop top-level blocks to code
	var workspace = Blockly.mainWorkspace;
	var code_setup = [];
	var code_loop = [];
	Blockly.JavaScript.init(workspace);

	var blocks = workspace.getTopBlocks(true);
	for (var x = 0, block; block = blocks[x]; x++) {
		var line = Blockly.JavaScript.blockToCode(block);
		if ($.isArray(line)) {
			// Value blocks return tuples of code and operator order.
			// Top-level blocks don't care about operator order.
			line = "  " + line[0];
		}
		if (line) {
			if (block.outputConnection && Blockly.JavaScript.scrubNakedValue) {
				// This block is a naked value.  Ask the language's code generator if
				// it wants to append a semicolon, or something.
				line = Blockly.JavaScript.scrubNakedValue(line);
			}
			if(block.type == "ono_onsetup"){
				code_setup.push(line);
			}else if(block.type == "ono_onloop"){
				code_loop.push(line);
			}
		}
	}

	code_setup = code_setup.join('\n');  // Blank line between each section.
	code_loop = code_loop.join('\n');

	var code = "function setup(){\n";
	code += code_setup;
	code += "}\n";
	code += "\n";
	code += "function loop(){\n";
	code += code_loop;
	code += "}\n";
	code += "\n";
	code += "setup();\n";
	code += "while(true){\n";
	code += "  loop();\n";
	code += "  wait(0.05);\n";
	code += "}";

	code = Blockly.JavaScript.finish(code);
	// Final scrubbing of whitespace.
	code = code.replace(/^\s+\n/, '');
	code = code.replace(/\n\s+$/, '\n');
	code = code.replace(/[ \t]+\n/g, '\n');

	console.log("Executing code:\n\n" +code);
	return code;
}

function env_ParseAndRun(){
	var code = env_Parse();
	env_interpreter = new Interpreter(code, env_InitApi);
	env_stepdelay = 0;
	env_t_start = Date.now();
	env_NextStep();
}

function env_NextStep(){
	if(!env_running){
		env_SetButtonToStart();
		return;
	}

	if(env_interpreter.step()){
		if(env_stepdelay > 0){
			env_timeout_obj = window.setTimeout(env_NextStep, env_stepdelay);
			env_stepdelay = 0;
		}else{
			env_NextStep();
			//env_timeout_obj = window.setTimeout(env_NextStep, 0);
		}
	}else{
		env_SetButtonToStart();
		env_running = false;
	}
}

function env_KeyDown(key){
	if($.inArray(key, KEYS) >= 0){
		env_keydown[key] = true;
	}
}

function env_KeyUp(key){
	if($.inArray(key, KEYS) >= 0){
		env_keydown[key] = false;
	}
}

function env_SetButtonToStart(){
	// Button
	$("#btnStartStop .fa").removeClass("fa-stop");
	$("#btnStartStop .fa").addClass("fa-play");
	$("#btnStartStop .text").html("Run");

	// Filename bar
	$(".filebox .status").html("Stopped");
	$(".filebox .fa-circle-o-notch").removeClass("fa-circle-o-notch fa-spin").addClass("fa-stop");
}

function env_SetButtonToStop(){
	// Button
	$("#btnStartStop .fa").removeClass("fa-play");
	$("#btnStartStop .fa").addClass("fa-stop");
	$("#btnStartStop .text").html("Stop");

	// Filename bar
	$(".filebox .status").html("Running");
	$(".filebox .fa-stop").removeClass("fa-stop").addClass("fa-circle-o-notch fa-spin");
}

function env_StartStop(){
	if(!env_running){
		// Start the script
		if(env_timeout_obj != null){
			window.clearTimeout(env_timeout_obj);
			env_timeout_obj = null;
		}
		env_running = true;
		env_SetButtonToStop();
		env_ParseAndRun();
	}else{
		// Stop the script
		if(env_timeout_obj != null){
			window.clearTimeout(env_timeout_obj);
			env_timeout_obj = null;
		}
		env_running = false;
		env_SetButtonToStart();
	}
}
