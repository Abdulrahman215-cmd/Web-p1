const ACCESS_TOKEN = //accesstoken;

mapboxgl.accessToken = ACCESS_TOKEN;
    const map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v12',
        center: [-73.99209, 40.68933],
        mapTypeId: 'roadmap',
        zoom: 8.8
    });

  navigator.geolocation.getCurrentPosition(function(position) {
    const userLocation = [position.coords.longitude, position.coords.latitude];
    map.setCenter(userLocation);
});

let coordinates = [];
function flyToLocation(coordinates) {
  map.flyTo({
      center: coordinates,
      zoom: 14,
      speed: 1.2,
      // cs50 helped me with the speed by telling me about essential
      essential: true
  });
  new mapboxgl.Marker()
      .setLngLat(coordinates)
      .addTo(map);
};

function drawRoute(route1) {
    map.addLayer({
      id: 'route',
      type: 'line',
      source: {
        type: 'geojson',
        data: {
          type: 'Feature',
          properties: {},
          geometry: route1
        }
      },
      layout: {
        'line-join': 'round',
        'line-cap': 'round'
      },
      paint: {
        'line-color': '#3887be',
        'line-width': 5,
        'line-opacity': 0.75
      }
    });
  }