

function showMainError(msg){
  $("#error_list").append("<div data-alert class=\"alert-box alert\">" + msg + "<a href=\"#\" class=\"close\">&times;</a></div>");
  $(document).foundation("alert", "reflow");
}
function showMainMessage(msg){
  $("#error_list").append("<div data-alert class=\"alert-box info\">" + msg + "<a href=\"#\" class=\"close\">&times;</a></div>");
  $(document).foundation("alert", "reflow");
}

function showPopup(sIcon, sTitle, sClass, sContent = "") {
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
