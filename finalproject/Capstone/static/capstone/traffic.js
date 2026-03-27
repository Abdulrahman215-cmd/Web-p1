let trafficMode = false;
let popup = new mapboxgl.Popup();

document.getElementById('trafficButton').addEventListener('click', () => {
    trafficMode = !trafficMode;
});

map.on('load', () => {
    // cs50 ai helped me in this line
    const savedTrafficData = JSON.parse(localStorage.getItem('trafficData')) || [];
    savedTrafficData.forEach((data, index) => {
        // and this
        if (data && data.lineCoordinates && data.lineCoordinates.length > 0) {
            const sourceId = `highlighted-street-${index}`;
        
        if (map.getSource(sourceId)) {
            map.removeSource(sourceId);
        }
        
        map.addSource(sourceId, {
            'type': 'geojson',
            'data': {
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': data.lineCoordinates
                }
            }
        });
        map.addLayer({
            'id': `highlighted-street-layer-${index}`,
            'type': 'line',
            'source': sourceId,
            'layout': {
                'line-join': 'round',
                'line-cap': 'round'
            },
            'paint': {
                'line-color': '#FF0000',
                'line-width': 5
            }
        });
        let closeButtonHTML = '';
            if (username === data.username) {
                closeButtonHTML = '<button class="btn btn-danger" id="close-button">Close</button>';
            }
            
        const popup = new mapboxgl.Popup()
            .setLngLat(data.lngLat)
            .setHTML(`
                <div>
                    <h3>${data.name}</h3>
                    <p>Reported by: <a href="${data.profileLink}">${data.username}</a></p>
                    ${closeButtonHTML}
                </div>
            `)
            .addTo(map);
            if (username === data.username) {
                document.getElementById(`close-button`).addEventListener('click', () => {

                    popup.remove();

                    map.removeLayer(`highlighted-street-layer-${index}`);
                    map.removeSource(sourceId);

                    // cs50 ai gave me this line of code
                    savedTrafficData.splice(index, 1);

                    localStorage.setItem('trafficData', JSON.stringify(savedTrafficData));
                   });
            
                }
        }
        });
    map.on('click', (e) => {
        if (!trafficMode) return;

        const features = map.queryRenderedFeatures(e.point, {
            layers: [
                'road-minor', 'road-street', 'road-secondary-tertiary', 
                'road-primary', 'road-motorway-trunk',
                'bridge-minor', 'bridge-street', 'bridge-secondary-tertiary', 
                'bridge-primary', 'bridge-motorway-trunk'
            ]
        });

        if (features.length > 0) {
            const feature = features[0];
            const lineCoordinates = feature.geometry.coordinates;

            if (map.getLayer('highlighted-street')) {
                map.removeLayer('highlighted-street');
            }
            if (map.getSource('highlighted-street')) {
                map.removeSource('highlighted-street');
            }

            map.addSource('highlighted-street', {
                'type': 'geojson',
                'data': feature.toJSON()
            });
            map.addLayer({
                'id': 'highlighted-street',
                'type': 'line',
                'source': 'highlighted-street',
                'layout': {
                    'line-join': 'round',
                    'line-cap': 'round'
                },
                'paint': {
                    'line-color': '#FF0000',  // Red color
                    'line-width': 5
                }
            });
            const trafficInfo = {
                name: feature.properties.name,
                lngLat: e.lngLat,
                username: username,
                profileLink: profileLink,
                lineCoordinates: lineCoordinates
            };
            let closeButtonHTML = '';
            if (username === trafficInfo.username) {
                closeButtonHTML = '<button class="btn btn-danger" id="close-button">Close</button>';
            }
                const popup = new mapboxgl.Popup()
                    .setLngLat(e.lngLat)
                    .setHTML(`
                    <div>
                        <h3>${feature.properties.name}</h3>
                        <p>Reported by: <a href="${profileLink}">${username}</a></p>
                        ${closeButtonHTML}
                    </div>
                    `)
                    .addTo(map);
                if (username === trafficInfo.username) {
                    document.getElementById('close-button').addEventListener('click', () => {
                        popup.remove();
                        map.removeLayer('highlighted-street');
                        map.removeSource('highlighted-street');

                    localStorage.setItem('trafficData', JSON.stringify(savedTrafficData));
                    
            });
        }
        // cs50 ai helped me with localstorage
        let trafficData = JSON.parse(localStorage.getItem('trafficData')) || [];
        trafficData.push(trafficInfo);
        localStorage.setItem('trafficData', JSON.stringify(trafficData));
        }
    });
});