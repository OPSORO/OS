Blockly.Lua.addReservedWords("Twitter");

Blockly.Blocks['sociono_get_tweet'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("get a single tweet based on hashtag ")
        .appendField(new Blockly.FieldTextInput("#opsoro"), "filter");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('give in the hashtag you want to filter');
    this.setHelpUrl('');
  }
};
Blockly.Lua['sociono_get_tweet'] = function(block) {
  var text_filter = block.getFieldValue('filter');
  var code = 'Twitter:get_tweet("'+text_filter+'")\n';
  return code;
};
Blockly.Blocks['sociono_start_stream'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Start twitter stream and filter on")
        .appendField(new Blockly.FieldTextInput("#opsoro"), "filter");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};
Blockly.Lua['sociono_start_stream'] = function(block) {
  var text_filter = block.getFieldValue('filter');
  var code = 'Twitter:start_streamreader("'+text_filter+'")\nfunction quit()\n  Twitter:stop_streamreader()\nend';
  return code;
};
Blockly.Blocks['sociono_stop_stream'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("stop twitter stream");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};
Blockly.Lua['sociono_stop_stream'] = function(block) {
  var code = 'Twitter:stop_streamreader()\n';
  return code;
};
// commented see twitter.md*
// Blockly.Blocks['sociono_stop_stream_exit'] = {
//   init: function() {
//     this.appendDummyInput()
//         .appendField("stop twitter stream with no feedback");
//     this.setPreviousStatement(true, null);
//     this.setNextStatement(true, null);
//     this.setColour(230);
//     this.setTooltip('a backup fucntion to be put in the when script stopped. stops the streamreader without returning any feedback');
//     this.setHelpUrl('');
//   }
// };
// Blockly.Lua['sociono_stop_stream_exit'] = function(block) {
//   var code = 'Twitter:stop_streamreader_on_exit()\n';
//   return code;
// };
