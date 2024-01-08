// The url with data
const url = "http://127.0.0.1:5000/api/v1.0/map"

// Display the default plots
function init() {

        d3.select("#container").html("");
        d3.json(url).then((results) => {
            var map = anychart.map();
            map.geoData(anychart.maps.united_states_of_america);

            // set the series
            var series = map.choropleth(results);

            // enable labels
            series.labels(true);

            // enable the tooltips and format them at once
            series.tooltip().format(function(e){
               return "State ID: " + e.getData("id") +"\n"+
               "Total Sales: $" + e.getData("value")
            });

            var scale = anychart.scales.ordinalColor([
                  { less: 3500 },
                  { from: 3501, to: 3800 },
                  { from: 3801, to: 4100 },
                  { from: 4101, to: 4400 },
                  { from: 4401, to: 4700 },
                  { from: 4701, to: 5000 },
                  { from: 5001, to: 5300 },
                  { from: 5301, to: 5600 },
                  { greater: 5600 }
                ]);
            scale.colors([
              '#81d4fa',
              '#4fc3f7',
              '#29b6f6',
              '#039be5',
              '#0288d1',
              '#0277bd',
              '#026DAB',
              '#01579b',
              '#025382'
            ]);
            series.colorScale(scale);
            var colorRange = map.colorRange();
            colorRange.enabled(true);
            // set the container
            map.container('container');
            map.draw();
      });
}

init();
