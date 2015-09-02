var knobx = 0.5;
var knoby = 0.5;
var r_factor = 0.4;
var w;

function resizeCanvas(){
	w = $("#circumplex").width();

	$("#circumplex").attr("width", w);
	$("#circumplex").attr("height", w);

	updateCircumplex();
}

function setupCircumplex(){
	$("#circumplex")
	.drawImage({
		layer: true,
		name: "bg",
		source: "./static/circumplex_bg.svg",
		x: 0, y: 0,
		width: w,
		height: w,
		fromCenter: false,
		click: function(layer){
			var knob = $("#circumplex").getLayer("knob");

			knob.x = layer.eventX;
			knob.y = layer.eventY;

			constrainKnob();

			$("#circumplex")
			.setLayer("line", {
				x2: knob.x,
				y2: knob.y
			})
			.drawLayers();

			updateUINumbers();
			sendToServer();
		}
	})
	.drawLine({
		layer: true,
		name: "line",
		strokeStyle: '#545454',
		strokeWidth: w*0.02,
		rounded: true,
		x1: w/2, y1: w/2,
		x2: w/2, y2: w/2
	})
	.drawArc({
		layer: true,
		name: "knob",
		draggable: true,
		fillStyle: "#22B573",
		shadowColor: "#23774E",
		shadowBlur: 0,
		shadowX: 0, shadowY: w*0.008,
		x: w/2, y: w/2,
		radius: w*0.03,
		mouseover: function(layer){
			layer.radius = w*0.03*1.2;
			$("#circumplex").drawLayers();
		},
		mouseout: function(layer){
			layer.radius = w*0.03;
			$("#circumplex").drawLayers();
		},
		drag: function(layer){
			constrainKnob();

			$("#circumplex")
			.setLayer("line", {
				x2: layer.x,
				y2: layer.y
			});
			updateUINumbers();
		},
		dragstop: function(layer){
			sendToServer();
		}
	});
}

function updateCircumplex(){
	$("#circumplex")
	.setLayer("bg", {
		width: w,
		height: w
	})
	.setLayer("line", {
		x1: w/2, y1: w/2,
		x2: w*knobx, y2: w*knoby
	})
	.setLayer("knob", {
		shadowY: w*0.008,
		radius: w*0.03,
		x: w*knobx,
		y: w*knoby
	})
	.drawLayers();
}

function constrainKnob(){
	var knob = $("#circumplex").getLayer("knob");

	var r = w*r_factor;

	var xoff = knob.x - w/2;
	var yoff = knob.y - w/2;
	l = Math.sqrt(xoff*xoff + yoff*yoff);

	if(l > r){
		knob.x = w/2 + (xoff * r/l);
		knob.y = w/2 + (yoff * r/l);
	}

	knobx = knob.x/w;
	knoby = knob.y/w;
}

function updateUINumbers(){
	var val = (knobx - 0.5)/r_factor;
	var ar = -1*(knoby - 0.5)/r_factor;

	var r = Math.sqrt(val*val + ar*ar);
	var phi = Math.atan2(ar, val);
	if(isNaN(phi)){
		phi = 0;
	}
	if(phi < 0){
		phi += 2*Math.PI;
	}
	phi = phi*(180/Math.PI);

	$("#lblVal").html(numeral(val).format("+0.000"));
	$("#lblAr").html(numeral(ar).format("+0.000"));
	$("#lblPhi").html(numeral(phi).format("0.0") + " °");
	$("#lblR").html(numeral(r).format("0.000"));
}

function sendToServer(){
	var val = (knobx - 0.5)/r_factor;
	var ar = -1*(knoby - 0.5)/r_factor;

	var r = Math.sqrt(val*val + ar*ar);
	var phi = Math.atan2(ar, val);
	if(isNaN(phi)){
		phi = 0;
	}
	if(phi < 0){
		phi += 2*Math.PI;
	}
	phi = phi*(180/Math.PI);

	$.ajax({
		dataType: "json",
		data: {"phi": phi, "r": r},
		type: "POST",
		url: "setemotion",
		success: function(data){
			if(data.status == "error"){
				addError(data.message);
			}
		}
	});
}

function addError(msg){
	$("#errors").append("<div data-alert class=\"alert-box alert\">" + msg + "<a href=\"#\" class=\"close\">&times;</a></div>");
	$(document).foundation("alert", "reflow");
}

$(document).ready(function(){
	$(window).resize(resizeCanvas);

	w = $("#circumplex").width();
	$("#circumplex").attr("width", w);
	$("#circumplex").attr("height", w);

	setupCircumplex();
	updateUINumbers();

	$("#circumplex").drawLayers();

	$("#btnEnable").click(function(){
		$.ajax({
			dataType: "json",
			url: "servos/enable",
			success: function(data){
				if(data.status == "error"){
					addError(data.message);
				}
			}
		});
	});
	$("#btnDisable").click(function(){
		$.ajax({
			dataType: "json",
			url: "servos/disable",
			success: function(data){
				if(data.status == "error"){
					addError(data.message);
				}
			}
		});
	});
});
