const message_display = document.querySelector('#message');

if (message_display){

    setTimeout(() => {
        message_display.classList.remove('alert');
        message_display.innerHTML = '';
    }, 3000);
}