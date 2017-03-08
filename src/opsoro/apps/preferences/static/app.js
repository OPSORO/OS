$(document).ready(function () {
  var GeneralSettings = function () {
    var self = this;

    self.robotName = ko.observable("");
    self.password = ko.observable("");
    self.passwordConfirm = ko.observable("");
  };

  var UpdateSettings = function () {
    var self = this;

    self.available = ko.observable(false);
    self.branch = ko.observable("");
    self.branches = ko.observable();
    self.autoUpdate = ko.observable(false);
  };

  var AliveSettings = function () {
    var self = this;

    self.enabled = ko.observable(false);
    self.aliveness = ko.observable(0);
    self.blink = ko.observable(false);
    self.gaze = ko.observable(false);
  };

  var AudioSettings = function () {
    var self = this;

    self.volume = ko.observable(0);
    self.ttsEngine = ko.observable("pico");
    self.ttsLanguage = ko.observable("nl");
    self.ttsGender = ko.observable("m");
  };

  var WirelessSettings = function () {
    var self = this;

    self.ssid = ko.observable("OPSORO-bot");

    self.password = ko.observable("");
    self.passwordConfirm = ko.observable("");
    self.samePassword = ko.observable(true);
    self.channel = ko.observable("0");
    self.settingsChanged = ko.observable(false);

    var changed_fn = function () {
      self.settingsChanged(true);
    };
    self.ssid.subscribe(changed_fn);
    self.password.subscribe(changed_fn);
    self.samePassword.subscribe(changed_fn);
    self.channel.subscribe(changed_fn);
    self.settingsChanged(false);
  };

  var SettingsModel = function () {
    var self = this;

    self.general = ko.observable(new GeneralSettings());
    self.update = ko.observable(new UpdateSettings());
    self.alive = ko.observable(new AliveSettings());
    self.audio = ko.observable(new AudioSettings());
    self.wireless = ko.observable(new WirelessSettings());
  };

  var viewmodel = new SettingsModel();
  ko.applyBindings(viewmodel);
  viewmodel.general().robotName(prefsJson.general.robotName || "Ono");

  viewmodel.update().available(prefsJson.update.available || false);
  viewmodel.update().branches(prefsJson.update.branches || undefined);
  viewmodel.update().autoUpdate(prefsJson.update.autoUpdate || false);
  viewmodel.update().branch(prefsJson.update.branch || '');

  viewmodel.alive().enabled(prefsJson.alive.enabled || false);
  viewmodel.alive().aliveness(prefsJson.alive.aliveness || 0);
  viewmodel.alive().blink(prefsJson.alive.blink || false);
  viewmodel.alive().gaze(prefsJson.alive.gaze || false);

  viewmodel.audio().volume(prefsJson.audio.volume || 50);
  viewmodel.audio().ttsEngine(prefsJson.audio.ttsEngine || "pico");
  viewmodel.audio().ttsLanguage(prefsJson.audio.ttsLanguage || "nl");
  viewmodel.audio().ttsGender(prefsJson.audio.ttsGender || "m");

  viewmodel.wireless().ssid(prefsJson.wireless.ssid || "OPSORO-bot");
  viewmodel.wireless().samePassword(prefsJson.wireless.samePassword || true);
  viewmodel.wireless().channel(prefsJson.wireless.channel || 6);
  viewmodel.wireless().settingsChanged(false);

  // Fix foundation not updating sliders
  $('.tab-title').click(function(){
    $(document).foundation('slider', 'reflow');
  });
});
