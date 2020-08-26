$(document).on('click', '.icon_icon', function (event) {

    event.preventDefault();


    $.ajax({
        url: $(this).attr('href'),
        type: 'POST',
        data: {

            val: $(this).attr('name'),
            pk: $(this).attr('href'),

        },
        dataType: 'json',
        success: function (response) {

            if (response['etat'] == true) {
                $('.icon_icon span').toggleClass('icon_heart icon_heart_alt');
            }
            else {
                $('.icon_icon span').toggleClass('icon_heart_alt icon_heart');
            }

        },
        error: function (rs, e) {
            console.log(rs);
        }
    });

});


$(document).on('click', '.cart-btn', function (event) {

    event.preventDefault();


    let id = $(this).attr('name');
    let url = $(this).attr('href');
    

    $.ajax({
        url: $(this).attr('href'),
        type: 'POST',
        data: {

            pk: id,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        dataType: 'json',
        success: function (response) {
            
            var html = ' <p>Added item <strong>' + response.item_title + '</strong> to cart.</p>'
            $('.modal-body').html(html);
            $('.myModalt').modal('show');
             	

            $( "div.tip" ).replaceWith( "<div class='tip'>" + response.count + "</div>" );
            
                
        },
        error: function (rs, e) {
            console.log(rs);
        }
    });




});

$('#header__right__widget').mouseenter(function (event){
   
    
    $.ajax({
        url: '/cart_list/',
        type: 'POST',
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
        },
        dataType: 'json',
        success: function (response) {
            
            $( "div.tip" ).replaceWith( "<div class='tip'>" + response.count + "</div>" );
        },
        error: function (rs, e) {
            // alert('error')
        }
    });

});