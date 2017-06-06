(function BanManager(){
		var self = this;

		self.templateBan = 'blacklistTemplate';

		self.phoneBan = ko.observable();

		self.bans = ko.observableArray();

		self.addBanItem = function(){
			self.bans.push(new Ban( self.phoneBan()));
		};

		self.removeBanItem = function(item){
			self.bans.remove(item);
		};

		self.loadbans = function(){
			// haven't tested, but probably won't work. I think you'd have to convert your JSON to observables
			self.bans = localStorage.getItem("stored_contacts");
		};

		self.saveBan = function(){
	    console.log('savingBan');
			self.addBanItem();
			localStorage.setItem("stored_bans", ko.toJSON(self.bans()));
			// na python
		};

		//	ko.cleanNode(self.templateName);
		ko.applyBindings(self.templateBan);

})();

function Ban(phoneBan){
	var self = this;

	self.phoneban = ko.observable(phoneBan);
}
