// getting the restorent id
const restorent_id = document.getElementById('restorent_id').innerText


// adding the new websockit which tell whether it is connected with phone pay or not

// software websockit
const software_socket = new WebSocket(`ws://${window.location.host}/ws/software_socket/`)

software_socket.onopen = () => {
    console.log('websockit connection is estblished for software socket')
    software_socket.send(JSON.stringify(
        {
            'user_id': '0',
            'action': ''
        }
    ))
};

software_socket.onmessage = (event) => {
    const data = JSON.parse(event.data)
    all_users = data.all_users
    console.log(all_users)
    console.log(restorent_id)
    if (all_users.includes(restorent_id)) {
        let btn = document.getElementById('software-connocter');
        btn.className = "btn btn-success";
        btn.innerHTML = '<i class="fa fa-circle me-2" aria-hidden="true"></i>UPI Connected'
    }
    else {
        let btn = document.getElementById('software-connocter');
        btn.className = "btn btn-danger";
        btn.innerHTML = '<span class="spinner-grow spinner-grow-sm me-2" role="status" aria-hidden="true"></span> UPI Disconnected'


    }
}

software_socket.onclose = () => {
    console.log('sockit connection is going to disconnect')
}

software_socket.onerror = (error) => {
    console.log('Error in Websockit', error)
}

