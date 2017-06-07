(function ContactManager(){
	var self = this;

	var dummy = JSON.stringify({"contacts": [
      {
        "name": "Siel",
        "phone": "0456745678"
      },
      {
        "name": "Ellen",
        "phone": "0476446578"
      },
      {
        "name": "Poema",
        "phone": "0456873467"
      }
    ]});
		//console.log(dummy);

	self.templateName = 'contactTemplate';

	self.conName = ko.observable();
	self.phone = ko.observable();

	self.contacts = ko.observableArray();

	self.addItem = function(){
		self.contacts.push(new Contact(self.conName(), self.phone()));
	};

	self.removeItem = function(item){
		self.contacts.remove(item);
	};

	self.load = function(){

		var dataobj = JSON.parse(dummy);
		$.each(dataobj.contacts, function(idx, line){
		 	self.contacts.push(new Contact( line.name, line.phone ));

		 });
	};

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

	self.saveJson = function(data_line){

		// get data first
		var dataJSON = JSON.parse(dummy);
		dataJSON.contacts.push(ko.toJSON(data_line));

		$.ajax({
	    url: '/signcontacts',
	    dataType: 'json',
	    data: JSON.stringify(dataJSON),
	    type: 'POST',
	    success: function(response) {
	        console.log(response);
	    },
	    error: function(error) {
	        console.log(error);
	    }
		});

	};


		ko.applyBindings(self.templateName);
		//self.load();

})();

function Contact(name,phone){
	var self = this;

	self.conName = ko.observable(name);
	self.phone = ko.observable(phone);
}
