document.addEventListener('DOMContentLoaded', function() {
  const queryInput = document.getElementById('search-query');
  const submitButton = document.querySelector('#submit_search');
  queryInput.addEventListener('input', function() {
      submitButton.disabled = queryInput.value.length === 0;
  });
  checkInput();
});

function checkInput() {
  const query = document.getElementById('search-query').value;
  const submitButton = document.querySelector('#submit_search');
  submitButton.disabled = query.length === 0;
}

document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const query = document.getElementById('search-query').value;
    searchLocation(query);
    checkInput();
  });
  
  function searchLocation(query) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(searchUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify({ 'search-query': query})
    })
    .then(response => response.json())
    .then(data => {
      console.log(data); 
      if (data.success) {
        updateMap(query);
      } else {
        console.error("Error updating search history.");
      }
    });
  }
  
  document.querySelectorAll('.search-item').forEach(item => {
    item.addEventListener('click', function() {
      const query = this.getAttribute('data-query');
      updateMap(query);
    });
  });
  
  function updateMap(query) {
    const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${query}.json?access_token=${ACCESS_TOKEN}`;
    fetch(url)
      .then(response => response.json())
      .then(data => {
        if (data.features && data.features.length > 0) {
          const newCoordinates = data.features[0].center;
          flyToLocation(newCoordinates);
        } else {
          console.error("No features found for the query.");
        }
      });
  }
  
  document.getElementById('search-query').addEventListener('input', function () {
    const query = this.value;
    const username = theUser;
    if (query.length > 2) {
        fetchSuggestions(query);
    } else if (query.length === 0) {
        if (username) {
            displaySearchHistory();
        } else {
            const suggestionsDiv = document.getElementById('suggestions');
            suggestionsDiv.innerHTML = '';
        }
    }
});
  
  function fetchSuggestions(query) {
      const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${query}.json?access_token=${ACCESS_TOKEN}`;
      fetch(url)
          .then(response => response.json())
          .then(data => {
              displaySuggestions(data.features);
          });
  }
  
  function displaySuggestions(features) {
    const suggestions = document.getElementById('suggestions');
    suggestions.innerHTML = '';
    // cs50 ai told me to use index and everything about index in these files was because of cs50 ai
    features.forEach((feature, index) => {
      const suggestion = document.createElement('div');
      suggestion.classList.add('search-item'); 
      const Hr = document.createElement('hr');
      Hr.id = 'hr';
      suggestions.appendChild(Hr);
      // cs50 helped me with textcontent
      suggestion.textContent = `${feature.place_name}`;
      suggestion.dataset.index = index;
      suggestion.addEventListener('click', () => {
        document.getElementById('search-query').value = feature.place_name;
        suggestions.innerHTML = '';
      });
      suggestions.appendChild(suggestion);
    });
  }
  
  function displaySearchHistory() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(searchUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        const suggestionsDiv = document.getElementById('suggestions');
        suggestionsDiv.innerHTML = '';
        data.history.forEach(item => {
            const Hr = document.createElement('hr');
            Hr.id = 'hr';
            suggestionsDiv.appendChild(Hr);
            const newSuggestion = document.createElement('p');
            newSuggestion.className = 'search-item';
            newSuggestion.textContent = `${item.query}`;
            suggestionsDiv.appendChild(newSuggestion);
            newSuggestion.addEventListener('click', function() {
              const query = item.query;
              updateMap(query);
              });
        });
    });
}