// chat/static/chat/scripts/rooms.js

$(function() {
  // Reference to the chat messages area
  let $chatWindow = $("#messages");

  // Our interface to the Chat client
  let chatClient;

  // A handle to the room's chat channel
  let roomChannel;

  // The server will assign the client a random username - stored here
  let username;

  // Helper function to print info messages to the chat window
  function print(infoMessage, asHtml) {
    let $msg = $('<div class="info">');
    if (asHtml) {
      $msg.html(infoMessage);
    } else {
      $msg.text(infoMessage);
    }
    $chatWindow.append($msg);
  }

// Helper function to print chat message to the chat window
 function printMessage(fromUser, message) {
   let $user = $('<span class="username">').text(fromUser + ":");
   if (fromUser === username) {
     $user.addClass("me");
   }
   let $message = $('<span class="message">').text(message);
   let $container = $('<div class="message-container">');
   $container.append($user).append($message);
   $chatWindow.append($container);
   $chatWindow.scrollTop($chatWindow[0].scrollHeight);
 }

  // Get an access token for the current user, passing a device ID
  // for browser-based apps, we'll just use the value "browser"
  $.getJSON(
    "/token",
    {
      device: "browser"
    },
    function(data) {
      // Alert the user they have been assigned a random username
      username = data.identity;
      print(
        "You have been assigned a random username of: " +
          '<span class="me">' +
          username +
          "</span>",
        true
      );

      // Initialize the Chat client
      Twilio.Chat.Client.create(data.token).then(client => {
        // Use client
        chatClient = client;
      });

    }
  );
});
