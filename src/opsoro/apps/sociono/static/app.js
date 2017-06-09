$(document).ready(function(){
	ko.bindingHandlers.avatar = {
		update: function(element, valueAccessor, allBindings) {
			var value = valueAccessor();
			var valueUnwrapped = ko.unwrap(value);
			$(element).css("background-image", "url('static/avatars/" + valueUnwrapped + "')")
		}
	};


	var searchField = "";

	// Here's my data model
	var VoiceLine = function(emotion, output, tts, wav, tweepyData){
		var self = this;

		self.emotion = ko.observable(emotion || emotions_data[0]);

		self.output = ko.observable(output || "tts");

		self.wav = ko.observable(wav || sounds_data[0]);

		self.isPlaying = ko.observable(false);
		self.hasPlayed = ko.observable(false);

		self.tweepyData = ko.observable(tweepyData || "")

		// If Data received from tweepy through addTweetLine(data)
		if (tweepyData) {
			self.picture = ko.observable(tweepyData["user"]["profile_picture"] || "");
			self.tts = ko.observable(tweepyData["text"]["original"] || "");
			self.url = ko.observable("https://twitter.com/" + tweepyData["user"]["username"] || "")
			self.lang = ko.observable(tweepyData["text"]["lang"] || "");
			self.emoticons = ko.observable(tweepyData["text"]["emoticon"] || "")
			console.log(self.emoticons())
		}

		self.contentPreview = ko.pureComputed(function(){
			if(self.output() == "tts"){
				// Generate tts preview html
				return "<span class='fa fa-comment'></span> " + self.tts();
			}else{
				// Generate wav preview html
				return "<span class='fa fa-music'></span> " + self.wav();
			}
		});

		self.emoji = ko.pureComputed(function(){
			return self.emotion().filename;
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
				
				if (self.emotion().poly){
					robotSendEmotionRPhi(1.0, self.emotion().poly * 18, -1);
				}
				if (self.emotion().dofs){
					robotSendReceiveAllDOF(self.emotion().dofs);
				}
				console.log(self.tts())
				console.log(self.lang())
				console.log(tweepyData)
				if(this.output() == "tts" && tweepyData){
					model.robotSendTTSLang(self.tweepyData());
				}else{
					robotSendSound(self.wav());
				}
				self.isPlaying(true);
			}
		};

		self.pickEmotion = function(){
			if(model.fileIsLocked()){
				return;
			}

			model.selectedVoiceLine(self);
			$("#PickEmotionModal").foundation("open");
		};
	};

	function robotSendTTSLang(text, lang){
		$.post('/apps/sociono/', { 'action': 'playTweet', 'text': text, 'lang': lang}, function(resp) {
			console.log("sound post done");
		});
	}


	var SocialScriptModel = function(){
		var self = this;

		self.fileIsLocked = ko.observable(true);
		self.fileIsModified = ko.observable(false);
		// self.fileName = ko.observable("");
		self.fileStatus = ko.observable("");
		self.fileExtension = ko.observable(".soc");

		self.sounds = sounds_data;
		self.emotions = emotions_data;

		console.log(self.emotions)

		self.selectedVoiceLine = ko.observable();

		self.voiceLines = ko.observableArray();
		self.fixedVoiceLine = ko.observable();
		self.fixedAvatars = ko.observableArray();

		self.fixedVoiceLine = new VoiceLine(self.emotions[0], "tts", "", "");


		self.toggleLocked = function(){
			if (self.fileIsLocked()) {
				self.unlockFile();
			}
			else {
				self.lockFile();
			}
		};

		self.lockFile = function(){
			self.fileIsLocked(true);
			self.fileStatus("Locked")
		};
		self.unlockFile = function(){
			self.fileIsLocked(false);
			self.fileStatus("Editing")
		};


		self.removeLine = function(line){
			self.fileIsModified(true);
			self.voiceLines.remove(line);
		};

		self.lockFile(); // lock the file so we get the correct lay-out (locked lay-out)


		self.changeEmotion = function(emotion){
			self.fileIsModified(true);
			self.selectedVoiceLine().emotion(emotion);
			$("#PickEmotionModal").foundation("close");
		};

		self.changeFixedEmotion = function(emotion){
			self.fixedVoiceLine.emotion(emotion);
		};


		// Auguste Code

		// Observables
		self.socialID = ko.observable("");
		self.isStreaming = ko.observable(false);
		self.index_voiceLine = ko.observable(0);// made observable to toggle button layout
		self.autoRead = ko.observable(false);

		self.addTweetLine = function(data){
			self.fileIsModified(true);

			console.log(data.text.emoticon)

			self.voiceLines.unshift( new VoiceLine(self.emotions[0], "tts", "", "", data) ); // unshift to push to first index of arr
		};


		self.toggleTweepy = function() {
			if(!socialID.value){
				showMainWarning("Please enter a hashtag");
				return;
			}

			if(self.isStreaming()) { // stop tweety if button is clicked again
				self.stopTweepy();
			} else {
				if(socialID.value != searchField){
					searchField = socialID.value;
					self.voiceLines.removeAll();
				}

				$.post('/apps/sociono/', { action: 'startTweepy', data: JSON.stringify({ socialID: socialID.value, autoRead: self.autoRead() }) }, function(resp) {
					console.log("post done");
				});
			}
			self.isStreaming(!self.isStreaming());
		}

		self.stopTweepy = function() {
			$.post('/apps/sociono/', { action: 'stopTweepy' }, function(resp) { // message ... success functions?
				console.log("Stopping Tweepy Stream!")
			});
		}
		self.toggleAutoLoopTweepy = function() {
			if (self.index_voiceLine() > 0) {
				self.autoLoopTweepyStop();
			} else {
				self.autoLoopTweepyStart();
			}
		}

		self.autoLoopTweepyStart = function() {
			self.isStreaming(false); // set the streaming button back on "Start"
			self.index_voiceLine(1); // set on null on initialize (reset)
			self.autoLoopTweepyNext();
		}

		self.autoLoopTweepyNext = function() {
			self.selectedVoiceLine(self.voiceLines()[self.index_voiceLine() - 1]); // starting at 1 so -1
			self.selectedVoiceLine().pressPlay();
		
			$.post('/apps/sociono/', { action: 'autoLoopTweepyNext' }, function(resp) {
				console.log("Waiting for sound to stop!");
			});
		}

		self.autoLoopTweepyRun = function() {
			console.log("Finished playing: " + self.index_voiceLine() + " / " + self.voiceLines().length);

			self.index_voiceLine(self.index_voiceLine() + 1); // increment observable

			if (self.index_voiceLine() <= self.voiceLines().length) {
				self.autoLoopTweepyNext();
				console.log("Running Loop: Next");
			}
		}

		self.autoLoopTweepyStop = function() {
			// post to stop sound
			console.log("Stop Auto Loop!");
		 	
		 	$.post('/apps/sociono/', { action: 'autoLoopTweepyStop' }, function(resp) {
				console.log("Stopping AutoLoop & Reading");
				self.index_voiceLine(0) // set to null to reset
			});
		}

		// Setup websocket connection.
		app_socket_handler = function(data) {
      		switch (data.action) {
				case "autoLoopTweepyStop":
					if (self.selectedVoiceLine() != undefined) {
						self.selectedVoiceLine().isPlaying(false);
					 	self.selectedVoiceLine().hasPlayed(true);
					}
					robotSendStop();
					break;
				case "autoLoopTweepyNext":
					if (self.selectedVoiceLine() != undefined) {
						self.selectedVoiceLine().isPlaying(false);
					 	self.selectedVoiceLine().hasPlayed(true);

					 	self.autoLoopTweepyRun()
					}
					break;
				case "dataFromTweepy":
					self.addTweetLine(data);
					break;
			}
		};

		// Custom TTS Speak function
		self.robotSendTTSLang = function robotSendTTSLang(tweepyData) {
			$.post('/apps/sociono/', { action: 'playTweet', data: JSON.stringify(tweepyData) }, function(resp) {
				console.log("sound post done");
			});
		};

		// Enter functionaliteit
		$(document).keyup(function (e) {
		    if ($(".socialID:focus") && (e.keyCode === 13)) {
				self.toggleTweepy();
		    }
		});
	};

	// This makes Knockout get to work
	var model = new SocialScriptModel();
	ko.applyBindings(model);
	model.fileIsModified(false);

	//config_file_operations("", model.fileExtension(), model.saveFileData, model.loadFileData, model.newFileData);

});
