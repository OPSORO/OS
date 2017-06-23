Blockly.Lua.addReservedWords("Sound");

Blockly.Blocks['sound_saytts'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("/static/images/fontawesome/white/svg/volume-down.svg", 16, 18, ""))
        .appendField("Say")
        .appendField(new Blockly.FieldTextInput("I am a robot!"), "TEXT");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(300);
    this.setTooltip('Say something using the text-to-speech function.');
  }
};
Blockly.Lua['sound_saytts'] = function(block) {
  var text_text = block.getFieldValue('TEXT');
  var code = 'Sound:say_tts("' + text_text + '")\n';
  return code;
};

Blockly.Blocks['sound_play'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("/static/images/fontawesome/white/svg/volume-down.svg", 16, 18, ""))
        .appendField("Play")
        .appendField(new Blockly.FieldDropdown(soundlist), "FILENAME");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(300);
    this.setTooltip('Play a sound sample.');
  }
};
Blockly.Lua['sound_play'] = function(block) {
  var dropdown_filename = block.getFieldValue('FILENAME');
  var code = 'Sound:play_file("' + dropdown_filename + '")\n';
  return code;
};
