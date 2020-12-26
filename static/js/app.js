


d3.json("/api/realstatelistings").then((data) => {
    console.log(data);



    document.getElementById("housePhotoPage").src = `${data[0].photolink}`;

    document.getElementById("myAnchor").innerHTML = `${data[0].address}`;
    document.getElementById("myAnchor").href = `${data[0].house_link}`;
    document.getElementById("myAnchor").target = "_blank";

    // document.getElementById("houseWebPage").src = `${data[0].house_link}`;

    // Leaft let map
    var map = L.map('map').setView([data[0].latitude, data[0].longitude], 14);

    // To use OpenStreetMap instead of MapBox
    var attribution = "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>";
    var titleUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var OpenStreetTiles = L.tileLayer(titleUrl, { attribution }).addTo(map);

    L.marker([data[0].latitude, data[0].longitude]).addTo(map)
        .bindPopup(`<h6>Details:</h6> <hr> 
                    <strong>Price:</strong> $${(data[0].price).toLocaleString()} <br/>
                    <strong>Address:</strong> ${data[0].address} <br/>
                    <strong>More info:</strong> <a href="${data[0].house_link}" target = "_blank">click here</a> <br/>`)
        .openPopup();


})


// // Display data on the page
// https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_elmnt_innerhtml
// function myFunction() {
//     document.getElementById("myAnchor").innerHTML = `${data[0].address}`;
//     document.getElementById("myAnchor").href = `${data[0].house_link}`;
//     document.getElementById("myAnchor").target = "_blank";
// }