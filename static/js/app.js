var username = document.getElementById("UserName").value;
console.log(username);


d3.json(`/api/userselections/${username}`).then((userdata) => {
    console.log(userdata);
    var userPreviousSelectionArray = userdata.map(element => element.house_id);
    console.log(userPreviousSelectionArray);

    d3.json("/api/realstatelistings").then((data) => {
        console.log(data);

        var houseSelect = 0;
        if (userPreviousSelectionArray.lenght != data.lenght) {

            console.log('No more houses to select')
            var myobj = document.getElementById("housePhotoPage");
            myobj.remove();

            var myobj = document.getElementById("myForm");
            myobj.remove();

        }
        else {
            // Selector to show only houses with no evaluation yet
            while (userPreviousSelectionArray.includes(data[houseSelect].house_id)) {
                console.log("Same Number");
                houseSelect++;
                console.log(houseSelect);
            }



            document.getElementById("housePhotoPage").src = `${data[houseSelect].image_1}`;

            // document.getElementById("myAnchor").innerHTML = `Address: ${data[houseSelect].address}`;
            // document.getElementById("myAnchor").href = `${data[houseSelect].house_link}`;
            // document.getElementById("myAnchor").target = "_blank";

            document.getElementById('Price').textContent = `Price: $${(data[houseSelect].price).toLocaleString()}`;
            document.getElementById('Address').textContent = `${data[houseSelect].address}`;
            document.getElementById('Beds').textContent = `${data[houseSelect].bed} bed(s)`;
            document.getElementById('Baths').textContent = `${data[houseSelect].bath} bath(s)`;
            document.getElementById('Sqft').textContent = `${data[houseSelect].sqft} sqft`;
            document.getElementById('Date').textContent = `Added on: ${data[houseSelect].created_date}`;



            // document.getElementById("houseWebPage").src = `${data[0].house_link}`;

            // Leaft let map
            var map = L.map('map', {
                scrollWheelZoom: false, //Disable scroll wheel zoom on Leaflet
                fullscreenControl: true,
            }
            ).setView([data[houseSelect].latitude, data[houseSelect].longitude], 10);

            // To use OpenStreetMap instead of MapBox
            var attribution = "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>";
            var titleUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
            var OpenStreetTiles = L.tileLayer(titleUrl, { attribution }).addTo(map);

            L.marker([data[houseSelect].latitude, data[houseSelect].longitude]).addTo(map)
                .bindPopup(`<h6>Details:</h6> <hr> 
                <strong>Price:</strong> $${(data[houseSelect].price).toLocaleString()} <br/>
                <strong>Address:</strong> ${data[houseSelect].address} <br/>
                <strong>More info:</strong> <a href="${data[houseSelect].house_link}" target = "_blank">click here</a> <br/>`)
                .openPopup();


            document.getElementById("houseID").value = `${data[houseSelect].house_id}`;
            document.getElementById("houseID").type = "hidden";
        }

    })
})




// // Display data on the page
// https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_elmnt_innerhtml
// function myFunction() {
//     document.getElementById("myAnchor").innerHTML = `${data[0].address}`;
//     document.getElementById("myAnchor").href = `${data[0].house_link}`;
//     document.getElementById("myAnchor").target = "_blank";
// }