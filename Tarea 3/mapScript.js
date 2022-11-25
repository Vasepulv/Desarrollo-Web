var mymap=L.map('map').setView([-33.5,-70.6,], 5);
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		id: 'mapbox/streets-v11',
		tileSize: 512,
		zoomOffset: -1
	}).addTo(mymap);

var dict={};

var isThere=false;

function addMarker(log, lat,comun){
	var thismarker=L.marker([lat,log]);
	
	if (dict[comun]!=undefined){
		var dictComuna=dict[comun];
		dictComuna.foto++;
		thismarker.bindPopup("<b>"+dictComuna.foto+"</b>");
	}
	else{
		var dictComuna=dict[comun]={};
		dictComuna.latitud=lat;
		dictComuna.longitud=log;
		dictComuna.foto=1;
		thismarker.addTo(mymap);
		thismarker.bindPopup("<b>"+dictComuna.foto+"</b>").openPopup();
	}
}