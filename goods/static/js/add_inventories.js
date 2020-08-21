


// дополнительный state - так получилось - больше так не делать
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
    render(state);
};

const categoryChangeHandler = (e) => {
    filterState.category = e.target.value
    render(state);
}

const brandChangeHandler = (e) => {
    filterState.brand = e.target.value
    render(state);
}
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

const render = (state) => {
    $categorySelector.val(filterState.category);
    $brandSelector.val(filterState.brand);
    $mainTable.empty();
    $('<thead><tr><th>Товар</th><th>Добавить</th></tr></thead>').appendTo($mainTable);
    const $tbody = $('<tbody>', {class: 'table-striped'}).appendTo($mainTable);
    let keysToShow = Object.keys(state)
    if (filterState.category) {
        keysToShow = keysToShow.filter((key) => state[key].category === Number(filterState.category))
    }
    if (filterState.brand) {
        keysToShow = keysToShow.filter((key) => state[key].brand === Number(filterState.brand))
    }
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
    render(state);
});