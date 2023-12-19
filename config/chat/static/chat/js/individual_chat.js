$(document).ready(function() {
    function sendMessage() {
        var messageContent = $('#message-input').val();
        $.ajax({
          url: "{% url 'send_message' conversation.id %}",
          type: 'POST',
          data: { 'content': messageContent, csrfmiddlewaretoken: '{{ csrf_token }}' },
          success: function(data) {
            $('#message-input').val('');
          },
        });
      }
    
      setInterval(updateMessages, 5000);
    
      function updateMessages() {
        $.ajax({
          url: "{% url 'update_messages' conversation.id %}",
          success: function(data) {
            $("#message-list").html(data);
          },
        });
      }
});