(function ContactManager(){
	var self = this;

	var GlobalDataJSON = [];
	self.templateName = 'contactTemplate';

	self.conName = ko.observable();
	self.phone = ko.observable();

	self.contacts = ko.observableArray();

	self.addItem = function(){
		self.contacts.push(new Contact(self.conName(), self.phone()));
	};

	self.removeItem = function(item){
		self.contacts.remove(item);

		console.log(item);
		console.log(self.conName.valueOf("Symbol(_latestValue)"));

		//delete GlobalDataJSON[item];
		//console.log(GlobalDataJSON);

		//deleten van item op naam
		// for (key in json) {
	  //   if (json.hasOwnProperty(key) && json[key] == 123) {
	  //       delete json[key];
	  //   }
		// }

		// var dataJSON = GlobalDataJSON;
		// dataJSON.push(item);
		// //console.log(dataJSON);
		// dataJSON = JSON.stringify(dataJSON);
		// console.log(dataJSON);
		//
		// $.post('/apps/contactlijst/signcontacts', { contacts: dataJSON }, function(resp) {
		// 	console.log('posted')
		// });
	};

	// json inladen en in de velden pushen
	self.load = function(){

		$.getJSON( '/apps/contactlijst/getcontacts', function( data ) {
			var json_data = JSON.parse(data);
			GlobalDataJSON = JSON.parse(json_data.contacts);
			 $.each(JSON.parse(json_data.contacts), function(idx, line){
			  	self.contacts.push(new Contact( line.name, line.phone ));
			 });
		});

	};

	//als er op de save button geklikt word en item laten toeveoegen
	self.save = function(){
  	// console.log('saving');
		self.addItem();
		var data_line = {
	    name : self.conName(),
	    phone : self.phone()
		};
		ko.toJSON(data_line);
		self.saveJson(data_line);
		// na python
	};

	// de json zelf opslaan in de json  en later doorsturen na de pytrhon
	self.saveJson = function(data_line){

		// get data first
		var dataJSON = GlobalDataJSON;
		dataJSON.push(data_line);
		//console.log(dataJSON);
		dataJSON = JSON.stringify(dataJSON);
		console.log(dataJSON);
		console.log(data_line);

		$.post('/apps/contactlijst/signcontacts', { contacts: dataJSON }, function(resp) {
			console.log('posted')
		});

	};


		ko.applyBindings(self.templateName);
		//self.load();

})();

// de zaken binden met de waardes
function Contact(name,phone){
	var self = this;

	self.conName = ko.observable(name);
	self.phone = ko.observable(phone);
}
