
$(document).ready(function(){
    var twee = ["blauw", "groen", "rood", "geel"];
    var kleuren = ["#00a8ec","#22b573","#df0024","#fcd016"];
    var antwoorden = [];
    var vraag = [];
    var score = 0;
    var niveau = 0;
    var text;
    var startOpnieuw = 0;
    var person = 0;
    var vraagNummer = 0;
    var wachtijd = 0;
    var keyAllowed = {};
    var d = new Date();
    var tijd = d.getTime();

    var b_test = "false";

    if(niveau == 0){
        wachtijd = 600;
    }
    if(niveau == 1){
        wachtijd = 1200;
    }
    if(niveau == 2){
        wachtijd = 1800;
    }
    if(niveau == 3){
        wachtijd = 2400;
    }
    if(niveau == 4){
        wachtijd = 3000;
    }
    if(niveau == 5){
        wachtijd = 3600;
    }
    if(niveau == 6){
        wachtijd = 4200;
    }
    if(niveau == 7){
        wachtijd = 4800;
    }
    if(niveau == 8){
        wachtijd = 5400;
    }

    $(".button.start").click(function(){
        if(startOpnieuw == 1){
            window.location.reload();
        }
        start();
    });

    $("#verander").hide();

    $("#invoerKnop").click(function(){
        console.log("hoi");
        $(".uitleg").hide()
        $(".levelselect").show();
        $(".back").show();
        $("#verander").show();
        $("#invoerKnop").hide();
        $("#naam").prop('disabled', true);
        person = $( "#naam" ).val();
        //$("#invoerKnop").text("verander");
        //if(startOpnieuw == 1){
        //    window.location.reload();
        //}
        start();
        vraagNummer = 0;

    });

    $("#verander").click(function(){
        $("#naam").prop('disabled', false);
        $("#verander").hide();
        $("#invoerKnop").show();
    });

    $('#naam').change(function() {
        $('#invoerKnop').prop('disabled', false);
    });

    $.ajax({
        dataType: "json",
        url: "servos/enable",
        success: function(data){
            if(data.status == "error"){
                addError(data.message);
            }
        }
    });

    $.ajax({
        dataType: "json",
        data: {"phi": 0 , "r": 1},
        type: "POST",
        url: "setemotion",
        success: function(data){
            if(data.status == "error"){
                addError(data.message);
            }
        }
    });

    function start() {
        for (i = 0; i < niveau + 2; i++) {

            var index = Math.floor(Math.random() * 4);
            var rand = twee[index];
            var randColor = kleuren[rand];
            console.log("rand=" +rand);
            vraag.push(rand);
            if((niveau+2) == vraag.length ){
                
                $(".question").html(vraag.join(' '));
                var vraagske = document.getElementsByClassName('question');
                console.log("kleuren =" +kleuren[0]);

                console.log("vraag: " + vraag);

                if(vraagNummer !== 0){

                    setTimeout(function() {

                        $.ajax({
                            dataType: "json",
                            data: {"phi": 0, "r": 1},
                            type: "POST",
                            url: "setemotion",
                            success: function(data){
                                if(data.status == "error"){
                                    addError(data.message);
                                }
                            }
                        });

                    },0);


                    setTimeout(function() {
                        $.ajax({
                            dataType: "json",
                            type: "GET",
                            url: "play/smb_coin.wav",
                            success: function(data){
                                if(data.status == "error"){
                                    addError(data.message);
                                }
                            }
                        });
                    },200);
                }

                setTimeout(function() {

                $.ajax({
                    dataType: "json",
                    type: "GET",
                    url: "play/"+vraag[0]+".wav",
                    success: function(data){
                        if(data.status == "error"){
                            addError(data.message);
                        }
                    }
                });

                },900);

                setTimeout(function() {

                    $.ajax({
                        dataType: "json",
                        type: "GET",
                        url: "play/"+vraag[1]+".wav",
                        success: function(data){
                            if(data.status == "error"){
                                addError(data.message);
                            }
                        }
                    });

                },900+600);

                if(vraag[2] != null){

                    setTimeout(function() {
                        $.ajax({
                            dataType: "json",
                            type: "GET",
                            url: "play/"+vraag[2]+".wav",
                            success: function(data){
                                if(data.status == "error"){
                                    addError(data.message);
                                }
                            }
                        });

                    },2100);
                }


                if(vraag[3] != null){

                    setTimeout(function() {
                        $.ajax({
                            dataType: "json",
                            type: "GET",
                            url: "play/"+vraag[3]+".wav",
                            success: function(data){
                                if(data.status == "error"){
                                    addError(data.message);
                                }
                            }
                        });

                    },2700);

                }


                if(vraag[4] != null){
                    setTimeout(function() {
                        $.ajax({
                            dataType: "json",
                            type: "GET",
                            url: "play/"+vraag[4]+".wav",
                            success: function(data){
                                if(data.status == "error"){
                                    addError(data.message);
                                }
                            }
                        });
                    },3300);
                }


                if(vraag[5] != null){
                    setTimeout(function() {
                        $.ajax({
                            dataType: "json",
                            type: "GET",
                            url: "play/"+vraag[5]+".wav",
                            success: function(data){
                                if(data.status == "error"){
                                    addError(data.message);
                                }
                            }
                        });
                    },3900);
                }


                if(vraag[6] != null){
                    setTimeout(function() {
                        $.ajax({
                            dataType: "json",
                            type: "GET",
                            url: "play/"+vraag[6]+".wav",
                            success: function(data){
                                if(data.status == "error"){
                                    addError(data.message);
                                }
                            }
                        });
                    },4500);
                }


                if(vraag[7] != null){
                    setTimeout(function() {
                        $.ajax({
                            dataType: "json",
                            type: "GET",
                            url: "play/"+vraag[7]+".wav",
                            success: function(data){
                                if(data.status == "error"){
                                    addError(data.message);
                                }
                            }
                        });
                    },5100);
                }


                if(vraag[8] != null){
                    setTimeout(function() {
                        $.ajax({
                            dataType: "json",
                            type: "GET",
                            url: "play/"+vraag[8]+".wav",
                            success: function(data){
                                if(data.status == "error"){
                                    addError(data.message);
                                }
                            }
                        });
                    },wachtijd+5700);
                }


            }
        }
        //b_test = "true";

        b_test = "false";
        var lengtewachten = (vraag.length*600);
        setTimeout(function() {
            b_test = "true";
            console.log("wachten voorbij");
        },lengtewachten);
    }

    function makenAntw(){





        console.log("antwoord: " + text);
        if(antwoorden.length < 4){

        }
        antwoorden.push(text);

        if((niveau + 2) == antwoorden.length ){

            console.log("antwoordarray:" +antwoorden);
        }

        if(antwoorden.length == vraag.length){
            var is_same = (antwoorden.length == vraag.length) && antwoorden.every(function(element, index) {
                    return element === vraag[index];
                });
            if(is_same== true){
                // alert("juist");
                score = score + (niveau+2) ;

                vraagNummer++;

                //$.ajax({
                //    dataType: "json",
                //    type: "GET",
                //    url: "play/fart-01.wav",
                //    success: function(data){
                //        if(data.status == "error"){
                //            addError(data.message);
                //        }
                //    }
                //});
                setTimeout(function() {

                    var z = Math.floor((Math.random() * 24) + 1);
                    $.ajax({
                        dataType: "json",
                        data: {"phi": z, "r": 1},
                        type: "POST",
                        url: "setemotion",
                        success: function(data){
                            if(data.status == "error"){
                                addError(data.message);
                            }
                        }
                    });

                },500);





                console.log("juist:");

                for (i = 0; i < 8; i++) {
                    if(score >= i*8){
                        niveau = i;
                    }
                }


            }else{
                console.log("fout :");

        if(score == 0){
            $.ajax({
                dataType: "json",
                type: "GET",
                url: "play/jammerprobeeropnieuw.wav",
                success: function(data){
                    if(data.status == "error"){
                        addError(data.message);
                    }
                }
            });
        }else{
            setTimeout(function() {
                $.ajax({
                    dataType: "json",
                    type: "GET",
                    url: "play/jammer.wav",
                    success: function(data){
                        if(data.status == "error"){
                            addError(data.message);
                        }
                    }
                });
            },0);

            setTimeout(function() {
                $.ajax({
                    dataType: "json",
                    type: "GET",
                    url: "play/jehebt.wav",
                    success: function(data){
                        if(data.status == "error"){
                            addError(data.message);
                        }
                    }
                });
            },1000);
            var zegPunten = score;
            setTimeout(function() {
                $.ajax({
                    dataType: "json",
                    type: "GET",
                    url: "play/"+zegPunten+".wav",
                    success: function(data){
                        if(data.status == "error"){
                            addError(data.message);
                        }
                    }
                });
                console.log(zegPunten);

            },2000);
            setTimeout(function() {
                $.ajax({
                    dataType: "json",
                    type: "GET",
                    url: "play/punten.wav",
                    success: function(data){
                        if(data.status == "error"){
                            addError(data.message);
                        }
                    }
                });

            },3500);

            $.ajax({
                dataType: "json",
                data: {"phi": 200, "r": 1},
                type: "POST",
                url: "setemotion",
                success: function(data){
                    if(data.status == "error"){
                        addError(data.message);
                    }
                }
            });

            if (localStorage.getItem("names") === null) {
                //var person = prompt("Wat is jouw naam?", "naam");
                var names = [];
                var a = [];
                a.push(score,person);
                names.push(a);

                localStorage.setItem("names", JSON.stringify(names));


            }
            else {



                var storedNames = JSON.parse(localStorage.getItem("names"));

                //var person = prompt("Wat is jouw naam?", "naam");
                var a = [];
                a.push(score,person);

                storedNames.push(a);

                var test = storedNames.sort(function(b ,a )
                {
                    if(a[0] === b[0])
                    {
                        var x = a[1].toLowerCase(), y = b[1].toLowerCase();

                        return x < y ? -1 : x > y ? 1 : 0;
                    }
                    return a[0] - b[0];
                });
                console.log(test);
                localStorage.setItem("names", JSON.stringify(test));

                var elems = document.getElementsByClassName('highscore');
                var elemsSettings = document.getElementsByClassName('gamesettings');
                var pointsdiv = document.getElementsByClassName('points');

                console.log("laatste: " + elemsSettings);
                for (i = 0; i < 10; i++) {
                    elemsSettings[0].style.display = "none";
                    elems[0].style.display = "inline-block";
                    pointsdiv[0].style.display = "none";
                    startOpnieuw = 1;
                    $(".high.high"+i).html(test[i][1]);
                    $(".high.score"+i).html(test[i][0]);
                }
            }

            niveau = 0;
            score = 0;
        }


            }
            console.log("score :"  + score);
            $(".points").html(score + " punten");



            console.log("niveau :"  +niveau );
            vraag = [];
            antwoorden = [];
            if(startOpnieuw != 1){
                start();
            }


        }



}
    
    function zethighscoresGoed(){
        var elems = document.getElementsByClassName('highscore');
        var elemsSettings = document.getElementsByClassName('gamesettings');

        console.log(elems);
        if (elems[0] !== null){
            elemsSettings[0].style.display = "hidden";
        }
    }
    
    function ZetSettingsGoed(){
        var elems = document.getElementsByClassName('highscore');
        var elemsSettings = document.getElementsByClassName('gamesettings');

        console.log(elems);
        if (elems[0] !== null){
            elems[0].style.display = "none";
            elemsSettings[0].style.display = "block";
        }
        
        start();
    }





    $(".antw").click(function(){
        text = $(this).text();
        text = text.replace(/\s/g, '');
        makenAntw();
    });


    $(document).keydown(function(e) {

        if(b_test == "true"){
        if (keyAllowed [e.which] === false) return;
        keyAllowed [e.which] = false;
        var tag = e.target.tagName.toLowerCase();
        if ( e.which === 70 && tag != 'input' && tag != 'textarea'){
            var d = new Date();
            var n = d.getTime();
            if((n-tijd) < 50 ){
                console.log("twee tegelijk....");
            }else{
                tijd = new Date().getTime();
                console.log("w");
                text = "blauw";
                makenAntw();
            }
            tijd = new Date().getTime();

        }
        if ( e.which === 81 && tag != 'input' && tag != 'textarea'){
            var d2 = new Date();
            var n2 = d2.getTime();
            if((n2-tijd) < 50 ){
                console.log("twee tegelijk....");
            }else{
                tijd = new Date().getTime();
                console.log("d");
                text = "geel";
                makenAntw();
            }
            tijd = new Date().getTime();
        }
        if ( e.which === 71 && tag != 'input' && tag != 'textarea'){
            var d3 = new Date();
            var n3 = d3.getTime();
            if((n3-tijd) < 50 ){
                console.log("twee tegelijk....");
            }else{
                tijd = new Date().getTime();
                console.log("a");
                text = "groen";
                makenAntw();

                //if(startOpnieuw == 1){
                //    window.location.reload();
                //}
            }
            tijd = new Date().getTime();
        }
        if ( e.which === 90 && tag != 'input' && tag != 'textarea'){
            var d4 = new Date();
            var n4 = d4.getTime();
            if((n4-tijd) < 50 ){
                console.log("twee tegelijk....");
            }else{
                tijd = new Date().getTime();
                console.log("s");
                text = "rood";
                makenAntw();
            }
            tijd = new Date().getTime();
        }
        }
    });



    $(document).keyup(function(e) {
        keyAllowed [e.which] = true;
    });

    $(document).focus(function(e) {
        keyAllowed = {};
    });







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
				model.fileIsModified(true);
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

		self.modified = function(){
			model.fileIsModified(true);
		}

		self.toggleOutput = function(){
			model.fileIsModified(true);
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
			if (self.emotion().emotion){
				$.ajax({
					dataType: "json",
					data: {"phi": self.emotion().emotion.phi, "r": self.emotion().emotion.r},
					type: "POST",
					url: "setemotion",
					success: function(data){
						if(data.status == "error"){
							addError(data.message);
						}
					}
				});
			}
			if (self.emotion().custom){
				$.each(self.emotion().custom, function(idx, customControl){
					$.ajax({
						dataType: "json",
						data: {"dofname": customControl.dofname, "pos": customControl.pos},
						type: "POST",
						url: "setDofPos",
						success: function(data){
							if(data.status == "error"){
								addError(data.message);
							}
						}
					});
				});
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
		self.fileName = ko.observable("");
		self.fileStatus = ko.observable("");
		self.fileExtension = ko.observable(".soc");

		self.sounds = sounds_data;
		self.emotions = emotions_data;

		self.selectedVoiceLine = ko.observable();

		self.voiceLines = ko.observableArray();
		self.init = function(){
			self.fileName("Untitled");
			self.voiceLines.removeAll();
			self.voiceLines.push(new VoiceLine(self.emotions[0], "tts", "", ""));			
			self.voiceLines.push(new VoiceLine(self.emotions[1], "tts", "", ""));
			self.voiceLines.push(new VoiceLine(self.emotions[2], "tts", "", ""));
			self.voiceLines.push(new VoiceLine(self.emotions[3], "tts", "", ""));


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

		self.addLine = function(){
			self.fileIsModified(true);
			self.voiceLines.push( new VoiceLine(self.emotions[0], "tts", "", "") );
      window.scrollTo(0, document.body.scrollHeight);
		};

		self.removeLine = function(line){
			self.fileIsModified(true);
			self.voiceLines.remove(line);
		};

		self.loadFileData = function(filename){
			if (filename == "") {
				return;
			}
			$.ajax({
				dataType: "text",
				type: "POST",
				url: "files/get",
				cache: false,
				data: {path: filename, extension: self.fileExtension()},
				success: function(data){
					// Load script
					self.voiceLines.removeAll();

					var dataobj = JSON.parse(data);

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
					if(filename_no_ext.toLowerCase().slice(-4) == self.fileExtension()){
						filename_no_ext = filename_no_ext.slice(0, -4);
					}
					self.fileName(filename_no_ext);
					self.fileIsModified(false);
					self.lockFile();
				},
				error: function(){
					window.location.href = "?";
				}
			});
		};

		self.saveFileData = function(filename){
			if(filename == ""){
				addError("No filename!");
				return;
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
						path: filename,
						filedata: json_data,
						overwrite: 1,
						extension: self.fileExtension()
					},
					type: "POST",
					url: "files/save",
					success: function(data){
						var filename_no_ext = filename;
						if(filename_no_ext.toLowerCase().slice(-4) == self.fileExtension()){
							filename_no_ext = filename_no_ext.slice(0, -4);
						}
						self.fileName(filename_no_ext);
						self.fileIsModified(false);
					}
				});
			}
		};

		self.changeEmotion = function(emotion){
			self.fileIsModified(true);
			self.selectedVoiceLine().emotion(emotion);
			$("#PickEmotionModal").foundation("reveal", "close");
		};

		if (action_data.openfile) {
			self.loadFileData(action_data.openfile || "");
		} else {
			self.init();
		}
	};
	// This makes Knockout get to work
	var model = new SocialScriptModel();
	ko.applyBindings(model);
	model.fileIsModified(false);

	config_file_operations("scripts", model.fileExtension(), model.saveFileData, model.loadFileData, model.init);

});
