var Turn = function(svg_code, specs, config) {
    var self = this;
    self.base = Module;
    self.base(svg_code, specs, config);

    self.arm_offset = ko.observable(0);
    self.arm_range = ko.observable(90);
    self.arm_anchor_offset = ko.observableArray();
    self.arm_anchor_offset.push(0);
    self.arm_anchor_offset.push(0);
    self.arm_width = ko.observable(32);
    self.arm_height = ko.observable(7);
    self.arm_image = ko.observable('small_arm_2.svg');

    self.arm = main_svg.image('/static/images/robot/arms/' + self.arm_image());
    // add drag events
    self.arm.style('cursor', 'grab');
    self.arm.draggable().on('dragmove', self._drag_move);
    self.arm.on('mousedown', self._mouse_down);
    self.arm.size(mm_to_screen(self.arm_width()), mm_to_screen(self.arm_height()));

    self.Update = function() {
      self.object.size(self.width(), self.height());
      self.object.center(self.x(), self.y());
      self.object.rotate(self.rotation(), self.x(), self.y());

      self.arm.rotate(0, self.x() + self.arm_anchor_offset()[0], self.y() + self.arm_anchor_offset()[1]);
      let armX = self.x();
      let armY = self.y();
      if (self.rotation()%180 == 0) {
        armX += ((self.rotation()-90) / 90) * gridSpace;
      } else if (self.rotation()%180 == 90) {
        armY += ((self.rotation()-180) / 90) * gridSpace;
      }
      self.arm.center(armX, armY);
      self.Update_dofs();
    };

    self.Update_dofs = function() {
      self.arm.rotate(self.rotation() + self.arm_offset() + self.dofs()[0].value() * self.arm_range(), self.x() + self.arm_anchor_offset()[0], self.y() + self.arm_anchor_offset()[1]);
    };
    self.Remove = function() {
      self.object.remove();
      self.arm.remove();
      virtualModel.modules.remove(self);
    };

    self.Set_dofs([1]);
    self.Update();

    return self;
};
Turn.prototype = new Module;
