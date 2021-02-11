$(document).ready(function() {
    $('.edit-row').hide();
    $('.edit-btn').click(function(){
    /* Creates accordian effect where only one row's details can be viewed at
    a time */
        let editRowId = $(this).parent().next().attr('id');
        console.log(`editRowId = ${editRowId}`)
        // Allows the single viewed row to be closed so all rows are hidden
        $('.edit-row:not(#'+editRowId+')').hide();
        $(`#${editRowId}`).toggle();
    });

    formatFileNameInTable();
    setupModal();
    $( ".delete-blog" ).click(deleteBlogModal);
    $('tbody tr form .file').each((i, el) => setupFileUpload($(el).attr('id')));
    setupFileUpload("upload_new_blog");
    const blog47 = $('#blog_edit_form_47 input[type="date"]');
    $('#blog_edit_form_47 .datetimepicker-dummy-input.is-datetimepicker-range').val('01/21/2008');
    
    $('#add_sub_form label').each( function() {
        const label = $(this).text();
        $(this).text(label.substr(0, label.length-1));
    });
   
    $('.sub_content_form p input').addClass('input');

    $('.errorlist li').addClass('help is-danger');
    // bulmaCalendar.attach(blog47, {startDate: new Date('10/24/2019')});
});

// document.getElementsByClassName("delete-blog").style.backgroundColor = "red";

function formatFileNameInTable() {
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
    const fileInputElement = $('#'+fileId+' input[type=file]');
    if (fileId.includes("edit_previous_blog")){
        formatFileNameInUpload(fileId, fileInputElement);
    }
    fileInputElement.change(() => {
        formatFileNameInUpload(fileId, fileInputElement);
    });   
}

function formatFileNameInUpload(fileId, fileInput) {
    let fileVal = fileInput.val();   
    let startIndex;
    if (fileInput.prop('files').length > 0) {
        startIndex = fileVal.lastIndexOf("\\") + 1;
        
    } else if (fileId.includes('edit_previous_blog')) {
        fileVal = $(`#${fileId} .file-name`).html();
        startIndex = fileVal.lastIndexOf("/") + 1;
    }    
    const fileNameLen = fileVal.length - startIndex;
    const formattedFile = fileVal.substr(startIndex, fileNameLen);
    $('#'+fileId+' .file-name').text(formattedFile);
}