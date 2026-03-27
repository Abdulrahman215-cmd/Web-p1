document.addEventListener('DOMContentLoaded', function checked() {
  const fromInput = document.getElementById('starting-point');
  const toInput = document.getElementById('ending-point');
  const submitButton1 = document.querySelector('#submit_direct');
  function checkInput1() {
    submitButton1.disabled = fromInput.value.length === 0 || toInput.value.length === 0;
  }

  fromInput.addEventListener('input', checkInput1);
  toInput.addEventListener('input', checkInput1);
  
  checkInput1();
});

document.getElementById('direction').addEventListener('submit', function(event) {
    event.preventDefault();
    const from = document.getElementById('starting-point').value;
    const to = document.getElementById('ending-point').value;
    directions(from, to);
  });

  function directions(from, to) {
    // cs50 ai told me about doing this 3 fetches inside one function
    const url1 = `https://api.mapbox.com/geocoding/v5/mapbox.places/${from}.json?access_token=${ACCESS_TOKEN}`;
    fetch(url1)
    .then(response => response.json())
    .then(data => {
        const coordinatesFrom = data.features[0].center;
        flyToLocation(coordinatesFrom);
        const url2 = `https://api.mapbox.com/geocoding/v5/mapbox.places/${to}.json?access_token=${ACCESS_TOKEN}`;
        fetch(url2)
        .then(response => response.json())
        .then(data => {
            const coordinatesTo = data.features[0].center;
            flyToLocation(coordinatesTo);
            fetchRoute(coordinatesFrom, coordinatesTo);

            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            fetch(directUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ from: from, to: to })
            })
            .then(response => response.json())
            .then(data => {
              console.log(data);
            })
            .catch(error => {
              console.error('Error:', error);
          });
        });
    });
}

function fetchRoute(coordinatesFrom, coordinatesTo) {
  const url = `https://api.mapbox.com/directions/v5/mapbox/driving/${coordinatesFrom[0]},${coordinatesFrom[1]};${coordinatesTo[0]},${coordinatesTo[1]}?geometries=geojson&steps=true&overview=full&annotations=speed,distance&access_token=${ACCESS_TOKEN}`;
    fetch(url)
    .then(response => response.json())
    .then(data => {
        const route1 = data.routes[0].geometry;
        const route = data.routes[0];
        const distance = route.distance; // Distance in meters
        const duration = route.duration; // Duration in seconds

        const distanceKm = (distance / 1000).toFixed(1); // Convert to kilometers
        // cs50 ai helped me with this line
        const timeDisplay = duration < 3600 ? `${(duration / 60).toFixed(2)} mins` : `${(duration / 3600).toFixed(2)} hours`;

        const popup = new mapboxgl.Popup()
        .setLngLat(coordinatesTo)
        .setHTML(`<div style="padding-right: 10px;">Distance: ${distanceKm} km<br>Time: ${timeDisplay}</div>`)
        .addTo(map);
        drawRoute(route1);
  });
}

  document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('starting-point').addEventListener('input', function() {
        const query = this.value;
        const username = theUser;
        if (query.length > 2) { 
          fetchSuggestions1(query);
        }  else if (query.length === 0) {
          if (username) {
            displaySearchHistory1();
          } else {
              const suggestionsDiv1 = document.getElementById('suggestions1');
              suggestionsDiv1.innerHTML = '';
          }
        }
    });

    document.getElementById('ending-point').addEventListener('input', function() {
        const query = this.value;
        const username = theUser;
        if (query.length > 2) { 
          fetchSuggestions1(query);
        } else if (query.length === 0) {
          if (username) {
            displaySearchHistory1();
          } else {
              const suggestionsDiv1 = document.getElementById('suggestions1');
              suggestionsDiv1.innerHTML = '';
          }
        }
    });
})

function fetchSuggestions1(query) {
  const url3 = `https://api.mapbox.com/geocoding/v5/mapbox.places/${query}.json?access_token=${ACCESS_TOKEN}`;
    fetch(url3)
    .then(response => response.json())
    .then(data => {
        const suggestions = data.features.map(feature => feature.place_name);
        displaySuggestions1(suggestions);
    });
  }    

  function displaySuggestions1(suggestions) {
    const suggestionBox = document.getElementById('suggestions1');
    suggestionBox.innerHTML = '';
    suggestions.forEach((suggestion) => {
        const Hr = document.createElement('hr');
        Hr.id = 'hr1';
        suggestionBox.appendChild(Hr);
        const suggestionItem = document.createElement('div');
        suggestionItem.classList.add('search-item1'); 
        suggestionItem.setAttribute('data-query', suggestion);
        suggestionItem.textContent = suggestion;
        suggestionBox.appendChild(suggestionItem);
    });
}

document.addEventListener('DOMContentLoaded', function() {
  const startingPointInput = document.getElementById('starting-point');
  const endingPointInput = document.getElementById('ending-point');
  const suggestionsDiv = document.getElementById('suggestions1');

  let lastClickedInput = null;

  startingPointInput.addEventListener('focus', function() {
    lastClickedInput = startingPointInput;
    suggestionsDiv.style.display = 'block';
  });

  endingPointInput.addEventListener('focus', function() {
    lastClickedInput = endingPointInput;
    suggestionsDiv.style.display = 'block';
  });

  suggestionsDiv.addEventListener('click', function(event) {
    const query = event.target.getAttribute('data-query');
    const submitButton1 = document.querySelector('#submit_direct');
    if (query) {
      // cs50 ai helped me with the split and include
      if (query.includes(' - ')) {
        const [start, end] = query.split(' - ');
        startingPointInput.value = start;
        endingPointInput.value = end;
        submitButton1.disabled = startingPointInput.value.length === 0 || endingPointInput === 0;
      } else {
        lastClickedInput.value = query;
      }
      suggestionsDiv.style.display = 'none';
    }
  });
});

function displaySearchHistory1() {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  fetch(directUrl, {
      method: 'GET',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
      }
  })
  .then(response => response.json())
  .then(data => {
      const suggestionsDiv1 = document.getElementById('suggestions1');
      suggestionsDiv1.innerHTML = '';
      data.history1.forEach(item => {
          const Hr = document.createElement('hr');
          Hr.id = 'hr1';
          suggestionsDiv1.appendChild(Hr);
          const newSuggestion1 = document.createElement('p');
          newSuggestion1.className = 'search-item1';
          newSuggestion1.textContent = `${item.start} - ${item.end}`;
          suggestionsDiv1.appendChild(newSuggestion1);
          newSuggestion1.addEventListener('click', function() {
            document.getElementById('starting-point').value = item.start;
            document.getElementById('ending-point').value = item.end;
            const submitButton1 = document.querySelector('#submit_direct');
            submitButton1.disabled = false;
            suggestionsDiv1.style.display = 'none';
            checked();
          });
      });
  });
}