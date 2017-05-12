var modules_definition = {};

// Converts from degrees to radians.
Math.radians = function(degrees) {
  return degrees * Math.PI / 180;
};

// Converts from radians to degrees.
Math.degrees = function(radians) {
  return radians * 180 / Math.PI;
};

function constrain(val, min, max) {
  return Math.min(max, Math.max(val, min));
}
function grid_to_screen(val) {
  // Make sure the grid value is an int
  val = Math.round(val) - 1;
  // 8mm between grid holes
  val *= virtualModel.grid.space;
  // start value
  val += virtualModel.grid.start;
  return val;
}
function screen_to_grid(val) {
  // start value
  val -= virtualModel.grid.start;
  // 8mm between grid holes
  val /= virtualModel.grid.space;
  // Make sure the grid value is an int
  return Math.round(val) - 1;
}
function mm_to_screen(val) {
  return val * virtualModel.grid.scale;
}
function snap_to_grid_x(value, object) {
  var size12 = (object.rotation%180 == 0 ? object.width : object.height) / 2;
  var min = virtualModel.grid.x + size12;
  var max = virtualModel.grid.x + virtualModel.grid.width - size12

  // Constrain value
  value = constrain(value, min, max);
  value -= virtualModel.grid.x;
  // Startposition
  value -= virtualModel.grid.start;
  // 8mm between holes
  value /= virtualModel.grid.space;
  // Make sure the grid value is an int
  value = Math.round(value);
  // convert back
  value *= virtualModel.grid.space;
  value += virtualModel.grid.start;
  value += virtualModel.grid.x;

  return value;
}
function snap_to_grid_y(value, object) {
  var size12 = (object.rotation%180 == 0 ? object.height : object.width) / 2;
  var min = virtualModel.grid.y + size12;
  var max = virtualModel.grid.y + virtualModel.grid.height - size12

  // Constrain value
  value = constrain(value, min, max);
  value -= virtualModel.grid.y;
  // Startposition
  value -= virtualModel.grid.start;
  // 8mm between holes
  value /= virtualModel.grid.space;
  // Make sure the grid value is an int
  value = Math.round(value);
  // convert back
  value *= virtualModel.grid.space;
  value += virtualModel.grid.start;
  value += virtualModel.grid.y;

  return value;
}
var Grid = function() {
  var self = this;
  self.x      = 30;
  self.y      = 30;
  self.holesX = 25;
  self.holesY = 36;

  self.object = main_svg.image('/static/images/robot/grids/A4_portrait.svg');
  self.object.addClass('grid');
  self.object.move(self.x, self.y);
  self.object.draggable().on('dragmove', function(e) { e.preventDefault(); });
  self.object.on('mousedown', function(){
    if (virtualModel.selected_module != undefined) {
      virtualModel.selected_module.deselect();
    }
  });
  self.resize = function(width) {
    self.width  = width - (2 * self.x);
    self.scale  = self.width / 205;
    self.height = 293 * self.scale;
    self.start  = 6.5 * self.scale;
    self.space  = 8 * self.scale;

    main_svg.size(width, self.height + (2 * self.y));

    self.object.size(self.width, self.height);
  };

  self.resize(470);
};
var Servo = function(pin, mid, min, max) {
  var self = this;
  self.pin = (pin || -1);
  self.mid = (mid || 1500);
  self.min = (min || -100);
  self.max = (max || 100);
};
var Dof = function(name) {
  var self = this;
  self.name           = name;
  self.name_formatted = name.replace(' ', '_');
  self.value          = 0;
  self.to_value       = 0;
  self.isServo        = false;
  self.servo          = new Servo(-1, 1500, 0, 0);
  self.poly           = [];
  self.interval       = undefined;
  for (var i = 0; i < 20; i++) {
      self.poly.push(0);
  }

  self.setServo = function(pin, mid, min, max) {
    self.servo = new Servo(pin, mid, min, max);
    self.isServo = true;
  };
  self.set_poly = function(poly) {
    if (poly.length < 20) { return; }
    for (var i = 0; i < 20; i++) {
        self.poly[i] = constrain(poly[i] || 0, -1, 1);
    }
  };
  self.update_single_poly = function(index) {
    if (index < 0 || index > 19) { return; }
    self.poly[index] = ((constrain(self.value || 0, -1, 1)));
  };
  self.apply_poly = function(index, update_call) {
    if (index < 0 || index > 19) { return; }
    self.set_value(self.poly[index], update_call);
  };
  self.set_value = function(value, update_call) {
    value = constrain(value || 0, -1, 1);

    // Make a smooth transition between the old and new dof value
    if (self.interval != undefined) {
      clearInterval(self.interval);
    }
    var steps = 10;
    var step = (value - self.value) / steps;
    var delay = Math.abs(step) * 200;
    self.value = constrain(self.value + step, -1, 1);
    self.interval = setInterval(function() {
      self.value = constrain(self.value + step, -1, 1);
      steps--;
      if (steps <= 1) {
        self.value = value;
        clearInterval(self.interval);
        self.interval = undefined;
      }
      if (update_call != undefined) { update_call(); }
    }, delay);
  };
};
var Module = function(svg_code, specs, config) {
  var self = this;

  self.code     = svg_code || '';
  self.specs    = specs || '';
  self._config   = undefined;

  self.name           = '';
  self.type           = '';
  self.x              = 0;
  self.y              = 0;
  self.grid_x         = 0;
  self.grid_y         = 0;
  self.width          = 0;
  self.height         = 0;
  self.actual_width   = 0;
  self.actual_height  = 0;
  self.rotation       = 0;
  self.dofs           = [];
  self._drag_offset   = [0, 0];

  self.set_dofs = function(values) {
    if (values.length != self.dofs.length) {
      console.log('error dofs');
      return;
    }
    for (var i = 0; i < self.dofs.length; i++) {
      self.dofs[i].value = constrain(values[i] || 0, -1, 1);
    }
    self.update_dofs();
  };
  self.apply_poly = function(index) {
    if (index < 0 || index > 19) { return; }
    for (var i = 0; i < self.dofs.length; i++) {
      self.dofs[i].apply_poly(index, self.update_dofs);
    }
  };

  self.set_pos = function(x, y) {
    self.x = snap_to_grid_x(x, self);
    self.y = snap_to_grid_y(y, self);
    self.update();
  };
  self.update_grid_pos = function() {
    self.grid_x = screen_to_grid(self.x);
    self.grid_y = screen_to_grid(self.y);
  };
  self.set_size = function(width, height) {
    self.width = width;
    self.height = height;
    self.update();config
  };
  self.set_rotation = function(rotation) {
    rotation = rotation % 360;
    self.rotation = (Math.round(rotation / 90) * 90); // 90° angles only
    // When object is over the side -> reposition
    self.set_pos(self.x, self.y);
  };
  self.rotate = function() {
    self.set_rotation(self.rotation + 90);
  };
  self.update_dofs = function() {};
  self.update = function() {
    if (self.object == undefined) { return; }

    var maxSize = Math.max(self.width, self.height);
    self.object.size(maxSize, maxSize);

    self.object.center(self.x, self.y);
    self.group.rotate(self.rotation);
  };
  self.resize = function() {

    if (self.extra != undefined) {
      self.resize_extra();
    }
    self.set_pos(virtualModel.grid.x + grid_to_screen(self.grid_x), virtualModel.grid.y + grid_to_screen(self.grid_y));
    self.set_size(mm_to_screen(self.actual_width), mm_to_screen(self.actual_height));

  };
  self._drag_move = function(e) {
    e.preventDefault();

    if (e.detail.event.type != 'mousemove') { return; }

    var x = e.detail.event.pageX - virtualModel.canvasX - self._drag_offset[0];
    var y = e.detail.event.pageY - virtualModel.canvasY - self._drag_offset[1];

    self.set_pos(x, y);
    self.update_grid_pos();
  };
  self._mouse_down = function(e) {
    self._drag_offset = [e.pageX - virtualModel.canvasX - self.x, e.pageY - virtualModel.canvasY - self.y];
    self.select();
  };
  self.remove = function() {
    self.deselect();
    self.object.remove();
    if (self.extra != undefined) {
      self.extra.remove();
    }
    var index = virtualModel.modules.indexOf(self);
    if (index > -1) {
      virtualModel.modules.splice(index, 1);
    }
  };
  self.select = function() {
    if (virtualModel.selected_module != undefined) {
      virtualModel.selected_module.deselect();
    }
    self.object.front();
    if (self.extra != undefined) {
      self.extra.front();
    }
    self.object.addClass('selected_module');
    virtualModel.selected_module = self;
    // Notify other scripts
    virtualModel.notify();
  };
  self.deselect = function() {
    self.object.removeClass('selected_module');
    virtualModel.selected_module = undefined;
    // Notify other scripts
    virtualModel.notify();
  };

  // Apply parameters
  if (self.specs != '') {
    self.type = self.specs.type;
    self.name = self.type;
    self.actual_width = self.specs.size.width;
    self.actual_height = self.specs.size.height;
    self.resize();

    // initialize dofs if the module has any
    if (self.specs.dofs != undefined) {
      for (var i = 0; i < self.specs.dofs.length; i++) {
        var newdof = new Dof(self.specs.dofs[i].name);
        if (self.specs.dofs[i].servo != undefined) {
          newdof.setServo(-1, 1500, self.specs.dofs[i].servo.min, self.specs.dofs[i].servo.max)
        }
        self.dofs.push(newdof);
      }
    }
  }
  self.set_config = function(conf) {
    if (conf != undefined && conf != '') {
      self._config = conf;
      self.name = self._config.name;
      self.grid_x = self._config.grid.x;
      self.grid_y = self._config.grid.y;
      self.resize();
      self.set_rotation(self._config.grid.rotation || 0);

      if (self._config.dofs != undefined) {
        for (var i = 0; i < self._config.dofs.length; i++) {
          var dof = self._config.dofs[i];
          if (dof.servo != undefined) {
            self.dofs[i].servo.pin = dof.servo.pin;
            self.dofs[i].servo.mid = dof.servo.mid;
            self.dofs[i].servo.min = dof.servo.min;
            self.dofs[i].servo.max = dof.servo.max;
          }
          if (dof.poly != undefined) {
            self.dofs[i].set_poly(dof.poly);
          }
        }
      }
    }
  };
  self.set_config(config);

  self.get_config = function() {
    if (self._config == undefined || self._config == '') {
      self._config = {};
    }
    if (self._config != undefined && self._config != '') {
      self._config.name = self.name;
      self._config.type = self.type;

      if (self._config.grid == undefined) {
        self._config.grid = {};
      }
      self._config.grid.x = self.grid_x;
      self._config.grid.y = self.grid_y;
      self._config.grid.rotation = self.rotation;

      if (self._config.dofs == undefined) {
        self._config.dofs = [];
      }
      for (var i = 0; i < self.dofs.length; i++) {
        var dof = self.dofs[i];
        if (self._config.dofs[i] == undefined) {
          self._config.dofs[i] = {};
        }
        self._config.dofs[i].name = dof.name;
        if (dof.servo != undefined) {
          if (self._config.dofs[i].servo == undefined) {
            self._config.dofs[i].servo = {}
          }
          self._config.dofs[i].servo.pin = dof.servo.pin;
          self._config.dofs[i].servo.mid = dof.servo.mid;
          self._config.dofs[i].servo.min = dof.servo.min;
          self._config.dofs[i].servo.max = dof.servo.max;
        }
        if (dof.poly != undefined) {
          self._config.dofs[i].poly = dof.poly;
        }
      }
    }
    return self._config;
  };

  if (self.code != '') {
    self.visual = main_svg.svg(self.code);

    self.object = self.visual.select('.object').last();
    self.group = self.object.select('.group').last();

    if (virtualModel.edit) {
      if (virtualModel.move) {
        // add drag events
        self.object.style('cursor', 'move');
        self.object.draggable().on('dragmove', self._drag_move);
        if (self.extra != undefined) {
          self.extra.style('cursor', 'move');
          self.extra.draggable().on('dragmove', self._drag_move);
        }
      } else {
        self.object.style('cursor', 'pointer');
        self.object.draggable().on('dragmove', function(e) { e.preventDefault(); });
        if (self.extra != undefined) {
          self.extra.style('cursor', 'pointer');
          self.extra.draggable().on('dragmove', function(e) { e.preventDefault(); });
        }
      }
      self.object.on('mousedown', self._mouse_down);
      if (self.extra != undefined) {
        self.extra.on('mousedown', self._mouse_down);
      }
    }
    self.update();
  }

};

var VirtualModel = function() {
  var self = this;

  // create svg drawing
  main_svg = SVG('model_screen');

  self.edit = false;
  self.move = false;
  if ($('#model_screen').hasClass('edit')) {
    self.edit = true;
  }
  if ($('#model_screen').hasClass('config')) {
    self.move = true;
  }

  self.change_handler = undefined;
  self.notify = function() {
    if (self.change_handler == undefined) {
      return;
    }
    self.change_handler();
  };

  self.grid = new Grid();
  self.modules = [];
  self.selected_module = undefined;
  self.set_config = function(conf) {
    var mod_count = self.modules.length;
    for (var i = 0; i < mod_count; i++) {
      self.modules[0].remove();
    }
    if (conf == undefined || conf == '') { return; }
    var mod_conf = conf['modules'];
    if (mod_conf != undefined) {
      for (var i = 0; i < mod_conf.length; i++) {
        self.add_module(mod_conf[i].type, mod_conf[i]);
      }
    }
    virtualModel.notify();
  }
  self.get_config = function() {
    var mod_count = self.modules.length;
    var config_modules = [];
    for (var i = 0; i < mod_count; i++) {
      config_modules.push(self.modules[i].get_config());
    }
    return { 'modules': config_modules };
  }
  self.init = function() {
    self.set_config(configs);
  };
  self.add_module = function(mod_type, config) {
    var mod = new modules_definition[mod_type](svg_codes[mod_type], specs[mod_type], config);
    self.modules.push(mod);
  };
  self.resize = function() {
    // update grid x & y reference points
    var rect = $('svg').first().position();
    self.canvasX = rect.left;
    self.canvasY = rect.top;

    self.grid.resize($('#model_screen').width());

    for (var i = 0; i < self.modules.length; i++) {
      self.modules[i].resize();
    }
  };
  self.resize();

  self.update_dofs = function(dofs) {
    if (dofs == undefined) { return; }
    for (var i = 0; i < self.modules.length; i++) {
      var mod = self.modules[i];
      for (var j = 0; j < mod.dofs.length; j++) {
        var dof = mod.dofs[j];
        if (dof.servo.pin >= 0) {
          dof.set_value(dofs[dof.servo.pin], mod.update_dofs);
        }
      }
    }
  };
  self.apply_poly = function(poly_index) {
    if (poly_index == undefined || poly_index < 0) { return; }
    for (var i = 0; i < self.modules.length; i++) {
      self.modules[i].apply_poly(poly_index);
    }
  };

  self.sound = undefined;
  self.update_sound = function(type, msg) {
    var icon = 'fa-music'
    if (type == 'tts') {
      icon = 'fa-commenting-o'
    }
    $('.robot_sound').html('<span class="fa ' + icon + '"></span> ' + msg);

    var sound_src = '/sound/?t=' + type + '&f=' + msg;
    if (self.sound == undefined) {
      self.sound = new Audio(sound_src);
    } else {
      self.sound.pause();
      self.sound.src = sound_src;
      self.sound.load();
    }
    self.sound.play();
  };
};

var main_svg;
var virtualModel = new VirtualModel();

$(document).ready(function() {
  virtualModel.init();

  $(window).resize(virtualModel.resize);

});
