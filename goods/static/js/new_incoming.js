

// обработчики
const submit = (e) => {
    const f = 4;
};

/* const minusHandler = (e) => {
    e.preventDefault();
    const id = $(e.target).attr('data-id');
    $input = $(`input[data-id=${id}]`);
    state[String(id)].quantity -= 1;
    $input.val(state[String(id)].quantity);
    //render(state);
};

const plusHandler = (e) => {
    e.preventDefault();
    const id = $(e.target).attr('data-id');
    $input = $(`input[data-id=${id}]`);
    state[String(id)].quantity += 1;
    $input.val(state[String(id)].quantity);
    //render(state);
}; */

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
    render(state);
};

// render
const $div = $('<div>').appendTo('body');
$('<input>', {
    id: 'invoiceName',
    type: "text",
}).appendTo($div);
$('<input>', {
           value: 'Сохранить',
           type: 'submit',
           on: {click: submit}
        }).appendTo($div);
const $mainTable = $('<table>');
$('body').append($mainTable);

const render = (state) => {
    $mainTable.empty();
    $('<tr><th>Товар</th><th>Куплено на склад</th><th>Цена покупки</th></tr>').appendTo($mainTable);
    Object.keys(state).forEach((key) => {
        const $tr = $('<tr>').appendTo($mainTable);
        const $tdName = $(`<td>${state[key].name}</td>`).appendTo($tr);
        const $tdControler = $('<td>').appendTo($tr);
        /* const aMinus = $('<a>', {
            text: ' - ' ,
            href: '#',
            'data-id': key,
            on: {click: minusHandler}
        }).appendTo($tdControler); */
        const $input = $('<input>', {
           value: state[String(key)].quantity,
           id: `quantity${key}`,
           'data-id': key,
           type: "number",
           size: 1,
           on: {change: inputHandler}
        }).appendTo($tdControler);
        /* const aPlus = $('<a>', {
            text: ' + ',
            href: '#',
            'data-id': key,
            on: {click: plusHandler}
        }).appendTo($tdControler); */
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