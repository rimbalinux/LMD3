var sp_url = '';
var sepidol = /static\/(.*)sepidol\.js(\?.*)?$/;

$('head script[src]').each(function(i, s) {
    if (s.src.match(sepidol)) {
        var path = s.src.replace(sepidol, '');
        sp_url = path;
    }
});

function act_payload(resp, target){
    json = false;
    try {
        json = JSON.parse(resp);
    }catch(e){}
    if (json){
        payload = json.payload
        if (!payload) return json;
        if (payload.html) target.html(payload.html);
        data = (payload.data && payload.data != 'undefined') ? payload.data : json;
        for (var key in payload) {
          if (key != 'html' && key != 'data'){
              sdata = payload[key];
              data = (sdata && sdata != 'undefined') ? sdata : data;
              try {
                  eval (key+'(data);');
              } catch(e) {
              //    alert('error '+key+' method doesn\'t exists\n'+e)
              }
          }
        }
        return json;
    }
    return resp;
}

function _get(url, event, cb) {
    target = event.target || event.srcElement;
    $.ajax({
        url: url,
        dataType: 'text',
        complete: function(){
            $(target).parent().find('span.loader').remove();
        },
        error: function(resp) {$.facebox(resp.statusText)},
        success: function(resp) {
            resp = act_payload(resp, target);
            if (typeof cb == 'function') return cb(resp);
            return resp;
        }
        });
    //alert(typeof target);
    return false;
}

function wait_for_load(url, event, cb, inline){
    target = event.target || event.srcElement;
    if (typeof cb == 'string' && inline != 'undefined' ) {
        $('#'+cb).html('<div style="text-align:center;"><img src="'+sp_url+'images/loading.gif" /></div>');
	} else {
        $(target).parent().append('<span class="loader" style="border:none;margin-left:3px;"><img src="'+sp_url+'images/loading_small.gif" /></span>');
	};
	resp = _get(url, event, cb);
	if (resp){
        if (typeof cb == 'function')
            cb(resp);
        else if (typeof cb == 'string')
            if ($('#'+cb).length) $('#'+cb).html(resp);
            else $(target).parent().html(resp);
        else
            $(target).html(resp);
	}
};

// slidedown
function stoggle(sel){
    $(sel).slideToggle();
    return false;
}

function hitRun(obj, target)
{
    
}

function app(r){
    d = '<li id="pp_'+r.id+'"><a href="/ajax?action=Personal&c=mpp&pid='+r.pid+'" rel="facebox">'+r.name+'</a><br/>'+r.description+'</li>';
    $('ul.metapick').append(d);
    $.facebox('<h3>Data saved!</h3>');
}

function mpp(r){
    d = '<a href="/ajax?action=Personal&c=mpp&pid='+r.pid+'" rel="facebox">'+r.name+'</a><br/>'+r.description;
    $('li#pp_'+r.id).html(d);
    $.facebox('<h3>Data saved!</h3>');
}

/**
 * metaforms
 **/
 
function mfpick(resp)
{
    if (!resp) return
    cmd = resp.cmd;
    if (!cmd) return;
    lcprod = $('div#metagrid').find('ul.metapick');
    lcform = $('div#metaforms').find('ul.metapick');
    if (cmd == 'pick' || cmd=='new') {
        lcprod.prepend('<li id="lp'+resp.id+'">'+resp.title+'<br/><small>'+resp.description+'</small></li>')
    }else if(cmd == 'unpick'){
        lcprod.find('#lp'+resp.id).slideUp().remove();
    }
    if (cmd=='new'){
        stoggle('#newfield');
        lcform.prepend('<li id="lp'+resp.id+'">'+resp.title+'<br/><small>'+resp.description+'</small></li>');
    }
}
function act_metaform(obj, e)
{
    e.preventDefault();
    o = $(obj);
    if (o.hasClass('metaform-pick')){
        act='pick';
        o.removeClass('uiAdd').addClass('uiRemove');
    }else if(o.hasClass('metaform-unpick')){
        act = 'unpick';
        o.parents('li').slideUp().remove();
        //removeClass('uiRemove').addClass('uiAdd');
    }else{
        return;
    }
    return _get(obj+'?cmd='+act, e, mfpick);
}

function gridform_toggle(e)
{
    var gf = $('#gridform');
    if (gf.is(':hidden'))
    {
        gf.slideDown();
        $('#griddata').slideUp();
        $(":text:visible:enabled:first").focus();
    }
    else {
        gf.slideUp();
        $('#griddata').slideDown();        
    }
}

/**
 * BOOTLOADER
 */
$(function() {
	$('form.UIWait').live('submit', function() {
	    target = $(this).parent();
		var options = {clearForm: false, success: function(resp){return act_payload(resp, target)}};
		if ($(this).attr('enctype').length){
		    options.iframe = true;
		}
		$(this).ajaxSubmit(options);
		return false;
	});

	$('a.UIWait').live('click', function(e) {
	    e.preventDefault();
	    wait_for_load($(this).attr('href'), e);
	});
	//facebox
	$('a[rel*=facebox]').facebox();
	//metaform action
	$('a.metaform-act').live('click', function(e){
	    act_metaform(this, e);
	    //e.preventDefault();
	});
    $(document).bind('beforeReveal.facebox', function() {
        $("#facebox .content").empty();
    });
    $('.uiTip').tipsy({live:true, gravity: 's'});
    $('.acRemove').live('click', function(e){
        t = $(this).attr('original-title');
        c = confirm('Are you sure to remove ' + t + ' ?\n this action can not be undone.');
        if (!c) {
            e.preventDefault();
        }
    });
    $('form.validate').validator();
});

var _map = {scrollwheel: false, zoom: 9, controls: ["GSmallZoomControl3D", "GMenuMapTypeControl"]};
var _icon = {image: "/images/map_marker.png",
              iconsize: [26, 26],
              iconanchor: [5,16],
              infowindowanchor: [12, 0]};
/*

*/
