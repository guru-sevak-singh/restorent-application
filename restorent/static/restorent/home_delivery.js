userdetail = localStorage.getItem('user_information');

if (userdetail == null) {
    userdetail = {}
}
else {
    // showing the user information on the form
    userdetail = JSON.parse(userdetail);
    let nameInput = document.getElementById('name');
    nameInput.value = userdetail.name;
    nameInput.setAttribute('class', 'form-control is-valid');

    let phoneInput = document.getElementById('phone-number');
    phoneInput.value = userdetail.phone_number;
    phoneInput.setAttribute('class', 'form-control is-valid');

    let addressInput = document.getElementById('address');
    addressInput.value = userdetail.address;
    addressInput.setAttribute('class', 'form-control is-valid')
}

window.onload = function () {
    setTimeout(() => {
        $("#detailBox").modal('show');
    }, 1000); // 2000 milisecond means 1 second
};

function submitForm() {
    invalids = document.getElementsByClassName('is-valid');
    if (invalids.length == 3) {
        // save the data in local storage
        userdetail.name = document.getElementById('name').value;
        userdetail.phone_number = document.getElementById('phone-number').value;
        userdetail.address = document.getElementById('address').value;
        localStorage.setItem("user_information", JSON.stringify(userdetail));
        $("#detailBox").modal('hide');
    }

}

let nameInput = document.getElementById('name');
nameInput.addEventListener('change', (e) => {
    let user_name = e.target.value;
    user_name = user_name.replaceAll(" ", "");
    if (user_name == "") {
        nameInput.setAttribute('class', 'form-control is-invalid');
    }
    else {
        nameInput.setAttribute('class', 'form-control is-valid');
    }
})

let phoneInput = document.getElementById('phone-number');
phoneInput.addEventListener('change', (e) => {
    let phone_number = e.target.value;
    console.log(phone_number);

    if (phone_number.includes(' ') || phone_number.length != 10) {
        phoneInput.setAttribute('class', 'form-control is-invalid')
    }

    else {
        phoneInput.setAttribute('class', 'form-control is-valid')
    }
})

let addressInput = document.getElementById('address');
addressInput.addEventListener('change', (e) => {
    let address = e.target.value;
    address = address.replaceAll(" ", "");
    address = address.replaceAll("\n", "");
    console.log(address)
    if (address == "") {
        addressInput.setAttribute('class', 'form-control is-invalid');
    }
    else {
        addressInput.setAttribute('class', 'form-control is-valid');
    }
})