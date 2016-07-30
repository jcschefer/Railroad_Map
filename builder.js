 var drawLines = function(map, latLng){

  console.log('about to load coordinate data');
  
  var astarLat = gastarLat();
  var astarLong = gastarLong();
  var dijkstraLat = gdijkstraLat();
  var dijkstraLong = gdijkstraLong();
  var otherLat = gotherLat();
  var otherLong = gotherLong();
  
  console.log('builder.js received data!');
  
  var lineWeight = 3;
  
  
  for( i = 0; i < astarLat.length; i += 2)
  {
  
    var coordspathtoshow = [
      {lat: parseFloat(astarLat[i])  , lng: parseFloat(astarLong[i])},
      {lat: parseFloat(astarLat[i+1]), lng: parseFloat(astarLong[i+1])}
    ];
  
    var polylinepathtoshow = new google.maps.Polyline( {
      path : coordspathtoshow,
      strokeColor : "#FF0000",
      strokeOpacity : 1.0,
      strokeWeight  : lineWeight
    });
  
    polylinepathtoshow.setMap(map);
  }
  console.log('astar lines drawn!');
  
  for( i = 0; i < dijkstraLat.length; i += 2)
  {
  
    var coordspathtoshow = [
      {lat: parseFloat(dijkstraLat[i])  , lng: parseFloat(dijkstraLong[i])},
      {lat: parseFloat(dijkstraLat[i+1]), lng: parseFloat(dijkstraLong[i+1])}
    ];
  
    var polylinepathtoshow = new google.maps.Polyline( {
      path : coordspathtoshow,
      strokeColor : "#00FF00",
      strokeOpacity : 1.0,
      strokeWeight  : lineWeight
    });
  
    polylinepathtoshow.setMap(map);
  }
  console.log('dijkstra lines drawn!');
  
  for( i = 0; i < otherLat.length; i += 2)
  {
  
    var coordspathtoshow = [
      {lat: parseFloat(otherLat[i])  , lng: parseFloat(otherLong[i])},
      {lat: parseFloat(otherLat[i+1]), lng: parseFloat(otherLong[i+1])}
    ];
  
    var polylinepathtoshow = new google.maps.Polyline( {
      path : coordspathtoshow,
      strokeColor : "#0000FF",
      strokeOpacity : 1.0,
      strokeWeight  : lineWeight
    });
  
    polylinepathtoshow.setMap(map);
  }
  console.log('remaining lines drawn!');
}

function initialize() {
  var latLng = new google.maps.LatLng(39.0,-96.0);
  var map = new google.maps.Map(document.getElementById('mapCanvas'), {
    zoom: 4,
    center: latLng,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });
  google.maps.event.addListener(map, 'tilesloaded', drawLines(map, latLng));
}
google.maps.event.addDomListener(window, 'load', initialize);

