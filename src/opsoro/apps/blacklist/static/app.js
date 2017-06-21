(function BlacklistManager(){
		var self = this;
		GlobalDataJSON = [];

		self.templateBan = 'blacklistTemplate';

		self.wordBan = ko.observable();
		self.replacedWord = ko.observable();
		self.bans = ko.observableArray();


		// var inputs = document.querySelectorAll( '.inputfile' );
		// 	Array.prototype.forEach.call( inputs, function( input )
		// 	{
		// 		var label	 = input.nextElementSibling,
		// 			labelVal = label.innerHTML;
		//
		// 		input.addEventListener( 'change', function( e )
		// 		{
		// 			var fileName = '';
		// 			fileName = e.target.value.split( '\\' ).pop();
		//
		// 			if( fileName )
		// 				label.querySelector( 'span' ).innerHTML = fileName;
		// 			else
		// 				label.innerHTML = labelVal;
		// 		});
		//
		// 		// Firefox bug fix
		// 		input.addEventListener( 'focus', function(){ input.classList.add( 'has-focus' ); });
		// 		input.addEventListener( 'blur', function(){ input.classList.remove( 'has-focus' ); });
		// 	});
		//
		// self.uploadFile = function(){
		//
		// 	console.log('uploadFile');
		// 	// var newitems = [];
		// 	// $.grep(bans(), function(e){
		// 	// 	var data_line = {
		// 	// 		banWord : e.wordBan(),
		// 	// 		replacedWord : e.replacedWord()
		// 	// 	};
		// 	// 	newitems.push(data_line);
		// 	// });
		// 	//
		// 	// GlobalDataJSON = newitems;
		// 	// newitems = JSON.stringify(newitems);
		// 	// $.post('/apps/blacklist/signblacklist', { banlist: newitems }, function(resp) {
		// 	//
		// 	// });
		// };
		//
		// self.saveFile = function(){
		//
		// 	console.log('savig saveFile');
		// 	// var newitems = [];
		// 	// $.grep(bans(), function(e){
		// 	// 	var data_line = {
		// 	// 		banWord : e.wordBan(),
		// 	// 		replacedWord : e.replacedWord()
		// 	// 	};
		// 	// 	newitems.push(data_line);
		// 	// });
		// 	//
		// 	// GlobalDataJSON = newitems;
		// 	// newitems = JSON.stringify(newitems);
		// 	// $.post('/apps/blacklist/signblacklist', { banlist: newitems }, function(resp) {
		// 	//
		// 	// });
		// };

		self.addBanItem = function(){
			self.bans.push(new Ban( self.wordBan(), self.replacedWord()));
			self.reset();
		};

		self.removeBanItem = function(item){

			self.bans.remove(item);

			var newitems = [];
			var items = GlobalDataJSON;
			var deletedItem = item.wordBan()
			var result = $.grep(items, function(e){
				if (e.banWord != deletedItem) {
					newitems.push(e)
				}
			});
			GlobalDataJSON = newitems;
			newitems = JSON.stringify(newitems);

			 $.post('/apps/blacklist/signblacklist', { banlist: newitems }, function(resp) {
			 	console.log('posted to python');
			 });
		};

		// de bestaande objecten inladen en i nde html steken
		self.loadBlacklist = function(){

			$.get('/apps/blacklist/getblacklist', function( data ) {
				if (data != "{}") {
					var json_data = data;
					GlobalDataJSON = json_data.banlist;
					 $.each(json_data.banlist, function(idx, line){
							self.wordBan(line.banWord);
							self.replacedWord(line.replacedWord);
							self.bans.push(new Ban( self.wordBan(), self.replacedWord()));
							self.reset();
					 });
				}
			});
		};


		// als er op de save knop geduwdt word et object opstlaan
	
		$('input[type=text]').on('keydown', function(e) {
		    if (e.which == 13) {
			self.saveBannedWord();
		    }
		});
		self.saveBannedWord = function(){
			if(self.wordBan() != ""){
				$( "#error_exists").empty();
				self.replacedWord("swear");

				var exists = false;
				var data_line = {
					banWord : self.wordBan(),
					replacedWord : self.replacedWord()
				};

				ko.toJSON(data_line);
				$.grep(GlobalDataJSON, function(e){
					if (JSON.stringify(e) == JSON.stringify(data_line)) {
						exists = true;
					}
				});
				if (!exists) {
					self.saveJson(data_line);
				}else{
					$("#error_exists").append("<br /><small>Word exists</small>");

				}
			}else{
				$("#error_exists").append("<br /><small>field is empty</small>");
			}
		};

		self.saveAll = function(){

			console.log('savig all');
			var newitems = [];
			$.grep(bans(), function(e){
				var data_line = {
					banWord : e.wordBan(),
					replacedWord : e.replacedWord()
				};
				newitems.push(data_line);
			});

			GlobalDataJSON = newitems;
			newitems = JSON.stringify(newitems);
			$.post('/apps/blacklist/signblacklist', { banlist: newitems }, function(resp) {

			});
		};

		// bedoeling op te slaan in de python
		self.saveJson = function(data_line){

			var dataJSON = GlobalDataJSON;
			dataJSON.push(data_line);
			dataJSON = JSON.stringify(dataJSON);
			$.post('/apps/blacklist/signblacklist', { banlist: dataJSON }, function(resp) {
			 	self.addBanItem();
			});
		};

		self.reset = function() {
			self.wordBan('');
			self.replacedWord('');
		};

		ko.applyBindings(self.templateBan);

})();

// data binden met de objecten
function Ban(wodBan, replacedWord){
	var self = this;

	self.wordBan = ko.observable(wodBan);
	self.replacedWord = ko.observable(replacedWord);
}

var FileModel= function (name, src) {
    var self = this;
    this.name = name;
    this.src= src ;
};
