Blockly.Lua.addReservedWords("Twitter");


Blockly.Blocks['sociono_get_tweet'] = {
  init: function() {
    this.appendValueInput("value")
        .setCheck(null)
        .appendField("get a single tweet based on hashtag ");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('connect your variable to this block to filter by');
    this.setHelpUrl('');
  }
};
Blockly.Lua['sociono_get_tweet'] = function(block) {
  var value_value = Blockly.Lua.valueToCode(block, 'value', Blockly.Lua.ORDER_ATOMIC);
  var code = 'Twitter:get_tweet('+value_value+')\n';
  return code;
};
Blockly.Blocks['sociono_stop_stream'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("stop twitter stream");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('use this block to stop the stream and the sound from playing');
    this.setHelpUrl('');
  }
};
Blockly.Lua['sociono_stop_stream'] = function(block) {
  var code = 'Twitter:stop_streamreader()\n';
  return code;
};
Blockly.Blocks['start_streamreader_loop'] = {
  init: function() {
    this.appendValueInput("streamreader_filter")
        .setCheck("String")
        .appendField("start streamreader and filter by:");
    this.appendValueInput("amount")
        .setCheck("Number")
        .appendField("for");
    this.appendDummyInput()
        .appendField("times");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip('start streamreader and filter on a variable. for a set amount of times');
    this.setHelpUrl('');
  }
};
Blockly.Lua['start_streamreader_loop'] = function(block) {
  var value_streamreader_filter = Blockly.Lua.valueToCode(block, 'streamreader_filter', Blockly.Lua.ORDER_ATOMIC);
  var value_amount = Blockly.Lua.valueToCode(block, 'amount', Blockly.Lua.ORDER_ATOMIC);
  var statements_input = Blockly.Lua.statementToCode(block, 'input');
  var code = 'Twitter:start_streamreader_amount('+value_streamreader_filter+','+ value_amount+')\n';
  return code;
};
