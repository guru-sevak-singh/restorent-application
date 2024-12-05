const table_name = document.getElementById('table-name').innerText;

if (document.getElementById('all-selected-orders') != undefined){
    let all_selected_items = document.getElementById('all-selected-orders').innerText;
    localStorage.setItem(table_name, all_selected_items);
}


let temp = localStorage.getItem(table_name)
if (temp == null) {
    localStorage.setItem(table_name, '{}')
}
else {
    showOldData()
}

function showOldData() {
    let all_items = JSON.parse(temp);
    
    for (let i in all_items) {
        // tet the table id
        let tab_id = `item-id-${i}`
        // get the card
        let card = document.getElementById(tab_id);
        // make the item
        let active_tab = card.getElementsByClassName('menu-item')[0];
        // make the item highlight
        active_tab.classList.add('active');
        // make add box d-none
        card.getElementsByClassName('add-box')[0].classList.add('d-none');
        // remove remove box d-none
        card.getElementsByClassName('remove-box')[0].classList.remove('d-none');
        // set Quantity 1
        card.getElementsByClassName('quantity')[0].innerText = all_items[i]['quantity'];
    }
}

function addToCart(btn) {
    // adding the active class to complet card
    btn.parentElement.parentElement.parentElement.parentElement.classList.add('active')
    // getting the card so we can get the item details
    card = btn.parentElement.parentElement.parentElement.parentElement
    // fetching the details from card
    item_name = card.getElementsByClassName('item-name')[0].innerText;
    item_type = card.getElementsByClassName('item-type')[0].classList.value
    item_type = item_type.replaceAll('-icon item-type', '');
    item_price = card.getElementsByClassName('item-price')[0].innerText;
    item_description = card.getElementsByClassName('item-description')[0].innerText;
    pk = card.getElementsByClassName('item-pk')[0].innerText;
    // creating data to save in local storage
    append_data = {}
    append_data['item_type'] = item_type
    append_data['name'] = item_name;
    append_data['item_price'] = item_price;
    append_data['item_description'] = item_description;
    append_data.quantity = 1;
    // make add box d-none
    card.getElementsByClassName('add-box')[0].classList.add('d-none')
    // remove remove box d-none
    card.getElementsByClassName('remove-box')[0].classList.remove('d-none')
    // set Quantity 1
    card.getElementsByClassName('quantity')[0].innerText = 1
    // getting the data from local storage
    cart_data = localStorage.getItem(table_name)
    // making the data readbale
    cart_data = JSON.parse(cart_data)
    // updating the data
    cart_data[pk] = append_data
    json_data = JSON.stringify(cart_data)
    // saving new data to local storage
    localStorage.setItem(table_name, json_data)
    // updating the cart lenght
    UpdateCart()

}

function IncreseQuantity(btn) {
    // getting the parentDiv
    parentDiv = btn.parentElement.parentElement.parentElement.parentElement.parentElement;

    // getting the pk
    pk = parentDiv.getElementsByClassName('item-pk')[0].innerText;

    // making ui and better experience
    big_box = btn.parentElement;
    quantity_box = big_box.getElementsByClassName('quantity')[0]
    quantity = Number(quantity_box.innerText);

    // increse the quantity
    quantity += 1;
    quantity_box.innerText = quantity;

    // get data from local storage
    cart_data = localStorage.getItem(table_name);

    // convert local data into dictionary
    cart_data = JSON.parse(cart_data);

    // update the data
    cart_data[pk].quantity = quantity;

    // again making data as for saving purpose
    cart_data = JSON.stringify(cart_data)

    // save cart data in local storage
    localStorage.setItem(table_name, cart_data)

    // updating the cart lenght
    UpdateCart()

}

function DecreseQuantity(btn) {

    parentDiv = btn.parentElement.parentElement.parentElement.parentElement.parentElement;

    // getting the pk
    pk = parentDiv.getElementsByClassName('item-pk')[0].innerText;

    // making ui and better experience
    big_box = btn.parentElement;
    quantity_box = big_box.getElementsByClassName('quantity')[0]
    quantity = Number(quantity_box.innerText);

    // increse the quantity
    quantity -= 1;
    if (quantity >= 1) {
        quantity_box.innerText = quantity;

        // get data from local storage
        cart_data = localStorage.getItem(table_name);

        // convert local data into dictionary
        cart_data = JSON.parse(cart_data);

        // update the data
        cart_data[pk].quantity = quantity;

        // again making data as for saving purpose
        cart_data = JSON.stringify(cart_data)

        // save cart data in local storage
        localStorage.setItem(table_name, cart_data)
    }

    else {
        parentDiv.getElementsByClassName('remove-from-cart')[0].click()
    }

    // updating the cart lenght
    UpdateCart()

}

function removeItem(btn) {
    parentDiv = btn.parentElement.parentElement.parentElement.parentElement.parentElement;

    // remove active class
    parentDiv.classList.remove('active');

    // getting the pk
    pk = parentDiv.getElementsByClassName('item-pk')[0].innerText;

    // get cart_data from local storage
    cart_data = localStorage.getItem(table_name);

    // convert from json to dictionary
    cart_data = JSON.parse(cart_data);

    // updateing the data for saving
    delete cart_data[pk];

    // save in cart data
    cart_data = JSON.stringify(cart_data)
    localStorage.setItem(table_name, cart_data)

    // remove remove-box d-none
    parentDiv.getElementsByClassName('remove-box')[0].classList.add('d-none');

    // adding d-none to add-box
    parentDiv.getElementsByClassName('add-box')[0].classList.remove('d-none');

    // updating the cart lenght
    UpdateCart()
}


function UpdateCart() {

    // getting the data of this table
    let cart_data = localStorage.getItem(table_name);
    cart_data = JSON.parse(cart_data);
    let cart_length = Object.keys(cart_data).length;

    if (cart_length == 0) {
        document.getElementById('cart-div').style.display = 'none';
    }
    else {
        document.getElementById('cart-div').style.display = 'block';
    }
    document.getElementById('cart-length').innerText = cart_length;

    getCartAmount(cart_data)
}

UpdateCart()

function getCartAmount(cart_data) {
    // cart data get from old data
    let total_amount = 0;
    for (let cart_item in cart_data) {
        item_amount = cart_data[cart_item]['item_price'] * cart_data[cart_item]['quantity']
        total_amount += item_amount
    }

    document.getElementById('cart-amount').innerText = total_amount
}