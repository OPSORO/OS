define("ace/mode/onolua_highlight_rules", function(require, exports, module) {

var oop = require("ace/lib/oop");
var LuaHighlightRules = require("ace/mode/lua_highlight_rules").LuaHighlightRules;

var OnoLuaHighlightRules = function() {
	var functions = (
		// Arduino-like functions
		"setup|loop|quit|print|sleep|rising_edge|falling_edge|seconds|delay|min|"+
		"max|abs|constrain|map|millis|"+

		// UI class methods
		"init|add_button|add_key|is_button_pressed|is_key_pressed|"+

		// Hardware class methods
		"ping|reset|led_on|led_off|I2C:detect|I2C:read8|I2C:write8|I2C:read16|"+
		"I2C:write16|Servo:init|Servo:enable|Servo:disable|Servo:neutral|"+
		"Servo:set|Servo:set_all|Capacitive:init|Capacitive:set_threshold|"+
		"Capacitive:get_filtered_data|Capacitive:get_baseline_data|Capacitive:get_touched|"+
		"Capacitive:set_gpio_pinmode|Capacitive:read_gpio|Capacitive:write_gpio|Neopixel:init|Neopixel:enable|"+
		"Neopixel:disable|Neopixel:set_brightness|Neopixel:show|Neopixel:set_pixel|Neopixel:set_range|"+
		"Neopixel:set_all|Neopixel:set_pixel_hsv|Neopixel:set_range_hsv|Neopixel:set_all_hsv|"+
		"Analog:read_channel|Analog:read_all_channels|"+

		// Sound class methods
		"say_tts|play_file|"+

		// Expression class methods
		// "get_emotion_complex|set_emotion_r_phi|set_emotion_val_ar|update|empty_config|load_config|dofs|add_overlay|remove_overlay|clear_overlays|"+
		"get_emotion_complex|set_emotion_e|set_emotion_r_phi|set_emotion_val_ar|update|"+

		// Robot class methods
		"set_dof_value|set_dof_values|"+

		// Animate class methods
		"has_ended"

		// new? DOF or Servo classes?
	);

	this.$rules = new LuaHighlightRules().getRules();

	// Insert new rules just before Lua keyword map
	this.$rules.start.splice(-5, 0,
		{
			token: "support.function",
			regex: functions
		},
		{
			token: "constant.library",
			regex: "UI|Hardware|Sound|Expression|Robot|AnimatePeriodic|Animate|Serial"
		}
	);

	this.normalizeRules();

}

oop.inherits(OnoLuaHighlightRules, LuaHighlightRules);

exports.OnoLuaHighlightRules = OnoLuaHighlightRules;
});
