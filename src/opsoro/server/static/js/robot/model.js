var modules_definition = {};

var canvasX = 0;
var canvasY = 0;
var gridWidth = 410;//205;
var gridHeight = 586;//293;
var gridHolesX = 25;
var gridHolesY = 36;
var scale = gridWidth / 205;
var gridStart = 6.5 * scale;
var gridSpace = 8 * scale;

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

// function grid_to_mm(gridValue) {
//   // Make sure the grid value is an int
//   gridValue = Math.round(gridValue);
//   // start value
//   let mmValue = 6.5;
//   // 8mm between grid holes
//   mmValue += gridValue * 8;
//
//   return mmValue;
// }
function grid_to_screen(val) {
  // Make sure the grid value is an int
  val = Math.round(val);
  // 8mm between grid holes
  val *= gridSpace;
  // start value
  val += gridStart;
  return val;
}
function screen_to_grid(val) {
  // start value
  val -= gridStart;
  // 8mm between grid holes
  val /= gridSpace;
  // Make sure the grid value is an int
  return Math.round(val);
}
function mm_to_screen(val) {
  return val * scale;
}
// function mm_to_grid(val) {
//   // Startposition
//   val -= 6.5;
//   // 8mm between holes
//   let gridValue = mmValue / 8;
//   // Make sure the grid value is an int
//   gridValue = Math.round(gridValue);
//   // Constrain grid value
//   gridValue = constrain(gridValue, 0, 50);
//
//   return gridValue;
// }
function snap_to_grid_x(value, object) {
  let size12 = (object.rotation()%180 == 0 ? object.width() : object.height()) / 2;
  let min = virtualModel.grid.x() + size12;
  let max = virtualModel.grid.x() + gridWidth - size12

  // Constrain value
  value = constrain(value, min, max);
  value -= virtualModel.grid.x();
  // Startposition
  value -= gridStart;
  // 8mm between holes
  value /= gridSpace;
  // Make sure the grid value is an int
  value = Math.round(value);
  // convert back
  value *= gridSpace;
  value += gridStart;
  value += virtualModel.grid.x();

  return value;
}
function snap_to_grid_y(value, object) {
  let size12 = (object.rotation()%180 == 0 ? object.height() : object.width()) / 2;
  let min = virtualModel.grid.y() + size12;
  let max = virtualModel.grid.y() + gridHeight - size12

  // Constrain value
  value = constrain(value, min, max);
  value -= virtualModel.grid.y();
  // Startposition
  value -= gridStart;
  // 8mm between holes
  value /= gridSpace;
  // Make sure the grid value is an int
  value = Math.round(value);
  // convert back
  value *= gridSpace;
  value += gridStart;
  value += virtualModel.grid.y();

  return value;
}

var Servo = function(pin, mid, min, max) {
    var self = this;
    self.pin = ko.observable(pin || 0);
    self.mid = ko.observable(mid || 1500);
    self.min = ko.observable(min || -1000);
    self.max = ko.observable(max || 1000);
};
var Dof = function(name) {
    var self = this;
    self.name = ko.observable(name);
    self.isServo = ko.observable(false);
    self.servo = ko.observable(new Servo(0, 1500, 0, 0));
    // self.isMap = ko.observable(false);
    // self.map = ko.observable(new Mapping(0));
    self.value = ko.observable(0.0);

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

    self._drag_offset     = [0, 0];

    self.Set_dofs = function(values) {
      if (values.length != self.dofs().length) {
        console.log('error dofs');
        return;
      }
      for (let i = 0; i < self.dofs().length; i++) {
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
      self.Set_pos(self.x(), self.y());
    };
    self.Rotate = function() {
      self.Set_rotation(self.rotation() + 90);
    };

    self.Update_dofs = function() {};
    self.Update = function() {
      if (self.object == undefined) { return; }
      self.object.size(self.width(), self.height());
      self.object.center(self.x(), self.y());
      self.object.rotate(self.rotation(), self.x(), self.y());

    };
    self._drag_move = function(e) {
      e.preventDefault();

      if (e.detail.event.type != 'mousemove') { return; }

      let x = e.detail.event.pageX - canvasX - self._drag_offset[0];
      let y = e.detail.event.pageY - canvasY - self._drag_offset[1];

      self.Set_pos(x, y);
    }
    self._mouse_down = function(e) {
      self._drag_offset = [e.pageX - canvasX - self.x(), e.pageY - canvasY - self.y()];
      self.Select();
    }
    self.Remove = function() {
      self.Deselect();
      self.object.remove();
      virtualModel.modules.remove(self);
    };
    self.Select = function() {
      if (virtualModel.selected_module() != undefined) {
        virtualModel.selected_module().Deselect();
      }
      self.object.style({ stroke: 'rgb(255, 206, 57)' })
      virtualModel.selected_module(self);
      $('.slider').foundation('_reflow');
    };
    self.Deselect = function() {
      self.object.style({ stroke: 'transparent' })
      virtualModel.selected_module(undefined);
    };

    // Apply parameters
    if (self.specs != '') {
      self.type(self.specs.type);
      self.Set_size(mm_to_screen(self.specs.size.width), mm_to_screen(self.specs.size.height));
      self.actual_width(self.specs.size.width);
      self.actual_height(self.specs.size.height);

      // initialize dofs if the module has any
      if (self.specs.dofs != undefined) {
        for (let i = 0; i < self.specs.dofs.length; i++) {
          let newdof = new Dof(self.specs.dofs[i].name);
          if (self.specs.dofs[i].servo != undefined) {
            newdof.setServo(0, 1500, self.specs.dofs[i].servo.min, self.specs.dofs[i].servo.max)
          }
          self.dofs().push(newdof);
        }
      }
    }
    if (self.config != '') {
      self.name.value(self.config.name);
      self.grid_x(self.config.grid.x);
      self.grid_y(self.config.grid.y);
      self.Set_pos(virtualModel.grid.x() + grid_to_screen(self.config.grid.x), virtualModel.grid.y() + grid_to_screen(self.config.grid.y));
      self.Set_rotation(self.config.grid.rotation || 0);

      if (self.config.dofs != undefined) {
        for (let i = 0; i < self.config.dofs.length; i++) {
          self.dofs()[i].servo().pin(self.config.dofs[i].servo.pin);
          self.dofs()[i].servo().mid(self.config.dofs[i].servo.mid);
        }
      }
    }
    if (self.code != '') {
      self.visual = main_svg.svg(self.code);

      self.object = self.visual.select('.object').last();
      self.group = self.object.select('.group').last();

      // add drag events
      self.object.style('cursor', 'grab');
      self.object.draggable().on('dragmove', self._drag_move);
      self.object.on('mousedown', self._mouse_down);
      self.Update();
    }



};

var VirtualModel = function() {
    var self = this;

    $('#model_screen').position().top;
    // create svg drawing
    main_svg = SVG('model_screen').size(gridWidth + 60, gridHeight + 60);//$(window).height() / 2);


    self.orientation = 1;

    self.available_servos = ko.observableArray();
    for (let i = 0; i < 16; i++) {
      self.available_servos.push(i);
    }

    self.grid = main_svg.image('/static/images/robot/grids/A4_portrait.svg');
    self.grid.addClass('grid');
    self.grid.size(gridWidth, gridHeight);
    self.grid.move(30, 30);
    self.grid.draggable().on('dragmove', function(e) { e.preventDefault(); });
    self.grid.on('mousedown', function(){
      if (self.selected_module() != undefined) {
        self.selected_module().Deselect();
      }
    });

    self.modules = ko.observableArray();

    self.selected_module = ko.observable();

    self.init = function() {
      for (var i = 0; i < configs.length; i++) {
        let mod_type = configs[i].type;
        // console.log(mod_name);
        // let mod = new modules_definition[mod_type](svg_codes[mod_type], specs[mod_type], configs[i]);
        // self.modules.push(mod);
        self.Add_module(mod_type, configs[i]);
      }
    };

    self.Add_module = function(mod_type, config) {
      let mod = new modules_definition[mod_type](svg_codes[mod_type], specs[mod_type], config);
      self.modules.push(mod);
    };

    self.resize = function() {
      // Update grid x & y reference points
      var rect = $('svg').first().position();
      canvasX = rect.left;
      canvasY = rect.top;
    };
    self.resize();
}

var main_svg;
var virtualModel;

$(document).ready(function() {
    modules_definition = {
        'eye':      Eye,
        'turn':     Turn,
        'heart':    Heart,
        'speaker':  Speaker,
        'mouth':    Mouth,
    };

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
    virtualModel.modules()[virtualModel.modules().length-1].Set_pos(ev.pageX - canvasX, ev.pageY - canvasY);
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
