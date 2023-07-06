// Check if the map instance already exists
var map = L.map("map");
if (!map.hasLayer()) {
  // Initialize the map
  console.log("init map")
  L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png", {
    attribution: 'Map data &copy; <a href="https://carto.com/">Carto</a>',
    subdomains: "abcd",
    minZoom: 0,
    maxZoom: 20,
  }).addTo(map);

  // Add markers
  var marker1 = L.marker([53.54453345986325, 9.97229808027687]).addTo(map);
  var marker2 = L.marker([53.5407209260667, 9.974240506415265]).addTo(map);
  var marker3 = L.marker([53.528229198221254, 9.97576905634448]).addTo(map);
  var marker4 = L.marker([53.524121573023905, 9.981857299201057]).addTo(map);

  // Create a marker group and add all markers to it
  var markerGroup = L.featureGroup([marker1, marker2, marker3, marker4]);

  // Fit the map bounds to the marker group
  map.fitBounds(markerGroup.getBounds());

  // Draw a line between markers
  var line = L.polyline(
    [
      marker1.getLatLng(),
      marker2.getLatLng(),
      marker3.getLatLng(),
      marker4.getLatLng(),
    ],
    {
      color: "red",
    }
  ).addTo(map);
}
