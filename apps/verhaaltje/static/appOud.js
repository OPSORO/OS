$(document).ready(function(){

    /**
     * Created by Lukas on 15/06/2016.
     */
    var lijntje = 0 ;
    var per10Array = [];
    var arrayMetAlleVerhaaltjes = ["hans","greitje","heks","lazy morning","test"];
    var aantallijen = [];
    var res = 0 ;

    $(".back").hide();
    $(".next").hide();

    for (x in arrayMetAlleVerhaaltjes) {
        console.log(x*3);

        if(x < 3){
            if( x == 0 ) {
                $(".foo").append("<div class='rowStory rowStory1'></div>");
            }

            console.log(arrayMetAlleVerhaaltjes[x]);
            $(".rowStory1").append("<div class='block'>"+arrayMetAlleVerhaaltjes[x]+"</div>");

        }



        if(x >= 3){
            if( x == 3 ) {
                $(".foo").append("<div class='rowStory rowStory2'></div>");
            }
            $(".rowStory2").append("<div class='block'>"+arrayMetAlleVerhaaltjes[x]+"</div>");
            console.log("rij25" +arrayMetAlleVerhaaltjes[x]);
        }



    }

    $(".foo").append("<div class='block add'><span class='fa fa-plus'></span> </div>");

    $.fn.highlight = function(what,spanClass) {
        return this.each(function(){
            var container = this,
                content = container.innerHTML,
                pattern = new RegExp('(>[^<.]*)(' + what + ')([^<.]*)','g'),
                replaceWith = '$1<span ' + ( spanClass ? 'class="' + spanClass + '"' : '' ) + '">$2</span>$3',
                highlighted = content.replace(pattern,replaceWith);
            container.innerHTML = highlighted;
        });
    }

    function leesLijn(){
        aantallijen++;
        //console.log(aantallijen-1);
        console.log(res[aantallijen-1]);

        //console.log("aantallijen/3   "+ aantallijen/3);
        if(aantallijen% 10 == 0 || aantallijen == 1 ){
            $("#verhaal").html("");
            if(typeof(res[lijntje]) == 'undefined'){

                $("#verhaal").append("<b>verhaaaltje gedaan</b>");
                console.log("gout");
            }else{
                for (i = 0; i < 10; i++) {


                    if(typeof(res[lijntje]) == 'undefined'){
                        console.log("gout");
                    }else{
                        //console.log(res[lijntje]);
                        $("#verhaal").append("<b>"+res[lijntje]+"</b>");
                        per10Array.push(res[lijntje]);
                        lijntje++;

                    }
                }
                console.log(per10Array);
                per10Array =[];
            }

        }

        $('#verhaal').highlight(res[aantallijen-1],'highlight');
        $('#verhaal').show();
    }

    $(".block").click(function(){



        text = $(this).text();

        if(text == ' add '){
            console.log("oei")
        }else{
            $(".back").show();
            $(".next").show();
            $(".rowStory").hide();
            $(".add").hide();

            console.log(text);

            $.ajax({
                url: "./test/"+text+".txt",
                async: false,
                success: function (data){
                    pageExecute.fileContents = data;
                }
            });
            leesLijn();

           
        }




    });

    $(".next").click(function(){

        leesLijn();
    });

    $(".back").click(function(){

        res = [];
        aantallijen = 0;
        lijntje =0;
        $(".rowStory").show();
        $(".add").show();
        $(".block").show();
        $('#verhaal').hide();

        $(".next").hide();
        $(".back").hide();
    });


    var Model = function(){
    var self = this;

    // File operations toolbar item
		self.fileIsLocked = ko.observable(false);
		self.fileIsModified = ko.observable(false);
		self.fileName = ko.observable("");
		self.fileStatus = ko.observable("");
		self.fileExtension = ko.observable(".ext");

    // Script operations toolbar item
    self.isRunning = ko.observable(false);
    self.isUI = ko.observable(false);

    // Lock/Unlock toolbar item
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

    // Popup window
    self.popupTextInput = ko.observable("Hi! This text can be changed. Click on the button to change me!");
    self.showPopup = function(){
      $("#popup_window").foundation("reveal", "open");
    };
    self.closePopup = function(){
      $("#popup_window").foundation("reveal", "close");
    };
    self.popupButtonHandler = function(){
      self.closePopup();
    };

    self.init = function(){
      // Clear data, new file, ...
			self.fileName("Untitled");
			self.unlockFile();
			self.fileIsModified(false);
    };

    self.loadFileData = function(filename){
			if (filename == "") {
				//("No filename!");
				return;
			}
			$.ajax({
				dataType: "text",
				type: "POST",
				url: "files/get",
				cache: false,
				data: {path: filename, extension: self.fileExtension()},
				success: function(data){
					// Load data
					var dataobj = JSON.parse(data);

          // Do something with the data

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
				//("No filename!");
				return;
			}else{
        // Convert data
        file_data = {};
				var data = ko.toJSON(file_data, null, 2);
        // Send data
				$.ajax({
					dataType: "json",
					data: {
						path: filename,
						filedata: data,
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
  };
  // This makes Knockout get to work
  var model = new Model();
  ko.applyBindings(model);
	model.fileIsModified(false);

  // Configurate toolbar handlers
  //config_file_operations("", model.fileExtension(), model.saveFileData, model.loadFileData, model.init);
});
