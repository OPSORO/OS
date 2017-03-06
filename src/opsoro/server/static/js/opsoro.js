function showMainError(msg){
  $("#errors").append("<div data-alert class='alert-box alert'>" + msg + "<a href='#' class='close'>&times;</a></div>");
  $(document).foundation('alert', 'reflow');
  // setTimeout(function () {
  //     showFiles(_CurrentPath, _OnlyFolders, _SaveFileView);
  // }, 200);
}
function showMainMessage(msg){
  $("#errors").append("<div data-alert class='alert-box info'>" + msg + "<a href='#' class='close'>&times;</a></div>");
  $(document).foundation('alert', 'reflow');
}
function showMainSuccess(msg){
  $("#errors").append("<div data-alert class='alert-box success'>" + msg + "<a href='#' class='close'>&times;</a></div>");
  $(document).foundation('alert', 'reflow');
}

function showPopup(sIcon, sTitle, sClass, sContent) {
  $("#popup").addClass(sClass);
  $("#popup .titlebar .titleicon span").addClass(sIcon);
  $("#popup .titlebar .title").html(sTitle);

  if (sContent != ""){
    $("#popup .content").html(sContent);
  }

  $("#popup .btnClose").off("click");
  $("#popup .btnClose").on("click", closePopup);

  // Open message popup
  if (!$("#popup").hasClass("open")){
    $("#popup").foundation("reveal", "open");
  }
}
function closePopup() {
  $("#popup").foundation("reveal", "close");

  // Clear text & icon
  $("#popup .titlebar .titleicon span").removeClass();
  $("#popup .titlebar .titleicon span").addClass("fa");
  $("#popup .titlebar .title").html("");
  $("#popup .content").html("");

  $("#popup").removeClass();
  $("#popup").addClass("reveal-modal");
}
function showMessagePopup(sIcon, sTitle, sText, handlers) {
  $("#message_popup .titlebar .titleicon span").addClass(sIcon);
  $("#message_popup .titlebar .title").html(sTitle);
  $("#message_popup .content .text").html(sText);

  data = {};

  // Input enabling
  if (handlers.inputText != undefined){
    $("#message_popup .inputText").removeClass("hide");
    $("#message_popup .inputText").on("input", handlers.inputText);
  }

  // Button click handlers
  if (handlers.btnOk != undefined){
    $("#message_popup .btnOk").removeClass("hide");
    $("#message_popup .btnOk").on("click", handlers.btnOk);
  }
  if (handlers.btnYes != undefined){
    $("#message_popup .btnYes").removeClass("hide");
    $("#message_popup .btnYes").on("click", handlers.btnYes);
  }
  if (handlers.btnNo != undefined){
    $("#message_popup .btnNo").removeClass("hide");
    $("#message_popup .btnNo").on("click", handlers.btnNo);
  }
  if (handlers.btnSave != undefined){
    $("#message_popup .btnSave").removeClass("hide");
    $("#message_popup .btnSave").on("click", handlers.btnSave);
  }
  if (handlers.btnCancel != undefined){
    $("#message_popup .btnCancel").removeClass("hide");
    $("#message_popup .btnCancel").on("click", handlers.btnCancel);
  }

  $("#message_popup .btnClose").off("click");
  $("#message_popup .btnClose").on("click", closeMessagePopup);

  // Open message popup
  if (!$("#message_popup").hasClass("open")){
    $("#message_popup").foundation("reveal", "open");
  }
}
function closeMessagePopup() {
  $("#message_popup").foundation("reveal", "close");

  // Clear text & icon
  $("#message_popup .titlebar .titleicon span").removeClass();
  $("#message_popup .titlebar .titleicon span").addClass("fa");
  $("#message_popup .titlebar .title").html("");
  $("#message_popup .content .text").html("");

  // Clear inputs
  $("#message_popup .inputText").val("");

  // Hide inputs
  $("#message_popup .inputText").addClass("hide");

  // Hide buttons
  $("#message_popup .btnOk").addClass("hide");
  $("#message_popup .btnYes").addClass("hide");
  $("#message_popup .btnNo").addClass("hide");
  $("#message_popup .btnSave").addClass("hide");
  $("#message_popup .btnCancel").addClass("hide");

  // Remove click handlers
  $("#message_popup .btnOk").off("click");
  $("#message_popup .btnYes").off("click");
  $("#message_popup .btnNo").off("click");
  $("#message_popup .btnSave").off("click");
  $("#message_popup .btnCancel").off("click");
}

function popupWindow(mylink, windowname)
{
	if (! window.focus) return true;
	var href;
	if (typeof(mylink) == 'string')
	   href=mylink;
	else
	   href=mylink.href;
	window.open(href, windowname, 'width=400,height=400,scrollbars=no');
	return false;
}


// -------------------------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------------------------
// Socket connection
//--------------------------------------------------------------------------------------------------------
// Setup websocket connection.
$(document).ready(function(){
  conn = null;
  connReady = false;
  conn = new SockJS("http://" + window.location.host + "/usersockjs");

  conn.onopen = function(){
    // $.ajax({
    //   url: "/appsockjstoken",
    //   cache: false
    // })
    // .done(function(data) {
    //   conn.send(JSON.stringify({action: "authenticate", token: data}));
    //   console.log('SOCKET connected');
    //   connReady = true;
    // });
  };

  conn.onmessage = function(e){
    console.log('SOCKET message');
    try {
      var msg = $.parseJSON(e.data);
      console.log(msg.action);
      switch(msg.action){
        case "logout":
          // alert('Another user logged in.')
          if (window.location.href != '/login') {
            window.location.href = '/';
          }
          break;
        case "info":
          console.log(msg);
          break;
        case "users":
          console.log(msg.count);
          break;
      }
    } catch (e) {
      console.log(e);
    } finally {

    }

  };

  conn.onclose = function(){
    console.log('SOCKET close');
    conn = null;
    connReady = false;
  };
});
// -------------------------------------------------------------------------------------------------------
// Robot control functions
// -------------------------------------------------------------------------------------------------------
function robotSendReceiveConfig(config_data)
{
  var json_data = ko.toJSON(config_data, null, 2);
  $.ajax({
    dataType: 'json',
    type: 'POST',
    url: '/robot/config/',
    data: { config_data: json_data },
    success: function(data){
      if (!data.success) {
        showMainError(data.message);
      } else {
        return data.config;
      }
    }
  });
}

function robotSendEmotionRPhi(r, phi, time)
{
  // time: -1 for default smooth transition time
  $.ajax({
    dataType: 'json',
    type: 'POST',
    url: '/robot/emotion/',
    data: {'r': r, 'phi': phi, 'time': time},
    success: function(data){
      if (!data.success) {
        showMainError(data.message);
      }
    }
  });
}

function robotSendDOF(moduleName, dofName, dofValue)
{
  $.ajax({
    dataType: 'json',
    type: 'POST',
    url: '/robot/dof/',
    data: {'module_name': moduleName, 'dof_name': dofName, 'value': dofValue},
    success: function(data){
      if (!data.success) {
        showMainError(data.message);
      }
    }
  });
}

function robotSendReceiveAllDOF(dofData)
{
  if (dofData == undefined)
  {
    $.ajax({
      dataType: 'json',
      type: 'POST',
      url: '/robot/dofs/',
      success: function(data){
        if (!data.success) {
          showMainError(data.message);
        } else {
          return data.dofs;
        }
      }
    });
    return;
  }
  var json_data = ko.toJSON(dofData, null, 2);
  $.ajax({
    dataType: 'json',
    type: 'POST',
    url: '/robot/dofs/',
    data: { dofdata: json_data },
    success: function(data){
      if (!data.success) {
        showMainError(data.message);
      } else {
        return data.dofs;
      }
    }
  });
}

function robotSendServo(pin, value)
{
  $.ajax({
    dataType: 'json',
    type: 'POST',
    url: '/robot/servo/',
    data: {'pin_number': pin, 'value': value},
    success: function(data){
      if (!data.success) {
        showMainError(data.message);
      }
    }
  });
}

function robotSendTTS(text)
{
  $.ajax({
    dataType: "json",
    type: "GET",
    url: "/robot/tts/",
    data: {t: text},
    success: function(data){
      if (!data.success) {
        showMainError(data.message);
      }
    }
  });
}

function robotSendSound(soundName)
{
  $.ajax({
    dataType: "json",
    type: "GET",
    url: "/robot/sound/",
    data: {s: soundName},
    success: function(data){
      if(data.status == "error"){
        showMainError(data.message);
      }

    }
  });
}

function robotSendStop()
{
  $.ajax({
    dataType: "json",
    type: "GET",
    url: "/robot/stop/",
    success: function(data){
      if(data.status == "error"){
        showMainError(data.message);
      }

    }
  });
}

// -------------------------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------------------------

$(document).foundation();
