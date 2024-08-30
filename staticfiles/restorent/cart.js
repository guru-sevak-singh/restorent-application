const table_name = document.getElementById('table-name').innerText;

function setCartItems() {
    // get data of this table
    cart = localStorage.getItem(table_name)
    cart = JSON.parse(cart)

    for (let i in cart) {
        cart_item = cart[i]
        item_name = cart_item.name;
        item_type = cart_item.item_type;
        item_price = cart_item.item_price;
        item_description = cart_item.item_description;
        item_quantity = cart_item.quantity;
        createItemCart(item_name, item_type, item_price, item_quantity, item_description, i);
    }

    getCartAmount(cart)
}

function createItemCart(item_name, item_type, item_price, item_quantity, item_description, item_id) {
    cart_box = document.getElementById('cart-items');
    old_html = cart_box.innerHTML;
    new_item_card = `
                    <div class="col-lg-6 col-md-6 col-12 mb-4">
                        <div class="cart-item">
                            <h1 class='item-id' style="display:none;">${item_id}</h1>
                            <div class="row">
                                <div class="col-lg-8 col-md-6 col-9">
                                    <h6 class="d-flex align-items-center">
                                        <span class="${item_type}-icon"></span>
                                        <span class="ms-2">${item_name}</span>
                                    </h6>
                                </div>
                                <div class="col-lg-4 col-md-6 col-3 text-end">
                                    <h6 class="price"><span class="me-1-cust">₹</span>${item_price}</h6>
                                </div>
                            </div>

                            <p class="text-muted small">${item_description}</p>
                            <div class="row align-items-center g-3">
                                <div class="col-lg-6 col-md-6 col-12">
                                    <div class="quantity">
                                        <button class="btn btn-primary" onclick="DecreseQuantity(this)">-</button>
                                        <input type="text" class="quantity-box" value="${item_quantity}" readonly>
                                        <button class="btn btn-primary" onclick="IncreseQuantity(this)">+</button>
                                    </div>
                                </div>
                                <div class="col-lg-6 col-md-6 col-12 text-md-end text-lg-end text-start">
                                    <a class="dismiss-icon text-primary text-end remove-link" onclick="removeItem(this)">
                                        <i class="fas fa-times me-1"></i>
                                        Remove Item
                                    </a>
                                </div>
                            </div>

                        </div>
                    </div>
    `
    old_html += new_item_card
    cart_box.innerHTML = old_html;

}

function IncreseQuantity(button) {
    // getting the parent div
    let parentDiv = button.parentElement.parentElement.parentElement.parentElement;

    // getting the item id
    let item_id = parentDiv.getElementsByClassName('item-id')[0].innerText;

    // getting the cart data
    cart_data = localStorage.getItem(table_name);
    cart_data = JSON.parse(cart_data);

    // getting the Exact Item
    let item = cart_data[item_id];

    // getting teh quantity
    let quantity = item.quantity;

    // Increse The Quantity
    quantity += 1;

    // update in cart
    cart_data[item_id].quantity = quantity;

    // Show The New Quantity
    parentDiv.getElementsByClassName('quantity-box')[0].value = quantity;
    getCartAmount(cart_data);

    // make data to store
    cart_data = JSON.stringify(cart_data);

    // update_data in local storage
    localStorage.setItem(table_name, cart_data);

}

function DecreseQuantity(button) {
    // getting the parent div
    let parentDiv = button.parentElement.parentElement.parentElement.parentElement;

    // getting the item id
    let item_id = parentDiv.getElementsByClassName('item-id')[0].innerText;

    // getting the cart data
    cart_data = localStorage.getItem(table_name);
    cart_data = JSON.parse(cart_data);

    // getting the Exact Item
    let item = cart_data[item_id];

    // getting teh quantity
    let quantity = item.quantity;

    // Decrease The Quantity
    quantity -= 1;

    // Check if quantity equal to 0
    if (quantity == 0) {
        let removeLink = parentDiv.getElementsByClassName('remove-link')[0];
        removeLink.click();
    }

    else {

        // update in cart
        cart_data[item_id].quantity = quantity;

        // Show The New Quantity
        parentDiv.getElementsByClassName('quantity-box')[0].value = quantity;
        getCartAmount(cart_data);

        // make data to store
        cart_data = JSON.stringify(cart_data);

        // update_data in local storage
        localStorage.setItem(table_name, cart_data);
    }

}

function removeItem(button) {
    // getting the parentDiv
    parentDiv = button.parentElement.parentElement.parentElement.parentElement;

    // getting the pk
    pk = parentDiv.getElementsByClassName('item-id')[0].innerText;

    // get cart_data from local storage
    cart_data = localStorage.getItem(table_name);

    // convert from json to dictionary
    cart_data = JSON.parse(cart_data);

    // updateing the data for saving
    delete cart_data[pk];

    // update ui
    getCartAmount(cart_data);

    // save in cart data
    cart_data = JSON.stringify(cart_data);
    localStorage.setItem(table_name, cart_data);

    // remove cart ddiv
    parentDiv.remove();

}

setCartItems()


function getCartAmount(cart_data) {

    // cart data get from old data
    let total_amount = 0;
    for (let cart_item in cart_data) {
        item_amount = cart_data[cart_item]['item_price'] * cart_data[cart_item]['quantity'];
        total_amount += item_amount;
    }
    calculateTax(total_amount)
    document.getElementById('cart-amount').innerText = total_amount;

    totalPayBalance();
}

function totalPayBalance() {
    let elements = document.querySelectorAll('.amounts');
    let total_amount = 0;
    elements.forEach(element => {
        number = Number(element.innerText);
        total_amount += number;
    });

    total_amount = total_amount.toFixed(2)
    
    document.getElementById('total-amount').innerText = total_amount;
}

function calculateTax(amount) {
    let all_taxes = document.querySelectorAll('.tax-perscantage');
    let all_tax_amounts = document.querySelectorAll('.tax-amount');

    for (let i = 0; i < all_taxes.length; i++) {
        try {
            let tax_perscantage = parseFloat(all_taxes[i].innerText);
            let tax_amount = amount * (tax_perscantage / 100);
            tax_amount = tax_amount.toFixed(2)
            all_tax_amounts[i].innerText = tax_amount;
        }
        catch (error) {
            console.log(error)
        }
    }
}

function createOrder() {
    let user_detail = document.getElementById('user-detail')
    if (user_detail != null) {
        let user_information = localStorage.getItem('user_information');
        user_detail.value = user_information;
    }

    cart_data = localStorage.getItem(table_name);
    document.getElementById('order_data').value = cart_data;
    // localStorage.removeItem(table_name)
    document.getElementById('order_submit').click()
}