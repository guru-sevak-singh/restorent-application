// creating websocket socket url
const websocket_url = `ws://${window.location.host}/ws/payment_data/`

// creating socket
const socket = new WebSocket(websocket_url)

// socket check if any data come from socket or not
socket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    console.log(data)
}

socket.onclose = (e) => {
    console.error('socket is disconnected');
}

