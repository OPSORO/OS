$(document).ready(function(){
	ko.bindingHandlers.avatar = {
		update: function(element, valueAccessor, allBindings) {
			var value = valueAccessor();
			var valueUnwrapped = ko.unwrap(value);
			$(element).css("background-image", "url('static/avatars/" + valueUnwrapped + "')")
		}
	};


	var searchField = "";

	var sendPost = function(action, data){
		$.ajax({
			dataType: 'json',
			type: 'POST',
			url: '/apps/tweader/',
			data: {action: action, data: data },
			success: function(data){
				if (!data.success) {
					showMainError(data.message);
				} else {
					return data.config;
				}
			}
		});
	}

	function highlight_links(str) {
	    // force http: on www.
	    str = str.replace(/www\./g, "http://www.");
	    // eliminate duplicates after force
	    str = str.replace(/https:\/\/http:\/\/www\./g, "https://www.");
	    str = str.replace(/http:\/\/http:\/\/www\./g, "http://www.");
	    // Set the regex string
	    var regex = /(\b(https?|ftp|file|http):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
	    // Replace plain text links by hyperlinks
	    var replaced_text = str.replace(regex, "<a href='$1' class='contact-link' target='_blank'>$1</a>");

	    return replaced_text;
	}

	// Here's my data model
	var VoiceLine = function(tweepyData){
		var self = this;

		self.isPlaying = ko.observable(false);
		self.hasPlayed = ko.observable(false);

		self.tweepyData = ko.observable(tweepyData || "")

		// If Data received from tweepy through addTweetLine(data)
		if (tweepyData) {
			self.picture = ko.observable(tweepyData["user"]["profile_picture"] || "");
			self.tts = ko.observable(tweepyData['text']['original'] || "");
			self.tts(highlight_links(self.tts()));//make http, https, ... links clickable
			self.url = ko.observable("https://twitter.com/" + tweepyData["user"]["username"] || "")
			self.lang = ko.observable(tweepyData["text"]["lang"] || "");
			self.emoticons = ko.observable(tweepyData["text"]["emoticon"] || "")
		}

		self.contentPreview = ko.pureComputed(function(){
				return "<span class='fa fa-comment'></span> " + self.tts();
		});

		self.modified = function(){
			model.fileIsModified(true);
		}

		self.pressPlay = function(){
			if(self.isPlaying()){
				robotSendStop();
			 	self.isPlaying(false);
			 	self.hasPlayed(true);
			}else{
				if (model.selectedVoiceLine() != undefined) {
					model.selectedVoiceLine().isPlaying(false);
				}
				model.selectedVoiceLine(self);
				model.robotSendTTSLang(self.tweepyData());
				self.isPlaying(true);
			}
		};
	};

	var SocialScriptModel = function(){
		var self = this;

		self.selectedVoiceLine = ko.observable();
		self.voiceLines = ko.observableArray();

		// Auguste Code

		// Observables
		self.socialID = ko.observable("");
		self.isStreaming = ko.observable(false);// made observable to toggle button layout
		self.index_voiceLine = ko.observable(0);
		self.autoRead = ko.observable(false);
		self.autoLooping = ko.observable(false);

		//change autoread when streaming
		self.toggleAutoRead = function(){
			if(self.isStreaming()){
				//only send when streaming
				sendPost('toggleAutoRead', {});
			}
			self.autoRead(!self.autoRead());
		}

		self.addTweetLine = function(data){
			self.voiceLines.unshift(new VoiceLine(data)); // unshift to push to first index of arr
		};

		self.toggleTweepy = function() {
			if(self.isStreaming()) { // stop tweety if button is clicked again
				self.stopTweepy();
				self.isStreaming(!self.isStreaming());
				return;
			}
			if(!socialID.value){
				showMainWarning("Please enter a value");
				return;
			}
			if(socialID.value != searchField){
				searchField = socialID.value;
				self.voiceLines.removeAll();
			}
			if(self.autoLooping())  self.toggleAutoLoopTweepy();
			sendPost('startTweepy', JSON.stringify({socialID: socialID.value, autoRead: self.autoRead()}));
			self.isStreaming(!self.isStreaming()); //change streaming status

		}

		self.stopTweepy = function() {
			sendPost('stopTweepy', {})
		}

		self.toggleAutoLoopTweepy = function() {
			if (self.autoLooping()) {
				self.autoLoopTweepyStop();
			} else {
				self.autoLoopTweepyStart();
			}
		}

		self.autoLoopTweepyStart = function() {
			self.isStreaming(false); // set the streaming button back on "Start"
			self.autoLooping(true);
			self.index_voiceLine(1); // set on null on initialize (reset)
			self.autoLoopTweepyNext();
		}

		self.autoLoopTweepyNext = function() {
			self.selectedVoiceLine(self.voiceLines()[self.index_voiceLine() - 1]); // starting at 1 so -1
			self.selectedVoiceLine().pressPlay();
			console.log("hier stuurt hij bpost");
			sendPost('autoLoopTweepyNext', {});

		}

		self.autoLoopTweepyRun = function() {
			self.index_voiceLine(self.index_voiceLine() + 1); // increment observable
			if (self.index_voiceLine() <= self.voiceLines().length) {
				self.autoLoopTweepyNext();
			}
			else {
				self.index_voiceLine(1);
				self.autoLoopTweepyNext();
			}
		}

		self.autoLoopTweepyStop = function() {
			self.autoLooping(false);
			sendPost('autoLoopTweepyStop', {});
		}

		// Setup websocket connection.


		// Custom TTS Speak function
		self.robotSendTTSLang = function(tweepyData) {
			sendPost('playTweet', JSON.stringify(tweepyData));
		};


	};

	// This makes Knockout get to work
	var model = new SocialScriptModel();
	ko.applyBindings(model);

	// Enter functionaliteit
	$(document).keyup(function (e) {
			if ($(".socialID:focus") && (e.keyCode === 13)) {
			model.toggleTweepy();
			}
	});

	app_socket_handler = function(data) {
				switch (data.action) {
			case "autoLoopTweepyStop":
				if (model.selectedVoiceLine() != undefined) {
					model.selectedVoiceLine().isPlaying(false);
					model.selectedVoiceLine().hasPlayed(true);
				}
				robotSendStop();
				break;
			case "autoLoopTweepyNext":
				if (model.selectedVoiceLine() != undefined) {
					model.selectedVoiceLine().isPlaying(false);
					model.selectedVoiceLine().hasPlayed(true);

					model.autoLoopTweepyRun()
				}
				break;
			case "dataFromTweepy":
				model.addTweetLine(data);
				break;
		}
	};

});
$( window ).unload(function() {
  $.ajax({
    dataType: 'json',
    type: 'POST',
    url: '/apps/facebook_live/',
    data: {action: 'stopTweepy', data: {} },
    success: function(data){
      if (!data.success) {
        showMainError(data.message);
      } else {
        return "";
      }
    }
  });
  return "";
});
