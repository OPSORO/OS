$(document).ready(function(){
  var viewModel = function() {
      console.log('test');
      $.getJSON( '/apps/telegram/getmessages', function( data ) {
      //console.log(data["messages"]);
      var jsondata = data["messages"];
      console.log(jsondata);
      for(index = 0; index<jsondata.length; ++ index){
        console.log(jsondata[index]);
        var message = jsondata[index]["message"];
        var firstname = jsondata[index]["first_name"];
        console.log(message);
        $('#messages').append('<p>' + message + '</p>');
      }
			//var json_data = JSON.parse(data);
      //globaljson = JSON.parse(json_data.messages)
      //for(var i in data)
      //console.log(json_data["message"]);
    })
    .error(function(error){
      console.log(error);

		});
    }



ko.applyBindings(viewModel);
})
