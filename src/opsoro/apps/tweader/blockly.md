# Blockly

The subfolder blockly in sociono is used to declera new blocks for the blockly app.
This folder contains two files:
1. sociono.xml: Here we declare new blocks ie. `<block type="type_name"></block>`
2. sociono.js: We initialize the blocks and assign the code that needs to be executed.
  2.1`Blockly.Blocks['type_name'] = {}` is where the code for the layout is put.
  2.2.`Blockly.Lua['type_name'] = function(block) {}` is where we will put the code that is to be generated in.

For this project we have made a custom class twitter.py that holds the code used for the blockly module.
## binding blockly folder
Before we can use our blockly module in the general blockly app we need to declare it in: ```scripthost.py```.
In order to add a module in blockly that is in an app folder ie. ```sociono/blockly``` to work correctly you need to make a few changes in ```scripthost.py``` located in the folder lua_scripting.
```
from opsoro.twitter import Twitter #import the class

```
In the function ```setup_runtime``` add the line ```g["Twitter"] = Twitter```.
This step is also explained in twitter.md.
## using blockly
You can easily create new blocks for blockly by using the site: https://blockly-demo.appspot.com/static/demos/blockfactory/index.html

This site implements a visual way where the user can create blocks by dragging simple blocks and connecting them to create more advanced blocks in the left view. On the right view the user can see the preview of the block and the code needed to implement the block ie.
1. Definitions for json or js which describe the layout of the block
2. The generator stubs: the code that will be executed. this can be: JavaScript, Python, Lua, PHP or Dart.

### block definitions
The block definition describes the layout of the block.
```
Blockly.Blocks['sociono_get_tweet'] = {
  init: function() {
    this.appendValueInput("value") #this is a value input
        .setCheck(null)
        .appendField("get a single tweet based on hashtag "); #a sipmle text that the user will see
    this.setInputsInline(true); # if set to true the input will be in the block itself instead of a puzzelslot at the end of the block
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230); # colour of the block
    this.setTooltip('connect your variable to this block to filter by'); # tooltip for the user.
    this.setHelpUrl('');
  }
};
```

### generator stubs
The preview for the generated code will give this:
```
Blockly.Lua['sociono_get_tweet'] = function(block) {
    var value_value = Blockly.Lua.valueToCode(block, 'value', Blockly.Lua.ORDER_ATOMIC);
    var code = 'Twitter:get_tweet('+value_value+')\n';
  return code;
};

```
```var value_value = Blockly.Lua.valueToCode(block, 'value', Blockly.Lua.ORDER_ATOMIC);``` Here we take the data from the input field and store it in a variable.

```var code = 'Twitter:get_tweet('+value_value+')\n';``` This is the code that the will be returned to the generator. All code snippets needs to be put between single quotes except the values declared in the program.


```
To change the programming language you can select the language you want it to be. This can also be done manually ie. ```Blockly.Lua['block_type']``` to ```Blockly.Python['block_type']```
