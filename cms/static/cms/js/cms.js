$(document).ready(function() {
    formatFileName();
    setupModal();
    $( ".delete-blog" ).click(deleteBlogModal);
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

function setupModal() {
    $('.modal-close, .modal-cancel').click(() => $('.modal').removeClass('is-active'));

}

function deleteBlogModal() {
    console.log('deleteBlog accessed.')
    let prevSib = $(this).prev();
    while(!prevSib.hasClass('blog-title')) {
        prevSib = prevSib.prev();
    }
    
    let title = prevSib.text();
    $('.insert-title').html(title);

    $('.modal').addClass('is-active ');
    $(".modal-confirm").click(() => deleteBlog(title));
}

function deleteBlog(titleOfBlogToDelete) {
    data = {'csrfmiddlewaretoken': csrfToken, 'blog_title': titleOfBlogToDelete};
    $.post(`delete_blog/`, data).done( function() {
        location.reload();
    });
}
