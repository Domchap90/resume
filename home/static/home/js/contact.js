$(document).ready(function () {
    const labels = $('#contact_form label');
    const labelArr = [...labels]
    for (let l in labelArr) 
        console.log(`label is ${l.innerHTML} `)
    // labels.forEach( x => console.log($(x).html()));
    $('#contact_form_container p input').addClass('input');
    $('#contact_form_container p textarea').addClass('textarea');
});

