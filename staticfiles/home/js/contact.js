$(document).ready(function () {
     $('#contact_form label').each( function() {
        const label = $(this).text();
        $(this).text(label.substr(0, label.length-1));
     });
   
    $('#contact_form_container p input').addClass('input');
    $('#contact_form_container p textarea').addClass('textarea');
});

