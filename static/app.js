$(document).ready(function() {
    const socket = io();

    $('#send-button').click(function() {
        const userInput = $('#user-input').val();
        if (userInput) {
            $('#chat-box').append(`<div class="message user">${userInput}</div>`);
            socket.emit('message', { message: userInput });
            $('#user-input').val('');
        }
    });

    socket.on('response', function(data) {
        $('#chat-box').append(`<div class="message bot">${data.message}</div>`);
        $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
    });

    $('#user-input').keypress(function(event) {
        if (event.which == 13) {
            $('#send-button').click();
        }
    });
});
