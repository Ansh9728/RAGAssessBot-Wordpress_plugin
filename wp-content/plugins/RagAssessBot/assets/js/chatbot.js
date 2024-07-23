
jQuery(document).ready(function($) {
    const chatbotContainer = $('#chatbot-container');
    const chatbotIcon = $('#chatbot-icon');
    const chatInterface = $('#chat-interface');
    const userInput = $('#user-input');
    const sendButton = $('#send-button');
    const chatLog = $('#chat-log');

    // Toggle chat interface on icon click
    chatbotIcon.on('click', function() {
        chatInterface.toggle();
        chatbotContainer.toggleClass('active');
    });

    // Handle user input submission
    function sendMessage() {
        const userMessage = userInput.val().trim();

        // Check for empty message before sending
        if (userMessage === "") {
            return; // Exit function if message is empty
        }

        // Display user message
        const userMessageElement = $('<div>').addClass('user-message').text(userMessage);
        console.log(userMessage);
        chatLog.append(userMessageElement);

        // Clear input field
        userInput.val('');

        // Send the user message to the backend
        $.ajax({
            url: 'chatbotAjax.ajaxurl',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({
                // action: 'rag_cot_chatbot_query',
                query: userMessage,
                context:""
            }),
            success: function(response) {
                console.log(userMessage);
                if (response.success) {
                    const botMessage = response.data.response;
                    const botMessageElement = $('<div>').addClass('bot-message').text(botMessage);
                    chatLog.append(botMessageElement);
                    chatLog.scrollTop(chatLog.prop("scrollHeight"));
                } else {
                    const botMessageElement = $('<div>').addClass('bot-message').text('Error: ' + response.data.message);
                    chatLog.append(botMessageElement);
                }
            },
            error: function(xhr, status, error) {
                const botMessageElement = $('<div>').addClass('bot-message').text('Error communicating with the server.');
                chatLog.append(botMessageElement);
                console.error('Error:', error);
                console.error('Status:', status);
                console.error('XHR:', xhr);
            },

        });
    }

    // Handle both button click and Enter key press
    sendButton.on('click', sendMessage);
    userInput.on('keypress', function(e) {
        if (e.which === 13) {
            sendMessage();
            return false; // Prevent default form submission
        }
    });
});
