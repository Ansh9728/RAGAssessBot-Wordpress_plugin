
<div id="chatbot-container" class="closed">
    <div id="chatbot-header">
        <img src="<?php echo plugin_dir_url(__FILE__) . '../assets/img/agent-01.png'; ?>" alt="Chatbot Icon" id="chatbot-icon">
    </div>
    <div id="chat-interface" style="display: none;">
        <div id="chat-log"></div>
        <div id="chat-input-container">
            <input type="text" id="user-input" placeholder="Type your message here..."/>
            <button id="send-button">Send</button>
        </div>
    </div>
</div>
