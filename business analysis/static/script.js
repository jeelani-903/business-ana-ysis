// Function to create a Plotly plot
function createPlot(divId, data) {
    Plotly.newPlot(divId, data);
}

// Function to create a scatter plot with annotations and hover text
function createScatterPlot(divId, data) {
    var scatterData = [{
        x: data.x,
        y: data.y,
        mode: 'markers+text',  // Display markers and text annotations
        type: 'scatter',
        text: data.text,  // Display company names as annotations
        marker: {
            size: 10,  // Adjust marker size as needed
        },
        hoverinfo: 'text+x+y', // Display text, x, and y values on hover
    }];

    var layout = {
        title: 'Overall Performance by City (Scatter Plot with Annotations)',
        xaxis: {
            title: 'City',
        },
        yaxis: {
            title: 'Total Sales',
        },
    };

    Plotly.newPlot(divId, scatterData, layout);
}

// Function to create a line graph
function createLineGraph(divId, data) {
    var lineData = [{
        x: data.x,
        y: data.y,
        mode: 'lines+markers',  // Display lines and markers
        type: 'scatter',
        marker: {
            size: 6,  // Adjust marker size as needed
        },
    }];

    var layout = {
        title: 'Total Sales by Year (Line Graph)',
        xaxis: {
            title: 'Year',
        },
        yaxis: {
            title: 'Total Sales',
        },
    };

    Plotly.newPlot(divId, lineData, layout);
}

// Function to fetch data and create the scatter plot
function createScatterPlotWithData() {
    // Fetch data for the scatter plot
    fetch('/scatter_data')
        .then(response => response.json())
        .then(data => {
            console.log('Fetched scatter plot data:', data);

            // Create the scatter plot with annotations
            createScatterPlot('scatter_plot', data);
            console.log('Created scatter plot with annotations.');
        })
        .catch(error => console.error('Error:', error));
}

// Function to fetch data and create the line graph for total sales by year
function createLineGraphWithData() {
    // Fetch data for the line graph
    fetch('/sales_by_year_data')
        .then(response => response.json())
        .then(data => {
            console.log('Fetched sales by year data:', data);

            // Convert data to appropriate types
            data.x = data.x.map(String); // Convert year values to strings

            // Create the line graph for total sales by year
            createLineGraph('sales_by_year', data);
            console.log('Created line graph for total sales by year.');
        })
        .catch(error => console.error('Error:', error));
}

// Function to update individual company performance based on selected years
function updateIndividualCompanyPerformance() {
    console.log('Updating individual company performance...');
    var selectedCompany = document.getElementById('company_dropdown').value;
    var selectedStartYear = document.getElementById('start_year').value;
    var selectedEndYear = document.getElementById('end_year').value;

    try {
        // Fetch data for the selected company and year range from the server
        fetch(`/get_history?company=${selectedCompany}&start_year=${selectedStartYear}&end_year=${selectedEndYear}`)
            .then(response => response.json())
            .then(data => {
                console.log('Fetched data:', data);

                // Create the updated individual performance graph
                createPlot('individual_company', JSON.parse(data.history_data));
                console.log('Updated individual company performance graph.');
            })
            .catch(error => console.error('Error:', error));
    } catch (error) {
        console.error('Error occurred while updating individual company performance:', error);
    }
}

// Function to update the total sales graph based on selected years
function updateTotalSalesGraph() {
    console.log('Updating total sales graph...');
    var selectedStartYear = document.getElementById('total_sales_start_year').value;
    var selectedEndYear = document.getElementById('total_sales_end_year').value;

    try {
        // Fetch data for the selected year range from the server
        fetch(`/sales_by_year_data?start_year=${selectedStartYear}&end_year=${selectedEndYear}`)
            .then(response => response.json())
            .then(data => {
                console.log('Fetched sales data:', data);

                // Create the updated total sales graph
                createLineGraph('sales_by_year', data);
                console.log('Updated total sales graph.');
            })
            .catch(error => console.error('Error:', error));
    } catch (error) {
        console.error('Error occurred while updating total sales graph:', error);
    }
}

// Call the functions to create the initial plots when the document is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    createScatterPlotWithData();
    createLineGraphWithData();  // Call this to initially load the line graph
    updateIndividualCompanyPerformance(); // Call this to initially load individual performance
});
