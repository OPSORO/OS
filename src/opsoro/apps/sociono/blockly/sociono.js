Blockly.Blocks['sociono_twitter'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("/static/images/fontawesome/white/svg/smile-o.svg", 16, 18, ""))
        .appendField("test block")
        .appendField(new Blockly.FieldDropdown([["neutral", "NEUTRAL"], ["happy", "HAPPY"], ["sad", "SAD"], ["angry", "ANGRY"], ["surprise", "SURPRISE"], ["fear", "FEAR"], ["disgust", "DISGUST"]]), "EMOTION");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(105);
    this.setTooltip('Set the current facial expression using Ekman\'s basic emotions');
  }
};
Blockly.Lua['sociono_twitter'] = function(block) {
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
