$(document).ready(function() {
    formatFileName();
    $( ".delete-blog" ).click(deleteBlog);
});

// document.getElementsByClassName("delete-blog").style.backgroundColor = "red";

function formatFileName() {
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
            if (fileNameLen < 20) formattedName = fileStr.substr(startIndex, fileNameLen);
            else
                formattedName = fileStr.substr(startIndex, 21);
            if (fileNameLen > 20) formattedName += ' ...';
        } else {
            formattedName = fileStr.substr(startIndex);
        }
        
        $(this).html(formattedName);
    });
}

function deleteBlog() {
    console.log('deleteBlog accessed.')
    let prevSib = $(this).prev();
    while(!prevSib.hasClass('blog-title')) {
        prevSib = prevSib.prev();
    }
    
    let title = prevSib.text();
    console.log(`title = ${title}`)

    $('.modal').addClass('is-active ');
    data = {'csrfmiddlewaretoken': csrfToken, 'blog_title': title};
    // $.post(`delete_blog/`, data).done( function() {
    //     location.reload();
    // });
}

