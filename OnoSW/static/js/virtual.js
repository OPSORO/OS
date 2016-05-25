var knobx = 0.5;
var knoby = 0.5;
var r_factor = 0.4;
var w;

var dof_names = [
	"r_eb_inner",
	"r_eb_outer",
	"r_e_ver",
	"r_e_hor",
	"r_e_lid",
	"m_l",
	"m_mid",
	"m_r",
	"l_e_lid",
	"l_e_ver",
	"l_e_hor",
	"l_eb_inner",
	"l_eb_outer",
];

var previous_dofs = {};
// // dofs["r_eb_inner"] 	= 0.0;
// // dofs["r_eb_outer"] 	= 0.0;
// // dofs["r_e_ver"] 		= 0.0;
// // dofs["r_e_hor"] 		= 0.0;
// // dofs["r_e_lid"] 		= 0.0;
// // dofs["m_l"] 				= 0.0;
// // dofs["m_mid"]				= 0.0;
// // dofs["m_r"] 				= 0.0;
// // dofs["l_e_lid"] 		= 0.0;
// // dofs["l_e_ver"] 		= 0.0;
// // dofs["l_e_hor"] 		= 0.0;
// // dofs["l_eb_inner"] 	= 0.0;
// // dofs["l_eb_outer"] 	= 0.0;
//
// dofs["r_eb_inner"] 	= 0.74;
// dofs["r_eb_outer"] 	= 0.42;
// dofs["r_e_ver"] 		= 0.61;
// dofs["r_e_hor"] 		= -0.27;
// dofs["r_e_lid"] 		= 1.0;
// dofs["m_l"] 				= -0.01;
// dofs["m_mid"]				= -0.01;
// dofs["m_r"] 				= -1.0;
// dofs["l_e_lid"] 		= 0.63;
// dofs["l_e_ver"] 		= 0.61;
// dofs["l_e_hor"] 		= 0.26;
// dofs["l_eb_inner"] 	= -1.0;
// dofs["l_eb_outer"] 	= -0.03;


function resizeCanvas(){
	w = $("#virtualModelCanvas").width();

	$("#virtualModelCanvas").attr("width", w);
	$("#virtualModelCanvas").attr("height", w);

	updateVirtualModel();
}

$.jCanvas.extend({
  name: 'drawMouth',
  type: 'mouth',
  props: {},
  fn: function(ctx, params) {
  	// Just to keep our lines short
  	var p = params;
		p.mouth_right = -p.mouth_right;
		p.mouth_left = -p.mouth_left;
		p.mouth_mid = -p.mouth_mid;

  	// Enable layer transformations like scale and rotate
  	$.jCanvas.transformShape(this, ctx, p);
  	// Draw mouth
  	ctx.beginPath();
      ctx.moveTo(p.x-8*p.size, p.y+(3*p.size*p.mouth_left));
      ctx.bezierCurveTo(
        p.x-8*p.size, p.y+(3*p.size*p.mouth_left)-1*p.size,
        p.x-4*p.size, p.y,
        p.x, p.y
      );
      ctx.bezierCurveTo(
        p.x+4*p.size, p.y,
        p.x+8*p.size, p.y+(3*p.size*p.mouth_right)-1*p.size,
        p.x+8*p.size, p.y+(3*p.size*p.mouth_right)
      );
      ctx.bezierCurveTo(
        p.x+8*p.size, p.y+(3*p.size*p.mouth_right)+1*p.size,
        p.x+4*p.size, p.y+(3*p.size*(p.mouth_mid+1)),
        p.x, 					p.y+(3*p.size*(p.mouth_mid+1))
      );
      ctx.bezierCurveTo(
        p.x-4*p.size, p.y+(3*p.size*(p.mouth_mid+1)),
        p.x-8*p.size, p.y+(3*p.size*p.mouth_left)+1*p.size,
        p.x-8*p.size, p.y+(3*p.size*p.mouth_left)
      );
  	ctx.closePath();
  	// Call the detectEvents() function to enable jCanvas events
  	// Be sure to pass it these arguments, too!
  	$.jCanvas.detectEvents(this, ctx, p);
  	// Call the closePath() functions to fill, stroke, and close the path
  	// This function also enables masking support and events
  	// It accepts the same arguments as detectEvents()
  	$.jCanvas.closePath(this, ctx, p);
  }
});

$.jCanvas.extend({
  name: 'drawEyeLid',
  type: 'eyeLid',
  props: {},
  fn: function(ctx, params) {
  	// Just to keep our lines short
  	var p = params;
  	// Enable layer transformations like scale and rotate
  	$.jCanvas.transformShape(this, ctx, p);
  	// Draw mouth
  	ctx.beginPath();
      ctx.moveTo(p.x-4*p.size, p.y+p.size);
      ctx.bezierCurveTo(
  	  	p.x-4*p.size, p.y,
        p.x-2*p.size, p.y,
        p.x, p.y
        );
        ctx.bezierCurveTo(
        p.x+2*p.size, p.y,
        p.x+4*p.size, p.y,
        p.x+4*p.size, p.y+p.size
      );
      ctx.bezierCurveTo(
        p.x+4*p.size, p.y+p.size,
        p.x+4*p.size, p.y+2*p.size,
        p.x+4*p.size, p.y+2*p.size
      );
  		ctx.bezierCurveTo(
        p.x+4*p.size, p.y+5*p.size,
        p.x+3*p.size, p.y+4*p.size-3.5*p.size*p.eyeLidOpen,
        p.x, p.y+4*p.size-3.5*p.size*p.eyeLidOpen
      );
  		ctx.bezierCurveTo(
        p.x-3*p.size, p.y+4*p.size-3.5*p.size*p.eyeLidOpen,
        p.x-4*p.size, p.y+5*p.size,
        p.x-4*p.size, p.y+2*p.size
      );
  		ctx.bezierCurveTo(
        p.x-4*p.size, p.y+2*p.size,
        p.x-4*p.size, p.y+p.size,
        p.x-4*p.size, p.y+p.size
      );
  	ctx.closePath();
  	// Call the detectEvents() function to enable jCanvas events
  	// Be sure to pass it these arguments, too!
  	$.jCanvas.detectEvents(this, ctx, p);
  	// Call the closePath() functions to fill, stroke, and close the path
  	// This function also enables masking support and events
  	// It accepts the same arguments as detectEvents()
  	$.jCanvas.closePath(this, ctx, p);
  }
});

$.jCanvas.extend({
  name: 'drawEyeBrow',
  type: 'eyeBrow',
  props: {},
  fn: function(ctx, params) {
  	// Just to keep our lines short
  	var p = params;

  	// Draw eyeBrow
		// Side: 0 = right, 1 = left
		p.y = p.y - 2*p.size*((p.inner + p.outer)/2);
		p.rotate = 30*((p.inner-p.outer)/2);
		if (p.side == 0){
			p.rotate = 180 + 30*((p.outer-p.inner)/2);
		}
  	// Enable layer transformations like scale and rotate
  	$.jCanvas.transformShape(this, ctx, p);

  	ctx.beginPath();
			ctx.moveTo(p.x-2*p.size, p.y-p.size);
			ctx.bezierCurveTo(
		  	p.x-p.size, p.y-p.size,
	      p.x+4*p.size, p.y-p.size,
	      p.x+4*p.size, p.y
	    );
	    ctx.bezierCurveTo(
	      p.x+4*p.size, p.y+p.size,
	      p.x-p.size, p.y+p.size,
	      p.x-2*p.size, p.y+p.size
	    );
	    ctx.bezierCurveTo(
	      p.x-3*p.size, p.y+p.size,
	      p.x-4*p.size, p.y+p.size,
	      p.x-4*p.size, p.y
	    );
			ctx.bezierCurveTo(
	      p.x-4*p.size, p.y-p.size,
	      p.x-3*p.size, p.y-p.size,
	      p.x-2*p.size, p.y-p.size
	    );
  	ctx.closePath();

  	// Call the detectEvents() function to enable jCanvas events
  	// Be sure to pass it these arguments, too!
  	$.jCanvas.detectEvents(this, ctx, p);
  	// Call the closePath() functions to fill, stroke, and close the path
  	// This function also enables masking support and events
  	// It accepts the same arguments as detectEvents()
  	$.jCanvas.closePath(this, ctx, p);
  }
});

function setupVirtualModel(){
	$("#virtualModelCanvas")
	.drawImage({
		layer: true,
		name: "bg",
		source: "static/img/empty_face.svg",
		x: 0, y: 0,
		width: w,
		height: w,
		fromCenter: false,
	})
	.drawMouth({
    layer: true,
  	name:"mouthlayer",
  	strokeStyle: '#c00',
  	strokeWidth: 4,
    fillStyle: '#000000',
    size: w/60,
    x: w/2, y: w*0.375,
  	mouth_mid: dofs["m_mid"],
    mouth_left: dofs["m_l"],
  	mouth_right: dofs["m_r"]
	})
	.drawEllipse({
  	layer:true,
  	name:"rightEyePupil",
    fillStyle: '#000000',
    x: w*0.405, y: w*0.25,
    width: w/30, height: w/30
	})
	.drawEllipse({
  	layer:true,
  	name:"leftEyePupil",
    fillStyle: '#000000',
    x: w*0.605, y: w*0.25,
    width: w/30, height: w/30
	})
	.drawEyeLid({
    layer: true,
  	name:"rightEyeLidlayer",
    fillStyle: '#FFD63D',
    size: w/65,
  	x: w*0.405, y: w*0.2,
  	eyeLidOpen: dofs["r_e_lid"]
	})
	.drawEyeLid({
    layer: true,
  	name:"leftEyeLidlayer",
    fillStyle: '#FFD63D',
    size: w/65,
  	x: w*0.605, y: w*0.2,
  	eyeLidOpen: dofs["l_e_lid"]
	})
	.drawEyeBrow({
    layer: true,
  	name:"rightEyeBrowlayer",
    fillStyle: '#000000',
    size: w/65,
  	x: w*0.605, y: w*0.16,
  	side: 0,
  	outer: dofs["r_eb_outer"],
  	inner: dofs["r_eb_inner"]
	})
	.drawEyeBrow({
    layer: true,
  	name:"leftEyeBrowlayer",
    fillStyle: '#000000',
    size: w/65,
  	x: w*0.605, y: w*0.16,
  	side: 1,
  	outer: dofs["l_eb_outer"],
  	inner: dofs["l_eb_inner"]
	})
  updateVirtualModel();
}

function updateVirtualModel(){
	$("#virtualModelCanvas")
	.setLayer("bg", {
		width: w,
		height: w
	})
	.setLayer("mouthlayer", {
    x: w/2, y: w*0.375,
  	size: w/60,
		mouth_mid: dofs["m_mid"],
		mouth_left: dofs["m_l"],
		mouth_right: dofs["m_r"]
	})
	.setLayer("rightEyePupil", {
		x: w*0.405 + (w/35 * dofs["r_e_hor"]), y: w*0.25 - (w/35 * dofs["r_e_ver"]),
		width: w/30, height: w/30
	})
	.setLayer("rightEyeLidlayer", {
		size: w/65,
		x: w*0.405, y: w*0.2,
		eyeLidOpen: dofs["r_e_lid"]
	})
	.setLayer("rightEyeBrowlayer", {
		size: w/65,
		x: w*0.405, y: w*0.16,
		outer: dofs["r_eb_outer"],
		inner: dofs["r_eb_inner"]
	})
	.setLayer("leftEyePupil", {
		x: w*0.605 - (w/35 * dofs["l_e_hor"]), y: w*0.25 - (w/35 * dofs["l_e_ver"]),
		width: w/30, height: w/30
	})
	.setLayer("leftEyeLidlayer", {
		size: w/65,
		x: w*0.605, y: w*0.2,
		eyeLidOpen: dofs["l_e_lid"]
	})
	.setLayer("leftEyeBrowlayer", {
		size: w/65,
		x: w*0.605, y: w*0.16,
		outer: dofs["l_eb_outer"],
		inner: dofs["l_eb_inner"]
	})
	.drawLayers();
}

function checkData(){
	for (var i = 0; i<13; i++) {
  	if (dofs[dof_names[i]] == undefined){
			if (previous_dofs[dof_names[i]] == undefined){
				dofs[dof_names[i]] = 0.0;
			}else{
				dofs[dof_names[i]] = previous_dofs[dof_names[i]];
			}
		}
	}
	previous_dofs = dofs;
}

updateData = function(){
	$.ajax({
		dataType: "text",
		type: "POST",
		url: "/virtual",
		data: { dataonly: 1 },
		success: function(data){
			// alert(data);
			dofs = JSON.parse(data)["data"];
			//alert(dofs["l_eb_inner"]);
			checkData();
			updateVirtualModel();
			$("#virtualModelCanvas").drawLayers();
		}
	});
	setTimeout(updateData,500);
}

$(document).ready(function(){
	$(window).resize(resizeCanvas);

	w = $("#virtualModelCanvas").width();
	$("#virtualModelCanvas").attr("width", w);
	$("#virtualModelCanvas").attr("height", w);

	setupVirtualModel();

	updateData();

});
