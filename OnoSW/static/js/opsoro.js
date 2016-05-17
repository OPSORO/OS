

function showMainError(msg){
  $("#error_list").append("<div data-alert class=\"alert-box alert\">" + msg + "<a href=\"#\" class=\"close\">&times;</a></div>");
  $(document).foundation("alert", "reflow");
}
function showMainMessage(msg){
  $("#error_list").append("<div data-alert class=\"alert-box info\">" + msg + "<a href=\"#\" class=\"close\">&times;</a></div>");
  $(document).foundation("alert", "reflow");
}
