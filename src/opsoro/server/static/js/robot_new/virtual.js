
function updateVirtualModel() {
    virtualModel.updateDofVisualisation(-2, false);
}

updateData = function() {
    var timeOut = 500;

    // prev_dof_values = dof_values;
    // dof_values = robotSendReceiveAllDOF(undefined); //JSON.parse(data);
    // console.log(dof_values);
    // if (prev_dof_values != undefined) {
    //   for (var i = 0; i < prev_dof_values.length; i++) {
    //     if (prev_dof_values[i] != dof_values[i]) {
    //       timeOut = 100;
    //     }
    //   }
    // }
    // // checkData();
    // updateVirtualModel();
    // $.ajax({
    //   dataType: 'json',
    //   type: 'POST',
    //   url: '/robot/dofs/',
    //   success: function(data){
    //     if (!data.success) {
    //       showMainError(data.message);
    //     } else {
    //       return data.dofs;
    //     }
    //   }
    // });


    $.ajax({
        dataType: "json",
        type: "POST",
        url: "/robot/dofs/",
        // data: {
        //     getdata: 1
        // },
        success: function(data) {
            //alert(data);
            // console.log(data);
            prev_dof_values = dof_values;
            // dof_values = data.split(','); //JSON.parse(data);
            dof_values = data.dofs;
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

    $(window).resize(virtualModel.redraw);
    updateData();
    virtualModel.redraw();


});
