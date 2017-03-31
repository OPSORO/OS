$(document).ready(function () {
  var GeneralSettings = function () {
    var self = this;

    self.robotName = ko.observable('');
    self.startupApp = ko.observable('');
    self.apps = ['--None--'];
    self.apps = self.apps.concat(appsJson);
  };

  var UpdateSettings = function () {
    var self = this;

    self.available = ko.observable(false);
    self.revision = ko.observable('');
    self.branch = ko.observable('');
    self.branches = ko.observable();
    self.autoUpdate = ko.observable(false);
  };

  var BehaviourSettings = function () {
    var self = this;

    self.enabled = ko.observable(false);
    self.caffeine = ko.observable(0);
    self.blink = ko.observable(false);
    self.gaze = ko.observable(false);
  };

  var AudioSettings = function () {
    var self = this;

    self.volume = ko.observable(0);
    self.ttsEngine = ko.observable('pico');
    self.ttsLanguage = ko.observable('nl');
    self.ttsGender = ko.observable('m');
  };

  var WirelessSettings = function () {
    var self = this;

    self.ssid = ko.observable('OPSORO-bot');

    self.password = ko.observable('');
    self.passwordConfirm = ko.observable('');
    self.samePassword = ko.observable(true);
    self.channel = ko.observable('0');
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

  var SecuritySettings = function () {
    var self = this;

    self.password = ko.observable('');
    self.passwordConfirm = ko.observable('');
  };

  var SettingsModel = function () {
    var self = this;

    self.general = ko.observable(new GeneralSettings());
    self.update = ko.observable(new UpdateSettings());

    self.behaviour = ko.observable(new BehaviourSettings());

    self.audio = ko.observable(new AudioSettings());

    self.wireless = ko.observable(new WirelessSettings());

    self.security = ko.observable(new SecuritySettings());
  };

  var viewmodel = new SettingsModel();
  ko.applyBindings(viewmodel);
  viewmodel.general().robotName(prefsJson.general.robotName || 'robot');
  viewmodel.general().startupApp(prefsJson.general.startupApp || '');
  // viewmodel.general().apps = appsJson;

  viewmodel.update().available(prefsJson.update.available || false);
  viewmodel.update().branches(prefsJson.update.branches || undefined);
  viewmodel.update().autoUpdate(prefsJson.update.autoUpdate || false);
  viewmodel.update().branch(prefsJson.update.branch || '');
  viewmodel.update().revision(prefsJson.update.revision || '');

  viewmodel.behaviour().enabled(prefsJson.behaviour.enabled || false);
  viewmodel.behaviour().caffeine(prefsJson.behaviour.caffeine || 0);
  viewmodel.behaviour().blink(prefsJson.behaviour.blink || false);
  viewmodel.behaviour().gaze(prefsJson.behaviour.gaze || false);

  viewmodel.audio().volume(prefsJson.audio.volume || 50);
  viewmodel.audio().ttsEngine(prefsJson.audio.ttsEngine || 'pico');
  viewmodel.audio().ttsLanguage(prefsJson.audio.ttsLanguage || 'nl');
  viewmodel.audio().ttsGender(prefsJson.audio.ttsGender || 'm');

  viewmodel.wireless().ssid(prefsJson.wireless.ssid || 'OPSORO-bot');
  viewmodel.wireless().samePassword(prefsJson.wireless.samePassword || true);
  viewmodel.wireless().channel(prefsJson.wireless.channel || 6);
  viewmodel.wireless().settingsChanged(false);

  // console.log('loaded');
  // console.log(viewmodel.general().apps);

});
