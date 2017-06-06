Blockly.Blocks['touch_init'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("/static/images/fontawesome/white/svg/hand-o-up.svg", 16, 18, ""))
        .appendField("Initialize with")
        .appendField(new Blockly.FieldDropdown([["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"], ["5", "5"], ["6", "6"], ["7", "7"], ["8", "8"], ["9", "9"], ["10", "10"], ["11", "11"], ["12", "12"]]), "ELECTRODE")
        .appendField("electrodes");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(210);
    this.setTooltip('Initialize the capacitive touch sensor with a specified number of electrodes.');
  }
};
Blockly.Lua['touch_init'] = function(block) {
  var dropdown_electrode = block.getFieldValue('ELECTRODE');
  var code = 'Hardware.Capacitive:init(' + dropdown_electrode + ')\n';
  return code;
};

Blockly.Blocks['touch_etouched'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("/static/images/fontawesome/white/svg/hand-o-up.svg", 16, 18, ""))
        .appendField("When electrode")
        .appendField(new Blockly.FieldDropdown([["E0", "0"], ["E1", "1"], ["E2", "2"], ["E3", "3"], ["E4", "4"], ["E5", "5"], ["E6", "6"], ["E7", "7"], ["E8", "8"], ["E9", "9"], ["E10", "10"], ["E11", "11"]]), "ELECTRODE")
        .appendField("is")
    this.appendStatementInput("BODY_TOU")
        .appendField("Touched");
    this.appendStatementInput("BODY_REL")
        .appendField("Released");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setColour(210);
    this.setTooltip('Execute a block of code when an electrode is touched or released.');
  }
};
Blockly.Lua['touch_etouched'] = function(block) {
  var dropdown_electrode = block.getFieldValue('ELECTRODE');
  var statements_body_tou = Blockly.Lua.statementToCode(block, 'BODY_TOU');
  var statements_body_rel = Blockly.Lua.statementToCode(block, 'BODY_REL');

  var touch_var = Blockly.Lua.variableDB_.getDistinctName('e' + dropdown_electrode + '_touch', Blockly.Variables.NAME_TYPE);

  var code = 'local ' + touch_var + ' =  Hardware.Capacitive:get_touched()\n';
  code += touch_var + ' = bit.band(' + touch_var + ', 2^' + dropdown_electrode + ') > 0\n';

  if(statements_body_tou == '' && statements_body_rel == ''){
    return '';
  }
  if(statements_body_tou != ''){
    code += 'if rising_edge("' + touch_var + '", ' + touch_var + ') then\n';
    code += statements_body_tou;
    code += 'end\n';
  }
  if(statements_body_rel != ''){
    code += 'if falling_edge("' + touch_var + '", ' + touch_var + ') then\n';
    code += statements_body_rel;
    code += 'end\n';
  }

  return code;
};
