<?php

/**
 * Plugin Name: RAG Bot Application
 * Description: A chatbot that uses Retrieval-Augmented Generation (RAG) and Chain of Thought (CoT) strategy.
 * Version: 1.1
 * Author: Anshu Kumar Singh
 */

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

// Enqueue the CSS and JavaScript file
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

// Create table and store this data into vector database
register_activation_hook(__FILE__, 'langchain_document_table');

function langchain_document_table() {
    global $wpdb;
    $table_name = $wpdb->prefix . "langchain_chunk_documents";
    $charset_collate = $wpdb->get_charset_collate();

    $sql = "CREATE TABLE $table_name (
        id mediumint(9) NOT NULL AUTO_INCREMENT,
        title varchar(255) NOT NULL,
        content longtext NOT NULL,
        source_url varchar(255),
        PRIMARY KEY (id)
    ) $charset_collate;";

    require_once(ABSPATH . "wp-admin/includes/upgrade.php");
    dbDelta($sql);
}

// Create custom WordPress API
add_action('rest_api_init', function() {
    register_rest_route('store_chunk_docs/v1', '/store-document', array(
        'methods' => 'POST',
        'callback' => 'store_document_callback',
        'permission_callback' => '__return_true',
    ));

    register_rest_route('store_chunk_docs/v1', '/get-documents', array(
        'methods' => 'GET',
        'callback' => 'get_documents_callback',
        'permission_callback' => '__return_true',
    ));
});

function store_document_callback(WP_REST_Request $request) {
    global $wpdb;

    // Check if the table exists
    $table_name = $wpdb->prefix . 'langchain_chunk_documents';
    if ($wpdb->get_var("SHOW TABLES LIKE '$table_name'") != $table_name) {
        return new WP_REST_Response('Table does not exist', 500);
    }

    // Get the posted data
    $params = $request->get_json_params();

    // Check for required parameters
    if (empty($params['title']) || empty($params['content']) || empty($params['source_url'])) {
        return new WP_REST_Response('Missing required parameters', 400);
    }

    $title = sanitize_text_field($params['title']);
    $content = wp_kses_post($params['content']);
    $source_url = esc_url_raw($params['source_url']);

    // Insert data into created table
    $table_name = $wpdb->prefix . 'langchain_chunk_documents';
    $result = $wpdb->insert(
        $table_name,
        array(
            'title' => $title,
            'content' => $content,
            'source_url' => $source_url,
        ),
        array('%s', '%s', '%s')
    );

    if ($result === false) {
        return new WP_REST_Response('Error storing document', 500);
    }

    return new WP_REST_Response('Document stored successfully', 200);
}

function get_documents_callback(WP_REST_Request $request) {
    global $wpdb;

    $source_url = esc_url_raw($request->get_param('source_url'));

    // Check if source_url is provided
    if (empty($source_url)) {
        return new WP_REST_Response('source_url parameter is required', 400);
    }

    // Fetch documents matching the source_url
    $table_name = $wpdb->prefix . 'langchain_chunk_documents';
    $results = $wpdb->get_results($wpdb->prepare("SELECT * FROM $table_name WHERE source_url = %s", $source_url), ARRAY_A);

    if (empty($results)) {
        return new WP_REST_Response(null, 404);
    }

    return new WP_REST_Response($results, 200);
}
