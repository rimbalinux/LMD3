/**
 * LangChange : a jQuery Plug-in
 * Samuel Garneau <samgarneau@gmail.com>
 * http://samgarneau.com
 * 
 * Released under no license, just use it where you want and when you want.
 */
function createCookie(name,value,days) {
	if (days) {
		var date = new Date();
		date.setTime(date.getTime()+(days*24*60*60*1000));
		var expires = "; expires="+date.toGMTString();
	}
	else var expires = "";
	document.cookie = name+"="+value+expires+"; path=/";
}

function readCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
}

function eraseCookie(name) {
	createCookie(name,"",-1);
}

(function($){
	
	$.fn.changeLang = function(params){
		
		var defaults = {
			file: '/static/lang/lang_content.xml',
			lang: 'en'
		}
		
		var aTexts = new Array();
		
		if(params) $.extend(defaults, params);
		//alert(defaults.file);
		
		$.ajax({
		      type: "GET",
		      url: defaults.file,
		      dataType: "xml",
		      success: function(xml)
					   {
		           			$(xml).find('text').each(function()
							{
								var textId = $(this).attr("id");
		                 				var text = $(this).find(defaults.lang).text();
								
								aTexts[textId] = text;
								//alert(aTexts);
							});
		
							$.each($("*"), function(i, item)
							{
								//alert($(item).attr("langtag"));
								if($(item).attr("langtag") != null){
									$(item).fadeOut(50).fadeIn(50).text(aTexts[$(item).attr("langtag")]);
								}
							});
		               }
		      });
	};
	
})(jQuery);