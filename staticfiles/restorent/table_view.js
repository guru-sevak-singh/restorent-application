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
    let table_pk = data.pk;
    let table = document.getElementById(`table-id-${table_pk}`);

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
                <i class="fa fas fa-utensils text-primary mb-0 me-3"></i>Order Served
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

    order_list.innerHTML = order_html;   
}

// Function to Play Notification Sound
function playAudio(){
    const audio = new Audio('/static/sound/notification.wav');
    audio.play().catch(error =>{
        console.error('Error in Playing audio', error)
    })
}