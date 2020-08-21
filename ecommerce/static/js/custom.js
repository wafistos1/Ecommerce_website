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