$(document).ready(function () {

  // data ophalen idk...
  var Userscontact = function(){
    var self = this;

    self.personName = ko.observable('');
    self.personNumber = ko.observable('');

  };

  // model
  ContactModel = function(){
    var self = this;

    self.users = ko.observable(new Userscontact());
  }

  //doorgeven???
  var viewmodel = new contactModel();
  ko.applyBindings(viewmodel);
  viewmodel.Users().



//  var person = { name: "elleneke",
//                  number: 034536326346
//    };

//    ko.applyBindings(person, document.getElementById("person"));

});
