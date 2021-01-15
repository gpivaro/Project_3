

// Define a function we want to run once for each feature in the features array
function addPopup(feature, layer) {
    // Give each feature a popup describing the place and time of the earthquake
    return layer.bindPopup(`<p><span style="font-weight: bold;">Zip Code: </span>${feature.properties.ZCTA5CE10}</p>`);
}

d3.json("/api/realstatelistings").then((data) => {
    console.log(data);

    var averagePrice = 0
    data.forEach(element => {
        averagePrice = averagePrice + element.price;
    })
    averagePrice = Math.round(averagePrice / data.length);

    document.getElementById('RealStateTotal').textContent = `${data.length.toLocaleString()}`;
    document.getElementById('AveragePrice').textContent = `$${averagePrice.toLocaleString()}`;

    // To use OpenStreetMap instead of MapBox
    var attribution = '"Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> \
                        contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, \
                        Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>"';
    var titleUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var OpenStreetTiles = L.tileLayer(titleUrl, { attribution });

    realstatemarkers = []
    data.forEach(element => {
        var marker = L.marker([element.latitude, element.longitude])
            .bindPopup(`<h6>House details:</h6> <hr> 
            <img style="height: 120px;" src="${element.image_1}"><br/><br/>
            <strong>Price:</strong> $${(element.price).toLocaleString()} <br/>
            <strong>Address:</strong> ${element.address} <br/>
            <strong>More info:</strong> <a href="${element.house_link}" target = "_blank">click here</a> <br/>`);
        realstatemarkers.push(marker);
    })

    var realstateLayer = L.layerGroup(realstatemarkers);


    url_zip_codes = "static/data/HOUSTON_ZIPCODES_GEOJSON.json"
    // url_zip_codes = "https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/tx_texas_zip_codes_geo.min.json"

    // Data Loading in D3: https://www.tutorialsteacher.com/d3js/loading-data-from-file-in-d3js
    // Promises chaining https://javascript.info/promise-chaining
    // Using GeoJSON with Leaflet https://leafletjs.com/examples/geojson/
    // url_tectonics = 'https://raw.githubusercontent.com/gpivaro/leaflet-challenge/main/data/tectonicplates-master/GeoJSON/PB2002_boundaries.json'
    // d3.json("/data/tectonicplates-master/GeoJSON/PB2002_boundaries.json").then((tectonicPlatesData) => {
    d3.json(url_zip_codes).then((TexasZipCodeData) => {
        console.log(TexasZipCodeData);
        console.log(TexasZipCodeData.features);
        console.log(TexasZipCodeData.features[0].properties.ZCTA5CE10);


        var zipCodesLayer = L.geoJSON(TexasZipCodeData, {
            onEachFeature: addPopup,
            color: "black"
        });

        // Leaft let map
        var map = L.map('mapMap', {
            center: [29.75, -95.37],
            zoom: 13,
            scrollWheelZoom: false, //Disable scroll wheel zoom on Leaflet
            fullscreenControl: true,
            layers: [OpenStreetTiles, realstateLayer, zipCodesLayer]
        });

        var baseMaps = {
            "Streets": OpenStreetTiles
        };

        var overlayMaps = {
            "Houses": realstateLayer,
            "Zip Codes": zipCodesLayer
        };

        L.control.layers(baseMaps, overlayMaps, { collapsed: true }).addTo(map);

    });


    // Get Zip Code from address
    var addressString = data[0].address.split(" ");
    console.log(addressString[addressString.length - 1])


})
