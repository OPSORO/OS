


var select_dof = function(index) {
  var self = this;
  self.index = index || 0;
  self.name = ko.observable(virtualModel.selected_module.dofs[self.index].name);
  self.name_formatted = ko.observable(virtualModel.selected_module.dofs[self.index].name_formatted);

  self.pin = virtualModel.selected_module.dofs[self.index].servo.pin;

  self.value_value = ko.observable(virtualModel.selected_module.dofs[self.index].value);
  self.value = ko.pureComputed({
    read: function () {
      return self.value_value();
    },
    write: function (value) {
      if (value == self.value_value()) { return; }

      self.value_value(value);
      virtualModel.selected_module.dofs[self.index].value = parseFloat(value);

      virtualModel.selected_module.update_dofs();

      if (model.selected_expression().selected()) {
        if (self.pin >= 0) {
          model.selected_expression().dof_values[self.pin] = self.value_value();
        }
        if (model.selected_expression().poly_index() >= 0) {
          virtualModel.selected_module.dofs[self.index].update_single_poly(model.selected_expression().poly_index());
        }
        model.selected_expression().update();
      }
    },
    owner: self
  });
};

var Expression = function(name, filename, poly_index, dof_values) {
  var self = this;
  self.name       = new ClickToEdit(name, 'Untitled');
  self.default    = '2753';
  self.filename   = ko.observable(filename || self.default);
  self.poly_index = ko.observable(poly_index || -1);
  self.default_dofs = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ];
  self.dof_values = dof_values || self.default_dofs;
  self.selected   = ko.observable(false);

  if (self.poly_index() >= 0) {
    if (self.dof_values == self.default_dofs) {
      // Update dof values with module poly values
      for (var i = 0; i < virtualModel.modules.length; i++) {
        var mod = virtualModel.modules[i];
        for (var j = 0; j < mod.dofs.length; j++) {
          var dof = mod.dofs[j];
          if (dof.servo.pin >= 0) {
            self.dof_values[dof.servo.pin] = dof.poly[self.poly_index()];
          }
        }
      }
    } else {
      // Update module poly values with dof values
      for (var i = 0; i < virtualModel.modules.length; i++) {
        var mod = virtualModel.modules[i];
        for (var j = 0; j < mod.dofs.length; j++) {
          var dof = mod.dofs[j];
          if (dof.servo.pin >= 0) {
            dof.value = self.dof_values[dof.servo.pin];
            dof.update_single_poly(self.poly_index());
          }
        }
      }
    }

  }

  self.update = function() {
    if (!self.selected()) { return; }
    if(connReady) {
      conn.send(JSON.stringify({
        action: "setDofs",
        dofs: self.dof_values,
      }));
    }
  };

  self.get_config = function() {
    var config = {};
    config['name'] = self.name.value();
    config['filename'] = self.filename();
    config['dofs'] = self.dof_values;
    if (self.poly_index() >= 0) {
      config['poly'] = self.poly_index();
    }
    return config;
  };

  self.select = function() {
    if (self.selected()) { return; }
    for (var i = 0; i < model.expressions().length; i++) {
      model.expressions()[i].selected(false);
    }
    model.selected_expression(self);

    if (self.poly_index() < 0) {
      // Use dof values
      virtualModel.update_dofs(self.dof_values);
    } else {
      // Use dof poly
      virtualModel.apply_poly(self.poly_index());
    }
    self.selected(true);
    self.update();
  };
  self.update_icon = function(icon) {
    self.filename(icon);
    $("#PickIconModal").foundation("close");
  };
  self.change_icon = function() {
    // Reset icons
    for (var i = 0; i < model.used_icons.length; i++) {
      if (model.used_icons[i] == self.default) {
        continue;
      }
      model.icons.push(model.used_icons[i]);
    }
    model.used_icons = []
    for (var i = 0; i < model.expressions().length; i++) {
      model.icons.remove(model.expressions()[i].filename());
      model.used_icons.push(model.expressions()[i].filename());
    }
    model.icons.sort();
    // View icons
    $("#PickIconModal").foundation("open");
  };
  self.remove = function() {
    model.expressions.remove(self);
    if (model.expressions().length > 0) {
      model.expressions()[0].select();
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

  self.icons = ko.observableArray(icon_data);
  self.used_icons = [];

  self.expressions = ko.observableArray();
  self.selected_expression = ko.observable();
  self.add_expression = function(name, filename, poly_index, dof_values) {
    if (typeof name == 'object') {
      name = 'custom';
      filename = '';
    }
    name      = name || '';
    var exp = new Expression(name, filename, poly_index, dof_values);
    self.expressions.push(exp);
    if (filename == '') {
      exp.change_icon();
      self.expressions()[self.expressions().length-1].select();
    }
  };
  self.get_config = function() {
    var config = [];
    if (self.expressions() == undefined) { return config; }

    for (var i = 0; i < self.expressions().length; i++) {
      config.push(self.expressions()[i].get_config());
    }
    return config;
  };
  self.set_config = function(config) {
    self.expressions.removeAll();
    if (config != undefined && config.length > 0) {
      for (var i = 0; i < config.length; i++) {
        var dat = config[i];
        self.add_expression(dat.name, dat.filename, dat.poly, dat.dofs);
      }
    } else {
      self.add_expression('', '1f610');
    }
    self.expressions()[0].selected(true);
    self.selected_expression(self.expressions()[0]);
  };

  self.update_icon = function(icon) {
    if (self.selected_expression != undefined) {
      self.selected_expression().update_icon(icon);
    }
  };

  self.fileIsModified = ko.observable(false);
  self.fileStatus = ko.observable('');
  self.fileExtension = '.conf';

  self.newFileData = function() {
    self.set_config([]);
    self.fileIsModified(false);
  };
  self.loadFileData = function(data) {
    var dataobj = undefined;
    if (data == undefined) {
    } else {
      dataobj = JSON.parse(data);
    }
    // Load script
    self.set_config(dataobj);
    self.fileIsModified(false);
    return true;
  };
  self.saveFileData = function() {
    file_data = self.get_config();
    self.fileIsModified(false);
    return ko.toJSON(file_data, null, 2);
  };
  self.setDefault = function() {
    robotSendReceiveExpressions(self.get_config());
    robotSendReceiveConfig(virtualModel.get_config());
  };

  self.init = function() {
    if (self.expressions() == undefined || self.expressions().length < 2) {
      if (self.expressions()[0].name.value() == '') {
        self.set_config(expression_data);
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

});
