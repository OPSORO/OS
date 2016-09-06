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
		"ping|reset|led_on|led_off|i2c_detect|i2c_read8|i2c_write8|i2c_read16|"+
		"i2C_write16|servo_init|servo_enable|servo_disable|servo_neutral|"+
		"servo_set|servo_set_all|cap_init|cap_set_threshold|"+
		"cap_get_filtered_data|cap_get_baseline_data|cap_get_touched|"+
		"cap_set_gpio_pinmode|cap_read_gpio|cap_write_gpio|neo_init|neo_enable|"+
		"neo_disable|neo_set_brightness|neo_show|neo_set_pixel|neo_set_range|"+
		"neo_set_all|neo_set_pixel_hsv|neo_set_range_hsv|neo_set_all_hsv|"+
		"ana_read_channel|ana_read_all_channels|"+

		// Sound class methods
		"say_tts|play_file|"+

		// Expression class methods
		"get_emotion_complex|set_emotion_r_phi|set_emotion_val_ar|update|empty_config|load_config|dofs|add_overlay|remove_overlay|clear_overlays|"+

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
			regex: "UI|Hardware|Sound|Expression|AnimatePeriodic|Animate|Serial"
		}
	);

	this.normalizeRules();

}

oop.inherits(OnoLuaHighlightRules, LuaHighlightRules);

exports.OnoLuaHighlightRules = OnoLuaHighlightRules;
});
