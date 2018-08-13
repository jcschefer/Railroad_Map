 var map;
 var lines = {};

 var lineWeight = 3;

 var ASTAR_COLOR = '#FF0000';
 var DIJKSTRA_COLOR = '#00FF00';
 var REMAINING_COLOR = '#0000FF';

document.getElementById('source-destination-section').addEventListener('submit', function(event) {
  event.preventDefault();
  $('#loading-placeholder').show();

  $.getJSON({
	url: "/fetchSearchResults",
	data: $(event.target).serialize(),
	success: function(result) {
		var astar = new Set(result.aStarKeys);
		var dijkstra = new Set(result.dijkstraKeys);

		Object.keys(lines).forEach(function(path_key) {
			var color = REMAINING_COLOR;
			if (astar.has(path_key)) {
				color = ASTAR_COLOR;
			} else if (dijkstra.has(path_key)) {
				color = DIJKSTRA_COLOR;
			}

			lines[path_key].setOptions({strokeColor: color});
		});
		$('#loading-placeholder').hide();
  }});
});

var createLines = function(e) {
	$.getJSON({url: "/allLines", success: function(result){
		var paths = result.path;
		paths.forEach(function(path) {
			var coordinates = [
				{lat: path['source']['lat'], lng: path['source']['lng']},
				{lat: path['destination']['lat'], lng: path['destination']['lng']},
			];

			lines[path['key']] = new google.maps.Polyline({
				path: coordinates,
				strokeColor: REMAINING_COLOR,
				strokeOpacity: 1.0,
				strokeWeight: lineWeight,
			});
		});

		Object.keys(lines).forEach(function(lineKey) {
			lines[lineKey].setMap(map);
		});

		setTimeout(function() {
			$('#loading-placeholder').hide();
		}, 2000);
	}});
}

function initialize() {
  var latLng = new google.maps.LatLng(39.0,-96.0);
  map = new google.maps.Map(document.getElementById('mapCanvas'), {
    zoom: 4,
    center: latLng,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
	editable: false
  });
  google.maps.event.addListener(map, 'tilesloaded', createLines(map));
}
google.maps.event.addDomListener(window, 'load', initialize);
