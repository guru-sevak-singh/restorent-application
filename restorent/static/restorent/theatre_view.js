// menue url
const menue_url = '/show_menue/'

// creating web socket url
const websoclet_url = `ws://${window.location.host}/ws/dashboard_data/`

// creating socket
const socket = new WebSocket(websoclet_url)

function ShowCountStatus(){
    let all_seats = document.getElementsByClassName('seat').length;

    let orders = document.getElementsByClassName('orderreceived').length;
    document.getElementById('order-seat').innerText = String(orders - 1);
    let payments = document.getElementsByClassName('paymentreceived').length;
    document.getElementById('paymentreceived-seat').innerText = String(payments - 1)

    document.getElementById('available-seat').innerText = String(all_seats - orders - payments - 1)
}

// Function which show any data come from socekt
socket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    UpdateNewData(data.dashboard_data)
    playAudio();
    console.log(data);
}

// function run on close of socket
socket.onclose = (e) => {
    console.error('socket is disconected');
}

// function to send data to socket
function ChangeStatus(button) {
    let status = button.innerText
    if (status == 'Free'){
        status = 'free';
    }
    const data = {
        'pk': SelectedTableId,
        'status': status,
        'action': 'update_table_status'
    }

    // going data to socket
    socket.send(JSON.stringify(data))
}

var SelectedTableId = ""

// having a Selected Id to send data to socket
function ChangeUrl(pk, div) {
    SelectedTableId = pk;
    let btn = document.getElementById('table-status')
    let status = ""
    if (div.getAttribute('class') == 'seat'){
        status = "Bussy"
        btn.setAttribute('class', 'btn btn-danger')

    }
    else{
        status = "free"
        btn.setAttribute('class', 'btn btn-success')
    }
    btn.innerText = status;
    document.getElementById('url-button').setAttribute('href', `${menue_url}${pk}`)
    let table_name = div.innerText;
    document.getElementById('table-name').innerText = table_name;
    $("#changeTableStatus").modal('show');
}

function playAudio() {
    const audio = new Audio('/static/sound/notification.wav');
    audio.play().catch(error => {
        console.error('Error in Playing audio', error)
    })
}

function UpdateNewData(data) {
    let table_pk = data.pk;

    let table = document.getElementById(`table-id-${table_pk}`);
    if (table == null) {
        // not to do anything
        console.log('pass')
    }

    if (data.table_vacent_status == true) {
        table.setAttribute('class', 'seat orderreceived');

        if (data.payment_panding == false) {
            table.setAttribute('class', 'seat paymentreceived')
        }
    }
    else {
        table.setAttribute('class', 'seat');
    }

    try{
        let alert_message = data.alert_message
        if (alert_message) {
            alert(alert_message);
        }
    }
    catch(error){
        console.log(error)
    }

    ShowCountStatus()
}

ShowCountStatus()