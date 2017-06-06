var Eye = function(svg_code, specs, config) {
    var self = this;
    self.base = Module;
    self.base(svg_code, specs, config);

    self.pupil = self.group.select('.pupil').first();
    self.lid_1 = self.group.select('.lid_1').first();
    self.lid_2 = self.group.select('.lid_2').first();

    self.update_dofs = function() {
      var midX    = 35;
      var midY    = 24;

      var dPupil  = 10;
      self.pupil.center(midX + dPupil * self.dofs[0].value, midY + dPupil * self.dofs[1].value);

      var lid1 = 4 + 10 * (1 - self.dofs[2].value);
      self.lid_1.array().value[2][2] = self.lid_1.array().value[2][4] = lid1;
      self.lid_1.plot(self.lid_1.array());
      self.lid_2.array().value[2][2] = self.lid_2.array().value[2][4] = midY*2 - lid1;
      self.lid_2.plot(self.lid_2.array());
    };

    self.set_dofs([0, 0, 0]);

    return self;
};
Eye.prototype = new Module;

modules_definition['eye'] = Eye;
