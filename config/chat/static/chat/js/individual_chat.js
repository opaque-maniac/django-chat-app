$(document).ready(function() {
    function sendMessage() {
        var messageContent = $('#message-input').val();
        $.ajax({
          url: "{% url 'send_message' conversation.id %}",
          type: 'POST',
          data: { 'content': messageContent, csrfmiddlewaretoken: '{{ csrf_token }}' },
          success: function(data) {
            // Optionally handle success response
            // For example, clear the input field
            $('#message-input').val('');
          },
        });
      }
    
      // Update messages every 5 seconds (adjust as needed)
      setInterval(updateMessages, 5000);
    
      // Function to update messages
      function updateMessages() {
        $.ajax({
          url: "{% url 'update_messages' conversation.id %}",
          success: function(data) {
            // Update the message list with new messages
            $("#message-list").html(data);
          },
        });
      }
});