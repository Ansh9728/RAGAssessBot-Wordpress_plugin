import requests


def fetch_wordpress_posts_data(site_url):
    full_url = f"{site_url}/wp-json/wp/v2/posts"
    posts_data = requests.get(full_url).text
    return posts_data
