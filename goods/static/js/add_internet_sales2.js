// обработчики
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
            window.location.href = '/products/sales/today/internet';
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
    render();
};

const discountHandler = (e) => {
    const id = String($(e.target).attr('data-id'));
    $input = $(e.target);
    if (state[id].quantity === 0) {
        alert('Нельзя делать скидку на непроданный товар');
    } else {
        state[id].discount = Number($input.val());
    }
    render();
};

const categoryChangeHandler = (e) => {
    const category = e.target.value;
    filterState.category = category;

    let keysToShow = Object.keys(state);
    const brands = {};
    /* keysToShow.forEach((key) => {
        if (state[key].brand !== null) {
            brands[state[key].brand] = 0;
        }
    }); */
    $('select[name=brand]').children().each(function(val){
        brands[val] = 0;
     })
    if (category) {
        keysToShow = keysToShow.filter((key) => state[key].category === Number(category));
    }
    //console.log(keysToShow);
    keysToShow.forEach((key) => {
        if (state[key].brand !== null) {
            console.log(state[key].brand);
            brands[state[key].brand] += 1;
        }
    });
    console.log(brands);
    Object.keys(brands).forEach((brand) => {
        if (brands[brand]) {
            $('select[name=brand] option[value="'+ brand.toString() +'"]').show();
        } else {
            $('select[name=brand] option[value="'+ brand.toString() +'"]').hide();
        }
    });
    


    render();
}

const brandChangeHandler = (e) => {
    filterState.brand = e.target.value
    render();
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

const render = () => {
    $categorySelector.val(filterState.category);
    $brandSelector.val(filterState.brand);
    $tbody.empty();
    let keysToShow = Object.keys(state);
    if (filterState.category) {
        keysToShow = keysToShow.filter((key) => state[key].category === Number(filterState.category));
    }
    if (filterState.brand) {
        keysToShow = keysToShow.filter((key) => state[key].brand === Number(filterState.brand));
    }
    keysToShow.forEach((key) => {
        const $tr = $('<tr>').appendTo($tbody);
        $(`<td>${key}</td>`).appendTo($tr);
        const $tdControler = $('<td>').appendTo($tr);
        $('<input>', {
           value: state[key].quantity,
           id: `quantity${key}`,
           'data-id': key,
           type: "number",
           size: 1,
           on: {change: inputHandler}
        }).appendTo($tdControler);
        const $tdPrice = $('<td>').appendTo($tr);
        $('<div>', {
            text: state[key].internet_price,
            'data-id': key,
         }).appendTo($tdPrice);

        const $tdDiscount = $('<td>').appendTo($tr);
        $('<input>', {
            value: state[key].discount,
            'data-id': key,
            type: "number",
            size: 1,
            on: {change: discountHandler}
         }).appendTo($tdDiscount);

        const $tdSum = $('<td>').appendTo($tr);
        $('<div>', {
            text: state[String(key)].internet_price * state[key].quantity - state[key].discount,
            'data-id': key,
         }).appendTo($tdSum);
         
    });
};

let state = {};

jQuery(document).ready(function() {
    
    $.get("/products/api/", function(data) {
        data.forEach((product) => {
            state[product['name']] = product;
        });
        Object.keys(state).forEach((key) => {
            state[key]['quantity'] = 0;
            state[key]['discount'] = 0;
        });
        render();
    });
    
});