


var stations_style = {
  "bubblingMouseEvents": true,
  "color": "#1f81dd",
  "dashArray": null,
  "dashOffset": null,
  "fill": true,
  "fillColor": "#2e29cf",
  "fillOpacity": 0.8,
  "fillRule": "evenodd",
  "lineCap": "round",
  "lineJoin": "round",
  "opacity": 0.8,
  "radius": 4,
  "stroke": true,
  "weight": 2
}


var bounds = null;


var map_id = L.map(
	'map_id',
	{center: [43.312134,-1.981296],
	zoom: 14,
	zoomDelta: 0.5,
	maxBounds: bounds,
	layers: [],
	worldCopyJump: false,
	crs: L.CRS.EPSG3857,
	dragging: false,
	scrollWheelZoom: false
});



var tile_layer_878235c2508042be9565a61b726e6a6e = L.tileLayer(
	'https://api.mapbox.com/styles/v1/inigoml/cjiz1f25w073f2rpdr8jhp0e3/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiaW5pZ29tbCIsImEiOiJjamcycndxcDAwcmlsMnFwaHk4eDdpanhnIn0.lOge1jvtZgNLhr6yUdz8qA',
	{
	"attribution": null,
	"detectRetina": false,
	"maxZoom": 18,
	"minZoom": 1,
	"noWrap": false,
	"subdomains": "abc"
	}
	).addTo(map_id);

map_id.timeDimension = L.timeDimension({period:"PT10S"});



map_id.timeDimensionControl = L.control.timeDimension({
	position: 'bottomleft',
	title: "Time Control",
	autoPlay: true,
	speedStep: 5,
	minSpeed: 100,
	maxSpeed: 800,
	timeSteps: 1,
	timeZones: ["Local","UTC"],
	timeSliderDragUpdate: true,
	playerOptions: {
		transitionTime: 200,
		loop: true}
		});
map_id.addControl(map_id.timeDimensionControl);
map_id.timeDimensionControl._sliderSpeedValueChanged(300);
map_id.timeDimensionControl._buttonDateClicked();

function loadJSON(callback, json_file) {   
  var xobj = new XMLHttpRequest();
  xobj.overrideMimeType("application/json");
  xobj.open('GET', json_file, true);
  xobj.onreadystatechange = function () {
	if (xobj.readyState == 4 && xobj.status == "200") {
		json = JSON.parse(xobj.responseText)
		callback(json);
	}
  };
  xobj.send(null);
}
loadJSON(function(json) {
  //console.log(json);
  var geo_json_035cfa6336894c61adbecf8fb9fb4809 = L.geoJson(
		json                    
		).addTo(map_id);
	geo_json_035cfa6336894c61adbecf8fb9fb4809.setStyle({'color': '#2e29cf','weight': 2, 'opacity':0.5});
}, './assets/json/20069_bidegorri.geojson');


//loadJSON(function(json) {
//  //console.log(json);
//  var geo_json_035cfa6336894c61adbecf8fb9fb4809 = L.geoJson(
//		json                    
//		).addTo(map_id);
//	geo_json_035cfa6336894c61adbecf8fb9fb4809.setStyle({'color': '#1f81dd','weight': 1});
//}, '20069_aparcabicis.geojson');


var json_files = [];
for(var i=0; i<=8; i++){
	json_files.push('./assets/json/features_' + i + '.json')
}
for(var i=0; i<json_files.length; i++){
	var json = null;
	var timestamped_geo_json_09ca5e18802e4001bbbc54c5f6ebe43f;
	loadJSON(function(json) {
	  //console.log(json);
	timestamped_geo_json_09ca5e18802e4001bbbc54c5f6ebe43f = L.timeDimension.layer.geoJson(
		L.geoJson(json, 
		{style: function (feature) {
			return feature.properties.style
		},
			pointToLayer: pointToLayer    
		}),
		{updateTimeDimension: true,updateTimeDimensionMode: "union",
		addlastPoint: true, duration: 'PT5M'}
		).addTo(map_id);
		
		
	}, json_files[i]);
}
  
var geojsonMarkerOptions = {
		radius: 3,
		fillColor: "#d90368",
		color: "#000",
		weight: 1,
		opacity: 1,
		fillOpacity: 0.8
};
function pointToLayer(feature, latlng) {
		return L.circleMarker(latlng, geojsonMarkerOptions);
}         

var circle_marker_4bdb78116d8244b99affe0b034343413 = L.circleMarker(
	[43.321796,-1.985112],stations_style).addTo(map_id);
var popup_79b7210048064014a5ab1636be68e68a = L.popup({maxWidth: '300'});
var html_12842572c822435bb9f9598460c8f040 = $('<div id="html_12842572c822435bb9f9598460c8f040" style="width: 100.0%; height: 100.0%;">Ayuntamiento</div>')[0];
popup_79b7210048064014a5ab1636be68e68a.setContent(html_12842572c822435bb9f9598460c8f040);
circle_marker_4bdb78116d8244b99affe0b034343413.bindPopup(popup_79b7210048064014a5ab1636be68e68a);


var circle_marker_344087f49985491380a4ebd67c44c867 = L.circleMarker(
	[43.320526,-1.9824689999999998],stations_style).addTo(map_id);
var popup_20f692507615485681d2e62d2d5113d6 = L.popup({maxWidth: '300'});
var html_259cac09b81f4852a3c8330acdbd519a = $('<div id="html_259cac09b81f4852a3c8330acdbd519a" style="width: 100.0%; height: 100.0%;">Andia</div>')[0];
popup_20f692507615485681d2e62d2d5113d6.setContent(html_259cac09b81f4852a3c8330acdbd519a);
circle_marker_344087f49985491380a4ebd67c44c867.bindPopup(popup_20f692507615485681d2e62d2d5113d6);


var circle_marker_124cce99eb434e31a8c48ca04628b09e = L.circleMarker(
	[43.318356,-1.9816529999999999],stations_style).addTo(map_id);
var popup_4ddf4748bb7342a39eb8ede0ff0f4fe6 = L.popup({maxWidth: '300'});
var html_ed445c35af5046419a21b4aea79ce137 = $('<div id="html_ed445c35af5046419a21b4aea79ce137" style="width: 100.0%; height: 100.0%;">Arrasate</div>')[0];
popup_4ddf4748bb7342a39eb8ede0ff0f4fe6.setContent(html_ed445c35af5046419a21b4aea79ce137);
circle_marker_124cce99eb434e31a8c48ca04628b09e.bindPopup(popup_4ddf4748bb7342a39eb8ede0ff0f4fe6);


var circle_marker_8c812c75568c4cd78d4e7f06ff0a1da5 = L.circleMarker(
	[43.318637,-1.9773189999999998],stations_style).addTo(map_id);
var popup_f9e2047a060a4d1a9debb400e08f073b = L.popup({maxWidth: '300'});
var html_29e2b18c3b1543dc8960126ceb818ecb = $('<div id="html_29e2b18c3b1543dc8960126ceb818ecb" style="width: 100.0%; height: 100.0%;">Paseo Francia</div>')[0];
popup_f9e2047a060a4d1a9debb400e08f073b.setContent(html_29e2b18c3b1543dc8960126ceb818ecb);
circle_marker_8c812c75568c4cd78d4e7f06ff0a1da5.bindPopup(popup_f9e2047a060a4d1a9debb400e08f073b);


var circle_marker_c3e02868d29b4f0ba642a66050ca4ee8 = L.circleMarker(
	[43.31328,-1.98174],stations_style).addTo(map_id);
var popup_d491658682954327869f3193007df1f1 = L.popup({maxWidth: '300'});
var html_24534865443b4a488495396e02a841a2 = $('<div id="html_24534865443b4a488495396e02a841a2" style="width: 100.0%; height: 100.0%;">Easo</div>')[0];
popup_d491658682954327869f3193007df1f1.setContent(html_24534865443b4a488495396e02a841a2);
circle_marker_c3e02868d29b4f0ba642a66050ca4ee8.bindPopup(popup_d491658682954327869f3193007df1f1);


var circle_marker_4451049baa2a484198e2742ae4f2e8fd = L.circleMarker(
	[43.307468,-1.978738],stations_style).addTo(map_id);
var popup_73885a2dddfe46cab098424178fefb0c = L.popup({maxWidth: '300'});
var html_3daff845a35844bfa0dc6afb37d15ef6 = $('<div id="html_3daff845a35844bfa0dc6afb37d15ef6" style="width: 100.0%; height: 100.0%;">Pio XII</div>')[0];
popup_73885a2dddfe46cab098424178fefb0c.setContent(html_3daff845a35844bfa0dc6afb37d15ef6);
circle_marker_4451049baa2a484198e2742ae4f2e8fd.bindPopup(popup_73885a2dddfe46cab098424178fefb0c);


var circle_marker_48c1e09de04044caa47b7c57edd33e8f = L.circleMarker(
	[43.309983,-1.971539],stations_style).addTo(map_id);
var popup_958be82a4e664ad2abd40661820e7a93 = L.popup({maxWidth: '300'});
var html_e39bde70ac84444e9d455f6c7c0c91a8 = $('<div id="html_e39bde70ac84444e9d455f6c7c0c91a8" style="width: 100.0%; height: 100.0%;">Riberas</div>')[0];
popup_958be82a4e664ad2abd40661820e7a93.setContent(html_e39bde70ac84444e9d455f6c7c0c91a8);
circle_marker_48c1e09de04044caa47b7c57edd33e8f.bindPopup(popup_958be82a4e664ad2abd40661820e7a93);


var circle_marker_4a512cb7bc9444af8fe5f1f5e9bee0b5 = L.circleMarker(
	[43.304235999999996,-1.976203],stations_style).addTo(map_id);
var popup_dfcbb9ea3ee848a2a8b1f3391db3a106 = L.popup({maxWidth: '300'});
var html_1bd60e8614794bbfa773274ca7f7a98c = $('<div id="html_1bd60e8614794bbfa773274ca7f7a98c" style="width: 100.0%; height: 100.0%;">Isabel II</div>')[0];
popup_dfcbb9ea3ee848a2a8b1f3391db3a106.setContent(html_1bd60e8614794bbfa773274ca7f7a98c);
circle_marker_4a512cb7bc9444af8fe5f1f5e9bee0b5.bindPopup(popup_dfcbb9ea3ee848a2a8b1f3391db3a106);


var circle_marker_bebd6c50a5e14efda483e77c46b09c22 = L.circleMarker(
	[43.302231,-1.975082],stations_style).addTo(map_id);
var popup_aaa003cd0be745148eed6e84e5b4d577 = L.popup({maxWidth: '300'});
var html_28072bb0152446cfbc7d1bbca758797f = $('<div id="html_28072bb0152446cfbc7d1bbca758797f" style="width: 100.0%; height: 100.0%;">Anoeta</div>')[0];
popup_aaa003cd0be745148eed6e84e5b4d577.setContent(html_28072bb0152446cfbc7d1bbca758797f);
circle_marker_bebd6c50a5e14efda483e77c46b09c22.bindPopup(popup_aaa003cd0be745148eed6e84e5b4d577);


var circle_marker_66b9578c4fc94b51948fdf012807bbbb = L.circleMarker(
	[43.3125157,-2.005941],stations_style).addTo(map_id);
var popup_96a639c848c740078ece47b213780ab2 = L.popup({maxWidth: '300'});
var html_e0993e23874747369fb14846d4e815d6 = $('<div id="html_e0993e23874747369fb14846d4e815d6" style="width: 100.0%; height: 100.0%;">Av. Zarautz</div>')[0];
popup_96a639c848c740078ece47b213780ab2.setContent(html_e0993e23874747369fb14846d4e815d6);
circle_marker_66b9578c4fc94b51948fdf012807bbbb.bindPopup(popup_96a639c848c740078ece47b213780ab2);


var circle_marker_e7439883592b42738b67db1edec90960 = L.circleMarker(
	[43.311939,-2.00869],stations_style).addTo(map_id);
var popup_914134f821594404aa58603bd4956d81 = L.popup({maxWidth: '300'});
var html_cafe412bfbe1492da878a68e2ba9976c = $('<div id="html_cafe412bfbe1492da878a68e2ba9976c" style="width: 100.0%; height: 100.0%;">Magisterio</div>')[0];
popup_914134f821594404aa58603bd4956d81.setContent(html_cafe412bfbe1492da878a68e2ba9976c);
circle_marker_e7439883592b42738b67db1edec90960.bindPopup(popup_914134f821594404aa58603bd4956d81);


var circle_marker_6dad69a2ce124f28a3c14ab85046d161 = L.circleMarker(
	[43.309012,-2.0104290000000002],stations_style).addTo(map_id);
var popup_d436316bc6dd45db8d9013d3e9b0f1e1 = L.popup({maxWidth: '300'});
var html_a8881c9dda554828ae95ebb9cb4f9914 = $('<div id="html_a8881c9dda554828ae95ebb9cb4f9914" style="width: 100.0%; height: 100.0%;">Universidades</div>')[0];
popup_d436316bc6dd45db8d9013d3e9b0f1e1.setContent(html_a8881c9dda554828ae95ebb9cb4f9914);
circle_marker_6dad69a2ce124f28a3c14ab85046d161.bindPopup(popup_d436316bc6dd45db8d9013d3e9b0f1e1);


var circle_marker_708f67a6c4e44c0e9f275141417dab3e = L.circleMarker(
	[43.302496000000005,-2.001486],stations_style).addTo(map_id);
var popup_9f650c7edac341249cb642434b178dd5 = L.popup({maxWidth: '300'});
var html_7194cd477ef641168614a02f5c91681c = $('<div id="html_7194cd477ef641168614a02f5c91681c" style="width: 100.0%; height: 100.0%;">Lugaritz</div>')[0];
popup_9f650c7edac341249cb642434b178dd5.setContent(html_7194cd477ef641168614a02f5c91681c);
circle_marker_708f67a6c4e44c0e9f275141417dab3e.bindPopup(popup_9f650c7edac341249cb642434b178dd5);


var circle_marker_d47a6e8e27b14eb9a15ef1cef73b8093 = L.circleMarker(
	[43.324075,-1.973489],stations_style).addTo(map_id);
var popup_bda9c71d6e7b434c80d38089d13bc865 = L.popup({maxWidth: '300'});
var html_0454271c256c4805a1245f6352fa3f70 = $('<div id="html_0454271c256c4805a1245f6352fa3f70" style="width: 100.0%; height: 100.0%;">Plaza Cataluña</div>')[0];
popup_bda9c71d6e7b434c80d38089d13bc865.setContent(html_0454271c256c4805a1245f6352fa3f70);
circle_marker_d47a6e8e27b14eb9a15ef1cef73b8093.bindPopup(popup_bda9c71d6e7b434c80d38089d13bc865);


var circle_marker_6998876446044ecebf7256d2466527c5 = L.circleMarker(
	[43.325755,-1.9711290000000001],stations_style).addTo(map_id);
var popup_23c8eca7829c45d8b01038f76d43d84a = L.popup({maxWidth: '300'});
var html_4efbcd8b800741779eaebe843ae6f682 = $('<div id="html_4efbcd8b800741779eaebe843ae6f682" style="width: 100.0%; height: 100.0%;">San Francisco</div>')[0];
popup_23c8eca7829c45d8b01038f76d43d84a.setContent(html_4efbcd8b800741779eaebe843ae6f682);
circle_marker_6998876446044ecebf7256d2466527c5.bindPopup(popup_23c8eca7829c45d8b01038f76d43d84a);


var circle_marker_c415e3055d634d28a5490d03cbebf8b3 = L.circleMarker(
	[43.313203,-1.956611],stations_style
	).addTo(map_id);
var popup_7ad9ac89335c4aeab7ff3354a9b7e624 = L.popup({maxWidth: '300'});
var html_dc8d01b7454644008b52c3440d0b6c4f = $('<div id="html_dc8d01b7454644008b52c3440d0b6c4f" style="width: 100.0%; height: 100.0%;">Intxaurrondo</div>')[0];
popup_7ad9ac89335c4aeab7ff3354a9b7e624.setContent(html_dc8d01b7454644008b52c3440d0b6c4f);
circle_marker_c415e3055d634d28a5490d03cbebf8b3.bindPopup(popup_7ad9ac89335c4aeab7ff3354a9b7e624);



