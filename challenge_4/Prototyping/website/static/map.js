// Initialize the map
var map = L.map('map').setView([53.5349, 9.9946], 13); // Adjust the initial center and zoom level as needed

// Add the tile layer (e.g., OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
  maxZoom: 18
}).addTo(map);

// Add markers
var marker1 = L.marker([53.54453345986325, 9.97229808027687]).addTo(map);
var marker2 = L.marker([53.5407209260667, 9.974240506415265]).addTo(map);
var marker3 = L.marker([53.528229198221254, 9.97576905634448]).addTo(map);
var marker4 = L.marker([53.524121573023905, 9.981857299201057]).addTo(map);

// Draw a line between markers
var line = L.polyline([marker1.getLatLng(), marker2.getLatLng(), marker3.getLatLng(), marker4.getLatLng()], {
  color: 'red'
}).addTo(map);