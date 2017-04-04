var Speaker = function(svg_code, specs, config) {
    var self = this;
    self.base = Module;
    self.base(svg_code, specs, config);

    return self;
};
Speaker.prototype = new Module;

modules_definition['speaker'] = Speaker;
