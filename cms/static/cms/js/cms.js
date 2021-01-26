$(document).ready(function() {
    formatFileName();
    setupModal();
    $( ".delete-blog" ).click(deleteBlogModal);
    setupFileUpload("upload_new_blog");
    // setupFileUpload("edit_previous_blog");
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

function setupFileUpload(fileId) {
    const fileInput = $('#'+fileId+' input[type=file]');
    fileInput.change(() => {
        if (fileInput.prop('files').length > 0) {
            const fileVal = fileInput.val();
            const startIndex = fileVal.lastIndexOf("\\") + 1;
            const fileNameLen = fileVal.length - startIndex;
            const formattedFile = fileVal.substr(startIndex, fileNameLen);
            $('#'+fileId+' .file-name').text(formattedFile);
        }
    })   
}