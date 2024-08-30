function OpenAddAreaPopUp() {
    document.getElementById('exampleModalLabel').innerText = 'Add Area'
    document.getElementById('work-message').innerText = ' to Add';
    document.getElementById('area_name').value = "";
    document.getElementById('area_name').parentElement.style.display = 'block';

    document.getElementById('no_of_tables').value = "";
    document.getElementById('remove-submit').style.display = 'none';
    document.getElementById('add-submit').style.display = 'block';
    
    $("#sittingAreaName").modal('show');
}


function removeTable(area_id, area_name) {
    document.getElementById('area_name').value = area_id;
    document.getElementById('area_name').parentElement.style.display = 'none';
    document.getElementById('exampleModalLabel').innerText = 'Remove Tables';
    document.getElementById('work-message').innerText = ' to remove from:-' + area_name;
    
    document.getElementById('remove-submit').style.display = 'block';
    document.getElementById('add-submit').style.display = 'none';
    $("#sittingAreaName").modal('show');
}