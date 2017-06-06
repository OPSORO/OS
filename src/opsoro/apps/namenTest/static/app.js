(function ContactManager(){
	var self = this;

	self.templateName = 'contactTemplate';

	self.conName = ko.observable();
	self.phone = ko.observable();

	self.contacts = ko.observableArray();

	self.addItem = function(){
		self.contacts.push(new Contact(self.conName(), self.phone(), self.email(), self.address()));
	};

	self.removeItem = function(item){
		self.contacts.remove(item);
	};

	self.load = function(){
		// haven't tested, but probably won't work. I think you'd have to convert your JSON to observables
		self.contacts = localStorage.getItem("stored_contacts");
	};

	self.save = function(){
        console.log('saving');
		self.addItem();
		localStorage.setItem("stored_contacts", ko.toJSON(self.contacts()));
	};

	ko.applyBindings(self.templateName);


	self.contacts = 'contacts';

  self.personName = ko.observable();
  self.personNumber = ko.observable();

  self.persons = ko.observableArray();

  self.addItem = function(){
		self.persons.push(new Contact(self.personName(), self.personNumber()));
	};

	self.removeItem = function(item){
		self.persons.remove(item);
	};

	self.load = function(){
		// haven't tested, but probably won't work. I think you'd have to convert your JSON to observables
		self.persons = localStorage.getItem("stored_contacts");
	};

	self.save = function(){
        console.log('saving');
		self.addItem();
		localStorage.setItem("stored_contacts", ko.toJSON(self.contacts()));
	};

	ko.applyBindings(self.contacts);





})();

function Contact(personName,personNumber){
	var self = this;

	self.personName = ko.observable(personName);
	self.personNumber = ko.observable(personNumber);

}
