ko.bindingHandlers.slider = {
	init: function(element, valueAccessor){
		valueAccessor().extend({ rateLimit: 50 });

		$(element).on('moved.zf.slider', function(){
			var value = valueAccessor();
			value( $(element).find(".slider-handle").attr("aria-valuenow") );
		});
	},
	update: function (element, valueAccessor, allBindingsAccessor, viewModel) {
		var value = valueAccessor();
		var valueUnwrapped = ko.unwrap(value) || 60;
		var elem = new Foundation.Slider($(element), { 'binding': true, 'initialStart': valueUnwrapped });
		// elem.Set(100);
		// $(element).foundation('slider', 'set_value', valueUnwrapped || 0);
		ko.bindingHandlers.slider.init(element, valueAccessor);
	}
};
