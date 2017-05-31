var Heart = function(svg_code, specs, config) {
    var self = this;
    self.base = Module;
    self.base(svg_code, specs, config);

    return self;
};
Heart.prototype = new Module;

modules_definition['heart'] = Heart;
