/*
* JQuery feed fetcher from Google Feed
*
* Makes on the fly translate the supplied HTML tag
*
* Adds the following methods to jQuery:
* 
* $('.translate').translator(); - hide the applied element(s), make a request to the Google Translator API,
*									  and display the result at the same place
*
* Parameters
*	source_lang: '[lang]' - the source language of the matched translatable element
*	destination_lang '[lang]' - the destination language of the matched translatable element
*
* Result
* 	- A translated text at the same place (if the translating success)
*
* WARNING
* You need to load the JS API from google to use this plug-in
*
*	<script type="text/javascript" src="http://www.google.com/jsapi"></script>
*	<script type="text/javascript">
*    	google.load("language", "1");
*	</script>
*
* Copyright (c) 2009 Istvan Ferenc Toth
*
* Plugin homepage:
* http://adminlight.com/static/files/jquerytrans.html
*
* Example:
* http://adminlight.com/static/files/jquerytrans.html
*
* Version 0.1.0.0
*
* Tested with:
* - Linux: Firefox 2
* - Windows: Firefox 2, Internet Explorer 6+
*
* Licensed under the MIT license:
* http://www.opensource.org/licenses/mit-license.php
*
* Credits:
*   - http://code.google.com/: 
*   - http://adminlight.com: 
*	- http://www.learningjquery.com/2007/10/a-plugin-development-pattern
*/
(function($){ 
     $.fn.extend({  
         tinytrans: function(options) { 
			var opts = $.extend({}, $.fn.tinytrans.defaults, options);
            return this.each(function() { 
			var o = $.meta ? $.extend({}, opts, $this.data()) : opts;
                var obj = $(this); 
				google.language.translate(obj.html(), o.source_lang, o.destination_lang, function(result) {
					obj.html(result.translation);		
				});
			});
        } 
    }); 
	// plugin defaults
	$.fn.tinytrans.defaults = {
	  source_lang: 'en',
	  destination_lang: 'id'
	};
})(jQuery); 