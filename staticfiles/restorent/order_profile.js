function showTax() {
    order_area = document.getElementById('order-items');

    sub_amount = parseFloat(document.getElementById('sub-amount').innerText);

    all_taxes = order_area.querySelectorAll('.tax-perscantage');

    grand_sum = 0
    grand_sum += sub_amount;

    tax_amounts = order_area.querySelectorAll('.tax-amount')
    for (let i = 0; i < all_taxes.length; i++) {

        tax_perscantage = parseFloat(all_taxes[i].innerText)

        tax_amount = sub_amount * (tax_perscantage / 100)

        tax_amounts[i].innerText = tax_amount
        grand_sum += tax_amount
    }

    grand_sum = grand_sum.toFixed(2)
    amount_titles = document.querySelectorAll('.amount-with-tax')

    amount_titles.forEach(element => {
        element.innerText = grand_sum;
    });

    document.getElementById('bill_amount').value = parseFloat(grand_sum);

    adjusted_amount = parseInt(JSON.parse(document.getElementById('adjustment-amount').innerText));

    panding_amount = parseFloat(grand_sum) + adjusted_amount

    panding_amount_span = document.getElementById('panding-amount')

    panding_amount_span.innerText = panding_amount.toFixed(2);

    document.getElementById('id_adjustment').value = adjusted_amount;
}


showTax();

paid_amount = document.getElementById('id_paid_amount');
adjustment = document.getElementById('id_adjustment');

let new_adjustment_value = parseFloat(document.getElementById('id_adjustment').value);
let bill_amount = parseFloat(document.getElementById('bill_amount').value);
new_amount = bill_amount + new_adjustment_value;
new_amount = new_amount.toFixed(2)
new_amount = parseFloat(new_amount)
console.log(new_amount)
paid_amount.value = new_amount;

adjustment.addEventListener('change', (e) => {
    new_adjustment_value = parseFloat(e.target.value);
    let bill_amount = parseFloat(document.getElementById('bill_amount').value);
    new_amount = bill_amount + new_adjustment_value;
    new_amount = new_amount.toFixed(2)
    new_amount = parseFloat(new_amount)
    console.log(new_amount)
    paid_amount.value = new_amount
})

async function getRequest(url) {
    console.log(url);
    return fetch(url)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            return data;
        })
        .catch(function (error) {
            console.error('Error:', error);
            throw new Error('Failed to fetch data');
        });
}

const order_id = document.getElementById('order-id').innerText



document.getElementById('food-delivery-pending').addEventListener('click', () => {
    let url = `/update_order_status/${order_id}/false`;
    getRequest(url);
    document.getElementById('delivery-status').innerHTML = '<i class="fa fas fa-clock text-danger mb-0 me-1"></i>Delivery Pending';
})

document.getElementById('food-delivery-done').addEventListener('click', () => {
    let url = `/update_order_status/${order_id}/true`;
    getRequest(url);
    document.getElementById('delivery-status').innerHTML = '<i class="fa fas fa-check-circle text-success mb-0 me-1"></i>Delivery Done';
})

function printKot() {
    window.open(`/kot/${order_id}`, "", "width=600, height=600")
}

function printBill() {
    window.open(`/bill/${order_id}`, "", "width=600, height=600")
}
