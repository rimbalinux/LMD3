var subdistrict_sel = 0;
var district_sel = 0;
var village_sel = 0;
$(function(){
    if ($('#fdistrict').length){
    	// dependen dropdown
    	$('#district').bind('change',function(){
    			var me = this[this.selectedIndex];
    			if(me.value !=""){
    				$.ajax({
    					type: 'GET',
    					url:'/admin/events/getchild?id='+$(me).val(),
    					success:function(json){
    						var data = eval('(' + json + ')');
    						$('#sub_district').empty()
    						$('#sub_district').append($('<option />').val("").text('Select Sub District').attr('langtag','loc-sel-subdistrict'));
    						for(var i = 0;i< data.length;i++){
    							$('#sub_district').append($('<option />').val(data[i].dl_id).text(data[i].dl_name));
    						}
    						if (subdistrict_sel){
    							$('#sub_district').val('0');
    							$('#sub_district').val(subdistrict_sel);
    							$('#sub_district').change();
    						}
							if(currentLang == 'id'){
								$("body").changeLang({lang: "id", file: "/static/lang/lang_content.xml"});
							}
    					},
    					error:function(){
    						alert('error guys')
    					}
    				});	
    			}
    	});
    	//var addBinding = function(){
    		$('#sub_district').bind('change',function(){
    			var me = this[this.selectedIndex];
    			if(me.value !=""){
    				$.ajax({
    					type: 'GET',
    					url:'/admin/events/getchild?id='+$(me).val(),
    					success:function(json){
    						var data = eval('(' + json + ')');
    						$('#village').empty()
    						$('#village').append($('<option />').val("").text('Select Village').attr('langtag','loc-sel-village'));
    						for(var i = 0;i< data.length;i++){
    							$('#village').append($('<option />').val(data[i].dl_id).text(data[i].dl_name));	
    						}
    						if (village_sel){
    							$('#village').val('0');
    							$('#village').val(village_sel);
    							$('#village').change();
    						}
							if(currentLang == 'id'){
								$("body").changeLang({lang: "id", file: "/static/lang/lang_content.xml"});
							}
    					},
    					error:function(){
    						alert('error guys')
    					}
    				});	
    			}
    		});
    	//};
    	
    	if (district_sel) {
    	   _ds = $('#district');
    	   _ds.val(district_sel);
    	   _ds.change();
        }

	}

	function setGeoPos(){
		n1 = $('#n1').val();
		n2 = ($('#n2').val()/60);
		e1 = $('#e1').val();
		e2 = ($('#e2').val()/60);
		var n = 0;
		n = (Number(n1)+Number(n2)).toString();
		var e = 0;
		e = (Number(e1)+Number(e2)).toString();
		$('#geo_pos').val(n+","+e);
	}
	$('#n1').bind('keyup',function(){
		setGeoPos();
	});
	$('#n2').bind('keyup',function(){
		setGeoPos();
	});
	$('#e1').bind('keyup',function(){
		setGeoPos();
	});
	$('#e2').bind('keyup',function(){
		setGeoPos();
	});

	var pos = $('#geo_pos').val();
	if( $('#geo_pos').length && pos ){
		geopoint = pos.split(',');
		n1val = geopoint[0].split(".")[0];
		n2val = "0."+geopoint[0].split(".")[1];
		e1val = geopoint[1].split(".")[0];
		e2val = "0."+geopoint[1].split(".")[1];
		$('#n1').val(n1val);
		$('#n2').val(Number(n2val)*60);
		$('#e1').val(e1val);
		$('#e2').val(Number(e2val)*60);
		//alert(n1val+'-'+n2val+'-'+e1val+'-'+e2val);
	}

});
