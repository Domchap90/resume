const messages = document.getElementById('message_container').childNodes;

bulmaToast.setDefaults({
    dismissible: true,
    duration: 30000,
    position: "bottom-right"
});

for (let m of messages) {
    if (m.nodeName === 'P') {

        let msg = m.textContent;
        msg = highlightEmail(msg);

        if (m.classList.contains('success')) {

            bulmaToast.toast({
                message: msg,
                type: 'is-success',

            });

        } else {
            msg = firstSentenceOnly(msg);
            bulmaToast.toast({
                message: msg,
                type: 'is-danger',
            });

        }
    }
}

function highlightEmail(stringWithEmail) {
    const emailFormat = /([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})/;
    const emailIndex = stringWithEmail.search(emailFormat);
    const email = stringWithEmail.match(emailFormat)[0];
    const emailLen = email.length;

    let adjustedString = stringWithEmail;

    if (emailIndex !== -1) {
        adjustedString = stringWithEmail.slice(0, emailIndex) + `<strong>`
        + email + `</strong>` + stringWithEmail.slice(emailIndex+emailLen);
    }

    return adjustedString;
}
   
function firstSentenceOnly(string) {
    const periodIndex = string.search(/\.\s/);
    let firstSentence = string;
    
    if (periodIndex !== -1) {
        firstSentence = string.slice(0, periodIndex+1);
    }

    return firstSentence;
}