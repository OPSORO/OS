
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
	var VoiceLine = function(emotion, output, tts, wav, picture, url, lang){
		var self = this;

		self.emotion = ko.observable(emotion || emotions_data[0]);

		self.output = ko.observable(output || "tts");
		self.tts = ko.observable(tts || "");
		self.wav = ko.observable(wav || sounds_data[0]);
		self.picture = ko.observable(picture || "");

		self.isPlaying = ko.observable(false);
		self.hasPlayed = ko.observable(false);

		self.url = ko.observable(url || "")
		self.lang = ko.observable(lang || "");

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
				if(this.output() == "tts"){
					robotSendTTSLang(self.tts, self.lang);
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

	var SocialScriptModel = function(){
		var self = this;

		self.fileIsLocked = ko.observable(true);
		self.fileIsModified = ko.observable(false);
		// self.fileName = ko.observable("");
		self.fileStatus = ko.observable("");
		self.fileExtension = ko.observable(".soc");

		self.sounds = sounds_data;
		self.emotions = emotions_data;

		self.selectedVoiceLine = ko.observable();

		self.voiceLines = ko.observableArray();
		self.fixedVoiceLine = ko.observable();
		self.fixedAvatars = ko.observableArray();

		$.each(self.emotions, function(idx, emot){
			self.fixedAvatars.push(new VoiceLine(emot, "tts", "", ""));
		});
		self.fixedVoiceLine = new VoiceLine(self.emotions[0], "tts", "", "");

		self.newFileData = function(){
			self.voiceLines.removeAll();
			self.unlockFile();
			self.fileIsModified(false);
		};

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

		self.loadFileData = function(data){
			if (data == undefined) {
				return;
			}
			// Load script
			self.voiceLines.removeAll();

			var dataobj = JSON.parse(data);

			$.each(dataobj.voice_lines, function(idx, line){
				var emo = self.emotions[0];
				$.each(self.emotions, function(idx, emot){
					if(emot.name.toLowerCase() == line.emotion.toLowerCase()){
						emo = emot;
					}
				});
				if(line.output.type == "tts"){
					self.voiceLines.push(new VoiceLine(emo, line.output.type, line.output.data, ""));
				}else{
					self.voiceLines.push(new VoiceLine(emo, line.output.type, "", line.output.data));
				}
			});
			// // Update filename and asterisk
			// var filename_no_ext = filename;
			// if(filename_no_ext.toLowerCase().slice(-4) == self.fileExtension()){
			// 	filename_no_ext = filename_no_ext.slice(0, -4);
			// }
			// self.fileName(filename_no_ext);
			self.fileIsModified(false);
			self.lockFile();
			return true;
		};

		self.saveFileData = function(){
			var file_data = {voice_lines: []};
			$.each(self.voiceLines(), function(idx, item){
				var line = {};
				line.emotion = item.emotion().name;
				line.output = {};
				if(item.output() == "tts"){
					line.output.type = "tts";
					line.output.data = item.tts();
				}else if(item.output() == "wav"){
					line.output.type = "wav";
					line.output.data = item.wav();
				}else{
					line.output.type = "tts";
					line.output.data = "";
				}
				file_data.voice_lines.push(line);
			});
			//console.log(file_data);
			self.fileIsModified(false);
			return ko.toJSON(file_data, null, 2);
		};

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
		self.index_voiceLine = ko.observable(0) // made observable to toggle button layout

		self.addTweetLine = function(data, picture, url, lang){
			self.fileIsModified(true);
			self.voiceLines.unshift( new VoiceLine(self.emotions[0], "tts", data, "", picture, url, lang) ); // unshift to push to first index of arr
		}

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

				$.post('/apps/sociono/', { action: 'startTweepy', data: socialID.value }, function(resp) {
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
			self.index_voiceLine(1); // set on null on initialize (reset)
			self.autoLoopTweepyNext();
		}

		self.autoLoopTweepyStop = function() {
			// post to stop sound
			console.log("Stop Auto Loop!");
			console.log(self.index_voiceLine());
		 	//self.selectedVoiceLine().isPlaying(false);
		 	//self.selectedVoiceLine().hasPlayed(true);
		 	$.post('/apps/sociono/', { action: 'autoLoopTweepyStop' }, function(resp) {
				console.log("Stopping Robot?");
				self.index_voiceLine(0) // set to null to reset
			});
		}

		self.autoLoopTweepyNext = function() {
			self.selectedVoiceLine(self.voiceLines()[self.index_voiceLine() - 1]); // starting at 1 so -1
			self.selectedVoiceLine().pressPlay();

			$.post('/apps/sociono/', { action: 'autoLoopTweepyNext' }, function(resp) {
				console.log("Playing Next Sound");
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
					self.addTweetLine(data["text"]["filtered"], data["user"]["profile_picture"], "https://twitter.com/" + data['user']['username'], data['text']['lang']);
					break;
				case "test":
					console.log(data)
			}
		};

		// Enter functionaliteit
		$(document).keyup(function (e) {
		    if ($(".socialID:focus") && (e.keyCode === 13)) {
				self.toggleTweepy();
		    }
		});


	};

	function robotSendTTSLang(text, lang){
		$.post('/apps/sociono/', { 'action': 'playTweet', 'text': text, 'lang': lang}, function(resp) {
			console.log("sound post done");
		});
	}

	// This makes Knockout get to work
	var model = new SocialScriptModel();
	ko.applyBindings(model);
	model.fileIsModified(false);

	//config_file_operations("", model.fileExtension(), model.saveFileData, model.loadFileData, model.newFileData);

});
