$(document).ready(function() {
    $('.nav-button').forEach(function(button) {
        if (button.hasClass('selected')) {
            if (button.hasId('chats')) {
                if($('#all-chats-container').hasClass('hidden')) {
                    $('#all-chats-container').removeClass('hidden');
                    $('#new-chat-container').addClass('hidden');
                }
            } else if (button.hasId('new')) {
                if($('#new-chat-container').hasClass('hidden')) {
                    $('#new-chat-container').removeClass('hidden');
                    $('#all-chats-container').addClass('hidden');
                }
            }
        }
    });
});