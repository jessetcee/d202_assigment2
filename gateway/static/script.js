function updateSensorData() {
    fetch('/api/Sensors-data')
        .then(response => response.json())
        .then(data => {
            for (const Sensors in data) {
                document.getElementById(`${Sensors}_temp`).innerText = data[Sensors].temp;
            }
        });
}

// Update Sensors data every 5 seconds
setInterval(updateSensorData, 4000);

// Fetch initial Sensors data when the page loads
updateSensorData();
