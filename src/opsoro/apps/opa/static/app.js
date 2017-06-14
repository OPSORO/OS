$(document).ready(function() {

     
    //Websockets
    conn = null;
    connReady = false;
    conn = new SockJS('http://' + window.location.host + '/sockjs');

    conn.onopen = function(){
      console.log("SockJS connected.");
      $.ajax({
        url: "/sockjstoken/",
        cache: false
      }).done(function(data) {
        
        if ('formatted_name' in app_data) {
            appname = app_data['formatted_name'];
            console.log(appname)
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
    
    conn.onmessage = function(e) {
        var applet = $('.activity').first().clone();
        var data = JSON.parse(e.data);
        if(data.hasOwnProperty('data'))
        {
        if(data.data.action == "MessageInComing"){
            applet.find(".date-time").empty().append(data.data.date + " " + data.data.time);
            applet.find(".activity_service").empty().append(data.data.service);
            applet.find(".activity_content").css("background-color", data.data.color);
            applet.removeClass("bounceIn").addClass("bounceInRight");
            applet.find(".icon").addClass("animated rotateIn")
            $(".activities").append(applet);
        }
        if(data.data.action == "MessageCommand"){
            if(data.data.data == "Remove"){
                $('#cmdqueue').find('.command:first').remove();
            }
        }
        if(data.data.action == "MessageResponse"){
            console.log(data.data.data)
        }
        }
    };   

    conn.onclose = function() {
            console.log("SockJS disconnected.");
            conn = null;
            connReady = false;
    };

    //JQuery UI
    /*
    $('#cmdqueue').sortable({
        revert: true,
        placeholder: "highlight command",
        cancel: ".disabled",
        stop: function ( event, ui){
            
            var data = $(this).sortable('toArray', { attribute: 'command-id' });
            conn.send(JSON.stringify({
                action: "command",
                data: data
            }));
            
        }
    });
    $('#sortable').disableSelection();
    $('.draggable').draggable({
            connectToSortable: "#cmdqueue",
            helper: "clone",
            revert: "invalid",
            start:  function (event,ui){
                return true;
            },
            drag: function (event,ui){
                $(this).removeClass('bounceIn')
            },
            stop: function (event,ui){
                $(this).addClass('bounceIn')
            }
    });
    $('#cmdqueue').droppable({
      drop: function( event, ui ) {
        $('#cmdqueue-placeholder').find('p').addClass("hidden");
      }
    });

    
    $('#cmdqueue').on('click', '.command', function() {      
        this.parentNode.removeChild(this);
    });
    */
    $('#filters').accordion({
      collapsible: true
    });
    $('input').click(function(event) {
        event.preventDefault();
    });
    $('#cmdgrid').on('dblclick', '.command', function() {
        //command clonen naar de command queue
        //eerste clone nemen van de selected value voor reactie
        var expression = $(this).find('.expression').val()
        var sound = $(this).find('.sound').val()
        var command = $(this).clone().appendTo('#cmdqueue');
        command.find('.expression').val(expression);
        command.find('.sound').val(sound);
        command.uniqueId();
        $('#cmdqueue-placeholder').find('p').addClass("hidden");
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
        /*
        $.ajax({
            type: "POST",
            url: "/apps/opa/addcommand",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: JSON.stringify(data)
        });*/
    });
    $('#cmdqueue').on('click', '.command', function() {      
        this.parentNode.removeChild(this);
        data = {
            'id': $(this).attr('id')
        }
        conn.send(JSON.stringify({
                action: "remove-command",
                data: data
        }));
    });

    
    //Knockout JS
    var Model = function() {
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
        self.toggleLocked = function() {
            if (self.fileIsLocked()) {
                self.unlockFile();
            } else {
                self.lockFile();
            }
        };
        self.lockFile = function() {
            self.fileIsLocked(true);
            self.fileStatus("Locked")
        };
        self.unlockFile = function() {
            self.fileIsLocked(false);
            self.fileStatus("Editing")
        };

        

        // Popup window
        /*
        self.popupTextInput = ko.observable("Hi! This text can be changed. Click on the button to change me!");
        self.showPopup = function() {
          $("#popup_window").foundation('open');

        };
        self.closePopup = function() {
            $("#popup_window").foundation('close');
        };
        self.popupButtonHandler = function() {
            self.closePopup();
        };

        self.init = function() {
            // Clear data, new file, ...
            self.fileName("Untitled");
            self.unlockFile();
            self.fileIsModified(false);
        };

        self.loadFileData = function(data) {
            if (data == undefined) {
                return;
            }

            // Load data, parse if needed
            var dataobj = JSON.parse(data);


            self.fileIsModified(false);
            self.lockFile();
        };

        self.saveFileData = function() {
            // Convert data
            file_data = {};

            var data = ko.toJSON(file_data, null, 2);
            self.fileIsModified(false);
            return data;
        };
        */
    };

    function Applet(Applet_name, Applet_url, Applet_color, Applet_categorie, Applet_logo) {
        this.Applet_name = Applet_name;
        this.Applet_url = Applet_url;
        this.Applet_color = Applet_color;
        this.Applet_categorie = Applet_categorie;
        this.Applet_logo = Applet_logo;
    }

    function Command(Command_id,Command_name,Command_color,Command_description,Command_uses
    ,Command_type,Command_eventname,Command_customizeable,Command_expressions,Command_selectedReaction,Command_say
    ,Command_saySomething,Command_sounds,Command_selectedSound,Command_displaySoundOptions,Command_displayOptions,Command_message) {
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

    function Expression(Expression_name){
        this.Expression_name = Expression_name;
    }

    var listOfApplets = [];
    var listOfCommands = [];
    var listOfExpressions = [];
    var listOfSounds = [];
    var queue = [];

    $.when(
        $.get( "/apps/opa/getapplets", function( data ) {
            $(data['Applets']).each(function(index, item){
                listOfApplets.push(new Applet(item.Applet_name, item.Applet_url, item.Applet_color, item.Applet_categorie, item.Applet_logo));            
            });
        }),

        $.get( "/apps/opa/getreactions", function( data ) {
            $(data['expressions']).each(function(index, item){
                listOfExpressions.push(item.name);
            });
        }),

        $.get( "/apps/opa/getsounds", function( data ) {
            console.log("get sounds");
            $(data['sounds']).each(function(index, item){
                listOfSounds.push(item);
            });
        }),

        $.get( "/apps/opa/getcommands", function( data ) {
            console.log("get commands");
            //default waarden meegeven
            $(data['Commands']).each(function(index, item){
                listOfCommands.push(new Command(item.Command_id,item.Command_name,item.Command_color
                ,item.Command_description,item.Command_uses,item.Command_type,
                item.Command_eventname,item.Command_customizeable,listOfExpressions,
                "neutral",item.Command_say,true,listOfSounds,"1_kamelenrace.wav",false,false,""));
            });
        })

    ).then(function(){
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
        viewModel.filteredCommands = ko.computed(function (){
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
            var selectedProtocols = ko.utils.arrayFilter(viewModel.protocol(), function (p) {
                return p.selected();
            });
            if (selectedProtocols.length == 0) { //if none selected return all
                //console.log("selected is null");
                //console.log(selectedProtocols.length);
                //console.log(viewModel.protocoldocs());
                return viewModel.protocoldocs();
            }
            else { 
                return ko.utils.arrayFilter(viewModel.protocoldocs(), function (item) {
                return ko.utils.arrayFilter(selectedProtocols, function (p) {
                    if(p.name == 'All'){
                        return viewModel.protocoldocs();
                    }
                    return p.name == item.Applet_categorie
                }).length > 0;
            });
            
            }
        })
        
        ko.bindingHandlers.visibleAndSelect = {
            update: function(element, valueAccessor) {
                ko.bindingHandlers.visible.update(element, valueAccessor);
                if (valueAccessor()) {
                    setTimeout(function() {
                        $(element).find("input").focus().select();
                    }, 0); //new tasks are not in DOM yet
                }
            }
        };

        viewModel.commandQuery.subscribe(viewModel.search);
        console.log(viewModel.commands())
        ko.applyBindings(viewModel);
        
    });


    
    
    /*
    $.get("/apps/opa/getapplets", function(data, status){
        var i =0;
         $(data['Applets']).each(function(index, item){
            
           listOfApplets.push(new Applet(item.Applet_name, item.Applet_url, item.Applet_color, item.Applet_categorie, item.Applet_logo));
          
       });
    });
*/
    

    //var newDropped = false;
   
    //ko.applyBindings(viewModel, $("#protocoldocs")[0]);
    // This makes Knockout get to work
   // ko.applyBindings(model);
    
    // Configurate toolbar handlers
    //config_file_operations("", model.fileExtension(), model.saveFileData, model.loadFileData, model.init);
});
