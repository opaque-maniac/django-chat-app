$(document).ready(function() {
    $('.nav-button').forEach(function(button) {
        button.on('click', function() {
            if (this.hasClass('selected')) {
                return;
            } else {
                if (this.hasId('chats')) {
                    $('#new').removeClass('selected');
                    $('#chats').addClass('selected');
                } else {
                    $('#chats').removeClass('selected');
                    $('#new').addClass('selected');
                }
            }
        });
    });
});