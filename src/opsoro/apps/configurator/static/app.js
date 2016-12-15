// $(document).ready(function() {
// 	var angleSnap = 360;
//
//
//   var Model = function(){
//     var self = this;
// 		//
//     // // File operations toolbar item
// 		// self.fileIsLocked = ko.observable(false);
// 		// self.fileIsModified = ko.observable(false);
// 		// self.fileName = ko.observable("Untitled");
// 		// self.fileStatus = ko.observable("");
// 		// self.fileExtension = ko.observable(".conf");
// 		//
// 		// self.config = undefined;//config_data;
// 		// self.allModules = modules_name;
// 		// self.allSkins = skins_name;
// 		// self.skin = ko.observable(self.allSkins[0]);
// 		// self.name = ko.observable("OPSORO robot");
// 		//
// 		// self.isSelectedModule = ko.observable(false);
// 		// self.selectedModule = ko.observable();
// 		// // self.selectedModule_SelectedDofIndex = ko.observable(0);
// 		// self.selectedModule_SelectedDof = ko.observable();
// 		//
// 		// self.modules = ko.observableArray();
// 		//
// 		// // create svg drawing
//     // self.svg = SVG('config_screen').size('100%', '600');
// 		//
// 		// self.modelwidth = $('#config_screen svg').width();
// 		// self.modelheight = self.svg.height();
// 		// self.refSize = 0;
// 		//
// 		// self.gridSize = ko.observable(20);
// 		// self.screenGridSize = Math.min(self.modelwidth, self.modelheight) / self.gridSize();
// 		// self.snap = ko.observable(1);
// 		//
// 		// self.centerX = self.modelwidth/2;
// 		// self.centerY = self.modelheight/2;
// 		//
// 		// self.skin_image = undefined;
// 		// self.newConfig = true;
// 		//
// 		// self.clearDraw = function(){
// 		// 	self.resetSelect();
// 		// 	self.svg.clear();
// 		// 	if (self.config != undefined) {
// 		// 		if (self.config.grid != undefined) {
// 		// 			self.gridSize(self.config.grid);
// 		// 		}
// 		// 	}
// 		// 	self.screenGridSize = Math.min(self.modelwidth, self.modelheight) / self.gridSize();
// 		// 	var pattern = self.svg.pattern(self.screenGridSize, self.screenGridSize, function(add) {
// 		// 	  // add.rect(self.screenGridSize, self.screenGridSize).fill('#eee');
// 		// 	  // add.rect(10,10);
// 		// 		var size = self.screenGridSize * 3 / 16;
// 		// 	  add.rect(size, size).fill('#444');
// 		// 	  add.rect(size, size).move(self.screenGridSize - size, 0).fill('#444');
// 		// 	  add.rect(size, size).move(0, self.screenGridSize - size).fill('#444');
// 		// 	  add.rect(size, size).move(self.screenGridSize - size, self.screenGridSize - size).fill('#444');
// 		// 	})
// 		// 	self.grid = self.svg.rect(self.modelwidth, self.modelheight).attr({ fill: pattern });
// 		// };
// 		// self.setSelectedModule = function(module) {
// 		// 	self.selectedModule(module);
// 		// 	self.selectedModule_SelectedDof(self.selectedModule().dofs()[0]);
// 		// 	self.isSelectedModule(true);
// 		// 	self.updateMappingGraph();
// 		// };
// 		// self.selectedModule_RotateLeft = function() {
// 		// 	self.selectedModule().rotation((self.selectedModule().rotation() - 90) % 360);
// 		// 	self.selectedModule().image.rotate(self.selectedModule().rotation());
// 		// };
// 		// self.selectedModule_RotateRight = function() {
// 		// 	self.selectedModule().rotation((self.selectedModule().rotation() + 90) % 360);
// 		// 	self.selectedModule().image.rotate(self.selectedModule().rotation());
// 		// };
// 		// self.selectedModule_AddDof = function() {
// 		// 	var newDof = new Dof("New dof");
// 		// 	self.selectedModule().dofs.push(newDof);
// 		// 	self.selectedModule_SelectedDof(newDof);
// 		// 	// self.selectedModule_SelectedDofIndex(self.selectedModule().dofs().length-1);
// 		// };
// 		// self.selectedModule_Remove = function() {
// 		// 	self.resetSelect();
// 		// 	self.selectedModule().image.remove();
// 		// 	self.modules.remove(self.selectedModule());
// 		// };
// 		// self.selectedModule_RemoveDof = function() {
// 		// 	// self.selectedModule().dofs.splice(self.selectedModule_SelectedDofIndex(), 1);
// 		// 	self.selectedModule().dofs.remove(self.selectedModule_SelectedDof());
// 		// 	// self.selectedModule_SelectedDofIndex(0);
// 		// 	if (self.selectedModule().dofs().length == 0) {
// 		// 		self.selectedModule_AddDof();
// 		// 	}
// 		// 	self.selectedModule_SelectedDof(self.selectedModule().dofs()[0]);
// 		// };
// 		//
// 		// self.saveConfig = function(){
// 		// 	var svg_data = {};
// 		// 	svg_data['name'] = self.name();
// 		// 	svg_data['skin'] = self.skin();
// 		// 	svg_data['grid'] = self.gridSize();
// 		//
// 		// 	svg_data['modules'] = [];
// 		//
// 		// 	for (var i = 0; i < self.modules().length; i++) {
// 		// 		var singleModule = self.modules()[i];
// 		// 		var module_data = {};
// 		// 		module_data['module'] = singleModule.module();
// 		// 		module_data['name'] = singleModule.name();
// 		// 		var matrix = new SVG.Matrix(singleModule.image);
// 		// 		module_data['canvas'] = {
// 		// 			x: 				(singleModule.image.cx() - self.centerX) / self.refSize,
// 		// 			y: 				(singleModule.image.cy() - self.centerY) / self.refSize,
// 		// 			width: 		singleModule.image.width() / self.refSize,
// 		// 			height: 	singleModule.image.height() / self.refSize,
// 		// 			rotation: matrix.extract().rotation
// 		// 		};
// 		// 		if (singleModule.dofs() != undefined) {
// 		// 			module_data['dofs'] = [];
// 		// 			for (var j = 0; j < singleModule.dofs().length; j++) {
// 		// 				var singleDof = singleModule.dofs()[j];
// 		// 				var dof_data = {};
// 		//
// 		// 				dof_data['name'] = singleDof.name();
// 		// 				if (singleDof.isServo()) {
// 		// 					dof_data['servo'] = singleDof.servo();
// 		// 				}
// 		// 				if (singleDof.isMap()) {
// 		// 					dof_data['mapping'] = singleDof.map();
// 		// 				}
// 		// 				module_data['dofs'].push(dof_data);
// 		// 			}
// 		// 		}
// 		// 		svg_data['modules'].push(module_data);
// 		// 	}
// 		//
// 		// 	return svg_data;
// 		// };
// 		//
//     // self.init = function() {
//     //   // Clear data, new file, ...
// 		// 	self.fileName("Untitled");
// 		// 	self.fileIsModified(false);
// 		// 	self.redraw();
//     // };
// 		//
//     // self.loadFileData = function(filename) {
// 		// 	if (filename == "") {
// 		// 		//("No filename!");
// 		// 		return;
// 		// 	}
// 		// 	$.ajax({
// 		// 		dataType: "text",
// 		// 		type: "POST",
// 		// 		url: "files/get",
// 		// 		cache: false,
// 		// 		data: {path: filename, extension: self.fileExtension()},
// 		// 		success: function(data) {
// 		// 			// Load data
// 		// 			var dataobj = JSON.parse(data);
// 		// 			// Do something with the data
// 		// 			self.newConfig = true;
// 		// 			self.config = dataobj;
// 		// 			self.redraw();
// 		// 			// Update filename and asterisk
// 		// 			var filename_no_ext = filename;
// 		// 			if(filename_no_ext.toLowerCase().slice(-4) == self.fileExtension()){
// 		// 				filename_no_ext = filename_no_ext.slice(0, -4);
// 		// 			}
// 		// 			self.fileName(filename_no_ext);
// 		// 			self.fileIsModified(false);
// 		// 		},
// 		// 		error: function() {
// 		// 			window.location.href = "?";
// 		// 		}
// 		// 	});
// 		// };
// 		//
// 		// self.saveFileData = function(filename){
// 		// 	if(filename == "") {
// 		// 		//("No filename!");
// 		// 		return;
// 		// 	} else {
//     //     // Convert data
//     //     file_data = self.saveConfig();
// 		//
// 		// 		var data = ko.toJSON(file_data, null, 2);
// 		// 		// var data = file_data;
// 		// 		// alert(data);
// 		//
//     //     // Send data
// 		// 		$.ajax({
// 		// 			dataType: "json",
// 		// 			data: {
// 		// 				path: filename,
// 		// 				filedata: data,
// 		// 				overwrite: 1,
// 		// 				extension: self.fileExtension()
// 		// 			},
// 		// 			type: "POST",
// 		// 			url: "files/save",
// 		// 			success: function(data){
// 		// 				var filename_no_ext = filename;
// 		// 				if(filename_no_ext.toLowerCase().slice(-4) == self.fileExtension()){
// 		// 					filename_no_ext = filename_no_ext.slice(0, -4);
// 		// 				}
// 		// 				self.fileName(filename_no_ext);
// 		// 				self.fileIsModified(false);
// 		// 			}
// 		// 		});
// 		// 	}
// 		// };
// 		//
// 		// //-------------------------------------------------------------------------------
// 		// // SVG stuff
// 		// //-------------------------------------------------------------------------------
// 		//
// 		// // 	var axisY = self.svg.line(0, centerY, self.modelwidth/2, centerY).stroke({ width: 1 });
// 		// // var axisX = self.svg.line(centerX, 0, centerX, self.modelheight).stroke({ width: 1 });
// 		// // var Seperator = self.svg.line(self.modelwidth/2, 0, self.modelwidth/2, self.modelheight).stroke({ width: 3 });
// 		//
// 		// // Draw skin & modules
// 		// self.redraw = function() {
// 		// 	if (!self.newConfig) { self.config = self.saveConfig();	}
// 		// 	else { self.newConfig = false; }
// 		// 	self.clearDraw();
// 		// 	if (self.config != undefined) {
// 		// 		self.skin_image = self.svg.image('static/images/skins/' + self.config.skin + '.svg').loaded(self.drawModules);
// 		// 	}
// 		// 	else {
// 		// 		self.skin_image = self.svg.image('static/images/skins/' + self.skin() + '.svg').loaded(self.drawModules);
// 		// 	}
// 		// };
// 		//
// 		// var previousMapIndex = -1;
// 		// self.updateDofVisualisation = function(mapIndex) {
// 		// 	if (previousMapIndex != mapIndex) {
// 		// 		$.each(self.modules(), function(idx, mod) {
// 		// 			mod.updateDofVisualisation(mapIndex);
// 		// 		});
// 		// 	} else {
// 		// 		self.selectedModule().updateDofVisualisation(mapIndex);
// 		// 	}
// 		// 	previousMapIndex = mapIndex;
// 		// };
// 		//
// 		// self.drawModules = function() {
// 		// 	$("image, svg").mousedown(function(){
// 		// 		model.resetSelect();
// 		// 		return false;
// 		// 	});
// 		//
// 		//
// 		//
// 		//
// 		// 	var dx = self.modelwidth / self.skin_image.width();
// 		// 	var dy = self.modelheight / self.skin_image.height();
// 		//
// 		// 	var modelWidth, modelHeight;
// 		//
// 		// 	if (dx < dy) {
// 		// 		modelWidth = self.modelwidth;
// 		// 		modelHeight = self.skin_image.height() * dx;
// 		// 	}	else {
// 		// 		modelWidth = self.skin_image.width() * dy;
// 		// 		modelHeight = self.modelheight;
// 		// 	}
// 		//
// 		// 	self.skin_image.size(modelWidth, modelHeight);
// 		// 	self.centerX = modelWidth / 2;
// 		// 	self.centerY = modelHeight / 2
// 		//
// 		// 	// Divide in 2
// 		// 	self.refSize = Math.max(modelWidth, modelHeight) / 2;
// 		//
// 		// 	if (self.config == undefined) { return; }
// 		// 	self.skin(self.config.skin);
// 		// 	self.name(self.config.name);
// 		// 	self.createModules();
// 		// 	// Draw modules on top of the skin
// 		// 	$.each(self.modules(), function(idx, mod) {
// 		// 		mod.draw();
// 		// 	});
// 		// 	self.resetSelect();
// 		// }
// 		//
// 		// self.mappingGraph = SVG('poly_screen').size('100%', '121');
// 		//
// 		// self.mappingGraphWidth = $('#poly_screen svg').width();
// 		// self.mappingGraphHeight = self.mappingGraph.height();
// 		// self.mappingPoints = ko.observableArray();
// 		//
// 		// // var rect = self.mappingGraph.rect(self.mappingGraphWidth, self.mappingGraphHeight);
// 		// // rect.fill("#AAA");
// 		//
// 		// self.mappingGraphCenterY = self.mappingGraphHeight / 2;
// 		// self.mappingGraphNodeSize = self.mappingGraphWidth / 30;
// 		//
// 		// self.mappingGraph_StepWidth = self.mappingGraphWidth / 21;
// 		// self.mappingGraph_StartX = self.mappingGraphNodeSize;
// 		//
// 		//
// 		// var startX, text, line;
// 		// startX = 5;
// 		// var texts = ['1', '0', '-1'];
// 		// var Ys = [self.mappingGraphNodeSize, self.mappingGraphCenterY, self.mappingGraphHeight - self.mappingGraphNodeSize];
// 		// line = self.mappingGraph.line(startX*2, Ys[0], startX*2, Ys[2]).stroke({ width: 0.5 });
// 		// line = self.mappingGraph.line(self.mappingGraphWidth-1, Ys[0], self.mappingGraphWidth-1, Ys[2]).stroke({ width: 0.5 });
// 		//
// 		// for (var i = Ys[0]; i < Ys[2]; i+= self.mappingGraphHeight/40){
// 		// 	self.mappingGraph.line(startX*2, i, self.mappingGraphWidth-1, i).stroke({ width: 0.2 });
// 		// }
// 		//
// 		// for (var i = 0; i < texts.length; i++){
// 		// 	text = self.mappingGraph.plain(texts[i]);
// 		// 	text.center(startX, Ys[i]);
// 		// 	line = self.mappingGraph.line(startX*2, Ys[i], self.mappingGraphWidth-1, Ys[i]).stroke({ width: 0.5 });
// 		// }
// 		//
// 		// var updateInfoTxt = function(circ) {
// 		// 	self.mappingGraph_InfoRect.show();
// 		// 	self.mappingGraph_InfoTxt.show();
// 		// 	var num = (self.mappingGraphCenterY - circ.cy()) / (self.mappingGraphCenterY - self.mappingGraphNodeSize);
// 		// 	num = Math.round(num * 20) / 20;	// Round to 0.05
// 		// 	self.mappingGraph_InfoTxt.plain(num);
// 		// 	if (circ.cx() > self.mappingGraph_InfoRect.width() * 2) {
// 		// 		self.mappingGraph_Info.move(circ.cx() - self.mappingGraph_InfoRect.width() - self.mappingGraphNodeSize*3/2, circ.cy() + self.mappingGraph_InfoRect.height()/2 - 1)
// 		// 	} else {
// 		// 		self.mappingGraph_Info.move(circ.cx() + self.mappingGraphNodeSize*3/2, circ.cy() + self.mappingGraph_InfoRect.height()/2 - 1)
// 		// 	}
// 		// 	return num;
// 		// };
// 		// var hideInfoTxt = function() {
// 		// 	self.mappingGraph_InfoRect.hide();
// 		// 	self.mappingGraph_InfoTxt.hide();
// 		// };
// 		//
// 		// for (var i = 0; i < 20; i++) {
// 		// 	line = self.mappingGraph.line(self.mappingGraph_StartX*2 + self.mappingGraph_StepWidth * i, Ys[0], self.mappingGraph_StartX*2 + self.mappingGraph_StepWidth * i, Ys[2]).stroke({ width: 0.2 });
// 		// 	var circle = self.mappingGraph.circle(self.mappingGraphNodeSize);
// 		// 	circle.fill('#286')
// 		// 	circle.center(self.mappingGraph_StartX*2 + self.mappingGraph_StepWidth * i, self.mappingGraphCenterY);
// 		// 	circle.draggable(function(x, y) {
// 		// 	  return { x: x == self.mappingGraph_StartX*2 + self.mappingGraph_StepWidth * i, y: y > self.mappingGraphNodeSize/2 - 1 && y < (self.mappingGraphHeight - self.mappingGraphNodeSize*3/2) }
// 		// 	});
// 		// 	circle.attr({ index: i });
// 		// 	circle.on('mouseover', function() {
// 		// 		updateInfoTxt(this);
// 		// 	});
// 		// 	circle.on('mouseleave', function() {
// 		// 		hideInfoTxt();
// 		// 	});
// 		// 	circle.on('dragmove', function() {
// 		// 		var num = updateInfoTxt(this);
// 		// 		self.selectedModule_SelectedDof().map().poly()[this.attr('index')] = num;
// 		// 		model.updateDofVisualisation(this.attr('index'));
// 		// 	});
// 		// 	circle.on('dragend', function(e){
// 		// 		var num = updateInfoTxt(this);
// 		// 		this.cy(self.mappingGraphCenterY - num * (self.mappingGraphCenterY - self.mappingGraphNodeSize));
// 		// 		self.selectedModule_SelectedDof().map().poly()[this.attr('index')] = num;
// 		// 		model.updateDofVisualisation(this.attr('index'));
// 		// 	});
// 		// 	self.mappingPoints.push(circle);
// 		// }
// 		// self.mappingGraph_Info = self.mappingGraph.nested();
// 		// self.mappingGraph_InfoRect = self.mappingGraph_Info.rect(30, 12);
// 		// self.mappingGraph_InfoRect.move(-2, -10);
// 		// self.mappingGraph_InfoRect.fill('#fff');
// 		// self.mappingGraph_InfoRect.stroke({ color: '#222', opacity: 0.8, width: 1 });
// 		// self.mappingGraph_InfoTxt = self.mappingGraph_Info.plain('');
// 		// self.mappingGraph_InfoTxt.move(0, 0);
// 		// self.mappingGraph_InfoTxt.fill('#000');
// 		// hideInfoTxt();
// 		//
// 		// self.updateMappingGraph = function() {
// 		// 	for (var i = 0; i < self.mappingPoints().length; i++) {
// 		// 		self.mappingPoints()[i].cy(self.mappingGraphCenterY - self.selectedModule_SelectedDof().map().poly()[i] * (self.mappingGraphCenterY - self.mappingGraphNodeSize));
// 		// 	}
// 		// };
// 		//
// 		// self.resetSelect = function(){
// 		// 	for (var i = 0; i < self.modules().length; i++) {
// 		// 		// self.modules()[i].image.selectize(false);
// 		// 		self.modules()[i].image.opacity(0.8);
// 		// 	}
// 		// 	self.isSelectedModule(false);
// 		// };
// 		//
// 		// // Create modules
// 		// self.createModules = function() {
// 		// 	self.modules.removeAll();
// 		// 	if (self.config != undefined) {
// 		// 		$.each(self.config.modules, function(idx, mod) {
// 		// 			var newModule = new Module(mod.module, mod.name, mod.canvas.x, mod.canvas.y, mod.canvas.width, mod.canvas.height, mod.canvas.rotation);
// 		//
// 		// 			$.each(mod.dofs, function(idx, dof) {
// 		// 				var newDof = new Dof(dof.name);
// 		// 				if (dof.servo != undefined) {
// 		// 					newDof.setServo(dof.servo.pin, dof.servo.mid, dof.servo.min, dof.servo.max);
// 		// 				}
// 		// 				if (dof.mapping != undefined) {
// 		// 					newDof.setMap(dof.mapping.neutral);
// 		// 					newDof.map().poly(dof.mapping.poly);
// 		// 				}
// 		// 				newModule.dofs.push(newDof);
// 		// 			});
// 		// 			self.modules.push(newModule);
// 		// 			if (self.selectedModule() == undefined) {
// 		// 				self.setSelectedModule(newModule);
// 		// 				self.isSelectedModule(false);
// 		// 			}
// 		// 		});
// 		// 	} else {
// 		// 		var newModule = new Module('', '', 0, 0, 0, 0, 0);
// 		// 		var newDof = new Dof('');
// 		// 		newModule.dofs.push(newDof);
// 		// 		self.setSelectedModule(newModule);
// 		// 		self.isSelectedModule(false);
// 		// 	}
// 		// };
// 		//
// 		// var newModule = new Module('', '', 0, 0, 0, 0, 0);
// 		// var newDof = new Dof('');
// 		// newModule.dofs.push(newDof);
// 		// self.setSelectedModule(newModule);
// 		// self.isSelectedModule(false);
// 		//
// 		// var index = 0;
// 		// self.svg_modules = SVG('modules_screen').size('100%', '60');
// 		// // Draw available modules
// 		// $.each(self.allModules, function(idx, mod){
// 		// 	// alert(mod);
// 		// 	// var moduleImage = self.svg.image('static/images/' + mod + '.svg').loaded(function() {
// 		//
// 		// 	var moduleImage = self.svg_modules.image('static/images/' + mod + '.svg').loaded(function() {
// 		// 		this.attr({ preserveAspectRatio: "none", type: mod });
// 		// 		var h = 50;
// 		// 		var w = 50;
// 		// 		var increase = 5;
// 		// 		this.size(w, h);
// 		//
// 		// 		this.move(index * (w+2*increase), increase);
// 		// 		index += 1;
// 		//
// 		// 		this.style('cursor', 'pointer');
// 		// 		// this.selectize();
// 		// 		// this.resize({snapToAngle:5});
// 		// 		// allModules.push(this);
// 		// 		this.on('mouseover', function(e){
// 		// 			this.size(w+increase, h+increase);
// 		// 		});
// 		// 		this.on('mouseleave', function(e){
// 		// 			this.size(w, h);
// 		// 		});
// 		// 		this.on('click', function(e){
// 		// 			var newModule = new Module(mod, mod, 0, 0, 0.2, 0.2, 0);
// 		// 			var tempModule = new module_function[mod](undefined, 0, 0, 0, 0);
// 		// 			for (var i = 0; i < tempModule.dofs.length; i++) {
// 		// 				var newDof = new Dof(tempModule.dofs[i]);
// 		// 				newModule.dofs.push(newDof);
// 		// 			}
// 		// 			self.setSelectedModule(newModule);
// 		// 			self.isSelectedModule(true);
// 		// 			newModule.draw();
// 		// 			self.modules.push(newModule);
// 		// 		});
// 		// 	});
// 		// });
//
// 		if (action_data.openfile) {
// 			virtualModel.loadFileData(action_data.openfile || "");
// 		} else {
// 			virtualModel.init();
// 		}
//   };
//   // This makes Knockout get to work
//   // var model = new Model();
//
//   virtualModel = new VirtualModel();
//   ko.applyBindings(virtualModel);
// 	virtualModel.fileIsModified(false);
//
//   // Configurate toolbar handlers
//   config_file_operations("/", virtualModel.fileExtension(), virtualModel.saveFileData, virtualModel.loadFileData, virtualModel.init);
//
//
//
//
// });
//


$(document).ready(function() {
    virtualModel = new VirtualModel();
    ko.applyBindings(virtualModel);
    virtualModel.fileIsModified(false);

    // Configurate toolbar handlers
    config_file_operations("/", virtualModel.fileExtension(), virtualModel.saveFileData, virtualModel.loadFileData, virtualModel.init);
		$(window).resize(virtualModel.redraw);
});
