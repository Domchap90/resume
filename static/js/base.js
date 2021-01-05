$('#burger_button').click(toggleNavMenu);

function toggleNavMenu() {
    if ($('#burger_button').hasClass('is-active')){
        $('#burger_button').removeClass('is-active');
        $('#navMenuTouch').removeClass('is-active');
    } else {
        $('#burger_button').addClass('is-active');
        $('#navMenuTouch').addClass('is-active');
    }
}