
function updateVirtualModel() {
    virtualModel.updateDofVisualisation(-2);
}

updateData = function() {
    var timeOut = 500;
    $.ajax({
        dataType: "text",
        type: "POST",
        url: "/robot/dofs/",
        data: {
            getdata: 1
        },
        success: function(data) {
            //alert(data);
            // console.log(data);
            prev_dof_values = dof_values;
            dof_values = data.split(','); //JSON.parse(data);
            // console.log(dof_values);
            if (prev_dof_values != undefined) {
              for (var i = 0; i < prev_dof_values.length; i++) {
                if (prev_dof_values[i] != dof_values[i]) {
                  timeOut = 100;
                }
              }
            }
            // checkData();
            updateVirtualModel();
            // $("#virtualModelCanvas").drawLayers();
        }
    });
    setTimeout(updateData, timeOut);
}

// // Setup websocket connection.
// var conn = null;
// var connReady = false;
// conn = new SockJS("http://" + window.location.host + "/sockjs");
//
// self.conn.onopen = function(){
// 	$.ajax({
// 		url: "/sockjstoken",
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

    $(window).resize(virtualModel.redraw);

    updateData();

});
