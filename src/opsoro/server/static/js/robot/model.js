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
  val = Math.round(val);
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
  return Math.round(val);
}
function mm_to_screen(val) {
  return val * virtualModel.grid.scale;
}
function snap_to_grid_x(value, object) {
  var size12 = (object.rotation()%180 == 0 ? object.width() : object.height()) / 2;
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
  var size12 = (object.rotation()%180 == 0 ? object.height() : object.width()) / 2;
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
var Expression = function(name, filename, poly_index, dof_values) {
  var self = this;
  self.name       = name || '';
  self.default    = '2753';
  self.filename   = ko.observable(filename || self.default);
  self.poly_index = ko.observable(poly_index || -1);
  self.dof_values = dof_values || [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ];
  self.selected   = ko.observable(false);

  self.update = function() {
    if (!self.selected()) { return; }
    var dofs = self.dof_values;
    for (var i = 0; i < virtualModel.modules().length; i++) {
      var mod = virtualModel.modules()[i];
      for (var j = 0; j < mod.dofs().length; j++) {
        dofs[mod.dofs()[j].servo().pin()] = parseFloat(mod.dofs()[j].value());
      }
    }
    self.dof_values = dofs;
    robotSendReceiveAllDOF(self.dof_values);
  };

  self.select = function() {
    for (var i = 0; i < virtualModel.expressions().length; i++) {
      virtualModel.expressions()[i].selected(false);
    }
    virtualModel.selected_expression(self);

    if (self.poly_index() < 0) {
      // Use dof values
      for (var i = 0; i < virtualModel.modules().length; i++) {
        var mod = virtualModel.modules()[i];
        for (var j = 0; j < mod.dofs().length; j++) {
          mod.dofs()[j].value(self.dof_values[mod.dofs()[j].servo().pin()]);

          mod.update_dofs();
        }
      }
    } else {
      // Use dof poly
      for (var i = 0; i < virtualModel.modules().length; i++) {
        virtualModel.modules()[i].apply_poly(self.poly_index());
      }
    }
    self.selected(true);
  };
  self.update_icon = function(icon) {
    self.filename(icon);
    $("#PickIconModal").foundation("close");
  };
  self.change_icon = function() {
    // Reset icons
    for (var i = 0; i < virtualModel.used_icons.length; i++) {
      if (virtualModel.used_icons[i] == self.default) {
        continue;
      }
      virtualModel.icons.push(virtualModel.used_icons[i]);
    }
    virtualModel.used_icons = []
    for (var i = 0; i < virtualModel.expressions().length; i++) {
      virtualModel.icons.remove(virtualModel.expressions()[i].filename());
      virtualModel.used_icons.push(virtualModel.expressions()[i].filename());
    }
    virtualModel.icons.sort();
    // View icons
    $("#PickIconModal").foundation("open");
  };
  self.remove = function() {
    virtualModel.expressions.remove(self);
    if (virtualModel.expressions().length > 0) {
      virtualModel.expressions()[0].select();
    }
  };

};
var Grid = function(pin, mid, min, max) {
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
    if (virtualModel.selected_module() != undefined) {
      virtualModel.selected_module().deselect();
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
  self.pin = ko.observable(pin || 0);
  self.mid = ko.observable(mid || 1500);
  self.min = ko.observable(min || -100);
  self.max = ko.observable(max || 100);

  self.update_mid = function() {
    if(connReady){
      conn.send(JSON.stringify({
        action: "setServoPos",
        pin: self.pin(),
        value: self.mid(),
      }));
    }
  };
  self._update_mid = ko.computed(function() {
    if(connReady){
      conn.send(JSON.stringify({
        action: "setServoPos",
        pin: self.pin(),
        value: self.mid(),
      }));
    }
    return self.mid();
  }, self);
};
var Dof = function(name) {
  var self = this;
  self.name           = ko.observable(name);
  self.name_formatted = ko.observable(name.replace(' ', '_'));
  self.value          = ko.observable(0);
  self.isServo        = ko.observable(false);
  self.servo          = ko.observable(new Servo(0, 1500, 0, 0));
  self.poly           = ko.observableArray();
  for (var i = 0; i < 20; i++) {
      self.poly.push(0);
  }

  self.setServo = function(pin, mid, min, max) {
    self.servo(new Servo(pin, mid, min, max));
    self.isServo(true);
  };
  self.set_poly = function(poly) {
    if (poly.length < 20) { return; }
    self.poly.removeAll();
    for (var i = 0; i < 20; i++) {
        self.poly.push((constrain(poly[i] || 0, -1, 1)));
    }
  };
  self.update_single_poly = function(index) {
    if (index < 0 || index > 19) { return; }
    self.poly()[index] = ((constrain(self.value() || 0, -1, 1)));
  };
  self.apply_poly = function(index) {
    if (index < 0 || index > 19) { return; }
    self.value(self.poly()[index]);
  };
};
var Module = function(svg_code, specs, config) {
  var self = this;

  self.code     = svg_code || '';
  self.specs    = specs || '';
  self.config   = config || '';

  self.name           = new ClickToEdit("", "Untitled");
  self.type           = ko.observable('');
  self.x              = ko.observable(0);
  self.y              = ko.observable(0);
  self.grid_x         = ko.observable(0);
  self.grid_y         = ko.observable(0);
  self.width          = ko.observable(0);
  self.height         = ko.observable(0);
  self.actual_width   = ko.observable(0);
  self.actual_height  = ko.observable(0);
  self.rotation       = ko.observable(0);
  self.dofs           = ko.observableArray();
  self._drag_offset   = [0, 0];

  self.set_dofs = function(values) {
    if (values.length != self.dofs().length) {
      console.log('error dofs');
      return;
    }
    for (var i = 0; i < self.dofs().length; i++) {
      self.dofs()[i].value(constrain(values[i] || 0, -1, 1));
    }
    self.update_dofs();
  };
  self.apply_poly = function(index) {
    if (index < 0 || index > 19) { return; }
    for (var i = 0; i < self.dofs().length; i++) {
      self.dofs()[i].apply_poly(index);
    }
    self.update_dofs();
  };

  self.set_pos = function(x, y) {
    // Reset rotation for position movement
    if (self.object != undefined) {
      // self.object.rotate(0, self.x(), self.y());
      // self.group.rotate(0);
    }
    self.x(snap_to_grid_x(x, self));
    self.y(snap_to_grid_y(y, self));
    self.grid_x(screen_to_grid(self.x()));
    self.grid_y(screen_to_grid(self.y()));
    self.update();
  };
  self.set_size = function(width, height) {
    self.width(width);
    self.height(height);
    self.update();
  };
  self.set_rotation = function(rotation) {
    rotation = rotation % 360;
    self.rotation(Math.round(rotation / 90) * 90); // 90° angles only
    // When object is over the side -> reposition
    self.set_pos(self.x(), self.y());
  };
  self.rotate = function() {
    self.set_rotation(self.rotation() + 90);
  };
  self.update_dofs = function() {};
  self.update = function() {
    if (self.object == undefined) { return; }

    var maxSize = Math.max(self.width(), self.height());
    self.object.size(maxSize, maxSize);

    self.object.center(self.x(), self.y());
    // self.object.rotate(self.rotation(), self.x(), self.y());
    self.group.rotate(self.rotation());
  };
  self._drag_move = function(e) {
    e.preventDefault();

    if (e.detail.event.type != 'mousemove') { return; }

    var x = e.detail.event.pageX - virtualModel.canvasX - self._drag_offset[0];
    var y = e.detail.event.pageY - virtualModel.canvasY - self._drag_offset[1];

    self.set_pos(x, y);
  };
  self._mouse_down = function(e) {
    self._drag_offset = [e.pageX - virtualModel.canvasX - self.x(), e.pageY - virtualModel.canvasY - self.y()];
    self.select();
  };
  self.remove = function() {
    self.deselect();
    self.object.remove();
    if (self.extra != undefined) {
      self.extra.remove();
    }
    virtualModel.modules.remove(self);
  };
  self.select = function() {
    if (virtualModel.selected_module() != undefined) {
      virtualModel.selected_module().deselect();
    }
    self.object.front();
    if (self.extra != undefined) {
      self.extra.front();
    }
    self.object.addClass('selected_module');
    virtualModel.selected_module(self);
    Foundation.reInit($('[data-slider]'));
  };
  self.deselect = function() {
    self.object.removeClass('selected_module');
    virtualModel.selected_module(undefined);
  };

  // Apply parameters
  if (self.specs != '') {
    self.type(self.specs.type);
    self.name.value(self.type());
    self.set_size(mm_to_screen(self.specs.size.width), mm_to_screen(self.specs.size.height));
    self.actual_width(self.specs.size.width);
    self.actual_height(self.specs.size.height);

    // initialize dofs if the module has any
    if (self.specs.dofs != undefined) {
      for (var i = 0; i < self.specs.dofs.length; i++) {
        var newdof = new Dof(self.specs.dofs[i].name);
        if (self.specs.dofs[i].servo != undefined) {
          newdof.setServo(0, 1500, self.specs.dofs[i].servo.min, self.specs.dofs[i].servo.max)
        }
        self.dofs.push(newdof);
      }

      self._update_dofs = ko.computed(function() {
        if (self.dofs().length == 0) { return undefined; }

        if (virtualModel.selected_expression().selected()) {
          if (virtualModel.selected_expression().poly_index() < 0) {
          } else {
            for (var i = 0; i < self.dofs().length; i++) {
              self.dofs()[i].update_single_poly(virtualModel.selected_expression().poly_index());
            }
          }
          virtualModel.selected_expression().update();
        }
        self.update_dofs();
        return self.dofs()[0].value();
      }, self);
    }
  }
  if (self.config != '') {
    self.name.value(self.config.name);
    self.grid_x(self.config.grid.x);
    self.grid_y(self.config.grid.y);
    self.set_pos(virtualModel.grid.x + grid_to_screen(self.config.grid.x), virtualModel.grid.y + grid_to_screen(self.config.grid.y));
    self.set_rotation(self.config.grid.rotation || 0);

    if (self.config.dofs != undefined) {
      for (var i = 0; i < self.config.dofs.length; i++) {
        var dof = self.config.dofs[i];
        if (dof.servo != undefined) {
          self.dofs()[i].servo().pin(dof.servo.pin);
          self.dofs()[i].servo().mid(dof.servo.mid);
        }
        if (dof.mapping != undefined) {
          self.dofs()[i].set_poly(dof.mapping.poly)
        }
      }
    }


  }
  if (self.code != '') {
    self.visual = main_svg.svg(self.code);

    self.object = self.visual.select('.object').last();
    self.group = self.object.select('.group').last();

    if (virtualModel.edit()) {
      // add drag events
      self.object.style('cursor', 'grab');
      self.object.draggable().on('dragmove', self._drag_move);
      if (self.extra != undefined) {
        self.extra.style('cursor', 'grab');
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
    self.update();
  }

};

var VirtualModel = function() {
  var self = this;

  // create svg drawing
  main_svg = SVG('model_screen');

  self.edit = ko.observable(false);
  if ($('#model_screen').hasClass('edit')) {
    self.edit(true);
  }

  self.available_servos = ko.observableArray();
  for (var i = 0; i < 16; i++) {
    self.available_servos.push(i);
  }

  self.grid = new Grid();
  self.modules = ko.observableArray();
  self.selected_module = ko.observable();
  self.init = function() {
    if (expression_data != undefined) {
      for (var i = 0; i < expression_data.length; i++) {
        var dat = expression_data[i];
        self.add_expression(dat.name, dat.filename, dat.poly, dat.dofs);
      }
    } else {
      self.add_expression('', '1f610');
    }
    self.expressions()[0].selected(true);
    self.selected_expression(self.expressions()[0]);
    for (var i = 0; i < configs.length; i++) {
      var mod_type = configs[i].type;
      self.add_module(mod_type, configs[i]);
    }
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
  };
  self.resize();

};

var main_svg;
var virtualModel;

$(document).ready(function() {
  virtualModel = new VirtualModel();
  virtualModel.init();
  ko.applyBindings(virtualModel);

  $(window).resize(virtualModel.resize);
  init_touch();
});

function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("module_type", ev.target.id);
}

function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("module_type");
  virtualModel.add_module(data, '');
  virtualModel.modules()[virtualModel.modules().length-1].set_pos(ev.pageX - virtualModel.canvasX, ev.pageY - virtualModel.canvasY);
  virtualModel.modules()[virtualModel.modules().length-1].select();
}

function touchHandler(event) {
  var touch = event.changedTouches[0];

  var simulatedEvent = document.createEvent("MouseEvent");
    simulatedEvent.initMouseEvent({
    touchstart: "mousedown",
    touchmove: "mousemove",
    touchend: "mouseup"
  }[event.type], true, true, window, 1,
    touch.screenX, touch.screenY,
    touch.clientX, touch.clientY, false,
    false, false, false, 0, null);

  touch.target.dispatchEvent(simulatedEvent);
  event.preventDefault();
}

function init_touch() {
  document.addEventListener("touchstart", touchHandler, true);
  document.addEventListener("touchmove", touchHandler, true);
  document.addEventListener("touchend", touchHandler, true);
  document.addEventListener("touchcancel", touchHandler, true);
}
