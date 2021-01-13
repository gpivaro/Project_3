var height_size = 500;
var width_size = 550;

// Responsive chart
var config = { responsive: true }

// Define a function we want to run once for each feature in the features array
function addPopup(feature, layer) {
    // Give each feature a popup describing the place and time of the earthquake
    return layer.bindPopup(`<h6 style="font-weight: bold;">Zip Code: ${feature.properties.ZCTA5CE10}</h6>`);
}

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



    url_zip_codes = "https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/tx_texas_zip_codes_geo.min.json"

    // Data Loading in D3: https://www.tutorialsteacher.com/d3js/loading-data-from-file-in-d3js
    // Promises chaining https://javascript.info/promise-chaining
    // Using GeoJSON with Leaflet https://leafletjs.com/examples/geojson/
    // url_tectonics = 'https://raw.githubusercontent.com/gpivaro/leaflet-challenge/main/data/tectonicplates-master/GeoJSON/PB2002_boundaries.json'
    // d3.json("/data/tectonicplates-master/GeoJSON/PB2002_boundaries.json").then((tectonicPlatesData) => {
    d3.json(url_zip_codes).then((TexasZipCodeData) => {
        console.log(TexasZipCodeData);
        console.log(TexasZipCodeData.features);
        console.log(TexasZipCodeData.features[0].properties.ZCTA5CE10);

        TexasZipCodeData.features.forEach(element => {
            if (element.properties.ZCTA5CE10 === "77002") {
                console.log(element)
            }
        })

        var zipCodesLayer = L.geoJSON(TexasZipCodeData, {
            onEachFeature: addPopup,
        });


        // Leaft let map
        var map = L.map('map', {
            center: [29.75, -95.37],
            zoom: 8.5,
            scrollWheelZoom: false, //Disable scroll wheel zoom on Leaflet
            fullscreenControl: true,
            layers: [OpenStreetTiles, realstateLayer]
        });
        var baseMaps = {
            "Streets Map": OpenStreetTiles
        };

        var overlayMaps = {
            "Houses": realstateLayer,
            "Zip Codes": zipCodesLayer
        };

        L.control.layers(baseMaps, overlayMaps).addTo(map);

    });



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

    var dataPlot1 = [trace1];

    var layout = {
        title: 'House Price vs. Size',
        showlegend: false,
        height: height_size,
        width: width_size,
        xaxis: {
            title: "Size (sqft)"
        },
        yaxis: {
            title: "Price ($)"
        }
    };

    Plotly.newPlot('bubbleChart', dataPlot1, layout, config);

    var trace2 = {
        x: data.map(element => element.latitude),
        y: data.map(element => element.longitude),
        text: ['A<br>size: 40', 'B<br>size: 60', 'C<br>size: 80', 'D<br>size: 100'],
        mode: 'markers',
        marker: {
            color: data.map(element => element.lot / 1000),
            // size: data.map(element => element.lot / 1000)
        }
    };

    var layout = {
        title: 'House Location vs. Price',
        showlegend: false,
        height: height_size,
        width: width_size,
        xaxis: {
            title: "Latitude"
        },
        yaxis: {
            title: "Longitude"
        }
    };

    var dataPlot2 = [trace2];


    Plotly.newPlot('scatterPlot', dataPlot2, layout, config);




})
