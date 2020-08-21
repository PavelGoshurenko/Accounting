


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
    const name = $('#invoiceName').val();
    const sendData = {};
    sendData['name'] = name;
    const incomings = {};
    Object.keys(state).filter((key) => (state[key].quantity !== 0)).forEach((key) => {
        incomings[key] = state[key];
    });
    sendData['incomings'] = incomings;
    //отправим JSON
    $.ajax({
        type: "POST",
        //url: "products/invoice/new/",
        data: {request: $.toJSON(sendData), csrfmiddlewaretoken: getCookie('csrftoken')},
        success: function(res) {
            window.location.href = '/products/invoices/';
        }
    });
};

const inputHandler = (e) => {
    const id = $(e.target).attr('data-id');
    $input = $(e.target);
    state[String(id)].quantity = Number($input.val());
    //$input.val(state[String(id)].quantity);
    //render(state);
};

const priceHandler = (e) => {
    const id = $(e.target).attr('data-id');
    $input = $(e.target);
    state[String(id)].purchase_price = Number($input.val());
    //render(state);
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
const $div = $('<div>').appendTo('#main-data');
$('<input>', {
    id: 'invoiceName',
    type: "text",
}).appendTo($div);
$('<input>', {
           value: 'Сохранить',
           type: 'submit',
           on: {click: submit}
        }).appendTo($div);
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
    $('<thead><tr><th>Товар</th><th>Куплено на склад</th><th>Цена покупки</th></tr></thead>').appendTo($mainTable);
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
           value: state[String(key)].quantity,
           id: `quantity${key}`,
           'data-id': key,
           type: "number",
           size: 1,
           on: {change: inputHandler}
        }).appendTo($tdControler);
        const $tdPrice = $('<td>').appendTo($tr);
        const $price = $('<input>', {
            value: state[String(key)].purchase_price,
            'data-id': key,
            type: "number",
            size: 1,
            on: {change: priceHandler}
         }).appendTo($tdPrice);
    });
};



jQuery(document).ready(function() {
    render(state);
});