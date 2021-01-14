/* Date.prototype.toLocaleDateString()
     https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleDateString */
var options = { year: 'numeric', month: 'numeric', day: 'numeric' };
options.timeZone = 'UTC';

var username = document.getElementById("UserName").value;
console.log(`Current username: ${username}`);


d3.json(`/api/userselections/${username}`).then((userdata) => {
    console.log(userdata);
    var userPreviousSelectionArray = userdata.map(element => element.house_id);

    d3.json("/api/realstatelistings").then((data) => {
        console.log(data);

        // For randomization of houses presented for selection
        var houseSelect = Math.floor(Math.random() * Object.keys(data).length);

        // ********* --->>>>    For debug
        // Use this values to force a scenario where the user has no more houses to select from.
        // var houseSelect = (Object.keys(data).length) - 1;
        // userPreviousSelectionArray = [data[(Object.keys(data).length) - 1].house_id];
        // console.log(data[(Object.keys(data).length) - 1].house_id);


        console.log(`Selected house_id: ${data[houseSelect].house_id}`);
        if (userPreviousSelectionArray.lenght != data.lenght) {

            console.log('No more houses to select')
            // var myobj = document.getElementById("housePhotoPage");
            // myobj.remove();

            // var myobj = document.getElementById("myForm");
            // myobj.remove();

        }
        else {
            // Selector to show only houses with no evaluation yet
            while (userPreviousSelectionArray.includes(data[houseSelect].house_id)) {
                console.log("Already classified by the user.");

                houseSelect++;
                console.log(houseSelect)
                if (houseSelect === Object.keys(data).length) {
                    console.log('Stop')
                    // Simulate an HTTP redirect:
                    window.location.replace("/end-classification");
                    break
                }
            }

            // ********* --->>>>    For debug
            console.log('--------------------------');
            console.log(`Selected house_id: ${data[houseSelect].house_id}`);
            console.log(data[houseSelect]);

            var added_date = data[houseSelect].created_date;
            document.getElementById('Price').textContent = `$${(data[houseSelect].price).toLocaleString()}`;
            document.getElementById('Address').textContent = `${data[houseSelect].address}`;
            document.getElementById('Beds').textContent = `${data[houseSelect].bed}`;
            document.getElementById('Baths').textContent = `${data[houseSelect].bath}`;
            document.getElementById('Sqft').textContent = `${(data[houseSelect].sqft).toLocaleString()}`;

            if (data[houseSelect].lot === 0) {
                document.getElementById('SqftLot').textContent = `N/A`;
            }
            else {
                document.getElementById('SqftLot').textContent = `${(data[houseSelect].lot).toLocaleString()}`;
            }


            document.getElementById('Date').textContent = `Added to the database on: ${added_date}`;

            var myobj = document.getElementById("housePhotoPage_1");
            var myobj = document.getElementById("mapLoading");
            myobj.remove();

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
                <strong>More info:</strong> <a href="${data[houseSelect].house_link}" target = "_blank">click here</a> <br/>`);
            // .openPopup();


            // Insert the house photo on the carousel
            if (data[houseSelect].image_1) {
                document.getElementById("housePhotoPage_1").src = `${data[houseSelect].image_1}`;
            }
            // If only one image available, show the same image on both slides
            if (data[houseSelect].image_2) {
                document.getElementById("housePhotoPage_2").src = `${data[houseSelect].image_2}`;
            }
            else {
                document.getElementById("housePhotoPage_2").src = `${data[houseSelect].image_1}`;
                // var myobj = document.getElementsByClassName("carousel-item");
                // myobj.remove();
            }



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