$(document).ready(function() {

    
    var commandData;
    $.ajax({
        url: "/apps/opa/getcommands",
        cache: false
    }).done(function(data){
        commandData = data.Commands
        console.log(commandData);
    });
    
    //Websockets
    conn = null;
    connReady = false;
    conn = new SockJS('http://' + window.location.host + '/appsockjs');

    conn.onopen = function() {
            console.log("SockJS connected.");
            $.ajax({
                url: "/appsockjstoken",
                cache: false
            }).done(function(data) {
                conn.send(JSON.stringify({
                    action: "authenticate",
                    token: data
                }));
                
                connReady = true;
                console.log("SockJS authenticated.");
            });
    };
    conn.onmessage = function(e) {
        var data = JSON.parse(e.data)
        if(data['data'] == "Remove"){
            $('#cmdqueue').find('.command:first').remove();
        }
    };   

    conn.onclose = function() {
            console.log("SockJS disconnected.");
            conn = null;
            connReady = false;
    };

    //JQuery UI
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

    $('#filters').accordion({
      collapsible: true
    });
    $('#cmdqueue').on('click', '.command', function() {      
        this.parentNode.removeChild(this);
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
    

    /*var listOfApplets = [
        new Applet("Test", "fkdsjfsdkf", "#000000", "News", "dlkjfskldjfsd"),
        new Applet("Test", "fkdsjfsdkf", "#000000", "News", "dlkjfskldjfsd"),
        new Applet("Test", "fkdsjfsdkf", "#000000", "News", "dlkjfskldjfsd"),
        new Applet("Test", "fkdsjfsdkf", "#000000", "News", "dlkjfskldjfsd"),   
    ];*/

    var listOfApplets = [ 

    ];
  
   $.ajax({
        url: "/apps/opa/getapplets",
        cache: false
    }).done(function(data){

    $(data['Applets']).each(function(index, item){
            
           listOfApplets.push(new Applet(item.Applet_name, item.Applet_url, item.Applet_color, item.Applet_categorie, item.Applet_logo));
          
       });      
    
    $(".applet").removeClass("hidden");

    console.log(listOfApplets);
     function protocol(id, name) {
    this.id = id;
    this.name = name;
    this.selected = ko.observable(false);
    }

    var listOfCategories = [
        new protocol(1, 'Social'),
        new protocol(2, 'News'),
        new protocol(3, 'Education'),
        new protocol(4, 'Location'),
        new protocol(5, 'Tools'),
    ];

    
    var viewModel = {
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

    viewModel.filteredProtocols = ko.computed(function () {
        var selectedProtocols = ko.utils.arrayFilter(viewModel.protocol(), function (p) {
            return p.selected();
        });
        if (selectedProtocols.length == 0) { //if none selected return all
            console.log("selected is null");
            console.log(selectedProtocols.length);
            console.log(viewModel.protocoldocs());
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
