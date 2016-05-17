
var scriptname = null;
var isScriptModified = false;

$(document).ready(function(){

	$.ajax({
		dataType: "json",
		url: "servos/enable",
		success: function(data){
			if(data.status == "error"){
				addError(data.message);
			}
		}
	});

	ko.bindingHandlers.avatar = {
		update: function(element, valueAccessor, allBindings) {
			var value = valueAccessor();
			var valueUnwrapped = ko.unwrap(value);
			$(element).css("background", "url('static/avatars/" + valueUnwrapped + "')")
		}
	};

	ko.bindingHandlers.outputswitch = {
		init: function(element, valueAccessor){
			$(element).change(function(){
				var value = valueAccessor();
				if( $(element).prop("checked") ){
					value("wav");
				}else{
					value("tts");
				}
			});
		},
		update: function(element, valueAccessor, allBindings) {
			var value = valueAccessor();
			var valueUnwrapped = ko.unwrap(value);
			$(element).prop("checked", valueUnwrapped == "tts" ? false : true);
		}
	};

	var switchID = 0; // Variable to generate unique IDs for toggle switches

	// Here's my data model
	var VoiceLine = function(emotion, output, tts, wav){
		var self = this;

		self.emotion = ko.observable(emotion || emotions_data[0]);

		self.output = ko.observable(output || "tts");
		self.tts = ko.observable(tts || "");
		self.wav = ko.observable(wav || sounds_data[0]);

		self.isPlaying = ko.observable(false);
		self.hasPlayed = ko.observable(false);

		self.switchID = "output-switch-" + switchID++;

		self.contentPreview = ko.pureComputed(function(){
			if(self.output() == "tts"){
				// Generate tts preview html
				return "<span class='fa fa-comment'></span> " + self.tts();
			}else{
				// Generate wav preview html
				return "<span class='fa fa-music'></span> " + self.wav();
			}
		});

		self.avatar = ko.pureComputed(function(){
			return self.emotion().image;
		});

		self.toggleOutput = function(){
			if(this.output() == "tts"){
				this.output("wav");
			}else{
				this.output("tts");
			}
		};

		self.pressPlay = function(){
			// if(self.isPlaying()){
			// 	self.isPlaying(false);
			// 	self.hasPlayed(true);
			// }else{
			$.ajax({
				dataType: "json",
				data: {"phi": self.emotion().phi, "r": self.emotion().r},
				type: "POST",
				url: "setemotion",
				success: function(data){
					if(data.status == "error"){
						addError(data.message);
					}
				}
			});
			if (self.emotion().eyes){
				if (self.emotion().eyes.left){
					if (self.emotion().eyes.left.lid){
						$.ajax({
							dataType: "json",
							data: {"left_lid": self.emotion().eyes.left.lid},
							type: "POST",
							url: "eye",
							success: function(data){
								if(data.status == "error"){
									addError(data.message);
								}
							}
						});
					}
				}
				if (self.emotion().eyes.right){
					if (self.emotion().eyes.right.lid){
						$.ajax({
							dataType: "json",
							data: {"right_lid": self.emotion().eyes.right.lid},
							type: "POST",
							url: "eye",
							success: function(data){
								if(data.status == "error"){
									addError(data.message);
								}
							}
						});
					}
				}
			}
			if (self.emotion().eyebrows){
				if (self.emotion().eyebrows.left){
					if (self.emotion().eyebrows.left.inner && self.emotion().eyebrows.left.outer){
						$.ajax({
							dataType: "json",
							data: {"left_inner": self.emotion().eyebrows.left.inner, "left_outer": self.emotion().eyebrows.left.outer},
							type: "POST",
							url: "eyebrow",
							success: function(data){
								if(data.status == "error"){
									addError(data.message);
								}
							}
						});
					}
				}
				if (self.emotion().eyebrows.right){
					if (self.emotion().eyebrows.right.inner && self.emotion().eyebrows.right.outer){
						$.ajax({
							dataType: "json",
							data: {"right_inner": self.emotion().eyebrows.right.inner, "right_outer": self.emotion().eyebrows.right.outer},
							type: "POST",
							url: "eyebrow",
							success: function(data){
								if(data.status == "error"){
									addError(data.message);
								}
							}
						});
					}
				}
			}
			if(this.output() == "tts"){
				$.ajax({
					dataType: "json",
					type: "GET",
					url: "saytts",
					data: {text: self.tts()}
				});
			}else{
				$.ajax({
					dataType: "json",
					type: "GET",
					url: "play/" + self.wav(),
					success: function(data){
						if(data.status == "error"){
							addError(data.message);
						}
					}
				});
			}
			self.isPlaying(true)
			// }
		};

		self.pickEmotion = function(){
			if(model.fileIsLocked()){
				return;
			}

			model.selectedVoiceLine(self);
			$("#PickEmotionModal").foundation("reveal", "open");
		};
	}

	var SocialScriptModel = function(){
		var self = this;

		self.fileIsLocked = ko.observable(false);
		self.fileIsModified = ko.observable(false);
		self.fileName = ko.observable("Untitled");
		self.fileStatus = ko.observable("Editing");

		self.sounds = sounds_data;
		self.emotions = emotions_data;

		self.selectedVoiceLine = ko.observable();

		self.voiceLines = ko.observableArray();
		self.init = function(){
			self.voiceLines.removeAll();
			self.voiceLines.push(new VoiceLine(self.emotions[0], "tts", "", ""));
		};
		self.init();

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

		self.addLine = function(){
			self.voiceLines.push( new VoiceLine(self.emotions[0], "tts", "", "") );
      window.scrollTo(0, document.body.scrollHeight);
		};

		self.removeLine = function(line){
			self.voiceLines.remove(line);
		};

		self.openFile = function(){
			$("#FilesModalSpinner").removeClass("hide");
			$("#FilesModalFilelist").html("");
			$("#FilesModalFilelist").load("filelist", function(){
				$("#FilesModalSpinner").addClass("hide");

				// Delete and Open button events need to be rebound here
				// because filelist is loaded via AJAX
				$(".btnDeleteFile").off("click");
				$(".btnDeleteFile").on("click", function(){
					filename = $(this).closest("div.file").data("scriptfile");
					$("#ConfirmDeleteModal").foundation("reveal", "open");
				});

				$(".btnOpenFile").off("click");
				$(".btnOpenFile").on("click", function(){
					filename = $(this).closest("div.file").data("scriptfile");

					var do_load = function(){
						$.ajax({
							url: "scripts/" + filename,
							dataType: "text",
							cache: false,
							success: function(data){
								// Load script
								self.voiceLines.removeAll();

								var dataobj = JSON.parse(data);
								//alert(dataobj.voice_lines[0].output.data);
								$.each(dataobj.voice_lines, function(idx, line){
									var emo = self.emotions[0];
									$.each(self.emotions, function(idx, emot){
										if(emot.name == line.emotion){
											emo = emot;
										}
									});

									if(line.output.type == "tts"){
										self.voiceLines.push(new VoiceLine(emo, line.output.type, line.output.data, ""));
									}else{
										self.voiceLines.push(new VoiceLine(emo, line.output.type, "", line.output.data));
									}
								});

								// Update filename and asterisk
								var filename_no_ext = filename;
								if(filename_no_ext.slice(-4) == ".soc" || filename_no_ext.slice(-4) == ".SOC"){
									filename_no_ext = filename_no_ext.slice(0, -4);
								}
								$(".filebox .filename").text(filename_no_ext);
								$(".filebox .fa-asterisk").addClass("hide");
								isScriptModified = false;
								scriptname = filename;

								self.lockFile();
								$("#FilesModal").foundation("reveal", "close");
							}
						});
					}

					if(isScriptModified){
						$("#btnConfirmLoad").off("click");
						$("#btnConfirmLoad").on("click", do_load);
						$("#ConfirmLoadModal").foundation("reveal", "open");
					}else{
						do_load();
					}

				});
			});

			$("#FilesModal").foundation("reveal", "open");
		};

		self.newFile = function(){
			// if(isScriptModified){
			$("#ConfirmNewModal").foundation("reveal", "open");
			// }else{
			// 	self.createNewFile();
			// }
		};

		self.createNewFile = function(){
			// if(scriptname != null){
			scriptname = null;

			self.init();

			$(".filebox .filename").html("Untitled");
			$(".filebox .fa-asterisk").addClass("hide");

			self.unlockFile();

			$("#ConfirmNewModal").foundation("reveal", "close");
			// }
		};

		self.deleteFile = function(){
			$.ajax({
				dataType: "json",
				type: "POST",
				url: "delete/" + filename,
				success: function(data){
					$("#ConfirmDeleteModal").foundation("reveal", "close");
					if(data.status == "error"){
						addError(data.message);
					}else{
						addMessage(data.message);
					}
				}
			});
		};

		self.saveFile = function(){
			if(scriptname == null){
				// Untitled script
				$("#txtFilename").val("");
				$("#SaveAsModal small.error").addClass("hide");
				$("#SaveAsModal").foundation("reveal", "open");
			}else{
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
				var json_data = ko.toJSON(file_data, null, 2);

				$.ajax({
					dataType: "json",
					data: {
						file: json_data,
						filename: scriptname,
						overwrite: 1
					},
					type: "POST",
					url: "save",
					success: function(data){
						if(data.status == "error"){
							addError(data.message);
						}else if(data.status == "success"){
							scriptname = data.filename;
							isScriptModified = false;

							var filename_no_ext = data.filename;
							if(filename_no_ext.slice(-4) == ".soc" || filename_no_ext.slice(-4) == ".SOC"){
								filename_no_ext = filename_no_ext.slice(0, -4);
							}

							$(".filebox .fa-asterisk").addClass("hide");
							$(".filebox .filename").html(filename_no_ext);
						}
					}
				});
				//alert(json_data);
			}
		};

		self.saveFileAs = function(){
			var filename = $("#txtFilename").val();

			$("#SaveAsModal small.error").addClass("hide");

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
			var json_data = ko.toJSON(file_data, null, 2);

			$.ajax({
				dataType: "json",
				data: {
					file: json_data,
					filename: filename,
					overwrite: 0
				},
				type: "POST",
				url: "save",
				success: function(data){
					if(data.status == "error"){
						$("#SaveAsModal small.error").html(data.message).removeClass("hide");
					}else if(data.status == "success"){
						scriptname = data.filename;
						isScriptModified = false;

						var filename_no_ext = data.filename;
						if(filename_no_ext.slice(-4) == ".soc" || filename_no_ext.slice(-4) == ".SOC"){
							filename_no_ext = filename_no_ext.slice(0, -4);
						}

						$(".filebox .fa-asterisk").addClass("hide");
						$(".filebox .filename").html(filename_no_ext);

						$("#SaveAsModal").foundation("reveal", "close");
					}
				}
			});
			return 0;
		};

		self.changeEmotion = function(emotion){
			self.selectedVoiceLine().emotion(emotion);
			$("#PickEmotionModal").foundation("reveal", "close");
		};
	};
	// This makes Knockout get to work
	var model = new SocialScriptModel();
	ko.applyBindings(model);
});
