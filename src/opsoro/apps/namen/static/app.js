(function ContactManager(){
	var self = this;

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
		// haven't tested, but probably won't work. I think you'd have to convert your JSON to observables
		self.contacts = localStorage.getItem("stored_contacts");
	};

	self.save = function(){
        console.log('saving');
		self.addItem();
		localStorage.setItem("stored_contacts", ko.toJSON(self.contacts()));
		// na python
	};

	ko.applyBindings(self.templateName);


})();

function Contact(name,phone){
	var self = this;

	self.conName = ko.observable(name);
	self.phone = ko.observable(phone);
}
