$(document).ready(function () {

    $("#slideshow > div:gt(0)").hide();

    $('.next').click(function () {
        $('#slideshow > div:first')
            .fadeOut(0)
            .next()
            .fadeIn(0)
            .end()
            .appendTo('#slideshow');
    })

    //Websockets
    conn = null;
    connReady = false;
    conn = new SockJS('http://' + window.location.host + '/sockjs');

    conn.onopen = function () {
        console.log("SockJS connected.");
        $.ajax({
            url: "/sockjstoken/",
            cache: false
        }).done(function (data) {

            if ('formatted_name' in app_data) {
                appname = app_data['formatted_name'];
            }

            conn.send(JSON.stringify({
                app: appname,
                action: "authenticate",
                token: data
            }));
            connReady = true;
            console.log("SockJS authenticated.");
        });
    };

    conn.onmessage = function (e) {
        var applet = $('.activity').first().clone();
        var data = JSON.parse(e.data);
        if (data.hasOwnProperty('data')) {
            if (data.data.action == "MessageInComing") {
                applet.find(".date-time").empty().append(data.data.date + " " + data.data.time);
                applet.find(".activity_service").empty().append(data.data.service);
                applet.find(".activity_content").css("background-color", data.data.color);
                applet.removeClass("bounceIn").addClass("bounceInRight");
                applet.find(".icon").addClass("animated rotateIn")
                $(".activities").append(applet);
            }
            if (data.data.action == "MessageCommand") {
                if (data.data.data == "Remove") {
                    $('#cmdqueue').find('.command:first').remove();
                }
            }
            if (data.data.action == "MessageResponse") {
                console.log(data.data.data)
            }
        }
    };

    conn.onclose = function () {
        console.log("SockJS disconnected.");
        conn = null;
        connReady = false;
    };

    /* JQuery UI */
    $('#filters').accordion({
        collapsible: true
    });
    $('#cmdgrid').on('dblclick', '.command', function () {
        //command clonen naar de command queue
        //eerste clone nemen van de selected value voor reactie
        var expression = $(this).find('.expression').val()
        var sound = $(this).find('.sound').val()
        var command = $(this).clone().appendTo('#cmdqueue');
        command.find('.expression').val(expression);
        command.find('.sound').val(sound);
        command.uniqueId();
        console.log(command.find('.type').val())
        data = {
            'id': command.attr('id'),
            'command-id': command.attr('command-id'),
            'command-message': command.find('.message').val(),
            'command-type': command.find('.type').val(),
            'command-eventname': command.find('.eventname').val(),
            'command-expression': expression,
            'command-hasTTS': command.find('.tts').is(':checked'),
            'command-say': command.find('.say').val(),
            'command-hasSound': command.find('.playSound').is(':checked'),
            'command-sound': command.find('.sound').val()
        }

        conn.send(JSON.stringify({
            action: "command",
            data: data
        }));

    });
    $('#cmdqueue').on('click', '.command', function () {
        this.parentNode.removeChild(this);
        data = {
            'id': $(this).attr('id')
        }
        conn.send(JSON.stringify({
            action: "remove-command",
            data: data
        }));
    });

    /* KNOCKOUT */
    function Applet(Applet_id, Applet_name, Applet_url, Applet_color, Applet_categorie, Applet_logo) {
        this.Applet_id = Applet_id;
        this.Applet_name = Applet_name;
        this.Applet_url = Applet_url;
        this.Applet_color = Applet_color;
        this.Applet_categorie = Applet_categorie;
        this.Applet_logo = Applet_logo;
    }

    function Command(Command_id, Command_name, Command_color, Command_description, Command_uses
        , Command_type, Command_eventname, Command_customizeable, Command_expressions, Command_selectedReaction, Command_say
        , Command_saySomething, Command_sounds, Command_selectedSound, Command_displaySoundOptions, Command_displayOptions, Command_message) {
        this.Command_id = Command_id;
        this.Command_name = Command_name;
        this.Command_color = Command_color;
        this.Command_description = Command_description;
        this.Command_uses = Command_uses;
        this.Command_type = Command_type;
        this.Command_eventname = Command_eventname;
        this.Command_customizeable = Command_customizeable;
        this.Command_expressions = Command_expressions;
        this.Command_selectedReaction = ko.observable(Command_selectedReaction);
        this.Command_say = Command_say;
        this.Command_saySomething = Command_saySomething;
        this.Command_sounds = Command_sounds;
        this.Command_selectedSound = ko.observable(Command_selectedSound);
        this.Command_displaySoundOptions = ko.observable(Command_displaySoundOptions);
        this.Command_displayOptions = ko.observable(Command_displayOptions);
        this.Command_message = ko.observable(Command_message);
    }

    function NewApplet() {
        this.NewApplet_id = ko.observable('');
        this.NewApplet_name = ko.observable('');
        this.NewApplet_url = ko.observable('');
        this.NewApplet_categorie = ko.observable('');
        this.NewApplet_logo = ko.observable('');
    }

    var listOfApplets = [];
    var listOfCommands = [];
    var listOfExpressions = [];
    var listOfSounds = [];
    var queue = [];

    $.when(
        $.get("/apps/opa/getapplets", function (data) {
            $(data['Applets']).each(function (index, item) {
                listOfApplets.push(new Applet(item.Applet_id, item.Applet_name, item.Applet_url, item.Applet_color, item.Applet_categorie, item.Applet_logo));
            });
        }),

        $.get("/apps/opa/getreactions", function (data) {
            $(data['expressions']).each(function (index, item) {
                listOfExpressions.push(item.name);
            });
        }),

        $.get("/apps/opa/getsounds", function (data) {
            $(data['sounds']).each(function (index, item) {
                listOfSounds.push(item);
            });
        }),

        $.get("/apps/opa/getcommands", function (data) {
            //default waarden meegeven
            $(data['Commands']).each(function (index, item) {
                listOfCommands.push(new Command(item.Command_id, item.Command_name, item.Command_color
                    , item.Command_description, item.Command_uses, item.Command_type,
                    item.Command_eventname, item.Command_customizeable, listOfExpressions,
                    "neutral", item.Command_say, true, listOfSounds, "1_kamelenrace.wav", false, false, ""));
            });
        })

    ).then(function () {
        console.log("ready")
        $(".applet").removeClass("hidden");

        function protocol(id, name) {
            this.id = id;
            this.name = name;
            this.selected = ko.observable(false);
        }

        var listOfCategories = [
            new protocol(1, 'Social'),
            new protocol(2, 'News'),
            new protocol(3, 'Location'),
            new protocol(4, 'Tools'),
            new protocol(5, 'Email'),
            new protocol(6, 'Calendar')
        ];


        var viewModel = {
            commands: ko.observableArray(listOfCommands),
            commandQuery: ko.observable(""),
            appletQuery: ko.observable(""),
            newApplet: NewApplet,
            colorpicker: ko.observable('orange'),
            protocoldocs: ko.observableArray(listOfApplets),
            protocol: ko.observableArray(listOfCategories),
            selectedProtocol: ko.observableArray(),
            addprotocol: function (protocol, elem) {
                var $checkBox = $(elem.srcElement);
                var isChecked = $checkBox.is(':checked');
                //If it is checked and not in the array, add it
                if (isChecked && viewModel.selectedProtocol.indexOf(protocol) < 0) {
                    viewModel.selectedProtocol.push(protocol);
                }
                //If it is in the array and not checked remove it
                else if (!isChecked && viewModel.selectedProtocol.indexOf(protocol) >= 0) {
                    viewModel.selectedProtocol.remove(protocol);
                }
                //Need to return to to allow the Checkbox to process checked/unchecked
                return true;
            }
        }
        viewModel.speechChanged = function (data) {
            if ($('#speechStartStop').is(':checked')) {
                if (!recognizer) {
                    Setup();
                }
                RecognizerStart(SDK, recognizer);
                Start();
            }
            else {
                RecognizerStop(SDK, recognizer);
                Stop();
            }
        }


        viewModel.addApplet = function (form) {

            var unique_id = new Date().getTime();
            var a = new Applet(
                unique_id,
                viewModel.newApplet.NewApplet_name,
                'https://ifttt.com/applets/' + viewModel.newApplet.NewApplet_url + '/embed?redirect_uri=http://opa.eu.ngrok.io/apps/opa/',
                viewModel.colorpicker(),
                viewModel.newApplet.NewApplet_categorie.name,
                'static/images/opsoro_icon_light.png'
            )
            viewModel.protocoldocs.push(a);
            data = {
                'applet': a
            }
            conn.send(JSON.stringify({
                action: "saveapplet",
                data: data
            }));
        };

        viewModel.clearFilters = function () {
            var selectedProtocols = ko.utils.arrayFilter(viewModel.protocol(), function (p) {
                return p.selected(false);
            });
        };

        viewModel.filteredCommands = ko.computed(function () {
            var filter = viewModel.commandQuery().toLowerCase();

            if (!filter) {
                return viewModel.commands();
            } else {
                return ko.utils.arrayFilter(viewModel.commands(), function (item) {
                    return item['Command_name'].toLowerCase().indexOf(filter) !== -1;
                });
            }
        });

        viewModel.filteredProtocols = ko.computed(function () {
            var filter = viewModel.appletQuery().toLowerCase();
            var selectedProtocols = ko.utils.arrayFilter(viewModel.protocol(), function (p) {
                return p.selected();
            });
            if (selectedProtocols.length == 0 && filter == "") { //if none selected return all
                return viewModel.protocoldocs();
            }
            else if (selectedProtocols.length > 0 && filter == "") {
                return ko.utils.arrayFilter(viewModel.protocoldocs(), function (item) {
                    return ko.utils.arrayFilter(selectedProtocols, function (p) {
                        if (p.name == 'All') {
                            return viewModel.protocoldocs();
                        }
                        return p.name == item.Applet_categorie
                    }).length > 0;
                });

            }
            else {
                return ko.utils.arrayFilter(viewModel.filteredProtocols(), function (item) {
                    return item['Applet_name'].toLowerCase().indexOf(filter) !== -1;
                });
            }
        })

        ko.bindingHandlers.visibleAndSelect = {
            update: function (element, valueAccessor) {
                ko.bindingHandlers.visible.update(element, valueAccessor);
                if (valueAccessor()) {
                    setTimeout(function () {
                        $(element).find("input").focus().select();
                    }, 0); //new tasks are not in DOM yet
                }
            }
        };

        viewModel.commandQuery.subscribe(viewModel.search);
        ko.applyBindings(viewModel);

        viewModel.showPopup = function () {
            $("#popup_window").foundation('open');

        };
        viewModel.closePopup = function () {
            $("#popup_window").foundation('close');
        };

        $('#addApplet').removeClass('hidden');
        $('#addApplet').appendTo('#appletsGrid');


        document.getElementById("copyButton").addEventListener("click", function () {
            copyToClipboard(document.getElementById("copyTarget"));
        });

        function copyToClipboard(elem) {
            // create hidden text element, if it doesn't already exist
            var targetId = "_hiddenCopyText_";
            var isInput = elem.tagName === "INPUT" || elem.tagName === "TEXTAREA";
            var origSelectionStart, origSelectionEnd;
            if (isInput) {
                // can just use the original source element for the selection and copy
                target = elem;
                origSelectionStart = elem.selectionStart;
                origSelectionEnd = elem.selectionEnd;
            } else {
                // must use a temporary form element for the selection and copy
                target = document.getElementById(targetId);
                if (!target) {
                    var target = document.createElement("textarea");
                    target.style.position = "absolute";
                    target.style.left = "-9999px";
                    target.style.top = "0";
                    target.id = targetId;
                    target.value = "http://opsoro:spotify123@opa.eu.ngrok.io/apps/opa/action"
                    document.body.appendChild(target);
                }
            }
            // select the content
            var currentFocus = document.activeElement;
            target.focus();
            target.setSelectionRange(0, target.value.length);

            // copy the selection
            var succeed;
            try {
                succeed = document.execCommand("copy");
            } catch (e) {
                succeed = false;
            }
            // restore original focus
            if (currentFocus && typeof currentFocus.focus === "function") {
                currentFocus.focus();
            }

            if (isInput) {
                // restore prior selection
                elem.setSelectionRange(origSelectionStart, origSelectionEnd);
            } else {
                // clear temporary content
                target.textContent = "";
            }
            return succeed;
        }

        /* SPEECH */
        var SDK;
        var recognizer;
        var key = "98d77b29792e489db96b5094d29b34e5";
        var language = "en-US";
        var format = "Simple";
        var speechresult;

        // voor een of andere reden is deze checked bij load dus unchecken
        $('#speechStartStop').removeAttr('checked');

        // Laden speech browser sdk met require
        function Initialize(onComplete) {
            require(["Speech.Browser.Sdk"], function (SDK) {
                onComplete(SDK);
            });
        }

        // Setup recongizer
        function RecognizerSetup(SDK, recognitionMode, language, format, subscriptionKey) {
            var recognizerConfig = new SDK.RecognizerConfig(
                new SDK.SpeechConfig(
                    new SDK.Context(
                        new SDK.OS(navigator.userAgent, "Browser", null),
                        new SDK.Device("Raspberry Pi Foundation", "Raspberry Pi 3", "8"))),
                recognitionMode,
                language,
                format);

            // authenticatie
            var authentication = new SDK.CognitiveSubscriptionKeyAuthentication(subscriptionKey);

            return SDK.CreateRecognizer(recognizerConfig, authentication);
        }

        // Start recognition
        function RecognizerStart(SDK, recognizer) {
            recognizer.Recognize((event) => {

                // de verschillende events van speech recognition
                switch (event.Name) {
                    case "RecognitionTriggeredEvent":
                        UpdateStatus("Initializing");
                        break;
                    case "ListeningStartedEvent":
                        UpdateStatus("Listening");
                        robotSendSound("smb_1-up.wav");
                        break;
                    case "RecognitionStartedEvent":
                        UpdateStatus("Recognizing");
                        break;
                    case "SpeechStartDetectedEvent":
                        UpdateStatus("Speech detected");
                        break;
                    case "SpeechHypothesisEvent":
                        UpdateRecognizedHypothesis(event.Result.Text);
                        break;
                    case "SpeechEndDetectedEvent":
                        UpdateStatus("Processing");
                        break;
                    case "SpeechSimplePhraseEvent":
                        if (event.Result.RecognitionStatus != "Success") {
                            robotSendTTS("Sorry, I didn't understand what you said.");
                            UpdateStatus("Idle")
                            Stop();
                        } else {
                            speechresult = event.Result.DisplayText;
                        }
                        break;
                    case "RecognitionEndedEvent":
                        OnComplete();
                        UpdateStatus("Idle");
                        break;
                }
            })
                .On(() => {
                    //request succes
                },
                (error) => {
                    console.error(error);
                    UpdateStatus("Error")
                });
        }

        // Stop the Recognition.
        function RecognizerStop(SDK, recognizer) {
            recognizer.AudioSource.TurnOff();

        }
        function Setup() {
            recognizer = RecognizerSetup(SDK, SDK.RecognitionMode.Interactive, language, SDK.SpeechResultFormat[format], key);
        }

        function Start() {
            $('#speechIndicator').removeClass('fa fa-microphone')
            $('#speechIndicator').addClass('fa fa-microphone-slash animated infinite pulse recording')
        }

        function Stop() {
            $('#speechIndicator').removeClass('fa fa-microphone-slash animated infinite pulse recording')
            $('#speechIndicator').addClass('fa fa-microphone')
        }

        function UpdateStatus(status) {
            $('#speechStatus').html(status);
        }
        function UpdateRecognizedHypothesis(text) {
            $('#speechHypothesis').html(text);
        }
        
        function OnComplete() {
            var isUnderstood = false;
            // kijken welk command we moeten geven door te vergelijken met de speech command
            $.each(listOfCommands, function (index, value) {
                var compare = value['Command_description'].replace(/[^a-zA-Z ]/g, "").toString().toLowerCase();
                var result = speechresult.replace(/[^a-zA-Z ]/g, "").toString().toLowerCase();
                if(result.indexOf(compare) !== -1){
                    var n = result.split(compare)
                    if(value['Command_customizeable']){
                        $("#"+value['Command_id']).find('.message').val(n[1])
                    }
                    $( "#"+value['Command_id'] ).dblclick();
                    isUnderstood = true;
                }
            });
            if(!isUnderstood){
                robotSendTTS("Sorry, I didn't understand what you said.");
            }
            $('#speechStartStop').prop("checked", false);
            Stop();
        }
        
        Initialize(function (speechSdk) {
            SDK = speechSdk;
            $('.voice').removeClass('hidden');
        });
    });

});
