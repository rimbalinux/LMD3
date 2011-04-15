/*
 * 
 * Black'n'White plugin 1.0
 * $Date: 2008-06-17 15:38:15 +0200 (mar, 17 giu 2008) $
 * $Rev: 177 $
 * @requires jQuery v1.2.6
 * 
 * Copyright (c) 2008 Massimiliano Balestrieri
 * Examples and docs at: http://maxb.net/blog/
 * Licensed GPL licenses:
 * http://www.gnu.org/licenses/gpl.html
 * 
 */
 
if(!window.BlacknWhite)
    var BlacknWhite = {};
    
     
BlacknWhite = {
    init     : function(options)
    {
        options = $.extend({minor : 9}, options);
        
        if($.browser.msie && $.browser.version < options.minor)
            $('html').css("filter","gray"); 
    }
};


$(document).ready(function(){ 
    BlacknWhite.init();
    //BlacknWhite.init({minor : 8});
}); 