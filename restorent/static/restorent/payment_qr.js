// order-pk
const order_pk = JSON.parse(document.getElementById('order-pk').textContent)
const transaction_id = JSON.parse(document.getElementById('transaction_id').textContent)

console.log(order_pk, transaction_id)

// create websocket url
const websocket_url = `ws://${window.location.host}/ws/payment_data/`

// creating socket
const socket = new WebSocket(websocket_url)

// socket check if any data come from socket and not
socket.onmessage = (e) => {
    const eventData = JSON.parse(e.data);
    const payment_data = JSON.parse(eventData.payment_data)
    console.log(payment_data)

    if (payment_data.work === 'add_new_payment') {
        if (payment_data.order_id == order_pk) {
            window.open('/payment_added_successfully', '_self')
        }
    }

}

socket.onclose = (e) => {
    console.error('socket is closed')
}

// code for timer
// Function to start the countdown
function startCountdown() {

    // Set the time for the countdown (5 minutes = 300 seconds)
    let time = 300;

    const timerElement = document.getElementById('timer');

    const countdown = setInterval(() => {
        let minutes = Math.floor(time / 60);
        let seconds = time % 60;

        // Add leading zeros to the minutes and seconds
        minutes = minutes < 10 ? '0' + minutes : minutes;
        seconds = seconds < 10 ? '0' + seconds : seconds;

        // Display the countdown
        timerElement.textContent = `${minutes}:${seconds}`;

        // Decrease the time
        time--;

        // Check if time is up
        if (time < 0) {
            clearInterval(countdown);
            timerElement.textContent = "Time's Up!";
        }
    }, 1000);
}

// Start the countdown immediately
startCountdown();
