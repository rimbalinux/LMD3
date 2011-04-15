/**
 * @author Administrator
 */
(function($) {

	var map = null;
	var geocoder=null;
	var user={};
	window.people = {}
	var info_div = null;
	var carouselDiv=null;
	var visualization=null;
	/*
	 * person
	 */
	var Person = function(id,name,email,lat,lng,lc,sd,s){
		var me = this;
		window.people[id] = this;
		this.id = id;
		this.name = name;
		this.email = email;
		this.lc = lc;
		this.sub_district = sd;
		this.district = s;
		this.point = new GLatLng(lat,lng);
		this.marker = new GMarker(this.point);
		this.marker.disableDragging();
		this.info = new Info(this);
		
		map.addOverlay(this.marker);
		map.addOverlay(this.info);
		
		GEvent.addListener(this.marker,"click",function(latlang){
			$.ajax({
				type:'GET',
				url:'events/get',
				data:{id:me.id},
				success:updateSuccess,
				error:updateError
			});
			me.show();
			/*alert("This is fire to Show Person Info of "+ me.name);*/
		});
	}
	
	Person.prototype.moveandshow = function(){
		map.setCenter(this.marker.getPoint(),7);
	};
	
	Person.prototype.setInfo = function(info){
		this.info.setInfo(info);		
	};
	
	Person.prototype.move = function(lat,lng){
		if(this.point.lat() != lat && this.point.lng() != lng){
			this.point = new GLatLng(lat,lng);
			this.marker.setLatLng(this.point);
			this.info.redraw();
		}
	};
	
	Person.prototype.show =function(){
		//p = map.getCenter();
		map.panTo(this.point);
		//this.point = new GLatLng(this.marker.getLatLng().lat(),this.marker.getLatLng().lng())
		//this.info.redraw();
		//this.info.show();
		infowindow = '<div class="infoWindows"><div align="left" class="img_container" onclick="top.location.href=\'/people/profile?id='+this.id+'\';"><div style="background-image:url(/img?id='+ this.id +')"><img src="/images/blank.gif" width="60" height="80" /></div></div><a href="/people/profile?id='+this.id+'"><strong>'+ this.name +'</strong></a><br />'+this.lc+'<br />'+this.sub_district+'<br />'+this.district+'<br />'+this.point+'</div>';
		map.openInfoWindowHtml(this.marker.getPoint(),infowindow);//this.name document.createTextNode(
	};
	
	
	
	var Info = function(person){
		this.person = person;
	};
	
	Info.prototype = new GOverlay();
	
	Info.prototype.initialize = function(map){
		this.infoDiv = $('<div />').addClass('bubble');
    	this.infoDiv.append($('<div />').addClass('bubble-top'));
	    this.infoContent = $('<div />').addClass('bubble-middle');
	    this.infoDiv.append(this.infoContent);
	    this.infoDiv.append($('<div />').addClass('bubble-bottom'));
	    $(map.getPane(G_MAP_FLOAT_PANE)).append(this.infoDiv);
		this.xoffset = -10;
		this.yoffset = -30;
		var me = this;
		this.infoDiv.mouseover(function(){
			me.fade();
		});		
	};
	
	Info.prototype.setInfo = function(info){
		this.infoContent.empty().append(info);
		this.show();
	};
	
	Info.prototype.fade = function(){
		var infoDiv = this.infoDiv;
		infoDiv.stop().fadeTo(100, 1, function() {
			infoDiv.fadeTo(100000, 0.50);
		});
	}
	
	Info.prototype.show = function(){
		this.infoDiv.show();
	};
	
	Info.prototype.redraw = function(force){
		var point = map.fromLatLngToDivPixel(this.person.marker.getPoint());
		this.infoDiv.css('left', point.x + this.xoffset);
    	this.infoDiv.css('bottom', -1 * point.y - this.yoffset);
    	this.infoDiv.css('z-index', 150 + point.y);	
	};
	
	Info.prototype.hide = function(){
		this.infoDiv.hide();
	};
	
	var sanitizeInput = function(input) {
    return input.replace('&', '&amp;').replace('<', '&lt;').
        replace('>', '&gt;');
  };
  
  window.initData = function(){
  	$.get('/events/init',render);
  };
  
  window.render = function(json){
  	var data = eval('(' + json + ')');
  	//alert(data.length);
	user = data;
	for (var i = 0; i < data.length; i++) {
		var person = new Person(data[i].id, data[i].name, data[i].email, data[i].lat, data[i].lng, data[i].lc, data[i].sub_district, data[i].district);
	//alert(user[i].photo_url)
	}
	
	jQuery('#lp_photo_c').jcarousel({
        size: user.length,
        itemLoadCallback: {onBeforeAnimation: generateCImage}
    });
    
  };
  
  window.generateCImage = function(carousel,state){
  	for(var i=carousel.first;i<=carousel.last;i++){
		if(carousel.has(i)){
			continue;
		}
		if(i>user.length){
			break;
		}
		carousel.add(i,setUpImage(user[i-1]));
	}
  };
  //width="60" height="80" 
  window.setUpImage = function(item){
  	//return '<div class="img_container" align="center"><img src="' + item.photo_url + '" alt="' + item.photo_url + '" title="'+item.name+'" onclick="getData(\''+item.id+'\');" /></div>';
  	return '<div class="img_container" align="center"><div style="background-image:url(' + item.photo_url + ')"><img src="/images/blank.gif" width="60" height="80" alt="' + item.photo_url + '" title="'+item.name+'" onclick="getData(\''+item.id+'\');" /></div>';
  };
  
  window.getData = function(id){
  	$.ajax({
		type:'GET',
		url:'events/get',
		data:{id:id},
		success:updateSuccess,
		error:updateError
	});
  };
  
  window.updateSuccess = function(json){
  	var data = eval('('+json+')');
  	people[data.id].show();
  	
  	//var data = new google.visualization.DataTable(data.format, 0.5);
  	//visualization.draw(data, {'allowHtml': true});
	//$(info_div).html(json);
	//alert(data.html);
	$('#lp_info').html(data.html);
	$('#lp_search').hide("slow");
	$('#lp_search1').show();
	
	
  };
  
  window.updateError = function(){
  	alert("Something caught in an errors");
  }

jQuery(document).ready(function() {
	if (GBrowserIsCompatible()) {
			info_div = document.getElementById('lp_info');
			visualization = new google.visualization.Table(document.getElementById('lp_info'));
		  	  
			carouselDiv = $('#lp_photo_c');
			var mapDiv = document.getElementById('map_canvas');
			map = new GMap2(mapDiv);
			map.addControl(new GMapTypeControl());
			map.addControl(new GSmallMapControl());
			geocoder = new GClientGeocoder();
			map.setCenter(new GLatLng(4.54, 96.53), 7);
			initData();
	    }
		
});
	window.onload = function() {
		
		
	};
})(jQuery);


// write down by jester

