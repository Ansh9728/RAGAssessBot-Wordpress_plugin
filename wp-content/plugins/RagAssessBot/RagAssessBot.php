<?php

/**
 * Plugin Name: RAG Bot Application
 * Description: A chatbot that uses Retrieval-Augmented Generation (RAG) and Chain of Thought (CoT) strategy.
 * Version: 1.1
 * Author: Anshu Kumar Singh
 */

if (!defined('ABSPATH')) {
    exit; // Exit If accessed directly
}

// Enqueue the css and javascript file
function rag_bot_scripts() {
    wp_enqueue_script("jquery");

    wp_enqueue_script('rag-bot-script', plugin_dir_url(__FILE__) . 'assets/js/chatbot.js', array('jquery'), '1.1', true);
    wp_enqueue_style('rag-bot-style', plugin_dir_url(__FILE__) . 'assets/css/chatbot.css');

    // Localize the script with new data
    wp_localize_script('rag-bot-script', 'chatbotAjax', array(
        'ajaxurl' => admin_url('admin-ajax.php'),
        'site_url' => get_site_url(),
        
    ));
}

add_action('wp_enqueue_scripts', 'rag_bot_scripts');

// Add the chatbot container to the body
function rag_bot_body_container() {
    include plugin_dir_path(__FILE__) . 'templates/chatbot-template.php';
}
add_action('wp_body_open', 'rag_bot_body_container');
