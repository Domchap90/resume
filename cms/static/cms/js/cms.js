// import bulmaCalendar from '/bulma-calendar/dist/js/bulma-calendar.min';

$(document).ready( function() {
    $('#blog_content_form p:first-child').addClass('file');
    $('#blog_content_form p:first-child label').addClass('file-label');
    $('#blog_content_form p:first-child input').addClass('file-input');
    formatFileName();
    var calendars = bulmaCalendar.attach('[type="date"]', options);

// Loop on each calendar initialized
for(var i = 0; i < calendars.length; i++) {
	// Add listener to date:selected event
	calendars[i].on('select', date => {
		console.log(date);
	});
}

// To access to bulmaCalendar instance of an element
var element = document.querySelector('#blog_post_date');
if (element) {
	// bulmaCalendar instance is available as element.bulmaCalendar
	element.bulmaCalendar.on('select', function(datepicker) {
		console.log(datepicker.data.value());
	});
}
});

function formatFileName() {
    console.log("formatFileName function entered.")
    $(".file-name-display").each(function() {
        let fileStr = $(this).html();
        let startIndex = fileStr.lastIndexOf("/")+1;
        let fileNameLen = fileStr.length - startIndex;
        var formattedName;

        if ($(window).width () < 769) {
            if (fileNameLen < 10) formattedName = fileStr.substr(startIndex, fileNameLen);
            else
                formattedName = fileStr.substr(startIndex, 10);
            if (fileNameLen > 10) formattedName += ' ...';
        } else if ($(window).width () < 1024) {
            console.log(`fileStr = ${fileStr}, fileNameLen = ${fileNameLen}`)
            if (fileNameLen < 20) formattedName = fileStr.substr(startIndex, fileNameLen);
            else
                formattedName = fileStr.substr(startIndex, 21);
            if (fileNameLen > 20) formattedName += ' ...';
            console.log(`formattedName = ${formattedName}`)
        } else {
            formattedName = fileStr.substr(startIndex);
        }
        console.log(`formattedName is ${formattedName}`)
        $(this).html(formattedName);
    });
}

function deleteBlog() {
    const blogRow = $(this).parent().id();
    console.log(`blogRow = ${blogRow}`)
    $.ajax({
        type: 'POST',
        url: `delete_blog/`,
        data: {'blog_title': title},
        dataType: 'json',
        success: function(response) {
            
        }
    });