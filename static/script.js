function updateSensorData() {
    fetch('/api/Sensors-data')
        .then(response => response.json())
        .then(data => {
            for (const Sensors in data) {
                document.getElementById(`${Sensors}_temp`).innerText = data[Sensors].temp;
            }
        });
}

// Simulate live updates (In real scenarios, fetch data via WebSocket or AJAX)
setInterval(() => {
    let newTemperature = {
        timestamp: new Date().toLocaleTimeString(),
        temperature: Math.random() * 40  // Simulated temperature data
    };
    updateChart(newTemperature);
}, 5000);  // Update every 5 seconds



// Update Sensors data every 5 seconds
setInterval(updateSensorData, 4000);

// Fetch initial Sensors data when the page loads
updateSensorData();
