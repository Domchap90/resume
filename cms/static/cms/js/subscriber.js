$(document).ready(function() {
    console.log("subscriber js accessed.")
    $('#add_sub_form label').each( function() {
        const label = $(this).text();
        $(this).text(label.substr(0, label.length-1));
    });
   
    $('.sub-content-form p input').addClass('input');

    $('.errorlist li').addClass('help is-danger');
});