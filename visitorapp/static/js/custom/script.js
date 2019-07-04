$('#trades').click(function() {
    $.ajax({
        type: 'GET',
        url: '/',
        success: function(data, textStatus) {
            // alert(data, textStatus);
            $('#all-trades').html(data); // append to inner html
        },
        error: function(xhr, status, e) {
            alert(status, e);
        } 
    });
});
