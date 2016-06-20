$(document).ready(function(){
  $("a.btnDelSnd").click(function(){
    filename = $(this).closest("span.file").data("soundfile");
    fileElem = $(this).closest("span.file")
    $.ajax({
      dataType: "json",
      type: "POST",
      url: "delete/" + filename,
      success: function(data){
        if(data.status == "error"){
          addError(data.message);
        }else{
          addMessage(data.message);
          fileElem.hide();
        }
      }
    });
  });
  $("a.btnPlaySnd").click(function(){
    filename = $(this).closest("span.file").data("soundfile");
    $.ajax({
      dataType: "json",
      type: "GET",
      url: "play/" + filename,
      success: function(data){
        if(data.status == "error"){
          addError(data.message);
        }
      }
    });
  });

  $("#formTTS").submit(function(e){
    e.preventDefault();
  });
  $("#btnTTS").click(doTTS);
  $("#txtTTS").bind("keydown", function(e) {
    if (e.keyCode == 13) {
      doTTS();
    }
  });
  
  var Model = function(){
    var self = this;

    self.fileName = ko.observable("recording");
    self.isUploading = ko.observable(false);
    self.isRecordingEnabled = ko.observable(false);
    self.isRecording = ko.observable(false);
    self.isRecorded = ko.observable(false);

    self.enableRecording = function(){
      initAudio();
      self.isRecordingEnabled(true);
    };
    self.toggleRecording = function(){
      if (toggleRecording( self.isRecording() )) {
        self.isRecording( !self.isRecording() );
        if (!self.isRecording()){
          self.isRecorded(true);
        }
      }
    };

    self.saveRecording = function(){
      saveAudio("demo");
    };

    self.uploadRecording = function(){
      self.isUploading(true);
      var formData = new FormData();
      formData.append("soundfile", currentBlob, self.fileName() + ".wav");
      var xhr = new XMLHttpRequest();
      xhr.open('POST', 'upload', true);

      // Set up a handler for when the request finishes.
      xhr.onload = function () {
        if (xhr.status === 200) {
          // File(s) uploaded.
          addMessage('Upload complete.');
          setTimeout(function () {
            // Reload page
            history.go(0);
          }, 1000);
        } else {
          addError('An error occurred while uploading the recording.');
        }
        self.isUploading(false);
      };
      // Send the Data.
      xhr.send(formData);
    };

  };
  // This makes Knockout get to work
  var model = new Model();
  ko.applyBindings(model);
});
