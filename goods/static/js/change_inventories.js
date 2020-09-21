


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
    sendData['inventories'] = state;
    //отправим JSON
    $.ajax({
        type: "POST",
        data: {request: $.toJSON(sendData), csrfmiddlewaretoken: getCookie('csrftoken')},
        success: function(res) {
            window.location.href = '/products/inventories_result/';
        }
    });
};

const inputHandler = (e) => {
    const id = String($(e.target).attr('data-id'));
    $input = $(e.target);
    state[id].fact_quantity = Number($input.val());
    render(state);
};


// render

const $tabDiv = $('<div>', {class: 'table-responsive'}).appendTo('#main-data')
const $mainTable = $('<table>', {
    class: "table table-striped table-sm",
}).appendTo($tabDiv);
$('<input>', {
    value: 'Сохранить',
    type: 'submit',
    class: 'btn btn-secondary',
    on: {click: submit}
 }).appendTo($('#main-data'));

const render = (state) => {
    $mainTable.empty();
    $('<thead><tr><th>Товар</th><th>Бренд</th><th>Ожидаемое количество</th><th>Факт</th><th>Незадача</th></thead>').appendTo($mainTable);
    const $tbody = $('<tbody>', {class: 'table-striped'}).appendTo($mainTable);
    const keysToShow = Object.keys(state)
    keysToShow.forEach((key) => {
        const $tr = $('<tr>').appendTo($tbody);
        const $tdName = $(`<td>${state[key].name}</td>`).appendTo($tr);
        const $tdBrand = $(`<td>${state[key].brand}</td>`).appendTo($tr);
        const $tdSupposed = $('<td>').appendTo($tr);
        const $supposed = $('<div>', {
            text: state[String(key)].supposed_quantity,
            'data-id': key,
         }).appendTo($tdSupposed);

        const $tdFact = $('<td>').appendTo($tr);
        const $input = $('<input>', {
           value: state[String(key)].fact_quantity,
           id: `fact_quantity${key}`,
           'data-id': key,
           type: "number",
           size: 1,
           on: {change: inputHandler}
        }).appendTo($tdFact);

        const $tdShortage = $('<td>').appendTo($tr);
        const $shortage = $('<div>', {
            text: state[String(key)].supposed_quantity - state[String(key)].fact_quantity,
            'data-id': key,
         }).appendTo($tdShortage);
         
    });
};



jQuery(document).ready(function() {
    render(state);
});