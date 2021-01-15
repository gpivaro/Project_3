var height_size = 500;
var width_size = 550;

// Responsive chart
var config = { responsive: true }

d3.json("/api/realstatelistings").then((data) => {
    console.log(data);

    var averagePrice = 0
    data.forEach(element => {
        averagePrice = averagePrice + element.price;
    })
    averagePrice = Math.round(averagePrice / data.length);

    document.getElementById('RealStateTotal').textContent = `${data.length}`;
    document.getElementById('AveragePrice').textContent = `$${averagePrice.toLocaleString()}`;


    // Plotly bubble chart
    var trace1 = {
        x: data.map(element => element.sqft),
        y: data.map(element => element.price),
        text: ['A<br>size: 40', 'B<br>size: 60', 'C<br>size: 80', 'D<br>size: 100'],
        mode: 'markers',
        marker: {
            color: data.map(element => element.lot / 1000),
            // size: data.map(element => element.lot / 1000)
        }
    };

    var dataPlot1 = [trace1];

    var layout = {
        title: 'House Price vs. Size',
        showlegend: false,
        height: height_size,
        width: width_size,
        margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 0,
            pad: 0
        },
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
        margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 0,
            pad: 0
        },
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
