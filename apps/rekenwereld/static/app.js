$(document).ready(function(){
    $.ajax({
        dataType: "json",
        url: "servos/disable",
        success: function(data){
            if(data.status == "error"){
                addError(data.message);
            }
        }
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
    var person = 0;
    var level = 0;

    var b_antwoord = false;

    var knop = 0;
    var klikkenOfScherm = 1;

    var antwoordKnop = 0;
    var keyAllowed = {};
    var b_test = "false";
    var d = new Date();
    var tijd = d.getTime();

    var wachtopsom = 0;

    $(".maths").hide();
    $(".levelselect").hide();
    $(".back").hide();
    $("#verander").hide();


    $("#invoerKnop").click(function(){
        console.log("hoi");
        $(".uitleg").hide()
        $(".levelselect").show();

        //$(".back").show();
        $("#verander").show();
        $("#invoerKnop").hide();
        $("#naam").prop('disabled', true);
        person = $( "#naam" ).val();
        //$("#invoerKnop").text("verander");


    });

    $("#verander").click(function(){
        $("#naam").prop('disabled', false);
        $("#verander").hide();
        $("#invoerKnop").show();

    });



    $('#naam').change(function() {

        $('#invoerKnop').prop('disabled', false);
    });








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



    function start() {
        var x = Math.floor((Math.random() * 10) + 1);
        var y = Math.floor((Math.random() * 10) + 1);
        teken = tekens[Math.floor(Math.random() * tekens.length)];

        if(teken === "-" ){
            antwoord = (x-y);
            if((antwoord) > 0){
                som = [];
                som.push(x,teken, y,antwoord);
                mogelijkeAntwoorden = [];
                mogelijkeAntwoorden.push(antwoord);

                (function test() {
                    var z = Math.floor((Math.random() * 10) + 1);
                    var a = Math.floor((Math.random() * 10) + 1);
                    if(antwoord != z && z != a && antwoord != a){
                        mogelijkeAntwoorden.push(z,a);
                    }else{
                        test();
                    }
                }())



            }else{
                som = [];
                mogelijkeAntwoorden = [];
                start();
            }
        }
        if(teken === "+"){
            antwoord = (x+y);
            if((antwoord) < 10){
                som = [];
                som.push(x,teken, y,antwoord);
                mogelijkeAntwoorden = [];
                mogelijkeAntwoorden.push(antwoord);

                (function test() {
                    var z = Math.floor((Math.random() * 10) + 1);
                    var a = Math.floor((Math.random() * 10) + 1);
                    if(antwoord != z && z != a && antwoord != a){
                        mogelijkeAntwoorden.push(z,a);
                    }else{
                        test();
                    }
                }())
            }else{

                som = [];
                mogelijkeAntwoorden = [];
                start();
            }
        }
        b_test = "true";

    }

    function Tot10() {
        start();
        console.log("term1 = "+som[0]);
        console.log("teken = "+som[1]);
        console.log("term2 = "+som[2]);
        console.log("som = "+som);

        $(".vraag").html(som[0]+" "+som[1]+" "+som[2]);
        $(".number1").html(som[0]);

        if(vraagNummer !== 0){

            if(b_antwoord == "true"){



                //$.ajax({
                //    dataType: "json",
                //    data: {"phi": 23, "r": 1},
                //    type: "POST",
                //    url: "setemotion",
                //    success: function(data){
                //        if(data.status == "error"){
                //            addError(data.message);
                //        }
                //    }
                //});

                var goedArray = ["flink", "goedgedaan", "goedgespeeld", "goedzo", "smb_coin"];
                var index = Math.floor(Math.random() * 5);
                var goedzo = goedArray[index];
                $.ajax({
                    dataType: "json",
                    data: {"phi":24,"r":1},
                    type: "POST",
                    url: "setemotion",
                    success: function(data){
                        if(data.status == "error"){
                            addError(data.message);
                        }
                    }
                });


                setTimeout(function() {
                    $.ajax({
                        dataType: "json",
                        type: "GET",
                        url: "play/"+goedzo+".wav",
                        success: function(data){
                            if(data.status == "error"){
                                addError(data.message);
                            }
                        }
                    });
                },500);
            }else{
                $.ajax({
                    dataType: "json",
                    data: {"phi":200,"r":1},
                    type: "POST",
                    url: "setemotion",
                    success: function(data){
                        if(data.status == "error"){
                            addError(data.message);
                        }
                    }
                });

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
                },500);

            }

        }
        setTimeout(function() {
            $.ajax({
                dataType: "json",
                type: "GET",
                url: "play/"+som[0]+".wav",
                success: function(data){
                    if(data.status == "error"){
                        addError(data.message);
                    }
                }
            });

            $.ajax({
                dataType: "json",
                data: {"phi":0,"r":1},
                type: "POST",
                url: "setemotion",
                success: function(data){
                    if(data.status == "error"){
                        addError(data.message);
                    }
                }
            });

        },1500);

        setTimeout(function() {
            $.ajax({
                dataType: "json",
                type: "GET",
                url: "play/"+som[1]+".wav",
                success: function(data){
                    if(data.status == "error"){
                        addError(data.message);
                    }
                }
            });
        },2500);

        setTimeout(function() {
            $.ajax({
                dataType: "json",
                type: "GET",
                url: "play/"+som[2]+".wav",
                success: function(data){
                    if(data.status == "error"){
                        addError(data.message);
                    }
                }
            });
        },3500);

        $(".sign").html(som[1]);
        $(".number2").html(som[2]);

        b_test = "false";
        setTimeout(function() {
            b_test = "true";
            console.log("wachten voorbij");
        },3500);


        console.log("mogelijkeAntwoorden = "+mogelijkeAntwoorden);
        mogelijkeAntwoorden.shuffle();
        console.log("mogelijkeAntwoorden = "+mogelijkeAntwoorden);

        for (i = 0; i < mogelijkeAntwoorden.length; i++) {
            $(".answer"+i).html(mogelijkeAntwoorden[i]);
        }

        //antwoordArray();
        console.log("term2 = "+mogelijkeAntwoorden);


    }


    $(".level1").click(function(){
        level = 1;
        Tot10();
        $(".level").hide();
        $(".maths").show();
        $(".back").show();

    });

    $(".back").click(function(){

        $(".level").show();
        $(".maths").hide();
        $(".back").hide();
        $(".highscore").hide();

        antwoord = 0;
        vraagNummer = 0;
        score = 0;
        som = [];
        mogelijkeAntwoorden = [];
    });

    $(".answer").click(function(){
        knop = 0;
        text = $(this).text();
        console.log("antw = "+som[3]);
        if(som[3]== text){
            console.log("juist");
            som = [];
            score++;
            vraagNummer++;
            b_antwoord = "true";
            if(vraagNummer == 10){
                //$.ajax({
                //    dataType: "json",
                //    data: {"phi": 2, "r": 1},
                //    type: "POST",
                //    url: "setemotion",
                //    success: function(data){
                //        if(data.status == "error"){
                //            addError(data.message);
                //        }
                //    }
                //});
                HighScore();
            }else{
                if(level == 1){
                    Tot10();
                }
                if(level == 2){
                    Tot100();
                }
                if(level == 3){
                    Tafels();
                }
                if(level == 4){
                    Tot20();
                }
            }

        }else{
            console.log("fout");
            b_antwoord = "false";
            som = [];
            vraagNummer++;
            if(vraagNummer == 10){
                HighScore();

            }else{
                if(level == 1){
                    Tot10();
                }
                if(level == 2){
                    Tot100();
                }
                if(level == 3){
                    Tafels();
                }
                if(level == 4){
                    Tot20();
                }
            }

        }
        $(".points").html(score + " punten");
    });

    function HighScore(){
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
        },1500);
        setTimeout(function() {
            $.ajax({
                dataType: "json",
                type: "GET",
                url: "play/"+score+".wav",
                success: function(data){
                    if(data.status == "error"){
                        addError(data.message);
                    }
                }
            });
        },2500);
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
        },4000);

        if(level == 1){
            localstorageNaam = "namesRekenen";
        }
        if(level == 2){
            localstorageNaam = "namesRekenenTot100";
        }
        if(level == 3){
            localstorageNaam = "namesRekenenTafels";
        }
        if(level == 4){
            localstorageNaam = "namesRekenenTot20";
        }
        if (localStorage.getItem(localstorageNaam) === null) {

            var names = [];
            var a = [];
            a.push(score,person);
            names.push(a);

            localStorage.setItem(localstorageNaam, JSON.stringify(names));
            $(".score"+0).html(names[0][1]);
            $(".high"+0).html(names[0][0]);
            $(".highscore").show();
            $(".maths").hide();

        }else {
            var test;
            //if(score > 0){
            var storedNames = JSON.parse(localStorage.getItem(localstorageNaam));


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
                    $(".highscore").show();
                    $(".maths").hide();
                }
            }else{
                for (i = 0; i < 10; i++) {

                    $(".high"+i).html(test[i][1]);
                    $(".score"+i).html(test[i][0]);
                    $(".highscore").show();
                    $(".maths").hide();


                }
            }

        }

    }




    function startTot100() {
        var x = Math.floor((Math.random() * 100) + 1);
        var y = Math.floor((Math.random() * 100) + 1);
        teken = tekens[Math.floor(Math.random() * tekens.length)];

        if(teken === "-" ){
            antwoord = (x-y);
            if((antwoord) > 0){
                //hier is de fout !!!

                som = [];
                som.push(x,teken, y,antwoord);
                mogelijkeAntwoorden = [];
                mogelijkeAntwoorden.push(antwoord);

                (function test() {
                    var z = Math.floor((Math.random() * 100) + 1);
                    var a = Math.floor((Math.random() * 100) + 1);
                    if(antwoord != z && z != a && antwoord != a){
                        mogelijkeAntwoorden.push(z,a);
                    }else{
                        test();
                    }
                }())
            }else{
                som = [];
                teken = 0;
                mogelijkeAntwoorden = [];
                startTot100();
            }
        }
        if(teken === "+"){
            antwoord = (x+y);
            if((antwoord) < 100){
                som = [];
                som.push(x,teken, y,antwoord);
                mogelijkeAntwoorden = [];
                mogelijkeAntwoorden.push(antwoord);
                (function test() {
                    var z = Math.floor((Math.random() * 100) + 1);
                    var a = Math.floor((Math.random() * 100) + 1);
                    if(antwoord != z && z != a && antwoord != a){
                        mogelijkeAntwoorden.push(z,a);
                    }else{
                        test();
                    }
                }())
            }else{
                som = [];
                mogelijkeAntwoorden = [];
                startTot100();
            }
        }
        b_test = "true";


    }

    function Tot100(){
        som = [];
        mogelijkeAntwoorden = [];
        startTot100();


        console.log("term1 = "+som[0]);
        console.log("teken = "+som[1]);
        console.log("term2 = "+som[2]);
        console.log("som = "+som);

        $(".vraag").html(som[0]+" "+som[1]+" "+som[2]);
        $(".number1").html(som[0]);
        $(".sign").html(som[1]);
        $(".number2").html(som[2]);

        if(vraagNummer !== 0){
            //$.ajax({
            //    dataType: "json",
            //    data: {"phi": 23, "r": 1},
            //    type: "POST",
            //    url: "setemotion",
            //    success: function(data){
            //        if(data.status == "error"){
            //            addError(data.message);
            //        }
            //    }
            //});

            if(b_antwoord == "true"){
                var goedArray = ["flink", "goedgedaan", "goedgespeeld", "goedzo", "smb_coin"];
                var index = Math.floor(Math.random() * 5);
                var goedzo = goedArray[index];

                $.ajax({
                    dataType: "json",
                    data: {"phi":24,"r":1},
                    type: "POST",
                    url: "setemotion",
                    success: function(data){
                        if(data.status == "error"){
                            addError(data.message);
                        }
                    }
                });

                setTimeout(function() {
                    $.ajax({
                        dataType: "json",
                        type: "GET",
                        url: "play/"+goedzo+".wav",
                        success: function(data){
                            if(data.status == "error"){
                                addError(data.message);
                            }
                        }
                    });
                },500);
            }else{
                $.ajax({
                    dataType: "json",
                    data: {"phi":200,"r":1},
                    type: "POST",
                    url: "setemotion",
                    success: function(data){
                        if(data.status == "error"){
                            addError(data.message);
                        }
                    }
                });

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
                },500);

            }
        }
        setTimeout(function() {
            $.ajax({
                    dataType: "json",
                    type: "GET",
                    url: "play/"+som[0]+".wav",
                    success: function(data){
                        if(data.status == "error"){
                            addError(data.message);
                        }
                    }
            });
        },1500);

        setTimeout(function() {
            $.ajax({
                dataType: "json",
                type: "GET",
                url: "play/"+som[1]+".wav",
                success: function(data){
                    if(data.status == "error"){
                        addError(data.message);
                    }
                }
            });
        },3000);

        setTimeout(function() {
            $.ajax({
                dataType: "json",
                type: "GET",
                url: "play/"+som[2]+".wav",
                success: function(data){
                    if(data.status == "error"){
                        addError(data.message);
                    }
                }
            });
        },4500);

        b_test = "false";
        setTimeout(function() {
            b_test = "true";
            console.log("wachten voorbij");
        },4500);


        console.log("mogelijkeAntwoorden = "+mogelijkeAntwoorden);
        mogelijkeAntwoorden.shuffle();
        console.log("mogelijkeAntwoorden = "+mogelijkeAntwoorden);

        for (i = 0; i < mogelijkeAntwoorden.length; i++) {
            $(".answer"+i).html(mogelijkeAntwoorden[i]);
        }

        //antwoordArray();
        console.log("term2 = "+mogelijkeAntwoorden);

    }

    $(".level2").click(function(){
        level = 2;
        Tot100();
        $(".level").hide();
        $(".maths").show();
        $(".back").show();


    });

    function Tafels() {
        som = [];
        mogelijkeAntwoorden = [];
        startTafel();

        $(".vraag").html(som[0]+" "+som[1]+" "+som[2]);
        $(".number1").html(som[0]);
        $(".sign").html(som[1]);
        $(".number2").html(som[2]);

        if(vraagNummer !== 0){
            //$.ajax({
            //    dataType: "json",
            //    data: {"phi": 23, "r": 1},
            //    type: "POST",
            //    url: "setemotion",
            //    success: function(data){
            //        if(data.status == "error"){
            //            addError(data.message);
            //        }
            //    }
            //});

            if(b_antwoord == "true"){
                var goedArray = ["flink", "goedgedaan", "goedgespeeld", "goedzo", "smb_coin"];
                var index = Math.floor(Math.random() * 5);
                var goedzo = goedArray[index];

                $.ajax({
                    dataType: "json",
                    data: {"phi":24,"r":1},
                    type: "POST",
                    url: "setemotion",
                    success: function(data){
                        if(data.status == "error"){
                            addError(data.message);
                        }
                    }
                });

                setTimeout(function() {
                    $.ajax({
                        dataType: "json",
                        type: "GET",
                        url: "play/"+goedzo+".wav",
                        success: function(data){
                            if(data.status == "error"){
                                addError(data.message);
                            }
                        }
                    });
                },500);
            }else{
                $.ajax({
                    dataType: "json",
                    data: {"phi":200,"r":1},
                    type: "POST",
                    url: "setemotion",
                    success: function(data){
                        if(data.status == "error"){
                            addError(data.message);
                        }
                    }
                });

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
                },500);

            }
        }
        setTimeout(function() {
            $.ajax({
                dataType: "json",
                type: "GET",
                url: "play/"+som[0]+".wav",
                success: function(data){
                    if(data.status == "error"){
                        addError(data.message);
                    }
                }
            });
        },1500);

        setTimeout(function() {
            $.ajax({
                dataType: "json",
                type: "GET",
                url: "play/"+som[1]+".wav",
                success: function(data){
                    if(data.status == "error"){
                        addError(data.message);
                    }
                }
            });
        },2500);

        setTimeout(function() {
            $.ajax({
                dataType: "json",
                type: "GET",
                url: "play/"+som[2]+".wav",
                success: function(data){
                    if(data.status == "error"){
                        addError(data.message);
                    }
                }
            });
        },3500);

        b_test = "false";
        setTimeout(function() {
            b_test = "true";
            console.log("wachten voorbij");
        },3500);


        console.log("mogelijkeAntwoorden = "+mogelijkeAntwoorden);
        mogelijkeAntwoorden.shuffle();
        console.log("mogelijkeAntwoorden = "+mogelijkeAntwoorden);

        for (i = 0; i < mogelijkeAntwoorden.length; i++) {
            $(".answer"+i).html(mogelijkeAntwoorden[i]);
        }

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
        b_test = "true";

    }

    $(".level4").click(function(){
        level = 4;
        Tot20();
        $(".level").hide();
        $(".maths").show();
        $(".back").show();


    });

    function startTot20() {
        var x = Math.floor((Math.random() * 20) + 1);
        var y = Math.floor((Math.random() * 20) + 1);
        teken = tekens[Math.floor(Math.random() * tekens.length)];

        if(teken === "-" ){
            antwoord = (x-y);
            if((antwoord) > 0){
                som = [];
                som.push(x,teken, y,antwoord);
                mogelijkeAntwoorden = [];
                mogelijkeAntwoorden.push(antwoord);

                (function test() {
                    var z = Math.floor((Math.random() * 20) + 1);
                    var a = Math.floor((Math.random() * 20) + 1);
                    if(antwoord != z && z != a && antwoord != a){
                        mogelijkeAntwoorden.push(z,a);
                    }else{
                        test();
                    }
                }())



            }else{
                som = [];
                mogelijkeAntwoorden = [];
                start();
            }
        }
        if(teken === "+"){
            antwoord = (x+y);
            if((antwoord) < 20){
                som = [];
                som.push(x,teken, y,antwoord);
                mogelijkeAntwoorden = [];
                mogelijkeAntwoorden.push(antwoord);

                (function test() {
                    var z = Math.floor((Math.random() * 20) + 1);
                    var a = Math.floor((Math.random() * 20) + 1);
                    if(antwoord != z && z != a && antwoord != a){
                        mogelijkeAntwoorden.push(z,a);
                    }else{
                        test();
                    }
                }())
            }else{

                som = [];
                mogelijkeAntwoorden = [];
                start();
            }
        }
        b_test = "true";

    }

    function Tot20() {
        startTot20();
        console.log("term1 = "+som[0]);
        console.log("teken = "+som[1]);
        console.log("term2 = "+som[2]);
        console.log("som = "+som);

        $(".vraag").html(som[0]+" "+som[1]+" "+som[2]);
        $(".number1").html(som[0]);

        if(vraagNummer !== 0){
            //$.ajax({
            //    dataType: "json",
            //    data: {"phi": 23, "r": 1},
            //    type: "POST",
            //    url: "setemotion",
            //    success: function(data){
            //        if(data.status == "error"){
            //            addError(data.message);
            //        }
            //    }
            //});
            if(b_antwoord == "true"){
                var goedArray = ["flink", "goedgedaan", "goedgespeeld", "goedzo", "smb_coin"];
                var index = Math.floor(Math.random() * 5);
                var goedzo = goedArray[index];

                $.ajax({
                    dataType: "json",
                    data: {"phi":24,"r":1},
                    type: "POST",
                    url: "setemotion",
                    success: function(data){
                        if(data.status == "error"){
                            addError(data.message);
                        }
                    }
                });

                setTimeout(function() {
                    $.ajax({
                        dataType: "json",
                        type: "GET",
                        url: "play/"+goedzo+".wav",
                        success: function(data){
                            if(data.status == "error"){
                                addError(data.message);
                            }
                        }
                    });
                },500);
            }else{

                $.ajax({
                    dataType: "json",
                    data: {"phi":200,"r":1},
                    type: "POST",
                    url: "setemotion",
                    success: function(data){
                        if(data.status == "error"){
                            addError(data.message);
                        }
                    }
                });

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
                },500);


            }

        }
        setTimeout(function() {
            $.ajax({
                dataType: "json",
                type: "GET",
                url: "play/"+som[0]+".wav",
                success: function(data){
                    if(data.status == "error"){
                        addError(data.message);
                    }
                }
            });
        },1500);

        setTimeout(function() {
            $.ajax({
                dataType: "json",
                type: "GET",
                url: "play/"+som[1]+".wav",
                success: function(data){
                    if(data.status == "error"){
                        addError(data.message);
                    }
                }
            });
        },2500);

        setTimeout(function() {
            $.ajax({
                dataType: "json",
                type: "GET",
                url: "play/"+som[2]+".wav",
                success: function(data){
                    if(data.status == "error"){
                        addError(data.message);
                    }
                }
            });
        },3500);

        $(".sign").html(som[1]);
        $(".number2").html(som[2]);

        b_test = "false";
        setTimeout(function() {
            b_test = "true";
            console.log("wachten voorbij");
        },3500);


        console.log("mogelijkeAntwoorden = "+mogelijkeAntwoorden);
        mogelijkeAntwoorden.shuffle();
        console.log("mogelijkeAntwoorden = "+mogelijkeAntwoorden);

        for (i = 0; i < mogelijkeAntwoorden.length; i++) {
            $(".answer"+i).html(mogelijkeAntwoorden[i]);
        }

        //antwoordArray();
        console.log("term2 = "+mogelijkeAntwoorden);


    }




    $(".level3").click(function(){
        level = 3;
        Tafels();
        $(".level").hide();
        $(".maths").show();
        $(".back").show();
    });


    $("#opties").click(function(){
        klikkenOfScherm = 1;
        console.log(klikkenOfScherm);
    });

    $("#klikken").click(function(){
        klikkenOfScherm = 0;
        console.log(klikkenOfScherm);

    });

    $("#plus").click(function(){
        knop++;
    });


    $("#enter").click(function(){
        console.log(knop);
        if(som[3]== knop){
            console.log("juist");
            b_antwoord == "true";
            som = [];
            score++;
            vraagNummer++;
            if(vraagNummer == 10){

                HighScore();
            }else{
                if(level == 1){
                    Tot10();
                }
                if(level == 2){
                    Tot100();
                }
                if(level == 3){
                    Tafels();
                }
                if(level == 4){
                    Tot20();
                }
            }
        }else{
            console.log("fout");
            b_antwoord == "false";
            som = [];
            vraagNummer++;
            if(vraagNummer == 10){
                HighScore();
            }else{
                if(level == 1){
                    Tot10();
                }
                if(level == 2){
                    Tot100();
                }
                if(level == 3){
                    Tafels();
                }
                if(level == 4){
                    Tot20();
                }
            }
        }
        $(".points").html(score + " punten");
        knop = 0;
    });



    $(document).keydown(function(e) {

        if(b_test == "true"){
            if (keyAllowed [e.which] === false) return;
            keyAllowed [e.which] = false;
            var tag = e.target.tagName.toLowerCase();
            if ( e.which === 32 && tag != 'input' && tag != 'textarea'){
                var d = new Date();
                var n = d.getTime();
                if((n-tijd) < 300 ){
                    console.log("twee tegelijk....");
                }else{
                    tijd = new Date().getTime();
                    console.log("w");


                    if(wachtopsom == 0){
                        wachtopsom = 1;
                        setTimeout(function() {
                            $.ajax({
                                dataType: "json",
                                type: "GET",
                                url: "play/"+som[0]+".wav",
                                success: function(data){
                                    if(data.status == "error"){
                                        addError(data.message);
                                    }
                                }
                            });
                            wachtopsom = 1;
                        },1500);

                        setTimeout(function() {
                            $.ajax({
                                dataType: "json",
                                type: "GET",
                                url: "play/"+som[1]+".wav",
                                success: function(data){
                                    if(data.status == "error"){
                                        addError(data.message);
                                    }
                                }
                            });
                            wachtopsom = 1;
                        },2500);

                        setTimeout(function() {
                            $.ajax({
                                dataType: "json",
                                type: "GET",
                                url: "play/"+som[2]+".wav",
                                success: function(data){
                                    if(data.status == "error"){
                                        addError(data.message);
                                    }
                                }
                            });
                            wachtopsom = 0;
                        },3500);
                    }
                    }

                tijd = new Date().getTime();

            }
            if ( e.which === 81 && tag != 'input' && tag != 'textarea'){
                var d = new Date();
                var n = d.getTime();
                if((n-tijd) < 50 ){
                    console.log("twee tegelijk....");
                }else{
                    tijd = new Date().getTime();
                    console.log("f");
                    console.log(mogelijkeAntwoorden[0]);
                    antwoordKnop = mogelijkeAntwoorden[0];

                    $.ajax({
                        dataType: "json",
                        type: "GET",
                        url: "play/"+mogelijkeAntwoorden[0]+".wav",
                        success: function(data){
                            if(data.status == "error"){
                                addError(data.message);
                            }
                        }
                    });

                    text = "blauw";
                }
                tijd = new Date().getTime();

            }
            if ( e.which === 90 && tag != 'input' && tag != 'textarea'){
                var d2 = new Date();
                var n2 = d2.getTime();
                if((n2-tijd) < 50 ){
                    console.log("twee tegelijk....");
                }else{
                    tijd = new Date().getTime();
                    if(klikkenOfScherm == 1){
                        //68
                        //71
                        console.log("2de optie");
                        console.log(mogelijkeAntwoorden[1]);
                        $.ajax({
                            dataType: "json",
                            type: "GET",
                            url: "play/"+mogelijkeAntwoorden[1]+".wav",
                            success: function(data){
                                if(data.status == "error"){
                                    addError(data.message);
                                }
                            }
                        });

                        antwoordKnop = mogelijkeAntwoorden[1];
                        text = "2de";


                    }
                }
                tijd = new Date().getTime();
            }
            if ( e.which === 70 && tag != 'input' && tag != 'textarea' || e.which === 83 && tag != 'input' && tag != 'textarea'){
                var d3 = new Date();
                var n3 = d3.getTime();
                if((n3-tijd) < 50 ){
                    console.log("twee tegelijk....");
                }else{
                    tijd = new Date().getTime();
                    console.log("a");
                    if (klikkenOfScherm == 0) {
                        console.log(knop);
                        if (som[3] == knop) {
                            console.log("juist");
                            b_antwoord = "true";
                            som = [];
                            score++;
                            vraagNummer++;
                            if (vraagNummer == 10) {

                                HighScore();
                            }else{
                                if(level == 1){
                                    Tot10();
                                }
                                if(level == 2){
                                    Tot100();
                                }
                                if(level == 3){
                                    Tafels();
                                }
                                if(level == 4){
                                    Tot20();
                                }
                            }
                        } else {
                            console.log("fout");
                            b_antwoord = "false";
                            som = [];
                            vraagNummer++;
                            if (vraagNummer == 10) {
                                HighScore();
                            }else{
                                if(level == 1){
                                    Tot10();
                                }
                                if(level == 2){
                                    Tot100();
                                }
                                if(level == 3){
                                    Tafels();
                                }
                                if(level == 4){
                                    Tot20();
                                }
                            }
                        }
                        $(".points").html(score + " punten");
                        knop = 0;
                    }

                    //65
                    //81
                    if(klikkenOfScherm == 1){
                        console.log("q");
                        text = "groen";
                        console.log(mogelijkeAntwoorden[2]);
                        $.ajax({
                            dataType: "json",
                            type: "GET",
                            url: "play/"+mogelijkeAntwoorden[2]+".wav",
                            success: function(data){
                                if(data.status == "error"){
                                    addError(data.message);
                                }
                            }
                        });
                        antwoordKnop = mogelijkeAntwoorden[2];

                    }

                    if(startOpnieuw == 1){
                        window.location.reload();
                    }
                }
                tijd = new Date().getTime();
            }
            if ( e.which === 71 && tag != 'input' && tag != 'textarea' || e.which === 68 && tag != 'input' && tag != 'textarea'){
                var d4 = new Date();
                var n4 = d4.getTime();
                if((n4-tijd) < 50 ){
                    console.log("twee tegelijk....");
                }else{
                    tijd = new Date().getTime();
                    console.log("s");
                    console.log("Enter");
                    text = "3de";

                    if(antwoordKnop != 0) {

                        if(antwoordKnop == som[3]){
                            console.log("juist");
                            b_antwoord = "true";
                            som = [];
                            score++;
                            vraagNummer++;
                            if(vraagNummer == 10){

                                HighScore();
                            }else{
                                if(level == 1){
                                    Tot10();
                                }
                                if(level == 2){
                                    Tot100();
                                }
                                if(level == 3){
                                    Tafels();
                                }
                                if(level == 4){
                                    Tot20();
                                }
                            }
                        }else{
                            b_antwoord = "false";
                            console.log("fout");
                            som = [];
                            vraagNummer++;
                            if(vraagNummer == 10){
                                HighScore();
                            }else{
                                if(level == 1){
                                    Tot10();
                                }
                                if(level == 2){
                                    Tot100();
                                }
                                if(level == 3){
                                    Tafels();
                                }
                                if(level == 4){
                                    Tot20();
                                }
                            }
                        }
                        $(".points").html(score + " punten");
                    }else{
                        console.log("de array is leeg");
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
                    }


                    antwoordKnop = 0;
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
  };
  // This makes Knockout get to work
  var model = new Model();
  ko.applyBindings(model);
	model.fileIsModified(false);

  // Configurate toolbar handlers
  //config_file_operations("", model.fileExtension(), model.saveFileData, model.loadFileData, model.init);
});
