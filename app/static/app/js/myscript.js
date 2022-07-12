$('#slider1, #slider2, #slider3').owlCarousel({
    rtl: true,
    loop: true,
    margin: 10,
    nav: true,
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 3
        },
        1000: {
            items: 5
        }
    }
})

$('.plus-cart').click(function() {
    console.log("Plus Clicked!!")
    var id = $(this).attr("pid").toString();
    var elm = this.parentNode.children[2];

    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            //console.log(data)
            //console.log("success")
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total-amount').innerText = data.total_amount
            elm.innerText = data.quantity
        }
    })
});

$('.minus-cart').click(function() {
    console.log("Minus Clicked!!")
    var id = $(this).attr("pid").toString();
    var elm = this.parentNode.children[2];
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            //console.log(data)
            //console.log("success")
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total-amount').innerText = data.total_amount
            elm.innerText = data.quantity
        }
    })
});

$('.remove-cart').click(function() {
    console.log("Minus Clicked!!")
    var id = $(this).attr("pid").toString();
    var id1 = 'remove' + id;
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function(data) {
            document.getElementById('amount').innerText = data.amount
            document.getElementById('total-amount').innerText = data.total_amount
            document.getElementById(id1).remove()
        }
    })
});