var isFullscreen = false;
var codeViewOn = false;
var ignoreNextChangeEvt = true;
var monitorKeypresses = false;
var Blockly = null;
var workspace = null;

function find_block_values(block_type, field_name) {
  var all_xml = $(Blockly.Xml.workspaceToDom(workspace));
  var fields = all_xml.find("block[type='" + block_type + "'] > field[name='" + field_name + "']");

  var ret = [];
  fields.each(function(idx, elem) {
      ret.push($(elem).text());
  });
  return ret;
}

function addError(msg) {
  $("#console").append("<span style=\"color: #ab3226;\">" + msg + "</span><br>");
  $("#console").scrollTop($("#console").prop("scrollHeight"));
}

function addMessage(msg) {
  $("#console").append(msg + "<br>");
  $("#console").scrollTop($("#console").prop("scrollHeight"));
}

function addConsole(msg, color, icon) {
  var line = "";
  if (color) {
      line += "<span style=\"color: " + color + ";\">";
  }
  if (icon) {
      line += "<span class=\"fa " + icon + "\"></span> ";
  }
  line += msg;
  if (color) {
      line += "</span>";
  }
  line += "<br>";

  $("#console").append(line);
  $("#console").scrollTop($("#console").prop("scrollHeight"));
}

function blocklyLoaded(blockly, ws) {
  // Called once Blockly is fully loaded.
  Blockly = blockly;
  workspace = ws;

  // if (isScriptRunning) {
  //     // Load current script into workspace
  //     $.ajax({
  //         url: "currentscript.xml.tmp",
  //         dataType: "text",
  //         cache: false,
  //         success: function(data) {
  //             // Load script
  //             ignoreNextChangeEvt = true;
  //             Blockly.mainWorkspace.clear();
  //             var xml = Blockly.Xml.textToDom(data);
  //             Blockly.Xml.domToWorkspace(workspace, xml);
  //         }
  //     });
  //
  // }

  ws.addChangeListener(function() {
    // Change listener gets called on load, use bool as workaround
    if (!ignoreNextChangeEvt) {
        isWorkspaceModified = true;
        $(".filebox .fa-asterisk").removeClass("hide");
    }
    ignoreNextChangeEvt = false;
  });
}

function generateLua() {
  var code = Blockly.Lua.workspaceToCode(workspace);
  return code;
}

function generateXml() {
  var xml = Blockly.Xml.workspaceToDom(workspace);
  var xml_text = Blockly.Xml.domToText(xml);
  return xml_text;
}

$(document).ready(function() {
  var Model = function() {
    var self = this;

    self.fileIsLocked = ko.observable(false);
    self.fileIsModified = ko.observable(isScriptModified);
    // self.fileName = ko.observable("Untitled");
    self.fileStatus = ko.observable("Editing");
    self.fileExtension = ko.observable(".xml");
    self.isRunning = ko.observable(isScriptRunning);
    self.isUI = ko.observable(false);

    // Setup ACE editor.
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/twilight");
    editor.setReadOnly(true);

    var LuaMode = require("ace/mode/lua").Mode;
    var mode = new LuaMode();
    var Tokenizer = require("ace/tokenizer").Tokenizer;
    var OnoLuaHighlightRules = require("ace/mode/onolua_highlight_rules").OnoLuaHighlightRules;
    mode.$tokenizer = new Tokenizer(new OnoLuaHighlightRules().getRules());
    editor.session.setMode(mode);

    editor.getSession().setUseSoftTabs(false);
    editor.getSession().setTabSize(4);
    editor.$blockScrolling = Infinity; // Disable warning

    // Setup websocket connection.
    app_socket_handler = function(data) {
      switch (data.action) {
        case "addConsole":
          addConsole(data.message, data.color, data.icon);
          break;
        case "scriptStarted":
          addConsole("Script started.", "#888888", "fa-play");
          self.fileStatus("Running");
          self.isRunning(true);
          //SetButtonToStop();
          break;
        case "scriptStopped":
          addConsole("Script stopped.", "#888888", "fa-stop");
          self.fileStatus("Stopped");
          self.isRunning(false);
          self.isUI(false);
          $("#btnScriptUI").addClass("hide");
          break;
        case "initUI":
          self.isUI(true);
          $("#btnScriptUI").removeClass("hide");
          $("#ScriptUIWrench").removeClass("hide");
          $("#ScriptUIButtons").addClass("hide");
          $("#ScriptUIButtons").html("");
          $("#ScriptUIKeys").addClass("hide");
          $("#ScriptUIKeys").html("");
          $("#ScriptUIModal hr").addClass("hide");
          break;
        case "UIAddButton":
          $("#ScriptUIWrench").addClass("hide");
          $("#ScriptUIButtons").removeClass("hide");

          if (!$("#ScriptUIKeys").hasClass("hide")) {
            $("#ScriptUIModal hr").removeClass("hide");
          }

          var li = "<li>";
          li += "<a href=\"#\" class=\"button btnScriptUI\" data-toggle=\"" + data.toggle + "\" data-buttonname=\"" + data.name + "\">";
          li += "<span class=\"fa " + data.icon + " fa-2x\"></span><br>"
          li += data.caption;
          li += "</a>";
          li += "</li>";
          $("#ScriptUIButtons").append(li);
          break;
        case "UIAddKey":
          var div = "";
          var arrows = ["up", "down", "left", "right"];
          var alphabet = "abcdefghijklmnopqrstuvwxyz";
          var keymap = {
              "up": 38,
              "down": 40,
              "left": 37,
              "right": 39,
              "space": 32,
              "a": 65,
              "b": 66,
              "c": 67,
              "d": 68,
              "e": 69,
              "f": 70,
              "g": 71,
              "h": 72,
              "i": 73,
              "j": 74,
              "k": 75,
              "l": 76,
              "m": 77,
              "n": 78,
              "o": 79,
              "p": 80,
              "q": 81,
              "r": 82,
              "s": 83,
              "t": 84,
              "u": 85,
              "v": 86,
              "w": 87,
              "x": 88,
              "y": 89,
              "z": 90
          };

          if (data.key == "space") {
            // Key is space bar
            div = "<div class=\"keyboardKey space\" data-key=\"" + data.key + "\" data-keycode=\"" + keymap[data.key] + "\">&nbsp;</div>";
          } else if (arrows.indexOf(data.key) > -1) {
            // Key is an arrow
            div = "<div class=\"keyboardKey\"  data-key=\"" + data.key + "\" data-keycode=\"" + keymap[data.key] + "\"><span class=\"fa fa-caret-" + data.key + "\"></span></div>";
          } else if (alphabet.indexOf(data.key) > -1) {
            // Key is a letter
            div = "<div class=\"keyboardKey letter\"  data-key=\"" + data.key + "\" data-keycode=\"" + keymap[data.key] + "\">" + data.key + "</div>";
          } else {
            return;
          }

          $("#ScriptUIWrench").addClass("hide");
          $("#ScriptUIKeys").removeClass("hide");
          $("#ScriptUIKeys").append(div);

          if (!$("#ScriptUIButtons").hasClass("hide")) {
            $("#ScriptUIModal hr").removeClass("hide");
          }

          break;
        }
    };

    // Don't submit form on enter
    $("input,select").keypress(function(evt) {
      return evt.keyCode != 13;
    });

    self.saveFileData = function() {
      var data = generateXml();

      self.fileIsModified(false);
      return data;
    };

    self.loadFileData = function(data) {
      if (data == undefined) {
        return;
      }
      if (Blockly == null) {
        // Wait for blockly to load
        setTimeout(function() {
          // Load script
          console.log("Open file");
          ignoreNextChangeEvt = true;
          Blockly.mainWorkspace.clear();
          var xml = Blockly.Xml.textToDom(data);
          Blockly.Xml.domToWorkspace(workspace, xml);

          // Update filename and asterisk var filename_no_ext = filename; if (filename_no_ext.slice(-4) == ".lua" || filename_no_ext.slice(-4) == ".LUA") { 	filename_no_ext = filename_no_ext.slice(0, -4); } self.fileName(filename_no_ext);
          self.fileIsModified(false);
        }, 1000);
        return;
      }
      // Load script
      ignoreNextChangeEvt = true;
      Blockly.mainWorkspace.clear();
      var xml = Blockly.Xml.textToDom(data);
      Blockly.Xml.domToWorkspace(workspace, xml);

      // Update filename and asterisk var filename_no_ext = filename; if (filename_no_ext.slice(-4) == ".lua" || filename_no_ext.slice(-4) == ".LUA") { 	filename_no_ext = filename_no_ext.slice(0, -4); } self.fileName(filename_no_ext);
      self.fileIsModified(false);
    };

    self.newFileData = function() {
      ignoreNextChangeEvt = true;
      if (Blockly != null) {
        Blockly.mainWorkspace.clear();
      }

      self.fileIsModified(false);
    };

    self.startStopScript = function() {
      if (!self.isRunning()) {
        // Start the script
        var luacode = generateLua();
        var xmlcode = generateXml();

        $.ajax({
          dataType: "json",
          data: {
            luacode: luacode,
            xmlcode: xmlcode,
            name: scriptname,
            modified: isScriptModified ? 1 : 0
          },
          type: "POST",
          url: "startscript",
          success: function(data) {
            if (data.status == "error") {
              addError(data.message);
            }
          }
        });
      } else {
        // Stop the script
        $.ajax({
          dataType: "json",
          data: {},
          type: "POST",
          url: "stopscript",
          success: function(data) {
            if (data.status == "error") {
              addError(data.message);
            }
          }
        });
      }
    };

    // Clear log
    self.clearLog = function() {
      $("#console").html("");
    };

    // Code view
    self.codeView = function() {
      if (codeViewOn) {
        // Switch to Blockly
        $("#pnlCode").addClass("hide");
        $("#pnlBlockly").removeClass("hide");
        //$("#btnCodeView").removeClass("active");
      } else {
        // Switch to code
        var code = generateLua();
        editor.setValue(code);
        editor.gotoLine(1, 0, false);

        $("#pnlCode").removeClass("hide");
        $("#pnlBlockly").addClass("hide");
        //$("#btnCodeView").addClass("active");

        editor.resize();
      }
      codeViewOn = !codeViewOn;
    };

    $(document).on("opened.fndtn.reveal", "#ScriptUIModal[data-reveal]", function() {
      monitorKeypresses = true;
    });
    $(document).on("closed.fndtn.reveal", "#ScriptUIModal[data-reveal]", function() {
      monitorKeypresses = false;
    });

    // Monitor keypresses
    var keysDown = {};
    $(document).keydown(function(evt) {
      if (!monitorKeypresses) {
          return;
      }

      var keycode = (evt.keyCode ? evt.keyCode : evt.which);

      if (keysDown[keycode] == null) {
        // First press
        var elem = $("#ScriptUIKeys .keyboardKey[data-keycode=" + keycode + "]");
        elem.addClass("down");

        if (connReady) {
          conn.send(JSON.stringify({
            action: "keyDown",
            key: elem.data("key")
          }));
        }

        keysDown[keycode] = true;
      }
    });

    $(document).keyup(function(evt) {
      if (!monitorKeypresses) {
        return;
      }
      var keycode = (evt.keyCode ? evt.keyCode : evt.which);
      keysDown[keycode] = null;

      var elem = $("#ScriptUIKeys .keyboardKey[data-keycode=" + keycode + "]");
      elem.removeClass("down");

      if (connReady) {
        conn.send(JSON.stringify({
          action: "keyUp",
          key: elem.data("key")
        }));
      }
    });

    $("#ScriptUIModal").on("mousedown", "a.btnScriptUI", function() {
      var elem = $(this);
      if (connReady && !elem.hasClass("toggled")) {
        conn.send(JSON.stringify({
          action: "buttonDown",
          button: elem.data("buttonname")
        }));
      }
    });

    $("#ScriptUIModal").on("mouseup", "a.btnScriptUI", function() {
      var elem = $(this);

      if (elem.data("toggle")) {
        // Toggle button
        if (elem.hasClass("toggled")) {
          if (connReady) {
            conn.send(JSON.stringify({
              action: "buttonUp",
              button: elem.data("buttonname")
            }));
          }
        }
        elem.toggleClass("toggled");
      } else {
        // Regular button
        if (connReady) {
          conn.send(JSON.stringify({
            action: "buttonUp",
            button: elem.data("buttonname")
          }));
        }
      }
    });

    self.scriptUI = function() {
      $("#ScriptUIModal").foundation("open");
    };

  };
  // This makes Knockout get to work
  var model = new Model();
  ko.applyBindings(model);
  model.fileIsModified(false);

  // if (Blockly != null) {
  config_file_operations("", model.fileExtension(), model.saveFileData, model.loadFileData, model.newFileData);
  loadFileHandler('currentscript.xml.tmp');
  // }
});
