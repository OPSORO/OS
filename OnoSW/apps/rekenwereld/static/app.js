$(document).ready(function(){

    var tekens = ["-", "+"];
    var tafels = ["X", "%"];

    var teken = 0;
    var tafel = 0;

    var som = [];
    var mogelijkeAntwoorden = [];

    var juisteAntwoord = 0;
    var antwoord = 0;
    var vraagNummer = 0;

    var score = 0;
    var test = [];

    var level = 0;

    $(".maths").hide();
    function start() {
        for (i = 0; i < 3; i++) {

            var x = Math.floor((Math.random() * 10) + 1);
            var y = Math.floor((Math.random() * 10) + 1);
            teken = tekens[Math.floor(Math.random() * tekens.length)];

            if(teken === "-" ){
                antwoord = (x-y);
                //if((antwoord) > 0){
                som.push(x,teken, y,antwoord);
                mogelijkeAntwoorden.push(antwoord);

                //}else{
                //  start();
                //}
            }
            if(teken === "+"){
                antwoord = (x+y);
                //if((antwoord) < 10){
                som.push(x,teken, y,antwoord);
                mogelijkeAntwoorden.push(antwoord);

                //}else{
                //    start();
                //}
            }
        }
    }







    Array.prototype.shuffle = function() {
        var input = this;

        for (var i = input.length-1; i >=0; i--) {

            var randomIndex = Math.floor(Math.random()*(i+1));
            var itemAtIndex = input[randomIndex];

            input[randomIndex] = input[i];
            input[i] = itemAtIndex;
        }
        return input;
    }

    //console.log(test);

    //console.log(test);

    function Tot10() {
        start();
        console.log("term1 = "+som[0]);
        console.log("teken = "+som[1]);
        console.log("term2 = "+som[2]);
        console.log("som = "+som);

        $(".vraag").html(som[0]+" "+som[1]+" "+som[2]);
        $(".number1").html(som[0]);
        $(".sign").html(som[1]);
        $(".number2").html(som[2]);

        console.log("mogelijkeAntwoorden = "+mogelijkeAntwoorden);
        mogelijkeAntwoorden.shuffle();
        console.log("mogelijkeAntwoorden = "+mogelijkeAntwoorden);

        for (i = 0; i < mogelijkeAntwoorden.length; i++) {
            $(".answer"+i).html(mogelijkeAntwoorden[i]);
        }

        //antwoordArray();
        console.log("term2 = "+mogelijkeAntwoorden);

        mogelijkeAntwoorden = [];
    }
    $(".level1").click(function(){
        level = 1;
        Tot10();
        $(".level").hide();
        $(".maths").show();

    });

    $(".back").click(function(){

        $(".level").show();
        $(".maths").hide();
        $(".highscore").hide();

        var antwoord = 0;
        var vraagNummer = 0;

    });

    $(".answer").click(function(){
        text = $(this).text();
        console.log("antw = "+som[3]);
        if(som[3]== text){
            alert("juist");
            som = [];
            score++;
            vraagNummer++;
            if(vraagNummer == 10){

                HighScore();
            }
            if(level == 1){
                Tot10();
            }
            if(level == 2){
                Tot100();
            }
            if(level == 3){
                Tafels();
            }
        }else{
            alert("fout");
            som = [];
            vraagNummer++;
            if(vraagNummer == 10){
                HighScore();
            }
            if(level == 1){
                Tot10();
            }
            if(level == 2){
                Tot100();
            }
            if(level == 3){
                Tafels();
            }
        }
    });

    function HighScore(){
        if(level == 1){
            localstorageNaam = "namesRekenen";
        }
        if(level == 2){
            localstorageNaam = "namesRekenenTot100";
        }
        if(level == 3){
            localstorageNaam = "namesRekenenTafels";
        }
        if (localStorage.getItem(localstorageNaam) === null) {
            var person = prompt("Wat is jouw naam?", "naam");
            var names = [];
            var a = [];
            a.push(score,person);
            names.push(a);

            localStorage.setItem(localstorageNaam, JSON.stringify(names));


        }else {
            var test;
            //if(score > 0){
            var storedNames = JSON.parse(localStorage.getItem(localstorageNaam));

            var person = prompt("Wat is jouw naam?", "naam");
            var a = [];
            a.push(score,person);

            storedNames.push(a);

            test = storedNames.sort(function(b ,a )
            {
                if(a[0] === b[0])
                {
                    var x = a[1].toLowerCase(), y = b[1].toLowerCase();

                    return x < y ? -1 : x > y ? 1 : 0;
                }
                return a[0] - b[0];
            });
            localStorage.setItem(localstorageNaam, JSON.stringify(test));
            //}
            if(test.length < 10 ){
                for (i = 0; i < test.length; i++) {

                    $(".high"+i).html(test[i][1]);
                    $(".score"+i).html(test[i][0]);
                    $(".maths").hide();
                    $(".highscore").show();

                }
            }else{
                for (i = 0; i < 10; i++) {

                    $(".high"+i).html(test[i][1]);
                    $(".score"+i).html(test[i][0]);
                    $(".maths").hide();
                    $(".highscore").show();

                }
            }

        }

    }

    //$(".start").click(function(){
    //
    //    test.push(start());
    //    console.log("test = "+ test);
    //    start();
    //    console.log("test");
    //    var vraag = x + teken + y;
    //    //console.log(x);
    //    //console.log(y);
    //    //console.log(x + y );
    //    // console.log(vraag);
    //
    //    if(teken == "-" ){
    //        console.log(vraag);
    //        console.log("antwoord="+ (x - y)  );
    //    }
    //    if(teken == "+"){
    //        console.log(vraag);
    //        console.log("antwoord="+ (x + y)  );
    //    }
    //
    //});


    function startTot100() {

        for (i = 0; i < 3; i++) {

            var x = Math.floor((Math.random() * 100) + 1);
            var y = Math.floor((Math.random() * 100) + 1);
            teken = tekens[Math.floor(Math.random() * tekens.length)];

            if(teken === "-" ){
                antwoord = (x-y);
                //if((antwoord) > 0){
                som.push(x,teken, y,antwoord);
                mogelijkeAntwoorden.push(antwoord);

                //}else{
                //  start();
                //}
            }
            if(teken === "+"){
                antwoord = (x+y);
                //if((antwoord) < 10){
                som.push(x,teken, y,antwoord);
                mogelijkeAntwoorden.push(antwoord);

                //}else{
                //    start();
                //}
            }
        }

    }

    function Tot100(){
        startTot100();


        console.log("term1 = "+som[0]);
        console.log("teken = "+som[1]);
        console.log("term2 = "+som[2]);
        console.log("som = "+som);

        $(".vraag").html(som[0]+" "+som[1]+" "+som[2]);
        $(".number1").html(som[0]);
        $(".sign").html(som[1]);
        $(".number2").html(som[2]);

        console.log("mogelijkeAntwoorden = "+mogelijkeAntwoorden);
        mogelijkeAntwoorden.shuffle();
        console.log("mogelijkeAntwoorden = "+mogelijkeAntwoorden);

        for (i = 0; i < mogelijkeAntwoorden.length; i++) {
            $(".answer"+i).html(mogelijkeAntwoorden[i]);
        }

        //antwoordArray();
        console.log("term2 = "+mogelijkeAntwoorden);

        mogelijkeAntwoorden = [];
    }

    $(".level2").click(function(){
        level = 2;
        Tot100();
        $(".level").hide();
        $(".maths").show();



    });

    function Tafels() {
        startTafel();

        $(".vraag").html(som[0]+" "+som[1]+" "+som[2]);
        $(".number1").html(som[0]);
        $(".sign").html(som[1]);
        $(".number2").html(som[2]);

        console.log("mogelijkeAntwoorden = "+mogelijkeAntwoorden);
        mogelijkeAntwoorden.shuffle();
        console.log("mogelijkeAntwoorden = "+mogelijkeAntwoorden);

        for (i = 0; i < mogelijkeAntwoorden.length; i++) {
            $(".answer"+i).html(mogelijkeAntwoorden[i]);
        }
        mogelijkeAntwoorden = [];
    }

    function startTafel(){
        for (i = 0; i < 3; i++) {

            var x = Math.floor((Math.random() * 10) + 1);
            var y = Math.floor((Math.random() * 10) + 1);
            teken = "X";

            antwoord = (x*y);
            som.push(x,teken, y,antwoord);
            mogelijkeAntwoorden.push(antwoord);
        }
    }



    $(".level3").click(function(){
        level = 3;
        Tafels();
        $(".level").hide();
        $(".maths").show();

    });

    //
    //$(".antw").click(function(){
    //    text = $(this).text();
    //    text = text.replace(/\s/g, '');
    //    makenAntw();
    //});


    $(document).on('keypress', function(e) {
        var tag = e.target.tagName.toLowerCase();
        if ( e.which === 70 && tag != 'input' && tag != 'textarea')
        {
            //78
            console.log("w");
            text = "blauw";
            makenAntw();
        }

    });

    $(document).on('keypress', function(e) {
        var tag = e.target.tagName.toLowerCase();
        if ( e.which === 68 && tag != 'input' && tag != 'textarea'){
            //68
            console.log("d");
            text = "wit";
            makenAntw();
        }

    });

    $(document).on('keypress', function(e) {
        var tag = e.target.tagName.toLowerCase();
        if ( e.which === 81 && tag != 'input' && tag != 'textarea'){
            //65
            console.log("a");
            text = "groen";
            makenAntw();
        }

    });

    $(document).on('keypress', function(e) {
        var tag = e.target.tagName.toLowerCase();
        if ( e.which === 90 && tag != 'input' && tag != 'textarea'){
            //83
            console.log("s");
            text = "rood";
            makenAntw();
        }

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
