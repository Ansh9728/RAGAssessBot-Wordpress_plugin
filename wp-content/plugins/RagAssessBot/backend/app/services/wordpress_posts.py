import requests
import json


def get_post_details(post_data):
        
        post = json.loads(post_data)
        
        processed_data = []
        
        for item in post:
            post_details = {
                "title":item['title']['rendered'],
                "content":item['content']['rendered']
            }
            processed_data.append(post_details)

        return processed_data


def fetch_wordpress_posts(site_url):
    full_url = f"{site_url}/wp-json/wp/v2/posts"
    posts_data = requests.get(full_url).text

    posts_details = get_post_details(posts_data)
    return posts_details

