


let state = {};
filterState = {
    'category': '',
    'brand': '',
}

// обработчики

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
  };

const submit = (e) => {
    e.preventDefault();
    $(e.target).attr('disabled', 'disabled');
    const sendData = {};
    const inventories = {};
    Object.keys(state).filter((key) => (state[key].added )).forEach((key) => {
        inventories[key] = state[key];
    });
    sendData['inventories'] = inventories;
    //отправим JSON
    $.ajax({
        type: "POST",
        data: {request: $.toJSON(sendData), csrfmiddlewaretoken: getCookie('csrftoken')},
        success: function(res) {
            window.location.href = '/products/inventories';
            
        }
    });
};

const inputHandler = (e) => {
    const id = $(e.target).attr('data-id');
    $input = $(e.target);
    state[String(id)].added = $input.is(':checked');
    //$input.val(state[String(id)].quantity);
    render();
};

const categoryChangeHandler = (e) => {
    filterState.category = e.target.value
    render();
}

const brandChangeHandler = (e) => {
    filterState.brand = e.target.value
    render();
}

const addAllHandler = (e) => {
    e.preventDefault();
    e.data.keys.map((key) => {
        state[String(key)].added = !(state[String(key)].added);
    })
    render();
};
// render

$('<input>', {
           value: 'Сохранить',
           type: 'submit',
           class: 'btn btn-secondary',
           on: {click: submit}
        }).appendTo($('#submit_button'));
const $tabDiv = $('<div>', {class: 'table-responsive'}).appendTo('#main-data')
const $mainTable = $('<table>', {
    class: "table table-striped table-sm",
}).appendTo($tabDiv);
$('#main-data').append($tabDiv);

$categorySelector = $('select[name=category]');
$categorySelector.change(categoryChangeHandler);

$brandSelector = $('select[name=brand]');
$brandSelector.change(brandChangeHandler);

const render = () => {
    $categorySelector.val(filterState.category);
    $brandSelector.val(filterState.brand);
    $mainTable.empty();
    $('<thead><tr><th>Товар</th><th><a href="#" id="add_all"> Добавить </a></th></tr></thead>').appendTo($mainTable);
    const $tbody = $('<tbody>', {class: 'table-striped'}).appendTo($mainTable);
    let keysToShow = Object.keys(state)
    if (filterState.category) {
        keysToShow = keysToShow.filter((key) => state[key].category === Number(filterState.category))
    }
    if (filterState.brand) {
        keysToShow = keysToShow.filter((key) => state[key].brand === Number(filterState.brand))
    }
    $('#add_all').on('click', {keys: keysToShow}, addAllHandler);
    keysToShow.forEach((key) => {
        const $tr = $('<tr>').appendTo($tbody);
        const $tdName = $(`<td>${state[key].name}</td>`).appendTo($tr);
        const $tdControler = $('<td>').appendTo($tr);
        const $input = $('<input>', {
            checked: state[String(key)].added,
            id: `added${key}`,
            'data-id': key,
            type: "checkbox",
            on: {change: inputHandler}
        }).appendTo($tdControler);
        
         
    });
};



jQuery(document).ready(function() {
    
    $.get("/products/api/add_inv/", function(data) {
        data.forEach((product) => {
            state[product['name']] = product;
        });
        Object.keys(state).forEach((key) => {
            state[key]['added'] = false;
        });
        render();
    });
    
});