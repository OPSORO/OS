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
var Expression = function(name, filename) {
  var self = this;
  self.name       = ko.observable(name || '');
  self.filename   = ko.observable(filename || '');
  self.poly_index = ko.observable(-1);
  self.dof_values = ko.observableArray();
  self.selected   = ko.observable(false);

  for (var i = 0; i < 16; i++) {
    self.dof_values.push(0);
  }

  self.select = function() {
    for (var i = 0; i < virtualModel.expressions().length; i++) {
      virtualModel.expressions()[i].selected(false);
    }
    self.selected(true);

    if (self.poly_index() < 0) {
      // Use dof values

    } else {
      // Use dof poly

    }
  };
};
var Grid = function(pin, mid, min, max) {
  var self = this;
  self.x      = 30;
  self.y      = 30;
  self.width  = 410;//205;
  self.height = 586;//293;
  self.holesX = 25;
  self.holesY = 36;
  self.scale  = self.width / 205;
  self.start  = 6.5 * self.scale;
  self.space  = 8 * self.scale;

  main_svg.size(self.width + self.x * 2, self.height + self.y * 2);

  self.object = main_svg.image('/static/images/robot/grids/A4_portrait.svg');
  self.object.addClass('grid');
  self.object.size(self.width, self.height);
  self.object.move(self.x, self.y);
  self.object.draggable().on('dragmove', function(e) { e.preventDefault(); });
  self.object.on('mousedown', function(){
    if (virtualModel.selected_module() != undefined) {
      virtualModel.selected_module().Deselect();
    }
  });
};
var Servo = function(pin, mid, min, max) {
  var self = this;
  self.pin = ko.observable(pin || 0);
  self.mid = ko.observable(mid || 1500);
  self.min = ko.observable(min || -1000);
  self.max = ko.observable(max || 1000);
};
var Dof = function(name) {
  var self = this;
  self.name           = ko.observable(name);
  self.name_formatted = ko.observable(name.replace(' ', '_'));
  self.value          = ko.observable(0.00);
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

  self.Set_dofs = function(values) {
    if (values.length != self.dofs().length) {
      console.log('error dofs');
      return;
    }
    for (var i = 0; i < self.dofs().length; i++) {
      self.dofs()[i].value(constrain(values[i] || 0, -1, 1));
    }
    self.Update_dofs();
  };

  self.Set_pos = function(x, y) {
    // Reset rotation for position movement
    if (self.object != undefined) {
      self.object.rotate(0, self.x(), self.y());
    }
    self.x(snap_to_grid_x(x, self));
    self.y(snap_to_grid_y(y, self));
    self.grid_x(screen_to_grid(self.x()));
    self.grid_y(screen_to_grid(self.y()));
    self.Update();
  };
  self.Set_size = function(width, height) {
    self.width(width);
    self.height(height);
    self.Update();
  };
  self.Set_rotation = function(rotation) {
    rotation = rotation % 360;
    self.rotation(Math.round(rotation / 90) * 90); // 90° angles only
    // When object is over the side -> reposition
    self.Set_pos(self.x(), self.y());
  };
  self.Rotate = function() {
    self.Set_rotation(self.rotation() + 90);
  };
  self.Update_dofs = function() {
    console.log('wiiiiiiiiiiiiiiiiii');
  };
  self.Update = function() {
    if (self.object == undefined) { return; }
    self.object.size(self.width(), self.height());
    self.object.center(self.x(), self.y());
    self.object.rotate(self.rotation(), self.x(), self.y());

  };
  self._drag_move = function(e) {
    e.preventDefault();

    if (e.detail.event.type != 'mousemove') { return; }

    var x = e.detail.event.pageX - virtualModel.canvasX - self._drag_offset[0];
    var y = e.detail.event.pageY - virtualModel.canvasY - self._drag_offset[1];

    self.Set_pos(x, y);
  };
  self._mouse_down = function(e) {
    self._drag_offset = [e.pageX - virtualModel.canvasX - self.x(), e.pageY - virtualModel.canvasY - self.y()];
    self.Select();
  };
  self.Remove = function() {
    self.Deselect();
    self.object.remove();
    if (self.extra != undefined) {
      self.extra.remove();
    }
    virtualModel.modules.remove(self);
  };
  self.Select = function() {
    if (virtualModel.selected_module() != undefined) {
      virtualModel.selected_module().Deselect();
    }
    self.object.front();
    if (self.extra != undefined) {
      self.extra.front();
    }
    self.object.style({ stroke: 'rgb(255, 206, 57)' });
    virtualModel.selected_module(self);
    Foundation.reInit($('[data-slider]'));
  };
  self.Deselect = function() {
    self.object.style({ stroke: 'transparent' });
    virtualModel.selected_module(undefined);
  };

  // Apply parameters
  if (self.specs != '') {
    self.type(self.specs.type);
    self.name.value(self.type());
    self.Set_size(mm_to_screen(self.specs.size.width), mm_to_screen(self.specs.size.height));
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

      self._update_dofs   = ko.computed(function() {
        self.Update_dofs();
        if (self.dofs().length == 0) { return undefined; }
        return self.dofs()[0].value();
      }, self);
    }
  }
  if (self.config != '') {
    self.name.value(self.config.name);
    self.grid_x(self.config.grid.x);
    self.grid_y(self.config.grid.y);
    self.Set_pos(virtualModel.grid.x + grid_to_screen(self.config.grid.x), virtualModel.grid.y + grid_to_screen(self.config.grid.y));
    self.Set_rotation(self.config.grid.rotation || 0);

    if (self.config.dofs != undefined) {
      for (var i = 0; i < self.config.dofs.length; i++) {
        var dof = self.config.dofs[i];
        if (dof.servo != undefined) {
          self.dofs()[i].servo().pin(dof.servo.pin);
          self.dofs()[i].servo().mid(dof.servo.mid);
        }
        if (dof.mapping != undefined) {
          for (var i = 0; i < self.dofs()[i].poly().length; i++) {
            self.dofs()[i].poly()[i] = dof.mapping[i];
          }
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
    self.Update();
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
    for (var i = 0; i < configs.length; i++) {
      var mod_type = configs[i].type;
      self.Add_module(mod_type, configs[i]);
    }
  };
  self.Add_module = function(mod_type, config) {
    var mod = new modules_definition[mod_type](svg_codes[mod_type], specs[mod_type], config);
    self.modules.push(mod);
  };
  self.resize = function() {
    // Update grid x & y reference points
    var rect = $('svg').first().position();
    self.canvasX = rect.left;
    self.canvasY = rect.top;
  };
  self.resize();

  if (expression_data != undefined) {
    self.expressions = ko.observableArray();
    for (var i = 0; i < expression_data.length; i++) {
      var exp = new Expression(expression_data[i].name, expression_data[i].filename);
      self.expressions.push(exp);
    }
    self.expressions()[0].selected(true);
  }
};

var main_svg;
var virtualModel;

$(document).ready(function() {
  virtualModel = new VirtualModel();
  virtualModel.init();
  ko.applyBindings(virtualModel);

  $(window).resize(virtualModel.resize);

  // setTimeout("location.reload();", 200);
  init();
});

function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("module_type", ev.target.id);
}

function drop(ev) {
  ev.preventDefault();
  console.log(ev);
  var data = ev.dataTransfer.getData("module_type");
  virtualModel.Add_module(data, '');
  virtualModel.modules()[virtualModel.modules().length-1].Set_pos(ev.pageX - virtualModel.canvasX, ev.pageY - virtualModel.canvasY);
  virtualModel.modules()[virtualModel.modules().length-1].Select();
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

function init() {
  document.addEventListener("touchstart", touchHandler, true);
  document.addEventListener("touchmove", touchHandler, true);
  document.addEventListener("touchend", touchHandler, true);
  document.addEventListener("touchcancel", touchHandler, true);
}
