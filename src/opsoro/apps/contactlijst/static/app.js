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

		var newitems = [];
		var items = GlobalDataJSON;
		var deletedItem = {name: item.conName(), phone: item.phone()}
		var result = $.grep(items, function(e){
			if (JSON.stringify(e) != JSON.stringify(deletedItem)) {
				newitems.push(e)
			}
		});
		GlobalDataJSON = newitems;
		newitems = JSON.stringify(newitems);
		 $.post('/apps/contactlijst/signcontacts', { contacts: newitems }, function(resp) {
		 	console.log('posted');
		 });
	};

	// json inladen en in de velden pushen
	self.load = function(){

		$.getJSON( '/apps/contactlijst/getcontacts', function( data ) {
			var json_data = JSON.parse(data);
			GlobalDataJSON = JSON.parse(json_data.contacts);
			 $.each(JSON.parse(json_data.contacts), function(idx, line){
			  	//self.contacts.push(new Contact( line.name, line.phone ));
					self.conName = ko.observable(line.name);
					self.phone = ko.observable(line.phone);
					self.addItem();
			 });
		});

	};

	//als er op de save button geklikt word en item laten toeveoegen
	self.save = function(){

		var data_line = {
	    name : self.conName(),
	    phone : self.phone()
		};
		ko.toJSON(data_line);
		self.saveJson(data_line);
	};

	// de json zelf opslaan in de json  en later doorsturen na de pytrhon
	self.saveJson = function(data_line){

		var dataJSON = GlobalDataJSON;
		dataJSON.push(data_line);
		dataJSON = JSON.stringify(dataJSON);
		$.post('/apps/contactlijst/signcontacts', { contacts: dataJSON }, function(resp) {
			self.addItem();
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
