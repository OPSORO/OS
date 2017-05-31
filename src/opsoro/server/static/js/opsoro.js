function showMainError(msg){
  $('#errors').append("<div class='callout alert' data-closable>" + msg + "<button class='close-button' aria-label='Dismiss' type='button' data-close><span aria-hidden='true'>&times;</span></button></div>");
  $(document).foundation('reflow');
}
function showMainWarning(msg){
  $('#errors').append("<div class='callout warning' data-closable>" + msg + "<button class='close-button' aria-label='Dismiss' type='button' data-close><span aria-hidden='true'>&times;</span></button></div>");
  $(document).foundation('reflow');
}
function showMainMessage(msg){
  $('#errors').append("<div class='callout primary' data-closable>" + msg + "<button class='close-button' aria-label='Dismiss' type='button' data-close><span aria-hidden='true'>&times;</span></button></div>");
  $(document).foundation('reflow');
}
function showMainSuccess(msg){
  $('#errors').append("<div class='callout success' data-closable>" + msg + "<button class='close-button' aria-label='Dismiss' type='button' data-close><span aria-hidden='true'>&times;</span></button></div>");
  $(document).foundation('reflow');
}
var popup_classes;
function showPopup(sIcon, sTitle, sClass, sContent) {
  popup_classes = sClass;
  $('#popup').addClass(popup_classes);
  $('#popup .titlebar .titleicon span').addClass(sIcon);
  $('#popup .titlebar .title').html(sTitle);

  if (sContent != ''){
    $('#popup .content').html(sContent);
  }

  $('#popup .btnClose').off('click');
  $('#popup .btnClose').on('click', closePopup);

  // Open message popup
  $('#popup').foundation('open');

}
function closePopup() {
  $('#popup').foundation('close');

  // Clear text & icon
  $('#popup .titlebar .titleicon span').removeClass();
  $('#popup .titlebar .titleicon span').addClass('fa');
  $('#popup .titlebar .title').html('');
  $('#popup .content').html('');

  $('#popup').removeClass(popup_classes);
  $('#popup').addClass('reveal');
}
function showMessagePopup(sIcon, sTitle, sText, handlers) {
  $('#message_popup .titlebar .titleicon span').addClass(sIcon);
  $('#message_popup .titlebar .title').html(sTitle);
  $('#message_popup .content .text').html(sText);

  data = {};

  // Input enabling
  if (handlers.inputText != undefined){
    $('#message_popup .inputText').removeClass('hide');
    $('#message_popup .inputText').on('input', handlers.inputText);
  }

  // Button click handlers
  if (handlers.btnOk != undefined){
    $('#message_popup .btnOk').removeClass('hide');
    $('#message_popup .btnOk').on('click', handlers.btnOk);
  }
  if (handlers.btnYes != undefined){
    $('#message_popup .btnYes').removeClass('hide');
    $('#message_popup .btnYes').on('click', handlers.btnYes);
  }
  if (handlers.btnNo != undefined){
    $('#message_popup .btnNo').removeClass('hide');
    $('#message_popup .btnNo').on('click', handlers.btnNo);
  }
  if (handlers.btnSave != undefined){
    $('#message_popup .btnSave').removeClass('hide');
    $('#message_popup .btnSave').on('click', handlers.btnSave);
  }
  if (handlers.btnCancel != undefined){
    $('#message_popup .btnCancel').removeClass('hide');
    $('#message_popup .btnCancel').on('click', handlers.btnCancel);
  }

  $('#message_popup .btnClose').off('click');
  $('#message_popup .btnClose').on('click', closeMessagePopup);

  // Open message popup
  if (!$('#message_popup').hasClass('open')){
    $('#message_popup').foundation('open');
  }
}
function closeMessagePopup() {
  $('#message_popup').foundation('close');

  // Clear text & icon
  $('#message_popup .titlebar .titleicon span').removeClass();
  $('#message_popup .titlebar .titleicon span').addClass('fa');
  $('#message_popup .titlebar .title').html('');
  $('#message_popup .content .text').html('');

  // Clear inputs
  $('#message_popup .inputText').val('');

  // Hide inputs
  $('#message_popup .inputText').addClass('hide');

  // Hide buttons
  $('#message_popup .btnOk').addClass('hide');
  $('#message_popup .btnYes').addClass('hide');
  $('#message_popup .btnNo').addClass('hide');
  $('#message_popup .btnSave').addClass('hide');
  $('#message_popup .btnCancel').addClass('hide');

  // Remove click handlers
  $('#message_popup .btnOk').off('click');
  $('#message_popup .btnYes').off('click');
  $('#message_popup .btnNo').off('click');
  $('#message_popup .btnSave').off('click');
  $('#message_popup .btnCancel').off('click');
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
  conn = new SockJS('http://' + window.location.host + '/usersockjs');

  conn.onopen = function(){
    // $.ajax({
    //   url: '/appsockjstoken',
    //   cache: false
    // })
    // .done(function(data) {
    //   conn.send(JSON.stringify({action: 'authenticate', token: data}));
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
        case 'refresh':
          setTimeout(function() { location.reload(); }, 1000);
          break;
        case 'info':
          console.log(msg);
          break;
        case 'users':
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
    dataType: 'json',
    type: 'GET',
    url: '/robot/tts/',
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
    dataType: 'json',
    type: 'GET',
    url: '/robot/sound/',
    data: {s: soundName},
    success: function(data){
      if(data.status == 'error'){
        showMainError(data.message);
      }

    }
  });
}

function robotSendStop()
{
  $.ajax({
    dataType: 'json',
    type: 'GET',
    url: '/robot/stop/',
    success: function(data){
      if(data.status == 'error'){
        showMainError(data.message);
      }

    }
  });
}

// -------------------------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------------------------

function ClickToEdit(value, placeholder){
  var self = this;
  // Data
  self.value = ko.observable(value);
  self.editing = ko.observable(false);
  self.placeholder = placeholder || "empty";

  // Behaviors
  self.edit = function(){ self.editing(true) }

  self.displayValue = ko.pureComputed(function(){
      if(self.value() == ""){
            return "<i style='color: #888;'>" + self.placeholder +"</i>"
      }
      return self.value();
  }, self);

}
