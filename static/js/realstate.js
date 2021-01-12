d3.json("/api/realstatelistings").then((data) => {
    console.log(data);

    var averagePrice = 0
    data.forEach(element => {
        averagePrice = averagePrice + element.price;
    })
    averagePrice = Math.round(averagePrice / data.length);

    document.getElementById('RealStateTotal').textContent = `${data.length}`;
    document.getElementById('AveragePrice').textContent = `$${averagePrice.toLocaleString()}`;

    // To use OpenStreetMap instead of MapBox
    var attribution = "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>";
    var titleUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var OpenStreetTiles = L.tileLayer(titleUrl, { attribution });

    realstatemarkers = []
    data.forEach(element => {
        var marker = L.marker([element.latitude, element.longitude])
            .bindPopup(`<h6>Details:</h6> <hr> 
            <strong>Price:</strong> $${(element.price).toLocaleString()} <br/>
            <strong>Address:</strong> ${element.address} <br/>
            <strong>More info:</strong> <a href="${element.house_link}" target = "_blank">click here</a> <br/>`);
        realstatemarkers.push(marker);
    })

    var realstateLayer = L.layerGroup(realstatemarkers);

    // Leaft let map
    var map = L.map('map', {
        center: [29.75, -95.37],
        zoom: 8.5,
        scrollWheelZoom: false, //Disable scroll wheel zoom on Leaflet
        fullscreenControl: true,
        layers: [OpenStreetTiles, realstateLayer]
    });
    var baseMaps = {
        "Streets": OpenStreetTiles
    };

    var overlayMaps = {
        "Houses": realstateLayer
    };

    L.control.layers(baseMaps, overlayMaps).addTo(map);


    // Plotly bubble chart
    var trace1 = {
        x: data.map(element => element.sqft),
        y: data.map(element => element.price),
        text: ['A<br>size: 40', 'B<br>size: 60', 'C<br>size: 80', 'D<br>size: 100'],
        mode: 'markers',
        marker: {
            // color: ['rgb(93, 164, 214)', 'rgb(255, 144, 14)', 'rgb(44, 160, 101)', 'rgb(255, 65, 54)'],
            // size: data.map(element => element.lot / 1000)
        }
    };

    var data = [trace1];

    var layout = {
        title: 'House Price vs. Size',
        showlegend: false,
        height: 600,
        width: 1000,
        xaxis: {
            title: "Size (sqft)"
        },
        yaxis: {
            title: "Price ($)"
        }
    };

    Plotly.newPlot('bubbleChart', data, layout);
})
