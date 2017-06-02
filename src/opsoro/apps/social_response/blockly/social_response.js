Blockly.Lua.addReservedWords("Social_response");

Blockly.Blocks['social_response_facebook'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("/static/images/fontawesome/white/svg/smile-o.svg", 16, 18, ""))
        .appendField("set emotion to")
        .appendField(new Blockly.FieldDropdown([["neutral", "NEUTRAL"], ["happy", "HAPPY"], ["sad", "SAD"], ["angry", "ANGRY"], ["surprise", "SURPRISE"], ["fear", "FEAR"], ["disgust", "DISGUST"]]), "EMOTION");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(105);
    this.setTooltip('Set the current facial expression using Ekman\'s basic emotions');
  }
};
Blockly.Lua['social_response_facebook'] = function(block) {
  var dropdown_emotion = block.getFieldValue('EMOTION');
  var va_map = {
    HAPPY:    {phi: 18 * Math.PI/180.0,  r: 1.0},
    SAD:      {phi: 200 * Math.PI/180.0, r: 1.0},
    ANGRY:    {phi: 153 * Math.PI/180.0, r: 1.0},
    SURPRISE: {phi: 90 * Math.PI/180.0,  r: 1.0},
    FEAR:     {phi: 125 * Math.PI/180.0, r: 1.0},
    DISGUST:  {phi: 172 * Math.PI/180.0, r: 1.0},
    NEUTRAL:  {phi: 0, r: 0.0}
  };
  var code = 'Expression:set_emotion_r_phi(' + va_map[dropdown_emotion].r.toFixed(1) + ', ' + va_map[dropdown_emotion].phi.toFixed(2) +')\n';
  return code;
};

Blockly.Blocks['social_response_twitter'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("/static/images/fontawesome/white/svg/smile-o.svg", 16, 18, ""))
        .appendField("Set emotion to");
    this.appendValueInput("VALENCE")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Valence");
    this.appendValueInput("AROUSAL")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Arousal");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(105);
    this.setTooltip('Set the current facial expression using Valence and Arousal. Parameters range from -1.0 to +1.0.');
  }
};
Blockly.Lua['social_response_twitter'] = function(block) {
  var value_valence = Blockly.Lua.valueToCode(block, 'VALENCE', Blockly.Lua.ORDER_ATOMIC);
  var value_arousal = Blockly.Lua.valueToCode(block, 'AROUSAL', Blockly.Lua.ORDER_ATOMIC);

  var code = 'Expression:set_emotion_val_ar(' + value_valence + ', ' + value_arousal +')\n';
  return code;
};
