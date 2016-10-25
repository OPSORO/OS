var virtualModel;
var modules_name;
var skins_name;
var action_data;
var config_data;
var dof_values;

// $(document).ready(function() {
var module_function = {
    'eye': DrawEye,
    'eyebrow': DrawEyebrow,
    'mouth': DrawMouth
};

function constrain(val, min, max) {
    return Math.min(max, Math.max(val, min));
}

var Mapping = function(neutral) {
    var self = this;
    self.neutral = ko.observable(neutral);
    self.poly = ko.observableArray();

    // Populate Poly
    for (var i = 0; i < 20; i++) {
        self.poly.push(0.0);
    }

    self.setPolyPos = function(index, position) {
        self.poly()[index] = position;
    };
};
var MappingGraph = function() {
    var self = this;

    if ($('#poly_screen').length == 0) {
        return;
    }

    self.svg = SVG('poly_screen').size('100%', '121');

    self.width = $('#poly_screen svg').width();
    self.height = self.svg.height();
    self.points = ko.observableArray();

    // var rect = self.svg.rect(self.width, self.height);
    // rect.fill("#AAA");

    self.centerY = self.height / 2;
    self.nodeSize = self.width / 30;

    self.stepWidth = self.width / 21;
    self.startX = self.nodeSize;

    self.updateGraph = function() {
        if (virtualModel == undefined) {
            return;
        }
        for (var i = 0; i < self.points().length; i++) {
            self.points()[i].cy(self.centerY - virtualModel.selectedModule_SelectedDof().map().poly()[i] * (self.centerY - self.nodeSize));
        }
    };

    var startX,
        text,
        line;
    startX = 5;
    var texts = ['1', '0', '-1'];
    var Ys = [
        self.nodeSize, self.centerY, self.height - self.nodeSize
    ];
    line = self.svg.line(startX * 2, Ys[0], startX * 2, Ys[2]).stroke({
        width: 0.5
    });
    line = self.svg.line(self.width - 1, Ys[0], self.width - 1, Ys[2]).stroke({
        width: 0.5
    });

    for (var i = Ys[0]; i < Ys[2]; i += self.height / 40) {
        self.svg.line(startX * 2, i, self.width - 1, i).stroke({
            width: 0.2
        });
    }
    for (var i = 0; i < texts.length; i++) {
        text = self.svg.plain(texts[i]);
        text.center(startX, Ys[i]);
        line = self.svg.line(startX * 2, Ys[i], self.width - 1, Ys[i]).stroke({
            width: 0.5
        });
    }
    var updateInfoTxt = function(circ) {
        self.infoRect.show();
        self.infoTxt.show();
        var num = (self.centerY - circ.cy()) / (self.centerY - self.nodeSize);
        num = Math.round(num * 20) / 20; // Round to 0.05
        self.infoTxt.plain(num);
        if (circ.cx() > self.infoRect.width() * 2) {
            self.info.move(circ.cx() - self.infoRect.width() - self.nodeSize * 3 / 2, circ.cy() + self.infoRect.height() / 2 - 1)
        } else {
            self.info.move(circ.cx() + self.nodeSize * 3 / 2, circ.cy() + self.infoRect.height() / 2 - 1)
        }
        return num;
    };
    var hideInfoTxt = function() {
        self.infoRect.hide();
        self.infoTxt.hide();
    };
    for (var i = 0; i < 20; i++) {
        line = self.svg.line(self.startX * 2 + self.stepWidth * i, Ys[0], self.startX * 2 + self.stepWidth * i, Ys[2]).stroke({
            width: 0.2
        });
        var circle = self.svg.circle(self.nodeSize);
        circle.fill('#286')
        circle.center(self.startX * 2 + self.stepWidth * i, self.centerY);
        circle.draggable(function(x, y) {
            return {
                x: x == self.startX * 2 + self.stepWidth * i,
                y: y > self.nodeSize / 2 - 1 && y < (self.height - self.nodeSize * 3 / 2)
            }
        });
        circle.attr({
            index: i
        });
        circle.on('mouseover', function() {
            updateInfoTxt(this);
        });
        circle.on('mouseleave', function() {
            hideInfoTxt();
        });
        circle.on('dragmove', function() {
            var num = updateInfoTxt(this);
            virtualModel.selectedModule_SelectedDof().map().poly()[this.attr('index')] = num;
            virtualModel.updateDofVisualisation(this.attr('index'), false);
        });
        circle.on('dragend', function(e) {
            var num = updateInfoTxt(this);
            this.cy(self.centerY - num * (self.centerY - self.nodeSize));
            virtualModel.selectedModule_SelectedDof().map().poly()[this.attr('index')] = num;
            virtualModel.updateDofVisualisation(this.attr('index'), true);
        });
        self.points.push(circle);
    }
    self.info = self.svg.nested();
    self.infoRect = self.info.rect(30, 12);
    self.infoRect.move(-2, -10);
    self.infoRect.fill('#fff');
    self.infoRect.stroke({
        color: '#222',
        opacity: 0.8,
        width: 1
    });
    self.infoTxt = self.info.plain('');
    self.infoTxt.move(0, 0);
    self.infoTxt.fill('#000');
    hideInfoTxt();

};
var Servo = function(pin, mid, min, max) {
    var self = this;
    self.pin = ko.observable(pin);
    self.mid = ko.observable(mid);
    self.min = ko.observable(min);
    self.max = ko.observable(max);
};
var Dof = function(name) {
    var self = this;
    self.name = ko.observable(name);
    self.isServo = ko.observable(false);
    self.servo = ko.observable(new Servo(0, 1500, 0, 0));
    self.isMap = ko.observable(false);
    self.map = ko.observable(new Mapping(0));
    self.value = ko.observable(0.0);

    self.setServo = function(pin, mid, min, max) {
        self.servo(new Servo(pin, mid, min, max));
        self.isServo(true);
    };
    self.setMap = function(neutral) {
        self.map(new Mapping(neutral));
        self.isMap(true);
    };
};
var Module = function(type, name, x, y, width, height, rotation) {
    var self = this;
    self.module = ko.observable(type);
    self.name = ko.observable(name);
    self.x = ko.observable(x);
    self.y = ko.observable(y);
    self.width = ko.observable(width);
    self.height = ko.observable(height);
    self.rotation = ko.observable(Math.round(rotation / 90) * 90); // 90° angles only
    self.dofs = ko.observableArray();
    self.image = undefined;
    self.drawObject = undefined;

    self.snapToGrid = function() {
        var newX,
            newY;
        newX = Math.round(self.image.cx() / (virtualModel.snap() * virtualModel.screenGridSize)) * (virtualModel.snap() * virtualModel.screenGridSize);
        newY = Math.round(self.image.cy() / (virtualModel.snap() * virtualModel.screenGridSize)) * (virtualModel.snap() * virtualModel.screenGridSize);
        self.image.center(newX, newY);
    };

    self.draw = function() {
        self.update(self.x(), self.y(), self.width(), self.height(), self.rotation());
        self.drawObject = new module_function[self.module()](virtualModel.svg, self.x(), self.y(), self.width(), self.height());
        self.image = self.drawObject.image;

        self.updateImage();
    };

    self.updateDofVisualisation = function(mapIndex, updateRobot) {
        if (self.drawObject == undefined) {
            return;
        }
        if (updateRobot == undefined) {
          updateRobot = false;
        }
        var values = [];

        $.each(self.dofs(), function(idx, dof) {
            dof.value(0);
            if (dof_values != undefined) {
                if (dof.isServo()) {
                    dof.value(dof_values[dof.servo().pin()]);
                }
            } else {
                if (dof.isMap() && dof.isServo()) {
                    if (mapIndex < 0) {
                        dof.value(dof.map().neutral());
                    } else {
                        dof.value(dof.map().poly()[mapIndex]);
                    }
                }
            }
            if (updateRobot) {
              virtualModel.updateDof(dof);
            }
            values.push(parseFloat(dof.value()));
        });
        if (values.length == self.drawObject.dofs.length) {
            self.drawObject.x = self.x();
            self.drawObject.y = self.y();
            self.drawObject.width = self.width();
            self.drawObject.height = self.height();
            self.drawObject.Set(values)
            self.drawObject.Update();
        }
        if (mapIndex < 0) {
            self.snapToGrid();
        }
    };

    self.update = function(x, y, w, h, r) {
        r = Math.round(r / 90) * 90;
        self.rotation(r);
        self.x(Math.ceil(virtualModel.centerX + x * virtualModel.refSize));
        self.y(Math.ceil(virtualModel.centerY + y * virtualModel.refSize));
        self.width(Math.ceil(w * virtualModel.refSize));
        self.height(Math.ceil(h * virtualModel.refSize));
    };
    self.updateImage = function() {
        if (!virtualModel.editable) {
            return;
        }
        if (self.image == undefined) {
            return;
        }
        self.image.attr({
            preserveAspectRatio: "none"
        });

        self.image.style('cursor', 'grab');
        self.image.draggable();
        self.snapToGrid();
        self.image.on('mousedown', function() {
            virtualModel.resetSelect();
            // this.selectize();
            this.opacity(1);
            virtualModel.setSelectedModule(self);
        });
        self.image.on('dragend', function(e) {
            self.snapToGrid();
            self.x(this.cx());
            self.y(this.cy());
            self.drawObject.x = self.x();
            self.drawObject.y = self.y();
            self.drawObject.width = self.width();
            self.drawObject.height = self.height();
        });
    };
};

function DrawModule(svg, x, y, width, height) {
    var self = this;
    self.svg = svg || undefined;
    self.x = x || 0;
    self.y = y || 0
    self.width = width || 0;
    self.height = height || 0;
    self.dofs = [];
}

// ----------------------------------------------------------------------------------------------------
// Mouth
// ----------------------------------------------------------------------------------------------------
function DrawMouth(svg, x, y, width, height) {
    var self = this;
    self.base = DrawModule;
    self.base(svg, x, y, width, height);

    self.dofs = ['left_vertical', 'middle_vertical', 'right_vertical', 'left_rotation', 'right_rotation'];

    self.increase = self.height / 2;

    self.Set = function(values) {
        self.right_Y = constrain(values[0] || 0, -1, 1); // -1.0 -> 1.0
        self.middle_Y = constrain(values[1] || 0, -1, 1); // -1.0 -> 1.0
        self.left_Y = constrain(values[2] || 0, -1, 1); // -1.0 -> 1.0
        self.right_R = constrain(values[3] || 0, -1, 1); // -1.0 -> 1.0
        self.left_R = constrain(values[4] || 0, -1, 1); // -1.0 -> 1.0
    }
    self.Set([-0.5, 0.5, -0.5, 0, 0]);

    if (self.svg == undefined) {
        return;
    }

    self.curve = new SVG.PathArray([
        ['M', 0, 0]
    ]);
    self.image = self.svg.nested();
    self.image.attr({
        x: self.x - self.width / 2,
        y: self.y - self.height / 2,
        width: self.width,
        height: self.height
    });
    self.image_mouth = self.image.path(self.curve);

    self.Update = function() {
        var leftX,
            rightX,
            topY,
            middleY1,
            middleY2,
            centerY;

        leftX = 0;
        rightX = self.width;
        middleY1 = self.left_R * 90;
        middleY2 = self.right_R * 90;

        centerY = self.height / 2;

        self.increase = self.height / 2;

        self.curve = new SVG.PathArray([
            [
                'M', leftX, centerY + (self.left_Y * self.increase)
            ],
            [
                'C', leftX + self.width / 4,
                centerY + middleY1,
                rightX - self.width / 4,
                centerY + middleY2,
                rightX,
                centerY + (self.right_Y * self.increase)
            ],
            [
                'C', rightX - self.width / 4,
                centerY + (self.middle_Y * self.increase / 2) + middleY2 + self.increase / 2,
                leftX + self.width / 4,
                centerY + (self.middle_Y * self.increase / 2) + middleY1 + self.increase / 2,
                leftX,
                centerY + (self.left_Y * self.increase)
            ],
            ['z']
        ]);

        self.image_mouth.plot(self.curve);
        // // Round bezier corners
        var endsize = 1;
        var marker = self.svg.marker(endsize, endsize, function(add) {
            add.circle(endsize).fill('#C00');
        })
        self.image_mouth.marker('start', marker);
        self.image_mouth.marker('mid', marker);
        self.image_mouth.fill('#222').stroke({
            width: Math.min(self.width, self.height) / 8,
            color: '#C00'
        });


        self.image.attr({
            x: self.x - self.width / 2,
            y: self.y - self.height / 2,
            width: self.width,
            height: self.height
        });
    };
    self.Update();
}
DrawMouth.prototype = new DrawModule;

// ----------------------------------------------------------------------------------------------------
// Eyebrow
// ----------------------------------------------------------------------------------------------------
function DrawEyebrow(svg, x, y, width, height) {
    var self = this;
    self.base = DrawModule;
    self.base(svg, x, y, width, height);

    self.dofs = ['Left Vertical', 'Right Vertical', 'Rotation'];
    self.increase = self.height / 2;

    self.Set = function(values) {
        self.right_Y = constrain(values[0] || 0, -1, 1); // -1.0 -> 1.0
        self.left_Y = constrain(values[1] || 0, -1, 1); // -1.0 -> 1.0
        self.rotation = constrain(values[2] || 0, -1, 1); // -1.0 -> 1.0
    }
    self.Set([0, 0, 0]);

    if (self.svg == undefined) {
        return;
    }

    self.curve = new SVG.PathArray([
        ['M', 0, 0]
    ]);
    self.image = self.svg.nested();
    self.image.attr({
        x: self.x - self.width / 2,
        y: self.y - self.height / 2,
        width: self.width,
        height: self.height
    });
    self.image_eyebrow = self.image.path(self.curve);

    self.Update = function() {
        var leftX,
            rightX,
            centerY;
        leftX = 0;
        rightX = self.width;
        self.increase = self.height / 2;
        centerY = self.height / 2;
        self.curve = new SVG.PathArray([
            [
                'M', leftX, centerY + (self.left_Y * self.increase)
            ],
            [
                'C', leftX + self.width / 4,
                centerY + (self.left_Y * self.increase) - self.increase / 2,
                rightX - self.width / 4,
                centerY + (self.right_Y * self.increase) - self.increase / 2,
                rightX,
                centerY + (self.right_Y * self.increase)
            ]
        ]);

        self.image_eyebrow.plot(self.curve);
        // Round bezier corners
        var endsize = 1;
        var marker = self.svg.marker(endsize, endsize, function(add) {
            add.circle(endsize).fill('#222');
        })
        self.image_eyebrow.marker('start', marker);
        self.image_eyebrow.marker('end', marker);
        self.image_eyebrow.fill('none').stroke({
            width: Math.min(self.width, self.height) / 6,
            color: '#222'
        });

        self.image_eyebrow.rotate(self.rotation * 45);

        self.image.attr({
            x: self.x - self.width / 2,
            y: self.y - self.height / 2,
            width: self.width,
            height: self.height
        });
    };
    self.Update();
}
DrawEyebrow.prototype = new DrawModule;

// ----------------------------------------------------------------------------------------------------
// Eye
// ----------------------------------------------------------------------------------------------------
function DrawEye(svg, x, y, width, height) {
    var self = this;
    self.base = DrawModule;
    self.base(svg, x, y, width, height);

    self.dofs = ['Pupil Horizontal', 'Pupil Vertical', 'Eyelid Closure'];

    self.Set = function(values) {
        self.pupil_X = constrain(values[0] || 0, -1, 1); // -1.0 -> 1.0
        self.pupil_Y = constrain(values[1] || 0, -1, 1); // -1.0 -> 1.0
        self.lid = constrain(-values[2] || 0, -1, 1); // -1.0 -> 1.0
    }
    self.Set([0, 0, 0.5]);

    if (self.svg == undefined) {
        return;
    }

    self.curve = new SVG.PathArray([
        ['M', 0, 0]
    ]);
    self.image = self.svg.nested();
    self.image.attr({
        x: self.x - self.width / 2,
        y: self.y - self.height / 2,
        width: self.width,
        height: self.height
    });

    self.image_eye = self.image.ellipse(self.width, self.height);
    self.image_eye.fill('#DDD');

    self.image_pupil = self.image.ellipse(self.width / 5, self.height / 5); //((parseInt(self.width) + parseInt(self.height)) / 5);
    self.image_pupil.center(self.width / 2, self.height / 2);
    self.image_pupil.fill('#000');

    self.image_lid = self.image.path(self.curve);

    self.Update = function() {
        var leftX,
            rightX,
            topY,
            pupil_factor;
        leftX = 0;
        rightX = self.width;
        topY = 0;
        pupil_factor = 2.5;

        self.image_eye.size(self.width, self.height);
        self.image_eye.center(self.width / 2, self.height / 2);
        self.image_pupil.size(self.width / pupil_factor, self.height / pupil_factor);
        self.image_pupil.center(self.width / 2 - self.pupil_X * (self.width / 2 - self.image_pupil.width() / 1.4), self.height / 2 - self.pupil_Y * (self.height / 2 - self.image_pupil.height() / 1.4));

        self.curve = new SVG.PathArray([
            [
                'M', leftX, self.height / 2
            ],
            [
                'C', leftX, -self.height / 4,
                rightX, -self.height / 4,
                rightX,
                self.height / 2
            ],
            [
                'C', rightX, self.height / 2 + self.lid * self.height * 5 / 8,
                leftX,
                self.height / 2 + self.lid * self.height * 5 / 8,
                leftX,
                self.height / 2
            ],
            ['z']
        ]);

        self.image_lid.plot(self.curve);

        // Round bezier corners
        // var endsize = 1;
        // var marker = self.svg.marker(endsize, endsize, function(add) {
        //     add.circle(endsize).fill('#999');
        // })
        // self.image_lid.marker('start', marker);
        // self.image_lid.marker('mid', marker);
        self.image_lid.fill('#444'); //.stroke({ width: 1, color: '#999' });


        self.image.attr({
            x: self.x - self.width / 2,
            y: self.y - self.height / 2,
            width: self.width,
            height: self.height
        });
        // self.image.size(self.width, self.height);
        // self.image.move(self.x, self.y);
    };
    self.Update();
}
DrawEyebrow.prototype = new DrawModule;

var VirtualModel = function() {
    var self = this;

    // File operations toolbar item
    self.fileIsLocked = ko.observable(false);
    self.fileIsModified = ko.observable(false);
    self.fileName = ko.observable("Untitled");
    self.fileStatus = ko.observable("");
    self.fileExtension = ko.observable(".conf");

    self.config = (config_data == undefined ?
        undefined :
        config_data); //JSON.parse(config_data));
    self.allModules = ['eye', 'eyebrow', 'mouth']; //modules_name;
    self.allSkins = ['ono', 'nmct', 'robo']; //skins_name;
    self.skin = ko.observable((self.allSkins == undefined ?
        'ono' :
        self.allSkins[0]));
    self.name = ko.observable("OPSORO robot");

    self.isSelectedModule = ko.observable(false);
    self.selectedModule = ko.observable();
    self.selectedModule_SelectedDof = ko.observable();

    self.modules = ko.observableArray();

    // create svg drawing
    self.svg = SVG('model_screen').size('100%', '600');

    self.modelwidth = $('#model_screen svg').width();
    self.modelheight = self.svg.height();
    self.refSize = Math.max(self.modelwidth, self.modelheight) / 2;

    self.gridSize = ko.observable(18);
    self.screenGridSize = Math.min(self.modelwidth, self.modelheight) / self.gridSize();
    self.snap = ko.observable(1);

    self.centerX = self.modelwidth / 2;
    self.centerY = self.modelheight / 2;

    self.skin_image = undefined;
    self.newConfig = true;

    self.editable = ($('#poly_screen').length != 0);

    self.mappingGraph = new MappingGraph();

    self.updateServoPin = function() {

    }
    self.updateServoMid = function() {
        if (!self.selectedModule_SelectedDof().isServo()) {
            return;
        }
        console.log(parseInt(self.selectedModule_SelectedDof().servo().mid()));
        robotSendServo(self.selectedModule_SelectedDof().servo().pin(), parseInt(self.selectedModule_SelectedDof().servo().mid()));
    }
    self.updateServoMin = function() {
        if (!self.selectedModule_SelectedDof().isServo()) {
            return;
        }
        console.log(parseInt(self.selectedModule_SelectedDof().servo().mid()) + parseInt(self.selectedModule_SelectedDof().servo().min()));
        robotSendServo(self.selectedModule_SelectedDof().servo().pin(), parseInt(self.selectedModule_SelectedDof().servo().mid()) + parseInt(self.selectedModule_SelectedDof().servo().min()));
    }
    self.updateServoMax = function() {
        if (!self.selectedModule_SelectedDof().isServo()) {
            return;
        }
        console.log(parseInt(self.selectedModule_SelectedDof().servo().mid()) + parseInt(self.selectedModule_SelectedDof().servo().max()));
        robotSendServo(self.selectedModule_SelectedDof().servo().pin(), parseInt(self.selectedModule_SelectedDof().servo().mid()) + parseInt(self.selectedModule_SelectedDof().servo().max()));
    }
    self.updateDofs = function() {
        if (!self.selectedModule_SelectedDof().isServo()) {
            return;
        }

        var dof_values = {};

        for (var i = 0; i < self.modules().length; i++) {
            var singleModule = self.modules()[i];
            dof_values[singleModule.name()] = {};
            for (var j = 0; j < singleModule.dofs().length; j++) {
                var singleDof = singleModule.dofs()[j];
                dof_values[singleModule.name()][singleDof.name()] = singleDof.value();

                var value = parseInt(singleDof.servo().mid());
                if (singleDof.value() >= 0) {
                    value += parseInt(singleDof.value() * singleDof.servo().max());
                } else {
                    value += parseInt(-singleDof.value() * singleDof.servo().min());
                }

                robotSendServo(singleDof.servo().pin(), value);
            }
            console.log(dof_values[singleModule.name()]);
            // mod_values[singleModule.name()].push(dof_values);

        }
        // console.log(dof_values[]);
        // robotSendReceiveAllDOF(dof_values);
    }

    self.updateDof = function(singleDof) {
        if (singleDof == undefined) {
            return;
        }
        if (!singleDof.isServo()) {
            return;
        }

        if (singleDof.value() > 1.0) {
          singleDof.value(1.0);
        }
        if (singleDof.value() < -1.0) {
          singleDof.value(-1.0);
        }


        var value = parseInt(singleDof.servo().mid());
        if (singleDof.value() >= 0) {
            value += parseInt(singleDof.value() * singleDof.servo().max());
        } else {
            value += parseInt(-singleDof.value() * singleDof.servo().min());
        }

        robotSendServo(singleDof.servo().pin(), value);
    }

    self.clearDraw = function() {
        console.log('Clear');
        self.svg.clear();
        self.modelwidth = $('#model_screen svg').width();
        self.modelheight = self.svg.height();
        self.refSize = Math.max(self.modelwidth, self.modelheight) / 2;
        self.screenGridSize = Math.min(self.modelwidth, self.modelheight) / self.gridSize();
        self.centerX = self.modelwidth / 2;
        self.centerY = self.modelheight / 2;


        self.resetSelect();
        if (self.config != undefined) {
            if (self.config.grid != undefined) {
                self.gridSize(self.config.grid);
            }
        }
        self.screenGridSize = Math.min(self.modelwidth, self.modelheight) / self.gridSize();
        if (!self.editable) {
            return;
        }
        var pattern = self.svg.pattern(self.screenGridSize, self.screenGridSize, function(add) {
            // add.rect(self.screenGridSize, self.screenGridSize).fill('#eee');
            // add.rect(10,10);
            var size = self.screenGridSize * 3 / 16;
            add.rect(size, size).fill('#444');
            add.rect(size, size).move(self.screenGridSize - size, 0).fill('#444');
            add.rect(size, size).move(0, self.screenGridSize - size).fill('#444');
            add.rect(size, size).move(self.screenGridSize - size, self.screenGridSize - size).fill('#444');
        })
        self.grid = self.svg.rect(self.modelwidth, self.modelheight).attr({
            fill: pattern
        });
    };
    self.setSelectedModule = function(module) {
        self.selectedModule(module);
        self.selectedModule_SelectedDof(self.selectedModule().dofs()[0]);
        if (!self.editable) {
            return;
        }
        self.fileIsModified(true);
        self.isSelectedModule(true);
        self.mappingGraph.updateGraph();
        self.updateServoMid();
    };
    self.selectedModule_RotateLeft = function() {
        self.selectedModule().rotation((self.selectedModule().rotation() - 90) % 360);
        self.selectedModule().image.rotate(self.selectedModule().rotation());
    };
    self.selectedModule_RotateRight = function() {
        self.selectedModule().rotation((self.selectedModule().rotation() + 90) % 360);
        self.selectedModule().image.rotate(self.selectedModule().rotation());
    };
    self.selectedModule_AddDof = function() {
        var newDof = new Dof("New dof");
        self.selectedModule().dofs.push(newDof);
        self.selectedModule_SelectedDof(newDof);
    };
    self.selectedModule_Remove = function() {
        self.resetSelect();
        self.selectedModule().image.remove();
        self.modules.remove(self.selectedModule());
    };
    self.selectedModule_RemoveDof = function() {
        self.selectedModule().dofs.remove(self.selectedModule_SelectedDof());
        if (self.selectedModule().dofs().length == 0) {
            self.selectedModule_AddDof();
        }
        self.selectedModule_SelectedDof(self.selectedModule().dofs()[0]);
    };

    self.saveConfig = function() {
        console.log('Save');
        if (!self.editable) {
            return;
        }
        var svg_data = {};
        svg_data['name'] = self.name();
        svg_data['skin'] = self.skin();
        svg_data['grid'] = self.gridSize();

        svg_data['modules'] = [];

        for (var i = 0; i < self.modules().length; i++) {
            var singleModule = self.modules()[i];
            var module_data = {};
            module_data['module'] = singleModule.module();
            module_data['name'] = singleModule.name();
            var matrix = new SVG.Matrix(singleModule.image);
            module_data['canvas'] = {
                x: (singleModule.image.cx() - self.centerX) / self.refSize,
                y: (singleModule.image.cy() - self.centerY) / self.refSize,
                width: singleModule.width() / self.refSize,
                height: singleModule.height() / self.refSize,
                rotation: matrix.extract().rotation
            };
            if (singleModule.dofs() != undefined) {
                module_data['dofs'] = [];
                for (var j = 0; j < singleModule.dofs().length; j++) {
                    var singleDof = singleModule.dofs()[j];
                    var dof_data = {};

                    dof_data['name'] = singleDof.name();
                    if (singleDof.isServo()) {
                        dof_data['servo'] = singleDof.servo();
                    }
                    if (singleDof.isMap()) {
                        dof_data['mapping'] = singleDof.map();
                    }
                    module_data['dofs'].push(dof_data);
                }
            }
            svg_data['modules'].push(module_data);
        }
        return svg_data;
    };

    self.init = function() {
        self.config = undefined;
        self.newConfig = true;
        self.redraw();
    };

    self.loadFileData = function(data) {
        if (data == undefined) {
            return;
        }
        // Load data
        var dataobj = JSON.parse(data);
        console.log(dataobj);
        // Do something with the data
        self.newConfig = true;
        self.config = dataobj;
        self.redraw();
        self.fileIsModified(false);
    };

    self.saveFileData = function() {
        if (!self.editable) {
            return;
        }
        return ko.toJSON(self.saveConfig(), null, 2);
    };

    self.setDefault = function() {
        if (!self.editable) {
            return;
        }
        // Convert data
        // file_data = self.saveConfig();
        // var data = ko.toJSON(file_data, null, 2);

        // Send data
        robotSendReceiveConfig(self.saveConfig());
    };

    //-------------------------------------------------------------------------------
    // SVG stuff
    //-------------------------------------------------------------------------------

    // 	var axisY = self.svg.line(0, centerY, self.modelwidth/2, centerY).stroke({ width: 1 });
    // var axisX = self.svg.line(centerX, 0, centerX, self.modelheight).stroke({ width: 1 });
    // var Seperator = self.svg.line(self.modelwidth/2, 0, self.modelwidth/2, self.modelheight).stroke({ width: 3 });

    // Draw skin & modules
    self.redraw = function() {
        console.log('Redraw');
        if (!self.newConfig && self.fileIsModified()) {
            // Convert and convert back, bad reading otherwise
            self.config = JSON.parse(ko.toJSON(self.saveConfig()));
            //alert('not good');
        } else {
            self.newConfig = true;
        }
        self.clearDraw();
        if (self.config != undefined) {
            self.skin_image = self.svg.image('/static/images/skins/' + self.config.skin + '.svg').loaded(self.drawModules);
        } else {
            self.skin_image = self.svg.image('/static/images/skins/' + self.skin() + '.svg').loaded(self.drawModules);
        }

        self.fileIsModified(false);
    };

    var previousMapIndex = -1;
    self.updateDofVisualisation = function(mapIndex, updateRobot) {
        // alert('');
        if (mapIndex < -1 || previousMapIndex != mapIndex) {
            // Update all modules (when selecting new emotion for mapping)
            $.each(self.modules(), function(idx, mod) {
                mod.updateDofVisualisation(mapIndex, updateRobot);
            });
        } else {
            // Update single module (when changing mapping)
            self.selectedModule().updateDofVisualisation(mapIndex, updateRobot);
        }
        previousMapIndex = mapIndex;
        // self.updateDofs();
    };

    self.drawModules = function() {
        $("image, svg").mousedown(function() {
            virtualModel.resetSelect();
            // virtualModel.updateDofVisualisation(-1);
            return false;
        });

        var dx = self.modelwidth / self.skin_image.width();
        var dy = self.modelheight / self.skin_image.height();

        var modelWidth,
            modelHeight;

        if (dx < dy) {
            modelWidth = self.modelwidth;
            modelHeight = self.skin_image.height() * dx;
        } else {
            modelWidth = self.skin_image.width() * dy;
            modelHeight = self.modelheight;
        }

        self.skin_image.size(modelWidth, modelHeight);
        self.centerX = modelWidth / 2;
        self.centerY = modelHeight / 2

        // Divide in 2
        self.refSize = Math.max(modelWidth, modelHeight) / 2;

        if (self.config == undefined) {
            return;
        }
        self.skin(self.config.skin);
        self.name(self.config.name);
        self.createModules();
        // Draw modules on top of the skin
        $.each(self.modules(), function(idx, mod) {
            mod.draw();
        });
        self.resetSelect();
    }

    self.resetSelect = function() {
        if (!self.editable) {
            return;
        }
        for (var i = 0; i < self.modules().length; i++) {
            // self.modules()[i].image.selectize(false);
            self.modules()[i].image.opacity(0.8);
            // self.modules()[i].image.stroke('#000')
        }
        // if (self.isSelectedModule()) {
        //   self.updateDofVisualisation(-2, true);
        // }
        self.isSelectedModule(false);
    };

    // Create modules
    self.createModules = function() {
        self.modules.removeAll();
        if (self.config != undefined) {
            $.each(self.config.modules, function(idx, mod) {
                var newModule = new Module(mod.module, mod.name, mod.canvas.x, mod.canvas.y, mod.canvas.width, mod.canvas.height, mod.canvas.rotation);
                if (mod.dofs.length == 0) {
                    newModule.dofs.push(new Dof(''));
                }
                $.each(mod.dofs, function(idx, dof) {
                    var newDof = new Dof(dof.name);
                    if (dof.servo != undefined) {
                        newDof.setServo(dof.servo.pin, dof.servo.mid, dof.servo.min, dof.servo.max);
                    }
                    if (dof.mapping != undefined) {
                        newDof.setMap(dof.mapping.neutral);
                        if (dof.mapping.poly != undefined) {
                            newDof.map().poly(dof.mapping.poly);
                        }
                    }
                    newModule.dofs.push(newDof);
                });
                self.modules.push(newModule);
                if (self.selectedModule() == undefined) {
                    self.setSelectedModule(newModule);
                    self.isSelectedModule(false);
                }
            });
        } else {
            var newModule = new Module('', '', 0, 0, 0, 0, 0);
            var newDof = new Dof('');
            newModule.dofs.push(newDof);
            self.setSelectedModule(newModule);
            self.isSelectedModule(false);
        }
    };

    var newModule = new Module('', '', 0, 0, 0, 0, 0);
    var newDof = new Dof('');
    newModule.dofs.push(newDof);
    self.setSelectedModule(newModule);
    self.isSelectedModule(false);

    if (self.editable) {
        var index = 0;
        self.svg_modules = SVG('modules_screen').size('100%', '60');
        // Draw available modules
        if (self.allModules != undefined) {
            $.each(self.allModules, function(idx, mod) {
                // alert(mod);
                // var moduleImage = self.svg.image('static/images/' + mod + '.svg').loaded(function() {

                var moduleImage = self.svg_modules.image('/static/images/modules/' + mod + '.svg').loaded(function() {
                    this.attr({
                        preserveAspectRatio: "none",
                        type: mod
                    });
                    var h = 50;
                    var w = 50;
                    var increase = 5;
                    this.size(w, h);

                    this.move(index * (w + 2 * increase), increase);
                    index += 1;

                    this.style('cursor', 'pointer');
                    // this.selectize();
                    // this.resize({snapToAngle:5});
                    // allModules.push(this);
                    this.on('mouseover', function(e) {
                        this.size(w + increase, h + increase);
                    });
                    this.on('mouseleave', function(e) {
                        this.size(w, h);
                    });
                    this.on('click', function(e) {
                        var newModule = new Module(mod, mod, 0, 0, 0.2, 0.2, 0);
                        var tempModule = new module_function[mod](undefined, 0, 0, 0, 0);
                        for (var i = 0; i < tempModule.dofs.length; i++) {
                            var newDof = new Dof(tempModule.dofs[i]);
                            newModule.dofs.push(newDof);
                        }
                        self.setSelectedModule(newModule);
                        self.isSelectedModule(true);
                        newModule.draw();
                        self.modules.push(newModule);
                    });
                });
            });
        }
    }
    var mousePos;
    document.onmousemove = handleMouseMove;
    document.addEventListener('touchmove', handleMouseMove)

    setInterval(getMousePosition, 750);
    function handleMouseMove(event) {
        var dot, eventDoc, doc, body, pageX, pageY;

        event = event || window.event; // IE-ism

        // If pageX/Y aren't available and clientX/Y are,
        // calculate pageX/Y - logic taken from jQuery.
        // (This is to support old IE)
        if (event.pageX == null && event.clientX != null) {
            eventDoc = (event.target && event.target.ownerDocument) || document;
            doc = eventDoc.documentElement;
            body = eventDoc.body;

            event.pageX = event.clientX +
              (doc && doc.scrollLeft || body && body.scrollLeft || 0) -
              (doc && doc.clientLeft || body && body.clientLeft || 0);
            event.pageY = event.clientY +
              (doc && doc.scrollTop  || body && body.scrollTop  || 0) -
              (doc && doc.clientTop  || body && body.clientTop  || 0 );
        }

        // Use event.pageX / event.pageY here
        mousePos = {
            x: event.pageX,
            y: event.pageY
        };
    }

    function getMousePosition() {
        var pos = mousePos;
        if (!pos) {
            // We haven't seen any movement yet
        }
        else {
            // Use pos.x and pos.y

            var right_eye_module = undefined;
            var left_eye_module = undefined;

            for (var i = 0; i < self.modules().length; i++) {
                // self.modules()[i].image.selectize(false);
                if (self.modules()[i].name() == 'eye_left') {
                  left_eye_module = self.modules()[i];
                }
                if (self.modules()[i].name() == 'eye_right') {
                  right_eye_module = self.modules()[i];
                }
            }

            var delta = 0.2;
            var left_eye_dof_x = -(mousePos.x - left_eye_module.x()) / (left_eye_module.x() * delta);
            var left_eye_dof_y = -(mousePos.y - left_eye_module.y()) / (left_eye_module.y() * delta);

            var right_eye_dof_x = -(mousePos.x - right_eye_module.x()) / (right_eye_module.x() * delta);
            var right_eye_dof_y = -(mousePos.y - right_eye_module.y()) / (right_eye_module.y() * delta);

            robotSendDOF('eye_left', 'pupil_horizontal', left_eye_dof_x);
            robotSendDOF('eye_left', 'pupil_vertical', left_eye_dof_y);

            robotSendDOF('eye_right', 'pupil_horizontal', right_eye_dof_x);
            robotSendDOF('eye_right', 'pupil_vertical', right_eye_dof_y);
        }
    }
    //
    // if (action_data != undefined && action_data.openfile) {
    //     self.loadFileData(action_data.openfile || "");
    // } else {
    //     self.init();
    // }
};

// $(document).ready(function() {
// 	// This makes Knockout get to work
//   // virtualModel = new VirtualModel();
//
// });
