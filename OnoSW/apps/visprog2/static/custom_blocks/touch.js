Blockly.Blocks['touch_init'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("static/icons/fa-hand-o-up.png", 16, 18, ""))
        .appendField("Initialize with")
        .appendField(new Blockly.FieldDropdown([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"], ["5", "5"], ["6", "6"], ["7", "7"], ["8", "8"], ["9", "9"], ["10", "10"], ["11", "11"], ["12", "12"]]), "ELECTRODE")
        .appendField("electrodes");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['touch_init'] = function(block) {
  var dropdown_name = block.getFieldValue('ELECTRODE');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};

Blockly.Blocks['touch_etouched'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("http://i.imgur.com/WoThsms.png", 16, 18, ""))
        .appendField("When electrode")
        .appendField(new Blockly.FieldDropdown([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"], ["5", "5"], ["6", "6"], ["7", "7"], ["8", "8"], ["9", "9"], ["10", "10"], ["11", "11"], ["12", "12"]]), "ELECTRODE")
        .appendField("is")
        .appendField(new Blockly.FieldDropdown([["touched", "TOUCHED"], ["released", "RELEASED"]]), "TOU_REL");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};
Blockly.JavaScript['touch_etouched'] = function(block) {
  var dropdown_electrode = block.getFieldValue('ELECTRODE');
  var dropdown_tou_rel = block.getFieldValue('TOU_REL');
  // TODO: Assemble JavaScript into code variable.
  var code = '...';
  return code;
};
