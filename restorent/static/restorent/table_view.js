// creating web socket url
const websoclet_url = `ws://${window.location.host}/ws/dashboard_data/`

// creating socket
const socket = new WebSocket(websoclet_url)

// function which show any data come from socket
socket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    UpdateNewData(data.dashboard_data)
    playAudio()
}

// function run on closing of socket
socket.onclose = (e) => {
    console.error('socket is disconnected');
}

// function to send data to socket
function ChangeStatus() {
    let status = document.getElementById('vacent_status').value;
    const data = {
        'pk': SelectedTableId,
        'status': status,
        'action': 'update_table_status'
    }    
    
    console.log('going to send the socket request...');
    socket.send(JSON.stringify(data))
}


var SelectedTableId = ''

const UpdateStatusUrl = `/update_table_status/`

// having a Selected Id to send data to socket
function ChangeUrl(pk) {
    SelectedTableId = pk;
    $("#changeTableStatus").modal('show');
}

// function which show the updated data on the UI/UX
function UpdateNewData(data) {
    console.log(data)
    let table_pk = data.pk;


    let table = document.getElementById(`table-id-${table_pk}`);
    if (table == null) {
        if (data.restorent_id == restorent_id) {
            // check if delivery floor there or not
            let delivery_floor = document.getElementById('Delivery')
            if (delivery_floor == null) {
                // create a delivery floor
                let new_html = `<div class="row g-4 mt-2" id="Delivery">
                    <h4>
                    Delivery
                    </h4>
                </div>`
                document.getElementById('tableContainer').innerHTML += new_html;
            }
            delivery_floor = document.getElementById('Delivery')
            let new_html = `
                <div class="col-lg-3 col-sm-6 wow fadeInUp" data-wow-delay="0.1s" id="table-id-${data.pk}">
                    <div class="service-item rounded">
                        <div class="table-status busy cursor-pointer" onclick="ChangeUrl('${data.pk}')">
                            Busy
                        </div>
                        <div class="p-3">
                            <a href="#" id="/order_profile/${data.pk}">
                                <h5 class="mb-3">${data.table_name}</h5>
                                <div class="order-list">
                                    <p class="order-status mb-2">
                                        <i class="fa fas fa-utensils text-primary mb-0 me-3"></i> Preparing Order
                                    </p>
                                    <p class="order-status">
                                        <i class="fa fas fa-clock text-danger mb-0 me-3"></i> Payment Pending
                                    </p>
                                </div>
                            </a>
                        </div>
                    </div>
                </div>
            `
            delivery_floor.innerHTML += new_html

        }
    }

    let cursorPointer = table.getElementsByClassName('cursor-pointer')[0];

    let order_list = table.getElementsByClassName('order-list')[0];

    let order_html = '';

    if (data.table_vacent_status == true) {

        cursorPointer.innerText = 'Busy';
        if (cursorPointer.classList.contains('bg-success')) {
            cursorPointer.classList.remove('bg-success')
        }
        cursorPointer.classList.add('busy');

        if (data.order_panding == true) {
            order_html += `
            <p class="order-status mb-2">
                <i class="fa fas fa-utensils text-primary mb-0 me-3"></i>Preparing Order
            </p>
            `
        }
        else {
            order_html += `
            <p class="order-status mb-2">
                <i class="fa fa-check-circle text-success"></i>Order Served
            </p>
            `
        }

        if (data.payment_panding == true) {
            order_html += `
            <p class="order-status">
            <i class="fa fas fa-clock text-danger mb-0 me-3"></i>
            Payment Pending
            </p>
            `
        }

        else {
            order_html += `
            <p class='order-status'>
            <i class="fa fa-check-circle text-success" aria-hidden="true"></i>
            Payment Done
            </p>
            `
        }
    }

    else {
        cursorPointer.innerText = 'Free';

        if (cursorPointer.classList.contains('busy')) {
            cursorPointer.classList.remove('busy')
        }
        cursorPointer.classList.add('bg-success');

        order_html = `
        <p class="order-status mb-2">
            <i class="fa fa-cart-plus text-primary mb-0 me-3"></i>Generate Order
        </p>
        `
    }

    try {
        let alert_message = data.alert_message
        if (alert_message) {
            alert(alert_message)
        }
    }
    catch (error) {
        console.log(error)
    }
    order_list.innerHTML = order_html;
}

// // Function to Play Notification Sound
function playAudio() {
    const audio = new Audio('/static/sound/notification.wav');
    audio.play().catch(error => {
        console.error('Error in Playing audio', error)
    })
}

function removeTable(complete_table_name) {
    localStorage.removeItem(complete_table_name);
}


// Define the Queue class
class Queue {
    constructor() {
        this.items = [];
    }

    enqueue(element) {
        this.items.push(element);
    }

    dequeue() {
        if (this.isEmpty()) {
            return undefined;
        }
        return this.items.shift();
    }

    isEmpty() {
        return this.items.length === 0;
    }
}

// Initialize a queue instance
var queue = new Queue();

// Function to play audio notifications from the queue
setInterval(function () {
    var audio = queue.dequeue();
    if (audio !== undefined) {
        audio.play().catch(function (error) {
            console.error("Audio play failed:", error);
        });

        // Remove the audio element after playback
        setTimeout(function () {
            audio.remove();
        }, 1000); // Duration of sound clip (adjust as necessary)
    }
}, 300); // Check the queue every 300ms

// Example usage: Call playAudio() to add audio to the queue
playAudio(); // Call this whenever you want to play a notification sound
