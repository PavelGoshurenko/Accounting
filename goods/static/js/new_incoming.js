let state = {};
START_CATEGORY = '5';

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
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
        data: {request: $.toJSON(sendData), csrfmiddlewaretoken: getCookie('csrftoken')},
        success: function(res) {
            window.location.href = '/products/invoices/';
        }
    });
};

const inputHandler = (e) => {
    const id = $(e.target).attr('data-id');
    $input = $(e.target);
    state[id].quantity = Number($input.val());
};

const brandFilter = (category) => {
    const brands = {};
    $('select[name=brand]').children().each(function (index, value){
        brands[$(this).val()] = 0;
      });
    let keysToShow = Object.keys(state);
    if (category !== '') {
        keysToShow = keysToShow.filter((key) => state[key].category === Number(category));
    }
    keysToShow.forEach((key) => {
        if (state[key].brand !== null) {
            brands[state[key].brand.toString()] += 1;
        }
    });
    Object.keys(brands).forEach((brand) => {
        if (brands[brand] > 0 || brand === '') {
            $('select[name=brand] option[value="'+ brand +'"]').show();
        } else {
            $('select[name=brand] option[value="'+ brand +'"]').hide();
        }
    });
};

const categoryChangeHandler = (e) => {
    const category = e.target.value;
    filterState.category = category;
    filterState.brand = '';
    brandFilter(category);
    render();
}

const brandChangeHandler = (e) => {
    filterState.brand = e.target.value
    render();
}
// render

filterState = {
    'category': START_CATEGORY,
    'brand': '',
}
brandFilter(START_CATEGORY);
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

const render = () => {
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
        $(`<td>${key}</td>`).appendTo($tr);
        const $tdControler = $('<td>').appendTo($tr);
        const $input = $('<input>', {
           value: state[key].quantity,
           id: `quantity${key}`,
           'data-id': key,
           type: "number",
           size: 1,
           on: {change: inputHandler}
        }).appendTo($tdControler);
        $(`<td>${state[key].purchase_price}</td>`).appendTo($tr);
    });
};



jQuery(document).ready(function() {
    
    $.get("/products/api/", function(data) {
        data.forEach((product) => {
            state[product['name']] = product;
        });
        Object.keys(state).forEach((key) => {
            state[key]['quantity'] = 0;
        });
        render();
    });
    
});