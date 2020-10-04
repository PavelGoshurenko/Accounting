// обработчики
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const submit = (e) => {
    e.preventDefault();
    $(e.target).attr('disabled', 'disabled');
    const sendData = {};
    const sales = {};
    Object.keys(state).filter((key) => (state[key].quantity !== 0)).forEach((key) => {
        sales[key] = state[key];
    });
    sendData['sales'] = sales;
    let xhr = new XMLHttpRequest();
    let url = document.location.href;
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            if (window.location.pathname.substr(-4) === 'shop') {
                window.location.href = '/products/sales/today/shop';
            }
            else {
                window.location.href = '/products/sales/today/internet';
            }
        }
    };
    xhr.send($.toJSON(sendData));
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

filterState = {
    'category': 1,
    'brand': '',
}
$('<input>', {
    value: 'Сохранить',
    type: 'submit',
    class: 'btn btn-secondary',
    on: {click: submit}
 }).appendTo($('#submit_button'));
const $tabDiv = $('<div>', {class: 'table-responsive'}).appendTo('#main-data');
const $mainTable = $('<table>', {
    class: "table table-striped table-sm",
    }).appendTo($tabDiv);
$('#main-data').append($tabDiv);
$categorySelector = $('select[name=category]');
$categorySelector.change(categoryChangeHandler);
$brandSelector = $('select[name=brand]');
$brandSelector.change(brandChangeHandler);
$('<thead><tr><th>Товар</th><th> Количество</th><th>Цена</th><th>Скидка</th><th>Стоимость</th></tr></thead>').appendTo($mainTable);
const $tbody = $('<tbody>', {class: 'table-striped'}).appendTo($mainTable);

const render = (state) => {
    $categorySelector.val(filterState.category);
    $brandSelector.val(filterState.brand);
    $tbody.empty();
    let keysToShow = Object.keys(state)
    if (filterState.category) {
        keysToShow = keysToShow.filter((key) => state[key].category === Number(filterState.category))
    }
    if (filterState.brand) {
        keysToShow = keysToShow.filter((key) => state[key].brand === Number(filterState.brand))
    }
    keysToShow.forEach((key) => {
        const $tr = $('<tr>').appendTo($tbody);
        $(`<td>${state[key].name}</td>`).appendTo($tr);
        const $tdControler = $('<td>').appendTo($tr);
        $('<input>', {
           value: state[String(key)].quantity,
           id: `quantity${key}`,
           'data-id': key,
           type: "number",
           size: 1,
           on: {change: inputHandler}
        }).appendTo($tdControler);
        const $tdPrice = $('<td>').appendTo($tr);
        $('<div>', {
            text: state[String(key)].shop_price,
            'data-id': key,
         }).appendTo($tdPrice);

        const $tdDiscount = $('<td>').appendTo($tr);
        $('<input>', {
            value: state[String(key)].discount,
            'data-id': key,
            type: "number",
            size: 1,
            on: {change: discountHandler}
         }).appendTo($tdDiscount);

        const $tdSum = $('<td>').appendTo($tr);
        $('<div>', {
            text: state[String(key)].shop_price * state[String(key)].quantity - state[String(key)].discount,
            'data-id': key,
         }).appendTo($tdSum);
         
    });
};


jQuery(document).ready(function() {
    render(state);
});