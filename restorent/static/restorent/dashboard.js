// Global variable to store the chart instance
let orderComparisonChart;

// Function to create or update the chart
function createOrUpdateChart(newData) {
    // If the chart already exists, update it
    if (orderComparisonChart) {
        // Update the chart's data
        orderComparisonChart.data.datasets[0].data = [newData.table_orders, newData.Delivery_order];
        orderComparisonChart.update(); // Update the chart to reflect changes
    } else {
        // Create the chart for the first time
        const ctx1 = document.getElementById('orderComparisonChart').getContext('2d');
        orderComparisonChart = new Chart(ctx1, {
            type: 'pie', // Pie chart type
            data: {
                labels: ['Table Orders', 'Delivery Orders'],
                datasets: [{
                    data: [newData.table_orders, newData.Delivery_order],
                    backgroundColor: ['rgba(254, 175, 57, 0.6)', 'rgba(44, 64, 110, 0.8)'], // Colors for each section
                    hoverOffset: 4 // Space when hovering over the segments
                }]
            },
            options: {
                responsive: true, // Ensures the chart is responsive
                plugins: {
                    legend: {
                        position: 'top', // Position of the legend
                    },
                    title: {
                        display: false,
                        text: 'Comparison of Table Orders and Delivery Orders' // Chart title
                    }
                }
            }
        });
    }
}


// create all years in dropdown
let year_dropdown = document.getElementById('year-dropdown');
let running_year = document.getElementById('running-year').innerText;
let drop_down_html = ''
for (let i = 0; i < 6; i++) {
    drop_down_html += `
    <a id="year-${running_year}" onclick="ShowRevenueChart(${running_year})" class="dropdown-item">${running_year}</a>
    `
    running_year -= 1;
}
year_dropdown.innerHTML = drop_down_html;

document.getElementById(`year-${document.getElementById('running-year').innerText}`).classList.add('active')


// function which change the graph and get data into the graph
let revenueChart

function createRevenueChart(data) {
    let monthlyRevenue = Object.values(data);
    let labels = Object.keys(data);

    console.log(monthlyRevenue)
    console.log(labels)

    if (revenueChart) {
        // Update the chart's data
        revenueChart.data.datasets[0].data = monthlyRevenue;
        revenueChart.data.labels = labels
        revenueChart.update(); // Update the chart to reflect changes
    }
    else {
        // Getting the canvas element
        const ctx = document.getElementById('revenueChart').getContext('2d');

        // Creating the chart
        revenueChart = new Chart(ctx, {
            type: 'bar', // Bar chart type
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total Revenue (₹)',
                    data: monthlyRevenue,
                    backgroundColor: 'rgb(254, 175, 57, 0.6)', // Bar color
                    borderColor: '#feaf39', // Border color
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true, // Ensures y-axis starts at 0
                        grid: {
                            display: false // Removes y-axis grid lines
                        }
                    },
                    x: {
                        grid: {
                            display: false // Removes x-axis grid lines
                        }
                    }
                },
                plugins: {
                    title: {
                        display: false,
                        text: 'Total Revenue for the Year'
                    }
                }
            }
        });
        // revenue chart end
    }
}

async function ShowRevenueChart(year) {
    let url = `/api/get_yearly_revenue/${year}`
    let data = await getRequest(url)
    createRevenueChart(data)

    all_active_tags = year_dropdown.getElementsByClassName('dropdown-item')
    for (let i = 0; i < all_active_tags.length; i++) {
        let tag = all_active_tags[i]
        if (tag.innerText == String(year)) {
            console.log(tag)
            tag.setAttribute('class', 'dropdown-item active');
        }
        else {
            tag.setAttribute('class', 'dropdown-item');
        }

    }


    document.getElementById('running-year').innerText = year
}

ShowRevenueChart(document.getElementById('running-year').innerText)


// function to get data using get request
async function getRequest(url) {
    console.log(url);
    return fetch(url)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {

            return data;

        })
        .catch(function (error) {
            console.error('Error:', error);
            throw new Error('Failed to fetch data');
        });
}
// getting the data using api
const api_url = '/api/dashboard_data'

async function get_all_data() {
    const date = document.getElementById('daterange').value
    const complete_url = `${api_url}?daterange=${date}`
    all_data = await getRequest(complete_url)

    document.getElementById('table-orders').innerText = all_data.table_orders;
    document.getElementById('delivery-orders').innerText = all_data.Delivery_order;
    document.getElementById('total-payment').innerText = all_data['Total Payment']
    document.getElementById('vacent-table').innerText = all_data['Vacant Table']

    createOrUpdateChart({ table_orders: all_data.table_orders, Delivery_order: all_data.Delivery_order });
    return all_data

}
all_data = get_all_data()

document.getElementById('submit-button').addEventListener('click', async (e) => {
    await get_all_data()
})

// addign the payment socket



// adding the table socket
