const add_url = document.getElementById('item-form').action

function OpenAddItem(id) {
    document.getElementById('id_catogary').value = id;
    document.getElementById('id_name').value = "";
    document.getElementById('id_food_image').value = '';
    document.getElementById('id_price').value = "";
    document.getElementById('id_description').value = "";
    
    document.getElementById('item-form').action = add_url;

}

function EditItem(id, button, food_id) {
    document.getElementById('item-form').action = `${add_url}/${food_id}`
    document.getElementById('id_catogary').value = id;
    div = button.parentElement.parentElement.parentElement;
    food_type = div.getElementsByClassName('food-type')[0].classList.value;
    food_name = div.getElementsByClassName('food-name')[0].innerText
    food_price = div.getElementsByClassName('food-price')[0].innerText;
    food_description = div.getElementsByClassName('food-description')[0].innerText;

    food_type = food_type.replaceAll('-icon food-type', '')
    console.log(food_type)

    document.getElementById('id_food_type').value = food_type;
    document.getElementById('id_name').value = food_name
    document.getElementById('id_price').value = food_price;
    document.getElementById('id_description').value = food_description;
    

}

function DeleteItem(id) {
    document.getElementById('deleted-item-id').value = id;
    $("#deleteItem").modal('show');
}