// Create modules
// self.createModules = function() {
// 	self.modules.removeAll();
// 	if (self.config != undefined) {
// 		$.each(self.config.modules, function(idx, mod) {
// 			var newModule = new Module(mod.module, mod.name, mod.canvas.x, mod.canvas.y, mod.canvas.width, mod.canvas.height, mod.canvas.rotation);
//
// 			$.each(mod.dofs, function(idx, dof) {
// 				var newDof = new Dof(dof.name);
// 				if (dof.servo != undefined) {
// 					newDof.setServo(dof.servo.pin, dof.servo.mid, dof.servo.min, dof.servo.max);
// 				}
// 				if (dof.mapping != undefined) {
// 					newDof.setMap(dof.mapping.neutral);
// 					newDof.map().poly(dof.mapping.poly);
// 				}
// 				newModule.dofs.push(newDof);
// 			});
// 			self.modules.push(newModule);
// 			if (self.selectedModule() == undefined) {
// 				self.setSelectedModule(newModule);
// 				self.isSelectedModule(false);
// 			}
// 		});
// 	} else {
// 		var newModule = new Module('', '', 0, 0, 0, 0, 0);
// 		var newDof = new Dof('');
// 		newModule.dofs.push(newDof);
// 		self.setSelectedModule(newModule);
// 		self.isSelectedModule(false);
// 	}
// };

function updateVirtualModel() {
    virtualModel.updateDofVisualisation(-2);
}

function resizeCanvas() {
    // Resize model to fit screen
    // var w = $("#virtualModelDiv").width();
    // var h = $("#virtualModelDiv").height();
    // size = w;
    // if (h < size) { size = h; }
    // $("#model_screen svg").attr("width", size);
    // $("#model_screen svg").attr("height", size);
    updateVirtualModel();
}

updateData = function() {
    $.ajax({
        dataType: "text",
        type: "POST",
        url: "/virtual",
        data: {
            getdata: 1
        },
        success: function(data) {
            //alert(data);
            // console.log(data);
            dof_values = JSON.parse(data)["dofs"];
            // console.log(dof_values);

            // checkData();
            updateVirtualModel();
            // $("#virtualModelCanvas").drawLayers();
        }
    });
    setTimeout(updateData, 50);
}

// // Setup websocket connection.
// var conn = null;
// var connReady = false;
// conn = new SockJS("http://" + window.location.host + "/appsockjs");
//
// self.conn.onopen = function(){
// 	$.ajax({
// 		url: "/appsockjstoken",
// 		cache: false
// 	})
// 	.done(function(data) {
// 		conn.send(JSON.stringify({action: "authenticate", token: data}));
// 		connReady = true;
// 	});
// };
//
// self.conn.onmessage = function(e){
// 	var msg = $.parseJSON(e.data);
// 	switch(msg.action){
// 		case "soundStopped":
//
// 			break;
// 	}
// };
//
// self.conn.onclose = function(){
// 	conn = null;
// 	connReady = false;
// };

$(document).ready(function() {

    virtualModel = new VirtualModel();

    $(window).resize(resizeCanvas);

    resizeCanvas();
    // w = $("#virtualModelCanvas").width();
    // $("#virtualModelCanvas").attr("width", w);
    // $("#virtualModelCanvas").attr("height", w);

    // setupVirtualModel();

    updateData();

});
