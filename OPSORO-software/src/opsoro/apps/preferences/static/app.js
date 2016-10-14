$(document).ready(function () {
  var GeneralSettings = function () {
    var self = this;

    self.robotName = ko.observable("");
    self.password = ko.observable("");
    self.passwordConfirm = ko.observable("");
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
    self.audio = ko.observable(new AudioSettings());
    self.wireless = ko.observable(new WirelessSettings());
  };

  var viewmodel = new SettingsModel();
  ko.applyBindings(viewmodel);
  viewmodel.general().robotName(prefsJson.general.robotName || "Ono");
  viewmodel.audio().volume(prefsJson.audio.volume || 50);
  viewmodel.audio().ttsEngine(prefsJson.audio.ttsEngine || "pico");
  viewmodel.audio().ttsLanguage(prefsJson.audio.ttsLanguage || "nl");
  viewmodel.audio().ttsGender(prefsJson.audio.ttsGender || "m");
  viewmodel.wireless().ssid(prefsJson.wireless.ssid || "OPSORO-bot");
  viewmodel.wireless().samePassword(prefsJson.wireless.samePassword || true);
  viewmodel.wireless().channel(prefsJson.wireless.channel || 6);
  viewmodel.wireless().settingsChanged(false);
});
