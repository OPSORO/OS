var Mouth = function(svg_code, specs, config) {
    var self = this;
    self.base = Module;
    self.base(svg_code, specs, config);

    self.lip_1 = self.group.select('.lip_1').first();

    self.update_dofs = function() {
      // Bezier mouth
      var midY = 9.5;
      self.lip_1.array().value[1][2] = midY + (20 * self.dofs[0].value);
      self.lip_1.array().value[1][4] = midY + (20 * -self.dofs[1].value);
      self.lip_1.plot(self.lip_1.array());
    };

    self.set_dofs([0, 0]);

    return self;
};
Mouth.prototype = new Module;

modules_definition['mouth'] = Mouth;
