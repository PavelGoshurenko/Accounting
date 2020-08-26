


// дополнительный state - так получилось - больше так не делать
filterState = {
    'category': 1,
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
    // sendData['name'] = name;
    const sales = {};
    Object.keys(state).filter((key) => (state[key].quantity !== 0)).forEach((key) => {
        sales[key] = state[key];
    });
    sendData['sales'] = sales;
    //отправим JSON
    $.ajax({
        type: "POST",
        //url: "products/invoice/new/",
        data: {request: $.toJSON(sendData), csrfmiddlewaretoken: getCookie('csrftoken')},
        success: function(res) {
            if (window.location.pathname.substr(-4) === 'shop') {
                window.location.href = '/products/sales/today/shop';
            }
            else {
                window.location.href = '/products/sales/today/internet';
            }
            
        }
    });
};

const inputHandler = (e) => {
    const id = String($(e.target).attr('data-id'));
    $input = $(e.target);
    state[id].quantity = Number($input.val());
    if (state[id].quantity === 0 && state[id].discount !== 0) {
        alert('Нельзя делать скидку на непроданный товар');
        state[id].discount = 0;
    }
    render(state);
};

const discountHandler = (e) => {
    const id = String($(e.target).attr('data-id'));
    $input = $(e.target);
    if (state[id].quantity === 0) {
        alert('Нельзя делать скидку на непроданный товар');
    } else {
        state[id].discount = Number($input.val());
    }
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
    $('<thead><tr><th>Товар</th><th> Количество</th><th>Цена</th><th>Скидка</th><th>Стоимость</th></tr></thead>').appendTo($mainTable);
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
        const $price = $('<div>', {
            text: state[String(key)].shop_price,
            'data-id': key,
         }).appendTo($tdPrice);

        const $tdDiscount = $('<td>').appendTo($tr);
        const $discount = $('<input>', {
            value: state[String(key)].discount,
            'data-id': key,
            type: "number",
            size: 1,
            on: {change: discountHandler}
         }).appendTo($tdDiscount);

        const $tdSum = $('<td>').appendTo($tr);
        const $sum = $('<div>', {
            text: state[String(key)].shop_price * state[String(key)].quantity - state[String(key)].discount,
            'data-id': key,
         }).appendTo($tdSum);
         
    });
};



jQuery(document).ready(function() {
    render(state);
});