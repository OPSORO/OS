

var select_dof = function(index) {
  var self = this;
  self.index = index || 0;
  self.name = ko.observable(virtualModel.selected_module.dofs[self.index].name);
  self.name_formatted = ko.observable(virtualModel.selected_module.dofs[self.index].name_formatted);

  self.pin_value = ko.observable(virtualModel.selected_module.dofs[self.index].servo.pin);
  self.pin = ko.pureComputed({
    read: function () {
      return self.pin_value();
    },
    write: function (value) {
      if (value == self.pin_value()) { return; }
      model.update_servo_pins(self.pin_value(), value);
      self.pin_value(value);
      virtualModel.selected_module.dofs[self.index].servo.pin = value;
      self._update_servo(self.mid_value());
    },
    owner: self
  });

  self.mid_value = ko.observable(virtualModel.selected_module.dofs[self.index].servo.mid);
  self.mid = ko.pureComputed({
    read: function () {
      return self.mid_value();
    },
    write: function (value) {
      if (value == self.mid_value()) { return; }
      self.mid_value(value);
      virtualModel.selected_module.dofs[self.index].servo.mid = value;
      self._update_servo(value);
    },
    owner: self
  });

  self.min_value = ko.observable(virtualModel.selected_module.dofs[self.index].servo.min);
  self.min = ko.pureComputed({
    read: function () {
      return self.min_value();
    },
    write: function (value) {
      if (value == self.min_value()) { return; }
      self.min_value(value);
      virtualModel.selected_module.dofs[self.index].servo.min = value;
      self._update_servo(value);
    },
    owner: self
  });

  self.max_value = ko.observable(virtualModel.selected_module.dofs[self.index].servo.max);
  self.max = ko.pureComputed({
    read: function () {
      return self.max_value();
    },
    write: function (value) {
      if (value == self.max_value()) { return; }
      self.max_value(value);
      virtualModel.selected_module.dofs[self.index].servo.max = value;
      self._update_servo(value);
    },
    owner: self
  });

  self._update_servo = function(value) {
    if (self.pin_value() < 0) { return; }
    if(connReady) {
      conn.send(JSON.stringify({
        action: "setServoPos",
        pin: self.pin_value(),
        value: value,
      }));
    }
  };
};

var select_module = function() {
  var self = this;
  self.name = new ClickToEdit(virtualModel.selected_module.name, 'Untitled');
  self.code = ko.observable(virtualModel.selected_module.code);
  self.dofs = ko.observableArray();

  self.rotate = function() {
    virtualModel.selected_module.rotate();
  };
  self.remove = function() {
    for (var i = 0; i < self.dofs().length; i++) {
      model.update_servo_pins(self.dofs()[i].pin_value(), -1);
    }
    virtualModel.selected_module.remove();
  };

  self.name_changed = ko.computed(function () {
    var value = self.name.value();
    virtualModel.selected_module.name = value;
    return value;
  }, self);

  self.refresh = function() {
    self.dofs.removeAll();

    if (virtualModel.selected_module == undefined) { return; }

    self.name.value(virtualModel.selected_module.name);
    for (var i = 0; i < virtualModel.selected_module.dofs.length; i++) {
      self.dofs.push(new select_dof(i));
    }
  };
  self.refresh();

};

var AppModel = function() {
  var self = this;
  // Setup link with virtual model
  self.selected_module = ko.observable();

  self.change_handler = function() {
    if (virtualModel.selected_module == undefined) {
      self.selected_module(undefined);
      return;
    }
    self.selected_module(new select_module());
    Foundation.reInit($('[data-slider]'));
  };
  virtualModel.change_handler = self.change_handler;

  self.available_servos = ko.observableArray();
  self.available_servos.push({ 'name': 'Not connected', 'pin': -1, 'class': '', 'disabled': false });
  for (var i = 0; i < 16; i++) {
    self.available_servos.push({ 'name': 'Pin ' + i, 'pin': i, 'class': 'pin' + i, 'disabled': false });
  }

  self.update_servo_pins = function(old_value, new_value) {
    if (new_value >= 0) {
      self.available_servos()[new_value + 1]['disabled'] = true;
      $('.' + self.available_servos()[new_value + 1]['class']).attr('disabled', '');
    }
    if (old_value >= 0) {
      self.available_servos()[old_value + 1]['disabled'] = false;
      $('.' + self.available_servos()[old_value + 1]['class']).removeAttr('disabled');
    }
  };

  self.fileIsModified = ko.observable(false);
  self.fileStatus = ko.observable('');
  self.fileExtension = '.conf';

  self.newFileData = function() {
    virtualModel.set_config({});
    self.fileIsModified(false);
  };

  self.loadFileData = function(data) {
    if (data == undefined) { return; }
    // Load script
    var dataobj = JSON.parse(data);
    virtualModel.set_config(dataobj);
    self.fileIsModified(false);
    return true;
  };

  self.saveFileData = function() {
    file_data = virtualModel.get_config();
    self.fileIsModified(false);
    return ko.toJSON(file_data, null, 2);
  };

  self.setDefault = function() {
    robotSendReceiveConfig(virtualModel.get_config());
  };

  self.init = function() {
    for (var i = 0; i < virtualModel.modules.length; i++) {
      var mod = virtualModel.modules[i];
      for (var j = 0; j < mod.dofs.length; j++) {
        var dof = mod.dofs[j];
        if (dof.servo.pin >= 0) {
          self.available_servos()[dof.servo.pin + 1].disabled = true;
        }
      }
    }
  };
};

var model;
$(document).ready(function() {
  model = new AppModel();
	ko.applyBindings(model);

  setTimeout(model.init, 500);

  config_file_operations("", model.fileExtension, model.saveFileData, model.loadFileData, model.newFileData);

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
  virtualModel.modules[virtualModel.modules.length-1].set_pos(ev.pageX - virtualModel.canvasX, ev.pageY - virtualModel.canvasY);
  virtualModel.modules[virtualModel.modules.length-1].update_grid_pos();
  virtualModel.modules[virtualModel.modules.length-1].select();
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
