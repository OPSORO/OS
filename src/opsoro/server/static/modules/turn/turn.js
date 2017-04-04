var Turn = function(svg_code, specs, config) {
    var self = this;
    self.base = Module;

    self.arm_offset = ko.observable(0);
    self.arm_range = ko.observable(90);
    self.arm_anchor_offset = ko.observableArray();
    self.arm_anchor_offset.push(0);
    self.arm_anchor_offset.push(0);
    self.arm_width = ko.observable(32);
    self.arm_height = ko.observable(7);
    self.arm_image = ko.observable('small_arm_2.svg');

    self.extra = main_svg.image('/static/images/robot/arms/' + self.arm_image());

    self.base(svg_code, specs, config);

    self.extra.size(mm_to_screen(self.arm_width()), mm_to_screen(self.arm_height()));
    self.extra.front();

    self.Update = function() {
      // self.extra.rotate(0, self.x() + self.arm_anchor_offset()[0], self.y() + self.arm_anchor_offset()[1]);
      self.object.size(self.width(), self.height());
      self.object.center(self.x(), self.y());
      self.object.rotate(self.rotation(), self.x(), self.y());

      self.extra.rotate(0, self.extra.cx() + self.arm_anchor_offset()[0], self.extra.cy() + self.arm_anchor_offset()[1]);
      // self.arm.rotate(0, self.x(), self.y());
      let armX = self.x();
      let armY = self.y();
      if (self.rotation()%180 == 0) {
        armX += ((self.rotation()-90) / 90) * virtualModel.grid.space;
      } else if (self.rotation()%180 == 90) {
        armY += ((self.rotation()-180) / 90) * virtualModel.grid.space;
      }
      self.extra.center(armX, armY);
      self.Update_dofs();
    };

    self.Update_dofs = function() {
      self.extra.rotate(self.rotation() + self.arm_offset() + (self.dofs()[0].value() * self.arm_range()), self.extra.cx() + self.arm_anchor_offset()[0], self.extra.cy() + self.arm_anchor_offset()[1]);
      // self.extra.rotate(self.rotation()%180 + self.arm_offset() + (self.dofs()[0].value() * self.arm_range()), self.x(), self.y());
    };

    self.Set_dofs([0]);
    self.Update();

    return self;
};
Turn.prototype = new Module;

modules_definition['turn'] = Turn;
