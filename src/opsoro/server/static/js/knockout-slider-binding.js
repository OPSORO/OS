ko.bindingHandlers.slider = {
	init: function(element, valueAccessor){
		valueAccessor().extend({ rateLimit: 50 });

		$(element).on('change.fndtn.slider', function(){
			var value = valueAccessor();
			value( $(element).attr('data-slider') );
		});
	},
	update: function (element, valueAccessor, allBindingsAccessor, viewModel) {
		var value = valueAccessor();
		var valueUnwrapped = ko.unwrap(value);
		$(element).foundation('slider', 'set_value', valueUnwrapped || 0);
		ko.bindingHandlers.slider.init(element, valueAccessor);
	}
};
