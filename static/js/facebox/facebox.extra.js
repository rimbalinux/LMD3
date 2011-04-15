(function($) {
  ////
  //
  // Depends on the amazing Ajax form plugin.
  //
  // Callback receives responseText and 'success' / 'error'
  // based on response.
  //
  //  i.e.:
  //    $('#someform').spamjax(function(text, status) {
  //      if (status == 'success') { alert('yay') } else { alert('o no') }
  //    })
  //
  // settings hash:
  //   facebox: true        // a facebox 'loading' will open pre-submit
  //   confirmation: string // a confirm pop-up will open with the supplied string
  //
  //  i.e.:
  //    $('#someform').spamjax({ facebox: true }, function(text, status) {
  //      if (status == 'success') { alert('yay') } else { alert('o no') }
  //    })
  $.fn.spamjax = function(callback, settings) {
    alert('spam called')
    event.preventDefault();
    if ($.isFunction(settings)) {
      var s = callback, callback = settings, settings = s
    }

    var settings = settings || {}
    var options  = {}

    // if there's no facebox we can't use it
    if (!$.facebox) settings.facebox = null 

    options.complete = function(xhr, ok) { callback.call(this, xhr.responseText, ok) }

    if (settings.confirmation) {
      options.beforeSubmit = function() {
        var execute = confirm(settings.confirmation)
        if (!execute) return false
        if (settings.facebox) $.facebox.loading()
      }
    } else if (settings.facebox) { 
      options.beforeSubmit = $.facebox.loading
    }

    $.get(this.href, function(data) { return data; })
    //return $(this).ajaxForm($.extend(settings, options))
    return false;
  }
})(jQuery);
