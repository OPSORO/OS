var Turn = function(svg_code, specs, config) {
    var self = this;
    self.base = Module;

    self.arm_offset         = 0;
    self.arm_range          = 45;
    self.arm_anchor_offset  = [0, 0];
    self.arm_width          = 32;
    self.arm_height         = 7;
    self.arm_image          = 'small_arm_2.svg';

    self.extra = main_svg.image('/static/images/robot/arms/' + self.arm_image);

    self.resize_extra = function() {
      self.extra.rotate(0, self.extra.cx() + self.arm_anchor_offset[0], self.extra.cy() + self.arm_anchor_offset[1]);
      self.extra.size(mm_to_screen(self.arm_width), mm_to_screen(self.arm_height));
      self.update_dofs();
    };
    self.resize_extra();

    self.base(svg_code, specs, config);


    self.update = function() {
      var maxSize = Math.max(self.width, self.height);
      self.object.size(maxSize, maxSize);
      self.object.center(self.x, self.y);
      self.group.rotate(self.rotation);

      self.extra.rotate(0, self.extra.cx() + self.arm_anchor_offset[0], self.extra.cy() + self.arm_anchor_offset[1]);

      var armX = self.x;
      var armY = self.y;
      if (self.rotation%180 == 0) {
        armX += ((self.rotation-90) / 90) * virtualModel.grid.space;
      } else if (self.rotation%180 == 90) {
        armY += ((self.rotation-180) / 90) * virtualModel.grid.space;
      }
      self.extra.center(armX, armY);
      self.update_dofs();
      self.extra.front();
    };

    self.update_dofs = function() {
      self.extra.rotate(self.rotation + self.arm_offset + (self.dofs[0].value * self.arm_range), self.extra.cx() + self.arm_anchor_offset[0], self.extra.cy() + self.arm_anchor_offset[1]);
    };

    self.set_dofs([0]);
    self.update();

    return self;
};
Turn.prototype = new Module;

modules_definition['turn'] = Turn;
