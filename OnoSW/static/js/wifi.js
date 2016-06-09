$(function(){
	

$.ajax({
	type: "GET",
	url: "/app/WiFi/static/wifi"
	}).done(function(o){

	var split = o.split("\n");
	
	for (i = 0; i < split.length-1; ++i) {
    		
	

		$("#ssid-select").append($("<option></option>")
                    .attr("value",split[i])
                    .text(split[i]));
		
	}


});


$("#passwordfield").on("keyup",function(){
    if($(this).val())
        $(".fa-eye").show();
    else
        $(".fa-eye").hide();
    });
$(".fa-eye").mousedown(function(){
                $("#passwordfield").attr('type','text');
            }).mouseup(function(){
            	$("#passwordfield").attr('type','password');
            }).mouseout(function(){
            	$("#passwordfield").attr('type','password');
            });


});

