// The url with data
const category_url = "http://127.0.0.1:5000/api/v1.0/categories"
const treemap_url = "http://127.0.0.1:5000/api/v1.0/<category_name>/treemap"
const bubble_url = "http://127.0.0.1:5000/api/v1.0/<category_name>/bubble"
const pie_url = "http://127.0.0.1:5000/api/v1.0/<category_name>/pie"
const bar_url = "http://127.0.0.1:5000/api/v1.0/<category_name>/bar"

// Display the default plots
function init() {

    let dropdownMenu = d3.select("#selDataset");

    // Fetch the JSON data and console log it
    d3.json(category_url).then((data) => {

        // An array of id names
        let names = Object.keys(data);

        // Iterate through the names Array
        names.forEach((name) => {
            // Append each name as an option to the drop down menu
            // This is adding each name to the html file as an option element with value = a name in the names array
            dropdownMenu.append("option").text(name).property("value", name);
        });

        // Assign the first name to name variable
        let name = names[0];

        // Call the functions to make the demographic panel, bar chart, and bubble chart
        demo(name);
        treemap(name);
        bubble(name);
        pie(name);
        bar(name);
    });
}

// Make the summary panel
function demo(selectedValue) {
    // Fetch the JSON data and console log it
    d3.json(category_url).then((data) => {

        // An array of metadata objects
        let metadata = data[selectedValue];
        
        // Clear the child elements in div with id sample-metadata
        d3.select("#sample-metadata").html("");
  
        // Object.entries() is a built-in method in JavaScript 
        // This returns an array of a given object's own enumerable property [key, value]
        let entries = Object.entries(metadata);
        
        // Iterate through the entries array
        // Add a h5 child element for each key-value pair to the div with id sample-metadata
        entries.forEach(([key,value]) => {
            d3.select("#sample-metadata").append("h5").text(`${key}: ${value}`);
        });
    });
  }

function treemap(selectedValue){
    let url = ''
    d3.select("#treemap").html("");
    // Fetch the JSON data and console log it
    url = treemap_url.replace('<category_name>', selectedValue)
    d3.json(url).then((results) => {
        var data = anychart.data.tree([results]);

        // Creates Tree map.
        var chart = anychart.treeMap(data);

        // set the maximum depth of levels shown
        chart.maxDepth(2);

        // set the depth of hints
        chart.hintDepth(1);

        // set the opacity of hints
        chart.hintOpacity(0.7);

        // enable HTML for labels
        chart.labels().useHtml(true);

        // configure labels
        chart.labels().format(function() {
          return "<span style='font-weight:bold'>" + this.name +
                 "</span><br>$" + this.value;
        });

        // configure tooltips
        chart.tooltip().format(function() {
          return "Total Sale Amount: $" + this.value;
        });
        chart.title('Total Sales Amount for Category - ' + selectedValue + ' and Items under each category');
        chart.container('treemap');
        chart.draw();
    });
}


// Make the bubble chart
function bubble(selectedValue) {
    let url = ''
    d3.select("#bubble").html("");

    // Fetch the JSON data and console log it
    url = bubble_url.replace('<category_name>', selectedValue)
    d3.json(url).then((results) => {
        // create a categorized chart
        chart = anychart.cartesian();


        // add a marker series
        if (selectedValue === 'All'){
            for (const [key, value] of Object.entries(results)) {
                series = chart.bubble(value);
                series.tooltip().format("Category: " + key + " \nSales: ${%value}");
            }
        }
        else {
            series = chart.bubble(results)
            series.tooltip().format("Category: " + selectedValue + " \nSales: ${%value}");
        }

        // set chart title
        chart.title("Total Sales By Season for Category - " + selectedValue);

        // set axes titles
        chart.xAxis().title("Seasons");
        chart.yAxis().title("Total Sale Amount, $");

        // draw
        chart.minBubbleSize("3%");
        chart.maxBubbleSize("10%");
        chart.container("bubble");
        chart.draw();
    });
}

function pie(selectedValue){
    let url = ''
    d3.select("#pie").html("");
    // Fetch the JSON data and console log it
    url = pie_url.replace('<category_name>', selectedValue)
    d3.json(url).then((data) => {
        // create a chart and set the data
        chart = anychart.pie(data);

        // set chart title
        chart.title("Payment Type Used for Category - " + selectedValue);

        // set the container id
        chart.container("pie");

        // initiate drawing the chart
        chart.draw();
    });
}

// Make the bar chart
function bar(selectedValue) {
    let url = ''
    d3.select("#bar").html("");

    // Fetch the JSON data and console log it
    url = bar_url.replace('<category_name>', selectedValue)
    d3.json(url).then((results) => {
        // create a categorized chart
        chart = anychart.bar();


        // add a marker series
        if (selectedValue === 'All'){
            for (const [key, value] of Object.entries(results)) {
                series = chart.bar(value);
                series.tooltip().format("Category: " + key + " \nSales: ${%value}");
            }
        }
        else {
            series = chart.bar(results)
            series.tooltip().format("Category: " + selectedValue + " \nSales: ${%value}");
        }

        // set chart title
        chart.title("Total Sales By Age Group for Category - " + selectedValue);

        // set axes titles
        chart.xAxis().title("Age Group");
        chart.yAxis().title("Total Sale Amount, $");

        // draw
        chart.container("bar");
        chart.draw();
    });
}

// Toggle to new plots when option changed
function optionChanged(selectedValue) {
    demo(selectedValue);
    treemap(selectedValue);
    bubble(selectedValue);
    pie(selectedValue);
    bar(selectedValue);
}

init();

