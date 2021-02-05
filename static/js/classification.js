/* Date.prototype.toLocaleDateString()
     https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleDateString */
var options = { year: 'numeric', month: 'numeric', day: 'numeric' };
options.timeZone = 'UTC';

var username = document.getElementById("UserName").value;
console.log(`Current username: ${username}`);



d3.json(`/api/userselections/${username}`).then((userdata) => {
    console.log(userdata);
    var userPreviousSelectionArray = userdata.map(element => element.house_id);
    console.log(`Previous selection ${userPreviousSelectionArray[Object.keys(userPreviousSelectionArray).length - 1]}`)

    var previous_selection = userdata[Object.keys(userdata).length - 1];
    if (previous_selection === undefined) {
        var previous_selection = {}
        previous_selection.house_id = 1;
    }


    // Verify the house cluster for the previous user selection
    d3.json(`/api/house-cluster/${previous_selection.house_id}`).then((houseCluster) => {

        var previous_selection_cluster = houseCluster.house_cluster
        var previous_selection_choice = previous_selection.user_choice
        console.log(`Previous cluster: ${previous_selection_cluster} | choice: ${previous_selection_choice}`);


        if (previous_selection_choice != 'Dislike') {
            var targetCluster = previous_selection_cluster;
        }
        else {
            var targetCluster = (previous_selection_cluster + 1) % 3;
        }
        console.log(`Target cluster: ${targetCluster}`);

        d3.json("/api/realstatelistings").then((realEstateData) => {
            // console.log(realEstateData);
            // Filter houses by the cluster they are in

            var housesOnTargetCluster = []
            realEstateData.forEach(element => {
                if (element.cluster === targetCluster) {
                    housesOnTargetCluster.push(element)
                }
            })

            /* ******************************************************************************** */
            /* ******************************************************************************** */


            // For randomization of houses presented for selection
            var houseSelect = Math.floor(Math.random() * Object.keys(housesOnTargetCluster).length);

            // ********* --->>>>    For debug
            // Use this values to force a scenario where the user has no more houses to select from.
            // var houseSelect = (Object.keys(data).length) - 1;
            // userPreviousSelectionArray = [data[(Object.keys(data).length) - 1].house_id];
            // console.log(data[(Object.keys(data).length) - 1].house_id);


            console.log(`Selected house_id: ${housesOnTargetCluster[houseSelect].house_id}`);
            if (userPreviousSelectionArray.lenght != housesOnTargetCluster.lenght) {

                console.log('No more houses to select')
                // var myobj = document.getElementById("housePhotoPage");
                // myobj.remove();

                // var myobj = document.getElementById("myForm");
                // myobj.remove();

            }
            else {
                // Selector to show only houses with no evaluation yet
                while (userPreviousSelectionArray.includes(housesOnTargetCluster[houseSelect].house_id)) {
                    console.log("Already classified by the user.");

                    houseSelect++;
                    console.log(houseSelect)

                    if (houseSelect === Object.keys(housesOnTargetCluster).length) {
                        console.log('Stop')
                        // Simulate an HTTP redirect:
                        window.location.replace("/end-classification");
                        break
                    }
                }




                // ********* --->>>>    For debug
                console.log('--------------------------');
                console.log(`Selected house_id: ${housesOnTargetCluster[houseSelect].house_id}`);
                console.log(housesOnTargetCluster[houseSelect]);


                var added_date = housesOnTargetCluster[houseSelect].created_date;
                document.getElementById('Price').textContent = `$${(housesOnTargetCluster[houseSelect].price).toLocaleString()}`;
                document.getElementById('Address').textContent = `${housesOnTargetCluster[houseSelect].address}`;
                document.getElementById('Beds').textContent = `${housesOnTargetCluster[houseSelect].bed}`;
                document.getElementById('Baths').textContent = `${housesOnTargetCluster[houseSelect].bath}`;
                document.getElementById('Sqft').textContent = `${(housesOnTargetCluster[houseSelect].sqft).toLocaleString()}`;

                if (housesOnTargetCluster[houseSelect].lot === 0) {
                    document.getElementById('SqftLot').textContent = `N/A`;
                }
                else {
                    document.getElementById('SqftLot').textContent = `${(housesOnTargetCluster[houseSelect].lot).toLocaleString()}`;
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
                ).setView([housesOnTargetCluster[houseSelect].latitude, housesOnTargetCluster[houseSelect].longitude], 10);

                // To use OpenStreetMap instead of MapBox
                var attribution = "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>";
                var titleUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
                var OpenStreetTiles = L.tileLayer(titleUrl, { attribution }).addTo(map);

                L.marker([housesOnTargetCluster[houseSelect].latitude, housesOnTargetCluster[houseSelect].longitude]).addTo(map)
                    .bindPopup(`<h6>Details:</h6> <hr> 
                <strong>Price:</strong> $${(housesOnTargetCluster[houseSelect].price).toLocaleString()} <br/>
                <strong>Address:</strong> ${housesOnTargetCluster[houseSelect].address} <br/>
                <strong>More info:</strong> <a href="${housesOnTargetCluster[houseSelect].house_link}" target = "_blank">click here</a> <br/>`);
                // .openPopup();


                // Insert the house photo on the carousel
                if (housesOnTargetCluster[houseSelect].image_1) {
                    document.getElementById("housePhotoPage_1").src = `${housesOnTargetCluster[houseSelect].image_1}`;
                }
                // If only one image available, show the same image on both slides
                if (housesOnTargetCluster[houseSelect].image_2) {
                    document.getElementById("housePhotoPage_2").src = `${housesOnTargetCluster[houseSelect].image_2}`;
                }
                else {
                    document.getElementById("housePhotoPage_2").src = `${housesOnTargetCluster[houseSelect].image_1}`;
                    // var myobj = document.getElementsByClassName("carousel-item");
                    // myobj.remove();
                }



                document.getElementById("houseID").value = `${housesOnTargetCluster[houseSelect].house_id}`;
                document.getElementById("houseID").type = "hidden";
            }


            /* ******************************************************************************** */
            /* ******************************************************************************** */


        })


    })

})